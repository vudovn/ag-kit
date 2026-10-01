#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const root=process.cwd();
const out=path.resolve(root,process.argv[2]||'dist/runtime-artifacts');
fs.rmSync(out,{recursive:true,force:true});
fs.mkdirSync(out,{recursive:true});

const artifacts=[];
for(const entry of fs.readdirSync(path.join(root,'runtimes'),{withFileTypes:true}).filter(x=>x.isDirectory()).sort((a,b)=>a.name.localeCompare(b.name))){
  const buildPath=path.join(root,'runtimes',entry.name,'build.mjs');
  if(!fs.existsSync(buildPath))continue;
  const mod=await import(pathToFileURL(buildPath).href);
  if(typeof mod.buildRuntimeArtifact!=='function')throw new Error(`${entry.name}: build.mjs must export buildRuntimeArtifact(root, outputRoot)`);
  const built=await mod.buildRuntimeArtifact(root,out);
  if(!built||built.runtime!==entry.name)throw new Error(`${entry.name}: artifact builder returned an invalid runtime identity`);
  if(!built.output||!fs.existsSync(built.output))throw new Error(`${entry.name}: artifact builder did not create its declared output`);
  artifacts.push({runtime:entry.name,output:path.relative(out,built.output).split(path.sep).join('/'),manifest:built.manifest?.name||null});
}

if(!artifacts.length)throw new Error('No runtime adapter exposes a native artifact builder.');
const index={schema:1,builtAt:new Date().toISOString(),artifacts};
fs.writeFileSync(path.join(out,'ARTIFACTS.json'),`${JSON.stringify(index,null,2)}\n`);
console.log(`Built and verified native artifacts for ${artifacts.length} runtime adapter(s) in ${path.relative(root,out)}.`);
for(const artifact of artifacts)console.log(`- ${artifact.runtime}: ${artifact.output}`);
