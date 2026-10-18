import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory, memoryEvolutionStatus, recallEvolvingMemory, supersedeMemory } from "../lib/memory-evolution.js";
import { memoryGraphStatus, parseMemoryRelations, rebuildMemoryGraph } from "../lib/memory-graph.js";

const tempRoot = (t) => { const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-memory-graph-")); t.after(() => fs.rmSync(root, { recursive: true, force: true })); return root; };

test("memory relation parser ignores code examples and extracts links, tags, metadata, and facts", () => {
    const parsed = parseMemoryRelations(`Use [[Billing Service]] with #architecture/backend.\n[owner:: platform-team]\nDatabase: PostgreSQL\n\`[[fake-link]] #fake [owner:: fake]\`\n\`\`\`md\n[[also-fake]] #fake/two\n\`\`\``);
    assert.deepEqual(parsed.links.map((item) => item.target), ["billing-service"]);
    assert.deepEqual(parsed.tags.map((item) => item.path), ["architecture/backend"]);
    assert.deepEqual(parsed.meta, [{ key: "owner", value: "platform-team" }]);
    assert.ok(parsed.facts.some((item) => item.predicate === "owner" && item.object === "platform-team"));
    assert.ok(parsed.facts.some((item) => item.predicate === "database" && item.object === "PostgreSQL"));
});

test("near-duplicate ingest reuses same-kind memory but keeps different kinds distinct", (t) => {
    const root = tempRoot(t);
    const first = addEvolvingMemory({ root, text: "Use PostgreSQL transactions for billing writes and keep retries idempotent", kind: "decision", session: "s1" });
    const duplicate = addEvolvingMemory({ root, text: "Use PostgreSQL transactions for billing writes and keep retries idempotent", kind: "decision", session: "s2" });
    assert.equal(duplicate.deduped, true);
    assert.equal(duplicate.id, first.id);
    const otherKind = addEvolvingMemory({ root, text: "Use PostgreSQL transactions for billing writes and keep retries idempotent", kind: "learning", session: "s2" });
    assert.equal(otherKind.deduped, false);
    assert.notEqual(otherKind.id, first.id);
    assert.equal(memoryEvolutionStatus(root).graph.entries, 2);
});

test("supersede always creates a new durable temporal replacement", (t) => {
    const root = tempRoot(t);
    const first = addEvolvingMemory({ root, text: "API timeout is 30 seconds for checkout requests", kind: "decision", durable: true, session: "s1" });
    const next = supersedeMemory({ root, id: first.id, text: "API timeout is 30 seconds for checkout requests", kind: "decision", session: "s2" });
    assert.notEqual(next.replacement.id, first.id);
    assert.equal(next.old.status, "superseded");
    assert.equal(next.replacement.status, "durable");
});

test("graph sidecar is rebuildable and recall returns structured relations", (t) => {
    const root = tempRoot(t);
    const added = addEvolvingMemory({ root, text: "[[Auth Service]] owns #security/auth.\n[owner:: identity-team]", kind: "convention", durable: true, session: "s1" });
    const graphFile = path.join(root, ".ag-kit", "memory", "graph.json");
    fs.rmSync(graphFile);
    const rebuilt = rebuildMemoryGraph(root);
    assert.ok(rebuilt.entries[added.id]);
    const status = memoryGraphStatus(root);
    assert.equal(status.links, 1);
    assert.equal(status.tags, 1);
    const recalled = recallEvolvingMemory({ root, query: "Auth Service", session: "s2" });
    assert.equal(recalled.length, 1);
    assert.equal(recalled[0].relations.links[0].target, "auth-service");
    assert.equal(recalled[0].relations.meta[0].key, "owner");
});
