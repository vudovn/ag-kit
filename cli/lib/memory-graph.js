import fs from "node:fs";
import path from "node:path";
import { ensureDir, readJson, stateRoot, writeJson } from "./project-state.js";

const GRAPH_SCHEMA = 1;
const DEFAULT_THRESHOLD = 0.88;
const DEFAULT_WINDOW = 50;
const graphFile = (root) => path.join(stateRoot(root), "memory", "graph.json");
const entriesDir = (root) => path.join(stateRoot(root), "memory", "entries");
const evolutionFile = (root) => path.join(stateRoot(root), "memory", "evolution.json");
const defaultGraph = () => ({ schema: GRAPH_SCHEMA, rebuiltAt: null, entries: {} });
const normalizeSpace = (value) => String(value || "").toLowerCase().replace(/\s+/g, " ").trim();
const stripFrontmatter = (value) => String(value || "").replace(/^---\s*\n[\s\S]*?\n---\s*\n?/, "");
const tokenize = (value) => [...new Set(normalizeSpace(value).match(/[\p{L}\p{N}_-]{3,}/gu) || [])];

const maskCode = (value) => String(value || "")
    .replace(/```[\s\S]*?```/g, (match) => match.replace(/[^\n]/g, " "))
    .replace(/`[^`\n]+`/g, (match) => " ".repeat(match.length));

const normalizeLink = (value) => String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\p{L}\p{N}/_-]/gu, "");

const pushUnique = (array, item, key) => {
    if (!array.some((entry) => key(entry) === key(item))) array.push(item);
};

export function parseMemoryRelations(text) {
    const body = stripFrontmatter(text);
    const masked = maskCode(body);
    const links = [];
    const tags = [];
    const meta = [];
    const facts = [];

    for (const match of masked.matchAll(/\[\[([^\]\n|]+)(?:\|[^\]\n]+)?\]\]/g)) {
        const target = normalizeLink(match[1]);
        if (target) pushUnique(links, { target }, (item) => item.target);
    }
    for (const match of masked.matchAll(/(?:^|[^\p{L}\p{N}_&])#([\p{L}\p{N}_/-]+)/gmu)) {
        const tag = String(match[1]).toLowerCase().replace(/^\/+|\/+$/g, "");
        if (tag) pushUnique(tags, { path: tag, depth: tag.split("/").length }, (item) => item.path);
    }
    for (const match of masked.matchAll(/\[([A-Za-z_][\w-]*)::\s*([^\]\n]{1,240})\]/g)) {
        const item = { key: match[1].toLowerCase(), value: match[2].trim() };
        meta.push(item);
        facts.push({ subject: "memory", predicate: item.key, object: item.value, confidence: 0.9, source: "metadata" });
    }
    for (const line of masked.split(/\r?\n/)) {
        const match = line.match(/^\s*([A-Za-z][A-Za-z0-9 _-]{0,39}):\s+([^\n]{1,240})\s*$/);
        if (!match || /^https?:/i.test(match[2])) continue;
        const predicate = match[1].trim().toLowerCase().replace(/\s+/g, "-");
        const object = match[2].trim();
        if (["http", "https"].includes(predicate)) continue;
        pushUnique(facts, { subject: "memory", predicate, object, confidence: 0.65, source: "key-value" }, (item) => `${item.predicate}\u0000${normalizeSpace(item.object)}`);
    }
    return { links, tags, meta, facts, tokens: tokenize(body), normalized: normalizeSpace(body) };
}

const parseKind = (raw) => raw.match(/^---\s*\n[\s\S]*?\nkind:\s*([^\n]+)[\s\S]*?\n---/m)?.[1]?.trim() || "legacy";
const parseTitle = (raw, fallback) => raw.match(/^#\s+(.+)$/m)?.[1]?.trim() || fallback;

const buildEntry = ({ id, raw, file, kind = "", title = "" }) => {
    const parsed = parseMemoryRelations(raw);
    const stat = fs.statSync(file);
    return {
        id,
        kind: kind || parseKind(raw),
        title: title || parseTitle(raw, id),
        file: path.basename(file),
        mtimeMs: stat.mtimeMs,
        indexedAt: new Date().toISOString(),
        links: parsed.links,
        tags: parsed.tags,
        meta: parsed.meta,
        facts: parsed.facts,
        tokens: parsed.tokens,
        normalized: parsed.normalized,
    };
};

const entryFiles = (root) => {
    const dir = entriesDir(root);
    ensureDir(dir);
    return fs.readdirSync(dir).filter((name) => name.endsWith(".md")).sort();
};

export function rebuildMemoryGraph(root = process.cwd()) {
    const graph = defaultGraph();
    for (const name of entryFiles(root)) {
        const file = path.join(entriesDir(root), name);
        const id = path.basename(name, ".md");
        graph.entries[id] = buildEntry({ id, raw: fs.readFileSync(file, "utf8"), file });
    }
    graph.rebuiltAt = new Date().toISOString();
    writeJson(graphFile(root), graph);
    return graph;
}

export function ensureMemoryGraph(root = process.cwd()) {
    const file = graphFile(root);
    const graph = readJson(file, null);
    const files = entryFiles(root);
    if (!graph || graph.schema !== GRAPH_SCHEMA || !graph.entries || Object.keys(graph.entries).length !== files.length) return rebuildMemoryGraph(root);
    for (const name of files) {
        const id = path.basename(name, ".md");
        const entry = graph.entries[id];
        if (!entry) return rebuildMemoryGraph(root);
        const mtimeMs = fs.statSync(path.join(entriesDir(root), name)).mtimeMs;
        if (Math.abs(Number(entry.mtimeMs || 0) - mtimeMs) > 1) return rebuildMemoryGraph(root);
    }
    return graph;
}

export function indexMemoryGraph(root, id, { kind = "", title = "" } = {}) {
    const graph = ensureMemoryGraph(root);
    const file = path.join(entriesDir(root), `${id}.md`);
    if (!fs.existsSync(file)) throw new Error(`memory entry not found: ${id}`);
    graph.entries[id] = buildEntry({ id, raw: fs.readFileSync(file, "utf8"), file, kind, title });
    graph.rebuiltAt = new Date().toISOString();
    writeJson(graphFile(root), graph);
    return graph.entries[id];
}

const jaccard = (leftValues, rightValues) => {
    const left = new Set(leftValues || []);
    const right = new Set(rightValues || []);
    if (left.size < 4 || right.size < 4) return 0;
    let shared = 0;
    for (const token of left) if (right.has(token)) shared += 1;
    return shared / (left.size + right.size - shared);
};

export function findNearDuplicate({ root = process.cwd(), text, kind = "learning", threshold = DEFAULT_THRESHOLD, window = DEFAULT_WINDOW } = {}) {
    if (process.env.AG_KIT_MEMORY_DEDUP_OFF === "1") return null;
    const parsed = parseMemoryRelations(text);
    const graph = ensureMemoryGraph(root);
    const evolution = readJson(evolutionFile(root), { entries: {} }) || { entries: {} };
    const candidates = Object.values(graph.entries)
        .filter((entry) => entry.kind === kind && !["archived", "superseded"].includes(evolution.entries?.[entry.id]?.status))
        .sort((a, b) => Number(b.mtimeMs || 0) - Number(a.mtimeMs || 0))
        .slice(0, Math.max(1, Number(window) || DEFAULT_WINDOW));
    for (const entry of candidates) {
        const exact = parsed.normalized && parsed.normalized === entry.normalized;
        const similarity = exact ? 1 : jaccard(parsed.tokens, entry.tokens);
        if (similarity >= Number(threshold)) return { id: entry.id, similarity, exact, entry };
    }
    return null;
}

export function relationsForMemory(root = process.cwd(), id) {
    const entry = ensureMemoryGraph(root).entries[id];
    if (!entry) return { links: [], tags: [], meta: [], facts: [] };
    return { links: entry.links || [], tags: entry.tags || [], meta: entry.meta || [], facts: entry.facts || [] };
}

export function memoryGraphStatus(root = process.cwd()) {
    const graph = ensureMemoryGraph(root);
    const entries = Object.values(graph.entries);
    return {
        schema: graph.schema,
        entries: entries.length,
        links: entries.reduce((sum, entry) => sum + (entry.links?.length || 0), 0),
        tags: entries.reduce((sum, entry) => sum + (entry.tags?.length || 0), 0),
        meta: entries.reduce((sum, entry) => sum + (entry.meta?.length || 0), 0),
        facts: entries.reduce((sum, entry) => sum + (entry.facts?.length || 0), 0),
        canonical: "markdown",
        sidecar: ".ag-kit/memory/graph.json",
        rebuiltAt: graph.rebuiltAt || null,
    };
}
