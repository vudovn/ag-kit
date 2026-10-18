import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { isDirectRun } from '../../cli/lib/direct-run.js';

const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..','..');

test('isDirectRun matches spaces, non-ASCII paths, and symlinks',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'ag kit dự án-'));
  try{
    const file=path.join(dir,'entry.mjs');
    fs.writeFileSync(file,'');
    const url=pathToFileURL(fs.realpathSync(file)).href;
    assert.equal(isDirectRun(url,file),true);
    const link=path.join(dir,'link.mjs');
    try{fs.symlinkSync(file,link);assert.equal(isDirectRun(url,link),true);}catch(error){if(error.code!=='EPERM')throw error;}
    assert.equal(isDirectRun(url,path.join(dir,'missing.mjs')),false);
    assert.equal(isDirectRun(url,undefined),false);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});

test('engine entrypoints run when the checkout path has spaces and non-ASCII characters',()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'ag kit dự án-'));
  try{
    fs.cpSync(path.join(repo,'engine'),path.join(dir,'engine'),{recursive:true});
    fs.cpSync(path.join(repo,'cli','lib'),path.join(dir,'cli','lib'),{recursive:true});
    for(const name of ['memory','team']){
      const run=spawnSync(process.execPath,[path.join(dir,'engine',`${name}.mjs`)],{encoding:'utf8'});
      assert.equal(run.status,1,`${name}.mjs should reach its CLI branch`);
      assert.match(run.stderr,/Usage:/);
    }
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
