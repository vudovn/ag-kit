#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { appendReceipt, parseArgs } from './lib.mjs';

export const roster = [
  { id:'codex', lineage:'openai', command:'codex', args:['--version'] },
  { id:'gemini', lineage:'google', command:'gemini', args:['--version'] },
  { id:'qwen', lineage:'alibaba', command:'qwen', args:['--version'] },
  { id:'opencode', lineage:'oss', command:'opencode', args:['--version'] },
  { id:'aider', lineage:'oss', command:'aider', args:['--version'] },
  { id:'copilot', lineage:'openai', command:'copilot', args:['--version'] }
];

export function probeRoster() {
  return roster.map(item => {
    const r = spawnSync(item.command,item.args,{encoding:'utf8',timeout:3000,shell:false});
    return {...item, available: !r.error && r.status === 0, version: (r.stdout||r.stderr||'').trim().split(/\r?\n/)[0] || null};
  });
}

export function prepareAudit({root=process.cwd(),target='.'}) {
  const probes = probeRoster();
  const available = probes.filter(x=>x.available);
  const lineages = [...new Set(available.map(x=>x.lineage))];
  const record = appendReceipt(root,'cross-audit',{action:'probe',target,available:available.map(x=>x.id),lineages});
  return { target, probes, lineages, receipt: record, status: lineages.length >= 2 ? 'ready' : 'degraded' };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = parseArgs(process.argv.slice(2));
  const target = args.target || args._[0] || '.';
  if (target !== '.' && !fs.existsSync(path.resolve(args.path||process.cwd(),target))) { console.error(`Target not found: ${target}`); process.exit(1); }
  console.log(JSON.stringify(prepareAudit({root:args.path||process.cwd(),target}),null,2));
}
