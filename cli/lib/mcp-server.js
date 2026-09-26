import fs from "node:fs";
import path from "node:path";
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";
import { addMemory, initTeam, memoryStatus, probeRoster, recallMemory } from "./v2-engine.js";

const projectRoot = () => path.resolve(process.env.AG_KIT_PROJECT || process.cwd());
const text = (value) => ({ content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }] });
const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true };
const additive = { readOnlyHint: false, destructiveHint: false, idempotentHint: false };

export const createMcpServer = () => {
    const server = new McpServer({ name: "ag-kit", version: "2.0.0" });
    server.registerTool("ag_memory_recall", { description: "Recall relevant project memory from the local AG Kit markdown store.", inputSchema: z.object({ query: z.string().min(1), limit: z.number().int().min(1).max(20).default(5) }), annotations: readOnly }, async ({ query, limit }) => text(recallMemory({ root: projectRoot(), query, limit })));
    server.registerTool("ag_memory_status", { description: "Inspect the local AG Kit memory store without modifying it.", inputSchema: z.object({}), annotations: readOnly }, async () => text(memoryStatus(projectRoot())));
    server.registerTool("ag_memory_add", { description: "Add a concise verified decision, convention, learning, or handoff note to project memory.", inputSchema: z.object({ text: z.string().min(1).max(12000), kind: z.enum(["decision", "convention", "learning", "handoff", "constraint"]).default("learning"), title: z.string().max(160).default("") }), annotations: additive }, async ({ text: body, kind, title }) => text(addMemory({ root: projectRoot(), text: body, kind, title })));
    server.registerTool("ag_team_init", { description: "Generate a small project-local specialist team from an explicit archetype.", inputSchema: z.object({ archetype: z.enum(["auto", "software", "web", "research", "content", "game", "operations"]).default("auto"), name: z.string().min(1).max(80).default("default"), brief: z.string().max(4000).default("") }), annotations: additive }, async ({ archetype, name, brief }) => text(initTeam({ root: projectRoot(), archetype, name, brief })));
    server.registerTool("ag_runtime_status", { description: "Read AG Kit runtime installation state for this project.", inputSchema: z.object({}), annotations: readOnly }, async () => { const file = path.join(projectRoot(), ".ag-kit", "runtime.json"); if (!fs.existsSync(file)) return text({ installed: false, projectRoot: projectRoot() }); return text({ installed: true, projectRoot: projectRoot(), ...JSON.parse(fs.readFileSync(file, "utf8")) }); });
    server.registerTool("ag_cross_audit_probe", { description: "Probe which independent local AI reviewer CLIs are reachable; does not run a review.", inputSchema: z.object({}), annotations: readOnly }, async () => text(probeRoster()));
    return server;
};
export const serveMcp = async () => serveStdio(() => createMcpServer());
