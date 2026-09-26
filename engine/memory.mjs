#!/usr/bin/env node
export { initMemory, addMemory, recallMemory, memoryStatus } from '../cli/lib/v2-engine.js';
import { initMemory, addMemory, recallMemory, memoryStatus, parseArgs } from '../cli/lib/v2-engine.js';
if (import.meta.url === `file://${process.argv[1]}`) {
  const args=parseArgs(process.argv.slice(2)); const [cmd,...rest]=args._; const root=args.path||process.cwd();
  if(cmd==='init') console.log(initMemory(root));
  else if(cmd==='add') console.log(JSON.stringify(addMemory({root,text:rest.join(' '),kind:args.kind||'learning',title:args.title||''}),null,2));
  else if(cmd==='recall') console.log(JSON.stringify(recallMemory({root,query:rest.join(' '),limit:args.limit||5}),null,2));
  else if(cmd==='status') console.log(JSON.stringify(memoryStatus(root),null,2));
  else { console.error('Usage: memory <init|add|recall|status>'); process.exitCode=1; }
}
