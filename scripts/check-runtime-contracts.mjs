#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const root=process.cwd();
const capabilities=JSON.parse(fs.readFileSync(path.join(root,'platform-capabilities.json'),'utf8'));
const errors=[];
let runtimeChecks=0;

for(const [name,platform] of Object.entries(capabilities.platforms)){
  const adapterPath=path.join(root,platform.adapter);
  if(!fs.existsSync(adapterPath)){errors.push(`${name}: missing adapter ${platform.adapter}`);continue;}
  const adapter=JSON.parse(fs.readFileSync(adapterPath,'utf8'));
  if(adapter.runtime!==name)errors.push(`${name}: adapter runtime mismatch`);
  if(adapter.tier!==platform.tier)errors.push(`${name}: adapter tier mismatch`);
  for(const key of ['rules','skills','agents','hooks','mcp','plugins'])if(Boolean(adapter.supports?.[key])!==Boolean(platform[key]))errors.push(`${name}: ${key} capability drift`);
  const checkPath=path.join(path.dirname(adapterPath),'check.mjs');
  if(fs.existsSync(checkPath)){
    const mod=await import(pathToFileURL(checkPath).href);
    if(typeof mod.diagnose!=='function'){errors.push(`${name}: check.mjs must export diagnose(root)`);continue;}
    const report=await mod.diagnose(root);runtimeChecks+=1;
    if(!report?.passed)for(const finding of report?.findings||[])if(finding.severity==='error')errors.push(`${name}: ${finding.code} - ${finding.message}`);
  }
}

if(Object.keys(capabilities.platforms).length<2)errors.push('runtime matrix must contain multiple runtimes');
if(errors.length){for(const error of errors)console.error(`runtime contract: ${error}`);process.exitCode=1;}
else console.log(`Runtime contracts OK: ${Object.keys(capabilities.platforms).length} adapters, ${runtimeChecks} adapter-specific native check(s).`);
