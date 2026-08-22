import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import test from 'node:test';

import {diagnose} from '../antigravity-doctor.mjs';
import {buildPlugin} from '../build-plugin.mjs';
import {evaluateCommand, extractCommand} from '../validate-tool-call.mjs';
import {planSync} from '../sync-mcp.mjs';

const root = path.resolve(import.meta.dirname, '../../..');

test('extracts Antigravity CommandLine payload', () => {
  assert.equal(extractCommand({tool_args: {CommandLine: 'npm test'}}), 'npm test');
});

test('allows normal project cleanup', () => {
  assert.equal(evaluateCommand('rm -rf ./dist').allowed, true);
  assert.equal(evaluateCommand('rm -rf node_modules').allowed, true);
});

test('blocks destructive root and disk commands', () => {
  assert.equal(evaluateCommand('sudo rm -rf /').allowed, false);
  assert.equal(evaluateCommand('mkfs.ext4 /dev/sda1').allowed, false);
  assert.equal(evaluateCommand('dd if=/dev/zero of=/dev/sda').allowed, false);
  assert.equal(evaluateCommand('format C:').allowed, false);
});

test('hook process returns non-zero for blocked command', () => {
  const result = spawnSync(process.execPath, [path.join(root, '.agents/hooks/validate-tool-call.mjs')], {
    input: JSON.stringify({tool_args: {CommandLine: 'rm -rf /'}}),
    encoding: 'utf8'
  });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /BLOCKED by AG Kit/);
});

test('doctor recognizes all six implementation phases', () => {
  const report = diagnose(root);
  assert.equal(report.runtime, 'antigravity');
  assert.equal(report.phases.discovery, true);
  assert.equal(report.phases.mcp, true);
  assert.equal(report.phases.hooks, true);
  assert.equal(report.phases.orchestration, true);
  assert.equal(report.phases.plugin, true);
  assert.equal(report.phases.validation, true);
  assert.equal(report.passed, true);
});

test('runtime contract uses documented CLI capabilities instead of an invented version floor', () => {
  const contract = JSON.parse(fs.readFileSync(path.join(root, '.agents/antigravity.json'), 'utf8'));
  assert.equal('minimumCliVersion' in contract, false);
  assert.deepEqual(contract.requiredCliCommands, ['changelog', 'plugin', 'update']);
});

test('MCP sync detects placeholders and plans without writing', () => {
  const plan = planSync({root, target: 'suite', force: false});
  assert.equal(plan.placeholders, true);
  assert.ok(Object.keys(plan.workspace.mcpServers).length > 0);
});

test('MCP sync selects a ready server without unrelated placeholders', () => {
  const plan = planSync({root, target: 'suite', force: false, servers: ['xquik']});
  assert.equal(plan.placeholders, false);
  assert.deepEqual(Object.keys(plan.workspace.mcpServers), ['xquik']);
  assert.deepEqual(plan.merged.mcpServers.xquik, {url: 'https://xquik.com/mcp'});
});

test('MCP sync rejects unknown server selection', () => {
  assert.throws(
    () => planSync({root, target: 'suite', force: false, servers: ['missing']}),
    /Unknown workspace MCP server: missing/
  );
});

test('plugin builder creates manifest, commands, skills, and hook', () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-kit-plugin-'));
  const output = path.join(temporary, 'plugin');
  const manifest = buildPlugin(root, output);
  assert.equal(manifest.runtime, 'antigravity');
  assert.ok(manifest.counts.skills > 0);
  assert.ok(manifest.counts.workflows > 0);
  assert.ok(fs.existsSync(path.join(output, 'gemini-extension.json')));
  assert.ok(fs.existsSync(path.join(output, 'commands/ag-kit/orchestrate.toml')));
  assert.ok(fs.existsSync(path.join(output, 'hooks/hooks.json')));
  assert.ok(fs.existsSync(path.join(output, 'PLUGIN_CONTENTS.json')));
  const firstInventory = fs.readFileSync(path.join(output, 'PLUGIN_CONTENTS.json'), 'utf8');
  buildPlugin(root, output);
  const secondInventory = fs.readFileSync(path.join(output, 'PLUGIN_CONTENTS.json'), 'utf8');
  assert.equal(secondInventory, firstInventory);
  fs.rmSync(temporary, {recursive: true, force: true});
});
