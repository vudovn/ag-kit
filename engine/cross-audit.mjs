#!/usr/bin/env node
export { auditRoster as roster, probeRoster, prepareAudit } from '../cli/lib/v2-engine.js';
export { snapshotAuditTarget, runConsensusAudit as runCrossAudit } from '../cli/lib/audit-consensus.js';
import { prepareAudit, parseArgs } from '../cli/lib/v2-engine.js';
import { runConsensusAudit } from '../cli/lib/audit-consensus.js';
if(import.meta.url===`file://${process.argv[1]}`){const a=parseArgs(process.argv.slice(2));const options={root:a.path||process.cwd(),target:a.target||a._[0]||'.'};console.log(JSON.stringify(a.probe?prepareAudit(options):runConsensusAudit({...options,reviewers:a.reviewers||3,excludeLineage:a['exclude-lineage']||process.env.AG_KIT_CALLING_LINEAGE||''}),null,2));}
