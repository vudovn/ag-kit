import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

export const SUPPORTED_RUNTIMES = ["antigravity", "claude", "codex", "gemini", "cursor", "windsurf", "copilot", "opencode"];

const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
const stateRoot = (root = process.cwd()) => path.join(path.resolve(root), ".ag-kit");
const slugify = (value) => String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 64) || "entry";

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
const tokenize = (value) => String(value).toLowerCase().match(/[\p{L}\p{N}_-]+/gu) || [];

export function initMemory(root = process.cwd()) {
    const dir = memoryDir(root);
    ensureDir(path.join(dir, "entries"));
    for (const [name, title] of [["DECISIONS.md", "Decisions"], ["CONVENTIONS.md", "Conventions"], ["HANDOFF.md", "Handoff"]]) {
        const file = path.join(dir, name);
        if (!fs.existsSync(file)) fs.writeFileSync(file, `# ${title}\n\n`);
    }
    return dir;
}

export function addMemory({ root = process.cwd(), text, kind = "learning", title = "" }) {
    if (!text?.trim()) throw new Error("memory text is required");
    const dir = initMemory(root);
    const id = `${Date.now()}-${slugify(title || text.slice(0, 48))}`;
    const file = path.join(dir, "entries", `${id}.md`);
    const body = `---\nid: ${id}\nkind: ${kind}\ncreated: ${new Date().toISOString()}\n---\n# ${title || kind}\n\n${text.trim()}\n`;
    fs.writeFileSync(file, body);
    appendReceipt(root, "memory", { action: "add", id, kind, file: path.relative(root, file) });
    return { id, file };
}

export function recallMemory({ root = process.cwd(), query = "", limit = 5 }) {
    const dir = initMemory(root);
    const terms = [...new Set(tokenize(query))];
    const files = fs.readdirSync(path.join(dir, "entries")).filter((name) => name.endsWith(".md"));
    const ranked = files.map((name) => {
        const file = path.join(dir, "entries", name);
        const text = fs.readFileSync(file, "utf8");
        const hay = text.toLowerCase();
        let score = 0;
        for (const term of terms) score += (hay.split(term).length - 1) * (term.length > 5 ? 2 : 1);
        return { file: path.relative(root, file), score, preview: text.replace(/^---[\s\S]*?---\s*/, "").trim().slice(0, 280) };
    }).filter((item) => terms.length === 0 || item.score > 0)
        .sort((a, b) => b.score - a.score || a.file.localeCompare(b.file))
        .slice(0, Number(limit));
    appendReceipt(root, "memory", { action: "recall", query, count: ranked.length });
    return ranked;
}

export function memoryStatus(root = process.cwd()) {
    const dir = initMemory(root);
    const entries = fs.readdirSync(path.join(dir, "entries")).filter((name) => name.endsWith(".md")).length;
    return { root: path.relative(root, dir) || ".", entries, canonical: "markdown", index: "rebuildable-keyword-scan" };
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
    if (["package.json", "Cargo.toml", "pyproject.toml", "go.mod"].some((name) => fs.existsSync(path.join(root, name)))) return "software";
    return "software";
}

export function initTeam({ root = process.cwd(), archetype = "auto", name = "default", brief = "" }) {
    const selected = archetype === "auto" ? inferArchetype(root) : archetype;
    const roles = archetypes[selected];
    if (!roles) throw new Error(`unknown archetype: ${selected}`);
    const teamDir = path.join(stateRoot(root), "team");
    const agentDir = path.join(stateRoot(root), "agents");
    ensureDir(teamDir); ensureDir(agentDir);
    const team = { schema: 1, name, archetype: selected, brief, roles, generatedAt: new Date().toISOString() };
    fs.writeFileSync(path.join(teamDir, "team.json"), `${JSON.stringify(team, null, 2)}\n`);
    for (const role of roles) {
        fs.writeFileSync(path.join(agentDir, `${role}.md`), `# ${role}\n\nProject role generated by AG Kit Team Assembly.\n\n## Mission\nWork only inside this role boundary. Read the project brief, shared core, loaded skills, and relevant packs before acting.\n\n## Coordination\nReturn evidence, artifacts, assumptions, and handoff notes. Never claim another role's verification as your own.\n`);
    }
    appendReceipt(root, "team", { action: "init", name, archetype: selected, roles });
    return team;
}

export const auditRoster = [
    { id: "codex", lineage: "openai", command: "codex", args: ["--version"] },
    { id: "gemini", lineage: "google", command: "gemini", args: ["--version"] },
    { id: "qwen", lineage: "alibaba", command: "qwen", args: ["--version"] },
    { id: "opencode", lineage: "oss", command: "opencode", args: ["--version"] },
    { id: "aider", lineage: "oss", command: "aider", args: ["--version"] },
    { id: "copilot", lineage: "openai", command: "copilot", args: ["--version"] },
];

export function probeRoster() {
    return auditRoster.map((item) => {
        const result = spawnSync(item.command, item.args, { encoding: "utf8", timeout: 3000, shell: false });
        return { ...item, available: !result.error && result.status === 0, version: (result.stdout || result.stderr || "").trim().split(/\r?\n/)[0] || null };
    });
}

export function prepareAudit({ root = process.cwd(), target = "." }) {
    const probes = probeRoster();
    const available = probes.filter((item) => item.available);
    const lineages = [...new Set(available.map((item) => item.lineage))];
    const receipt = appendReceipt(root, "cross-audit", { action: "probe", target, available: available.map((item) => item.id), lineages });
    return { target, probes, lineages, receipt, status: lineages.length >= 2 ? "ready" : "degraded" };
}

export function runPreflight({ root = process.cwd(), gates } = {}) {
    const selected = gates || [
        { name: "v2-architecture", command: "npm", args: ["run", "check:v2"], blocking: true },
        { name: "legacy-registry", command: "npm", args: ["run", "check:agents"], blocking: true },
        { name: "toolkit-tests", command: "npm", args: ["run", "test:toolkit"], blocking: true },
        { name: "antigravity-doctor", command: "npm", args: ["run", "check:antigravity"], blocking: true },
        { name: "antigravity-tests", command: "npm", args: ["run", "test:antigravity"], blocking: true },
        { name: "runtime-projections", command: "npm", args: ["run", "build:runtimes"], blocking: true },
    ];
    const results = selected.map((gate) => {
        const started = Date.now();
        const result = spawnSync(gate.command, gate.args, { cwd: root, encoding: "utf8", stdio: "pipe", timeout: 240000, shell: false });
        return { name: gate.name, blocking: gate.blocking, ok: result.status === 0, durationMs: Date.now() - started, exitCode: result.status, output: (result.stdout || result.stderr || "").trim().slice(-1200) };
    });
    const passed = !results.some((item) => item.blocking && !item.ok);
    appendReceipt(root, "preflight", { action: "run", passed, results: results.map(({ output, ...item }) => item) });
    return { passed, results };
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
    const regex = new RegExp(`${start.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[\\s\\S]*?${end.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`, "m");
    const next = regex.test(previous) ? previous.replace(regex, block) : `${previous.trim()}${previous.trim() ? "\n\n" : ""}${block}\n`;
    fs.writeFileSync(file, next);
};

export function installRuntime({ sourceRoot, targetRoot = process.cwd(), runtime }) {
    if (!SUPPORTED_RUNTIMES.includes(runtime)) throw new Error(`unsupported runtime: ${runtime}`);
    const source = path.resolve(sourceRoot);
    const target = path.resolve(targetRoot);
    const shared = path.join(source, "shared");
    if (!fs.existsSync(shared)) throw new Error(`shared source not found at ${shared}`);
    const core = fs.readFileSync(path.join(shared, "core", "CORE.md"), "utf8");

    copyDir(path.join(shared, "core"), path.join(target, ".ag-kit", "core"));
    copyDir(path.join(shared, "flows"), path.join(target, ".ag-kit", "flows"));
    copyDir(path.join(source, "packs"), path.join(target, ".ag-kit", "packs"));
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

    appendReceipt(target, "runtime", { action: "install", runtime });
    return { runtime, target, state: path.join(target, ".ag-kit") };
}
