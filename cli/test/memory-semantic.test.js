import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { loadTransformerEmbedder, rebuildSemanticIndex, semanticRecall, semanticStatus } from "../lib/memory-semantic.js";

const tempRoot = (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-semantic-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
};

const writeEntry = (root, name, body) => {
  const dir = path.join(root, ".ag-kit", "memory", "entries");
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, `${name}.md`), `---\nid: ${name}\nkind: learning\n---\n# ${name}\n\n${body}\n`);
};

const fakeProvider = () => {
  const calls = [];
  const vector = (text) => {
    const lower = String(text).toLowerCase();
    if (/database|postgres|transaction|concurrency/.test(lower)) return [1, 0, 0];
    if (/react|button|frontend|interface/.test(lower)) return [0, 1, 0];
    return [0, 0, 1];
  };
  return {
    model: "test-local-embedder",
    calls,
    async embed(texts) {
      calls.push([...texts]);
      return texts.map(vector);
    },
  };
};

test("semantic cold tier is disabled by default without importing a model runtime", async (t) => {
  const root = tempRoot(t);
  let imports = 0;
  const result = await semanticStatus(root, { importer: async () => { imports += 1; throw new Error("should not import"); } });
  assert.equal(result.enabled, false);
  assert.equal(result.reason, "disabled");
  assert.equal(imports, 0);
});

test("semantic provider fails closed to unavailable when optional dependency is absent", async (t) => {
  const root = tempRoot(t);
  const result = await loadTransformerEmbedder({
    root,
    config: { enabled: true, allowDownload: false, model: "local-model" },
    importer: async () => { throw new Error("missing"); },
  });
  assert.equal(result.available, false);
  assert.equal(result.reason, "dependency-missing");
  assert.equal(result.allowDownload, false);
});

test("semantic index is rebuildable, reuses unchanged vectors, and stores no raw memory", async (t) => {
  const root = tempRoot(t);
  writeEntry(root, "database", "Postgres transaction isolation protects concurrent billing updates.");
  writeEntry(root, "frontend", "React button states should expose accessible loading feedback.");
  const provider = fakeProvider();

  const first = await rebuildSemanticIndex({ root, provider, overrides: { enabled: true } });
  assert.equal(first.available, true);
  assert.equal(first.embedded, 2);
  assert.equal(first.reused, 0);
  assert.equal(provider.calls.length, 1);

  const second = await rebuildSemanticIndex({ root, provider, overrides: { enabled: true } });
  assert.equal(second.embedded, 0);
  assert.equal(second.reused, 2);
  assert.equal(provider.calls.length, 1, "unchanged entries should not be re-embedded");

  const indexText = fs.readFileSync(path.join(root, ".ag-kit", "memory", "semantic", "index.json"), "utf8");
  assert.equal(indexText.includes("Postgres transaction isolation"), false);
  assert.equal(indexText.includes("React button states"), false);
});

test("semantic recall ranks meaning-near entries using the local provider", async (t) => {
  const root = tempRoot(t);
  writeEntry(root, "database", "Postgres transaction isolation protects concurrent billing updates.");
  writeEntry(root, "frontend", "React button states should expose accessible loading feedback.");
  const provider = fakeProvider();

  const result = await semanticRecall({ root, query: "database concurrency", limit: 2, provider, overrides: { enabled: true } });
  assert.equal(result.available, true);
  assert.equal(result.engine, "semantic-vectors");
  assert.equal(result.results.length, 2);
  assert.match(result.results[0].file, /database\.md$/);
  assert.ok(result.results[0].score > result.results[1].score);
  assert.match(result.results[0].preview, /Postgres transaction isolation/);
});
