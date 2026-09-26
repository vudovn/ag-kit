import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { appendJsonl, ensureDir, slugify, stateRoot } from "./project-state.js";

const receiptFile = (root) => path.join(stateRoot(root), "receipts", "efficiency.jsonl");
const sandboxDir = (root) => path.join(stateRoot(root), "session-sandbox");
const nowId = () => new Date().toISOString().replace(/[:.]/g, "-");
const includesAny = (text, patterns) => patterns.some((pattern) => pattern.test(text));

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

export function runSandboxedCommand({ root = process.cwd(), command, args = [], timeoutMs = 120000, maxSummaryLines = 40 }) {
  if (!command) throw new Error("command is required");
  const projectRoot = path.resolve(root);
  ensureDir(sandboxDir(projectRoot));
  const started = Date.now();
  const result = spawnSync(command, args, { cwd: projectRoot, encoding: "utf8", shell: false, timeout: Number(timeoutMs), maxBuffer: 50 * 1024 * 1024, env: process.env });
  const durationMs = Date.now() - started;
  const stdout = result.stdout || "";
  const stderr = result.stderr || "";
  const full = `$ ${[command, ...args].join(" ")}\n\n[stdout]\n${stdout}\n[stderr]\n${stderr}`;
  const log = path.join(sandboxDir(projectRoot), `${nowId()}-${slugify(path.basename(command))}.log`);
  fs.writeFileSync(log, full);
  const summary = summarizeLines(full, Math.max(8, Number(maxSummaryLines)));
  const receipt = { ts: new Date().toISOString(), type: "sandbox-command", command, args, exitCode: result.status, signal: result.signal || null, durationMs, log: path.relative(projectRoot, log), totalLines: summary.totalLines, omittedLines: summary.omittedLines };
  appendJsonl(receiptFile(projectRoot), receipt);
  return { ok: !result.error && result.status === 0, error: result.error?.message || null, ...receipt, summary: summary.text };
}
