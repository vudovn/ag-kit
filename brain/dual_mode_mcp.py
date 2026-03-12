"""
🔄 LUNA Dual Mode MCP Server

Supports both stdio mode (for IDEs like Cursor/VSCode) and HTTP mode (REST API).

Feature Flag: FEATURE_DUAL_MODE_MCP

Usage:
    # stdio mode (IDE integration)
    python3 -m brain.runtime
    
    # HTTP mode (REST API)
    python3 -m brain.runtime --mode http --port 3000
"""

import os
import sys
import asyncio
import json
from typing import Optional, Dict, Any
from enum import Enum


class RuntimeMode(Enum):
    """Runtime operation mode"""
    STDIO = "stdio"      # IDE integration (Claude Code, Cursor)
    HTTP = "http"        # REST API mode
    BOTH = "both"        # Both modes simultaneously


class DualModeMCP:
    """
    Dual Mode MCP Server for LUNA Brain.
    
    Features:
    - stdio mode for IDE integration
    - HTTP mode for REST API
    - Automatic mode detection
    - Swagger UI in HTTP mode
    - Health check endpoint
    
    Usage:
        # Auto-detect mode
        mcp = DualModeMCP()
        await mcp.run()
        
        # Force HTTP mode
        mcp = DualModeMCP(mode=RuntimeMode.HTTP, port=3000)
        await mcp.run()
    """
    
    def __init__(
        self,
        mode: Optional[RuntimeMode] = None,
        host: str = "0.0.0.0",
        port: int = 3000
    ):
        """
        Initialize Dual Mode MCP.
        
        Args:
            mode: Operation mode (auto-detected if None)
            host: HTTP server host
            port: HTTP server port
        """
        self.mode = mode or self._detect_mode()
        self.host = host
        self.port = port
        
        # Import dependencies lazily
        self._fastapi_app = None
        self._stdio_streams = None
    
    def _detect_mode(self) -> RuntimeMode:
        """Auto-detect operation mode from environment"""
        # Check command line args
        if len(sys.argv) > 1:
            if "--mode" in sys.argv:
                idx = sys.argv.index("--mode")
                mode_str = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "stdio"
                return RuntimeMode(mode_str)
            elif "--http" in sys.argv:
                return RuntimeMode.HTTP
        
        # Check environment variable
        env_mode = os.getenv("DUAL_MODE_DEFAULT", "stdio")
        return RuntimeMode(env_mode)
    
    async def run(self):
        """Run MCP server in detected mode"""
        if self.mode == RuntimeMode.STDIO:
            await self._run_stdio()
        elif self.mode == RuntimeMode.HTTP:
            await self._run_http()
        elif self.mode == RuntimeMode.BOTH:
            await self._run_both()
    
    async def _run_stdio(self):
        """Run in stdio mode for IDE integration"""
        from mcp.server.stdio import stdio_server
        from mcp.server import Server
        
        print("🔄 Starting LUNA Brain in STDIO mode...", file=sys.stderr)
        
        # Create MCP server
        server = Server("luna-brain")
        
        # Register tools
        @server.list_tools()
        async def list_tools():
            return [
                {
                    "name": "get_contact",
                    "description": "Get contact from CRM with smart caching",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "contact_id": {"type": "string"}
                        },
                        "required": ["contact_id"]
                    }
                },
                {
                    "name": "check_handoff",
                    "description": "Check if conversation needs human handoff",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "conversation_id": {"type": "string"}
                        },
                        "required": ["conversation_id"]
                    }
                },
                {
                    "name": "get_cache_stats",
                    "description": "Get smart cache statistics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "get_contact":
                from brain.cache import contact_cache
                contact_id = arguments.get("contact_id")
                contact = contact_cache.get(contact_id)
                return {"contact": contact}
            
            elif name == "check_handoff":
                from brain.handoff import handoff_engine
                conversation_id = arguments.get("conversation_id")
                # Mock conversation for demo
                conversation = {"id": conversation_id}
                should, reason = handoff_engine.should_handoff(conversation)
                return {"should_handoff": should, "reason": str(reason) if reason else None}
            
            elif name == "get_cache_stats":
                from brain.cache import contact_cache
                stats = contact_cache.get_stats()
                return {"stats": stats}
            
            return {"error": f"Unknown tool: {name}"}
        
        # Run server
        async with stdio_server() as (read_stream, write_stream):
            self._stdio_streams = (read_stream, write_stream)
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    async def _run_http(self):
        """Run in HTTP mode for REST API"""
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            import uvicorn
        except ImportError:
            print("❌ FastAPI not installed. Run: pip install fastapi uvicorn", file=sys.stderr)
            sys.exit(1)
        
        print(f"🔄 Starting LUNA Brain in HTTP mode on http://{self.host}:{self.port}", file=sys.stderr)
        
        # Create FastAPI app
        app = FastAPI(
            title="LUNA Brain API",
            description="LUNA Multi-Brain V2 - Dual Mode MCP Server",
            version="2.0.0"
        )
        
        # Add CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Health check
        @app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "mode": "http",
                "version": "2.0.0"
            }
        
        # Stats endpoint
        @app.get("/stats")
        async def get_stats():
            from brain.cache import contact_cache
            from brain.handoff import handoff_engine
            
            return {
                "smart_cache": contact_cache.get_stats(),
                "human_handoff": handoff_engine.get_stats(),
                "feature_flags": {
                    "smart_cache": os.getenv("FEATURE_SMART_CACHE", "true"),
                    "handoff": os.getenv("FEATURE_HANDOFF", "true"),
                    "dual_mode_mcp": os.getenv("FEATURE_DUAL_MODE_MCP", "true")
                }
            }
        
        # Get contact endpoint
        @app.get("/api/v1/contacts/{contact_id}")
        async def get_contact(contact_id: str):
            from brain.cache import contact_cache
            
            contact = contact_cache.get(contact_id)
            if contact is None:
                # Cache miss - would fetch from CRM in production
                raise HTTPException(status_code=404, detail="Contact not found")
            
            return {"contact": contact, "cached": True}
        
        # Check handoff endpoint
        @app.post("/api/v1/conversations/{conversation_id}/handoff")
        async def check_handoff(conversation_id: str, conversation: dict):
            from brain.handoff import check_handoff, create_handoff_request
            
            conversation["id"] = conversation_id
            should, reason = check_handoff(conversation)
            
            result = {"should_handoff": should, "reason": str(reason) if reason else None}
            
            if should:
                request = create_handoff_request(conversation, reason)
                result["handoff_request"] = {
                    "conversation_id": request.conversation_id,
                    "priority": request.priority,
                    "context_summary": request.context_summary
                }
            
            return result
        
        # Cache management
        @app.delete("/api/v1/cache/{contact_id}")
        async def invalidate_cache(contact_id: str):
            from brain.cache import contact_cache
            
            contact_cache.invalidate(contact_id)
            return {"status": "ok", "message": f"Cache invalidated for {contact_id}"}
        
        @app.delete("/api/v1/cache")
        async def clear_cache():
            from brain.cache import contact_cache
            
            contact_cache.clear()
            return {"status": "ok", "message": "Cache cleared"}
        
        # Run server
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    
    async def _run_both(self):
        """Run both stdio and HTTP modes simultaneously"""
        print("🔄 Starting LUNA Brain in BOTH modes...", file=sys.stderr)
        
        # Run HTTP in background
        http_task = asyncio.create_task(self._run_http())
        
        # Run stdio in foreground
        try:
            await self._run_stdio()
        finally:
            http_task.cancel()


# Global singleton
mcp_server = DualModeMCP()


def get_mcp_server() -> DualModeMCP:
    """Get global MCP server instance"""
    return mcp_server


# Feature flag check
def is_dual_mode_enabled() -> bool:
    """Check if dual mode feature is enabled"""
    return os.getenv("FEATURE_DUAL_MODE_MCP", "true").lower() == "true"


# CLI entry point
if __name__ == "__main__":
    if is_dual_mode_enabled():
        asyncio.run(mcp_server.run())
    else:
        print("❌ Dual Mode MCP is disabled", file=sys.stderr)
        sys.exit(1)
