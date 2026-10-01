import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { chunkText, dedupeFindings } from "../lib/audit-chunker.js";
import { snapshotAuditTarget } from "../lib/audit-consensus.js";

const tempRoot = (t) => { const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-audit-test-")); t.after(() => fs.rmSync(root, { recursive: true, force: true })); return root; };

test("chunkText bounds large inputs and keeps overlap", () => {
    const text = Array.from({ length: 900 }, (_, index) => `section ${index}\n${"x".repeat(70)}\n`).join("\n");
    const chunks = chunkText(text, { maxChars: 4000, overlapChars: 300 });
    assert.ok(chunks.length > 1);
    assert.ok(chunks.every((chunk) => chunk.text.length <= 4000));
    for (let index = 1; index < chunks.length; index += 1) {
        assert.ok(chunks[index].start < chunks[index - 1].end);
        assert.ok(chunks[index].end > chunks[index - 1].end);
    }
});

test("dedupeFindings merges repeated chunk findings and preserves highest severity", () => {
    const merged = dedupeFindings([
        { severity: "important", title: "Missing null guard", evidence: "value can be undefined before access" },
        { severity: "blocking", title: "Missing null guard", evidence: "value can be undefined before property access and crash" },
        { severity: "optional", title: "Rename local variable", evidence: "style only" },
    ]);
    assert.equal(merged.length, 2);
    const guard = merged.find((item) => item.title.includes("null guard"));
    assert.equal(guard.severity, "blocking");
    assert.equal(guard.occurrences, 2);
});

test("audit snapshot refuses symlink escape outside project root", (t) => {
    const root = tempRoot(t);
    const outside = tempRoot(t);
    const secret = path.join(outside, "secret.txt");
    fs.writeFileSync(secret, "outside-secret\n");
    const link = path.join(root, "linked.txt");
    try { fs.symlinkSync(secret, link, "file"); } catch (error) {
        if (["EPERM", "EACCES"].includes(error.code)) return;
        throw error;
    }
    assert.throws(() => snapshotAuditTarget({ root, target: "linked.txt" }), /resolving symlinks/);
});

test("audit snapshot is bounded and marks truncation", (t) => {
    const root = tempRoot(t);
    const file = path.join(root, "large.txt");
    fs.writeFileSync(file, "a".repeat(600 * 1024));
    const snapshot = snapshotAuditTarget({ root, target: "large.txt" });
    assert.equal(snapshot.truncated, true);
    assert.ok(Buffer.byteLength(snapshot.content) <= 512 * 1024 + 4);
    assert.equal(snapshot.originalBytes, 600 * 1024);
});
