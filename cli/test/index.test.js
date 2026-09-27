import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { buildProgram } from "../bin/index.js";
import { buildV2Program } from "../lib/v2-cli.js";
import { addMemory, recallMemory, initTeam } from "../lib/v2-engine.js";
import { createMcpServer } from "../lib/mcp-server.js";
import { wireRuntimeMcp } from "../lib/runtime-mcp.js";
import { doctorRuntime, finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "../lib/runtime-lifecycle.js";

const execFileAsync = promisify(execFile);

const runSymlinkedEntry = async (t, relativeEntry, prefix) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  fs.mkdirSync(path.join(dir, ".bin"));
  const link = path.join(dir, ".bin", "ag-kit");
  fs.symlinkSync(path.resolve(relativeEntry), link);
  const { stdout } = await execFileAsync(process.execPath, [link, "--version"]);
  assert.match(stdout.trim(), /^\d{4}\.\d+\.\d+$/);
};

test("legacy CLI keeps safe lifecycle commands", () => {
  const program = buildProgram();
  const commands = new Map(program.commands.map((command) => [command.name(), command]));
  assert.deepEqual([...commands.keys()], ["init", "update", "rollback", "status"]);
  assert.ok(commands.get("update").options.some((option) => option.long === "--strategy"));
});

test("v2 CLI exposes operating-layer commands", () => {
  assert.deepEqual(buildV2Program().commands.map((command) => command.name()), [
    "runtime", "memory", "team", "flow", "cross-audit", "observe", "dashboard", "personalize", "design", "route", "run", "preflight", "mcp",
  ]);
});

test("runtime CLI exposes lifecycle verification and safe removal", () => {
  const runtime = buildV2Program().commands.find((command) => command.name() === "runtime");
  assert.deepEqual(runtime.commands.map((command) => command.name()), ["list", "install", "doctor", "uninstall"]);
});

test("dashboard CLI exposes summary lifecycle", () => {
  const dashboard = buildV2Program().commands.find((command) => command.name() === "dashboard");
  assert.deepEqual(dashboard.commands.map((command) => command.name()), ["summary", "start", "status", "stop"]);
});

test("memory and team engines are project-local", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-v2-cli-"));
  try {
    fs.writeFileSync(path.join(root, "package.json"), "{}");
    addMemory({ root, text: "Use transactions for billing", kind: "decision" });
    assert.equal(recallMemory({ root, query: "billing" }).length, 1);
    assert.equal(initTeam({ root, archetype: "auto" }).archetype, "software");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("MCP server constructs without transport", () => assert.ok(createMcpServer()));

test("runtime MCP wiring uses project-scoped formats", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-mcp-"));
  try {
    const claude = wireRuntimeMcp({ root, runtime: "claude" });
    assert.equal(claude.file, ".mcp.json");
    assert.equal(JSON.parse(fs.readFileSync(path.join(root, ".mcp.json"), "utf8")).mcpServers["ag-kit"].command, "ag-kit");
    const gemini = wireRuntimeMcp({ root, runtime: "gemini" });
    assert.equal(gemini.file, ".gemini/settings.json");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("runtime lifecycle preserves user drift while stripping AG Kit marker", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-lifecycle-"));
  try {
    const file = path.join(root, "AGENTS.md");
    fs.writeFileSync(file, "# User rules\n");
    const prepared = prepareRuntimeInstall({ root, runtime: "pi" });
    fs.writeFileSync(file, "# User rules\n\n<!-- AG-KIT:CORE:START -->\nAG Kit core\n<!-- AG-KIT:CORE:END -->\n");
    finalizeRuntimeInstall({ prepared, mcp: { wired: false, reason: "rules-only" } });
    assert.equal(doctorRuntime({ root, runtime: "pi" }).status, "live");
    fs.appendFileSync(file, "\nUser edit after install.\n");
    const result = uninstallRuntime({ root, runtime: "pi" });
    assert.equal(result.status, "uninstalled");
    const remaining = fs.readFileSync(file, "utf8");
    assert.match(remaining, /User rules/);
    assert.match(remaining, /User edit after install/);
    assert.doesNotMatch(remaining, /AG-KIT:CORE/);
    assert.equal(doctorRuntime({ root, runtime: "pi" }).status, "untouched");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("CLI dispatcher runs through npm bin symlink", async (t) => {
  await runSymlinkedEntry(t, "bin/ag-kit.js", "ag-kit-dispatcher-symlink-");
});

test("legacy CLI entry resolves npm-style symlink before direct-run detection", async (t) => {
  await runSymlinkedEntry(t, "bin/index.js", "ag-kit-legacy-symlink-");
});
