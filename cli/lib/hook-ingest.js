import fs from "node:fs";
import path from "node:path";
import { recordObservation } from "./observability.js";

const MAX_STDIN_BYTES = 2 * 1024 * 1024;
const MAX_LABEL = 160;
const SUPPORTED = new Set(["antigravity", "codex", "gemini", "cline"]);

const cleanLabel = (value, fallback = "unknown") => {
  const text = String(value || "").trim().slice(0, MAX_LABEL);
  return text ? text.replace(/[^\p{L}\p{N}._:/-]+/gu, "_") : fallback;
};

const existsDir = (dir) => {
  try { return fs.statSync(dir).isDirectory(); } catch { return false; }
};

export function findHookProjectRoot(start = process.cwd()) {
  let current;
  try {
    const resolved = path.resolve(start || process.cwd());
    current = fs.existsSync(resolved) ? fs.realpathSync(resolved) : resolved;
    if (!existsDir(current)) current = path.dirname(current);
  } catch {
    return null;
  }
  while (true) {
    if (existsDir(path.join(current, ".ag-kit"))) return current;
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}

const outcomeFrom = (runtime, payload) => {
  if (runtime === "cline" && typeof payload?.postToolUse?.success === "boolean") return payload.postToolUse.success ? "success" : "error";
  if (payload?.error) return "error";
  const response = payload?.tool_response;
  if (response && typeof response === "object" && (response.error || response.isError === true || response.errorType)) return "error";
  return "observed";
};

export function normalizeHookEvent(runtime, payload = {}) {
  if (!SUPPORTED.has(runtime)) return null;
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;

  let session = "hook";
  let toolName = "unknown";
  let eventName = "tool";
  let durationMs = null;

  if (runtime === "codex") {
    session = payload.session_id || payload.turn_id || "hook";
    toolName = payload.tool_name || "unknown";
    eventName = payload.hook_event_name || "PostToolUse";
  } else if (runtime === "gemini") {
    session = payload.session_id || "hook";
    toolName = payload.tool_name || payload.original_request_name || "unknown";
    eventName = payload.hook_event_name || "AfterTool";
  } else if (runtime === "cline") {
    session = payload.taskId || "hook";
    toolName = payload.postToolUse?.toolName || "unknown";
    eventName = payload.hookName || "PostToolUse";
    if (Number.isFinite(Number(payload.postToolUse?.executionTimeMs))) durationMs = Number(payload.postToolUse.executionTimeMs);
  } else if (runtime === "antigravity") {
    session = payload.conversationId || "hook";
    toolName = payload.toolCall?.name || "unknown";
    eventName = payload.hookEventName || payload.hook_event_name || "PostToolUse";
  }

  const metadata = {
    eventName: cleanLabel(eventName, "tool"),
    toolName: cleanLabel(toolName),
    outcome: cleanLabel(outcomeFrom(runtime, payload), "observed"),
  };
  if (durationMs !== null) metadata.durationMs = Math.max(0, Math.round(durationMs));

  return {
    runtime,
    session: cleanLabel(session, "hook"),
    kind: "tool",
    metadata,
  };
}

export function ingestHookPayload({ runtime, payload, cwd = process.cwd() }) {
  const normalized = normalizeHookEvent(runtime, payload);
  if (!normalized) return { recorded: false, reason: "unsupported-or-invalid-payload" };
  const hintedRoot = payload?.cwd || payload?.workspacePaths?.[0] || cwd;
  const root = findHookProjectRoot(hintedRoot) || findHookProjectRoot(cwd);
  if (!root) return { recorded: false, reason: "ag-kit-project-not-found" };
  const event = recordObservation({ root, ...normalized });
  return { recorded: true, root, event };
}

const readBoundedStdin = async (stream = process.stdin) => {
  const chunks = [];
  let bytes = 0;
  let overflow = false;
  for await (const chunk of stream) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    bytes += buffer.length;
    if (!overflow && bytes <= MAX_STDIN_BYTES) chunks.push(buffer);
    else overflow = true;
  }
  return { overflow, bytes, text: overflow ? "" : Buffer.concat(chunks).toString("utf8") };
};

const recordOverflow = (runtime, cwd, bytes) => {
  const root = findHookProjectRoot(cwd);
  if (!root || !SUPPORTED.has(runtime)) return;
  recordObservation({
    root,
    runtime,
    session: "hook",
    kind: "hook-overflow",
    metadata: { eventName: "hook", outcome: "payload-too-large", bytes: Math.max(0, Number(bytes) || 0) },
  });
};

export async function runHookIngestCli(argv = process.argv) {
  const runtime = String(argv[3] || "").toLowerCase();
  try {
    const input = await readBoundedStdin();
    if (input.overflow) recordOverflow(runtime, process.cwd(), input.bytes);
    else {
      let payload = null;
      try { payload = JSON.parse(input.text || "{}"); } catch {}
      if (payload) ingestHookPayload({ runtime, payload, cwd: process.cwd() });
    }
  } catch (error) {
    if (process.env.AG_KIT_HOOK_DEBUG === "1") process.stderr.write(`AG Kit hook ingest: ${error?.message || error}\n`);
  }
  process.stdout.write("{}\n");
}
