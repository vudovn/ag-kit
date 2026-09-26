#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const readJson=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const add=(r,severity,phase,code,file,message)=>r.findings.push({severity,phase,code,file,message});
const countSkills=dir=>fs.existsSync(dir)?fs.readdirSync(dir,{withFileTypes:true}).filter(e=>e.isDirectory()&&fs.existsSync(path.join(dir,e.name,'SKILL.md'))).length:0;
const countMd=dir=>fs.existsSync(dir)?fs.readdirSync(dir).filter(x=>x.endsWith('.md')).length:0;

export function diagnose(root){
  const report={runtime:'antigravity',root,passed:true,counts:{},phases:{},findings:[]};
  const base=path.join(root,'.agents');
  let contract=null;
  try{contract=readJson(path.join(base,'antigravity.json'));if(contract.runtime!=='antigravity')add(report,'error','discovery','contract.runtime','.agents/antigravity.json','runtime must be antigravity');}catch(e){add(report,'error','discovery','contract.invalid','.agents/antigravity.json',e.message);}
  report.counts.skills=countSkills(path.join(base,'skills'));report.counts.agents=countMd(path.join(base,'agents'));report.counts.rules=countMd(path.join(base,'rules'));
  if(report.counts.skills!==18)add(report,'error','discovery','skills.count','.agents/skills',`Expected lean projection of 18 skills, found ${report.counts.skills}`);
  if(report.counts.agents!==4)add(report,'error','discovery','agents.count','.agents/agents',`Expected 4 permanent agents, found ${report.counts.agents}`);
  for(const legacy of ['agent','workflows','memory'])if(fs.existsSync(path.join(base,legacy)))add(report,'error','discovery','legacy.present',`.agents/${legacy}`,'Legacy runtime surface must not exist in v2');
  const rules=fs.existsSync(path.join(base,'rules'))?fs.readdirSync(path.join(base,'rules')).filter(x=>x.endsWith('.md')):[];
  if(rules.length!==1||rules[0]!=='ag-kit-v2.md')add(report,'error','discovery','rules.projection','.agents/rules','Expected only ag-kit-v2.md projected from shared core');
  try{const mcp=readJson(path.join(base,'mcp_config.json'));report.counts.mcpServers=Object.keys(mcp.mcpServers||{}).length;if(!mcp.mcpServers)add(report,'error','mcp','mcp.servers','.agents/mcp_config.json','mcpServers must be an object');}catch(e){add(report,'error','mcp','mcp.invalid','.agents/mcp_config.json',e.message);}
  try{const hooks=readJson(path.join(base,'hooks.json'));const handlers=Object.values(hooks).filter(v=>v&&typeof v==='object').flatMap(v=>v.PreToolUse||[]).flatMap(v=>v.hooks||[]).length;report.counts.hooks=handlers;if(!handlers)add(report,'error','hooks','hooks.empty','.agents/hooks.json','At least one safety hook is required');}catch(e){add(report,'error','hooks','hooks.invalid','.agents/hooks.json',e.message);}
  for(const name of contract?.phases?.orchestration?.agents||[])if(!fs.existsSync(path.join(base,'agents',`${name}.md`)))add(report,'error','orchestration','agent.missing',`.agents/agents/${name}.md`,'Required agent missing');
  for(const name of contract?.phases?.orchestration?.skills||[])if(!fs.existsSync(path.join(base,'skills',name,'SKILL.md')))add(report,'error','orchestration','skill.missing',`.agents/skills/${name}/SKILL.md`,'Required skill missing');
  try{const plugin=readJson(path.join(root,contract?.phases?.plugin?.manifest||'.agents/plugins/ag-kit/plugin.json'));if(!plugin.name||!plugin.description)add(report,'error','plugin','plugin.shape','.agents/plugins/ag-kit/plugin.json','plugin requires name and description');}catch(e){add(report,'error','plugin','plugin.invalid','.agents/plugins/ag-kit/plugin.json',e.message);}
  for(const file of ['shared/core/CORE.md','platform-capabilities.json','scripts/check-v2.mjs','scripts/sync-antigravity-projection.mjs'])if(!fs.existsSync(path.join(root,file)))add(report,'error','validation','file.missing',file,'Required v2 validation file missing');
  for(const phase of ['discovery','mcp','hooks','orchestration','plugin','validation'])report.phases[phase]=!report.findings.some(x=>x.phase===phase&&x.severity==='error');
  report.passed=!report.findings.some(x=>x.severity==='error');return report;
}
if(import.meta.url===`file://${process.argv[1]}`){const root=process.cwd();const report=diagnose(root);console.log(`AG Kit Antigravity doctor: ${root}`);for(const [p,ok] of Object.entries(report.phases))console.log(`${ok?'[PASS]':'[FAIL]'} ${p}`);for(const x of report.findings)console.log(`[${x.severity.toUpperCase()}] ${x.file} ${x.code} - ${x.message}`);console.log(`Counts: ${JSON.stringify(report.counts)}`);process.exitCode=report.passed?0:1;}
