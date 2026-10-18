import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { addMemory, recallMemory, memoryStatus, rebuildMemoryIndex } from '../memory.mjs';
import { initTeam } from '../team.mjs';
import { snapshotAuditTarget } from '../cross-audit.mjs';

const temp=()=>fs.mkdtempSync(path.join(os.tmpdir(),'ag-kit-v2-'));

test('memory keeps markdown canonical and builds optional warm index',()=>{
  const root=temp();
  try{
    addMemory({root,text:'Use PostgreSQL transactions for billing writes',kind:'decision',title:'Billing DB'});
    addMemory({root,text:'Frontend uses accessible semantic HTML',kind:'convention'});
    const hit=recallMemory({root,query:'billing PostgreSQL'});
    assert.equal(hit.length,1);
    assert.match(hit[0].preview,/PostgreSQL/);
    assert.equal(memoryStatus(root).canonical,'markdown');
    assert.ok(['sqlite-fts5','sqlite','sqlite-empty','markdown-scan'].includes(memoryStatus(root).index));
    assert.ok(rebuildMemoryIndex(root).entries>=2);
  }finally{fs.rmSync(root,{recursive:true,force:true});}
});

test('team assembly writes a project-local role bench',()=>{
  const root=temp();
  try{
    fs.writeFileSync(path.join(root,'package.json'),JSON.stringify({dependencies:{next:'latest'}}));
    const team=initTeam({root,archetype:'auto',name:'app'});
    assert.equal(team.archetype,'web');
    assert.ok(fs.existsSync(path.join(root,'.ag-kit','agents','frontend-builder.md')));
  }finally{fs.rmSync(root,{recursive:true,force:true});}
});

test('audit snapshot keeps reviewers away from project filesystem',()=>{
  const root=temp();
  try{
    fs.writeFileSync(path.join(root,'sample.js'),'export const x = 1;\n');
    const snapshot=snapshotAuditTarget({root,target:'sample.js'});
    assert.equal(snapshot.kind,'file');
    assert.match(snapshot.content,/export const x/);
    assert.throws(()=>snapshotAuditTarget({root,target:'../outside'}));
  }finally{fs.rmSync(root,{recursive:true,force:true});}
});
