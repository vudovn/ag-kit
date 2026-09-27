import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { appendJsonl, ensureDir, readJson, readJsonl, stateRoot } from "./project-state.js";

const MAX_INPUT_BYTES = 2 * 1024 * 1024;
const nowStamp = () => new Date().toISOString().replace(/[:.]/g, "-");
const inside = (child, parent) => child === parent || child.startsWith(`${parent}${path.sep}`);

const resolveProjectFile = (root, file) => {
  const project = fs.realpathSync(path.resolve(root));
  const requested = path.resolve(project, file);
  let cursor = requested;
  while (!fs.existsSync(cursor)) {
    const parent = path.dirname(cursor);
    if (parent === cursor) break;
    cursor = parent;
  }
  const existingReal = fs.realpathSync(cursor);
  const suffix = path.relative(cursor, requested);
  const real = path.resolve(existingReal, suffix);
  if (!inside(real, project)) throw new Error("artifact path must stay inside the project root");
  if (fs.existsSync(requested)) {
    const targetReal = fs.realpathSync(requested);
    if (!inside(targetReal, project)) throw new Error("artifact path must stay inside the project root");
    return { project, file: targetReal };
  }
  return { project, file: real };
};

const compactProseBlock = (lines) => {
  const out = [];
  let paragraph = [];
  const flush = () => {
    if (!paragraph.length) return;
    const value = paragraph.join(" ").replace(/\s+/g, " ").trim();
    if (value && out[out.length - 1] !== value) out.push(value);
    paragraph = [];
  };
  for (const raw of lines) {
    const line = raw.trimEnd();
    const trimmed = line.trim();
    if (!trimmed) { flush(); if (out.length && out[out.length - 1] !== "") out.push(""); continue; }
    if (/^(#{1,6}\s|[-*+]\s|\d+[.)]\s|>\s|---$|\|)/.test(trimmed)) {
      flush();
      const normalized = trimmed.replace(/[ \t]+/g, " ");
      if (out[out.length - 1] !== normalized) out.push(normalized);
      continue;
    }
    paragraph.push(trimmed);
  }
  flush();
  while (out[0] === "") out.shift();
  while (out[out.length - 1] === "") out.pop();
  return out;
};

export function compactMarkdown(input) {
  const source = String(input).replace(/\r\n/g, "\n");
  const lines = source.split("\n");
  const result = [];
  let prose = [];
  let fenced = false;
  let fenceToken = "";
  const flushProse = () => { result.push(...compactProseBlock(prose)); prose = []; };

  for (const line of lines) {
    const match = line.match(/^\s*(```+|~~~+)/);
    if (match) {
      flushProse();
      if (!fenced) { fenced = true; fenceToken = match[1][0]; }
      else if (match[1][0] === fenceToken) { fenced = false; fenceToken = ""; }
      result.push(line.trimEnd());
      continue;
    }
    if (fenced) result.push(line);
    else prose.push(line);
  }
  flushProse();
  return `${result.join("\n").replace(/\n{3,}/g, "\n\n").trim()}\n`;
}

export function compressArtifact({ root = process.cwd(), file, write = false, output = "" }) {
  if (!file) throw new Error("file is required");
  const resolved = resolveProjectFile(root, file);
  const stat = fs.statSync(resolved.file);
  if (!stat.isFile()) throw new Error("compression target must be a file");
  if (stat.size > MAX_INPUT_BYTES) throw new Error(`compression target exceeds ${MAX_INPUT_BYTES} bytes`);
  const original = fs.readFileSync(resolved.file, "utf8");
  const compacted = compactMarkdown(original);
  const before = Buffer.byteLength(original);
  const after = Buffer.byteLength(compacted);
  const saved = Math.max(0, before - after);
  let destination = null;
  let backup = null;

  if (write) {
    backup = `${resolved.file}.bak.${nowStamp()}`;
    fs.copyFileSync(resolved.file, backup);
    fs.writeFileSync(resolved.file, compacted);
    destination = resolved.file;
  } else {
    const candidate = output || `${path.relative(resolved.project, resolved.file)}.compressed.md`;
    const target = resolveProjectFile(resolved.project, candidate).file;
    ensureDir(path.dirname(target));
    fs.writeFileSync(target, compacted);
    destination = target;
  }

  const receipt = { ts: new Date().toISOString(), kind: "compress", source: path.relative(resolved.project, resolved.file), destination: path.relative(resolved.project, destination), bytesBefore: before, bytesAfter: after, bytesSaved: saved, reductionPct: before ? Number(((saved / before) * 100).toFixed(1)) : 0, backup: backup ? path.relative(resolved.project, backup) : null };
  appendJsonl(path.join(stateRoot(resolved.project), "receipts.jsonl"), receipt);
  return receipt;
}

const gitStatus = (root) => {
  const result = spawnSync("git", ["status", "--short"], { cwd: root, encoding: "utf8", timeout: 5000, windowsHide: true });
  if (result.status !== 0) return [];
  return String(result.stdout || "").split(/\r?\n/).filter(Boolean).slice(0, 200);
};

const recentEvidence = (root) => readJsonl(path.join(stateRoot(root), "receipts.jsonl")).slice(-8).map((item) => {
  const label = item.kind || item.action || item.type || "event";
  return `${item.ts || ""} ${label}`.trim();
});

export function createHandoff({ root = process.cwd(), goal = "", state = "", decisions = [], evidence = [], risks = [], next = "" } = {}) {
  const project = fs.realpathSync(path.resolve(root));
  const agRoot = stateRoot(project);
  ensureDir(agRoot);
  const current = path.join(agRoot, "handoff.md");
  if (fs.existsSync(current)) {
    const archiveDir = path.join(agRoot, "handoffs");
    ensureDir(archiveDir);
    fs.copyFileSync(current, path.join(archiveDir, `handoff-${nowStamp()}.md`));
  }
  const flow = readJson(path.join(agRoot, "flow", "session.json"), null);
  const changed = gitStatus(project);
  const inheritedEvidence = evidence.length ? evidence : recentEvidence(project);
  const lines = [
    "# AG Kit Handoff", "",
    `- Created: ${new Date().toISOString()}`,
    `- Project: ${path.basename(project)}`,
    flow?.mode ? `- Flow: ${flow.mode}${flow.phase ? ` / ${flow.phase}` : ""}` : "",
    "", "## Goal", goal || flow?.goal || "Not recorded.",
    "", "## Current state", state || "Continue from the repository and evidence below.",
    "", "## Decisions", ...(decisions.length ? decisions.map((item) => `- ${item}`) : ["- None recorded for this handoff."]),
    "", "## Changed files", ...(changed.length ? changed.map((item) => `- ${item}`) : ["- Working tree clean or Git unavailable."]),
    "", "## Verification evidence", ...(inheritedEvidence.length ? inheritedEvidence.map((item) => `- ${item}`) : ["- No local receipt evidence recorded."]),
    "", "## Open risks", ...(risks.length ? risks.map((item) => `- ${item}`) : ["- None explicitly recorded."]),
    "", "## Next concrete action", next || "Re-read this handoff, inspect current Git status, then continue the smallest unfinished verified step.", "",
  ];
  const content = compactMarkdown(lines.join("\n"));
  fs.writeFileSync(current, content);
  const receipt = { ts: new Date().toISOString(), kind: "handoff", file: path.relative(project, current), changedFiles: changed.length, bytes: Buffer.byteLength(content) };
  appendJsonl(path.join(agRoot, "receipts.jsonl"), receipt);
  return { ...receipt, content };
}

export function readHandoff(root = process.cwd()) {
  const project = fs.realpathSync(path.resolve(root));
  const file = path.join(stateRoot(project), "handoff.md");
  return { exists: fs.existsSync(file), file: path.relative(project, file), content: fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "" };
}
