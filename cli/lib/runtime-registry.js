import fs from "node:fs";
import path from "node:path";
import { appendReceipt, initMemory, installRuntime } from "./v2-engine.js";
import { resolveSafeProjectRoot } from "./project-state.js";

export const RUNTIME_TARGETS = ["antigravity", "claude", "codex", "gemini", "qwen", "kimi", "cline", "cursor", "windsurf", "copilot", "opencode", "openclaw", "aider", "wayland", "hermes", "pi"];
const LEGACY_INSTALLER_TARGETS = new Set(["antigravity", "claude", "codex", "gemini", "cursor", "windsurf", "copilot", "opencode"]);
const ensureDir=(dir)=>fs.mkdirSync(dir,{recursive:true});
const copyDir=(src,dst)=>{if(!fs.existsSync(src))return;ensureDir(path.dirname(dst));fs.rmSync(dst,{recursive:true,force:true});fs.cpSync(src,dst,{recursive:true});};
const managedBlock=(file,label,content)=>{ensureDir(path.dirname(file));const start=`<!-- AG-KIT:${label}:START -->`;const end=`<!-- AG-KIT:${label}:END -->`;const block=`${start}\n${content.trim()}\n${end}`;const previous=fs.existsSync(file)?fs.readFileSync(file,"utf8"):"";const escape=v=>v.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");const regex=new RegExp(`${escape(start)}[\\s\\S]*?${escape(end)}`,"m");fs.writeFileSync(file,regex.test(previous)?previous.replace(regex,block):`${previous.trim()}${previous.trim()?"\n\n":""}${block}\n`);};
const write=(file,content)=>{ensureDir(path.dirname(file));fs.writeFileSync(file,content);};

export function installRuntimeTarget({sourceRoot,targetRoot=process.cwd(),runtime}){
  if(!RUNTIME_TARGETS.includes(runtime))throw new Error(`unsupported runtime: ${runtime}`);
  const target=resolveSafeProjectRoot(targetRoot);
  if(LEGACY_INSTALLER_TARGETS.has(runtime))return installRuntime({sourceRoot,targetRoot:target,runtime});
  const source=path.resolve(sourceRoot);const shared=path.join(source,"shared");
  if(!fs.existsSync(shared))throw new Error(`shared source not found at ${shared}`);
  const core=fs.readFileSync(path.join(shared,"core","CORE.md"),"utf8");
  copyDir(path.join(shared,"core"),path.join(target,".ag-kit","core"));copyDir(path.join(shared,"flows"),path.join(target,".ag-kit","flows"));copyDir(path.join(source,"packs"),path.join(target,".ag-kit","packs"));
  ensureDir(path.join(target,".ag-kit"));fs.writeFileSync(path.join(target,".ag-kit","runtime.json"),`${JSON.stringify({schema:1,runtime,installedAt:new Date().toISOString()},null,2)}\n`);
  if(runtime==="qwen"){
    copyDir(path.join(shared,"skills"),path.join(target,".qwen","skills"));copyDir(path.join(shared,"agents"),path.join(target,".qwen","agents"));managedBlock(path.join(target,"QWEN.md"),"CORE",core);
  }else if(runtime==="kimi"){
    copyDir(path.join(shared,"skills"),path.join(target,".kimi-code","skills"));copyDir(path.join(shared,"agents"),path.join(target,".kimi-code","agents"));managedBlock(path.join(target,"AGENTS.md"),"CORE",core);
  }else if(runtime==="cline"){
    copyDir(path.join(shared,"skills"),path.join(target,".cline","skills"));managedBlock(path.join(target,".cline","rules","ag-kit.md"),"CORE",core);
  }else if(runtime==="aider"){
    managedBlock(path.join(target,"CONVENTIONS.md"),"CORE",core);const config=path.join(target,".aider.conf.yml");if(!fs.existsSync(config))fs.writeFileSync(config,"read:\n  - CONVENTIONS.md\n");
  }else if(runtime==="openclaw"){
    managedBlock(path.join(target,"AGENTS.md"),"CORE",core);
  }else if(runtime==="pi"){
    managedBlock(path.join(target,"AGENTS.md"),"CORE",core);
  }else if(runtime==="wayland"){
    write(path.join(target,".ag-kit","integrations","wayland","README.md"),`# AG Kit → Wayland\n\nWayland Core is MCP-native. AG Kit does not mutate the user-global Wayland/plugin registry automatically. Add a stdio MCP server named \`ag-kit\` whose command is \`ag-kit\` and args are \`[\"mcp\",\"serve\"]\`, then verify it with the Wayland runtime doctor.\n`);
  }else if(runtime==="hermes"){
    write(path.join(target,".ag-kit","integrations","hermes","mcp.yaml"),`mcp_servers:\n  ag-kit:\n    command: \"ag-kit\"\n    args: [\"mcp\", \"serve\"]\n    enabled: true\n`);
    write(path.join(target,".ag-kit","integrations","hermes","README.md"),`# AG Kit → Hermes\n\nHermes currently reads MCP configuration from its user-global config. Merge the adjacent \`mcp.yaml\` snippet into \`~/.hermes/config.yaml\` explicitly; AG Kit does not edit that file automatically.\n`);
  }
  initMemory(target);appendReceipt(target,"runtime",{action:"install",runtime});return{runtime,target,state:path.join(target,".ag-kit")};
}
