import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { detectRuntimes, findBinary } from "../lib/runtime-detect.js";

test("findBinary searches PATH without invoking a shell", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-bin-"));
  const name = process.platform === "win32" ? "codex.CMD" : "codex";
  const file = path.join(root, name);
  fs.writeFileSync(file, process.platform === "win32" ? "@echo off\r\n" : "#!/bin/sh\nexit 0\n");
  if (process.platform !== "win32") fs.chmodSync(file, 0o755);
  try {
    assert.equal(path.resolve(findBinary("codex", root)), path.resolve(file));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("runtime detection distinguishes project evidence from untouched targets", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-detect-"));
  try {
    fs.mkdirSync(path.join(root, ".cline"));
    fs.mkdirSync(path.join(root, ".ag-kit", "runtime-installs"), { recursive: true });
    fs.writeFileSync(path.join(root, ".ag-kit", "runtime-installs", "aider.json"), "{}\n");
    const results = detectRuntimes({ root, includeHome: false });
    const byName = Object.fromEntries(results.map((item) => [item.runtime, item]));
    assert.equal(byName.cline.detected, true);
    assert.deepEqual(byName.cline.projectMarkers, [".cline"]);
    assert.equal(byName.aider.lifecycle, true);
    assert.equal(results.length, 16);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
