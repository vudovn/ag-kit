import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { appendJsonl, ensureDir, slugify, stateRoot } from "./project-state.js";

const receiptFile = (root) => path.join(stateRoot(root), "receipts", "efficiency.jsonl");
const sandboxDir = (root) => path.join(stateRoot(root), "session-sandbox");
const nowId = () => new Date().toISOString().replace(/[:.]/g, "-");
const includesAny = (text, patterns) => patterns.some((pattern) => pattern.test(text));
const PYTHON_ALIASES = new Set(["python", "python3", "python.exe", "python3.exe"]);
const PYTHON_ENV_DIRS = [".venv", "venv", "env"];

export function routeTask(task = "", root = process.cwd()) {
  const text = String(task).toLowerCase();
  let role = "builder";
  let effort = "medium";
  let mode = "standard";
  let reason = "implementation-oriented request";

  if (includesAny(text, [/\b(read|find|search|locate|explain|inspect|research|docs?|trace|explore)\b/])) {
    role = "scout"; effort = "low"; mode = "quick"; reason = "read/research work can stay lightweight";
  }
  if (includesAny(text, [/\b(review|audit|security|test|verify|regression|quality|risk)\b/])) {
    role = "reviewer"; effort = "medium"; mode = "standard"; reason = "independent verification/review work";
  }
  if (includesAny(text, [/\b(architecture|architect|migration|redesign|system design|tradeoff|strategy|platform)\b/])) {
    role = "architect"; effort = "high"; mode = "deep"; reason = "high-leverage architecture/tradeoff work";
  }
  if (includesAny(text, [/\b(multi[- ]?system|cross[- ]?runtime|launch|production migration|large refactor|rewrite)\b/])) {
    effort = "high"; mode = "deep";
  }

  const result = { task: String(task), role, effort, mode, reason };
  appendJsonl(receiptFile(root), { ts: new Date().toISOString(), type: "route", ...result });
  return result;
}

const summarizeLines = (text, maxLines) => {
  const lines = String(text).split(/\r?\n/);
  if (lines.length <= maxLines) return { text: lines.join("\n"), totalLines: lines.length, omittedLines: 0 };
  const head = Math.min(5, Math.floor(maxLines / 3));
  const tail = Math.max(1, maxLines - head - 1);
  const omitted = Math.max(0, lines.length - head - tail);
  return { text: [...lines.slice(0, head), `... ${omitted} lines saved to sandbox log ...`, ...lines.slice(-tail)].join("\n"), totalLines: lines.length, omittedLines: omitted };
};

const usableFile = (file) => {
  try {
    if (!fs.statSync(file).isFile()) return false;
    fs.accessSync(file, process.platform === "win32" ? fs.constants.F_OK : fs.constants.X_OK);
    return true;
  } catch { return false; }
};

export function resolveSandboxCommand({ root = process.cwd(), command }) {
  const requestedCommand = String(command || "");
  const projectRoot = path.resolve(root);
  if (!PYTHON_ALIASES.has(requestedCommand.toLowerCase())) {
    return { requestedCommand, resolvedCommand: requestedCommand, environment: null };
  }

  const executable = process.platform === "win32" ? path.join("Scripts", "python.exe") : path.join("bin", "python");
  for (const envDir of PYTHON_ENV_DIRS) {
    const candidate = path.join(projectRoot, envDir, executable);
    if (!usableFile(candidate)) continue;
    return {
      requestedCommand,
      resolvedCommand: candidate,
      environment: { kind: "python-venv", path: envDir },
    };
  }

  return { requestedCommand, resolvedCommand: requestedCommand, environment: null };
}

export function runSandboxedCommand({ root = process.cwd(), command, args = [], timeoutMs = 120000, maxSummaryLines = 40 }) {
  if (!command) throw new Error("command is required");
  const projectRoot = path.resolve(root);
  ensureDir(sandboxDir(projectRoot));
  const resolved = resolveSandboxCommand({ root: projectRoot, command });
  const started = Date.now();
  const result = spawnSync(resolved.resolvedCommand, args, { cwd: projectRoot, encoding: "utf8", shell: false, timeout: Number(timeoutMs), maxBuffer: 50 * 1024 * 1024, env: process.env });
  const durationMs = Date.now() - started;
  const stdout = result.stdout || "";
  const stderr = result.stderr || "";
  const resolutionLine = resolved.resolvedCommand === resolved.requestedCommand ? "" : `\n[resolved]\n${resolved.resolvedCommand}`;
  const full = `$ ${[resolved.requestedCommand, ...args].join(" ")}${resolutionLine}\n\n[stdout]\n${stdout}\n[stderr]\n${stderr}`;
  const log = path.join(sandboxDir(projectRoot), `${nowId()}-${slugify(path.basename(resolved.requestedCommand))}.log`);
  fs.writeFileSync(log, full);
  const summary = summarizeLines(full, Math.max(8, Number(maxSummaryLines)));
  const receipt = {
    ts: new Date().toISOString(),
    type: "sandbox-command",
    command: resolved.requestedCommand,
    resolvedCommand: resolved.resolvedCommand,
    environment: resolved.environment,
    args,
    exitCode: result.status,
    signal: result.signal || null,
    durationMs,
    log: path.relative(projectRoot, log),
    totalLines: summary.totalLines,
    omittedLines: summary.omittedLines,
  };
  appendJsonl(receiptFile(projectRoot), receipt);
  return { ok: !result.error && result.status === 0, error: result.error?.message || null, ...receipt, summary: summary.text };
}
