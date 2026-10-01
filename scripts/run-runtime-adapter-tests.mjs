#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const root=process.cwd();
const runtimeRoot=path.join(root,'runtimes');
const tests=[];
for(const entry of fs.readdirSync(runtimeRoot,{withFileTypes:true}).filter(x=>x.isDirectory()).sort((a,b)=>a.name.localeCompare(b.name))){
  const dir=path.join(runtimeRoot,entry.name);
  for(const file of fs.readdirSync(dir).filter(x=>x.endsWith('.test.mjs')).sort())tests.push(path.join(dir,file));
}
if(!tests.length){console.error('No runtime adapter tests found.');process.exit(1);}
const result=spawnSync(process.execPath,['--test',...tests],{cwd:root,stdio:'inherit',shell:false});
process.exitCode=result.status??1;
