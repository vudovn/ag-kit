import { Command } from "commander";
import { downloadTemplate } from "giget";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { SUPPORTED_RUNTIMES, addMemory, initMemory, memoryStatus, recallMemory, initTeam, installRuntime, prepareAudit } from "./v2-engine.js";
import { serveMcp } from "./mcp-server.js";
import { wireRuntimeMcp } from "./runtime-mcp.js";
import { runCurrentPreflight } from "./preflight.js";

const REPO = "github:vudovn/ag-kit";
const withSource = async (branch, fn) => { const dir=fs.mkdtempSync(path.join(os.tmpdir(),"ag-kit-source-")); try { await downloadTemplate(branch?`${REPO}#${branch}`:REPO,{dir,force:true}); return await fn(dir); } finally { fs.rmSync(dir,{recursive:true,force:true}); } };

export const buildV2Program=()=>{
  const program=new Command().name("ag-kit").description("AG Kit v2 multi-runtime commands");
  const runtime=program.command("runtime").description("Inspect or install runtime adapters");
  runtime.command("list").action(()=>console.log(SUPPORTED_RUNTIMES.join("\n")));
  runtime.command("install <runtime>").option("-p, --path <dir>","Project directory",process.cwd()).option("-b, --branch <name>","AG Kit source branch").action(async(name,o)=>{const installed=await withSource(o.branch,sourceRoot=>installRuntime({sourceRoot,targetRoot:o.path,runtime:name}));const mcp=wireRuntimeMcp({root:o.path,runtime:name});console.log(JSON.stringify({...installed,mcp},null,2));});
  const memory=program.command("memory").description("Local-first project memory");
  memory.command("init").option("-p, --path <dir>","Project directory",process.cwd()).action(o=>console.log(initMemory(o.path)));
  memory.command("add <text...>").option("-p, --path <dir>","Project directory",process.cwd()).option("--kind <kind>","Entry kind","learning").option("--title <title>","Entry title","").action((body,o)=>console.log(JSON.stringify(addMemory({root:o.path,text:body.join(" "),kind:o.kind,title:o.title}),null,2)));
  memory.command("recall <query...>").option("-p, --path <dir>","Project directory",process.cwd()).option("--limit <n>","Maximum results","5").action((query,o)=>console.log(JSON.stringify(recallMemory({root:o.path,query:query.join(" "),limit:o.limit}),null,2)));
  memory.command("status").option("-p, --path <dir>","Project directory",process.cwd()).action(o=>console.log(JSON.stringify(memoryStatus(o.path),null,2)));
  program.command("team").description("Generate a project-specific specialist team").option("-p, --path <dir>","Project directory",process.cwd()).option("--archetype <type>","software|web|research|content|game|operations|auto","auto").option("--name <name>","Team name","default").option("--brief <text>","Project brief","").action(o=>console.log(JSON.stringify(initTeam({root:o.path,archetype:o.archetype,name:o.name,brief:o.brief}),null,2)));
  program.command("cross-audit [target]").description("Probe independent reviewer lineages and write an audit receipt").option("-p, --path <dir>","Project directory",process.cwd()).action((target=".",o)=>console.log(JSON.stringify(prepareAudit({root:o.path,target}),null,2)));
  program.command("preflight").description("Run AG Kit blocking release gates").option("-p, --path <dir>","AG Kit repository directory",process.cwd()).action(o=>{const r=runCurrentPreflight(o.path);for(const x of r.results)console.log(`${x.ok?"PASS":"FAIL"} ${x.name} ${x.durationMs}ms`);if(!r.passed)process.exitCode=1;});
  const mcp=program.command("mcp").description("AG Kit MCP bridge");mcp.command("serve").description("Serve the project-local AG Kit MCP over stdio").action(serveMcp);
  return program;
};
export const runV2Cli=async(argv=process.argv)=>buildV2Program().parseAsync(argv);
