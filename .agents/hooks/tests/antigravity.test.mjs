import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import test from 'node:test';
import {diagnose} from '../antigravity-doctor.mjs';
import {buildPlugin} from '../build-plugin.mjs';
import {evaluateCommand,extractCommand,hookDecision} from '../validate-tool-call.mjs';

const root=path.resolve(import.meta.dirname,'../../..');
const hookPayload=JSON.stringify({toolCall:{name:'run_command',args:{CommandLine:'rm -rf /'}}});

test('extracts native Antigravity CommandLine payload',()=>assert.equal(extractCommand({toolCall:{name:'run_command',args:{CommandLine:'npm test'}}}),'npm test'));
test('allows normal project cleanup',()=>assert.equal(evaluateCommand('rm -rf ./dist').allowed,true));
test('blocks destructive root commands',()=>assert.equal(evaluateCommand('sudo rm -rf /').allowed,false));
test('hook returns native deny JSON',()=>assert.deepEqual(hookDecision({toolCall:{name:'run_command',args:{CommandLine:'rm -rf /'}}}),{decision:'deny',reason:'AG Kit blocked unix-root-delete: recursive deletion of the filesystem root.'}));

test('hook process emits JSON',()=>{
  const r=spawnSync(process.execPath,[path.join(root,'.agents/hooks/validate-tool-call.mjs')],{input:hookPayload,encoding:'utf8',timeout:2000});
  assert.equal(r.status,0);
  assert.equal(JSON.parse(r.stdout).decision,'deny');
});

test('hook process resolves npm-style symlink entrypoints',()=>{
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'ag-kit-hook-link-'));
  try {
    const link=path.join(tmp,'validate-tool-call.mjs');
    fs.symlinkSync(path.join(root,'.agents/hooks/validate-tool-call.mjs'),link);
    const r=spawnSync(process.execPath,[link],{input:hookPayload,encoding:'utf8',timeout:2000});
    assert.equal(r.status,0);
    assert.equal(JSON.parse(r.stdout).decision,'deny');
  } finally {
    fs.rmSync(tmp,{recursive:true,force:true});
  }
});

test('lean native projection exists',()=>{assert.ok(fs.existsSync(path.join(root,'.agents/agents/scout.md')));assert.ok(fs.existsSync(path.join(root,'.agents/skills/ag-core/SKILL.md')));assert.equal(fs.existsSync(path.join(root,'.agents/workflows')),false);assert.equal(fs.existsSync(path.join(root,'.agents/agent')),false);});
test('doctor recognizes lean v2 contract',()=>{const r=diagnose(root);assert.equal(r.passed,true);assert.equal(r.counts.skills,18);assert.equal(r.counts.agents,4);});
test('native plugin builder is deterministic and lean',()=>{const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'ag-kit-plugin-'));const out=path.join(tmp,'plugin');const m=buildPlugin(root,out);assert.equal(m.runtime,'antigravity');assert.equal(m.counts.skills,18);assert.equal(m.counts.agents,4);assert.ok(fs.existsSync(path.join(out,'plugin.json')));assert.equal(fs.existsSync(path.join(out,'gemini-extension.json')),false);assert.ok(fs.existsSync(path.join(out,'hooks.json')));const a=fs.readFileSync(path.join(out,'PLUGIN_CONTENTS.json'),'utf8');buildPlugin(root,out);const b=fs.readFileSync(path.join(out,'PLUGIN_CONTENTS.json'),'utf8');assert.equal(a,b);fs.rmSync(tmp,{recursive:true,force:true});});
