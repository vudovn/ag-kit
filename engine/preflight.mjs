#!/usr/bin/env node
export { runPreflight } from '../cli/lib/v2-engine.js';
import { runPreflight, parseArgs } from '../cli/lib/v2-engine.js';
if (import.meta.url === `file://${process.argv[1]}`) { const a=parseArgs(process.argv.slice(2)); const r=runPreflight({root:a.path||process.cwd()}); for(const x of r.results) console.log(`${x.ok?'PASS':'FAIL'} ${x.name} ${x.durationMs}ms`); if(!r.passed) process.exitCode=1; }
