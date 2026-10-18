import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runBenchmarks } from "../lib/benchmark.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-benchmark-test-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

test("benchmark harness produces passing deterministic evidence and a local receipt", async (t) => {
  const root = tempRoot(t);
  const result = await runBenchmarks({ root });
  assert.equal(result.schema, 1);
  assert.equal(result.passed, true);
  assert.deepEqual(result.cases.map((item) => item.name), ["memory", "routing", "lifecycle", "compression"]);
  assert.ok(result.cases.every((item) => item.passed));
  assert.ok(result.cases.find((item) => item.name === "compression").evidence.bytesSaved > 0);
  assert.equal(result.cases.find((item) => item.name === "lifecycle").evidence.preservedUserState, true);
  assert.ok(result.receipt?.startsWith(".ag-kit/benchmarks/"));
  assert.ok(fs.existsSync(path.join(root, result.receipt)));
  assert.ok(fs.existsSync(path.join(root, ".ag-kit", "benchmarks", "latest.json")));
});

test("benchmark harness can run without writing a receipt", async (t) => {
  const root = tempRoot(t);
  const result = await runBenchmarks({ root, writeReceipt: false });
  assert.equal(result.passed, true);
  assert.equal(result.receipt, undefined);
  assert.equal(fs.existsSync(path.join(root, ".ag-kit", "benchmarks")), false);
});
