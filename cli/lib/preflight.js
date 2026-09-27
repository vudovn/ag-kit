import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { appendReceipt } from "./v2-engine.js";
import { resolveSafeProjectRoot } from "./project-state.js";

const AG_KIT_SELF_GATES = [
    ["v2-architecture", "check:v2"],
    ["documentation-links", "check:docs"],
    ["v2-engine-tests", "test:v2"],
    ["runtime-contracts", "check:runtimes"],
    ["runtime-adapter-tests", "test:runtimes"],
    ["runtime-projections", "build:runtimes"],
    ["runtime-artifacts", "build:runtime-artifacts"],
    ["cli-tests", "test:cli"],
];

const COMMON_NODE_SCRIPTS = [
    ["lint", ["lint"]],
    ["typecheck", ["typecheck", "type-check", "check:types"]],
    ["test", ["test"]],
    ["build", ["build"]],
];

const readJson = (file, fallback = null) => {
    try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return fallback; }
};

const packageRunner = (root) => {
    if (fs.existsSync(path.join(root, "pnpm-lock.yaml"))) return { command: "pnpm", argsFor: (script) => ["run", script] };
    if (fs.existsSync(path.join(root, "yarn.lock"))) return { command: "yarn", argsFor: (script) => [script] };
    if (fs.existsSync(path.join(root, "bun.lockb")) || fs.existsSync(path.join(root, "bun.lock"))) return { command: "bun", argsFor: (script) => ["run", script] };
    return { command: "npm", argsFor: (script) => ["run", script] };
};

const firstAvailable = (commands) => {
    for (const command of commands) {
        const result = spawnSync(command, ["--version"], { encoding: "utf8", timeout: 3000, shell: false });
        if (!result.error && result.status === 0) return command;
    }
    return commands[0];
};

const normalizeCustomGate = (gate, index) => {
    if (!gate || typeof gate !== "object") throw new Error(`preflight gate ${index + 1} must be an object`);
    if (typeof gate.name !== "string" || !gate.name.trim()) throw new Error(`preflight gate ${index + 1} requires a name`);
    if (typeof gate.command !== "string" || !gate.command.trim()) throw new Error(`preflight gate ${gate.name} requires a command`);
    if (gate.args !== undefined && (!Array.isArray(gate.args) || gate.args.some((arg) => typeof arg !== "string"))) throw new Error(`preflight gate ${gate.name} args must be an array of strings`);
    const timeoutMs = gate.timeoutMs === undefined ? 240000 : Number(gate.timeoutMs);
    if (!Number.isFinite(timeoutMs) || timeoutMs < 1000 || timeoutMs > 1200000) throw new Error(`preflight gate ${gate.name} timeoutMs must be between 1000 and 1200000`);
    return {
        name: gate.name.trim(),
        command: gate.command.trim(),
        args: gate.args || [],
        blocking: gate.blocking !== false,
        timeoutMs,
        source: "custom",
    };
};

export function discoverPreflightGates(root = process.cwd()) {
    const resolvedRoot = resolveSafeProjectRoot(root);
    const customFile = path.join(resolvedRoot, ".ag-kit", "preflight.json");
    if (fs.existsSync(customFile)) {
        const config = readJson(customFile);
        if (!config || !Array.isArray(config.gates)) throw new Error(".ag-kit/preflight.json must contain a gates array");
        return {
            mode: "custom",
            source: path.relative(resolvedRoot, customFile),
            gates: config.gates.map(normalizeCustomGate),
        };
    }

    const gates = [];
    const pkgFile = path.join(resolvedRoot, "package.json");
    const pkg = fs.existsSync(pkgFile) ? readJson(pkgFile, {}) : {};
    const scripts = pkg?.scripts && typeof pkg.scripts === "object" ? pkg.scripts : {};
    const runner = packageRunner(resolvedRoot);

    if (scripts["check:v2"]) {
        for (const [name, script] of AG_KIT_SELF_GATES) {
            if (scripts[script]) gates.push({ name, command: runner.command, args: runner.argsFor(script), blocking: true, timeoutMs: 240000, source: "ag-kit-self" });
        }
        return { mode: "ag-kit-self", source: "package.json", gates };
    }

    const usedScripts = new Set();
    for (const [name, candidates] of COMMON_NODE_SCRIPTS) {
        const script = candidates.find((candidate) => scripts[candidate] && !usedScripts.has(candidate));
        if (!script) continue;
        const body = String(scripts[script] || "");
        if (script === "test" && /no test specified/i.test(body)) continue;
        usedScripts.add(script);
        gates.push({ name, command: runner.command, args: runner.argsFor(script), blocking: true, timeoutMs: name === "build" ? 300000 : 240000, source: "package.json" });
    }

    if (fs.existsSync(path.join(resolvedRoot, "Cargo.toml"))) {
        gates.push({ name: "rust-test", command: "cargo", args: ["test", "--all-targets"], blocking: true, timeoutMs: 300000, source: "Cargo.toml" });
    }
    if (fs.existsSync(path.join(resolvedRoot, "go.mod"))) {
        gates.push({ name: "go-test", command: "go", args: ["test", "./..."], blocking: true, timeoutMs: 300000, source: "go.mod" });
    }

    const pyproject = path.join(resolvedRoot, "pyproject.toml");
    const pytestIni = path.join(resolvedRoot, "pytest.ini");
    const testsDir = path.join(resolvedRoot, "tests");
    const pythonProject = fs.existsSync(pyproject) || fs.existsSync(pytestIni);
    const pytestConfigured = fs.existsSync(pytestIni)
        || (fs.existsSync(pyproject) && /\[tool\.pytest/i.test(fs.readFileSync(pyproject, "utf8")))
        || (pythonProject && fs.existsSync(testsDir));
    if (pytestConfigured) {
        gates.push({ name: "python-test", command: firstAvailable(["python3", "python"]), args: ["-m", "pytest"], blocking: true, timeoutMs: 300000, source: fs.existsSync(pytestIni) ? "pytest.ini" : "pyproject.toml" });
    }

    return { mode: "project", source: "auto-detect", gates };
}

export function runCurrentPreflight(root = process.cwd()) {
    const resolvedRoot = resolveSafeProjectRoot(root);
    const discovered = discoverPreflightGates(resolvedRoot);
    const results = discovered.gates.map((gate) => {
        const started = Date.now();
        const result = spawnSync(gate.command, gate.args, {
            cwd: resolvedRoot,
            encoding: "utf8",
            stdio: "pipe",
            timeout: gate.timeoutMs,
            shell: false,
        });
        const output = `${result.stdout || ""}${result.stderr || ""}`.trim().slice(-1600);
        return {
            name: gate.name,
            command: gate.command,
            args: gate.args,
            blocking: gate.blocking,
            ok: !result.error && result.status === 0,
            durationMs: Date.now() - started,
            exitCode: result.status,
            error: result.error?.message || null,
            output,
            source: gate.source,
        };
    });
    const blocking = results.filter((item) => item.blocking);
    const passed = results.length > 0 && blocking.every((item) => item.ok);
    const status = results.length === 0 ? "no-gates" : passed ? "passed" : "failed";
    appendReceipt(resolvedRoot, "preflight", {
        action: "run",
        mode: discovered.mode,
        source: discovered.source,
        status,
        passed,
        results: results.map(({ output, ...item }) => item),
    });
    return {
        passed,
        status,
        mode: discovered.mode,
        source: discovered.source,
        reason: results.length === 0 ? "No preflight gates were discovered. Add project scripts or .ag-kit/preflight.json." : null,
        results,
    };
}
