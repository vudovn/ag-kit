import fs from "node:fs";
import path from "node:path";

const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
const readJson = (file) => { try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return {}; } };
const writeJson = (file, data) => { ensureDir(path.dirname(file)); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`); };
const portableRelative = (root, target) => path.relative(root, target).split(path.sep).join("/");
const stdio = { command: "ag-kit", args: ["mcp", "serve"] };
const mergeMcp = (file, entry = stdio) => {
  const data = readJson(file);
  data.mcpServers = { ...(data.mcpServers || {}), "ag-kit": entry };
  writeJson(file, data);
  return { wired: true, file };
};
const mergeOpenCodeMcp = (file) => {
  const data = readJson(file);
  data.$schema ||= "https://opencode.ai/config.json";
  data.mcp = { ...(data.mcp || {}), "ag-kit": { type: "local", command: ["ag-kit", "mcp", "serve"], enabled: true } };
  writeJson(file, data);
  return { wired: true, file };
};
const mergePromptHook = ({ root, file, runtime, event }) => {
  const data = readJson(file);
  data.hooks = { ...(data.hooks || {}) };
  const groups = Array.isArray(data.hooks[event]) ? data.hooks[event] : [];
  const command = `ag-kit prompt-hook ${runtime}`;
  const exists = groups.some((group) => Array.isArray(group?.hooks) && group.hooks.some((handler) => handler?.command === command));
  if (!exists) groups.push({ hooks: [{ type: "command", command, timeout: 5 }] });
  data.hooks[event] = groups;
  writeJson(file, data);
  return { wired: true, event, file: portableRelative(root, file), privacy: "no-raw-prompt-persistence" };
};

export function wireRuntimeMcp({ root = process.cwd(), runtime }) {
  const target = path.resolve(root);
  let result;
  if (runtime === "antigravity") result = mergeMcp(path.join(target, ".agents", "mcp_config.json"));
  else if (runtime === "claude") {
    result = mergeMcp(path.join(target, ".mcp.json"), { ...stdio, env: {} });
    const promptQuality = mergePromptHook({ root: target, file: path.join(target, ".claude", "settings.json"), runtime, event: "UserPromptSubmit" });
    return { ...result, file: portableRelative(target, result.file), promptQuality };
  }
  else if (runtime === "gemini") {
    result = mergeMcp(path.join(target, ".gemini", "settings.json"));
    const promptQuality = mergePromptHook({ root: target, file: path.join(target, ".gemini", "settings.json"), runtime, event: "BeforeAgent" });
    return { ...result, file: portableRelative(target, result.file), promptQuality };
  }
  else if (runtime === "qwen") {
    result = mergeMcp(path.join(target, ".qwen", "settings.json"));
    const promptQuality = mergePromptHook({ root: target, file: path.join(target, ".qwen", "settings.json"), runtime, event: "UserPromptSubmit" });
    return { ...result, file: portableRelative(target, result.file), promptQuality };
  }
  else if (runtime === "kimi") result = mergeMcp(path.join(target, ".kimi-code", "mcp.json"));
  else if (runtime === "cline") result = mergeMcp(path.join(target, ".cline", "mcp.json"));
  else if (runtime === "cursor") result = mergeMcp(path.join(target, ".cursor", "mcp.json"));
  else if (runtime === "copilot") result = mergeMcp(path.join(target, ".mcp.json"), { type: "local", ...stdio, env: {}, tools: ["*"] });
  else if (runtime === "opencode") result = mergeOpenCodeMcp(path.join(target, "opencode.json"));
  else if (runtime === "codex") {
    const pluginDir = path.join(target, ".codex-plugin");
    const pluginSkills = path.join(pluginDir, "skills");
    ensureDir(pluginDir);
    fs.rmSync(pluginSkills, { recursive: true, force: true });
    const projected = path.join(target, ".agents", "skills");
    if (fs.existsSync(projected)) fs.cpSync(projected, pluginSkills, { recursive: true });
    const mcpFile = path.join(pluginDir, ".mcp.json");
    writeJson(mcpFile, { mcpServers: { "ag-kit": stdio } });
    const hooksFile = path.join(pluginDir, "hooks", "hooks.json");
    writeJson(hooksFile, { hooks: { PostToolUse: [{ hooks: [{ type: "command", command: "ag-kit hook-ingest codex", async: true, timeout: 5 }] }] } });
    const pluginFile = path.join(pluginDir, "plugin.json");
    writeJson(pluginFile, { name: "ag-kit", version: "2.0.0", description: "AG Kit shared skills, project-local MCP bridge, and privacy-minimal lifecycle observability", skills: "./skills/", mcpServers: "./.mcp.json", hooks: "./hooks/hooks.json" });
    return { wired: true, file: portableRelative(target, mcpFile), plugin: portableRelative(target, pluginFile), skills: portableRelative(target, pluginSkills), observability: { wired: true, event: "PostToolUse", file: portableRelative(target, hooksFile), privacy: "metadata-only" } };
  } else if (runtime === "wayland") return { wired: false, staged: ".ag-kit/integrations/wayland/README.md", reason: "Wayland MCP is supported, but AG Kit will not mutate its user-global/plugin registry automatically." };
  else if (runtime === "hermes") return { wired: false, staged: ".ag-kit/integrations/hermes/mcp.yaml", reason: "Hermes MCP config is user-global; merge the staged snippet explicitly." };
  else if (runtime === "openclaw") return { wired: false, reason: "Run `openclaw mcp add`/`openclaw mcp set` for the ag-kit stdio server; OpenClaw owns its MCP registry." };
  else return { wired: false, reason: "runtime has no verified project-scoped MCP projection; configure its MCP client to run `ag-kit mcp serve` if supported" };
  return { ...result, file: portableRelative(target, result.file) };
}
