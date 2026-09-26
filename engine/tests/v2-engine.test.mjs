import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { addMemory, recallMemory, memoryStatus } from '../memory.mjs';
import { initTeam } from '../team.mjs';

const temp = () => fs.mkdtempSync(path.join(os.tmpdir(),'ag-kit-v2-'));

test('memory keeps markdown canonical and recalls matching entries', () => {
  const root=temp();
  addMemory({root,text:'Use PostgreSQL transactions for billing writes',kind:'decision',title:'Billing DB'});
  addMemory({root,text:'Frontend uses accessible semantic HTML',kind:'convention'});
  const hit=recallMemory({root,query:'billing PostgreSQL'});
  assert.equal(hit.length,1);
  assert.match(hit[0].preview,/PostgreSQL/);
  assert.equal(memoryStatus(root).canonical,'markdown');
  fs.rmSync(root,{recursive:true,force:true});
});

test('team assembly writes a project-local role bench', () => {
  const root=temp();
  fs.writeFileSync(path.join(root,'package.json'),'{}');
  const team=initTeam({root,archetype:'auto',name:'app'});
  assert.equal(team.archetype,'software');
  assert.ok(fs.existsSync(path.join(root,'.ag-kit','agents','architect.md')));
  assert.ok(team.roles.length>=3);
  fs.rmSync(root,{recursive:true,force:true});
});
