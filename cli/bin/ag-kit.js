#!/usr/bin/env node
const command = process.argv[2];
const runtimeSubcommand = command === "runtime" ? process.argv[3] : "";
const memorySubcommand = command === "memory" ? process.argv[3] : "";
const helpRequested = [undefined, "help", "-h", "--help"].includes(command);
const versionRequested = ["-v", "--version"].includes(command);
const runtimeHelpRequested = command === "runtime" && [undefined, "help", "-h", "--help"].includes(runtimeSubcommand);
const v2Commands = new Set(["runtime", "memory", "team", "flow", "cross-audit", "observe", "dashboard", "personalize", "design", "route", "run", "preflight", "mcp"]);

if (helpRequested) {
    const { printMainHelp } = await import("../lib/help.js");
    printMainHelp();
} else if (versionRequested) {
    const { cliVersion } = await import("../lib/source-spec.js");
    process.stdout.write(`${cliVersion}\n`);
} else if (runtimeHelpRequested) {
    const { printRuntimeHelp } = await import("../lib/help.js");
    printRuntimeHelp();
} else if (command === "prompt-check") {
    const { runPromptCli } = await import("../lib/prompt-cli.js");
    await runPromptCli(process.argv);
} else if (command === "prompt-hook") {
    const { runPromptHookCli } = await import("../lib/prompt-hook.js");
    await runPromptHookCli(process.argv);
} else if (command === "hook-ingest") {
    const { runHookIngestCli } = await import("../lib/hook-ingest.js");
    await runHookIngestCli(process.argv);
} else if (command === "benchmark") {
    const { runBenchmarkCli } = await import("../lib/benchmark-cli.js");
    await runBenchmarkCli(process.argv);
} else if (command === "memory" && memorySubcommand === "semantic") {
    const { runSemanticMemoryCli } = await import("../lib/memory-semantic-cli.js");
    await runSemanticMemoryCli(process.argv);
} else if (command === "brain") {
    const { runBrainCli } = await import("../lib/brain-cli.js");
    await runBrainCli(process.argv);
} else if (["compress", "handoff"].includes(command)) {
    const { runContextCli } = await import("../lib/context-cli.js");
    await runContextCli(process.argv);
} else if (command === "runtime" && ["detect", "install-present"].includes(runtimeSubcommand)) {
    const { runRuntimeAutoCli } = await import("../lib/runtime-auto-cli.js");
    await runRuntimeAutoCli(process.argv);
} else if (v2Commands.has(command)) {
    const { runV2Cli } = await import("../lib/v2-cli.js");
    await runV2Cli(process.argv);
} else {
    const { printMainHelp } = await import("../lib/help.js");
    process.stderr.write(`[ag-kit] unknown command: ${String(command)}\n\n`);
    printMainHelp(process.stderr);
    process.exitCode = 1;
}
