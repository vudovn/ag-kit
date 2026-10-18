#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {pathToFileURL} from 'node:url';

const BLOCK_RULES = [
  {
    id: 'unix-root-delete',
    pattern: /(?:^|[;&|]\s*)(?:sudo\s+)?rm\s+(?:-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*|-[A-Za-z]*f[A-Za-z]*r[A-Za-z]*)\s+(?:--\s+)?\/(?:\*|\s|$)/i,
    message: 'recursive deletion of the filesystem root'
  },
  {
    id: 'filesystem-format',
    pattern: /(?:^|[;&|]\s*)(?:sudo\s+)?mkfs(?:\.[A-Za-z0-9_-]+)?\b/i,
    message: 'filesystem formatting command'
  },
  {
    id: 'raw-disk-overwrite',
    pattern: /\bdd\b[^\n]*\bof=\/dev\/(?:sd|nvme|vd|xvd)[A-Za-z0-9_-]*/i,
    message: 'raw disk overwrite'
  },
  {
    id: 'windows-drive-format',
    pattern: /(?:^|[;&|]\s*)format(?:\.com)?\s+[A-Za-z]:/i,
    message: 'Windows drive format'
  },
  {
    id: 'windows-root-delete',
    pattern: /remove-item\b[^\n]*-(?:recurse|r)\b[^\n]*-(?:force|fo)\b[^\n]*(?:[A-Za-z]:\\(?:\s|$)|[A-Za-z]:\\\*)/i,
    message: 'recursive deletion of a Windows drive root'
  }
];

async function readStdin() {
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
    if (input.length > 1024 * 1024) throw new Error('hook payload exceeds 1 MiB');
  }
  return input;
}

function firstString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
}

export function extractCommand(payload) {
  const args = payload?.toolCall?.args ?? payload?.tool_args ?? payload?.toolArgs ?? payload?.arguments ?? {};
  return firstString(
    args.CommandLine,
    args.commandLine,
    args.command,
    args.cmd,
    payload?.command,
    payload?.cmd
  );
}

export function evaluateCommand(command) {
  for (const rule of BLOCK_RULES) {
    if (rule.pattern.test(command)) {
      return {allowed: false, rule: rule.id, reason: rule.message};
    }
  }
  return {allowed: true, rule: null, reason: 'no destructive command pattern matched'};
}

export function hookDecision(payload) {
  const command = extractCommand(payload);
  if (!command) {
    return {decision: 'allow', reason: 'AG Kit safety gate: no command payload detected.'};
  }

  const result = evaluateCommand(command);
  if (!result.allowed) {
    return {decision: 'deny', reason: `AG Kit blocked ${result.rule}: ${result.reason}.`};
  }

  return {decision: 'allow', reason: 'AG Kit safety gate: command passed destructive-operation checks.'};
}

async function main() {
  let raw;
  try {
    raw = await readStdin();
  } catch (error) {
    console.log(JSON.stringify({decision: 'force_ask', reason: `AG Kit could not read the hook payload: ${error.message}`}));
    return;
  }

  let payload;
  try {
    payload = JSON.parse(raw || '{}');
  } catch {
    console.log(JSON.stringify({decision: 'force_ask', reason: 'AG Kit received invalid hook JSON; manual approval required.'}));
    return;
  }

  console.log(JSON.stringify(hookDecision(payload)));
}

const resolveEntryHref = (entry) => {
  try {
    return pathToFileURL(fs.realpathSync(path.resolve(entry))).href;
  } catch {
    return null;
  }
};

const isDirectRun = process.argv[1] && resolveEntryHref(process.argv[1]) === import.meta.url;
if (isDirectRun) await main();
