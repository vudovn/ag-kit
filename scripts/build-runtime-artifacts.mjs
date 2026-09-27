#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const root=process.cwd();
const out=path.resolve(root,process.argv[2]||'dist/runtime-artifacts');
fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(out,{recursive:true});
let built=0;
for(const entry of fs.readdirSync(path.join(root,'runtimes'),{withFileTypes:true}).filter(x=>x.isDirectory()).sort((a,b)=>a.name.localeCompare(b.name))){
  const buildPath=path.join(root,'runtimes',entry.name,'build.mjs');
  if(!fs.existsSync(buildPath))continue;
  const mod=await import(pathToFileURL(buildPath).href);
  if(typeof mod.buildRuntimeArtifact!=='function')throw new Error(`${entry.name}: build.mjs must export buildRuntimeArtifact(root, outputRoot)`);
  await mod.buildRuntimeArtifact(root,out);built+=1;
}
console.log(`Built native artifacts for ${built} runtime adapter(s) in ${path.relative(root,out)}.`);
