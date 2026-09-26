import test from "node:test";
import assert from "node:assert/strict";
import { buildProgram } from "../bin/index.js";
import { buildV2Program } from "../lib/v2-cli.js";
import { addMemory, recallMemory, initTeam } from "../lib/v2-engine.js";

test("legacy CLI keeps safe lifecycle commands", () => {
    const program = buildProgram();
    const commands = new Map(program.commands.map((command) => [command.name(), command]));
    assert.deepEqual([...commands.keys()], ["init", "update", "rollback", "status"]);
    assert.ok(commands.get("update").options.some((option) => option.long === "--strategy"));
    assert.ok(commands.get("rollback").options.some((option) => option.long === "--backup"));
});

test("v2 CLI exposes runtime, memory, team, audit, and preflight", () => {
    const names = buildV2Program().commands.map((command) => command.name());
    assert.deepEqual(names, ["runtime", "memory", "team", "cross-audit", "preflight"]);
});

test("v2 memory and team engines are project-local", async (t) => {
    const { mkdtemp, rm, writeFile } = await import("node:fs/promises");
    const { tmpdir } = await import("node:os");
    const path = await import("node:path");
    const root = await mkdtemp(path.join(tmpdir(), "ag-kit-v2-cli-"));
    t.after(() => rm(root, { recursive: true, force: true }));
    await writeFile(path.join(root, "package.json"), "{}");
    addMemory({ root, text: "Use transactions for billing", kind: "decision" });
    assert.equal(recallMemory({ root, query: "billing" }).length, 1);
    assert.equal(initTeam({ root, archetype: "auto" }).archetype, "software");
});

test("CLI runs when invoked through an npm bin symlink", async (t) => {
    const { mkdtemp, mkdir, symlink, rm } = await import("node:fs/promises");
    const { tmpdir } = await import("node:os");
    const path = await import("node:path");
    const { execFile } = await import("node:child_process");
    const { promisify } = await import("node:util");
    const run = promisify(execFile);
    const dir = await mkdtemp(path.join(tmpdir(), "ag-kit-symlink-"));
    t.after(() => rm(dir, { recursive: true, force: true }));
    const binDir = path.join(dir, ".bin"); await mkdir(binDir);
    const link = path.join(binDir, "ag-kit"); await symlink(path.resolve("bin/ag-kit.js"), link);
    const { stdout } = await run(process.execPath, [link, "--version"]);
    assert.match(stdout.trim(), /^\d{4}\.\d+\.\d+$/);
});
