#!/usr/bin/env node
import { isDirectRun } from '../cli/lib/direct-run.js';
export { runCurrentPreflight as runPreflight } from '../cli/lib/preflight.js';
import { runCurrentPreflight } from '../cli/lib/preflight.js';
import { parseArgs } from '../cli/lib/v2-engine.js';
if(isDirectRun(import.meta.url)){const a=parseArgs(process.argv.slice(2));const r=runCurrentPreflight(a.path||process.cwd());for(const x of r.results)console.log(`${x.ok?'PASS':'FAIL'} ${x.name} ${x.durationMs}ms`);if(!r.passed)process.exitCode=1;}
