import test from "node:test";
import assert from "node:assert/strict";
import { runBenchmark } from "../../scripts/benchmark-v2.mjs";

test("v2 benchmark harness produces reproducible correctness evidence", async () => {
  const result = await runBenchmark();
  assert.equal(result.schema, 1);
  assert.equal(result.passed, true);
  assert.equal(result.benchmarks.memoryRecall.expectedTopHit, true);
  assert.equal(result.benchmarks.routing.passed, result.benchmarks.routing.cases);
  assert.ok(result.benchmarks.compression.bytesSaved > 0);
  assert.equal(result.benchmarks.compression.fencedCodePreserved, true);
  assert.equal(result.benchmarks.lifecycle.installedStatus, "live");
  assert.equal(result.benchmarks.lifecycle.finalStatus, "untouched");
  assert.equal(result.benchmarks.lifecycle.memoryPreserved, true);
});
