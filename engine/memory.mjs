#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { ensureDir, stateRoot, slugify, appendReceipt, parseArgs } from './lib.mjs';

const tokenize = (s) => String(s).toLowerCase().match(/[\p{L}\p{N}_-]+/gu) || [];
const memoryDir = (root) => path.join(stateRoot(root), 'memory');

export function initMemory(root = process.cwd()) {
  const dir = memoryDir(root);
  ensureDir(path.join(dir, 'entries'));
  for (const [name, title] of [['DECISIONS.md','Decisions'],['CONVENTIONS.md','Conventions'],['HANDOFF.md','Handoff']]) {
    const file = path.join(dir, name);
    if (!fs.existsSync(file)) fs.writeFileSync(file, `# ${title}\n\n`);
  }
  return dir;
}

export function addMemory({ root = process.cwd(), text, kind = 'learning', title = '' }) {
  if (!text?.trim()) throw new Error('memory text is required');
  const dir = initMemory(root);
  const id = `${Date.now()}-${slugify(title || text.slice(0, 48))}`;
  const file = path.join(dir, 'entries', `${id}.md`);
  const body = `---\nid: ${id}\nkind: ${kind}\ncreated: ${new Date().toISOString()}\n---\n# ${title || kind}\n\n${text.trim()}\n`;
  fs.writeFileSync(file, body);
  appendReceipt(root, 'memory', { action: 'add', id, kind, file: path.relative(root, file) });
  return { id, file };
}

export function recallMemory({ root = process.cwd(), query, limit = 5 }) {
  const dir = initMemory(root);
  const terms = [...new Set(tokenize(query))];
  const files = fs.readdirSync(path.join(dir,'entries')).filter(x=>x.endsWith('.md'));
  const ranked = files.map(name => {
    const file = path.join(dir,'entries',name);
    const text = fs.readFileSync(file,'utf8');
    const hay = text.toLowerCase();
    let score = 0;
    for (const term of terms) score += (hay.split(term).length - 1) * (term.length > 5 ? 2 : 1);
    return { file: path.relative(root,file), score, preview: text.replace(/^---[\s\S]*?---\s*/,'').trim().slice(0,280) };
  }).filter(x => terms.length === 0 || x.score > 0).sort((a,b)=>b.score-a.score || a.file.localeCompare(b.file)).slice(0, Number(limit));
  appendReceipt(root, 'memory', { action: 'recall', query, count: ranked.length });
  return ranked;
}

export function memoryStatus(root = process.cwd()) {
  const dir = initMemory(root);
  const entries = fs.readdirSync(path.join(dir,'entries')).filter(x=>x.endsWith('.md')).length;
  return { root: path.relative(root,dir) || '.', entries, canonical: 'markdown', index: 'rebuildable-keyword-scan' };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = parseArgs(process.argv.slice(2));
  const [cmd, ...rest] = args._;
  const root = args.path || process.cwd();
  if (cmd === 'init') console.log(initMemory(root));
  else if (cmd === 'add') console.log(JSON.stringify(addMemory({root,text:rest.join(' '),kind:args.kind||'learning',title:args.title||''}),null,2));
  else if (cmd === 'recall') console.log(JSON.stringify(recallMemory({root,query:rest.join(' '),limit:args.limit||5}),null,2));
  else if (cmd === 'status') console.log(JSON.stringify(memoryStatus(root),null,2));
  else { console.log('Usage: node engine/memory.mjs <init|add|recall|status> [text/query] [--path dir]'); process.exitCode = 1; }
}
