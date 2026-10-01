#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {pathToFileURL} from 'node:url';

function copyTree(source,destination){if(!fs.existsSync(source))return;fs.cpSync(source,destination,{recursive:true});}
function countSkillEntrypoints(dir){if(!fs.existsSync(dir))return 0;return fs.readdirSync(dir,{withFileTypes:true}).filter(entry=>entry.isDirectory()&&fs.existsSync(path.join(dir,entry.name,'SKILL.md'))).length;}
function countMarkdownFiles(dir){if(!fs.existsSync(dir))return 0;let count=0;for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name);if(entry.isDirectory())count+=countMarkdownFiles(full);else if(entry.name.toLowerCase().endsWith('.md'))count+=1;}return count;}
function sha256(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function inventory(output){const files=[];const visit=dir=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const full=path.join(dir,entry.name);if(entry.isDirectory())visit(full);else if(entry.name!=='PLUGIN_CONTENTS.json')files.push({path:path.relative(output,full).split(path.sep).join('/'),sha256:sha256(full)});}};visit(output);return files;}

export function buildPlugin(root,output){
  fs.rmSync(output,{recursive:true,force:true});fs.mkdirSync(output,{recursive:true});
  fs.copyFileSync(path.join(root,'.agents','plugins','ag-kit','plugin.json'),path.join(output,'plugin.json'));
  const skillSource=path.join(root,'.agents','skills'),agentSource=path.join(root,'.agents','agents'),ruleSource=path.join(root,'.agents','rules');
  copyTree(skillSource,path.join(output,'skills'));copyTree(agentSource,path.join(output,'agents'));copyTree(ruleSource,path.join(output,'rules'));
  const counts={skills:countSkillEntrypoints(skillSource),agents:countMarkdownFiles(agentSource),rules:countMarkdownFiles(ruleSource)};
  fs.copyFileSync(path.join(root,'.agents','hooks.json'),path.join(output,'hooks.json'));fs.copyFileSync(path.join(root,'.agents','mcp_config.json'),path.join(output,'mcp_config.json'));
  fs.mkdirSync(path.join(output,'hooks'),{recursive:true});fs.copyFileSync(path.join(root,'.agents','hooks','validate-tool-call.mjs'),path.join(output,'hooks','validate-tool-call.mjs'));
  const manifest={name:'ag-kit',runtime:'antigravity',schema:2,counts,files:inventory(output)};fs.writeFileSync(path.join(output,'PLUGIN_CONTENTS.json'),`${JSON.stringify(manifest,null,2)}\n`);return manifest;
}
export function buildRuntimeArtifact(root,outputRoot){const output=path.join(outputRoot,'antigravity','plugin');const manifest=buildPlugin(root,output);return {runtime:'antigravity',output,manifest};}
const direct=process.argv[1]&&pathToFileURL(fs.realpathSync(path.resolve(process.argv[1]))).href===import.meta.url;
if(direct){try{const root=process.cwd();const outputArg=process.argv.indexOf('--output-root');const out=path.resolve(root,outputArg>=0?process.argv[outputArg+1]:'dist/runtime-artifacts');const built=buildRuntimeArtifact(root,out);console.log(`Built runtime artifact [antigravity]: ${built.output}`);console.log(JSON.stringify(built.manifest.counts));}catch(error){console.error(`Runtime artifact build failed: ${error.message}`);process.exitCode=1;}}
