import fs from 'node:fs';
import path from 'node:path';

export const stateRoot = (root = process.cwd()) => path.join(path.resolve(root), '.ag-kit');
export const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
export const readJson = (file, fallback = null) => {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fallback; }
};
export const writeJson = (file, value) => {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
};
export const appendReceipt = (root, type, data) => {
  const dir = path.join(stateRoot(root), 'receipts');
  ensureDir(dir);
  const record = { ts: new Date().toISOString(), type, ...data };
  fs.appendFileSync(path.join(dir, `${type}.jsonl`), JSON.stringify(record) + '\n');
  return record;
};
export const slugify = (value) => String(value).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 64) || 'entry';
export const parseArgs = (argv) => {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const item = argv[i];
    if (!item.startsWith('--')) { out._.push(item); continue; }
    const key = item.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) { out[key] = next; i++; }
    else out[key] = true;
  }
  return out;
};
