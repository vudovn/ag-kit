import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory } from "../lib/memory-evolution.js";
import { brainStatus, registerProject, searchAcrossProjects, unregisterProject } from "../lib/memory-registry.js";

const project = (root, name) => {
  const dir = path.join(root, name);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "package.json"), "{}\n");
  return dir;
};

test("cross-project brain is opt-in, bounded, and read-only", () => {
  const harness = fs.mkdtempSync(path.join(os.homedir(), ".ag-kit-brain-test-"));
  const previousHome = process.env.AG_KIT_HOME;
  const previousNoCross = process.env.AG_KIT_NO_CROSS_PROJECT;
  process.env.AG_KIT_HOME = path.join(harness, "state");
  delete process.env.AG_KIT_NO_CROSS_PROJECT;
  try {
    const alpha = project(harness, "alpha");
    const beta = project(harness, "beta");
    addEvolvingMemory({ root: alpha, text: "Billing uses idempotency keys", kind: "decision", durable: true, session: "alpha" });
    addEvolvingMemory({ root: beta, text: "Deploys use blue green rollout", kind: "convention", durable: true, session: "beta" });
    registerProject({ root: alpha });
    registerProject({ root: beta });

    const all = searchAcrossProjects({ query: "rollout", limit: 10 });
    assert.equal(all.disabled, false);
    assert.ok(all.results.some((item) => item.project === "beta" && /blue green/i.test(item.content)));

    const excludingAlpha = searchAcrossProjects({ query: "billing", limit: 10, currentRoot: alpha });
    assert.equal(excludingAlpha.results.some((item) => item.project === "alpha"), false);
    assert.equal(brainStatus().live, 2);

    process.env.AG_KIT_NO_CROSS_PROJECT = "1";
    assert.equal(searchAcrossProjects({ query: "rollout" }).disabled, true);
    delete process.env.AG_KIT_NO_CROSS_PROJECT;

    assert.equal(unregisterProject({ root: beta }).removed, 1);
    assert.equal(brainStatus().projects, 1);
  } finally {
    if (previousHome === undefined) delete process.env.AG_KIT_HOME; else process.env.AG_KIT_HOME = previousHome;
    if (previousNoCross === undefined) delete process.env.AG_KIT_NO_CROSS_PROJECT; else process.env.AG_KIT_NO_CROSS_PROJECT = previousNoCross;
    fs.rmSync(harness, { recursive: true, force: true });
  }
});

test("projects outside home require explicit registration consent", () => {
  const external = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-external-"));
  fs.writeFileSync(path.join(external, "package.json"), "{}\n");
  try {
    assert.throws(() => registerProject({ root: external }), /outside home/);
  } finally {
    fs.rmSync(external, { recursive: true, force: true });
  }
});
