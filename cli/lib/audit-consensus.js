import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { appendReceipt, auditRoster, probeRoster, snapshotAuditTarget } from "./v2-engine.js";
import { ensureDir, stateRoot } from "./project-state.js";

const truncate = (value, max = 120000) => String(value || "").slice(0, max);
const promptFor = (snapshot) => `You are an independent read-only reviewer. Review ONLY the snapshot below. Do not edit files or assume repository access. Return JSON only using this schema: {"findings":[{"severity":"blocking|important|optional","title":"short concrete title","evidence":"specific reason or evidence"}]}. Include only concrete correctness, security, regression, test, or maintainability findings. If there is no issue, return {"findings":[]}.\n\nTARGET: ${snapshot.label}\n\n--- SNAPSHOT START ---\n${snapshot.content}\n--- SNAPSHOT END ---`;

const unwrap = (id, stdout) => {
    let raw = String(stdout || "").trim();
    if (["gemini", "qwen"].includes(id)) {
        try { const data = JSON.parse(raw); raw = String(data.response ?? data.result ?? data.output ?? raw); } catch {}
    }
    return raw;
};

export function parseReviewerFindings(output) {
    const raw = String(output || "").trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
    const candidates = [raw, raw.match(/\{[\s\S]*\}/)?.[0]].filter(Boolean);
    for (const candidate of candidates) {
        try {
            const data = JSON.parse(candidate);
            if (Array.isArray(data.findings)) return data.findings.map((item) => ({ severity: ["blocking", "important", "optional"].includes(String(item.severity).toLowerCase()) ? String(item.severity).toLowerCase() : "important", title: String(item.title || "Finding").trim(), evidence: String(item.evidence || "").trim() })).filter((item) => item.title);
        } catch {}
    }
    return raw.split(/\r?\n/).flatMap((line) => {
        const match = line.match(/^\s*(?:[-*]\s*)?(BLOCKING|IMPORTANT|OPTIONAL)[:\-]\s*(.+)$/i);
        return match ? [{ severity: match[1].toLowerCase(), title: match[2].trim(), evidence: "" }] : [];
    });
}

const words = (finding) => new Set(`${finding.title} ${finding.evidence}`.toLowerCase().match(/[a-z0-9_]{3,}/g) || []);
const similarity = (a, b) => {
    const left = words(a); const right = words(b); if (!left.size || !right.size) return 0;
    let shared = 0; for (const word of left) if (right.has(word)) shared += 1;
    return shared / (left.size + right.size - shared);
};
export function clusterFindings(results) {
    const clusters = [];
    for (const result of results) for (const finding of result.findings || []) {
        let cluster = clusters.find((item) => similarity(item.finding, finding) >= 0.45);
        if (!cluster) { cluster = { finding, reviewers: [], lineages: [], severities: [] }; clusters.push(cluster); }
        cluster.reviewers.push(result.reviewer); cluster.lineages.push(result.lineage); cluster.severities.push(finding.severity);
    }
    return clusters.map((cluster) => ({
        status: new Set(cluster.lineages).size >= 2 ? "consensus" : "contested",
        severity: cluster.severities.includes("blocking") ? "blocking" : cluster.severities.includes("important") ? "important" : "optional",
        title: cluster.finding.title,
        evidence: cluster.finding.evidence,
        reviewers: [...new Set(cluster.reviewers)],
        lineages: [...new Set(cluster.lineages)],
    }));
}

export function runConsensusAudit({ root = process.cwd(), target = ".", reviewers = 3, excludeLineage = process.env.AG_KIT_CALLING_LINEAGE || "", timeoutMs = 180000 } = {}) {
    const snapshot = snapshotAuditTarget({ root, target });
    const probes = probeRoster();
    const byId = new Map(auditRoster.map((item) => [item.id, item]));
    const selected = [];
    const lineages = new Set();
    for (const probe of probes) {
        if (!probe.available || !probe.executable || probe.lineage === excludeLineage || lineages.has(probe.lineage)) continue;
        selected.push(byId.get(probe.id)); lineages.add(probe.lineage);
        if (selected.length >= Math.max(1, Math.min(3, Number(reviewers)))) break;
    }
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-v2-"));
    const startedAll = Date.now();
    try {
        const prompt = promptFor(snapshot);
        const results = selected.map((reviewer) => {
            const started = Date.now();
            const result = spawnSync(reviewer.command, reviewer.run(prompt), { cwd: temp, encoding: "utf8", timeout: Number(timeoutMs), shell: false, env: process.env });
            const output = unwrap(reviewer.id, result.stdout);
            return { reviewer: reviewer.id, lineage: reviewer.lineage, ok: !result.error && result.status === 0, exitCode: result.status, durationMs: Date.now() - started, findings: parseReviewerFindings(output), output: truncate(output, 20000), error: truncate(result.error?.message || result.stderr || "", 1200) };
        });
        const findings = clusterFindings(results.filter((item) => item.ok));
        const counts = { consensus: findings.filter((item) => item.status === "consensus").length, contested: findings.filter((item) => item.status === "contested").length, blocking: findings.filter((item) => item.severity === "blocking").length, important: findings.filter((item) => item.severity === "important").length, optional: findings.filter((item) => item.severity === "optional").length };
        const auditDir = path.join(stateRoot(root), "audits"); ensureDir(auditDir);
        const reportPath = path.join(auditDir, `${Date.now()}-cross-audit.json`);
        const report = { schema: 2, target: snapshot.label, snapshotKind: snapshot.kind, excludedLineage: excludeLineage || null, reviewerCount: results.length, lineages: [...lineages], durationMs: Date.now() - startedAll, counts, findings, results };
        fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
        appendReceipt(root, "cross-audit", { action: "run-consensus", target: snapshot.label, reviewers: results.map((item) => item.reviewer), lineages: [...lineages], excludedLineage: excludeLineage || null, durationMs: report.durationMs, findingCounts: counts, report: path.relative(root, reportPath) });
        return { ...report, report: path.relative(root, reportPath), status: results.length >= 2 && results.every((item) => item.ok) ? "complete" : results.length ? "degraded" : "unavailable" };
    } finally { fs.rmSync(temp, { recursive: true, force: true }); }
}
