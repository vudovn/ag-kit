import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory, memoryEvolutionStatus, recallEvolvingMemory, referenceMemory, runMemoryDream } from "../lib/memory-evolution.js";
import { completeWave, decideFlow, flowEvidenceStatus, flowStatus, readyWaves, recordFlowArtifact, setWaveTable, startFlow } from "../lib/workflow-session.js";
import { recordObservation, summarizeObservability } from "../lib/observability.js";
import { forgetPreference, learnPreference, profileForInjection, profileStatus, setPersonalization } from "../lib/personalization.js";
import { checkDesignContract, initDesignContract, listDesignTemplates } from "../lib/design-contract.js";
import { clusterFindings, parseReviewerFindings } from "../lib/audit-consensus.js";

const tempRoot = (t) => { const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-features-")); t.after(() => fs.rmSync(root, { recursive: true, force: true })); return root; };
const appendReceipt = (root, type, receipt) => {
    const dir = path.join(root, ".ag-kit", "receipts");
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, `${type}.jsonl`), `${JSON.stringify(receipt)}\n`);
};
const futureTs = () => new Date(Date.now() + 1000).toISOString();

test("memory evolves from candidate to durable across references and sessions", (t) => {
    const root = tempRoot(t);
    const added = addEvolvingMemory({ root, text: "Use Zod, never Yup", kind: "convention", session: "s1" });
    referenceMemory({ root, id: added.id, session: "s1" });
    referenceMemory({ root, id: added.id, session: "s2" });
    assert.equal(memoryEvolutionStatus(root).counts.durable, 1);
    assert.equal(recallEvolvingMemory({ root, query: "Zod", session: "s3" }).length, 1);
    assert.equal(runMemoryDream({ root }).entries, 1);
});

test("DEEP flow requires fresh mechanical evidence at verification boundaries", (t) => {
    const root = tempRoot(t);
    const session = startFlow({ root, goal: "Ship feature", mode: "deep" });
    assert.deepEqual(session.phases, ["FRAME", "RECON", "SHAPE", "PLAN", "WAVES", "VERIFY", "CROSS_AUDIT", "SHIP"]);
    assert.equal(flowStatus(root).currentPhase, "FRAME");
    assert.throws(() => decideFlow({ root, approve: true }), /artifact/);

    for (const [phase, summary] of [
        ["FRAME", "Goal, constraints, and acceptance criteria framed"],
        ["RECON", "Repository and dependency reconnaissance complete"],
        ["SHAPE", "Approach selected with tradeoffs"],
        ["PLAN", "Implementation plan split into dependency waves"],
    ]) {
        assert.equal(flowStatus(root).currentPhase, phase);
        recordFlowArtifact({ root, summary });
        decideFlow({ root, approve: true });
    }

    assert.equal(flowStatus(root).currentPhase, "WAVES");
    assert.throws(() => setWaveTable({ root, waves: [
        { id: "a", tasks: ["A"], dependsOn: ["b"] },
        { id: "b", tasks: ["B"], dependsOn: ["a"] },
    ] }), /cycle/);

    setWaveTable({ root, waves: [
        { id: "foundation", mode: "parallel", tasks: ["A", "B"], dependsOn: [] },
        { id: "integration", mode: "sequential", tasks: ["C"], dependsOn: ["foundation"] },
    ] });
    assert.deepEqual(readyWaves(root).map((wave) => wave.id), ["foundation"]);
    assert.throws(() => completeWave({ root, id: "integration", summary: "too early" }), /blocked/);
    completeWave({ root, id: "foundation", summary: "Foundation tasks verified" });
    assert.deepEqual(readyWaves(root).map((wave) => wave.id), ["integration"]);
    completeWave({ root, id: "integration", summary: "Integration verified" });
    recordFlowArtifact({ root, summary: "All execution waves completed with evidence" });
    decideFlow({ root, approve: true });

    assert.equal(flowStatus(root).currentPhase, "VERIFY");
    recordFlowArtifact({ root, summary: "Project checks reviewed" });
    assert.equal(flowEvidenceStatus(root).status, "blocked");
    assert.throws(() => decideFlow({ root, approve: true }), /preflight-passed/);
    appendReceipt(root, "preflight", { ts: futureTs(), action: "run", status: "passed", passed: true, results: [{ name: "test", ok: true }] });
    assert.equal(flowEvidenceStatus(root).status, "ready");
    decideFlow({ root, approve: true });

    assert.equal(flowStatus(root).currentPhase, "CROSS_AUDIT");
    recordFlowArtifact({ root, summary: "Independent reviewers completed" });
    appendReceipt(root, "cross-audit", { ts: futureTs(), action: "run-consensus", lineages: ["openai"] });
    assert.throws(() => decideFlow({ root, approve: true }), /cross-audit-2-lineages/);
    appendReceipt(root, "cross-audit", { ts: futureTs(), action: "run-consensus", lineages: ["openai", "google"], reviewers: ["codex", "gemini"] });
    decideFlow({ root, approve: true });
    assert.equal(flowStatus(root).currentPhase, "SHIP");
});

test("stale verification receipts cannot satisfy a later VERIFY phase", (t) => {
    const root = tempRoot(t);
    appendReceipt(root, "preflight", { ts: new Date(Date.now() - 60000).toISOString(), status: "passed", passed: true });
    startFlow({ root, goal: "Small fix", mode: "quick" });
    for (const phase of ["FRAME", "PLAN", "EXECUTE"]) {
        assert.equal(flowStatus(root).currentPhase, phase);
        recordFlowArtifact({ root, summary: `${phase} complete` });
        decideFlow({ root, approve: true });
    }
    recordFlowArtifact({ root, summary: "Checks reviewed" });
    assert.equal(flowEvidenceStatus(root).status, "blocked");
    assert.throws(() => decideFlow({ root, approve: true }), /preflight-passed/);
});

test("observability records only explicit local metrics", (t) => {
    const root = tempRoot(t);
    recordObservation({ root, runtime: "claude", inputTokens: 100, outputTokens: 20, cacheReadTokens: 40, savedTokens: 40, costUsd: 0.01 });
    const summary = summarizeObservability(root);
    assert.equal(summary.totals.events, 1);
    assert.equal(summary.totals.savedTokens, 40);
    assert.equal(summary.runtimes.claude.inputTokens, 100);
});

test("personalization requires evidence and two sessions before confirmation", (t) => {
    const root = tempRoot(t);
    const first = learnPreference({ root, preference: "Use compact prose", evidence: "Changed three verbose paragraphs to one", session: "s1" });
    assert.equal(first.confirmed, false);
    const second = learnPreference({ root, preference: "Use compact prose", evidence: "Shortened the release note again", session: "s2" });
    assert.equal(second.confirmed, true);
    assert.equal(profileStatus(root).effectiveInjection, false);
    setPersonalization({ root, inject: true });
    assert.equal(profileForInjection({ root, host: "example" }).preferences.length, 1);
    assert.equal(forgetPreference({ root, id: second.id }).remaining, 0);
});

test("design contract ships twelve templates and validates nine sections", (t) => {
    const root = tempRoot(t);
    assert.equal(listDesignTemplates().length, 12);
    initDesignContract({ root, template: "graphite", brand: "Demo" });
    assert.equal(checkDesignContract(root).valid, true);
});

test("audit findings are parsed and clustered as consensus or contested", () => {
    const parsed = parseReviewerFindings('{"findings":[{"severity":"important","title":"Missing null guard","evidence":"value can be undefined"}]}');
    assert.equal(parsed.length, 1);
    const clusters = clusterFindings([
        { reviewer: "a", lineage: "one", findings: parsed },
        { reviewer: "b", lineage: "two", findings: [{ severity: "blocking", title: "Missing null guard", evidence: "value may be undefined" }] },
        { reviewer: "c", lineage: "three", findings: [{ severity: "optional", title: "Rename local variable", evidence: "style only" }] },
    ]);
    assert.ok(clusters.some((item) => item.status === "consensus" && item.title.includes("null guard")));
    assert.ok(clusters.some((item) => item.status === "contested"));
});
