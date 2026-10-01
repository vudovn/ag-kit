import { Command } from "commander";
import { downloadTemplate } from "giget";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { initMemory, memoryStatus, rebuildMemoryIndex, initTeam, prepareAudit } from "./v2-engine.js";
import { addEvolvingMemory, memoryEvolutionStatus, recallEvolvingMemory, referenceMemory, runMemoryDream, supersedeMemory } from "./memory-evolution.js";
import { RUNTIME_TARGETS, installRuntimeTarget } from "./runtime-registry.js";
import { doctorRuntimes, finalizeRuntimeInstall, prepareRuntimeInstall, restorePreparedInstall, uninstallRuntime } from "./runtime-lifecycle.js";
import { serveMcp } from "./mcp-server.js";
import { wireRuntimeMcp } from "./runtime-mcp.js";
import { runCurrentPreflight } from "./preflight.js";
import { completeWave, decideFlow, flowStatus, readyWaves, recordFlowArtifact, setWaveTable, startFlow } from "./workflow-session.js";
import { dashboardStatus, recordObservation, startDashboard, stopDashboard, summarizeObservability } from "./observability.js";
import { routeTask, runSandboxedCommand } from "./efficiency.js";
import { forgetPreference, learnPreference, listEgress, profileForInjection, profileStatus, setPersonalization } from "./personalization.js";
import { checkDesignContract, initDesignContract, listDesignTemplates } from "./design-contract.js";
import { runConsensusAudit } from "./audit-consensus.js";
import { runtimeSourceSpec } from "./source-spec.js";

const withSource = async (branch, fn) => { const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-source-")); try { await downloadTemplate(runtimeSourceSpec(branch), { dir, force: true }); return await fn(dir); } finally { fs.rmSync(dir, { recursive: true, force: true }); } };
const joined = (value) => Array.isArray(value) ? value.join(" ") : String(value || "");
const boolWord = (value) => ["on", "true", "1", "yes"].includes(String(value).toLowerCase());

export const buildV2Program = () => {
    const program = new Command().name("ag-kit").description("AG Kit v2 multi-runtime commands");

    const runtime = program.command("runtime").description("Inspect, install, verify, or safely remove runtime adapters");
    runtime.command("list").action(() => console.log(RUNTIME_TARGETS.join("\n")));
    runtime.command("install <runtime>").option("-p, --path <dir>", "Project directory", process.cwd()).option("-b, --branch <name>", "Explicit AG Kit source branch/ref override").action(async (name, options) => {
        const prepared = prepareRuntimeInstall({ root: options.path, runtime: name });
        try {
            const installed = await withSource(options.branch, (sourceRoot) => installRuntimeTarget({ sourceRoot, targetRoot: options.path, runtime: name }));
            const mcp = wireRuntimeMcp({ root: options.path, runtime: name });
            const lifecycle = finalizeRuntimeInstall({ prepared, mcp });
            console.log(JSON.stringify({ ...installed, mcp, lifecycle: { manifest: `.ag-kit/runtime-installs/${name}.json`, installedAt: lifecycle.installedAt } }, null, 2));
        } catch (error) {
            const recovery = restorePreparedInstall(prepared);
            error.message = `${error.message}\nAG Kit restored pre-install runtime paths: ${recovery.results.length}`;
            throw error;
        }
    });
    runtime.command("doctor [runtime]").option("-p, --path <dir>", "Project directory", process.cwd()).action((name = "", options) => console.log(JSON.stringify(doctorRuntimes({ root: options.path, runtime: name }), null, 2)));
    runtime.command("uninstall <runtime>").option("-p, --path <dir>", "Project directory", process.cwd()).action((name, options) => console.log(JSON.stringify(uninstallRuntime({ root: options.path, runtime: name }), null, 2)));

    const memory = program.command("memory").description("Local-first evolving project memory");
    memory.command("init").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(initMemory(options.path)));
    memory.command("add <text...>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--kind <kind>", "Entry kind", "learning").option("--title <title>", "Entry title", "").option("--session <id>", "Session id", "manual").option("--valid-from <iso>", "Validity start", "").option("--valid-to <iso>", "Validity end", "").option("--durable", "Mark immediately durable", false).action((body, options) => console.log(JSON.stringify(addEvolvingMemory({ root: options.path, text: joined(body), kind: options.kind, title: options.title, session: options.session, validFrom: options.validFrom, validTo: options.validTo, durable: options.durable }), null, 2)));
    memory.command("recall <query...>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--limit <n>", "Maximum results", "5").option("--session <id>", "Session id", "manual").option("--at <iso>", "Recall what was valid at an ISO timestamp", new Date().toISOString()).action((query, options) => console.log(JSON.stringify(recallEvolvingMemory({ root: options.path, query: joined(query), limit: options.limit, session: options.session, at: options.at }), null, 2)));
    memory.command("touch <id>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--session <id>", "Session id", "manual").action((id, options) => console.log(JSON.stringify(referenceMemory({ root: options.path, id, session: options.session }), null, 2)));
    memory.command("supersede <id> <text...>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--title <title>", "Replacement title", "").option("--kind <kind>", "Replacement kind", "decision").option("--session <id>", "Session id", "manual").option("--valid-from <iso>", "Validity start", "").option("--valid-to <iso>", "Validity end", "").action((id, body, options) => console.log(JSON.stringify(supersedeMemory({ root: options.path, id, text: joined(body), title: options.title, kind: options.kind, session: options.session, validFrom: options.validFrom, validTo: options.validTo }), null, 2)));
    memory.command("dream").option("-p, --path <dir>", "Project directory", process.cwd()).option("--stale-days <n>", "Archive unreferenced candidates older than this", "180").action((options) => console.log(JSON.stringify(runMemoryDream({ root: options.path, staleDays: Number(options.staleDays) }), null, 2)));
    memory.command("reindex").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(rebuildMemoryIndex(options.path), null, 2)));
    memory.command("status").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify({ ...memoryStatus(options.path), evolution: memoryEvolutionStatus(options.path) }, null, 2)));

    program.command("team").description("Generate a project-specific specialist team").option("-p, --path <dir>", "Project directory", process.cwd()).option("--archetype <type>", "software|web|research|content|game|operations|auto", "auto").option("--name <name>", "Team name", "default").option("--brief <text>", "Project brief", "").action((options) => console.log(JSON.stringify(initTeam({ root: options.path, archetype: options.archetype, name: options.name, brief: options.brief }), null, 2)));

    const flow = program.command("flow").description("Plan-before-build workflow with explicit user gates");
    flow.command("start <goal...>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--mode <mode>", "quick|standard|deep", "standard").option("--force", "Replace an active flow", false).action((goal, options) => console.log(JSON.stringify(startFlow({ root: options.path, goal: joined(goal), mode: options.mode, force: options.force }), null, 2)));
    flow.command("status").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(flowStatus(options.path), null, 2)));
    flow.command("artifact <summary...>").option("-p, --path <dir>", "Project directory", process.cwd()).option("--file <path>", "Artifact path", "").action((summary, options) => console.log(JSON.stringify(recordFlowArtifact({ root: options.path, summary: joined(summary), artifactPath: options.file }), null, 2)));
    flow.command("waves <json>").option("-p, --path <dir>", "Project directory", process.cwd()).action((json, options) => console.log(JSON.stringify(setWaveTable({ root: options.path, waves: JSON.parse(json) }), null, 2)));
    flow.command("ready").description("List execution waves whose dependencies are satisfied").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(readyWaves(options.path), null, 2)));
    flow.command("wave-complete <id> <summary...>").description("Checkpoint a completed execution wave with evidence").option("-p, --path <dir>", "Project directory", process.cwd()).action((id, summary, options) => console.log(JSON.stringify(completeWave({ root: options.path, id, summary: joined(summary) }), null, 2)));
    flow.command("approve [note...]").option("-p, --path <dir>", "Project directory", process.cwd()).action((note, options) => console.log(JSON.stringify(decideFlow({ root: options.path, approve: true, note: joined(note) }), null, 2)));
    flow.command("reject [note...]").option("-p, --path <dir>", "Project directory", process.cwd()).action((note, options) => console.log(JSON.stringify(decideFlow({ root: options.path, approve: false, note: joined(note) }), null, 2)));

    program.command("cross-audit [target]").description("Run independent read-only reviewers and classify consensus/contested findings").option("-p, --path <dir>", "Project directory", process.cwd()).option("--probe", "Only probe available reviewer CLIs").option("--reviewers <n>", "Maximum independent lineages", "3").option("--exclude-lineage <name>", "Exclude the calling model lineage", process.env.AG_KIT_CALLING_LINEAGE || "").action(async (target = ".", options) => console.log(JSON.stringify(options.probe ? prepareAudit({ root: options.path, target }) : await runConsensusAudit({ root: options.path, target, reviewers: options.reviewers, excludeLineage: options.excludeLineage }), null, 2)));

    program.command("observe <kind>").description("Append a bounded local observability/token event").option("-p, --path <dir>", "Project directory", process.cwd()).option("--runtime <name>", "Runtime", "unknown").option("--session <id>", "Session", "manual").option("--input <n>", "Input tokens", "0").option("--output <n>", "Output tokens", "0").option("--cached <n>", "Cache-read tokens", "0").option("--saved <n>", "Explicitly measured/known saved tokens", "0").option("--cost <usd>", "Recorded cost in USD", "0").action((kind, options) => console.log(JSON.stringify(recordObservation({ root: options.path, runtime: options.runtime, session: options.session, kind, inputTokens: options.input, outputTokens: options.output, cacheReadTokens: options.cached, savedTokens: options.saved, costUsd: options.cost }), null, 2)));
    const dashboard = program.command("dashboard").description("Local observability dashboard");
    dashboard.command("summary").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(summarizeObservability(options.path), null, 2)));
    dashboard.command("start").option("-p, --path <dir>", "Project directory", process.cwd()).option("--port <n>", "Local port", "4737").action((options) => startDashboard({ root: options.path, port: Number(options.port) }));
    dashboard.command("status").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(dashboardStatus(options.path), null, 2)));
    dashboard.command("stop").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(stopDashboard(options.path), null, 2)));

    const personalize = program.command("personalize").description("Evidence-backed local personalization and privacy controls");
    personalize.command("status").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(profileStatus(options.path), null, 2)));
    personalize.command("on").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(setPersonalization({ root: options.path, enabled: true }), null, 2)));
    personalize.command("off").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(setPersonalization({ root: options.path, enabled: false }), null, 2)));
    personalize.command("inject <state>").option("-p, --path <dir>", "Project directory", process.cwd()).action((state, options) => console.log(JSON.stringify(setPersonalization({ root: options.path, inject: boolWord(state) }), null, 2)));
    personalize.command("learn <preference...>").requiredOption("--evidence <text>", "Verbatim evidence span").option("--session <id>", "Session id", "manual").option("-p, --path <dir>", "Project directory", process.cwd()).action((preference, options) => console.log(JSON.stringify(learnPreference({ root: options.path, preference: joined(preference), evidence: options.evidence, session: options.session }), null, 2)));
    personalize.command("preview").option("--host <name>", "Cloud/runtime host receiving confirmed profile", "").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(profileForInjection({ root: options.path, host: options.host }), null, 2)));
    personalize.command("forget [id]").option("-p, --path <dir>", "Project directory", process.cwd()).action((id = "all", options) => console.log(JSON.stringify(forgetPreference({ root: options.path, id }), null, 2)));
    personalize.command("egress").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => console.log(JSON.stringify(listEgress(options.path), null, 2)));

    const design = program.command("design").description("Create and validate a cross-runtime DESIGN.md contract");
    design.command("list").action(() => console.log(listDesignTemplates().join("\n")));
    design.command("init").option("-p, --path <dir>", "Project directory", process.cwd()).option("--template <name>", "Template name or blank", "graphite").option("--brand <name>", "Brand/product name", "Project").option("--force", "Replace an existing DESIGN.md", false).action((options) => console.log(JSON.stringify(initDesignContract({ root: options.path, template: options.template, brand: options.brand, force: options.force }), null, 2)));
    design.command("check").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => { const result = checkDesignContract(options.path); console.log(JSON.stringify(result, null, 2)); if (!result.valid) process.exitCode = 1; });

    program.command("route <task...>").description("Choose a runtime-neutral role, effort tier, and flow depth").option("-p, --path <dir>", "Project directory", process.cwd()).action((task, options) => console.log(JSON.stringify(routeTask(joined(task), options.path), null, 2)));
    program.command("run <command> [args...]").description("Run a command without shell interpolation, keep full output on disk, and return a bounded summary").option("-p, --path <dir>", "Project directory", process.cwd()).option("--timeout <ms>", "Timeout in milliseconds", "120000").option("--max-lines <n>", "Maximum summary lines", "40").action((command, args = [], options) => { const result = runSandboxedCommand({ root: options.path, command, args, timeoutMs: Number(options.timeout), maxSummaryLines: Number(options.maxLines) }); console.log(result.summary); console.log(`\n[ag-kit] full output: ${result.log}`); if (!result.ok) process.exitCode = Number.isInteger(result.exitCode) ? result.exitCode : 1; });

    program.command("preflight").description("Run project-aware blocking ship gates").option("-p, --path <dir>", "Project directory", process.cwd()).action((options) => { const result = runCurrentPreflight(options.path); console.log(`[ag-kit] preflight ${result.mode}/${result.status}`); for (const item of result.results) console.log(`${item.ok ? "PASS" : "FAIL"} ${item.name} ${item.durationMs}ms`); if (result.reason) console.log(`[ag-kit] ${result.reason}`); if (!result.passed) process.exitCode = 1; });
    const mcp = program.command("mcp").description("AG Kit MCP bridge"); mcp.command("serve").description("Serve the project-local AG Kit MCP over stdio").action(serveMcp);
    return program;
};
export const runV2Cli = async (argv = process.argv) => buildV2Program().parseAsync(argv);
