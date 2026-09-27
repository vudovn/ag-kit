import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { recallMemory } from "./v2-engine.js";
import { readJson } from "./project-state.js";

const homeRoot = () => path.resolve(process.env.AG_KIT_HOME || path.join(os.homedir(), ".ag-kit"));
const registryFile = () => path.join(homeRoot(), "state", "projects.json");
const defaultRegistry = () => ({ schema: 1, projects: [] });
const disabled = () => process.env.AG_KIT_MINIMAL === "1" || process.env.AG_KIT_NO_CROSS_PROJECT === "1";
const markerNames = [".git", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", ".ag-kit/project"];
const safeDate = (value) => { const ms = Date.parse(value || ""); return Number.isFinite(ms) ? ms : null; };
const projectId = (root) => crypto.createHash("sha256").update(root).digest("hex").slice(0, 16);
const inside = (child, parent) => child === parent || child.startsWith(`${parent}${path.sep}`);

const userHome = () => {
  try { return fs.realpathSync(os.homedir()); } catch { return path.resolve(os.homedir()); }
};

const loadRegistry = () => {
  const value = readJson(registryFile(), defaultRegistry());
  return value?.schema === 1 && Array.isArray(value.projects) ? value : defaultRegistry();
};

const saveRegistry = (registry) => {
  const file = registryFile();
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  fs.writeFileSync(file, `${JSON.stringify(registry, null, 2)}\n`, { mode: 0o600 });
  try { fs.chmodSync(file, 0o600); } catch {}
  return registry;
};

export function validateRegisteredProject(root, { allowOutsideHome = false } = {}) {
  const requested = path.resolve(root || process.cwd());
  if (!fs.existsSync(requested)) return { ok: false, reason: "project does not exist", requested };
  let real;
  try { real = fs.realpathSync(requested); } catch { return { ok: false, reason: "project realpath failed", requested }; }
  const parsed = path.parse(real);
  if (real === parsed.root) return { ok: false, reason: "filesystem root cannot be registered", real };
  const home = userHome();
  if (real === home) return { ok: false, reason: "home directory cannot be registered as a project", real };
  if (!allowOutsideHome && !inside(real, home)) return { ok: false, reason: "project is outside home; pass --allow-outside-home explicitly", real };
  const marker = markerNames.find((name) => fs.existsSync(path.join(real, name)));
  if (!marker) return { ok: false, reason: "no project marker found; initialize the project before registering it", real };
  return { ok: true, real, marker, id: projectId(real), name: path.basename(real) || "project" };
}

export function registerProject({ root = process.cwd(), allowOutsideHome = false } = {}) {
  const checked = validateRegisteredProject(root, { allowOutsideHome });
  if (!checked.ok) throw new Error(checked.reason);
  const registry = loadRegistry();
  const now = new Date().toISOString();
  const existing = registry.projects.find((item) => item.id === checked.id || item.root === checked.real);
  if (existing) {
    existing.root = checked.real;
    existing.name = checked.name;
    existing.marker = checked.marker;
    existing.lastSeenAt = now;
    existing.allowOutsideHome = Boolean(allowOutsideHome);
  } else {
    registry.projects.push({ id: checked.id, root: checked.real, name: checked.name, marker: checked.marker, registeredAt: now, lastSeenAt: now, allowOutsideHome: Boolean(allowOutsideHome) });
  }
  saveRegistry(registry);
  return { registered: true, id: checked.id, name: checked.name, root: checked.real, marker: checked.marker };
}

export function unregisterProject({ root = process.cwd() } = {}) {
  const requested = path.resolve(root);
  let real = requested;
  try { real = fs.realpathSync(requested); } catch {}
  const registry = loadRegistry();
  const before = registry.projects.length;
  registry.projects = registry.projects.filter((item) => item.root !== real && item.id !== projectId(real));
  saveRegistry(registry);
  return { removed: before - registry.projects.length, root: real };
}

export function listRegisteredProjects() {
  const registry = loadRegistry();
  return registry.projects.map((item) => {
    const checked = validateRegisteredProject(item.root, { allowOutsideHome: Boolean(item.allowOutsideHome) });
    return { id: item.id, name: item.name, root: item.root, registeredAt: item.registeredAt, status: checked.ok ? "live" : "stale", reason: checked.ok ? null : checked.reason };
  });
}

const validAt = (meta, atMs) => {
  if (["archived", "superseded"].includes(meta?.status)) return false;
  if (!meta) return true;
  const from = safeDate(meta.validFrom);
  const to = safeDate(meta.validTo);
  if (from !== null && atMs < from) return false;
  if (to !== null && atMs > to) return false;
  return true;
};

export function searchAcrossProjects({ query = "", limit = 10, at = new Date().toISOString(), currentRoot = "" } = {}) {
  if (disabled()) return { disabled: true, reason: process.env.AG_KIT_MINIMAL === "1" ? "AG_KIT_MINIMAL" : "AG_KIT_NO_CROSS_PROJECT", results: [] };
  if (!String(query).trim()) return { disabled: false, results: [] };
  const registry = loadRegistry();
  const atMs = safeDate(at) ?? Date.now();
  const current = currentRoot ? path.resolve(currentRoot) : "";
  const results = [];
  for (const item of registry.projects.slice(0, 100)) {
    const checked = validateRegisteredProject(item.root, { allowOutsideHome: Boolean(item.allowOutsideHome) });
    if (!checked.ok) continue;
    if (current && checked.real === current) continue;
    const memoryRoot = path.join(checked.real, ".ag-kit", "memory");
    if (!fs.existsSync(memoryRoot)) continue;
    const evolution = readJson(path.join(memoryRoot, "evolution.json"), { entries: {} }) || { entries: {} };
    const local = recallMemory({ root: checked.real, query, limit: Math.max(10, Number(limit)) });
    for (const hit of local) {
      const id = path.basename(String(hit.file || ""), ".md");
      const meta = evolution.entries?.[id];
      if (!validAt(meta, atMs)) continue;
      const created = safeDate(meta?.createdAt) ?? atMs;
      const recency = Math.exp(-Math.max(0, atMs - created) / 86400000 / 90);
      const durable = meta?.status === "durable" ? 1.2 : 1;
      results.push({ project: checked.name, projectId: checked.id, id, file: path.relative(checked.real, hit.file || ""), status: meta?.status || "legacy", score: Number(hit.score || 1) * (1 + recency) * durable, content: hit.content });
    }
  }
  results.sort((a, b) => b.score - a.score);
  return { disabled: false, searchedProjects: registry.projects.length, results: results.slice(0, Math.max(1, Math.min(50, Number(limit) || 10))) };
}

export function brainStatus() {
  const projects = listRegisteredProjects();
  return { disabled: disabled(), registry: registryFile(), projects: projects.length, live: projects.filter((item) => item.status === "live").length, stale: projects.filter((item) => item.status === "stale").length };
}
