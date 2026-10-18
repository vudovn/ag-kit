import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { installSemanticProvider, loadTransformerEmbedder, semanticProviderStatus, semanticStatus, setSemanticEnabled, SEMANTIC_PROVIDER_VERSION } from "../lib/memory-semantic.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-semantic-provider-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

const fakeProviderPackage = (root, version = "0.0.0-test") => {
  const dir = path.join(root, ".ag-kit", "memory", "semantic", "provider", "node_modules", "@huggingface", "transformers");
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "package.json"), `${JSON.stringify({ name: "@huggingface/transformers", version, type: "module", exports: "./index.js" }, null, 2)}\n`);
  fs.writeFileSync(path.join(dir, "index.js"), `export async function pipeline(){const fn=async(texts)=>texts.map(()=>[1,2,3]);fn.dispose=async()=>{};return fn;}\n`);
};

test("semantic on/off is persisted project-locally without importing a provider", async (t) => {
  const root = tempRoot(t);
  setSemanticEnabled({ root, enabled: true, model: "local-model" });
  const enabled = await semanticStatus(root, { importer: async () => { throw new Error("missing"); } });
  assert.equal(enabled.enabled, true);
  assert.equal(enabled.model, "local-model");
  assert.equal(enabled.reason, "dependency-missing");

  setSemanticEnabled({ root, enabled: false });
  const disabled = await semanticStatus(root, { importer: async () => { throw new Error("must not import"); } });
  assert.equal(disabled.enabled, false);
  assert.equal(disabled.reason, "disabled");
});

test("semantic loader falls back to the explicit project-local provider", async (t) => {
  const root = tempRoot(t);
  fakeProviderPackage(root);
  setSemanticEnabled({ root, enabled: true, model: "local-model" });
  const loaded = await loadTransformerEmbedder({ root, config: { enabled: true, allowDownload: false, model: "local-model" } });
  assert.equal(loaded.available, true);
  const vectors = await loaded.embed(["hello"]);
  assert.equal(vectors.length, 1);
  assert.equal(vectors[0].length, 3);
  assert.ok(Math.abs(vectors[0].reduce((sum, value) => sum + value * value, 0) - 1) < 1e-6);
  await loaded.dispose();
});

test("semantic provider setup requires explicit network approval and pins the provider", async (t) => {
  const root = tempRoot(t);
  let calls = 0;
  const blocked = installSemanticProvider({ root, runner: () => { calls += 1; return { status: 0 }; } });
  assert.equal(blocked.installed, false);
  assert.equal(blocked.reason, "network-not-approved");
  assert.equal(calls, 0);

  const installed = installSemanticProvider({
    root,
    allowNetwork: true,
    runner: (_command, args) => {
      calls += 1;
      const prefix = args[args.indexOf("--prefix") + 1];
      fakeProviderPackage(root, SEMANTIC_PROVIDER_VERSION);
      assert.equal(prefix, path.join(root, ".ag-kit", "memory", "semantic", "provider"));
      assert.ok(args.includes(`@huggingface/transformers@${SEMANTIC_PROVIDER_VERSION}`));
      return { status: 0, stdout: "", stderr: "" };
    },
  });
  assert.equal(calls, 1);
  assert.equal(installed.installed, true);
  assert.equal(installed.version, SEMANTIC_PROVIDER_VERSION);
  assert.equal(semanticProviderStatus(root).installed, true);
  const status = await semanticStatus(root);
  assert.equal(status.enabled, true);
  assert.equal(status.available, true);
});
