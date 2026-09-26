#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const fail = (msg) => { console.error(`AG Kit v2: ${msg}`); process.exitCode = 1; };
const dirs = (p) => fs.existsSync(p) ? fs.readdirSync(p, {withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name) : [];

const capabilities = JSON.parse(fs.readFileSync(path.join(root,'platform-capabilities.json'),'utf8'));
const skills = dirs(path.join(root,'shared','skills'));
const agents = fs.readdirSync(path.join(root,'shared','agents')).filter(x=>x.endsWith('.md'));
const flows = fs.readdirSync(path.join(root,'shared','flows')).filter(x=>x.endsWith('.json'));
const resident = skills.filter(name => fs.readFileSync(path.join(root,'shared','skills',name,'SKILL.md'),'utf8').includes('resident: true'));

if (resident.length !== capabilities.targets.residentSkills) fail(`expected ${capabilities.targets.residentSkills} resident skill, found ${resident.length}`);
if (skills.length > capabilities.targets.topLevelSkillsMax) fail(`skill surface ${skills.length} exceeds ${capabilities.targets.topLevelSkillsMax}`);
if (agents.length !== capabilities.targets.permanentAgents) fail(`expected ${capabilities.targets.permanentAgents} permanent agents, found ${agents.length}`);
if (flows.length !== capabilities.targets.workflowEngines) fail(`expected ${capabilities.targets.workflowEngines} workflow engine, found ${flows.length}`);
if (!resident.includes('ag-core')) fail('ag-core must be the resident skill');

for (const [name, platform] of Object.entries(capabilities.platforms)) {
  const adapterPath = path.join(root, platform.adapter);
  if (!fs.existsSync(adapterPath)) { fail(`${name}: missing adapter ${platform.adapter}`); continue; }
  const adapter = JSON.parse(fs.readFileSync(adapterPath,'utf8'));
  if (adapter.runtime !== name) fail(`${name}: adapter runtime mismatch`);
  for (const key of ['rules','skills','agents','hooks','mcp','plugins']) {
    if (Boolean(adapter.supports?.[key]) !== Boolean(platform[key])) fail(`${name}: ${key} capability drift`);
  }
}

const coreLines = fs.readFileSync(path.join(root,'shared','core','CORE.md'),'utf8').trim().split(/\r?\n/).length;
if (coreLines > 80) fail(`resident core is ${coreLines} lines; keep it <= 80`);

if (!process.exitCode) console.log(`AG Kit v2 OK: ${skills.length} skills (${resident.length} resident), ${agents.length} agents, ${flows.length} flow, ${Object.keys(capabilities.platforms).length} runtimes, ${coreLines}-line core.`);
