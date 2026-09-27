import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const here = path.dirname(fileURLToPath(import.meta.url));
const bin = path.resolve(here, "../bin/ag-kit.js");

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-benchmark-cli-"));
  fs.writeFileSync(path.join(root, "package.json"), "{\"name\":\"benchmark-cli-test\"}\n");
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

test("ag-kit benchmark runs through the dispatcher and returns JSON evidence", (t) => {
  const root = tempRoot(t);
  const result = spawnSync(process.execPath, [bin, "benchmark", "--no-write", "-p", root], { encoding: "utf8", timeout: 30000 });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = JSON.parse(result.stdout);
  assert.equal(report.passed, true);
  assert.equal(report.benchmarks.length, 4);
  assert.equal(fs.existsSync(path.join(root, ".ag-kit", "benchmarks", "latest.json")), false);
});
