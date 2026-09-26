import http from "node:http";
import path from "node:path";
import { appendJsonl, readJsonl, stateRoot } from "./project-state.js";

const eventsFile = (root) => path.join(stateRoot(root), "observability", "events.jsonl");
const num = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;

export function recordObservation({ root = process.cwd(), runtime = "unknown", session = "manual", kind = "turn", inputTokens = 0, outputTokens = 0, cacheReadTokens = 0, savedTokens = 0, costUsd = 0, metadata = {} }) {
    const event = { ts: new Date().toISOString(), runtime, session, kind, inputTokens: num(inputTokens), outputTokens: num(outputTokens), cacheReadTokens: num(cacheReadTokens), savedTokens: num(savedTokens), costUsd: num(costUsd), metadata };
    appendJsonl(eventsFile(root), event);
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
    return { totals, runtimes, recent: events.slice(-20).reverse() };
}

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
const dashboardHtml = (summary) => {
    const runtimeRows = Object.entries(summary.runtimes).map(([name, data]) => `<tr><td>${escapeHtml(name)}</td><td>${data.events}</td><td>${data.inputTokens}</td><td>${data.outputTokens}</td><td>${data.cacheReadTokens}</td><td>${data.savedTokens}</td><td>$${data.costUsd.toFixed(4)}</td></tr>`).join("");
    return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AG Kit Dashboard</title><style>body{font:14px system-ui;margin:32px;max-width:1100px}h1{font-size:24px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}.card{border:1px solid #bbb;border-radius:10px;padding:16px}.value{font-size:24px;font-weight:700}table{border-collapse:collapse;width:100%;margin-top:20px}th,td{padding:8px;border-bottom:1px solid #ddd;text-align:right}th:first-child,td:first-child{text-align:left}</style></head><body><h1>AG Kit local observability</h1><p>Project-local telemetry only. This server binds to localhost.</p><div class="cards"><div class="card"><div>Events</div><div class="value">${summary.totals.events}</div></div><div class="card"><div>Input tokens</div><div class="value">${summary.totals.inputTokens}</div></div><div class="card"><div>Output tokens</div><div class="value">${summary.totals.outputTokens}</div></div><div class="card"><div>Cache-read tokens</div><div class="value">${summary.totals.cacheReadTokens}</div></div><div class="card"><div>Explicit saved tokens</div><div class="value">${summary.totals.savedTokens}</div></div><div class="card"><div>Recorded cost</div><div class="value">$${summary.totals.costUsd.toFixed(4)}</div></div></div><table><thead><tr><th>Runtime</th><th>Events</th><th>Input</th><th>Output</th><th>Cache</th><th>Saved</th><th>Cost</th></tr></thead><tbody>${runtimeRows}</tbody></table></body></html>`;
};

const isLoopback = (address = "") => address === "127.0.0.1" || address === "::1" || address === "::ffff:127.0.0.1";
export function startDashboard({ root = process.cwd(), port = 4737 } = {}) {
    const server = http.createServer((req, res) => {
        if (!isLoopback(req.socket.remoteAddress)) { res.writeHead(403, { "content-type": "text/plain" }); res.end("Forbidden\n"); return; }
        if (req.url === "/api/summary") { res.writeHead(200, { "content-type": "application/json; charset=utf-8" }); res.end(`${JSON.stringify(summarizeObservability(root), null, 2)}\n`); return; }
        if (req.url !== "/" && req.url !== "/index.html") { res.writeHead(404, { "content-type": "text/plain" }); res.end("Not found\n"); return; }
        res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(dashboardHtml(summarizeObservability(root)));
    });
    server.listen(Number(port), "127.0.0.1", () => console.log(`AG Kit dashboard: http://127.0.0.1:${Number(port)}`));
    return server;
}
