import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runtimeStatusForMcp } from "../lib/mcp-server.js";

const tempProject = () => fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-mcp-status-"));
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
};

test("MCP runtime status reports every lifecycle manifest", () => {
  const root = tempProject();
  try {
    const manifests = path.join(root, ".ag-kit", "runtime-installs");
    writeJson(path.join(manifests, "claude.json"), { schema: 1, runtime: "claude", installedAt: "2026-09-27T00:00:00.000Z", mcp: { wired: false }, entries: [] });
    writeJson(path.join(manifests, "pi.json"), { schema: 1, runtime: "pi", installedAt: "2026-09-27T00:00:00.000Z", mcp: { wired: false, reason: "rules-only" }, entries: [] });
    writeJson(path.join(root, ".ag-kit", "runtime.json"), { schema: 1, runtime: "pi", installedAt: "legacy-last-write" });

    const status = runtimeStatusForMcp(root);
    assert.equal(status.installed, true);
    assert.equal(status.source, "lifecycle-manifests");
    assert.deepEqual(status.runtimes.map((item) => item.runtime), ["claude", "pi"]);
    assert.equal(status.runtimes.find((item) => item.runtime === "claude").status, "standing-by");
    assert.equal(status.runtimes.find((item) => item.runtime === "pi").status, "live");
    assert.equal("legacy" in status, false);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("MCP runtime status falls back to legacy runtime metadata only without manifests", () => {
  const root = tempProject();
  try {
    writeJson(path.join(root, ".ag-kit", "runtime.json"), { schema: 1, runtime: "gemini", installedAt: "2026-09-27T00:00:00.000Z" });
    const status = runtimeStatusForMcp(root);
    assert.equal(status.installed, true);
    assert.equal(status.source, "legacy-runtime-json");
    assert.equal(status.legacy.runtime, "gemini");
    assert.deepEqual(status.runtimes, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("MCP runtime status inherits the v2 unsafe-root guard", () => {
  assert.throws(() => runtimeStatusForMcp(path.parse(process.cwd()).root), /filesystem root/);
  assert.throws(() => runtimeStatusForMcp(os.homedir()), /user home/);
});
