import test from "node:test";
import assert from "node:assert/strict";
import { buildProgram } from "../bin/index.js";

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";

const execFileAsync = promisify(execFile);

test("CLI exposes safe lifecycle commands", () => {
    const program = buildProgram();
    const commands = new Map(program.commands.map((command) => [command.name(), command]));

    assert.deepEqual([...commands.keys()], ["init", "update", "rollback", "status"]);
    assert.ok(commands.get("update").options.some((option) => option.long === "--strategy"));
    assert.ok(commands.get("update").options.some((option) => option.long === "--dry-run"));
    assert.ok(commands.get("rollback").options.some((option) => option.long === "--backup"));
});

test("CLI executes when invoked via symlink (npx simulation)", async () => {
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "ag-kit-symlink-test-"));
    const symlinkPath = path.join(tempDir, "ag-kit-bin");
    const binPath = path.resolve("bin/index.js");

    try {
        await fs.symlink(binPath, symlinkPath);
        const { stdout } = await execFileAsync(symlinkPath, ["--version"]);
        assert.ok(stdout.trim().length > 0, "CLI output should not be empty when invoked via symlink");
    } finally {
        await fs.rm(tempDir, { recursive: true, force: true });
    }
});
