import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runLocalBenchmarks } from "../lib/benchmark.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-benchmark-test-"));
  fs.writeFileSync(path.join(root, "package.json"), "{\"name\":\"benchmark-test\"}\n");
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

test("local benchmark harness produces deterministic evidence across four contracts", (t) => {
  const root = tempRoot(t);
  const report = runLocalBenchmarks({ root, write: false });
  assert.equal(report.passed, true);
  assert.deepEqual(report.benchmarks.map((item) => item.name), ["memory-recall", "routing", "compression", "runtime-lifecycle"]);
  assert.equal(report.benchmarks.find((item) => item.name === "memory-recall").score, 1);
  assert.equal(report.benchmarks.find((item) => item.name === "routing").score, 1);
  assert.equal(report.benchmarks.find((item) => item.name === "compression").anchorsPreserved, true);
  assert.equal(report.benchmarks.find((item) => item.name === "runtime-lifecycle").finalStatus, "untouched");
});

test("benchmark writes a portable receipt and latest snapshot", (t) => {
  const root = tempRoot(t);
  const report = runLocalBenchmarks({ root, write: true });
  assert.equal(report.passed, true);
  assert.match(report.receipt, /^\.ag-kit\/benchmarks\/.+-local\.json$/);
  assert.equal(fs.existsSync(path.join(root, report.receipt)), true);
  const latest = JSON.parse(fs.readFileSync(path.join(root, ".ag-kit", "benchmarks", "latest.json"), "utf8"));
  assert.equal(latest.passed, true);
  assert.equal(latest.methodology.includes("No network/model benchmark"), true);
});
