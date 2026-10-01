import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const here = path.dirname(fileURLToPath(import.meta.url));
const bin = path.resolve(here, "..", "bin", "ag-kit.js");
const run = (...args) => spawnSync(process.execPath, [bin, "prompt-check", ...args, "--json"], { encoding: "utf8", shell: false });

test("prompt-check CLI returns exit 2 with structured clarification for underspecified work", () => {
  const result = run("fix", "it");
  assert.equal(result.status, 2, result.stderr);
  const body = JSON.parse(result.stdout);
  assert.equal(body.status, "needs-context");
  assert.ok(body.questions.length >= 1);
  assert.equal(JSON.stringify(body).includes("fix it"), false);
});

test("prompt-check CLI stays zero for short concrete work", () => {
  const result = run("review", "PR", "#124");
  assert.equal(result.status, 0, result.stderr);
  const body = JSON.parse(result.stdout);
  assert.equal(body.status, "clear");
  assert.equal(body.ok, true);
});
