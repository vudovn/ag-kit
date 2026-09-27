#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const readStdin = async () => {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  try { return JSON.parse(input || "{}"); } catch { return {}; }
};

const inside = (child, parent) => {
  const rel = path.relative(parent, child);
  return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
};

const resolveWorkspace = (payload) => {
  const roots = Array.isArray(payload.workspacePaths) ? payload.workspacePaths.filter((item) => typeof item === "string") : [];
  const cwd = payload?.toolCall?.args?.Cwd;
  if (typeof cwd === "string" && roots.some((root) => inside(path.resolve(cwd), path.resolve(root)))) return path.resolve(cwd);
  for (const root of roots) {
    try { if (fs.statSync(root).isDirectory()) return path.resolve(root); } catch {}
  }
  return process.cwd();
};

const payload = await readStdin();
try {
  const name = String(payload?.toolCall?.name || "unknown").replace(/[^a-zA-Z0-9_.:-]/g, "_").slice(0, 80);
  const status = payload?.error ? "error" : "ok";
  const session = String(payload?.conversationId || "antigravity").slice(0, 120);
  spawnSync("ag-kit", ["observe", `tool:${name}:${status}`, "--runtime", "antigravity", "--session", session, "--path", resolveWorkspace(payload)], {
    stdio: "ignore",
    timeout: 3000,
    windowsHide: true,
  });
} catch {
  // Observability must never block the agent loop.
}
process.stdout.write("{}\n");
