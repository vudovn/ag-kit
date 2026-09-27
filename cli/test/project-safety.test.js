import test from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import { stateRoot } from "../lib/project-state.js";
import { prepareRuntimeInstall } from "../lib/runtime-lifecycle.js";

test("project state refuses filesystem root and user home", () => {
  assert.throws(() => stateRoot(path.parse(process.cwd()).root), /filesystem root/);
  assert.throws(() => stateRoot(os.homedir()), /user home/);
});

test("runtime lifecycle refuses filesystem root and user home", () => {
  assert.throws(() => prepareRuntimeInstall({ root: path.parse(process.cwd()).root, runtime: "antigravity" }), /filesystem root/);
  assert.throws(() => prepareRuntimeInstall({ root: os.homedir(), runtime: "antigravity" }), /user home/);
});
