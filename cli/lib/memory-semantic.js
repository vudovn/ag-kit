import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { appendReceipt } from "./v2-engine.js";
import { ensureDir, readJson, stateRoot, writeJson } from "./project-state.js";

const DEFAULT_MODEL = "onnx-community/all-MiniLM-L6-v2-ONNX";
const MODEL_PACKAGE = "@huggingface/transformers";
const INDEX_SCHEMA = 1;
const BATCH_SIZE = 16;
const MAX_ENTRY_CHARS = 12000;
const MAX_RESULTS = 50;

const enabledWord = (value) => ["1", "true", "yes", "on"].includes(String(value || "").toLowerCase());
const semanticDir = (root) => path.join(stateRoot(root), "memory", "semantic");
const indexFile = (root) => path.join(semanticDir(root), "index.json");
const entriesDir = (root) => path.join(stateRoot(root), "memory", "entries");
const modelCacheDir = (root) => path.join(semanticDir(root), "model-cache");
const digest = (value) => crypto.createHash("sha256").update(value).digest("hex");
const stripFrontmatter = (value) => String(value || "").replace(/^---[\s\S]*?---\s*/, "").trim();

export function semanticConfig(env = process.env, overrides = {}) {
  return {
    enabled: overrides.enabled ?? enabledWord(env.AG_KIT_VECTORS || env.AG_KIT_SEMANTIC_MEMORY),
    allowDownload: overrides.allowDownload ?? enabledWord(env.AG_KIT_VECTOR_ALLOW_DOWNLOAD),
    model: overrides.model || env.AG_KIT_VECTOR_MODEL || DEFAULT_MODEL,
  };
}

const normalizeVector = (values) => {
  const vector = Array.from(values || [], Number);
  const magnitude = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0));
  if (!vector.length || !Number.isFinite(magnitude) || magnitude === 0) return null;
  return vector.map((value) => value / magnitude);
};

const encodeVector = (vector) => {
  const buffer = Buffer.allocUnsafe(vector.length * 4);
  vector.forEach((value, index) => buffer.writeFloatLE(value, index * 4));
  return buffer.toString("base64");
};

const decodeVector = (encoded) => {
  const buffer = Buffer.from(String(encoded || ""), "base64");
  if (!buffer.length || buffer.length % 4 !== 0) return null;
  const vector = [];
  for (let offset = 0; offset < buffer.length; offset += 4) vector.push(buffer.readFloatLE(offset));
  return vector;
};

const entryRecords = (root) => {
  ensureDir(entriesDir(root));
  return fs.readdirSync(entriesDir(root)).filter((name) => name.endsWith(".md")).sort().map((name) => {
    const file = path.join(entriesDir(root), name);
    const source = fs.readFileSync(file, "utf8");
    const body = stripFrontmatter(source).slice(0, MAX_ENTRY_CHARS);
    return { name, file, relative: path.relative(root, file).split(path.sep).join("/"), body, digest: digest(source) };
  });
};

const tensorRows = (output, expected) => {
  const raw = typeof output?.tolist === "function" ? output.tolist() : output;
  if (!Array.isArray(raw)) return null;
  const rows = expected === 1 && raw.length && typeof raw[0] === "number" ? [raw] : raw;
  if (rows.length !== expected) return null;
  const normalized = rows.map(normalizeVector);
  return normalized.every(Boolean) ? normalized : null;
};

export async function loadTransformerEmbedder({ root = process.cwd(), config = semanticConfig(), importer = (specifier) => import(specifier) } = {}) {
  if (!config.enabled) return { available: false, reason: "disabled", model: config.model, allowDownload: config.allowDownload };
  let transformers;
  try {
    transformers = await importer(MODEL_PACKAGE);
  } catch {
    return { available: false, reason: "dependency-missing", dependency: MODEL_PACKAGE, model: config.model, allowDownload: config.allowDownload };
  }

  let extractor;
  try {
    extractor = await transformers.pipeline("feature-extraction", config.model, {
      cache_dir: modelCacheDir(root),
      local_files_only: !config.allowDownload,
    });
  } catch (error) {
    return {
      available: false,
      reason: config.allowDownload ? "model-load-failed" : "model-not-cached",
      dependency: MODEL_PACKAGE,
      model: config.model,
      allowDownload: config.allowDownload,
      error: String(error?.message || error).slice(0, 240),
    };
  }

  return {
    available: true,
    model: config.model,
    allowDownload: config.allowDownload,
    async embed(texts) {
      const list = Array.isArray(texts) ? texts : [texts];
      const output = await extractor(list, { pooling: "mean", normalize: true });
      const rows = tensorRows(output, list.length);
      if (!rows) throw new Error("semantic embedder returned an unexpected tensor shape");
      return rows;
    },
    async dispose() { if (typeof extractor?.dispose === "function") await extractor.dispose(); },
  };
}

const indexFresh = (root, index, model) => {
  if (!index || index.schema !== INDEX_SCHEMA || index.model !== model) return false;
  const records = entryRecords(root);
  const keys = Object.keys(index.entries || {}).sort();
  if (keys.length !== records.length) return false;
  return records.every((record) => index.entries?.[record.name]?.digest === record.digest);
};

const providerFor = async ({ root, config, provider, importer }) => {
  if (provider) return { available: true, model: provider.model || config.model, allowDownload: false, ...provider };
  return loadTransformerEmbedder({ root, config, importer });
};

export async function semanticStatus(root = process.cwd(), { env = process.env, importer = (specifier) => import(specifier), overrides = {} } = {}) {
  const config = semanticConfig(env, overrides);
  const index = readJson(indexFile(root), null);
  if (!config.enabled) return { enabled: false, available: false, reason: "disabled", model: config.model, index: index ? { entries: Object.keys(index.entries || {}).length, model: index.model, generatedAt: index.generatedAt } : null };
  let dependencyAvailable = true;
  try { await importer(MODEL_PACKAGE); } catch { dependencyAvailable = false; }
  return {
    enabled: true,
    available: dependencyAvailable,
    reason: dependencyAvailable ? (indexFresh(root, index, config.model) ? "ready" : "index-missing-or-stale") : "dependency-missing",
    dependency: MODEL_PACKAGE,
    allowDownload: config.allowDownload,
    model: config.model,
    index: index ? { entries: Object.keys(index.entries || {}).length, model: index.model, generatedAt: index.generatedAt, fresh: indexFresh(root, index, config.model) } : null,
  };
}

export async function rebuildSemanticIndex({ root = process.cwd(), env = process.env, importer = (specifier) => import(specifier), overrides = {}, provider = null } = {}) {
  const config = semanticConfig(env, { ...overrides, enabled: overrides.enabled ?? true });
  const active = await providerFor({ root, config, provider, importer });
  if (!active.available) {
    appendReceipt(root, "memory-semantic", { action: "rebuild", status: "unavailable", reason: active.reason, model: active.model || config.model, allowDownload: Boolean(config.allowDownload) });
    return active;
  }

  const model = active.model || config.model;
  const previous = readJson(indexFile(root), null);
  const reusable = previous?.schema === INDEX_SCHEMA && previous?.model === model ? previous.entries || {} : {};
  const records = entryRecords(root);
  const entries = {};
  const changed = [];

  for (const record of records) {
    const cached = reusable[record.name];
    if (cached?.digest === record.digest && decodeVector(cached.vector)) entries[record.name] = cached;
    else changed.push(record);
  }

  try {
    for (let start = 0; start < changed.length; start += BATCH_SIZE) {
      const batch = changed.slice(start, start + BATCH_SIZE);
      const vectors = await active.embed(batch.map((record) => record.body));
      if (!Array.isArray(vectors) || vectors.length !== batch.length) throw new Error("semantic embedder returned an invalid batch");
      batch.forEach((record, index) => {
        const vector = normalizeVector(vectors[index]);
        if (!vector) throw new Error(`semantic embedder returned an invalid vector for ${record.name}`);
        entries[record.name] = { digest: record.digest, dimensions: vector.length, vector: encodeVector(vector) };
      });
    }

    const dimensions = Object.values(entries)[0]?.dimensions || 0;
    const index = { schema: INDEX_SCHEMA, engine: "local-semantic-vectors", model, dimensions, generatedAt: new Date().toISOString(), entries };
    writeJson(indexFile(root), index);
    appendReceipt(root, "memory-semantic", { action: "rebuild", status: "ready", model, entries: records.length, embedded: changed.length, reused: records.length - changed.length, dimensions, allowDownload: Boolean(config.allowDownload) });
    return { available: true, status: "ready", model, entries: records.length, embedded: changed.length, reused: records.length - changed.length, dimensions, index: path.relative(root, indexFile(root)).split(path.sep).join("/") };
  } finally {
    if (!provider && typeof active.dispose === "function") await active.dispose();
  }
}

const dot = (left, right) => {
  if (!left || !right || left.length !== right.length) return -Infinity;
  let score = 0;
  for (let index = 0; index < left.length; index += 1) score += left[index] * right[index];
  return score;
};

export async function semanticRecall({ root = process.cwd(), query = "", limit = 5, env = process.env, importer = (specifier) => import(specifier), overrides = {}, provider = null } = {}) {
  const text = String(query || "").trim();
  if (!text) throw new Error("semantic recall query is required");
  const config = semanticConfig(env, { ...overrides, enabled: overrides.enabled ?? true });
  const active = await providerFor({ root, config, provider, importer });
  if (!active.available) {
    appendReceipt(root, "memory-semantic", { action: "recall", status: "unavailable", reason: active.reason, model: active.model || config.model, queryChars: text.length, allowDownload: Boolean(config.allowDownload) });
    return { ...active, results: [] };
  }

  const model = active.model || config.model;
  try {
    let index = readJson(indexFile(root), null);
    if (!indexFresh(root, index, model)) {
      const rebuilt = await rebuildSemanticIndex({ root, env, overrides: { ...overrides, enabled: true, model }, provider: active });
      if (!rebuilt.available) return { ...rebuilt, results: [] };
      index = readJson(indexFile(root), null);
    }

    const [queryVectorRaw] = await active.embed([text.slice(0, MAX_ENTRY_CHARS)]);
    const queryVector = normalizeVector(queryVectorRaw);
    if (!queryVector) throw new Error("semantic embedder returned an invalid query vector");
    const records = new Map(entryRecords(root).map((record) => [record.name, record]));
    const take = Math.max(1, Math.min(MAX_RESULTS, Number(limit) || 5));
    const results = Object.entries(index.entries || {}).flatMap(([name, entry]) => {
      const record = records.get(name);
      const vector = decodeVector(entry.vector);
      if (!record || !vector) return [];
      return [{ file: record.relative, score: Number(dot(queryVector, vector).toFixed(6)), preview: record.body.slice(0, 280), engine: "semantic-vectors" }];
    }).filter((item) => Number.isFinite(item.score)).sort((a, b) => b.score - a.score || a.file.localeCompare(b.file)).slice(0, take);

    appendReceipt(root, "memory-semantic", { action: "recall", status: "ready", model, queryChars: text.length, count: results.length, allowDownload: Boolean(config.allowDownload) });
    return { available: true, status: "ready", engine: "semantic-vectors", model, results };
  } finally {
    if (!provider && typeof active.dispose === "function") await active.dispose();
  }
}

export const SEMANTIC_MODEL_PACKAGE = MODEL_PACKAGE;
export const SEMANTIC_DEFAULT_MODEL = DEFAULT_MODEL;
