#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const options={root:process.cwd(),output:null};
  for(let i=0;i<argv.length;i+=1){if(argv[i]==='--root')options.root=path.resolve(argv[++i]);else if(argv[i]==='--output')options.output=path.resolve(argv[++i]);else throw new Error(`Unknown argument: ${argv[i]}`);}
  options.output??=path.join(options.root,'dist','antigravity-plugin'); return options;
}
function copyTree(source,destination){if(!fs.existsSync(source))return 0;fs.cpSync(source,destination,{recursive:true});return countFiles(source);}
function countFiles(dir){let count=0;for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name);if(entry.isDirectory())count+=countFiles(full);else count+=1;}return count;}
function sha256(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function inventory(output){const files=[];const visit=dir=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const full=path.join(dir,entry.name);if(entry.isDirectory())visit(full);else if(entry.name!=='PLUGIN_CONTENTS.json')files.push({path:path.relative(output,full).split(path.sep).join('/'),sha256:sha256(full)});}};visit(output);return files;}

export function buildPlugin(root,output){
  fs.rmSync(output,{recursive:true,force:true});fs.mkdirSync(output,{recursive:true});
  fs.copyFileSync(path.join(root,'.agents','plugins','ag-kit','plugin.json'),path.join(output,'plugin.json'));
  const counts={
    skills:copyTree(path.join(root,'.agents','skills'),path.join(output,'skills')),
    agents:copyTree(path.join(root,'.agents','agents'),path.join(output,'agents')),
    rules:copyTree(path.join(root,'.agents','rules'),path.join(output,'rules'))
  };
  fs.copyFileSync(path.join(root,'.agents','hooks.json'),path.join(output,'hooks.json'));
  fs.copyFileSync(path.join(root,'.agents','mcp_config.json'),path.join(output,'mcp_config.json'));
  fs.mkdirSync(path.join(output,'hooks'),{recursive:true});
  fs.copyFileSync(path.join(root,'.agents','hooks','validate-tool-call.mjs'),path.join(output,'hooks','validate-tool-call.mjs'));
  const manifest={name:'ag-kit',runtime:'antigravity',schema:2,counts,files:inventory(output)};
  fs.writeFileSync(path.join(output,'PLUGIN_CONTENTS.json'),`${JSON.stringify(manifest,null,2)}\n`);
  return manifest;
}
if(import.meta.url===`file://${process.argv[1]}`){try{const o=parseArgs(process.argv.slice(2));const m=buildPlugin(o.root,o.output);console.log(`Built Antigravity plugin: ${o.output}`);console.log(JSON.stringify(m.counts));}catch(error){console.error(`Plugin build failed: ${error.message}`);process.exitCode=1;}}
