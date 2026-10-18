import crypto from "node:crypto";
import path from "node:path";
import { appendJsonl, readJson, readJsonl, stateRoot, writeJson, writeJsonl } from "./project-state.js";

const profileFile = (root) => path.join(stateRoot(root), "profile", "profile.json");
const egressFile = (root) => path.join(stateRoot(root), "profile", "egress.jsonl");
const defaults = () => ({ schema: 1, enabled: true, inject: false, preferences: {} });
const load = (root) => readJson(profileFile(root), defaults()) || defaults();
const save = (root, profile) => writeJson(profileFile(root), profile);
const killed = () => ["1", "true", "yes", "on"].includes(String(process.env.AG_KIT_PROFILE_KILL || "").toLowerCase());
const idFor = (preference) => crypto.createHash("sha256").update(String(preference).trim().toLowerCase()).digest("hex").slice(0, 12);

export function profileStatus(root = process.cwd()) {
    const profile = load(root);
    const preferences = Object.values(profile.preferences);
    return { enabled: profile.enabled, inject: profile.inject, killSwitch: killed(), effectiveEnabled: profile.enabled && !killed(), effectiveInjection: profile.enabled && profile.inject && !killed(), candidate: preferences.filter((item) => !item.confirmed).length, confirmed: preferences.filter((item) => item.confirmed).length };
}

export function setPersonalization({ root = process.cwd(), enabled, inject } = {}) {
    const profile = load(root);
    if (enabled !== undefined) profile.enabled = Boolean(enabled);
    if (inject !== undefined) profile.inject = Boolean(inject);
    save(root, profile);
    return profileStatus(root);
}

export function learnPreference({ root = process.cwd(), preference, evidence, session = "manual" }) {
    const text = String(preference || "").trim();
    const proof = String(evidence || "").trim();
    if (!text) throw new Error("preference is required");
    if (!proof) throw new Error("verbatim evidence is required");
    const profile = load(root);
    const id = idFor(text);
    const item = profile.preferences[id] ||= { id, preference: text, evidence: [], sessions: [], confirmed: false, createdAt: new Date().toISOString() };
    if (!item.evidence.some((entry) => entry.text === proof && entry.session === session)) item.evidence.push({ text: proof, session, ts: new Date().toISOString() });
    item.sessions = [...new Set([...(item.sessions || []), session])];
    item.confirmed = item.sessions.length >= 2;
    item.updatedAt = new Date().toISOString();
    save(root, profile);
    return item;
}

export function profileForInjection({ root = process.cwd(), host = "" } = {}) {
    const profile = load(root);
    const status = profileStatus(root);
    if (!status.effectiveInjection) return { injected: false, reason: status.killSwitch ? "kill-switch" : !profile.enabled ? "disabled" : "injection-off", preferences: [] };
    const preferences = Object.values(profile.preferences).filter((item) => item.confirmed).map((item) => ({ id: item.id, preference: item.preference, evidence: item.evidence }));
    if (host && preferences.length) appendJsonl(egressFile(root), { ts: new Date().toISOString(), host, preferenceIds: preferences.map((item) => item.id) });
    return { injected: true, host: host || null, preferences };
}

export function forgetPreference({ root = process.cwd(), id = "all" } = {}) {
    const profile = load(root);
    const removed = id === "all" ? Object.keys(profile.preferences) : profile.preferences[id] ? [id] : [];
    if (id === "all") profile.preferences = {}; else delete profile.preferences[id];
    save(root, profile);
    const rows = readJsonl(egressFile(root)).filter((row) => !(row.preferenceIds || []).some((prefId) => removed.includes(prefId)));
    writeJsonl(egressFile(root), rows);
    return { removed, remaining: Object.keys(profile.preferences).length, egressRows: rows.length };
}

export function listEgress(root = process.cwd()) {
    return readJsonl(egressFile(root));
}
