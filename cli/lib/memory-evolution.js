import fs from "node:fs";
import path from "node:path";
import { addMemory, appendReceipt, recallMemory } from "./v2-engine.js";
import { ensureDir, readJson, stateRoot, writeJson } from "./project-state.js";
import { findNearDuplicate, indexMemoryGraph, memoryGraphStatus, rebuildMemoryGraph, relationsForMemory } from "./memory-graph.js";

const evolutionFile = (root) => path.join(stateRoot(root), "memory", "evolution.json");
const entriesDir = (root) => path.join(stateRoot(root), "memory", "entries");
const defaultState = () => ({ schema: 1, entries: {} });
const load = (root) => readJson(evolutionFile(root), defaultState()) || defaultState();
const save = (root, state) => writeJson(evolutionFile(root), state);
const unique = (values) => [...new Set(values.filter(Boolean))];
const idFromFile = (file) => path.basename(String(file), ".md");
const safeDate = (value) => { const ms = Date.parse(value || ""); return Number.isFinite(ms) ? ms : null; };

const maybePromote = (entry) => {
    if (entry.status === "candidate" && Number(entry.references || 0) >= 3 && unique(entry.sessions || []).length >= 2) {
        entry.status = "durable";
        entry.promotedAt = new Date().toISOString();
        return true;
    }
    return false;
};

export function addEvolvingMemory({ root = process.cwd(), text, kind = "learning", title = "", session = "manual", validFrom = "", validTo = "", durable = false, supersedes = "", dedup = true }) {
    if (dedup && kind !== "handoff") {
        const duplicate = findNearDuplicate({ root, text, kind });
        if (duplicate) {
            const evolution = referenceMemory({ root, id: duplicate.id, session });
            appendReceipt(root, "memory-evolution", { action: "dedupe", id: duplicate.id, kind, session, similarity: duplicate.similarity, exact: duplicate.exact });
            return {
                id: duplicate.id,
                file: path.join(entriesDir(root), `${duplicate.id}.md`),
                index: "deduped",
                deduped: true,
                similarity: duplicate.similarity,
                evolution,
                relations: relationsForMemory(root, duplicate.id),
            };
        }
    }

    const result = addMemory({ root, text, kind, title });
    const state = load(root);
    state.entries[result.id] = {
        id: result.id,
        file: path.relative(root, result.file),
        kind,
        title: title || kind,
        createdAt: new Date().toISOString(),
        validFrom: validFrom || null,
        validTo: validTo || null,
        status: durable ? "durable" : "candidate",
        references: 1,
        sessions: unique([session]),
        supersedes: supersedes || null,
        supersededBy: null,
    };
    save(root, state);
    const relations = indexMemoryGraph(root, result.id, { kind, title: title || kind });
    appendReceipt(root, "memory-evolution", { action: "add", id: result.id, status: state.entries[result.id].status, session, validFrom: validFrom || null, validTo: validTo || null, links: relations.links.length, tags: relations.tags.length, facts: relations.facts.length });
    return { ...result, deduped: false, evolution: state.entries[result.id], relations: relationsForMemory(root, result.id) };
}

export function referenceMemory({ root = process.cwd(), id, session = "manual" }) {
    const state = load(root);
    let entry = state.entries[id];
    if (!entry) {
        const file = path.join(entriesDir(root), `${id}.md`);
        if (!fs.existsSync(file)) throw new Error(`memory entry not found: ${id}`);
        entry = state.entries[id] = { id, file: path.relative(root, file), kind: "legacy", title: id, createdAt: fs.statSync(file).birthtime.toISOString(), validFrom: null, validTo: null, status: "durable", references: 0, sessions: [], supersedes: null, supersededBy: null };
    }
    entry.references = Number(entry.references || 0) + 1;
    entry.sessions = unique([...(entry.sessions || []), session]);
    entry.lastReferencedAt = new Date().toISOString();
    const promoted = maybePromote(entry);
    save(root, state);
    appendReceipt(root, "memory-evolution", { action: "reference", id, session, references: entry.references, sessions: entry.sessions.length, promoted });
    return { ...entry };
}

const validAt = (entry, atMs) => {
    if (["archived", "superseded"].includes(entry?.status)) return false;
    if (!entry) return true;
    const from = safeDate(entry.validFrom);
    const to = safeDate(entry.validTo);
    if (from !== null && atMs < from) return false;
    if (to !== null && atMs > to) return false;
    return true;
};

export function recallEvolvingMemory({ root = process.cwd(), query = "", limit = 5, at = new Date().toISOString(), session = "manual" }) {
    const state = load(root);
    const atMs = safeDate(at) ?? Date.now();
    const base = recallMemory({ root, query, limit: Math.max(20, Number(limit) * 5) });
    const ranked = base.flatMap((item) => {
        const id = idFromFile(item.file);
        const meta = state.entries[id];
        if (!validAt(meta, atMs)) return [];
        const createdMs = safeDate(meta?.createdAt) ?? atMs;
        const ageDays = Math.max(0, (atMs - createdMs) / 86400000);
        const recency = Math.exp(-ageDays / 90);
        const statusBoost = meta?.status === "durable" ? 1.2 : 1;
        return [{ ...item, id, status: meta?.status || "legacy", validFrom: meta?.validFrom || null, validTo: meta?.validTo || null, relations: relationsForMemory(root, id), score: Number(item.score || 1) * (1 + recency) * statusBoost }];
    }).sort((a, b) => b.score - a.score).slice(0, Number(limit));
    for (const item of ranked) referenceMemory({ root, id: item.id, session });
    return ranked;
}

export function supersedeMemory({ root = process.cwd(), id, text, title = "", kind = "decision", session = "manual", validFrom = "", validTo = "" }) {
    const state = load(root);
    if (!state.entries[id] && !fs.existsSync(path.join(entriesDir(root), `${id}.md`))) throw new Error(`memory entry not found: ${id}`);
    const next = addEvolvingMemory({ root, text, title, kind, session, validFrom, validTo, durable: true, supersedes: id, dedup: false });
    const refreshed = load(root);
    refreshed.entries[id] = refreshed.entries[id] || { id, file: path.join(".ag-kit", "memory", "entries", `${id}.md`), status: "durable", references: 0, sessions: [] };
    refreshed.entries[id].status = "superseded";
    refreshed.entries[id].supersededBy = next.id;
    save(root, refreshed);
    appendReceipt(root, "memory-evolution", { action: "supersede", id, supersededBy: next.id });
    return { old: refreshed.entries[id], replacement: next.evolution };
}

export function runMemoryDream({ root = process.cwd(), staleDays = 180 } = {}) {
    const state = load(root);
    const now = Date.now();
    const promoted = [];
    const archived = [];
    const duplicateGroups = new Map();
    ensureDir(entriesDir(root));
    for (const [id, entry] of Object.entries(state.entries)) {
        if (maybePromote(entry)) promoted.push(id);
        const created = safeDate(entry.createdAt) ?? now;
        if (entry.status === "candidate" && Number(entry.references || 0) <= 1 && (now - created) / 86400000 >= Number(staleDays)) {
            entry.status = "archived";
            entry.archivedAt = new Date().toISOString();
            archived.push(id);
        }
        const file = path.join(entriesDir(root), `${id}.md`);
        if (fs.existsSync(file) && !["archived", "superseded"].includes(entry.status)) {
            const body = fs.readFileSync(file, "utf8").replace(/^---[\s\S]*?---\s*/, "").replace(/\s+/g, " ").trim().toLowerCase();
            if (body) {
                const group = duplicateGroups.get(body) || [];
                group.push(id);
                duplicateGroups.set(body, group);
            }
        }
    }
    const deduplicated = [];
    for (const ids of duplicateGroups.values()) {
        if (ids.length < 2) continue;
        const keep = ids.sort((a, b) => String(state.entries[b]?.createdAt || "").localeCompare(String(state.entries[a]?.createdAt || "")))[0];
        for (const id of ids) if (id !== keep) {
            state.entries[id].status = "superseded";
            state.entries[id].supersededBy = keep;
            deduplicated.push(id);
        }
    }
    state.lastDreamAt = new Date().toISOString();
    save(root, state);
    const graph = rebuildMemoryGraph(root);
    appendReceipt(root, "memory-evolution", { action: "dream", promoted, archived, deduplicated, staleDays: Number(staleDays), graphEntries: Object.keys(graph.entries).length });
    return { promoted, archived, deduplicated, entries: Object.keys(state.entries).length, lastDreamAt: state.lastDreamAt };
}

export function memoryEvolutionStatus(root = process.cwd()) {
    const state = load(root);
    const counts = { candidate: 0, durable: 0, superseded: 0, archived: 0 };
    for (const entry of Object.values(state.entries)) counts[entry.status] = (counts[entry.status] || 0) + 1;
    return { schema: state.schema, counts, lastDreamAt: state.lastDreamAt || null, graph: memoryGraphStatus(root) };
}
