#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root = process.cwd();
const shared = path.join(root, 'shared');
const agentsRoot = path.join(root, '.agents');
const legacyPaths = ['agent', 'workflows', 'memory'];

const listFiles = (dir, base = dir) => {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, {withFileTypes: true}).sort((a,b)=>a.name.localeCompare(b.name))) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...listFiles(full, base));
    else out.push(path.relative(base, full).split(path.sep).join('/'));
  }
  return out;
};

const sameTree = (a, b) => {
  const left = listFiles(a); const right = listFiles(b);
  if (JSON.stringify(left) !== JSON.stringify(right)) return false;
  return left.every(file => fs.readFileSync(path.join(a,file)).equals(fs.readFileSync(path.join(b,file))));
};

const ruleText = () => `---\ntrigger: always_on\npriority: P0\nversion: 2.0.0\n---\n${fs.readFileSync(path.join(shared,'core','CORE.md'),'utf8')}`;

function check() {
  const errors = [];
  if (!sameTree(path.join(shared,'skills'), path.join(agentsRoot,'skills'))) errors.push('skills projection drift');
  if (!sameTree(path.join(shared,'agents'), path.join(agentsRoot,'agents'))) errors.push('agents projection drift');
  const rules = path.join(agentsRoot,'rules');
  const ruleFiles = fs.existsSync(rules) ? fs.readdirSync(rules).filter(x=>x.endsWith('.md')).sort() : [];
  if (JSON.stringify(ruleFiles) !== JSON.stringify(['ag-kit-v2.md'])) errors.push('rules projection must contain only ag-kit-v2.md');
  else if (fs.readFileSync(path.join(rules,'ag-kit-v2.md'),'utf8') !== ruleText()) errors.push('core rule projection drift');
  for (const item of legacyPaths) if (fs.existsSync(path.join(agentsRoot,item))) errors.push(`legacy .agents/${item} still exists`);
  if (errors.length) { for (const error of errors) console.error(`projection: ${error}`); process.exitCode=1; return; }
  console.log(`Antigravity projection OK: ${listFiles(path.join(agentsRoot,'skills')).filter(x=>x.endsWith('/SKILL.md')).length} skills, ${listFiles(path.join(agentsRoot,'agents')).filter(x=>x.endsWith('.md')).length} agents, 0 workflows.`);
}

function sync() {
  for (const item of ['skills','agents','rules',...legacyPaths]) fs.rmSync(path.join(agentsRoot,item), {recursive:true,force:true});
  fs.cpSync(path.join(shared,'skills'), path.join(agentsRoot,'skills'), {recursive:true});
  fs.cpSync(path.join(shared,'agents'), path.join(agentsRoot,'agents'), {recursive:true});
  fs.mkdirSync(path.join(agentsRoot,'rules'), {recursive:true});
  fs.writeFileSync(path.join(agentsRoot,'rules','ag-kit-v2.md'), ruleText());
  for (const item of ['manifest.json','manifest.lock.json','DEPENDENCY_GRAPH.md']) fs.rmSync(path.join(agentsRoot,item), {force:true});
  console.log('Synchronized Antigravity projection from shared/.');
  check();
}

if (process.argv.includes('--check')) check(); else sync();
