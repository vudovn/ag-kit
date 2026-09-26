#!/usr/bin/env node
export { auditRoster as roster, probeRoster, prepareAudit, snapshotAuditTarget, runCrossAudit } from '../cli/lib/v2-engine.js';
import { prepareAudit, runCrossAudit, parseArgs } from '../cli/lib/v2-engine.js';
if(import.meta.url===`file://${process.argv[1]}`){const a=parseArgs(process.argv.slice(2));const options={root:a.path||process.cwd(),target:a.target||a._[0]||'.'};console.log(JSON.stringify(a.probe?prepareAudit(options):runCrossAudit({...options,reviewers:a.reviewers||2}),null,2));}
