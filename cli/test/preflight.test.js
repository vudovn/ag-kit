import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { discoverPreflightGates, runCurrentPreflight } from "../lib/preflight.js";

const tempRoot = (t) => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-preflight-"));
    t.after(() => fs.rmSync(root, { recursive: true, force: true }));
    return root;
};

test("preflight auto-detects common project scripts instead of AG Kit-only gates", (t) => {
    const root = tempRoot(t);
    fs.writeFileSync(path.join(root, "package.json"), JSON.stringify({
        scripts: {
            lint: "node -e \"process.exit(0)\"",
            typecheck: "node -e \"process.exit(0)\"",
            test: "node -e \"process.exit(0)\"",
            build: "node -e \"process.exit(0)\"",
        },
    }));
    const discovered = discoverPreflightGates(root);
    assert.equal(discovered.mode, "project");
    assert.deepEqual(discovered.gates.map((gate) => gate.name), ["lint", "typecheck", "test", "build"]);
    assert.ok(discovered.gates.every((gate) => gate.command === "npm"));
});

test("custom preflight gates are shell-free, explicit, and blocking", (t) => {
    const root = tempRoot(t);
    fs.mkdirSync(path.join(root, ".ag-kit"), { recursive: true });
    fs.writeFileSync(path.join(root, ".ag-kit", "preflight.json"), JSON.stringify({
        schema: 1,
        gates: [
            { name: "portable-smoke", command: process.execPath, args: ["-e", "process.exit(0)"], blocking: true, timeoutMs: 10000 },
        ],
    }));
    const result = runCurrentPreflight(root);
    assert.equal(result.mode, "custom");
    assert.equal(result.status, "passed");
    assert.equal(result.passed, true);
    assert.equal(result.results[0].ok, true);
});

test("preflight reports no-gates instead of claiming a pass", (t) => {
    const root = tempRoot(t);
    const result = runCurrentPreflight(root);
    assert.equal(result.status, "no-gates");
    assert.equal(result.passed, false);
    assert.match(result.reason, /No preflight gates/);
});
