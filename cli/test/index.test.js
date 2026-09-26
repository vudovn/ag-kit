import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildProgram } from "../bin/index.js";
import { buildV2Program } from "../lib/v2-cli.js";
import { addMemory, recallMemory, initTeam } from "../lib/v2-engine.js";
import { createMcpServer } from "../lib/mcp-server.js";
import { wireRuntimeMcp } from "../lib/runtime-mcp.js";

test("legacy CLI keeps safe lifecycle commands",()=>{const p=buildProgram();const commands=new Map(p.commands.map(c=>[c.name(),c]));assert.deepEqual([...commands.keys()],["init","update","rollback","status"]);assert.ok(commands.get("update").options.some(o=>o.long==="--strategy"));});
test("v2 CLI exposes operating-layer commands",()=>assert.deepEqual(buildV2Program().commands.map(c=>c.name()),["runtime","memory","team","flow","cross-audit","observe","dashboard","personalize","design","preflight","mcp"]));
test("memory and team engines are project-local",()=>{const root=fs.mkdtempSync(path.join(os.tmpdir(),"ag-kit-v2-cli-"));try{fs.writeFileSync(path.join(root,"package.json"),"{}");addMemory({root,text:"Use transactions for billing",kind:"decision"});assert.equal(recallMemory({root,query:"billing"}).length,1);assert.equal(initTeam({root,archetype:"auto"}).archetype,"software");}finally{fs.rmSync(root,{recursive:true,force:true});}});
test("MCP server constructs without transport",()=>assert.ok(createMcpServer()));
test("runtime MCP wiring uses project-scoped formats",()=>{const root=fs.mkdtempSync(path.join(os.tmpdir(),"ag-kit-mcp-"));try{const claude=wireRuntimeMcp({root,runtime:"claude"});assert.equal(claude.file,".mcp.json");assert.equal(JSON.parse(fs.readFileSync(path.join(root,".mcp.json"),"utf8")).mcpServers["ag-kit"].command,"ag-kit");const gemini=wireRuntimeMcp({root,runtime:"gemini"});assert.equal(gemini.file,".gemini/settings.json");}finally{fs.rmSync(root,{recursive:true,force:true});}});
test("CLI runs through npm bin symlink",async(t)=>{const {execFile}=await import("node:child_process");const {promisify}=await import("node:util");const dir=fs.mkdtempSync(path.join(os.tmpdir(),"ag-kit-symlink-"));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));fs.mkdirSync(path.join(dir,".bin"));const link=path.join(dir,".bin","ag-kit");fs.symlinkSync(path.resolve("bin/ag-kit.js"),link);const {stdout}=await promisify(execFile)(process.execPath,[link,"--version"]);assert.match(stdout.trim(),/^\d{4}\.\d+\.\d+$/);});
