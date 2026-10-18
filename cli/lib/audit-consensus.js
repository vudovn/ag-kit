import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { appendReceipt, auditRoster, probeRoster } from "./v2-engine.js";
import { ensureDir, resolveSafeProjectRoot, stateRoot } from "./project-state.js";
import { chunkText, dedupeFindings } from "./audit-chunker.js";
import { traceEnv, traceFields } from "./trace-context.js";

const MAX_AUDIT_BYTES = 512 * 1024;
const CHUNK_CHARS = 32000;
const CHUNK_OVERLAP = 2400;
const MAX_REVIEW_OUTPUT_BYTES = 2 * 1024 * 1024;
const RETRY_ON_TIMEOUT = new Set(["gemini", "qwen"]);
const truncate = (value, max = 12000) => String(value || "").slice(0, max);

const inside = (root, candidate) => candidate === root || candidate.startsWith(`${root}${path.sep}`);
const boundBuffer = (buffer, maxBytes = MAX_AUDIT_BYTES) => ({
    content: buffer.subarray(0, Math.min(buffer.length, maxBytes)).toString("utf8"),
    originalBytes: buffer.length,
    truncated: buffer.length > maxBytes,
});

const readBoundedFile = (file) => boundBuffer(fs.readFileSync(file));

export function snapshotAuditTarget({ root = process.cwd(), target = "." }) {
    const resolvedRoot = resolveSafeProjectRoot(root);
    const realRoot = fs.realpathSync(resolvedRoot);
    if (target === "." || target === "diff") {
        const options = { cwd: realRoot, encoding: null, timeout: 15000, shell: false, maxBuffer: 4 * 1024 * 1024 };
        const staged = spawnSync("git", ["diff", "--cached", "--no-ext-diff", "--unified=3"], options);
        const diff = spawnSync("git", ["diff", "--no-ext-diff", "--unified=3", "HEAD"], options);
        const combined = Buffer.concat([
            Buffer.isBuffer(staged.stdout) ? staged.stdout : Buffer.from(staged.stdout || ""),
            Buffer.from("\n"),
            Buffer.isBuffer(diff.stdout) ? diff.stdout : Buffer.from(diff.stdout || ""),
        ]);
        const bounded = boundBuffer(combined);
        return { kind: "diff", label: "working tree diff", content: bounded.content.trim() || "(no diff)", originalBytes: bounded.originalBytes, truncated: bounded.truncated };
    }
    const absolute = path.resolve(resolvedRoot, target);
    if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) throw new Error(`audit target not found or not a file: ${target}`);
    const realTarget = fs.realpathSync(absolute);
    if (!inside(realRoot, realTarget)) throw new Error("audit target must stay inside project root after resolving symlinks");
    const bounded = readBoundedFile(realTarget);
    return { kind: "file", label: path.relative(realRoot, realTarget), content: bounded.content, originalBytes: bounded.originalBytes, truncated: bounded.truncated };
}

const promptFor = (snapshot, chunk, totalChunks) => `You are an independent read-only reviewer. Review ONLY the snapshot chunk below. Do not edit files, run tools, or assume repository access. Return JSON only using this schema: {"findings":[{"severity":"blocking|important|optional","title":"short concrete title","evidence":"specific reason or evidence"}]}. Include only concrete correctness, security, regression, test, or maintainability findings. If there is no issue, return {"findings":[]}.\n\nTARGET: ${snapshot.label}\nCHUNK: ${chunk.index + 1}/${totalChunks} (chars ${chunk.start}-${chunk.end})\n\n--- SNAPSHOT START ---\n${chunk.text}\n--- SNAPSHOT END ---`;

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

const runChild = ({ reviewer, prompt, cwd, timeoutMs, root }) => new Promise((resolve) => {
    let stdout = "";
    let stderr = "";
    let outputBytes = 0;
    let timedOut = false;
    let overflow = false;
    let spawnError = null;
    let settled = false;
    let timer = null;
    let killTimer = null;
    const child = spawn(reviewer.command, reviewer.run(prompt), {
        cwd,
        shell: false,
        env: traceEnv(root),
        stdio: ["ignore", "pipe", "pipe"],
        windowsHide: true,
    });
    const finish = (status, signal) => {
        if (settled) return;
        settled = true;
        if (timer) clearTimeout(timer);
        if (killTimer) clearTimeout(killTimer);
        resolve({ status, signal, stdout, stderr, timedOut, overflow, error: spawnError });
    };
    const terminate = () => {
        if (settled) return;
        child.kill("SIGTERM");
        if (!killTimer) killTimer = setTimeout(() => { if (!settled) child.kill("SIGKILL"); }, 300);
    };
    const append = (kind, chunk) => {
        const text = chunk.toString("utf8");
        outputBytes += Buffer.byteLength(text);
        if (outputBytes > MAX_REVIEW_OUTPUT_BYTES) {
            overflow = true;
            terminate();
            return;
        }
        if (kind === "stdout") stdout += text;
        else stderr += text;
    };
    child.stdout?.on("data", (chunk) => append("stdout", chunk));
    child.stderr?.on("data", (chunk) => append("stderr", chunk));
    child.once("error", (error) => { spawnError = error; finish(null, null); });
    child.once("close", (status, signal) => finish(status, signal));
    timer = setTimeout(() => {
        timedOut = true;
        terminate();
    }, Math.max(1000, Number(timeoutMs) || 120000));
});

const runReviewerChunk = async ({ reviewer, prompt, cwd, timeoutMs, root }) => {
    let attempts = 1;
    let result = await runChild({ reviewer, prompt, cwd, timeoutMs, root });
    if (result.timedOut && RETRY_ON_TIMEOUT.has(reviewer.id)) {
        attempts += 1;
        result = await runChild({ reviewer, prompt, cwd, timeoutMs, root });
    }
    const output = unwrap(reviewer.id, result.stdout);
    return {
        ok: !result.error && !result.timedOut && !result.overflow && result.status === 0,
        exitCode: result.status,
        signal: result.signal || null,
        attempts,
        timedOut: result.timedOut,
        overflow: result.overflow,
        output: truncate(output, 12000),
        findings: parseReviewerFindings(output),
        error: truncate(result.error?.message || (result.timedOut ? "reviewer timed out" : result.overflow ? "reviewer output exceeded limit" : result.stderr) || "", 1200),
    };
};

const runReviewer = async ({ reviewer, snapshot, chunks, cwd, timeoutMs, root }) => {
    const started = Date.now();
    const chunkResults = [];
    for (const chunk of chunks) {
        chunkResults.push({
            index: chunk.index,
            start: chunk.start,
            end: chunk.end,
            ...await runReviewerChunk({ reviewer, prompt: promptFor(snapshot, chunk, chunks.length), cwd, timeoutMs, root }),
        });
    }
    const findings = dedupeFindings(chunkResults.filter((item) => item.ok).flatMap((item) => item.findings));
    return {
        reviewer: reviewer.id,
        lineage: reviewer.lineage,
        ok: chunkResults.length > 0 && chunkResults.every((item) => item.ok),
        durationMs: Date.now() - started,
        chunkCount: chunkResults.length,
        successfulChunks: chunkResults.filter((item) => item.ok).length,
        findings,
        chunks: chunkResults.map(({ findings: _findings, ...item }) => item),
    };
};

export async function runConsensusAudit({ root = process.cwd(), target = ".", reviewers = 3, excludeLineage = process.env.AG_KIT_CALLING_LINEAGE || "", timeoutMs = 120000 } = {}) {
    const snapshot = snapshotAuditTarget({ root, target });
    const chunks = chunkText(snapshot.content, { maxChars: CHUNK_CHARS, overlapChars: CHUNK_OVERLAP });
    const probes = probeRoster();
    const byId = new Map(auditRoster.map((item) => [item.id, item]));
    const selected = [];
    const attemptedLineages = new Set();
    for (const probe of probes) {
        if (!probe.available || !probe.executable || probe.lineage === excludeLineage || attemptedLineages.has(probe.lineage)) continue;
        selected.push(byId.get(probe.id)); attemptedLineages.add(probe.lineage);
        if (selected.length >= Math.max(1, Math.min(3, Number(reviewers)))) break;
    }

    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-v4-"));
    const startedAll = Date.now();
    try {
        const results = await Promise.all(selected.map((reviewer) => runReviewer({ reviewer, snapshot, chunks, cwd: temp, timeoutMs, root })));
        const successful = results.filter((item) => item.ok);
        const successfulLineages = [...new Set(successful.map((item) => item.lineage))];
        const findings = clusterFindings(successful);
        const counts = {
            consensus: findings.filter((item) => item.status === "consensus").length,
            contested: findings.filter((item) => item.status === "contested").length,
            blocking: findings.filter((item) => item.severity === "blocking").length,
            important: findings.filter((item) => item.severity === "important").length,
            optional: findings.filter((item) => item.severity === "optional").length,
        };
        const status = snapshot.truncated ? "degraded" : successfulLineages.length >= 2 ? "complete" : successfulLineages.length ? "degraded" : "unavailable";
        const auditDir = path.join(stateRoot(root), "audits");
        ensureDir(auditDir);
        const reportPath = path.join(auditDir, `${Date.now()}-cross-audit.json`);
        const report = {
            schema: 4,
            ...traceFields(root),
            status,
            target: snapshot.label,
            snapshotKind: snapshot.kind,
            snapshotBytes: snapshot.originalBytes,
            truncated: snapshot.truncated,
            chunkCount: chunks.length,
            excludedLineage: excludeLineage || null,
            attemptedReviewers: results.map((item) => item.reviewer),
            attemptedLineages: [...attemptedLineages],
            reviewerCount: successful.length,
            lineages: successfulLineages,
            durationMs: Date.now() - startedAll,
            counts,
            findings,
            results,
        };
        fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
        appendReceipt(root, "cross-audit", {
            action: "run-consensus",
            status,
            target: snapshot.label,
            reviewers: successful.map((item) => item.reviewer),
            attemptedReviewers: results.map((item) => item.reviewer),
            lineages: status === "complete" ? successfulLineages : [],
            successfulLineages,
            attemptedLineages: [...attemptedLineages],
            truncated: snapshot.truncated,
            chunkCount: chunks.length,
            durationMs: report.durationMs,
            findingCounts: counts,
            report: path.relative(root, reportPath),
        });
        return { ...report, report: path.relative(root, reportPath) };
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
}
