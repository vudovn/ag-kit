import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import test from 'node:test';

import {diagnose} from '../antigravity-doctor.mjs';
import {buildPlugin} from '../build-plugin.mjs';
import {decisionForPayload, evaluateCommand, extractCommand} from '../validate-tool-call.mjs';
import {planSync} from '../sync-mcp.mjs';

const root = path.resolve(import.meta.dirname, '../../..');

test('extracts native and legacy Antigravity command payloads', () => {
  assert.equal(extractCommand({toolCall: {args: {CommandLine: 'npm test'}}}), 'npm test');
  assert.equal(extractCommand({tool_args: {CommandLine: 'npm test'}}), 'npm test');
});

test('allows normal cleanup and denies destructive commands', () => {
  assert.equal(evaluateCommand('rm -rf ./dist').decision, 'allow');
  assert.equal(evaluateCommand('rm -rf node_modules').decision, 'allow');
  assert.equal(evaluateCommand('sudo rm -rf /').decision, 'deny');
  assert.equal(evaluateCommand('mkfs.ext4 /dev/sda1').decision, 'deny');
  assert.equal(evaluateCommand('dd if=/dev/zero of=/dev/sda').decision, 'deny');
  assert.equal(evaluateCommand('format C:').decision, 'deny');
});

test('returns the native JSON decision contract', () => {
  assert.equal(decisionForPayload({toolCall: {args: {CommandLine: 'npm test'}}}).decision, 'allow');
  assert.equal(decisionForPayload({toolCall: {args: {CommandLine: 'rm -rf /'}}}).decision, 'deny');
  assert.equal(decisionForPayload({}).decision, 'allow');
});

test('hook process emits JSON and exits zero for allow, deny, and invalid input', () => {
  for (const [input, decision] of [
    [JSON.stringify({toolCall: {args: {CommandLine: 'npm test'}}}), 'allow'],
    [JSON.stringify({toolCall: {args: {CommandLine: 'rm -rf /'}}}), 'deny'],
    ['not-json', 'ask']
  ]) {
    const result = spawnSync(process.execPath, [path.join(root, '.agents/hooks/validate-tool-call.mjs')], {input, encoding: 'utf8'});
    assert.equal(result.status, 0);
    assert.equal(JSON.parse(result.stdout).decision, decision);
  }
});

test('doctor recognizes all six implementation phases', () => {
  const report = diagnose(root);
  assert.equal(report.runtime, 'antigravity');
  for (const phase of ['discovery', 'mcp', 'hooks', 'orchestration', 'plugin', 'validation']) assert.equal(report.phases[phase], true);
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

test('plugin builder creates deterministic inventory', () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-kit-plugin-'));
  const output = path.join(temporary, 'plugin');
  const manifest = buildPlugin(root, output);
  assert.equal(manifest.runtime, 'antigravity');
  assert.ok(manifest.counts.skills > 0);
  const first = fs.readFileSync(path.join(output, 'PLUGIN_CONTENTS.json'), 'utf8');
  buildPlugin(root, output);
  assert.equal(fs.readFileSync(path.join(output, 'PLUGIN_CONTENTS.json'), 'utf8'), first);
  fs.rmSync(temporary, {recursive: true, force: true});
});
