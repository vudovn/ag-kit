import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { resolveSafeProjectRoot, stateRoot } from "./project-state.js";

const require = createRequire(import.meta.url);
export const SUPPORTED_RUNTIMES = ["antigravity", "claude", "codex", "gemini", "cursor", "windsurf", "copilot", "opencode"];

const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
const slugify = (value) => String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 64) || "entry";
const tokenize = (value) => String(value).toLowerCase().match(/[\p{L}\p{N}_-]+/gu) || [];
const truncate = (value, max = 80000) => String(value || "").slice(0, max);

export const parseArgs = (argv) => {
    const out = { _: [] };
    for (let i = 0; i < argv.length; i += 1) {
        const item = argv[i];
        if (!item.startsWith("--")) { out._.push(item); continue; }
        const key = item.slice(2);
        const next = argv[i + 1];
        if (next && !next.startsWith("--")) { out[key] = next; i += 1; }
        else out[key] = true;
    }
    return out;
};

export const appendReceipt = (root, type, data) => {
    const dir = path.join(stateRoot(root), "receipts");
    ensureDir(dir);
    const record = { ts: new Date().toISOString(), type, ...data };
    fs.appendFileSync(path.join(dir, `${type}.jsonl`), `${JSON.stringify(record)}\n`);
    return record;
};

const memoryDir = (root) => path.join(stateRoot(root), "memory");
const memoryEntriesDir = (root) => path.join(memoryDir(root), "entries");
const memoryIndexFile = (root) => path.join(memoryDir(root), "index.sqlite");

const openSqlite = (file) => {
    try {
        const { DatabaseSync } = require("node:sqlite");
        ensureDir(path.dirname(file));
        return new DatabaseSync(file);
    } catch {
        return null;
    }
};

export function initMemory(root = process.cwd()) {
    const dir = memoryDir(root);
    ensureDir(memoryEntriesDir(root));
    for (const [name, title] of [["DECISIONS.md", "Decisions"], ["CONVENTIONS.md", "Conventions"], ["HANDOFF.md", "Handoff"]]) {
        const file = path.join(dir, name);
        if (!fs.existsSync(file)) fs.writeFileSync(file, `# ${title}\n\n`);
    }
    return dir;
}

const entryFiles = (root) => {
    initMemory(root);
    return fs.readdirSync(memoryEntriesDir(root)).filter((name) => name.endsWith(".md")).sort();
};

export function rebuildMemoryIndex(root = process.cwd()) {
    initMemory(root);
    const db = openSqlite(memoryIndexFile(root));
    if (!db) return { available: false, engine: "markdown-scan", entries: entryFiles(root).length };
    const entries = entryFiles(root).map((name) => ({ file: name, body: fs.readFileSync(path.join(memoryEntriesDir(root), name), "utf8") }));
    let engine = "sqlite";
    try {
        db.exec("DROP TABLE IF EXISTS memory_fts; CREATE VIRTUAL TABLE memory_fts USING fts5(file UNINDEXED, body);");
        const insert = db.prepare("INSERT INTO memory_fts(file, body) VALUES (?, ?)");
        for (const entry of entries) insert.run(entry.file, entry.body);
        engine = "sqlite-fts5";
    } catch {
        db.exec("DROP TABLE IF EXISTS memory_entries; CREATE TABLE memory_entries(file TEXT PRIMARY KEY, body TEXT NOT NULL);");
        const insert = db.prepare("INSERT OR REPLACE INTO memory_entries(file, body) VALUES (?, ?)");
        for (const entry of entries) insert.run(entry.file, entry.body);
    } finally {
        db.close();
    }
    appendReceipt(root, "memory", { action: "reindex", engine, entries: entries.length });
    return { available: true, engine, entries: entries.length, file: path.relative(root, memoryIndexFile(root)) };
}

const indexStale = (root) => {
    const index = memoryIndexFile(root);
    if (!fs.existsSync(index)) return true;
    const indexMtime = fs.statSync(index).mtimeMs;
    return entryFiles(root).some((name) => fs.statSync(path.join(memoryEntriesDir(root), name)).mtimeMs > indexMtime);
};

export function addMemory({ root = process.cwd(), text, kind = "learning", title = "" }) {
    if (!text?.trim()) throw new Error("memory text is required");
    initMemory(root);
    const id = `${Date.now()}-${slugify(title || text.slice(0, 48))}`;
    const file = path.join(memoryEntriesDir(root), `${id}.md`);
    const body = `---\nid: ${id}\nkind: ${kind}\ncreated: ${new Date().toISOString()}\n---\n# ${title || kind}\n\n${text.trim()}\n`;
    fs.writeFileSync(file, body);
    const index = rebuildMemoryIndex(root);
    appendReceipt(root, "memory", { action: "add", id, kind, file: path.relative(root, file), index: index.engine });
    return { id, file, index: index.engine };
}

const scanRecall = ({ root, query, limit }) => {
    const terms = [...new Set(tokenize(query))];
    return entryFiles(root).map((name) => {
        const file = path.join(memoryEntriesDir(root), name);
        const text = fs.readFileSync(file, "utf8");
        const hay = text.toLowerCase();
        let score = 0;
        for (const term of terms) score += (hay.split(term).length - 1) * (term.length > 5 ? 2 : 1);
        return { file: path.relative(root, file), score, preview: text.replace(/^---[\s\S]*?---\s*/, "").trim().slice(0, 280) };
    }).filter((item) => terms.length === 0 || item.score > 0)
      .sort((a, b) => b.score - a.score || a.file.localeCompare(b.file))
      .slice(0, Number(limit));
};

const sqliteRecall = ({ root, query, limit }) => {
    if (indexStale(root)) rebuildMemoryIndex(root);
    const db = openSqlite(memoryIndexFile(root));
    if (!db) return null;
    try {
        const terms = [...new Set(tokenize(query))];
        if (!terms.length) return null;
        let rows;
        try {
            const match = terms.map((term) => `"${term.replaceAll('"', '""')}"*`).join(" AND ");
            rows = db.prepare("SELECT file, body FROM memory_fts WHERE memory_fts MATCH ? LIMIT ?").all(match, Number(limit));
        } catch {
            const clauses = terms.map(() => "lower(body) LIKE ?").join(" AND ");
            rows = db.prepare(`SELECT file, body FROM memory_entries WHERE ${clauses} LIMIT ?`).all(...terms.map((term) => `%${term}%`), Number(limit));
        }
        return rows.map((row, index) => ({ file: path.join(".ag-kit", "memory", "entries", row.file), score: Math.max(1, Number(limit) - index), preview: String(row.body).replace(/^---[\s\S]*?---\s*/, "").trim().slice(0, 280) }));
    } catch {
        return null;
    } finally {
        db.close();
    }
};

export function recallMemory({ root = process.cwd(), query = "", limit = 5 }) {
    initMemory(root);
    const indexed = sqliteRecall({ root, query, limit });
    const ranked = indexed ?? scanRecall({ root, query, limit });
    appendReceipt(root, "memory", { action: "recall", query, count: ranked.length, engine: indexed ? "sqlite" : "markdown-scan" });
    return ranked;
}

export function memoryStatus(root = process.cwd()) {
    initMemory(root);
    const entries = entryFiles(root).length;
    const db = openSqlite(memoryIndexFile(root));
    let index = "markdown-scan";
    if (db) {
        try {
            const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all().map((row) => row.name);
            index = tables.includes("memory_fts") ? "sqlite-fts5" : tables.includes("memory_entries") ? "sqlite" : "sqlite-empty";
        } finally { db.close(); }
    }
    return { root: path.relative(root, memoryDir(root)) || ".", entries, canonical: "markdown", index };
}

const archetypes = {
    software: ["architect", "builder", "security-reviewer", "qa-reviewer"],
    web: ["product-architect", "frontend-builder", "backend-builder", "qa-reviewer"],
    research: ["investigator", "synthesist", "fact-checker"],
    content: ["strategist", "writer", "editor", "fact-checker"],
    game: ["game-architect", "gameplay-builder", "systems-builder", "qa-reviewer"],
    operations: ["operator", "automation-builder", "risk-reviewer"],
};

export function inferArchetype(root = process.cwd()) {
    if (fs.existsSync(path.join(root, "package.json"))) {
        try {
            const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
            const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
            if (Object.keys(deps).some((name) => ["next", "react", "vue", "nuxt", "@angular/core", "svelte"].includes(name))) return "web";
        } catch {}
        return "software";
    }
    if (["Cargo.toml", "pyproject.toml", "go.mod"].some((name) => fs.existsSync(path.join(root, name)))) return "software";
    if (fs.existsSync(path.join(root, "Assets")) || fs.existsSync(path.join(root, "ProjectSettings"))) return "game";
    return "software";
}

export function initTeam({ root = process.cwd(), archetype = "auto", name = "default", brief = "" }) {
    const selected = archetype === "auto" ? inferArchetype(root) : archetype;
    const roles = archetypes[selected];
    if (!roles) throw new Error(`unknown archetype: ${selected}`);
    const teamDir = path.join(stateRoot(root), "team");
    const agentDir = path.join(stateRoot(root), "agents");
    ensureDir(teamDir); ensureDir(agentDir);
    for (const file of fs.readdirSync(agentDir)) if (file.endsWith(".md")) fs.rmSync(path.join(agentDir, file));
    const team = { schema: 1, name, archetype: selected, brief, roles, generatedAt: new Date().toISOString() };
    fs.writeFileSync(path.join(teamDir, "team.json"), `${JSON.stringify(team, null, 2)}\n`);
    for (const role of roles) {
        fs.writeFileSync(path.join(agentDir, `${role}.md`), `# ${role}\n\nProject role generated by AG Kit Team Assembly.\n\n## Project brief\n${brief || "Read the project structure and current task before acting."}\n\n## Mission\nWork only inside this role boundary. Read the shared core, loaded skills, relevant packs, and project memory before acting.\n\n## Coordination\nReturn evidence, artifacts, assumptions, and handoff notes. Never claim another role's verification as your own.\n`);
    }
    appendReceipt(root, "team", { action: "init", name, archetype: selected, roles });
    return team;
}

export const auditRoster = [
    { id: "codex", lineage: "openai", command: "codex", probe: ["--version"], run: (prompt) => ["exec", prompt] },
    { id: "gemini", lineage: "google", command: "gemini", probe: ["--version"], run: (prompt) => ["-p", prompt, "--output-format", "json"] },
    { id: "qwen", lineage: "alibaba", command: "qwen", probe: ["--version"], run: (prompt) => ["--prompt", prompt, "--output-format", "json"] },
    { id: "opencode", lineage: "oss", command: "opencode", probe: ["--version"], run: (prompt) => ["run", "--standalone", prompt] },
    { id: "copilot", lineage: "openai", command: "copilot", probe: ["--version"], run: null },
    { id: "aider", lineage: "oss", command: "aider", probe: ["--version"], run: null },
];

export function probeRoster() {
    return auditRoster.map((item) => {
        const result = spawnSync(item.command, item.probe, { encoding: "utf8", timeout: 3000, shell: false });
        return { id: item.id, lineage: item.lineage, command: item.command, executable: Boolean(item.run), available: !result.error && result.status === 0, version: (result.stdout || result.stderr || "").trim().split(/\r?\n/)[0] || null };
    });
}

export function snapshotAuditTarget({ root = process.cwd(), target = "." }) {
    const resolvedRoot = path.resolve(root);
    if (target === "." || target === "diff") {
        const diff = spawnSync("git", ["diff", "--no-ext-diff", "--unified=3", "HEAD"], { cwd: resolvedRoot, encoding: "utf8", timeout: 10000, shell: false });
        const staged = spawnSync("git", ["diff", "--cached", "--no-ext-diff", "--unified=3"], { cwd: resolvedRoot, encoding: "utf8", timeout: 10000, shell: false });
        const content = truncate(`${staged.stdout || ""}\n${diff.stdout || ""}`.trim());
        return { kind: "diff", label: "working tree diff", content: content || "(no diff)" };
    }
    const absolute = path.resolve(resolvedRoot, target);
    if (!absolute.startsWith(`${resolvedRoot}${path.sep}`) && absolute !== resolvedRoot) throw new Error("audit target must stay inside project root");
    if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) throw new Error(`audit target not found or not a file: ${target}`);
    return { kind: "file", label: path.relative(resolvedRoot, absolute), content: truncate(fs.readFileSync(absolute, "utf8")) };
}

const reviewerPrompt = (snapshot) => `You are an independent read-only reviewer. Review ONLY the snapshot below. Do not attempt to edit files, run tools, or assume access to the source repository. Focus on concrete correctness, security, regression, test, and maintainability risks. Return concise findings grouped as BLOCKING, IMPORTANT, and OPTIONAL. If no concrete issue exists, say so.\n\nTARGET: ${snapshot.label}\n\n--- SNAPSHOT START ---\n${snapshot.content}\n--- SNAPSHOT END ---`;

const normalizeReviewerOutput = (id, stdout) => {
    const raw = String(stdout || "").trim();
    if (!raw) return "";
    if (["gemini", "qwen"].includes(id)) {
        try {
            const data = JSON.parse(raw);
            return String(data.response ?? data.result ?? data.output ?? raw);
        } catch {}
    }
    return raw;
};

export function runCrossAudit({ root = process.cwd(), target = ".", reviewers = 2, timeoutMs = 180000 }) {
    const snapshot = snapshotAuditTarget({ root, target });
    const probes = probeRoster();
    const byId = new Map(auditRoster.map((item) => [item.id, item]));
    const selected = [];
    const lineages = new Set();
    for (const probe of probes) {
        if (!probe.available || !probe.executable || lineages.has(probe.lineage)) continue;
        selected.push(byId.get(probe.id)); lineages.add(probe.lineage);
        if (selected.length >= Math.max(1, Math.min(3, Number(reviewers)))) break;
    }
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-"));
    try {
        const prompt = reviewerPrompt(snapshot);
        const results = selected.map((reviewer) => {
            const started = Date.now();
            const result = spawnSync(reviewer.command, reviewer.run(prompt), { cwd: temp, encoding: "utf8", timeout: Number(timeoutMs), shell: false, env: process.env });
            return {
                reviewer: reviewer.id,
                lineage: reviewer.lineage,
                ok: !result.error && result.status === 0,
                exitCode: result.status,
                durationMs: Date.now() - started,
                output: normalizeReviewerOutput(reviewer.id, result.stdout),
                error: truncate(result.error?.message || result.stderr || "", 1200)
            };
        });
        const auditDir = path.join(stateRoot(root), "audits");
        ensureDir(auditDir);
        const reportPath = path.join(auditDir, `${Date.now()}-cross-audit.json`);
        const report = { schema: 1, target: snapshot.label, snapshotKind: snapshot.kind, reviewerCount: results.length, lineages: [...lineages], results };
        fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
        appendReceipt(root, "cross-audit", { action: "run", target: snapshot.label, reviewers: results.map((r) => r.reviewer), lineages: [...lineages], passedCalls: results.filter((r) => r.ok).length, report: path.relative(root, reportPath) });
        return { ...report, report: path.relative(root, reportPath), status: results.length >= 2 && results.every((r) => r.ok) ? "complete" : results.length ? "degraded" : "unavailable" };
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
}

export function prepareAudit({ root = process.cwd(), target = "." }) {
    const probes = probeRoster();
    const available = probes.filter((item) => item.available && item.executable);
    const lineages = [...new Set(available.map((item) => item.lineage))];
    const receipt = appendReceipt(root, "cross-audit", { action: "probe", target, available: available.map((item) => item.id), lineages });
    return { target, probes, lineages, receipt, status: lineages.length >= 2 ? "ready" : "degraded" };
}

const copyDir = (src, dst) => {
    if (!fs.existsSync(src)) return;
    ensureDir(path.dirname(dst));
    fs.cpSync(src, dst, { recursive: true, force: true });
};

const managedBlock = (file, label, content) => {
    ensureDir(path.dirname(file));
    const start = `<!-- AG-KIT:${label}:START -->`;
    const end = `<!-- AG-KIT:${label}:END -->`;
    const block = `${start}\n${content.trim()}\n${end}`;
    const previous = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
    const escape = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`${escape(start)}[\\s\\S]*?${escape(end)}`, "m");
    const next = regex.test(previous) ? previous.replace(regex, block) : `${previous.trim()}${previous.trim() ? "\n\n" : ""}${block}\n`;
    fs.writeFileSync(file, next);
};

export function installRuntime({ sourceRoot, targetRoot = process.cwd(), runtime }) {
    if (!SUPPORTED_RUNTIMES.includes(runtime)) throw new Error(`unsupported runtime: ${runtime}`);
    const source = path.resolve(sourceRoot);
    const target = resolveSafeProjectRoot(targetRoot);
    const shared = path.join(source, "shared");
    if (!fs.existsSync(shared)) throw new Error(`shared source not found at ${shared}`);
    const core = fs.readFileSync(path.join(shared, "core", "CORE.md"), "utf8");
    copyDir(path.join(shared, "core"), path.join(target, ".ag-kit", "core"));
    copyDir(path.join(shared, "flows"), path.join(target, ".ag-kit", "flows"));
    copyDir(path.join(source, "packs"), path.join(target, ".ag-kit", "packs"));
    ensureDir(stateRoot(target));
    fs.writeFileSync(path.join(stateRoot(target), "runtime.json"), `${JSON.stringify({ schema: 1, runtime, installedAt: new Date().toISOString() }, null, 2)}\n`);
    if (runtime === "antigravity") {
        copyDir(path.join(shared, "skills"), path.join(target, ".agents", "skills"));
        copyDir(path.join(shared, "agents"), path.join(target, ".agents", "agents"));
        ensureDir(path.join(target, ".agents", "rules"));
        fs.writeFileSync(path.join(target, ".agents", "rules", "ag-kit-v2.md"), `---\ntrigger: always_on\npriority: P0\nversion: 2.0.0\n---\n${core}`);
    } else if (runtime === "claude") {
        copyDir(path.join(shared, "skills"), path.join(target, ".claude", "skills"));
        copyDir(path.join(shared, "agents"), path.join(target, ".claude", "agents"));
        managedBlock(path.join(target, "CLAUDE.md"), "CORE", core);
    } else if (runtime === "codex") {
        copyDir(path.join(shared, "skills"), path.join(target, ".agents", "skills"));
        managedBlock(path.join(target, "AGENTS.md"), "CORE", core);
    } else if (runtime === "gemini") {
        copyDir(path.join(shared, "skills"), path.join(target, ".gemini", "skills"));
        managedBlock(path.join(target, "GEMINI.md"), "CORE", core);
    } else if (runtime === "cursor") {
        ensureDir(path.join(target, ".cursor", "rules"));
        fs.writeFileSync(path.join(target, ".cursor", "rules", "ag-kit.mdc"), `---\ndescription: AG Kit shared core\nalwaysApply: true\n---\n${core}`);
    } else if (runtime === "windsurf") {
        managedBlock(path.join(target, ".windsurfrules"), "CORE", core);
    } else if (runtime === "copilot") {
        managedBlock(path.join(target, ".github", "copilot-instructions.md"), "CORE", core);
    } else if (runtime === "opencode") {
        managedBlock(path.join(target, "AGENTS.md"), "CORE", core);
    }
    initMemory(target);
    appendReceipt(target, "runtime", { action: "install", runtime });
    return { runtime, target, state: path.join(target, ".ag-kit") };
}
