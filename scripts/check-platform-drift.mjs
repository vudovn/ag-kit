#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const manifestPath = path.join(root, 'platform-capabilities.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const findings = [];

function checkPath(platform, capability, target) {
  if (!target) return;
  const resolved = path.join(root, target);
  if (!fs.existsSync(resolved)) {
    findings.push(`${platform}.${capability}: missing ${target}`);
  }
}

for (const [platform, config] of Object.entries(manifest.platforms ?? {})) {
  for (const [capability, target] of Object.entries(config.paths ?? {})) {
    if (config[capability] === true) checkPath(platform, capability, target);
  }
}

const antigravity = manifest.platforms?.antigravity;
if (!antigravity || antigravity.tier !== 'first-class') {
  findings.push('antigravity: must remain first-class');
}

const expectedNative = {
  rules: '.agents/rules',
  skills: '.agents/skills',
  agents: '.agents/agents',
  hooks: '.agents/hooks.json',
  mcp: '.agents/mcp_config.json',
  plugins: '.agents/plugins'
};
for (const [key, expected] of Object.entries(expectedNative)) {
  if (antigravity?.paths?.[key] !== expected) {
    findings.push(`antigravity.${key}: expected ${expected}, found ${antigravity?.paths?.[key] ?? '<missing>'}`);
  }
}

if (findings.length) {
  console.error('Platform capability drift detected:');
  for (const finding of findings) console.error(`- ${finding}`);
  process.exitCode = 1;
} else {
  console.log('Platform capability manifest is internally consistent.');
}
