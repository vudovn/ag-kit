#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const roots = [
  "README.md",
  "README-VI.md",
  "MIGRATION.md",
  "SECURITY.md",
  "PRODUCTION_CHECKLIST.md",
  "AGENT_FLOW.md",
  "docs",
];
const ignoredDirs = new Set(["node_modules", ".git", ".next", "dist", "coverage"]);

const markdownFiles = [];
const visit = (absolute) => {
  if (!fs.existsSync(absolute)) return;
  const stat = fs.statSync(absolute);
  if (stat.isFile()) {
    if (absolute.endsWith(".md")) markdownFiles.push(absolute);
    return;
  }
  for (const entry of fs.readdirSync(absolute, { withFileTypes: true })) {
    if (entry.isDirectory() && ignoredDirs.has(entry.name)) continue;
    visit(path.join(absolute, entry.name));
  }
};
for (const item of roots) visit(path.join(root, item));

const linkPattern = /!?\[[^\]]*\]\(([^)]+)\)/g;
const failures = [];
const stripTitle = (raw) => {
  const value = raw.trim();
  if (value.startsWith("<") && value.includes(">")) return value.slice(1, value.indexOf(">"));
  const match = value.match(/^(\S+)(?:\s+["'][^"']*["'])?$/);
  return match ? match[1] : value;
};

const isExternalOrRoute = (target) => {
  if (!target || target.startsWith("#") || target.startsWith("/")) return true;
  return /^(?:https?:|mailto:|tel:|data:|javascript:)/i.test(target);
};

for (const file of markdownFiles) {
  const body = fs.readFileSync(file, "utf8");
  for (const match of body.matchAll(linkPattern)) {
    const target = stripTitle(match[1]);
    if (isExternalOrRoute(target)) continue;
    const withoutFragment = target.split("#", 1)[0].split("?", 1)[0];
    if (!withoutFragment) continue;
    let decoded;
    try { decoded = decodeURIComponent(withoutFragment); }
    catch { decoded = withoutFragment; }
    const resolved = path.resolve(path.dirname(file), decoded);
    if (!fs.existsSync(resolved)) {
      failures.push({
        file: path.relative(root, file),
        target,
        resolved: path.relative(root, resolved),
      });
    }
  }
}

if (failures.length) {
  console.error(`AG Kit docs: ${failures.length} broken local link(s)`);
  for (const failure of failures) console.error(`- ${failure.file}: ${failure.target} -> ${failure.resolved}`);
  process.exitCode = 1;
} else {
  console.log(`AG Kit docs OK: checked ${markdownFiles.length} Markdown files for local link integrity.`);
}
