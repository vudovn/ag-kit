#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const fail = (message) => failures.push(message);
const failures = [];
const read = (relative) => fs.readFileSync(path.join(root, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));

const packageFiles = ["package.json", "cli/package.json", "web/package.json"];
const scripts = new Set();
for (const file of packageFiles) {
  if (!fs.existsSync(path.join(root, file))) continue;
  for (const name of Object.keys(readJson(file).scripts || {})) scripts.add(name);
}

const docs = [
  "README.md",
  "README-VI.md",
  "AGENTS.md",
  "CLAUDE.md",
  "MIGRATION.md",
  "SECURITY.md",
  "PRODUCTION_CHECKLIST.md",
  "AGENT_FLOW.md",
  ".github/RELEASE_SETUP.md",
];

const visitMarkdown = (relative) => {
  const absolute = path.join(root, relative);
  if (!fs.existsSync(absolute)) return [];
  const stat = fs.statSync(absolute);
  if (stat.isFile()) return absolute.endsWith(".md") ? [relative] : [];
  const rows = [];
  for (const entry of fs.readdirSync(absolute, { withFileTypes: true })) {
    const child = path.join(relative, entry.name);
    if (entry.isDirectory()) rows.push(...visitMarkdown(child));
    else if (entry.name.endsWith(".md")) rows.push(child);
  }
  return rows;
};

docs.push(...visitMarkdown("docs"));

for (const file of [...new Set(docs)]) {
  if (!fs.existsSync(path.join(root, file))) continue;
  const body = read(file);

  for (const match of body.matchAll(/\bnpm\s+run\s+([a-zA-Z0-9:_-]+)/g)) {
    const name = match[1];
    if (!scripts.has(name)) fail(`${file}: documents unknown npm script ${name}`);
  }

  for (const match of body.matchAll(/\bnode\s+((?:\.?\.?\/|[a-zA-Z0-9_.-]+\/)[^\s`'"<>]+\.m?js)\b/g)) {
    const candidate = match[1];
    if (candidate.includes("<") || candidate.includes(">")) continue;
    const resolved = path.resolve(root, candidate);
    if (!resolved.startsWith(`${root}${path.sep}`) || !fs.existsSync(resolved)) fail(`${file}: documents missing Node entrypoint ${candidate}`);
  }
}

const workflowDir = path.join(root, ".github", "workflows");
const actualGates = new Set();
if (fs.existsSync(workflowDir)) {
  for (const name of fs.readdirSync(workflowDir).filter((item) => /\.ya?ml$/.test(item))) {
    const body = fs.readFileSync(path.join(workflowDir, name), "utf8");
    const workflowName = body.match(/^name:\s*["']?([^"'\n]+)["']?\s*$/m)?.[1]?.trim();
    if (!workflowName) continue;
    actualGates.add(workflowName);
    for (const match of body.matchAll(/^\s{4}name:\s*["']?([^"'\n]+)["']?\s*$/gm)) actualGates.add(`${workflowName} / ${match[1].trim()}`);
  }
}

const checklist = read("PRODUCTION_CHECKLIST.md");
const requiredSection = checklist.split("## Required GitHub gates")[1] || "";
const documentedGates = [...requiredSection.matchAll(/^- \[ \] \*\*(.+?)\*\*/gm)].map((match) => match[1].trim());
if (!documentedGates.length) fail("PRODUCTION_CHECKLIST.md: no required GitHub gates found");
for (const gate of documentedGates) if (!actualGates.has(gate)) fail(`PRODUCTION_CHECKLIST.md: required gate does not exist: ${gate}`);

const ci = read(".github/workflows/ci.yml");
const benchmarkContract = [
  ["npm run benchmark:v2 -- --output dist/evidence/benchmark-v2.json", "benchmark command"],
  ["dist/evidence/benchmark-v2.json", "benchmark receipt path"],
  ["if-no-files-found: error", "artifact missing-file failure policy"],
];
for (const [needle, label] of benchmarkContract) if (!ci.includes(needle)) fail(`CI benchmark evidence missing ${label}`);
if (!/actions\/upload-artifact@[0-9a-f]{40}/.test(ci)) fail("CI benchmark artifact action must be pinned to a 40-character commit SHA");

if (failures.length) {
  console.error(`AG Kit docs claims: ${failures.length} drift issue(s)`);
  for (const issue of failures) console.error(`- ${issue}`);
  process.exitCode = 1;
} else {
  console.log(`AG Kit docs claims OK: ${new Set(docs).size} documentation surfaces, ${scripts.size} package scripts, ${documentedGates.length} required GitHub gates, benchmark evidence contract verified.`);
}
