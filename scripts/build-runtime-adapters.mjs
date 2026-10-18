#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const out = path.resolve(root, process.argv[2] || 'dist/runtimes');
const capabilities = JSON.parse(fs.readFileSync(path.join(root,'platform-capabilities.json'),'utf8'));
const core = fs.readFileSync(path.join(root,'shared/core/CORE.md'),'utf8');
const skills = fs.readdirSync(path.join(root,'shared/skills'), {withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name).sort();
const agents = fs.readdirSync(path.join(root,'shared/agents')).filter(x=>x.endsWith('.md')).sort();

fs.rmSync(out,{recursive:true,force:true});
fs.mkdirSync(out,{recursive:true});
for (const [name, platform] of Object.entries(capabilities.platforms)) {
  const target = path.join(out,name);
  fs.mkdirSync(target,{recursive:true});
  const adapter = JSON.parse(fs.readFileSync(path.join(root,platform.adapter),'utf8'));
  fs.writeFileSync(path.join(target,'adapter.json'), JSON.stringify(adapter,null,2)+'\n');
  fs.writeFileSync(path.join(target,'AGENTS.md'), `# AG Kit runtime projection: ${name}\n\n${core}\n`);
  fs.writeFileSync(path.join(target,'inventory.json'), JSON.stringify({runtime:name,tier:platform.tier,skills:platform.skills?skills:[],agents:platform.agents?agents:[],source:'shared'},null,2)+'\n');
}
console.log(`Built ${Object.keys(capabilities.platforms).length} runtime projections in ${path.relative(root,out)}`);
