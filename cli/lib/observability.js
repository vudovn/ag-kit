import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { ensureDir, readJson, readJsonl, stateRoot, writeJson } from "./project-state.js";

const MAX_BYTES = 10 * 1024 * 1024;
const MAX_ARCHIVES = 10;
const MAX_LINE_BYTES = 8 * 1024;
const observabilityDir = (root) => path.join(stateRoot(root), "observability");
const eventsFile = (root) => path.join(observabilityDir(root), "events.jsonl");
const dashboardStateFile = (root) => path.join(observabilityDir(root), "dashboard.json");
const num = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;
const stamp = () => new Date().toISOString().replace(/[:.]/g, "-");

const archives = (root) => {
  const dir = observabilityDir(root);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((name) => /^events\.jsonl\./.test(name)).map((name) => path.join(dir, name)).sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
};

const rotateIfNeeded = (root, incomingBytes) => {
  const live = eventsFile(root);
  if (!fs.existsSync(live) || fs.statSync(live).size + incomingBytes <= MAX_BYTES) return;
  fs.renameSync(live, `${live}.${stamp()}`);
  for (const old of archives(root).slice(MAX_ARCHIVES)) fs.rmSync(old, { force: true });
};

const boundedLine = (event) => {
  let line = JSON.stringify(event);
  if (Buffer.byteLength(line) <= MAX_LINE_BYTES) return line;
  const compact = { ...event, metadata: { truncated: true, keys: Object.keys(event.metadata || {}) } };
  line = JSON.stringify(compact);
  return Buffer.byteLength(line) <= MAX_LINE_BYTES ? line : JSON.stringify({ ts: event.ts, runtime: event.runtime, session: event.session, kind: event.kind, truncated: true });
};

export function recordObservation({ root = process.cwd(), runtime = "unknown", session = "manual", kind = "turn", inputTokens = 0, outputTokens = 0, cacheReadTokens = 0, savedTokens = 0, costUsd = 0, metadata = {} }) {
  const event = { ts: new Date().toISOString(), runtime, session, kind, inputTokens: num(inputTokens), outputTokens: num(outputTokens), cacheReadTokens: num(cacheReadTokens), savedTokens: num(savedTokens), costUsd: num(costUsd), metadata };
  const line = `${boundedLine(event)}\n`;
  ensureDir(observabilityDir(root));
  rotateIfNeeded(root, Buffer.byteLength(line));
  fs.appendFileSync(eventsFile(root), line);
  return event;
}

export function summarizeObservability(root = process.cwd()) {
  const events = readJsonl(eventsFile(root));
  const totals = { events: events.length, inputTokens: 0, outputTokens: 0, cacheReadTokens: 0, savedTokens: 0, costUsd: 0 };
  const runtimes = {};
  for (const event of events) {
    const bucket = runtimes[event.runtime] ||= { events: 0, inputTokens: 0, outputTokens: 0, cacheReadTokens: 0, savedTokens: 0, costUsd: 0 };
    for (const key of ["inputTokens", "outputTokens", "cacheReadTokens", "savedTokens", "costUsd"]) {
      const value = num(event[key]); totals[key] += value; bucket[key] += value;
    }
    bucket.events += 1;
  }
  totals.costUsd = Number(totals.costUsd.toFixed(6));
  for (const bucket of Object.values(runtimes)) bucket.costUsd = Number(bucket.costUsd.toFixed(6));
  return {
    totals,
    runtimes,
    recent: events.slice(-50).reverse(),
    ledger: { live: path.relative(path.resolve(root), eventsFile(root)), liveBytes: fs.existsSync(eventsFile(root)) ? fs.statSync(eventsFile(root)).size : 0, archives: archives(root).length, maxLiveBytes: MAX_BYTES, maxArchives: MAX_ARCHIVES, maxLineBytes: MAX_LINE_BYTES },
    methodology: { savedTokens: "Only explicitly supplied/measured saved tokens are counted. No synthetic no-AG-Kit multiplier is applied.", costUsd: "Recorded cost is accepted only as supplied by the runtime/user integration; AG Kit does not infer missing provider pricing." },
  };
}

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
const dashboardHtml = (summary) => {
  const runtimeRows = Object.entries(summary.runtimes).map(([name, data]) => `<tr><td>${escapeHtml(name)}</td><td>${data.events}</td><td>${data.inputTokens}</td><td>${data.outputTokens}</td><td>${data.cacheReadTokens}</td><td>${data.savedTokens}</td><td>$${data.costUsd.toFixed(4)}</td></tr>`).join("");
  const recentRows = summary.recent.slice(0, 25).map((event) => `<tr><td>${escapeHtml(event.ts)}</td><td>${escapeHtml(event.runtime)}</td><td>${escapeHtml(event.kind)}</td><td>${event.inputTokens || 0}</td><td>${event.outputTokens || 0}</td></tr>`).join("");
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AG Kit Dashboard</title><style>body{font:14px system-ui;margin:32px;max-width:1200px}h1{font-size:24px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}.card{border:1px solid #bbb;border-radius:10px;padding:16px}.value{font-size:24px;font-weight:700}table{border-collapse:collapse;width:100%;margin:20px 0}th,td{padding:8px;border-bottom:1px solid #ddd;text-align:right}th:first-child,td:first-child{text-align:left}@media(prefers-color-scheme:dark){body{background:#111;color:#eee}.card{border-color:#444}th,td{border-color:#333}}</style></head><body><h1>AG Kit local observability</h1><p>Project-local telemetry only. Bound to 127.0.0.1; no modeled savings multiplier.</p><div class="cards"><div class="card"><div>Events</div><div class="value">${summary.totals.events}</div></div><div class="card"><div>Input tokens</div><div class="value">${summary.totals.inputTokens}</div></div><div class="card"><div>Output tokens</div><div class="value">${summary.totals.outputTokens}</div></div><div class="card"><div>Cache-read</div><div class="value">${summary.totals.cacheReadTokens}</div></div><div class="card"><div>Explicit saved</div><div class="value">${summary.totals.savedTokens}</div></div><div class="card"><div>Recorded cost</div><div class="value">$${summary.totals.costUsd.toFixed(4)}</div></div></div><h2>By runtime</h2><table><thead><tr><th>Runtime</th><th>Events</th><th>Input</th><th>Output</th><th>Cache</th><th>Saved</th><th>Cost</th></tr></thead><tbody>${runtimeRows}</tbody></table><h2>Recent events</h2><table><thead><tr><th>Time</th><th>Runtime</th><th>Kind</th><th>Input</th><th>Output</th></tr></thead><tbody>${recentRows}</tbody></table></body></html>`;
};

const isLoopback = (address = "") => address === "127.0.0.1" || address === "::1" || address === "::ffff:127.0.0.1";
const pidAlive = (pid) => { try { process.kill(Number(pid), 0); return true; } catch { return false; } };

export function dashboardStatus(root = process.cwd()) {
  const file = dashboardStateFile(root);
  const state = readJson(file, null);
  if (!state) return { running: false, stateFile: path.relative(path.resolve(root), file) };
  const running = pidAlive(state.pid);
  if (!running) fs.rmSync(file, { force: true });
  return { ...state, running, stateFile: path.relative(path.resolve(root), file) };
}

export function stopDashboard(root = process.cwd()) {
  const state = dashboardStatus(root);
  if (!state.running) return { stopped: false, reason: "dashboard is not running" };
  process.kill(Number(state.pid), "SIGTERM");
  return { stopped: true, pid: state.pid, port: state.port };
}

export function startDashboard({ root = process.cwd(), port = 4737 } = {}) {
  const existing = dashboardStatus(root);
  if (existing.running) throw new Error(`dashboard already running on port ${existing.port}`);
  const server = http.createServer((req, res) => {
    if (!isLoopback(req.socket.remoteAddress)) { res.writeHead(403, { "content-type": "text/plain" }); res.end("Forbidden\n"); return; }
    if (req.url === "/api/summary") { res.writeHead(200, { "content-type": "application/json; charset=utf-8" }); res.end(`${JSON.stringify(summarizeObservability(root), null, 2)}\n`); return; }
    if (req.url === "/api/methodology") { res.writeHead(200, { "content-type": "application/json; charset=utf-8" }); res.end(`${JSON.stringify(summarizeObservability(root).methodology, null, 2)}\n`); return; }
    if (req.url !== "/" && req.url !== "/index.html") { res.writeHead(404, { "content-type": "text/plain" }); res.end("Not found\n"); return; }
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(dashboardHtml(summarizeObservability(root)));
  });
  const cleanup = () => { fs.rmSync(dashboardStateFile(root), { force: true }); };
  const shutdown = () => server.close(() => { cleanup(); process.exit(0); });
  process.once("SIGTERM", shutdown);
  process.once("SIGINT", shutdown);
  server.on("close", cleanup);
  server.listen(Number(port), "127.0.0.1", () => {
    const state = { pid: process.pid, port: Number(port), startedAt: new Date().toISOString(), url: `http://127.0.0.1:${Number(port)}` };
    writeJson(dashboardStateFile(root), state);
    console.log(`AG Kit dashboard: ${state.url}`);
  });
  return server;
}
