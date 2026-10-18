#!/usr/bin/env node
import { isDirectRun } from '../cli/lib/direct-run.js';
export { auditRoster as roster, probeRoster, prepareAudit } from '../cli/lib/v2-engine.js';
export { snapshotAuditTarget, runConsensusAudit as runCrossAudit } from '../cli/lib/audit-consensus.js';
import { prepareAudit, parseArgs } from '../cli/lib/v2-engine.js';
import { runConsensusAudit } from '../cli/lib/audit-consensus.js';
if(isDirectRun(import.meta.url)){const a=parseArgs(process.argv.slice(2));const options={root:a.path||process.cwd(),target:a.target||a._[0]||'.'};const result=a.probe?prepareAudit(options):await runConsensusAudit({...options,reviewers:a.reviewers||3,excludeLineage:a['exclude-lineage']||process.env.AG_KIT_CALLING_LINEAGE||''});console.log(JSON.stringify(result,null,2));}
