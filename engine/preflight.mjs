#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { appendReceipt, parseArgs } from './lib.mjs';

const defaultGates = [
  { name:'v2-architecture', command:'npm', args:['run','check:v2'], blocking:true },
  { name:'legacy-registry', command:'npm', args:['run','check:agents'], blocking:true },
  { name:'toolkit-tests', command:'npm', args:['run','test:toolkit'], blocking:true },
  { name:'antigravity-doctor', command:'npm', args:['run','check:antigravity'], blocking:true },
  { name:'antigravity-tests', command:'npm', args:['run','test:antigravity'], blocking:true },
  { name:'runtime-projections', command:'npm', args:['run','build:runtimes'], blocking:true }
];

export function runPreflight({ root = process.cwd(), gates = defaultGates }) {
  const results = [];
  for (const gate of gates) {
    const started = Date.now();
    const r = spawnSync(gate.command,gate.args,{cwd:root,encoding:'utf8',stdio:'pipe',timeout:240000,shell:false});
    results.push({name:gate.name,blocking:gate.blocking,ok:r.status===0,durationMs:Date.now()-started,exitCode:r.status,output:(r.stdout||r.stderr||'').trim().slice(-1200)});
  }
  const failed = results.filter(x=>x.blocking&&!x.ok);
  appendReceipt(root,'preflight',{action:'run',passed:failed.length===0,results:results.map(({output,...r})=>r)});
  return { passed:failed.length===0, results };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = parseArgs(process.argv.slice(2));
  const report = runPreflight({root:args.path||process.cwd()});
  for (const item of report.results) console.log(`${item.ok?'PASS':'FAIL'} ${item.name} ${item.durationMs}ms`);
  if (!report.passed) process.exitCode=1;
}
