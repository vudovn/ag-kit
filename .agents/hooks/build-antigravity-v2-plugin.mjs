#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const options = { root: process.cwd(), output: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--root') options.root = path.resolve(argv[++i]);
    else if (argv[i] === '--output') options.output = path.resolve(argv[++i]);
    else throw new Error(`Unknown argument: ${argv[i]}`);
  }
  options.output ??= path.join(options.root, 'dist', 'antigravity-plugin');
  return options;
}

function copyTree(source, destination) {
  if (!fs.existsSync(source)) return 0;
  fs.cpSync(source, destination, { recursive: true });
  let count = 0;
  const visit = dir => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(full);
      else count += 1;
    }
  };
  visit(source);
  return count;
}

function frontmatterDescription(text) {
  if (!text.startsWith('---\n')) return '';
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return '';
  const line = text.slice(4, end).split(/\r?\n/).find(item => item.startsWith('description:'));
  return line ? line.slice('description:'.length).trim().replace(/^['"]|['"]$/g, '') : '';
}

function convertWorkflows(root, output) {
  const source = path.join(root, '.agents', 'workflows');
  const commandsDest = path.join(output, 'commands');
  const skillsDest = path.join(output, 'skills');
  fs.mkdirSync(commandsDest, { recursive: true });

  let count = 0;
  for (const name of fs.readdirSync(source).filter(item => item.endsWith('.md')).sort()) {
    const text = fs.readFileSync(path.join(source, name), 'utf8');
    const commandName = name.replace(/\.md$/, '');
    const description = frontmatterDescription(text) || `Run AG Kit workflow ${commandName}`;

    // 1. commands/*.md (단일 표준 마크다운 커맨드)
    fs.writeFileSync(path.join(commandsDest, `${commandName}.md`), text, 'utf8');

    // 2. skills/<workflow>/SKILL.md (온디맨드 스킬로도 동시 등록)
    const skillDir = path.join(skillsDest, commandName);
    fs.mkdirSync(skillDir, { recursive: true });
    let skillContent = text;
    if (!skillContent.startsWith('---\n')) {
      skillContent = `---\nname: ${commandName}\ndescription: ${description}\n---\n\n${text}`;
    }
    fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent, 'utf8');

    count += 1;
  }
  return count;
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function inventory(output) {
  const files = [];
  const visit = dir => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(full);
      else files.push({ path: path.relative(output, full).split(path.sep).join('/'), sha256: sha256(full) });
    }
  };
  visit(output);
  return files;
}

export function buildAntigravity2Plugin(root, output) {
  fs.rmSync(output, { recursive: true, force: true });
  fs.mkdirSync(output, { recursive: true });

  const version = fs.readFileSync(path.join(root, '.agents', 'VERSION'), 'utf8').trim();

  // 1. Antigravity 2.0 공식 표준 plugin.json 생성
  const pluginManifest = {
    name: 'ag-kit',
    version,
    description: 'Antigravity-first agent engineering kit with rules, skills, workflows, orchestration, MCP guidance, and safety hooks.',
    skills: './skills/',
    rules: './rules/',
    commands: './commands/',
    hooks: './hooks.json'
  };
  fs.writeFileSync(path.join(output, 'plugin.json'), `${JSON.stringify(pluginManifest, null, 2)}\n`, 'utf8');

  // 2. 진입점 GEMINI.md 복사
  fs.copyFileSync(path.join(root, '.agents', 'hooks', 'plugin', 'GEMINI.md'), path.join(output, 'GEMINI.md'));

  // 3. Skills 복사 및 Workflows 변환 (중복 없는 13개 커맨드 및 60개 스킬)
  const skillsCount = copyTree(path.join(root, '.agents', 'skills'), path.join(output, 'skills'));
  const workflowsCount = convertWorkflows(root, output);
  const agentsCount = copyTree(path.join(root, '.agents', 'agent'), path.join(output, 'agents'));
  const rulesCount = copyTree(path.join(root, '.agents', 'rules'), path.join(output, 'rules'));

  // 4. Hooks 설정 (루트 hooks.json 및 권한 부여)
  const hooksConfig = {
    $schema: 'antigravity-hooks.schema.json',
    enabled: true,
    PreToolUse: [
      {
        matcher: 'run_command',
        command: 'node /Users/gwkang/.gemini/config/plugins/ag-kit/hooks/validate-tool-call.mjs',
        timeout: 10
      }
    ]
  };
  fs.writeFileSync(path.join(output, 'hooks.json'), `${JSON.stringify(hooksConfig, null, 2)}\n`, 'utf8');

  fs.mkdirSync(path.join(output, 'hooks'), { recursive: true });
  fs.copyFileSync(path.join(root, '.agents', 'hooks', 'validate-tool-call.mjs'), path.join(output, 'hooks', 'validate-tool-call.mjs'));
  fs.chmodSync(path.join(output, 'hooks', 'validate-tool-call.mjs'), 0o755);

  const manifest = {
    name: 'ag-kit',
    version,
    runtime: 'antigravity-2.0',
    counts: {
      skills: fs.readdirSync(path.join(output, 'skills')).length,
      agents: agentsCount,
      rules: rulesCount,
      commands: fs.readdirSync(path.join(output, 'commands')).filter(f => f.endsWith('.md')).length
    },
    files: inventory(output)
  };
  fs.writeFileSync(path.join(output, 'PLUGIN_CONTENTS.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  return manifest;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const options = parseArgs(process.argv.slice(2));
    const manifest = buildAntigravity2Plugin(options.root, options.output);
    console.log(`Successfully built Antigravity 2.0 plugin: ${options.output}`);
    console.log(JSON.stringify(manifest.counts, null, 2));
  } catch (error) {
    console.error(`Plugin build failed: ${error.message}`);
    process.exitCode = 1;
  }
}
