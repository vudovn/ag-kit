#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function add(report, severity, phase, code, file, message) {
  report.findings.push({severity, phase, code, file, message});
}

function countMarkdown(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, {withFileTypes: true}).filter(entry => entry.isFile() && entry.name.endsWith('.md')).length;
}

function countSkills(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, {withFileTypes: true})
    .filter(entry => entry.isDirectory() && fs.existsSync(path.join(dir, entry.name, 'SKILL.md'))).length;
}

function checkDiscovery(root, report) {
  const base = path.join(root, '.agents');
  const counts = {
    rules: countMarkdown(path.join(base, 'rules')),
    skills: countSkills(path.join(base, 'skills')),
    agents: countMarkdown(path.join(base, 'agents'))
  };
  Object.assign(report.counts, counts);
  for (const [kind, count] of Object.entries(counts)) {
    if (!count) add(report, 'error', 'discovery', `${kind}.missing`, `.agents/${kind}`, `No native Antigravity ${kind} discovered.`);
  }
  if (fs.existsSync(path.join(base, 'workflows'))) {
    report.counts.legacyWorkflows = countMarkdown(path.join(base, 'workflows'));
    add(report, 'warning', 'discovery', 'workflows.legacy', '.agents/workflows', 'Legacy workflows remain during migration; new orchestration should use skills.');
  }
}

function checkMcp(root, report) {
  const file = path.join(root, '.agents', 'mcp_config.json');
  if (!fs.existsSync(file)) return add(report, 'error', 'mcp', 'mcp.missing', '.agents/mcp_config.json', 'Workspace MCP configuration is missing.');
  try {
    const config = readJson(file);
    if (!config.mcpServers || typeof config.mcpServers !== 'object' || Array.isArray(config.mcpServers)) {
      add(report, 'error', 'mcp', 'mcp.servers', '.agents/mcp_config.json', 'mcpServers must be an object.');
      return;
    }
    report.counts.mcpServers = Object.keys(config.mcpServers).length;
    const text = JSON.stringify(config);
    if (/YOUR_[A-Z0-9_]+|CHANGE_ME|<[^>]+>/.test(text)) {
      add(report, 'warning', 'mcp', 'mcp.placeholder', '.agents/mcp_config.json', 'MCP config contains unresolved placeholders.');
    }
  } catch (error) {
    add(report, 'error', 'mcp', 'mcp.invalid_json', '.agents/mcp_config.json', error.message);
  }
}

function checkHooks(root, report) {
  const file = path.join(root, '.agents', 'hooks.json');
  if (!fs.existsSync(file)) return add(report, 'error', 'hooks', 'hooks.missing', '.agents/hooks.json', 'Native hooks configuration is missing.');
  try {
    const config = readJson(file);
    let handlers = 0;
    for (const [name, definition] of Object.entries(config)) {
      if (name === '$schema') continue;
      if (!definition || typeof definition !== 'object' || Array.isArray(definition)) {
        add(report, 'error', 'hooks', 'hooks.definition', `.agents/hooks.json#${name}`, 'Hook definition must be an object.');
        continue;
      }
      for (const event of ['PreToolUse', 'PostToolUse']) {
        if (definition[event] === undefined) continue;
        if (!Array.isArray(definition[event])) {
          add(report, 'error', 'hooks', 'hooks.event', `.agents/hooks.json#${name}.${event}`, `${event} must be an array.`);
          continue;
        }
        for (const entry of definition[event]) {
          if (typeof entry.matcher !== 'string' || !Array.isArray(entry.hooks) || entry.hooks.length === 0) {
            add(report, 'error', 'hooks', 'hooks.matched_event', `.agents/hooks.json#${name}.${event}`, 'Matched hook events require matcher and hooks[].');
            continue;
          }
          for (const handler of entry.hooks) {
            handlers += 1;
            if (typeof handler.command !== 'string' || !handler.command.trim()) {
              add(report, 'error', 'hooks', 'hooks.command', `.agents/hooks.json#${name}.${event}`, 'Command handler requires command.');
            }
          }
        }
      }
      for (const event of ['PreInvocation', 'PostInvocation', 'Stop']) {
        if (definition[event] === undefined) continue;
        if (!Array.isArray(definition[event])) add(report, 'error', 'hooks', 'hooks.event', `.agents/hooks.json#${name}.${event}`, `${event} must be an array.`);
        else handlers += definition[event].length;
      }
    }
    report.counts.hooks = handlers;
    if (!handlers) add(report, 'warning', 'hooks', 'hooks.empty', '.agents/hooks.json', 'No hook handlers registered.');
  } catch (error) {
    add(report, 'error', 'hooks', 'hooks.invalid_json', '.agents/hooks.json', error.message);
  }
}

function checkOrchestration(root, report, contract) {
  const orchestration = contract?.phases?.orchestration ?? {};
  for (const name of orchestration.agents ?? []) {
    const file = path.join(root, '.agents', 'agents', `${name}.md`);
    const nested = path.join(root, '.agents', 'agents', name, 'agent.md');
    if (!fs.existsSync(file) && !fs.existsSync(nested)) add(report, 'error', 'orchestration', 'agent.missing', `.agents/agents/${name}`, 'Required native custom agent is missing.');
  }
  for (const name of orchestration.skills ?? []) {
    const file = path.join(root, '.agents', 'skills', name, 'SKILL.md');
    if (!fs.existsSync(file)) add(report, 'error', 'orchestration', 'skill.missing', `.agents/skills/${name}/SKILL.md`, 'Required orchestration skill is missing.');
  }
}

function checkPlugin(root, report, contract) {
  const manifest = contract?.phases?.plugin?.manifest ?? '.agents/plugins/ag-kit/plugin.json';
  const file = path.join(root, manifest);
  if (!fs.existsSync(file)) return add(report, 'error', 'plugin', 'plugin.manifest_missing', manifest, 'Native Antigravity plugin manifest is missing.');
  try {
    const plugin = readJson(file);
    if (!plugin.name || !plugin.description) add(report, 'error', 'plugin', 'plugin.manifest_shape', manifest, 'plugin.json requires name and description.');
  } catch (error) {
    add(report, 'error', 'plugin', 'plugin.invalid_json', manifest, error.message);
  }
}

function checkValidation(root, report) {
  for (const file of ['AGENTS.md', 'platform-capabilities.json', 'scripts/check-platform-drift.mjs', '.agents/hooks/tests/antigravity.test.mjs', 'MIGRATION.md', 'SECURITY.md']) {
    if (!fs.existsSync(path.join(root, file))) add(report, 'error', 'validation', 'validation.file_missing', file, 'Required validation or operator file is missing.');
  }

  const versionFiles = [
    ['.agents/VERSION', value => value.trim()],
    ['package.json', value => JSON.parse(value).version],
    ['cli/package.json', value => JSON.parse(value).version],
    ['web/package.json', value => JSON.parse(value).version]
  ];
  const versions = [];
  for (const [file, parse] of versionFiles) {
    try {
      versions.push([file, parse(fs.readFileSync(path.join(root, file), 'utf8'))]);
    } catch (error) {
      add(report, 'error', 'validation', 'validation.version_invalid', file, error.message);
    }
  }
  if (new Set(versions.map(([, value]) => value)).size > 1) {
    add(report, 'error', 'validation', 'validation.version_mismatch', 'VERSION', `Release versions are not synchronized: ${versions.map(([file, value]) => `${file}=${value}`).join(', ')}`);
  }
  report.counts.releaseVersions = Object.fromEntries(versions);
}

export function diagnose(root) {
  const report = {runtime: 'antigravity', root, passed: true, counts: {}, phases: {}, findings: []};
  const contractPath = path.join(root, '.agents', 'antigravity.json');
  let contract = null;
  try {
    contract = readJson(contractPath);
    if (contract.runtime !== 'antigravity') add(report, 'error', 'discovery', 'contract.runtime', '.agents/antigravity.json', 'runtime must be antigravity.');
  } catch (error) {
    add(report, 'error', 'discovery', 'contract.invalid', '.agents/antigravity.json', error.message);
  }

  checkDiscovery(root, report);
  checkMcp(root, report);
  checkHooks(root, report);
  checkOrchestration(root, report, contract);
  checkPlugin(root, report, contract);
  checkValidation(root, report);

  for (const phase of ['discovery', 'mcp', 'hooks', 'orchestration', 'plugin', 'validation']) {
    report.phases[phase] = !report.findings.some(item => item.phase === phase && item.severity === 'error');
  }
  report.passed = !report.findings.some(item => item.severity === 'error');
  return report;
}

function parseArgs(argv) {
  const options = {root: process.cwd(), json: false, strict: false};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--root') options.root = path.resolve(argv[++i]);
    else if (argv[i] === '--json') options.json = true;
    else if (argv[i] === '--strict') options.strict = true;
    else if (argv[i] === '--help') options.help = true;
    else throw new Error(`Unknown argument: ${argv[i]}`);
  }
  return options;
}

function printHuman(report) {
  console.log(`AG Kit Antigravity doctor: ${report.root}`);
  for (const [phase, passed] of Object.entries(report.phases)) console.log(`${passed ? '[PASS]' : '[FAIL]'} ${phase}`);
  for (const item of report.findings) console.log(`[${item.severity.toUpperCase()}] ${item.file} ${item.code} - ${item.message}`);
  console.log(`Counts: ${JSON.stringify(report.counts)}`);
  console.log(report.passed ? '[PASS] Antigravity native contract is ready.' : '[FAIL] Antigravity contract has blocking findings.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      console.log('Usage: node .agents/hooks/antigravity-doctor.mjs [--root PATH] [--json] [--strict]');
      process.exit(0);
    }
    const report = diagnose(options.root);
    if (options.json) console.log(JSON.stringify(report, null, 2));
    else printHuman(report);
    const hasWarnings = report.findings.some(item => item.severity === 'warning');
    process.exitCode = report.passed && !(options.strict && hasWarnings) ? 0 : 1;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
