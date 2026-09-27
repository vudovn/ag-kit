import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { recordObservation, summarizeObservability } from "../lib/observability.js";
import { startFlow } from "../lib/workflow-session.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-observe-trace-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

test("observability rolls traced events together without hiding untraced history", (t) => {
  const root = tempRoot(t);
  recordObservation({ root, runtime: "legacy", kind: "idle", inputTokens: 3 });

  const flow = startFlow({ root, goal: "Correlate execution evidence", mode: "quick" });
  recordObservation({ root, runtime: "claude", kind: "tool", inputTokens: 100, outputTokens: 20, costUsd: 0.01 });
  recordObservation({ root, runtime: "codex", kind: "verify", inputTokens: 50, outputTokens: 10, savedTokens: 12, costUsd: 0.005 });

  const summary = summarizeObservability(root);
  assert.equal(summary.totals.events, 3);
  assert.equal(summary.untracedEvents, 1);
  assert.equal(summary.recentTraces[0].traceId, flow.traceId);
  assert.equal(summary.traces[flow.traceId].events, 2);
  assert.equal(summary.traces[flow.traceId].inputTokens, 150);
  assert.equal(summary.traces[flow.traceId].outputTokens, 30);
  assert.equal(summary.traces[flow.traceId].savedTokens, 12);
  assert.equal(summary.traces[flow.traceId].costUsd, 0.015);
  assert.deepEqual(summary.traces[flow.traceId].runtimes, { claude: 1, codex: 1 });
  assert.deepEqual(summary.traces[flow.traceId].kinds, { tool: 1, verify: 1 });
});
