import test from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import { stateRoot } from "../lib/project-state.js";
import { initMemory, initTeam, installRuntime } from "../lib/v2-engine.js";
import { prepareRuntimeInstall } from "../lib/runtime-lifecycle.js";

const filesystemRoot = path.parse(process.cwd()).root;
const userHome = os.homedir();

const assertUnsafeRootsRejected = (fn) => {
  assert.throws(() => fn(filesystemRoot), /filesystem root/);
  assert.throws(() => fn(userHome), /user home/);
};

test("project state refuses filesystem root and user home", () => {
  assertUnsafeRootsRejected((root) => stateRoot(root));
});

test("v2 memory and team writers refuse filesystem root and user home", () => {
  assertUnsafeRootsRejected((root) => initMemory(root));
  assertUnsafeRootsRejected((root) => initTeam({ root, archetype: "software" }));
});

test("runtime lifecycle refuses filesystem root and user home", () => {
  assertUnsafeRootsRejected((root) => prepareRuntimeInstall({ root, runtime: "antigravity" }));
});

test("direct v2 runtime install refuses filesystem root and user home before reading source projections", () => {
  assertUnsafeRootsRejected((targetRoot) => installRuntime({ sourceRoot: process.cwd(), targetRoot, runtime: "claude" }));
});
