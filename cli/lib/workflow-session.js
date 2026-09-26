import path from "node:path";
import { appendJsonl, readJson, stateRoot, writeJson } from "./project-state.js";

export const FLOW_PHASES = {
    quick: ["SHAPE", "PLAN", "EXECUTE", "VERIFY", "SHIP"],
    standard: ["SHAPE", "PLAN", "EXECUTE", "VERIFY", "AUDIT", "SHIP"],
    deep: ["SHAPE", "PLAN", "CONVERGE", "EXECUTE", "VERIFY", "AUDIT", "SHIP"],
};
const sessionFile = (root) => path.join(stateRoot(root), "flow", "session.json");
const historyFile = (root) => path.join(stateRoot(root), "flow", "history.jsonl");
const load = (root) => readJson(sessionFile(root), null);
const save = (root, session) => writeJson(sessionFile(root), session);

export function startFlow({ root = process.cwd(), goal, mode = "standard", force = false }) {
    const normalized = String(mode).toLowerCase();
    if (!FLOW_PHASES[normalized]) throw new Error(`unknown flow mode: ${mode}`);
    const previous = load(root);
    if (previous?.status === "active" && !force) throw new Error("an active AG Kit flow already exists; finish it or use --force");
    const phases = FLOW_PHASES[normalized];
    const session = { schema: 1, id: `flow-${Date.now()}`, goal: String(goal || "").trim(), mode: normalized, phases, phaseIndex: 0, currentPhase: phases[0], status: "active", startedAt: new Date().toISOString(), artifacts: {}, decisions: [], waves: [] };
    if (!session.goal) throw new Error("flow goal is required");
    save(root, session);
    appendJsonl(historyFile(root), { ts: new Date().toISOString(), event: "start", id: session.id, goal: session.goal, mode: session.mode });
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
        const tasks = Array.isArray(wave.tasks) ? wave.tasks.map(String).filter(Boolean) : [];
        const dependsOn = Array.isArray(wave.dependsOn) ? wave.dependsOn.map(String).filter(Boolean) : [];
        if (!tasks.length) throw new Error(`wave ${id} requires tasks`);
        return { id, mode, tasks, dependsOn };
    });
    for (const wave of normalized) for (const dep of wave.dependsOn) if (!ids.has(dep)) throw new Error(`wave ${wave.id} depends on unknown wave ${dep}`);
    session.waves = normalized;
    save(root, session);
    appendJsonl(historyFile(root), { ts: new Date().toISOString(), event: "waves", id: session.id, waves: normalized });
    return normalized;
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
    if (!session.artifacts[phase]?.summary) throw new Error(`phase ${phase} needs an artifact summary before approval`);
    if (phase === "CONVERGE" && !session.waves.length) throw new Error("DEEP CONVERGE requires an explicit wave table before approval");
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
