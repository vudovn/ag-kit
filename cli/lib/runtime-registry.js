import fs from "node:fs";
import path from "node:path";
import { appendReceipt, initMemory, installRuntime } from "./v2-engine.js";

export const RUNTIME_TARGETS = ["antigravity", "claude", "codex", "gemini", "qwen", "kimi", "cursor", "windsurf", "copilot", "opencode", "openclaw", "aider"];
const LEGACY_INSTALLER_TARGETS = new Set(["antigravity", "claude", "codex", "gemini", "cursor", "windsurf", "copilot", "opencode"]);
const ensureDir=(dir)=>fs.mkdirSync(dir,{recursive:true});
const copyDir=(src,dst)=>{if(!fs.existsSync(src))return;ensureDir(path.dirname(dst));fs.rmSync(dst,{recursive:true,force:true});fs.cpSync(src,dst,{recursive:true});};
const managedBlock=(file,label,content)=>{ensureDir(path.dirname(file));const start=`<!-- AG-KIT:${label}:START -->`;const end=`<!-- AG-KIT:${label}:END -->`;const block=`${start}\n${content.trim()}\n${end}`;const previous=fs.existsSync(file)?fs.readFileSync(file,"utf8"):"";const escape=v=>v.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");const regex=new RegExp(`${escape(start)}[\\s\\S]*?${escape(end)}`,"m");fs.writeFileSync(file,regex.test(previous)?previous.replace(regex,block):`${previous.trim()}${previous.trim()?"\n\n":""}${block}\n`);};

export function installRuntimeTarget({sourceRoot,targetRoot=process.cwd(),runtime}){
  if(!RUNTIME_TARGETS.includes(runtime))throw new Error(`unsupported runtime: ${runtime}`);
  if(LEGACY_INSTALLER_TARGETS.has(runtime))return installRuntime({sourceRoot,targetRoot,runtime});
  const source=path.resolve(sourceRoot);const target=path.resolve(targetRoot);const shared=path.join(source,"shared");
  if(!fs.existsSync(shared))throw new Error(`shared source not found at ${shared}`);
  const core=fs.readFileSync(path.join(shared,"core","CORE.md"),"utf8");
  copyDir(path.join(shared,"core"),path.join(target,".ag-kit","core"));copyDir(path.join(shared,"flows"),path.join(target,".ag-kit","flows"));copyDir(path.join(source,"packs"),path.join(target,".ag-kit","packs"));
  ensureDir(path.join(target,".ag-kit"));fs.writeFileSync(path.join(target,".ag-kit","runtime.json"),`${JSON.stringify({schema:1,runtime,installedAt:new Date().toISOString()},null,2)}\n`);
  if(runtime==="qwen"){
    copyDir(path.join(shared,"skills"),path.join(target,".qwen","skills"));copyDir(path.join(shared,"agents"),path.join(target,".qwen","agents"));managedBlock(path.join(target,"QWEN.md"),"CORE",core);
  }else if(runtime==="kimi"){
    copyDir(path.join(shared,"skills"),path.join(target,".kimi-code","skills"));copyDir(path.join(shared,"agents"),path.join(target,".kimi-code","agents"));managedBlock(path.join(target,"AGENTS.md"),"CORE",core);
  }else if(runtime==="aider"){
    managedBlock(path.join(target,"CONVENTIONS.md"),"CORE",core);const config=path.join(target,".aider.conf.yml");if(!fs.existsSync(config))fs.writeFileSync(config,"read:\n  - CONVENTIONS.md\n");
  }else if(runtime==="openclaw"){
    managedBlock(path.join(target,"AGENTS.md"),"CORE",core);
  }
  initMemory(target);appendReceipt(target,"runtime",{action:"install",runtime});return{runtime,target,state:path.join(target,".ag-kit")};
}
