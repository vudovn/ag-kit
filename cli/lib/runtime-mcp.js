import fs from "node:fs";
import path from "node:path";

const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
const readJson = (file) => {
    try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return {}; }
};
const writeJson = (file, data) => {
    ensureDir(path.dirname(file));
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
};

const stdio = { command: "ag-kit", args: ["mcp", "serve"] };

export function wireRuntimeMcp({ root = process.cwd(), runtime }) {
    const target = path.resolve(root);
    if (runtime === "antigravity") {
        const file = path.join(target, ".agents", "mcp_config.json");
        const data = readJson(file);
        data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": stdio };
        writeJson(file, data);
        return { wired: true, file: path.relative(target, file) };
    }
    if (runtime === "claude") {
        const file = path.join(target, ".mcp.json");
        const data = readJson(file);
        data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": { ...stdio, env: {} } };
        writeJson(file, data);
        return { wired: true, file: path.relative(target, file) };
    }
    if (runtime === "gemini") {
        const file = path.join(target, ".gemini", "settings.json");
        const data = readJson(file);
        data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": stdio };
        writeJson(file, data);
        return { wired: true, file: path.relative(target, file) };
    }
    if (runtime === "cursor") {
        const file = path.join(target, ".cursor", "mcp.json");
        const data = readJson(file);
        data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": stdio };
        writeJson(file, data);
        return { wired: true, file: path.relative(target, file) };
    }
    if (runtime === "copilot") {
        const file = path.join(target, ".mcp.json");
        const data = readJson(file);
        data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": { type: "local", ...stdio, env: {}, tools: ["*"] } };
        writeJson(file, data);
        return { wired: true, file: path.relative(target, file) };
    }
    if (runtime === "codex") {
        const pluginDir = path.join(target, ".codex-plugin");
        const pluginSkills = path.join(pluginDir, "skills");
        ensureDir(pluginDir);
        fs.rmSync(pluginSkills, { recursive: true, force: true });
        const projectedSkills = path.join(target, ".agents", "skills");
        if (fs.existsSync(projectedSkills)) fs.cpSync(projectedSkills, pluginSkills, { recursive: true });
        const mcpFile = path.join(pluginDir, ".mcp.json");
        writeJson(mcpFile, { mcpServers: { "ag-kit": stdio } });
        const pluginFile = path.join(pluginDir, "plugin.json");
        writeJson(pluginFile, {
            name: "ag-kit",
            version: "2.0.0",
            description: "AG Kit shared skills and project-local MCP bridge",
            skills: "./skills/",
            mcpServers: "./.mcp.json"
        });
        return {
            wired: true,
            file: path.relative(target, mcpFile),
            plugin: path.relative(target, pluginFile),
            skills: path.relative(target, pluginSkills)
        };
    }
    return {
        wired: false,
        reason: "runtime has no verified project-scoped MCP projection; configure its user-level MCP to run `ag-kit mcp serve`"
    };
}
