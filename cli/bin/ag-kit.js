#!/usr/bin/env node
const command = process.argv[2];
const v2Commands = new Set(["runtime", "memory", "team", "flow", "cross-audit", "observe", "dashboard", "personalize", "design", "preflight", "mcp"]);

if (v2Commands.has(command)) {
    const { runV2Cli } = await import("../lib/v2-cli.js");
    await runV2Cli(process.argv);
} else {
    const { runCli } = await import("./index.js");
    await runCli(process.argv);
}
