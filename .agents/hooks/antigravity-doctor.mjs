#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const options = {root: process.cwd(), json: false, strict: false};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--root') options.root = path.resolve(argv[++i]);
    else if (arg === '--json') options.json = true;
    else if (arg === '--strict') options.strict = true;
    else if (arg === '--help') options.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return options;
}

function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
function relative(root, file) { return path.relative(root, file).split(path.sep).join('/'); }
function add(report, severity, phase, code, file, message) { report.findings.push({severity, phase, code, file, message}); }

function frontmatter(file) {
  const text = fs.readFileSync(file, 'utf8');
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return null;
  const data = {};
  for (const line of text.slice(4, end).split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (match) data[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, '');
  }
  return data;
}

function markdownFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(name => name.endsWith('.md')).map(name => path.join(dir, name)).sort();
}

function skillFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, {withFileTypes: true}).filter(entry => entry.isDirectory()).map(entry => path.join(dir, entry.name, 'SKILL.md')).filter(fs.existsSync).sort();
}

function checkDiscovery(root, report) {
  const agents = path.join(root, '.agents');
  for (const [kind, files, fields] of [
    ['rules', markdownFiles(path.join(agents, 'rules')), ['trigger']],
    ['workflows', markdownFiles(path.join(agents, 'workflows')), ['description']],
    ['skills', skillFiles(path.join(agents, 'skills')), ['description']]
  ]) {
    report.counts[kind] = files.length;
    if (!files.length) add(report, 'error', 'discovery', `${kind}.missing`, `.agents/${kind}`, `No Antigravity ${kind} were discovered.`);
    for (const file of files) {
      const meta = frontmatter(file);
      if (!meta) add(report, 'error', 'discovery', `${kind}.frontmatter`, relative(root, file), 'Missing YAML frontmatter.');
      else for (const field of fields) if (!meta[field]) add(report, 'error', 'discovery', `${kind}.required`, relative(root, file), `Missing frontmatter field: ${field}`);
    }
  }
}

function walkStrings(value, callback) {
  if (typeof value === 'string') callback(value);
  else if (Array.isArray(value)) value.forEach(item => walkStrings(item, callback));
  else if (value && typeof value === 'object') Object.values(value).forEach(item => walkStrings(item, callback));
}

function checkMcp(root, report) {
  const file = path.join(root, '.agents', 'mcp_config.json');
  let config;
  try { config = readJson(file); } catch (error) { add(report, 'error', 'mcp', 'mcp.invalid', '.agents/mcp_config.json', error.message); return; }
  if (!config.mcpServers || typeof config.mcpServers !== 'object' || Array.isArray(config.mcpServers)) {
    add(report, 'error', 'mcp', 'mcp.servers', '.agents/mcp_config.json', 'mcpServers must be an object.');
    return;
  }
  report.counts.mcpServers = Object.keys(config.mcpServers).length;
  for (const [name, server] of Object.entries(config.mcpServers)) {
    if (!server || typeof server !== 'object' || !(typeof server.command === 'string' || typeof server.serverURL === 'string' || typeof server.url === 'string')) add(report, 'error', 'mcp', 'mcp.server_shape', `.agents/mcp_config.json#${name}`, 'Server needs command, serverURL, or url.');
    walkStrings(server, value => { if (/YOUR_[A-Z0-9_]+|CHANGE_ME|<[^>]+>/.test(value)) add(report, 'warning', 'mcp', 'mcp.placeholder', `.agents/mcp_config.json#${name}`, 'Server contains an unresolved placeholder; configure it before enabling the server.'); });
  }
}

function localCommandPath(command) {
  const match = command.match(/(?:^|\s)(\.agents[/\\][^\s"']+)/);
  return match ? match[1] : null;
}

function validateHandler(root, report, ref, handler) {
  if (!handler || typeof handler !== 'object') { add(report, 'error', 'hooks', 'hooks.handler_shape', ref, 'Hook handler must be an object.'); return; }
  if (handler.type !== undefined && handler.type !== 'command') add(report, 'error', 'hooks', 'hooks.type', ref, 'Only command handlers are supported.');
  if (typeof handler.command !== 'string' || !handler.command.trim()) add(report, 'error', 'hooks', 'hooks.command', ref, 'command is required.');
  if (handler.timeout !== undefined && (!Number.isInteger(handler.timeout) || handler.timeout < 1 || handler.timeout > 300)) add(report, 'error', 'hooks', 'hooks.timeout', ref, 'timeout must be an integer from 1 to 300 seconds.');
  const localPath = typeof handler.command === 'string' ? localCommandPath(handler.command) : null;
  if (localPath && !fs.existsSync(path.join(root, localPath))) add(report, 'error', 'hooks', 'hooks.command_missing', ref, `Local hook target does not exist: ${localPath}`);
}

function checkHooks(root, report) {
  const file = path.join(root, '.agents', 'hooks.json');
  let config;
  try { config = readJson(file); } catch (error) { add(report, 'error', 'hooks', 'hooks.invalid_json', '.agents/hooks.json', error.message); return; }
  let total = 0;
  for (const [name, definition] of Object.entries(config)) {
    if (name === '$schema') continue;
    const base = `.agents/hooks.json#${name}`;
    if (!definition || typeof definition !== 'object' || Array.isArray(definition)) { add(report, 'error', 'hooks', 'hooks.definition_shape', base, 'Named hook definition must be an object.'); continue; }
    if (definition.enabled !== undefined && typeof definition.enabled !== 'boolean') add(report, 'error', 'hooks', 'hooks.enabled', base, 'enabled must be boolean.');
    for (const event of ['PreToolUse', 'PostToolUse']) {
      if (definition[event] === undefined) continue;
      if (!Array.isArray(definition[event])) { add(report, 'error', 'hooks', 'hooks.event_shape', `${base}.${event}`, `${event} must be an array.`); continue; }
      definition[event].forEach((entry, index) => {
        const ref = `${base}.${event}[${index}]`;
        if (!entry || typeof entry !== 'object' || typeof entry.matcher !== 'string' || !Array.isArray(entry.hooks) || !entry.hooks.length) { add(report, 'error', 'hooks', 'hooks.tool_event_shape', ref, `${event} requires matcher and a non-empty hooks array.`); return; }
        entry.hooks.forEach((handler, handlerIndex) => { total += 1; validateHandler(root, report, `${ref}.hooks[${handlerIndex}]`, handler); });
      });
    }
    for (const event of ['PreInvocation', 'PostInvocation', 'Stop']) {
      if (definition[event] === undefined) continue;
      if (!Array.isArray(definition[event])) { add(report, 'error', 'hooks', 'hooks.event_shape', `${base}.${event}`, `${event} must be an array.`); continue; }
      definition[event].forEach((handler, index) => { total += 1; validateHandler(root, report, `${base}.${event}[${index}]`, handler); });
    }
  }
  report.counts.hooks = total;
  if (!total) add(report, 'warning', 'hooks', 'hooks.empty', '.agents/hooks.json', 'No native hooks are registered.');
}

function checkOrchestration(root, report, contract) {
  const cfg = contract?.phases?.orchestration ?? {};
  for (const [kind, names, resolve] of [
    ['workflow', cfg.workflows ?? [], name => path.join(root, '.agents', 'workflows', `${name}.md`)],
    ['agent', cfg.agents ?? [], name => path.join(root, '.agents', 'agent', `${name}.md`)],
    ['skill', cfg.skills ?? [], name => path.join(root, '.agents', 'skills', name, 'SKILL.md')]
  ]) for (const name of names) { const file = resolve(name); if (!fs.existsSync(file)) add(report, 'error', 'orchestration', `orchestration.${kind}_missing`, relative(root, file), `Required Antigravity ${kind} is missing.`); }
}

function checkPlugin(root, report) {
  for (const file of ['.agents/hooks/build-plugin.mjs', '.agents/hooks/plugin/GEMINI.md', '.agents/hooks/plugin/gemini-extension.template.json']) if (!fs.existsSync(path.join(root, file))) add(report, 'error', 'plugin', 'plugin.file_missing', file, 'Plugin packaging input is missing.');
}

function checkValidation(root, report) {
  for (const file of ['.agents/hooks/tests/antigravity.test.mjs', 'MIGRATION.md', 'SECURITY.md']) if (!fs.existsSync(path.join(root, file))) add(report, 'error', 'validation', 'validation.file_missing', file, 'Production validation or operator documentation is missing.');
  const specs = [['.agents/VERSION', value => value.trim()], ['package.json', value => JSON.parse(value).version], ['cli/package.json', value => JSON.parse(value).version], ['web/package.json', value => JSON.parse(value).version]];
  const versions = [];
  for (const [file, parse] of specs) try { versions.push([file, parse(fs.readFileSync(path.join(root, file), 'utf8'))]); } catch (error) { add(report, 'error', 'validation', 'validation.version_invalid', file, error.message); }
  if (new Set(versions.map(([, value]) => value)).size > 1) add(report, 'error', 'validation', 'validation.version_mismatch', 'VERSION', `Release versions are not synchronized: ${versions.map(([file, value]) => `${file}=${value}`).join(', ')}`);
  report.counts.releaseVersions = Object.fromEntries(versions);
}

export function diagnose(root) {
  const report = {runtime: 'antigravity', root, passed: true, counts: {}, phases: {}, findings: []};
  let contract;
  try { contract = readJson(path.join(root, '.agents', 'antigravity.json')); if (contract.runtime !== 'antigravity') add(report, 'error', 'discovery', 'contract.runtime', '.agents/antigravity.json', 'runtime must be antigravity.'); } catch (error) { add(report, 'error', 'discovery', 'contract.invalid', '.agents/antigravity.json', error.message); }
  checkDiscovery(root, report); checkMcp(root, report); checkHooks(root, report); checkOrchestration(root, report, contract); checkPlugin(root, report); checkValidation(root, report);
  for (const phase of ['discovery', 'mcp', 'hooks', 'orchestration', 'plugin', 'validation']) report.phases[phase] = !report.findings.some(item => item.phase === phase && item.severity === 'error');
  report.passed = !report.findings.some(item => item.severity === 'error');
  return report;
}

function printHuman(report) {
  console.log(`AG Kit Antigravity doctor: ${report.root}`);
  for (const [phase, passed] of Object.entries(report.phases)) console.log(`${passed ? '[PASS]' : '[FAIL]'} ${phase}`);
  for (const item of report.findings) console.log(`[${item.severity.toUpperCase()}] ${item.file} ${item.code} - ${item.message}`);
  console.log(`Counts: ${JSON.stringify(report.counts)}`);
  console.log(report.passed ? '[PASS] Antigravity contract is ready.' : '[FAIL] Antigravity contract has blocking findings.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) { console.log('Usage: node .agents/hooks/antigravity-doctor.mjs [--root PATH] [--json] [--strict]'); process.exit(0); }
    const report = diagnose(options.root);
    if (options.json) console.log(JSON.stringify(report, null, 2)); else printHuman(report);
    process.exitCode = report.passed && !(options.strict && report.findings.some(item => item.severity === 'warning')) ? 0 : 1;
  } catch (error) { console.error(error.message); process.exitCode = 2; }
}
