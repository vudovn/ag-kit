#!/usr/bin/env python3
"""
WebSocket event listener for VideoDB with auto-reconnect and graceful shutdown.

Usage:
  python scripts/ws_listener.py [OPTIONS] [output_dir]

Arguments:
  output_dir  Directory for output files (default: /tmp or VIDEODB_EVENTS_DIR env var)

Options:
  --clear     Clear the events file before starting (use when starting a new session)

Output files:
  <output_dir>/videodb_events.jsonl  - All WebSocket events (JSONL format)
  <output_dir>/videodb_ws_id         - WebSocket connection ID
  <output_dir>/videodb_ws_pid        - Process ID for easy termination

Output (first line, for parsing):
  WS_ID=<connection_id>

Examples:
  python scripts/ws_listener.py &                    # Run in background
  python scripts/ws_listener.py --clear              # Clear events and start fresh
  python scripts/ws_listener.py --clear /tmp/mydir   # Custom dir with clear
  kill $(cat /tmp/videodb_ws_pid)                    # Stop the listener
"""
import os
import sys
import json
import signal
import asyncio
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import videodb

# Retry config
MAX_RETRIES = 10
INITIAL_BACKOFF = 1  # seconds
MAX_BACKOFF = 60     # seconds

# Parse arguments
def parse_args():
    clear = False
    output_dir = None
    
    args = sys.argv[1:]
    for arg in args:
        if arg == "--clear":
            clear = True
        elif not arg.startswith("-"):
            output_dir = arg
    
    if output_dir is None:
        output_dir = os.environ.get("VIDEODB_EVENTS_DIR", "/tmp")
    
    return clear, Path(output_dir)

CLEAR_EVENTS, OUTPUT_DIR = parse_args()
EVENTS_FILE = OUTPUT_DIR / "videodb_events.jsonl"
WS_ID_FILE = OUTPUT_DIR / "videodb_ws_id"
PID_FILE = OUTPUT_DIR / "videodb_ws_pid"

# Track if this is the first connection (for clearing events)
_first_connection = True


def log(msg: str):
    """Log with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def append_event(event: dict):
    """Append event to JSONL file with timestamps."""
    event["ts"] = datetime.now(timezone.utc).isoformat()
    event["unix_ts"] = datetime.now(timezone.utc).timestamp()
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def write_pid():
    """Write PID file for easy process management."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))


def cleanup_pid():
    """Remove PID file on exit."""
    try:
        PID_FILE.unlink(missing_ok=True)
    except Exception:
        pass


async def listen_with_retry():
    """Main listen loop with auto-reconnect and exponential backoff."""
    global _first_connection
    
    retry_count = 0
    backoff = INITIAL_BACKOFF
    
    while retry_count < MAX_RETRIES:
        try:
            conn = videodb.connect()
            ws_wrapper = conn.connect_websocket()
            ws = await ws_wrapper.connect()
            ws_id = ws.connection_id
            
            # Ensure output directory exists
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            
            # Clear events file only on first connection if --clear flag is set
            if _first_connection and CLEAR_EVENTS:
                EVENTS_FILE.unlink(missing_ok=True)
                log("Cleared events file")
            _first_connection = False
            
            # Write ws_id to file for easy retrieval
            WS_ID_FILE.write_text(ws_id)
            
            # Print ws_id (parseable format for LLM)
            if retry_count == 0:
                print(f"WS_ID={ws_id}", flush=True)
            log(f"Connected (ws_id={ws_id})")
            
            # Reset retry state on successful connection
            retry_count = 0
            backoff = INITIAL_BACKOFF
            
            # Listen for messages
            async for msg in ws.receive():
                append_event(msg)
                channel = msg.get("channel", msg.get("event", "unknown"))
                text = msg.get("data", {}).get("text", "")
                if text:
                    print(f"[{channel}] {text[:80]}", flush=True)
            
            # If we exit the loop normally, connection was closed
            log("Connection closed by server")
            
        except asyncio.CancelledError:
            log("Shutdown requested")
            raise
        except Exception as e:
            retry_count += 1
            log(f"Connection error: {e}")
            
            if retry_count >= MAX_RETRIES:
                log(f"Max retries ({MAX_RETRIES}) exceeded, exiting")
                break
            
            log(f"Reconnecting in {backoff}s (attempt {retry_count}/{MAX_RETRIES})...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, MAX_BACKOFF)


async def main_async():
    """Async main with signal handling."""
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()
    
    def handle_signal():
        log("Received shutdown signal")
        shutdown_event.set()
    
    # Register signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handle_signal)
    
    # Run listener with cancellation support
    listen_task = asyncio.create_task(listen_with_retry())
    shutdown_task = asyncio.create_task(shutdown_event.wait())
    
    done, pending = await asyncio.wait(
        [listen_task, shutdown_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    log("Shutdown complete")


def main():
    write_pid()
    try:
        asyncio.run(main_async())
    finally:
        cleanup_pid()


if __name__ == "__main__":
    main()
