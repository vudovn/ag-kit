import fs from "node:fs";
import path from "node:path";
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";
import { initTeam, memoryStatus, probeRoster } from "./v2-engine.js";
import { addEvolvingMemory, memoryEvolutionStatus, recallEvolvingMemory } from "./memory-evolution.js";
import { semanticRecall } from "./memory-semantic.js";
import { brainStatus, searchAcrossProjects } from "./memory-registry.js";
import { doctorRuntimes } from "./runtime-lifecycle.js";
import { checkPromptQuality, PROMPT_QUALITY_MAX_CHARS } from "./prompt-quality.js";

const projectRoot = () => path.resolve(process.env.AG_KIT_PROJECT || process.cwd());
const text = (value) => ({ content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }] });
const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true };
const additive = { readOnlyHint: false, destructiveHint: false, idempotentHint: false };

export function runtimeStatusForMcp(root = projectRoot()) {
    const resolved = path.resolve(root);
    const runtimes = doctorRuntimes({ root: resolved });
    if (runtimes.length) {
        return { installed: true, projectRoot: resolved, runtimes, source: "lifecycle-manifests" };
    }

    const legacyFile = path.join(resolved, ".ag-kit", "runtime.json");
    if (!fs.existsSync(legacyFile)) return { installed: false, projectRoot: resolved, runtimes: [], source: "none" };
    try {
        const legacy = JSON.parse(fs.readFileSync(legacyFile, "utf8"));
        return { installed: true, projectRoot: resolved, runtimes: [], legacy, source: "legacy-runtime-json" };
    } catch {
        return { installed: false, projectRoot: resolved, runtimes: [], source: "invalid-legacy-runtime-json" };
    }
}

export const createMcpServer = () => {
    const server = new McpServer({ name: "ag-kit", version: "2.0.0" });
    server.registerTool("ag_prompt_check", { description: "Deterministically check whether a task has enough concrete context to act without guessing. Returns signals/questions only; raw prompt text is never persisted by this tool.", inputSchema: z.object({ prompt: z.string().min(1).max(PROMPT_QUALITY_MAX_CHARS), force: z.boolean().default(false) }), annotations: readOnly }, async ({ prompt, force }) => text(checkPromptQuality(prompt, { force })));
    server.registerTool("ag_memory_recall", { description: "Recall relevant project memory with temporal validity and recency-aware ranking.", inputSchema: z.object({ query: z.string().min(1), limit: z.number().int().min(1).max(20).default(5), session: z.string().default("mcp"), at: z.string().default(() => new Date().toISOString()) }), annotations: readOnly }, async ({ query, limit, session, at }) => text(recallEvolvingMemory({ root: projectRoot(), query, limit, session, at })));
    server.registerTool("ag_memory_semantic_recall", { description: "Explicit opt-in semantic recall using a project-local rebuildable vector cache. Requires the optional @huggingface/transformers package. Model downloads are disabled unless allowDownload=true.", inputSchema: z.object({ query: z.string().min(1).max(12000), limit: z.number().int().min(1).max(20).default(5), model: z.string().max(300).optional(), allowDownload: z.boolean().default(false) }), annotations: readOnly }, async ({ query, limit, model, allowDownload }) => text(await semanticRecall({ root: projectRoot(), query, limit, overrides: { enabled: true, allowDownload, ...(model ? { model } : {}) } })));
    server.registerTool("ag_memory_search_all", { description: "Search memory across projects the user explicitly registered with AG Kit. Never scans the home directory automatically.", inputSchema: z.object({ query: z.string().min(1), limit: z.number().int().min(1).max(50).default(10), at: z.string().default(() => new Date().toISOString()), excludeCurrent: z.boolean().default(false) }), annotations: readOnly }, async ({ query, limit, at, excludeCurrent }) => text(searchAcrossProjects({ query, limit, at, currentRoot: excludeCurrent ? projectRoot() : "" })));
    server.registerTool("ag_memory_status", { description: "Inspect local canonical memory, warm index, and evolution state.", inputSchema: z.object({}), annotations: readOnly }, async () => text({ ...memoryStatus(projectRoot()), evolution: memoryEvolutionStatus(projectRoot()) }));
    server.registerTool("ag_brain_status", { description: "Inspect the opt-in cross-project registry without modifying it.", inputSchema: z.object({}), annotations: readOnly }, async () => text(brainStatus()));
    server.registerTool("ag_memory_add", { description: "Add a concise verified candidate memory. It becomes durable after repeated references across sessions unless marked durable explicitly by the CLI.", inputSchema: z.object({ text: z.string().min(1).max(12000), kind: z.enum(["decision", "convention", "learning", "handoff", "constraint"]).default("learning"), title: z.string().max(160).default(""), session: z.string().default("mcp") }), annotations: additive }, async ({ text: body, kind, title, session }) => text(addEvolvingMemory({ root: projectRoot(), text: body, kind, title, session })));
    server.registerTool("ag_team_init", { description: "Generate a small project-local specialist team from an explicit archetype.", inputSchema: z.object({ archetype: z.enum(["auto", "software", "web", "research", "content", "game", "operations"]).default("auto"), name: z.string().min(1).max(80).default("default"), brief: z.string().max(4000).default("") }), annotations: additive }, async ({ archetype, name, brief }) => text(initTeam({ root: projectRoot(), archetype, name, brief })));
    server.registerTool("ag_runtime_status", { description: "Inspect every AG Kit-managed runtime lifecycle state for this project; falls back to legacy single-runtime metadata only when no lifecycle manifests exist.", inputSchema: z.object({}), annotations: readOnly }, async () => text(runtimeStatusForMcp(projectRoot())));
    server.registerTool("ag_cross_audit_probe", { description: "Probe which independent local AI reviewer CLIs are reachable; does not run a review.", inputSchema: z.object({}), annotations: readOnly }, async () => text(probeRoster()));
    return server;
};
export const serveMcp = async () => serveStdio(() => createMcpServer());
