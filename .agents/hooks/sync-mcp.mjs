#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const options = {root: process.cwd(), apply: false, print: false, force: false, target: 'suite', servers: []};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--root') options.root = path.resolve(argv[++i]);
    else if (arg === '--apply') options.apply = true;
    else if (arg === '--print') options.print = true;
    else if (arg === '--force') options.force = true;
    else if (arg === '--target') options.target = argv[++i];
    else if (arg === '--server') {
      const name = argv[++i];
      if (!name || name.startsWith('--')) throw new Error('--server needs a workspace server name');
      options.servers.push(name);
    }
    else if (arg === '--check') { /* default */ }
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!['suite', 'cli'].includes(options.target)) throw new Error('--target must be suite or cli');
  return options;
}

function readJson(file, fallback = null) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function containsPlaceholder(value) {
  let found = false;
  const walk = item => {
    if (typeof item === 'string' && /YOUR_[A-Z0-9_]+|CHANGE_ME|<[^>]+>/.test(item)) found = true;
    else if (Array.isArray(item)) item.forEach(walk);
    else if (item && typeof item === 'object') Object.values(item).forEach(walk);
  };
  walk(value);
  return found;
}

function selectServers(workspace, names) {
  const requested = [...new Set(names)];
  if (!requested.length) return workspace;
  const missing = requested.filter(name => !Object.hasOwn(workspace.mcpServers, name));
  if (missing.length) throw new Error(`Unknown workspace MCP server: ${missing.join(', ')}`);
  return {
    ...workspace,
    mcpServers: Object.fromEntries(requested.map(name => [name, workspace.mcpServers[name]]))
  };
}

function mergeServers(existing, workspace, force) {
  const result = structuredClone(existing ?? {mcpServers: {}});
  if (!result.mcpServers || typeof result.mcpServers !== 'object') result.mcpServers = {};
  const conflicts = [];
  for (const [name, server] of Object.entries(workspace.mcpServers ?? {})) {
    if (Object.hasOwn(result.mcpServers, name) && !force) {
      conflicts.push(name);
      continue;
    }
    result.mcpServers[name] = server;
  }
  return {result, conflicts};
}

function targetPath(target) {
  return target === 'suite'
    ? path.join(os.homedir(), '.gemini', 'config', 'mcp_config.json')
    : path.join(os.homedir(), '.gemini', 'antigravity-cli', 'mcp_config.json');
}

function backup(file) {
  if (!fs.existsSync(file)) return null;
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `${file}.ag-kit-backup-${stamp}`;
  fs.copyFileSync(file, backupFile);
  return backupFile;
}

export function planSync({root, target = 'suite', force = false, servers = []}) {
  const source = path.join(root, '.agents', 'mcp_config.json');
  const workspace = readJson(source);
  if (!workspace || typeof workspace.mcpServers !== 'object') throw new Error('Invalid workspace .agents/mcp_config.json');
  const selected = selectServers(workspace, servers);
  const destination = targetPath(target);
  const existing = readJson(destination, {mcpServers: {}});
  const {result, conflicts} = mergeServers(existing, selected, force);
  return {source, destination, workspace: selected, merged: result, conflicts, placeholders: containsPlaceholder(selected)};
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const options = parseArgs(process.argv.slice(2));
    const plan = planSync(options);
    console.log(`Source: ${plan.source}`);
    console.log(`Target: ${plan.destination}`);
    console.log(`Servers: ${Object.keys(plan.workspace.mcpServers).join(', ') || '(none)'}`);
    if (plan.conflicts.length) console.log(`Conflicts kept unchanged: ${plan.conflicts.join(', ')}`);
    if (plan.placeholders) console.log('Warning: unresolved placeholders detected; --apply is blocked until they are configured.');
    if (options.print) console.log(JSON.stringify(plan.merged, null, 2));
    if (options.apply) {
      if (plan.placeholders) throw new Error('Refusing to apply MCP configuration with unresolved placeholders.');
      fs.mkdirSync(path.dirname(plan.destination), {recursive: true});
      const backupFile = backup(plan.destination);
      fs.writeFileSync(plan.destination, `${JSON.stringify(plan.merged, null, 2)}\n`, 'utf8');
      console.log(`Applied MCP configuration.${backupFile ? ` Backup: ${backupFile}` : ''}`);
    } else {
      console.log('Check only. Use --apply after reviewing the plan.');
    }
  } catch (error) {
    console.error(`MCP sync failed: ${error.message}`);
    process.exitCode = 1;
  }
}
