import { spawnSync } from "node:child_process";
import { appendReceipt } from "./v2-engine.js";

const gates = [
    ["v2-architecture", ["run", "check:v2"]],
    ["documentation-links", ["run", "check:docs"]],
    ["v2-engine-tests", ["run", "test:v2"]],
    ["runtime-contracts", ["run", "check:runtimes"]],
    ["runtime-adapter-tests", ["run", "test:runtimes"]],
    ["runtime-projections", ["run", "build:runtimes"]],
    ["runtime-artifacts", ["run", "build:runtime-artifacts"]],
    ["cli-tests", ["run", "test:cli"]],
];

export function runCurrentPreflight(root = process.cwd()) {
    const results = gates.map(([name, args]) => {
        const started = Date.now();
        const result = spawnSync("npm", args, { cwd: root, encoding: "utf8", stdio: "pipe", timeout: 240000, shell: false });
        return { name, blocking: true, ok: result.status === 0, durationMs: Date.now() - started, exitCode: result.status, output: (result.stdout || result.stderr || "").trim().slice(-1200) };
    });
    const passed = results.every((item) => item.ok);
    appendReceipt(root, "preflight", { action: "run", passed, results: results.map(({ output, ...item }) => item) });
    return { passed, results };
}
