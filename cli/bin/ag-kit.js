#!/usr/bin/env node
const command = process.argv[2];
const runtimeSubcommand = command === "runtime" ? process.argv[3] : "";
const v2Commands = new Set(["runtime", "memory", "team", "flow", "cross-audit", "observe", "dashboard", "personalize", "design", "route", "run", "preflight", "mcp"]);

if (command === "brain") {
    const { runBrainCli } = await import("../lib/brain-cli.js");
    await runBrainCli(process.argv);
} else if (command === "runtime" && ["detect", "install-present"].includes(runtimeSubcommand)) {
    const { runRuntimeAutoCli } = await import("../lib/runtime-auto-cli.js");
    await runRuntimeAutoCli(process.argv);
} else if (v2Commands.has(command)) {
    const { runV2Cli } = await import("../lib/v2-cli.js");
    await runV2Cli(process.argv);
} else {
    const { runCli } = await import("./index.js");
    await runCli(process.argv);
}
