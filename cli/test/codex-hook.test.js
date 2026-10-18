import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { wireRuntimeMcp } from "../lib/runtime-mcp.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-codex-hook-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

test("Codex plugin bundles an async privacy-minimal PostToolUse hook", (t) => {
  const root = tempRoot(t);
  const projectedSkill = path.join(root, ".agents", "skills", "example");
  fs.mkdirSync(projectedSkill, { recursive: true });
  fs.writeFileSync(path.join(projectedSkill, "SKILL.md"), "# Example\n");

  const result = wireRuntimeMcp({ root, runtime: "codex" });
  assert.equal(result.observability.wired, true);
  assert.equal(result.observability.event, "PostToolUse");
  assert.equal(result.observability.privacy, "metadata-only");

  const hooks = JSON.parse(fs.readFileSync(path.join(root, ".codex-plugin", "hooks", "hooks.json"), "utf8"));
  const handler = hooks.hooks.PostToolUse[0].hooks[0];
  assert.equal(handler.type, "command");
  assert.equal(handler.command, "ag-kit hook-ingest codex");
  assert.equal(handler.async, true);
  assert.equal(handler.timeout, 5);

  const plugin = JSON.parse(fs.readFileSync(path.join(root, ".codex-plugin", "plugin.json"), "utf8"));
  assert.equal(plugin.hooks, "./hooks/hooks.json");
  assert.equal(plugin.mcpServers, "./.mcp.json");
  assert.ok(fs.existsSync(path.join(root, ".codex-plugin", "skills", "example", "SKILL.md")));
});
