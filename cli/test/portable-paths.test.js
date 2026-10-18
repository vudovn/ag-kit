import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "../lib/runtime-lifecycle.js";
import { wireRuntimeMcp } from "../lib/runtime-mcp.js";

const assertPortable = (value, label) => {
  assert.equal(typeof value, "string", `${label} must be a string`);
  assert.doesNotMatch(value, /\\/, `${label} must use portable '/' separators`);
};

test("machine-readable runtime paths are portable across operating systems", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-portable-paths-"));
  try {
    const agents = path.join(root, "AGENTS.md");
    fs.writeFileSync(agents, "# User rules\n");

    const prepared = prepareRuntimeInstall({ root, runtime: "pi" });
    assertPortable(prepared.backupRoot, "backupRoot");
    assertPortable(prepared.entries[0].backup, "entry backup");

    fs.writeFileSync(agents, "# User rules\n\n<!-- AG-KIT:CORE:START -->\nAG Kit core\n<!-- AG-KIT:CORE:END -->\n");
    finalizeRuntimeInstall({ prepared, mcp: { wired: false, reason: "rules-only" } });
    const uninstall = uninstallRuntime({ root, runtime: "pi" });
    assertPortable(uninstall.receipt, "uninstall receipt");

    const gemini = wireRuntimeMcp({ root, runtime: "gemini" });
    assert.equal(gemini.file, ".gemini/settings.json");
    assertPortable(gemini.file, "MCP file");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
