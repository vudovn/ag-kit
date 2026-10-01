import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { findHookProjectRoot, ingestHookPayload, normalizeHookEvent } from "../lib/hook-ingest.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const cliBin = path.resolve(__dirname, "..", "bin", "ag-kit.js");
const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-hook-ingest-"));
  fs.mkdirSync(path.join(root, ".ag-kit"), { recursive: true });
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};
const eventsFile = (root) => path.join(root, ".ag-kit", "observability", "events.jsonl");

 test("hook ingestion stores allowlisted metadata and never raw tool input/response", (t) => {
  const root = tempRoot(t);
  const nested = path.join(root, "src", "feature");
  fs.mkdirSync(nested, { recursive: true });
  assert.equal(findHookProjectRoot(nested), root);

  const result = ingestHookPayload({
    runtime: "codex",
    cwd: nested,
    payload: {
      session_id: "session-1",
      hook_event_name: "PostToolUse",
      tool_name: "Bash",
      cwd: nested,
      tool_input: { command: "echo SECRET_COMMAND" },
      tool_response: { output: "SECRET_RESPONSE" },
    },
  });
  assert.equal(result.recorded, true);

  const raw = fs.readFileSync(eventsFile(root), "utf8");
  assert.doesNotMatch(raw, /SECRET_COMMAND|SECRET_RESPONSE/);
  const event = JSON.parse(raw.trim());
  assert.equal(event.runtime, "codex");
  assert.equal(event.session, "session-1");
  assert.equal(event.kind, "tool");
  assert.deepEqual(event.metadata, { eventName: "PostToolUse", toolName: "Bash", outcome: "observed" });
});

test("host-specific normalization records only coarse outcome signals", () => {
  const gemini = normalizeHookEvent("gemini", {
    session_id: "g-1",
    hook_event_name: "AfterTool",
    tool_name: "run_shell_command",
    tool_response: { error: "SECRET_STACK_TRACE" },
  });
  assert.deepEqual(gemini, {
    runtime: "gemini",
    session: "g-1",
    kind: "tool",
    metadata: { eventName: "AfterTool", toolName: "run_shell_command", outcome: "error" },
  });

  const cline = normalizeHookEvent("cline", {
    taskId: "task-1",
    hookName: "PostToolUse",
    postToolUse: { toolName: "write_to_file", success: true, executionTimeMs: 42, result: "SECRET" },
  });
  assert.equal(cline.metadata.outcome, "success");
  assert.equal(cline.metadata.durationMs, 42);
  assert.equal(Object.hasOwn(cline.metadata, "result"), false);
});

test("hidden hook-ingest CLI is fail-open and emits host-safe JSON", (t) => {
  const root = tempRoot(t);
  const payload = JSON.stringify({ session_id: "g-cli", hook_event_name: "AfterTool", tool_name: "read_file", cwd: root, tool_response: {} });
  const run = spawnSync(process.execPath, [cliBin, "hook-ingest", "gemini"], { cwd: root, input: payload, encoding: "utf8", timeout: 5000 });
  assert.equal(run.status, 0);
  assert.equal(run.stdout.trim(), "{}");
  const event = JSON.parse(fs.readFileSync(eventsFile(root), "utf8").trim());
  assert.equal(event.runtime, "gemini");
  assert.equal(event.session, "g-cli");

  const invalid = spawnSync(process.execPath, [cliBin, "hook-ingest", "unknown"], { cwd: root, input: "not-json", encoding: "utf8", timeout: 5000 });
  assert.equal(invalid.status, 0);
  assert.equal(invalid.stdout.trim(), "{}");
});
