import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { resolveSandboxCommand, routeTask, runSandboxedCommand } from "../lib/efficiency.js";
import { dashboardStatus, recordObservation, summarizeObservability } from "../lib/observability.js";

test("routing keeps reads cheap and architecture high effort", () => {
  assert.equal(routeTask("find where auth is configured").role, "scout");
  const architecture = routeTask("design a cross-runtime migration architecture");
  assert.equal(architecture.role, "architect");
  assert.equal(architecture.effort, "high");
  assert.equal(architecture.mode, "deep");
});

test("command sandbox keeps full output on disk and returns a bounded summary", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-sandbox-"));
  try {
    const script = "for(let i=0;i<120;i++) console.log('line-'+i)";
    const result = runSandboxedCommand({ root, command: process.execPath, args: ["-e", script], maxSummaryLines: 20 });
    assert.equal(result.ok, true);
    assert.ok(result.omittedLines > 0);
    assert.match(result.summary, /saved to sandbox log/);
    assert.ok(fs.readFileSync(path.join(root, result.log), "utf8").includes("line-119"));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("bare Python commands prefer the project virtual environment", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-python-env-"));
  try {
    const relativePython = process.platform === "win32"
      ? path.join(".venv", "Scripts", "python.exe")
      : path.join(".venv", "bin", "python");
    const python = path.join(root, relativePython);
    fs.mkdirSync(path.dirname(python), { recursive: true });
    fs.writeFileSync(python, process.platform === "win32" ? "" : "#!/bin/sh\nexit 0\n");
    if (process.platform !== "win32") fs.chmodSync(python, 0o755);

    const resolved = resolveSandboxCommand({ root, command: "python" });
    assert.equal(resolved.resolvedCommand, python);
    assert.deepEqual(resolved.environment, { kind: "python-venv", path: ".venv" });

    const explicit = resolveSandboxCommand({ root, command: process.execPath });
    assert.equal(explicit.resolvedCommand, process.execPath);
    assert.equal(explicit.environment, null);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("observability reports only explicit metrics and dashboard starts stopped", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-observe-"));
  try {
    recordObservation({ root, runtime: "test", inputTokens: 10, outputTokens: 5, savedTokens: 3, costUsd: 0.01 });
    const summary = summarizeObservability(root);
    assert.equal(summary.totals.savedTokens, 3);
    assert.match(summary.methodology.savedTokens, /explicitly/);
    assert.equal(dashboardStatus(root).running, false);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
