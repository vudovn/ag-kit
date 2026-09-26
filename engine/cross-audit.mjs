#!/usr/bin/env node
export { auditRoster as roster, probeRoster, prepareAudit } from '../cli/lib/v2-engine.js';
import { prepareAudit, parseArgs } from '../cli/lib/v2-engine.js';
if (import.meta.url === `file://${process.argv[1]}`) { const a=parseArgs(process.argv.slice(2)); console.log(JSON.stringify(prepareAudit({root:a.path||process.cwd(),target:a.target||a._[0]||'.'}),null,2)); }
