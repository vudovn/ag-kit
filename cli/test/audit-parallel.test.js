import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runConsensusAudit } from "../lib/audit-consensus.js";
import { startFlow } from "../lib/workflow-session.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-parallel-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

const fakeReviewer = `#!/usr/bin/env node
const args = process.argv.slice(2);
if (args.includes("--version")) {
  console.log("fake-reviewer 1.0");
  process.exit(0);
}
setTimeout(() => {
  console.log(JSON.stringify({ findings: [{ severity: "optional", title: "Trace propagation", evidence: process.env.AG_KIT_TRACE_ID || "none" }] }));
}, 650);
`;

test("cross-audit overlaps independent reviewer lineages and propagates flow trace", { skip: process.platform === "win32" }, async (t) => {
  const root = tempRoot(t);
  const bin = path.join(root, "fake-bin");
  fs.mkdirSync(bin, { recursive: true });
  for (const name of ["codex", "gemini"]) {
    const file = path.join(bin, name);
    fs.writeFileSync(file, fakeReviewer);
    fs.chmodSync(file, 0o755);
  }
  fs.writeFileSync(path.join(root, "sample.txt"), "const answer = 42;\n");

  const previousPath = process.env.PATH;
  process.env.PATH = `${bin}${path.delimiter}${previousPath || ""}`;
  t.after(() => { process.env.PATH = previousPath; });

  const flow = startFlow({ root, goal: "Audit parallel execution", mode: "quick" });
  const report = await runConsensusAudit({ root, target: "sample.txt", reviewers: 2, timeoutMs: 5000 });

  assert.equal(report.status, "complete");
  assert.equal(report.traceId, flow.traceId);
  assert.deepEqual(new Set(report.lineages), new Set(["openai", "google"]));
  assert.equal(report.results.length, 2);
  for (const reviewer of report.results) {
    assert.equal(reviewer.ok, true);
    assert.match(reviewer.chunks[0].output, new RegExp(flow.traceId));
  }

  const summedReviewerMs = report.results.reduce((sum, reviewer) => sum + reviewer.durationMs, 0);
  assert.ok(summedReviewerMs > 0);
  assert.ok(report.durationMs < summedReviewerMs * 0.85, `expected overlap: wall=${report.durationMs}ms sum=${summedReviewerMs}ms`);
  assert.ok(report.findings.some((finding) => finding.status === "consensus" && finding.title === "Trace propagation"));
});
