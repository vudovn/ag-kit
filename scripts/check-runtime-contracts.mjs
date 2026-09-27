#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const root=process.cwd();
const capabilities=JSON.parse(fs.readFileSync(path.join(root,'platform-capabilities.json'),'utf8'));
const errors=[];
let runtimeChecks=0;
const read=(relative)=>fs.readFileSync(path.join(root,relative),'utf8');
const exists=(relative)=>fs.existsSync(path.join(root,relative));
const runtimeNames=Object.keys(capabilities.platforms||{});
const {PROMPT_HOOK_RUNTIMES}=await import(pathToFileURL(path.join(root,'cli','lib','prompt-hook.js')).href);

if(capabilities.sourceOfTruth!=='shared')errors.push(`sourceOfTruth must be shared, received ${JSON.stringify(capabilities.sourceOfTruth)}`);
if('primaryRuntime' in capabilities||'primary_runtime' in capabilities)errors.push('platform capability contract must not declare a primary runtime');
if(runtimeNames.length<2)errors.push('runtime matrix must contain multiple runtimes');

for(const [name,platform] of Object.entries(capabilities.platforms||{})){
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

for(const name of PROMPT_HOOK_RUNTIMES||[]){
  const platform=capabilities.platforms?.[name];
  if(!platform){errors.push(`prompt-hook runtime ${name} is missing from platform capabilities`);continue;}
  if(!platform.hooks)errors.push(`${name}: prompt-hook runtime must declare hooks=true in platform capabilities`);
  if(!platform.adapter||!exists(platform.adapter))continue;
  const adapter=JSON.parse(read(platform.adapter));
  if(!adapter.supports?.hooks)errors.push(`${name}: prompt-hook runtime adapter must declare supports.hooks=true`);
  if(!adapter.hooks)errors.push(`${name}: prompt-hook runtime adapter must declare its hook/config surface`);
}

const rootPackage=JSON.parse(read('package.json'));
const requiredGenericScripts=['check:runtimes','test:runtimes','build:runtimes','build:runtime-artifacts'];
for(const script of requiredGenericScripts)if(!rootPackage.scripts?.[script])errors.push(`missing generic runtime script ${script}`);
for(const script of Object.keys(rootPackage.scripts||{})){
  const lowered=script.toLowerCase();
  const runtime=runtimeNames.find((name)=>lowered.includes(name.toLowerCase()));
  if(runtime)errors.push(`root package script ${script} is runtime-specific (${runtime}); route adapter work through the generic runtime runners`);
}

const repoInstructions=read('AGENTS.md');
if(/^primary_runtime\s*:/im.test(repoInstructions))errors.push('AGENTS.md must not declare primary_runtime');
if(/(?:treats?|uses?|makes?)\s+[^\n.]*\b(?:antigravity|claude|codex|gemini|qwen|kimi|cline|cursor|windsurf|copilot|opencode|openclaw|aider|wayland|hermes|pi)\b[^\n.]*\bas (?:its |the )?primary runtime\b/i.test(repoInstructions))errors.push('AGENTS.md must not make a runtime primary');

const forbiddenLegacyFiles=[
  '.agents/antigravity.json',
  '.agents/hooks/antigravity-contract.schema.json',
  '.agents/hooks/antigravity-doctor.mjs',
  '.agents/hooks/antigravity-hooks.schema.json',
  '.agents/hooks/build-plugin.mjs',
  '.agents/hooks/tests/antigravity.test.mjs',
  '.github/workflows/antigravity.yml',
  'scripts/check-platform-drift.mjs',
];
for(const relative of forbiddenLegacyFiles)if(exists(relative))errors.push(`legacy runtime-centric file must stay removed: ${relative}`);

const workflowDir=path.join(root,'.github','workflows');
if(fs.existsSync(workflowDir)){
  for(const filename of fs.readdirSync(workflowDir)){
    const lowered=filename.toLowerCase();
    const runtime=runtimeNames.find((name)=>lowered===`${name}.yml`||lowered===`${name}.yaml`||lowered.startsWith(`${name}-`)||lowered.startsWith(`${name}_`));
    if(runtime)errors.push(`workflow ${filename} is runtime-specific (${runtime}); use a capability-tiered runtime workflow instead`);
  }
}

const publicDocs=[
  'README.md','README-VI.md','MIGRATION.md','PRODUCTION_CHECKLIST.md','SECURITY.md','AGENT_FLOW.md','CLAUDE.md',
  '.github/RELEASE_SETUP.md','docs/ARCHITECTURE_V2.md','docs/RUNTIMES.md','docs/PARITY_IJFW.md','cli/README.md','web/README.md'
];
const npmRun=/npm run ([\w:@.-]+)/g;
for(const relative of publicDocs){
  if(!exists(relative))continue;
  const body=read(relative);
  for(const match of body.matchAll(npmRun)){
    const script=match[1];
    const lowered=script.toLowerCase();
    const runtime=runtimeNames.find((name)=>lowered.includes(name.toLowerCase()));
    if(runtime)errors.push(`${relative}: root command npm run ${script} is runtime-specific (${runtime}); document the generic runtime runner instead`);
  }
  if(body.includes('Antigravity Compatibility'))errors.push(`${relative}: obsolete Antigravity Compatibility gate name; use Runtime Compatibility / Runtime contracts`);
}

if(errors.length){for(const error of errors)console.error(`runtime contract: ${error}`);process.exitCode=1;}
else console.log(`Runtime contracts OK: ${runtimeNames.length} adapters, ${runtimeChecks} adapter-specific native check(s), runtime-neutral repository contract enforced.`);
