#!/usr/bin/env node
import { isDirectRun } from '../cli/lib/direct-run.js';
export { inferArchetype, initTeam } from '../cli/lib/v2-engine.js';
import { initTeam, parseArgs } from '../cli/lib/v2-engine.js';
if(isDirectRun(import.meta.url)) { const a=parseArgs(process.argv.slice(2)); if(a._[0]!=='init'){console.error('Usage: team init');process.exitCode=1;} else console.log(JSON.stringify(initTeam({root:a.path||process.cwd(),archetype:a.archetype||'auto',name:a.name||'default',brief:a.brief||''}),null,2)); }
