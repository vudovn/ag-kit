import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { appendReceipt } from "../lib/v2-engine.js";
import { runSandboxedCommand } from "../lib/efficiency.js";
import { recordObservation } from "../lib/observability.js";
import { runCurrentPreflight } from "../lib/preflight.js";
import { currentTraceId } from "../lib/trace-context.js";
import { startFlow } from "../lib/workflow-session.js";

const tempRoot = (t) => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-trace-"));
    t.after(() => fs.rmSync(root, { recursive: true, force: true }));
    return root;
};

test("active flow trace correlates receipts, observations, preflight children, and sandbox commands", (t) => {
    const root = tempRoot(t);
    const flow = startFlow({ root, goal: "trace evidence", mode: "quick" });
    assert.equal(flow.traceId, flow.id);
    assert.equal(currentTraceId(root), flow.id);

    const receipt = appendReceipt(root, "trace-test", { action: "check" });
    assert.equal(receipt.traceId, flow.id);
    const observation = recordObservation({ root, runtime: "test", kind: "trace" });
    assert.equal(observation.traceId, flow.id);

    const traceFile = path.join(root, "trace-child.txt");
    fs.mkdirSync(path.join(root, ".ag-kit"), { recursive: true });
    fs.writeFileSync(path.join(root, ".ag-kit", "preflight.json"), JSON.stringify({
        gates: [{ name: "trace-child", command: process.execPath, args: ["-e", `require("fs").writeFileSync(${JSON.stringify(traceFile)}, process.env.AG_KIT_TRACE_ID || "")`] }],
    }, null, 2));
    const preflight = runCurrentPreflight(root);
    assert.equal(preflight.passed, true);
    assert.equal(fs.readFileSync(traceFile, "utf8"), flow.id);

    const sandbox = runSandboxedCommand({ root, command: process.execPath, args: ["-e", "console.log(process.env.AG_KIT_TRACE_ID || '')"] });
    assert.equal(sandbox.traceId, flow.id);
    assert.match(sandbox.summary, new RegExp(flow.id));
});

test("trace correlation stays absent when no active flow or explicit trace exists", (t) => {
    const root = tempRoot(t);
    assert.equal(currentTraceId(root), null);
    const receipt = appendReceipt(root, "trace-test", { action: "idle" });
    assert.equal(Object.hasOwn(receipt, "traceId"), false);
    const observation = recordObservation({ root, runtime: "test", kind: "idle" });
    assert.equal(Object.hasOwn(observation, "traceId"), false);
});
