#!/usr/bin/env node

import process from 'node:process';

const BLOCK_RULES = [
  {id: 'unix-root-delete', pattern: /(?:^|[;&|]\s*)(?:sudo\s+)?rm\s+(?:-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*|-[A-Za-z]*f[A-Za-z]*r[A-Za-z]*)\s+(?:--\s+)?\/(?:\*|\s|$)/i, message: 'recursive deletion of the filesystem root'},
  {id: 'filesystem-format', pattern: /(?:^|[;&|]\s*)(?:sudo\s+)?mkfs(?:\.[A-Za-z0-9_-]+)?\b/i, message: 'filesystem formatting command'},
  {id: 'raw-disk-overwrite', pattern: /\bdd\b[^\n]*\bof=\/dev\/(?:sd|nvme|vd|xvd)[A-Za-z0-9_-]*/i, message: 'raw disk overwrite'},
  {id: 'windows-drive-format', pattern: /(?:^|[;&|]\s*)format(?:\.com)?\s+[A-Za-z]:/i, message: 'Windows drive format'},
  {id: 'windows-root-delete', pattern: /remove-item\b[^\n]*-(?:recurse|r)\b[^\n]*-(?:force|fo)\b[^\n]*(?:[A-Za-z]:\\(?:\s|$)|[A-Za-z]:\\\*)/i, message: 'recursive deletion of a Windows drive root'}
];

function readStdin() {
  return new Promise((resolve, reject) => {
    let input = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => {
      input += chunk;
      if (input.length > 1024 * 1024) reject(new Error('hook payload exceeds 1 MiB'));
    });
    process.stdin.on('end', () => resolve(input));
    process.stdin.on('error', reject);
  });
}

function firstString(...values) {
  return values.find(value => typeof value === 'string' && value.trim())?.trim() ?? '';
}

export function extractCommand(payload) {
  const nativeArgs = payload?.toolCall?.args ?? {};
  const legacyArgs = payload?.tool_args ?? payload?.toolArgs ?? payload?.arguments ?? {};
  return firstString(
    nativeArgs.CommandLine,
    nativeArgs.commandLine,
    nativeArgs.command,
    nativeArgs.cmd,
    legacyArgs.CommandLine,
    legacyArgs.commandLine,
    legacyArgs.command,
    legacyArgs.cmd,
    payload?.command,
    payload?.cmd
  );
}

export function evaluateCommand(command) {
  for (const rule of BLOCK_RULES) {
    if (rule.pattern.test(command)) return {decision: 'deny', rule: rule.id, reason: rule.message};
  }
  return {decision: 'allow', rule: null, reason: 'Command passed the destructive-operation gate.'};
}

export function decisionForPayload(payload) {
  const command = extractCommand(payload);
  if (!command) return {decision: 'allow', reason: 'No command payload was present.'};
  const result = evaluateCommand(command);
  return result.decision === 'deny'
    ? {decision: 'deny', reason: `AG Kit blocked ${result.reason}.`}
    : {decision: 'allow', reason: result.reason};
}

async function main() {
  try {
    const raw = await readStdin();
    const payload = JSON.parse(raw || '{}');
    process.stdout.write(`${JSON.stringify(decisionForPayload(payload))}\n`);
    return 0;
  } catch (error) {
    process.stdout.write(`${JSON.stringify({decision: 'ask', reason: `AG Kit could not validate the tool call: ${error.message}`})}\n`);
    return 0;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) process.exitCode = await main();
