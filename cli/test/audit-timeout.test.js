import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runConsensusAudit } from "../lib/audit-consensus.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-timeout-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

const stubbornReviewer = `#!/usr/bin/env node
const args = process.argv.slice(2);
if (args.includes("--version")) { console.log("fake-codex 1.0"); process.exit(0); }
process.on("SIGTERM", () => {});
setTimeout(() => console.log('{"findings":[]}'), 10000);
`;

test("cross-audit hard-kills a reviewer that ignores the soft timeout", { skip: process.platform === "win32" }, async (t) => {
  const root = tempRoot(t);
  const bin = path.join(root, "fake-bin");
  fs.mkdirSync(bin, { recursive: true });
  const codex = path.join(bin, "codex");
  fs.writeFileSync(codex, stubbornReviewer);
  fs.chmodSync(codex, 0o755);
  fs.writeFileSync(path.join(root, "sample.txt"), "bounded audit\n");

  const previousPath = process.env.PATH;
  process.env.PATH = `${bin}${path.delimiter}${previousPath || ""}`;
  t.after(() => { process.env.PATH = previousPath; });

  const started = Date.now();
  const report = await runConsensusAudit({ root, target: "sample.txt", reviewers: 1, timeoutMs: 1000 });
  const elapsed = Date.now() - started;

  assert.equal(report.status, "unavailable");
  assert.equal(report.results.length, 1);
  assert.equal(report.results[0].ok, false);
  assert.equal(report.results[0].chunks[0].timedOut, true);
  assert.match(report.results[0].chunks[0].error, /timed out/i);
  assert.ok(elapsed < 4000, `expected hard-kill bound, elapsed=${elapsed}ms`);
});
