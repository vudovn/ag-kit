import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory, memoryEvolutionStatus, recallEvolvingMemory, referenceMemory, runMemoryDream } from "../lib/memory-evolution.js";
import { decideFlow, flowStatus, recordFlowArtifact, setWaveTable, startFlow } from "../lib/workflow-session.js";
import { recordObservation, summarizeObservability } from "../lib/observability.js";
import { forgetPreference, learnPreference, profileForInjection, profileStatus, setPersonalization } from "../lib/personalization.js";
import { checkDesignContract, initDesignContract, listDesignTemplates } from "../lib/design-contract.js";
import { clusterFindings, parseReviewerFindings } from "../lib/audit-consensus.js";

const tempRoot = (t) => { const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-features-")); t.after(() => fs.rmSync(root, { recursive: true, force: true })); return root; };

test("memory evolves from candidate to durable across references and sessions", (t) => {
    const root = tempRoot(t);
    const added = addEvolvingMemory({ root, text: "Use Zod, never Yup", kind: "convention", session: "s1" });
    referenceMemory({ root, id: added.id, session: "s1" });
    referenceMemory({ root, id: added.id, session: "s2" });
    assert.equal(memoryEvolutionStatus(root).counts.durable, 1);
    assert.equal(recallEvolvingMemory({ root, query: "Zod", session: "s3" }).length, 1);
    assert.equal(runMemoryDream({ root }).entries, 1);
});

test("flow cannot advance without an artifact and DEEP converge requires waves", (t) => {
    const root = tempRoot(t);
    startFlow({ root, goal: "Ship feature", mode: "deep" });
    assert.throws(() => decideFlow({ root, approve: true }), /artifact summary/);
    recordFlowArtifact({ root, summary: "Three approaches compared; chose option B" });
    decideFlow({ root, approve: true });
    recordFlowArtifact({ root, summary: "Implementation plan approved" });
    decideFlow({ root, approve: true });
    recordFlowArtifact({ root, summary: "Dependencies grouped into waves" });
    assert.throws(() => decideFlow({ root, approve: true }), /wave table/);
    setWaveTable({ root, waves: [{ id: "w1", mode: "parallel", tasks: ["A", "B"], dependsOn: [] }] });
    decideFlow({ root, approve: true });
    assert.equal(flowStatus(root).currentPhase, "EXECUTE");
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
