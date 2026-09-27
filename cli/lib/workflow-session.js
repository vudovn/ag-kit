import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { appendJsonl, readJson, stateRoot, writeJson } from "./project-state.js";

const moduleDir = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_FLOW_CONTRACT = {
    schema: 2,
    name: "development",
    modes: {
        quick: ["FRAME", "PLAN", "EXECUTE", "VERIFY"],
        standard: ["FRAME", "SHAPE", "PLAN", "EXECUTE", "VERIFY", "SHIP"],
        deep: ["FRAME", "RECON", "SHAPE", "PLAN", "WAVES", "VERIFY", "CROSS_AUDIT", "SHIP"],
    },
    requirements: {
        default: ["artifact"],
        WAVES: ["wave-table", "waves-complete"],
    },
};

export const FLOW_PHASES = Object.freeze(
    Object.fromEntries(Object.entries(DEFAULT_FLOW_CONTRACT.modes).map(([mode, phases]) => [mode, Object.freeze([...phases])])),
);

const sessionFile = (root) => path.join(stateRoot(root), "flow", "session.json");
const historyFile = (root) => path.join(stateRoot(root), "flow", "history.jsonl");
const load = (root) => readJson(sessionFile(root), null);
const save = (root, session) => writeJson(sessionFile(root), session);

const contractCandidates = (root) => [
    path.join(stateRoot(root), "flows", "development.json"),
    path.resolve(moduleDir, "..", "..", "shared", "flows", "development.json"),
];

const validModes = (modes) => modes && typeof modes === "object"
    && ["quick", "standard", "deep"].every((mode) => Array.isArray(modes[mode]) && modes[mode].every((phase) => typeof phase === "string" && phase.trim()));

export function loadFlowContract(root = process.cwd()) {
    for (const file of contractCandidates(root)) {
        if (!fs.existsSync(file)) continue;
        try {
            const contract = JSON.parse(fs.readFileSync(file, "utf8"));
            if (!validModes(contract.modes)) continue;
            return { ...contract, source: path.relative(root, file) || file };
        } catch {}
    }
    return { ...DEFAULT_FLOW_CONTRACT, source: "builtin-fallback" };
}

const phaseRequirements = (contract, phase) => {
    const requirements = contract?.requirements && typeof contract.requirements === "object" ? contract.requirements : {};
    return [...new Set([...(requirements.default || ["artifact"]), ...(requirements[phase] || [])])];
};

export function startFlow({ root = process.cwd(), goal, mode = "standard", force = false }) {
    const normalized = String(mode).toLowerCase();
    const contract = loadFlowContract(root);
    if (!contract.modes[normalized]) throw new Error(`unknown flow mode: ${mode}`);
    const previous = load(root);
    if (previous?.status === "active" && !force) throw new Error("an active AG Kit flow already exists; finish it or use --force");
    const phases = [...contract.modes[normalized]];
    const session = {
        schema: 2,
        id: `flow-${Date.now()}`,
        goal: String(goal || "").trim(),
        mode: normalized,
        contract: { schema: contract.schema || 1, name: contract.name || "development", source: contract.source },
        phases,
        phaseIndex: 0,
        currentPhase: phases[0],
        status: "active",
        startedAt: new Date().toISOString(),
        artifacts: {},
        decisions: [],
        waves: [],
    };
    if (!session.goal) throw new Error("flow goal is required");
    save(root, session);
    appendJsonl(historyFile(root), { ts: new Date().toISOString(), event: "start", id: session.id, goal: session.goal, mode: session.mode, phases, contract: session.contract });
    return session;
}

export function flowStatus(root = process.cwd()) {
    return load(root) || { status: "idle", currentPhase: null, mode: null, goal: null };
}

export function recordFlowArtifact({ root = process.cwd(), summary, artifactPath = "" }) {
    const session = load(root);
    if (!session || session.status !== "active") throw new Error("no active AG Kit flow");
    const phase = session.currentPhase;
    session.artifacts[phase] = { summary: String(summary || "").trim(), path: artifactPath || null, recordedAt: new Date().toISOString() };
    if (!session.artifacts[phase].summary) throw new Error("artifact summary is required before a phase can advance");
    save(root, session);
    appendJsonl(historyFile(root), { ts: new Date().toISOString(), event: "artifact", id: session.id, phase, summary: session.artifacts[phase].summary, path: artifactPath || null });
    return session.artifacts[phase];
}

const assertAcyclicWaves = (waves) => {
    const byId = new Map(waves.map((wave) => [wave.id, wave]));
    const visiting = new Set();
    const visited = new Set();
    const visit = (id) => {
        if (visited.has(id)) return;
        if (visiting.has(id)) throw new Error(`wave dependency cycle detected at ${id}`);
        visiting.add(id);
        for (const dep of byId.get(id)?.dependsOn || []) visit(dep);
        visiting.delete(id);
        visited.add(id);
    };
    for (const wave of waves) visit(wave.id);
};

export function setWaveTable({ root = process.cwd(), waves }) {
    const session = load(root);
    if (!session || session.status !== "active") throw new Error("no active AG Kit flow");
    if (!Array.isArray(waves) || !waves.length) throw new Error("wave table must be a non-empty array");
    const ids = new Set();
    const normalized = waves.map((wave, index) => {
        const id = String(wave.id || `wave-${index + 1}`);
        if (ids.has(id)) throw new Error(`duplicate wave id: ${id}`);
        ids.add(id);
        const mode = wave.mode === "parallel" ? "parallel" : "sequential";
        const tasks = Array.isArray(wave.tasks) ? wave.tasks.map(String).map((item) => item.trim()).filter(Boolean) : [];
        const dependsOn = Array.isArray(wave.dependsOn) ? wave.dependsOn.map(String).map((item) => item.trim()).filter(Boolean) : [];
        if (!tasks.length) throw new Error(`wave ${id} requires tasks`);
        if (dependsOn.includes(id)) throw new Error(`wave ${id} cannot depend on itself`);
        return { id, mode, tasks, dependsOn, status: "pending", completedAt: null, summary: null };
    });
    for (const wave of normalized) for (const dep of wave.dependsOn) if (!ids.has(dep)) throw new Error(`wave ${wave.id} depends on unknown wave ${dep}`);
    assertAcyclicWaves(normalized);
    session.waves = normalized;
    save(root, session);
    appendJsonl(historyFile(root), { ts: new Date().toISOString(), event: "waves", id: session.id, waves: normalized });
    return normalized;
}

export function readyWaves(root = process.cwd()) {
    const session = load(root);
    if (!session || session.status !== "active") return [];
    const complete = new Set(session.waves.filter((wave) => wave.status === "completed").map((wave) => wave.id));
    return session.waves.filter((wave) => wave.status !== "completed" && wave.dependsOn.every((dep) => complete.has(dep)));
}

export function completeWave({ root = process.cwd(), id, summary }) {
    const session = load(root);
    if (!session || session.status !== "active") throw new Error("no active AG Kit flow");
    const wave = session.waves.find((item) => item.id === id);
    if (!wave) throw new Error(`unknown wave: ${id}`);
    if (wave.status === "completed") return wave;
    const complete = new Set(session.waves.filter((item) => item.status === "completed").map((item) => item.id));
    const blockedBy = wave.dependsOn.filter((dep) => !complete.has(dep));
    if (blockedBy.length) throw new Error(`wave ${id} is blocked by incomplete dependencies: ${blockedBy.join(", ")}`);
    const note = String(summary || "").trim();
    if (!note) throw new Error("wave completion summary is required");
    wave.status = "completed";
    wave.completedAt = new Date().toISOString();
    wave.summary = note;
    save(root, session);
    appendJsonl(historyFile(root), { ts: wave.completedAt, event: "wave-complete", id: session.id, wave: wave.id, summary: note });
    return wave;
}

export function decideFlow({ root = process.cwd(), approve, note = "" }) {
    const session = load(root);
    if (!session || session.status !== "active") throw new Error("no active AG Kit flow");
    const phase = session.currentPhase;
    const decision = { ts: new Date().toISOString(), phase, approved: Boolean(approve), note: String(note || "") };
    session.decisions.push(decision);
    if (!approve) {
        save(root, session);
        appendJsonl(historyFile(root), { event: "reject", id: session.id, ...decision });
        return session;
    }

    const contract = loadFlowContract(root);
    const requirements = phaseRequirements(contract, phase);
    if (requirements.includes("artifact") && !session.artifacts[phase]?.summary) throw new Error(`phase ${phase} needs an artifact summary before approval`);
    if (requirements.includes("wave-table") && !session.waves.length) throw new Error(`${phase} requires an explicit wave table before approval`);
    if (requirements.includes("waves-complete")) {
        const incomplete = session.waves.filter((wave) => wave.status !== "completed").map((wave) => wave.id);
        if (incomplete.length) throw new Error(`${phase} has incomplete waves: ${incomplete.join(", ")}`);
    }

    if (session.phaseIndex === session.phases.length - 1) {
        session.status = "completed";
        session.completedAt = new Date().toISOString();
        session.currentPhase = null;
    } else {
        session.phaseIndex += 1;
        session.currentPhase = session.phases[session.phaseIndex];
    }
    save(root, session);
    appendJsonl(historyFile(root), { event: "approve", id: session.id, ...decision, nextPhase: session.currentPhase, status: session.status });
    return session;
}
