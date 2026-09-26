import { Command } from "commander";
import { downloadTemplate } from "giget";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
    SUPPORTED_RUNTIMES,
    addMemory,
    initMemory,
    memoryStatus,
    recallMemory,
    initTeam,
    installRuntime,
    prepareAudit,
    runPreflight,
} from "./v2-engine.js";

const REPO = "github:vudovn/ag-kit";

const withSource = async (branch, fn) => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-source-"));
    try {
        await downloadTemplate(branch ? `${REPO}#${branch}` : REPO, { dir, force: true });
        return await fn(dir);
    } finally {
        fs.rmSync(dir, { recursive: true, force: true });
    }
};

export const buildV2Program = () => {
    const program = new Command().name("ag-kit").description("AG Kit v2 multi-runtime commands");

    const runtime = program.command("runtime").description("Inspect or install runtime adapters");
    runtime.command("list").action(() => console.log(SUPPORTED_RUNTIMES.join("\n")));
    runtime.command("install <runtime>")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .option("-b, --branch <name>", "AG Kit source branch")
        .action(async (name, options) => {
            const result = await withSource(options.branch, (sourceRoot) => installRuntime({ sourceRoot, targetRoot: options.path, runtime: name }));
            console.log(JSON.stringify(result, null, 2));
        });

    const memory = program.command("memory").description("Local-first project memory");
    memory.command("init")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .action((options) => console.log(initMemory(options.path)));
    memory.command("add <text...>")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .option("--kind <kind>", "Entry kind", "learning")
        .option("--title <title>", "Entry title", "")
        .action((text, options) => console.log(JSON.stringify(addMemory({ root: options.path, text: text.join(" "), kind: options.kind, title: options.title }), null, 2)));
    memory.command("recall <query...>")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .option("--limit <n>", "Maximum results", "5")
        .action((query, options) => console.log(JSON.stringify(recallMemory({ root: options.path, query: query.join(" "), limit: options.limit }), null, 2)));
    memory.command("status")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .action((options) => console.log(JSON.stringify(memoryStatus(options.path), null, 2)));

    program.command("team")
        .description("Generate a project-specific specialist team")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .option("--archetype <type>", "software|web|research|content|game|operations|auto", "auto")
        .option("--name <name>", "Team name", "default")
        .option("--brief <text>", "Project brief", "")
        .action((options) => console.log(JSON.stringify(initTeam({ root: options.path, archetype: options.archetype, name: options.name, brief: options.brief }), null, 2)));

    program.command("cross-audit [target]")
        .description("Probe independent reviewer lineages and write an audit receipt")
        .option("-p, --path <dir>", "Project directory", process.cwd())
        .action((target = ".", options) => console.log(JSON.stringify(prepareAudit({ root: options.path, target }), null, 2)));

    program.command("preflight")
        .description("Run AG Kit blocking release gates")
        .option("-p, --path <dir>", "AG Kit repository directory", process.cwd())
        .action((options) => {
            const result = runPreflight({ root: options.path });
            for (const item of result.results) console.log(`${item.ok ? "PASS" : "FAIL"} ${item.name} ${item.durationMs}ms`);
            if (!result.passed) process.exitCode = 1;
        });

    return program;
};

export const runV2Cli = async (argv = process.argv) => buildV2Program().parseAsync(argv);
