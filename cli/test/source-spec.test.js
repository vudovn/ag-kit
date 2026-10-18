import test from "node:test";
import assert from "node:assert/strict";
import { cliVersion, runtimeSourceSpec } from "../lib/source-spec.js";

test("runtime source defaults to the CLI release tag", () => {
  assert.equal(runtimeSourceSpec(), `github:vudovn/ag-kit#v${cliVersion}`);
});

test("runtime source accepts an explicit branch or ref override", () => {
  assert.equal(runtimeSourceSpec("feat/example"), "github:vudovn/ag-kit#feat/example");
  assert.equal(runtimeSourceSpec("v2099.1.1"), "github:vudovn/ag-kit#v2099.1.1");
});
