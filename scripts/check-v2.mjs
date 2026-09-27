#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const fail = (msg) => { console.error(`AG Kit v2: ${msg}`); process.exitCode = 1; };
const dirs = (p) => fs.existsSync(p) ? fs.readdirSync(p, {withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name) : [];
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));

const capabilities = readJson('platform-capabilities.json');
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

const knowledgeMapPath = path.join(root, 'packs', 'legacy-knowledge-map.json');
const packRegistryPath = path.join(root, 'packs', 'registry.json');
let legacyKnowledgeCount = 0;
let packCount = 0;

if (!fs.existsSync(knowledgeMapPath)) fail('missing packs/legacy-knowledge-map.json');
if (!fs.existsSync(packRegistryPath)) fail('missing packs/registry.json');

if (fs.existsSync(knowledgeMapPath) && fs.existsSync(packRegistryPath)) {
  const knowledge = JSON.parse(fs.readFileSync(knowledgeMapPath, 'utf8'));
  const registry = JSON.parse(fs.readFileSync(packRegistryPath, 'utf8'));
  const entries = Array.isArray(knowledge.entries) ? knowledge.entries : [];
  const expectedLegacy = Number(knowledge.legacySkillCount || 0);
  const names = new Set();
  legacyKnowledgeCount = entries.length;
  packCount = Object.keys(registry.packs || {}).length;

  if (knowledge.schema !== 1) fail('legacy knowledge map schema must be 1');
  if (expectedLegacy !== 47) fail(`legacy knowledge baseline must account for 47 skills, found ${expectedLegacy}`);
  if (entries.length !== expectedLegacy) fail(`legacy knowledge map contains ${entries.length}/${expectedLegacy} entries`);
  if (registry.schema !== 1 || registry.policy !== 'cold-load-only') fail('pack registry must use schema 1 and cold-load-only policy');
  if (registry.installedLocation !== '.ag-kit/packs') fail('pack registry installedLocation must be .ag-kit/packs');

  for (const entry of entries) {
    if (!entry.legacySkill || names.has(entry.legacySkill)) fail(`duplicate or missing legacy skill entry: ${entry.legacySkill || '(empty)'}`);
    names.add(entry.legacySkill);
    if (!['skill-reference','pack-reference'].includes(entry.mode)) fail(`${entry.legacySkill}: invalid migration mode ${entry.mode}`);
    if (!entry.reference || entry.reference.endsWith('/SKILL.md')) fail(`${entry.legacySkill}: deep reference must not be auto-discoverable as SKILL.md`);

    const referencePath = path.join(root, entry.reference || '');
    if (!fs.existsSync(referencePath)) { fail(`${entry.legacySkill}: missing reference ${entry.reference}`); continue; }
    const reference = fs.readFileSync(referencePath, 'utf8');
    if (!reference.includes('Cold reference only.')) fail(`${entry.legacySkill}: reference is missing non-normative cold-load warning`);
    if (Number(entry.sourceBytes || 0) <= 0) fail(`${entry.legacySkill}: sourceBytes must be recorded`);

    if (entry.mode === 'skill-reference') {
      if (!skills.includes(entry.target)) fail(`${entry.legacySkill}: target skill ${entry.target} does not exist`);
      const index = path.join(root, 'shared', 'skills', entry.target, 'references', 'INDEX.md');
      if (!fs.existsSync(index)) fail(`${entry.legacySkill}: missing ${entry.target} reference index`);
      const skillText = fs.readFileSync(path.join(root, 'shared', 'skills', entry.target, 'SKILL.md'), 'utf8');
      if (!skillText.includes('Deep references: `references/INDEX.md`')) fail(`${entry.target}: SKILL.md must advertise lazy deep references`);
    } else {
      const pack = registry.packs?.[entry.target];
      if (!pack) { fail(`${entry.legacySkill}: target pack ${entry.target} is not registered`); continue; }
      if (!Array.isArray(pack.references) || !pack.references.includes(entry.reference)) fail(`${entry.legacySkill}: ${entry.reference} missing from pack registry`);
    }
  }

  for (const [packId, pack] of Object.entries(registry.packs || {})) {
    if (!Array.isArray(pack.triggers) || pack.triggers.length === 0) fail(`${packId}: pack must declare triggers`);
    const index = path.join(root, pack.index || '');
    if (!fs.existsSync(index)) { fail(`${packId}: missing PACK.md index ${pack.index}`); continue; }
    const lines = fs.readFileSync(index, 'utf8').trim().split(/\r?\n/).length;
    if (lines > 120) fail(`${packId}: PACK.md index is ${lines} lines; keep pack index <= 120 and move depth to references`);
    for (const reference of pack.references || []) if (!fs.existsSync(path.join(root, reference))) fail(`${packId}: missing registered reference ${reference}`);
  }
}

if (!process.exitCode) console.log(`AG Kit v2 OK: ${skills.length} skills (${resident.length} resident), ${agents.length} agents, ${flows.length} flow, ${Object.keys(capabilities.platforms).length} runtimes, ${coreLines}-line core, ${packCount} cold packs, ${legacyKnowledgeCount}/47 legacy knowledge references preserved.`);
