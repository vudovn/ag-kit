import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const MARKER_LABEL = "CORE";
const NO_MCP_TARGETS = new Set(["aider", "pi"]);
const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
const stateRoot = (root) => path.join(path.resolve(root), ".ag-kit");
const manifestsRoot = (root) => path.join(stateRoot(root), "runtime-installs");
const manifestFile = (root, runtime) => path.join(manifestsRoot(root), `${runtime}.json`);
const timestamp = () => new Date().toISOString().replace(/[:.]/g, "-");
const escapeRegex = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const specsByRuntime = {
  antigravity: [[".agents/skills", "tree"], [".agents/agents", "tree"], [".agents/rules/ag-kit-v2.md", "replace"], [".agents/mcp_config.json", "mcp-json"]],
  claude: [[".claude/skills", "tree"], [".claude/agents", "tree"], ["CLAUDE.md", "block"], [".mcp.json", "mcp-json"]],
  codex: [[".agents/skills", "tree"], ["AGENTS.md", "block"], [".codex-plugin", "tree"]],
  gemini: [[".gemini/skills", "tree"], ["GEMINI.md", "block"], [".gemini/settings.json", "mcp-json"]],
  qwen: [[".qwen/skills", "tree"], [".qwen/agents", "tree"], ["QWEN.md", "block"], [".qwen/settings.json", "mcp-json"]],
  kimi: [[".kimi-code/skills", "tree"], [".kimi-code/agents", "tree"], ["AGENTS.md", "block"], [".kimi-code/mcp.json", "mcp-json"]],
  cline: [[".cline/skills", "tree"], [".cline/rules/ag-kit.md", "block"], [".cline/mcp.json", "mcp-json"]],
  cursor: [[".cursor/rules/ag-kit.mdc", "replace"], [".cursor/mcp.json", "mcp-json"]],
  windsurf: [[".windsurfrules", "block"]],
  copilot: [[".github/copilot-instructions.md", "block"], [".mcp.json", "mcp-json"]],
  opencode: [["AGENTS.md", "block"]],
  openclaw: [["AGENTS.md", "block"]],
  aider: [["CONVENTIONS.md", "block"], [".aider.conf.yml", "replace"]],
  wayland: [[".ag-kit/integrations/wayland", "tree"]],
  hermes: [[".ag-kit/integrations/hermes", "tree"]],
  pi: [["AGENTS.md", "block"]],
};

const hash = (parts) => {
  const digest = crypto.createHash("sha256");
  for (const part of parts) digest.update(part);
  return digest.digest("hex");
};

const digestPath = (absolute) => {
  if (!fs.existsSync(absolute)) return { exists: false, type: null, digest: null };
  const stat = fs.lstatSync(absolute);
  if (stat.isSymbolicLink()) return { exists: true, type: "symlink", digest: hash(["symlink\0", fs.readlinkSync(absolute)]) };
  if (stat.isFile()) return { exists: true, type: "file", digest: hash(["file\0", fs.readFileSync(absolute)]) };
  if (!stat.isDirectory()) return { exists: true, type: "other", digest: hash(["other\0", String(stat.mode), String(stat.size)]) };
  const parts = [];
  const walk = (dir, prefix = "") => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { parts.push(`dir\0${rel}\0`); walk(full, rel); }
      else if (entry.isSymbolicLink()) parts.push(`link\0${rel}\0${fs.readlinkSync(full)}\0`);
      else if (entry.isFile()) parts.push(Buffer.concat([Buffer.from(`file\0${rel}\0`), fs.readFileSync(full), Buffer.from("\0")]));
      else parts.push(`other\0${rel}\0`);
    }
  };
  walk(absolute);
  return { exists: true, type: "directory", digest: hash(["directory\0", ...parts]) };
};

const copyPath = (from, to) => {
  if (!fs.existsSync(from)) return;
  ensureDir(path.dirname(to));
  fs.rmSync(to, { recursive: true, force: true });
  fs.cpSync(from, to, { recursive: true, force: true });
};

const removeManagedBlock = (file, label = MARKER_LABEL) => {
  if (!fs.existsSync(file) || !fs.lstatSync(file).isFile()) return { changed: false, removed: false };
  const start = `<!-- AG-KIT:${label}:START -->`;
  const end = `<!-- AG-KIT:${label}:END -->`;
  const regex = new RegExp(`\\n?${escapeRegex(start)}[\\s\\S]*?${escapeRegex(end)}\\n?`, "m");
  const previous = fs.readFileSync(file, "utf8");
  if (!regex.test(previous)) return { changed: false, removed: false };
  const next = previous.replace(regex, "\n").replace(/^\s+|\s+$/g, "");
  if (!next) { fs.rmSync(file, { force: true }); return { changed: true, removed: true }; }
  fs.writeFileSync(file, `${next}\n`);
  return { changed: true, removed: false };
};

const removeMcpEntry = (file) => {
  if (!fs.existsSync(file) || !fs.lstatSync(file).isFile()) return { changed: false, removed: false };
  let data;
  try { data = JSON.parse(fs.readFileSync(file, "utf8")); } catch { return { changed: false, removed: false, invalidJson: true }; }
  if (!data?.mcpServers || !("ag-kit" in data.mcpServers)) return { changed: false, removed: false };
  delete data.mcpServers["ag-kit"];
  if (Object.keys(data.mcpServers).length === 0) delete data.mcpServers;
  if (Object.keys(data).length === 0) { fs.rmSync(file, { force: true }); return { changed: true, removed: true }; }
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
  return { changed: true, removed: false };
};

const hasManagedBlock = (file, label = MARKER_LABEL) => {
  if (!fs.existsSync(file) || !fs.lstatSync(file).isFile()) return false;
  const body = fs.readFileSync(file, "utf8");
  return body.includes(`<!-- AG-KIT:${label}:START -->`) && body.includes(`<!-- AG-KIT:${label}:END -->`);
};

const hasMcpEntry = (file) => {
  try {
    const data = JSON.parse(fs.readFileSync(file, "utf8"));
    const entry = data?.mcpServers?.["ag-kit"];
    return Boolean(entry && entry.command === "ag-kit" && Array.isArray(entry.args) && entry.args[0] === "mcp" && entry.args[1] === "serve");
  } catch { return false; }
};

const runtimeSpecs = (runtime) => {
  const specs = specsByRuntime[runtime];
  if (!specs) throw new Error(`unsupported runtime lifecycle: ${runtime}`);
  return specs.map(([relativePath, strategy]) => ({ relativePath, strategy }));
};

export function prepareRuntimeInstall({ root = process.cwd(), runtime }) {
  const projectRoot = path.resolve(root);
  const id = `${runtime}-${timestamp()}`;
  const backupRoot = path.join(stateRoot(projectRoot), "install-backups", id);
  const entries = runtimeSpecs(runtime).map(({ relativePath, strategy }) => {
    const absolute = path.join(projectRoot, relativePath);
    const before = digestPath(absolute);
    const backup = before.exists ? path.join(backupRoot, "original", relativePath) : null;
    if (backup) copyPath(absolute, backup);
    return { relativePath, strategy, before, backup: backup ? path.relative(projectRoot, backup) : null };
  });
  return { schema: 1, id, runtime, root: projectRoot, preparedAt: new Date().toISOString(), backupRoot: path.relative(projectRoot, backupRoot), entries };
}

export function restorePreparedInstall(prepared) {
  const results = [];
  for (const entry of [...prepared.entries].reverse()) {
    const absolute = path.join(prepared.root, entry.relativePath);
    if (entry.before.exists && entry.backup) {
      copyPath(path.join(prepared.root, entry.backup), absolute);
      results.push({ path: entry.relativePath, action: "restored" });
    } else {
      fs.rmSync(absolute, { recursive: true, force: true });
      results.push({ path: entry.relativePath, action: "removed" });
    }
  }
  return { runtime: prepared.runtime, recovered: true, results };
}

export function finalizeRuntimeInstall({ prepared, mcp = null }) {
  const entries = prepared.entries.map((entry) => ({ ...entry, after: digestPath(path.join(prepared.root, entry.relativePath)) }));
  const manifest = {
    schema: 1,
    runtime: prepared.runtime,
    installedAt: new Date().toISOString(),
    backupRoot: prepared.backupRoot,
    mcp,
    entries,
  };
  ensureDir(manifestsRoot(prepared.root));
  fs.writeFileSync(manifestFile(prepared.root, prepared.runtime), `${JSON.stringify(manifest, null, 2)}\n`);
  return manifest;
}

const readManifest = (root, runtime) => {
  const file = manifestFile(root, runtime);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8"));
};

export function doctorRuntime({ root = process.cwd(), runtime }) {
  const projectRoot = path.resolve(root);
  const manifest = readManifest(projectRoot, runtime);
  if (!manifest) return { runtime, status: "untouched", checks: [], mcp: { status: "unknown" } };
  const checks = manifest.entries.map((entry) => {
    const absolute = path.join(projectRoot, entry.relativePath);
    const current = digestPath(absolute);
    let ok = false;
    let state = "missing";
    if (entry.strategy === "block") { ok = hasManagedBlock(absolute); state = ok ? "managed" : current.exists ? "drift" : "missing"; }
    else if (entry.strategy === "mcp-json") { ok = hasMcpEntry(absolute); state = ok ? "wired" : current.exists ? "drift" : "missing"; }
    else { ok = current.exists && current.digest === entry.after?.digest; state = ok ? "managed" : current.exists ? "drift" : "missing"; }
    return { path: entry.relativePath, strategy: entry.strategy, ok, state, expectedDigest: entry.after?.digest || null, currentDigest: current.digest };
  });
  const broken = checks.some((item) => !item.ok);
  const mcpExpected = !NO_MCP_TARGETS.has(runtime);
  const mcpStatus = manifest.mcp?.wired ? "wired" : mcpExpected ? "standing-by" : "not-applicable";
  const status = broken ? "degraded" : mcpStatus === "standing-by" ? "standing-by" : "live";
  return { runtime, status, checks, mcp: { status: mcpStatus, ...(manifest.mcp || {}) }, installedAt: manifest.installedAt };
}

export function doctorRuntimes({ root = process.cwd(), runtime = "" } = {}) {
  if (runtime) return doctorRuntime({ root, runtime });
  const dir = manifestsRoot(root);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((name) => name.endsWith(".json")).sort().map((name) => doctorRuntime({ root, runtime: name.slice(0, -5) }));
}

export function uninstallRuntime({ root = process.cwd(), runtime }) {
  const projectRoot = path.resolve(root);
  const manifest = readManifest(projectRoot, runtime);
  if (!manifest) return { runtime, status: "untouched", results: [] };
  const results = [];
  for (const entry of [...manifest.entries].reverse()) {
    const absolute = path.join(projectRoot, entry.relativePath);
    const current = digestPath(absolute);
    const unchanged = current.exists && current.digest === entry.after?.digest;
    const backup = entry.backup ? path.join(projectRoot, entry.backup) : null;
    if (entry.before?.exists && unchanged && backup && fs.existsSync(backup)) {
      copyPath(backup, absolute);
      results.push({ path: entry.relativePath, action: "restored-original" });
      continue;
    }
    if (!entry.before?.exists && unchanged) {
      fs.rmSync(absolute, { recursive: true, force: true });
      results.push({ path: entry.relativePath, action: "removed-managed" });
      continue;
    }
    if (entry.strategy === "block") {
      const result = removeManagedBlock(absolute);
      results.push({ path: entry.relativePath, action: result.changed ? "stripped-managed-block" : "preserved-drift", drift: !result.changed });
      continue;
    }
    if (entry.strategy === "mcp-json") {
      const result = removeMcpEntry(absolute);
      results.push({ path: entry.relativePath, action: result.changed ? "removed-mcp-entry" : "preserved-drift", drift: !result.changed });
      continue;
    }
    results.push({ path: entry.relativePath, action: "preserved-drift", drift: true });
  }
  const active = manifestFile(projectRoot, runtime);
  fs.rmSync(active, { force: true });
  const uninstalls = path.join(stateRoot(projectRoot), "runtime-uninstalls");
  ensureDir(uninstalls);
  const receipt = path.join(uninstalls, `${runtime}-${timestamp()}.json`);
  fs.writeFileSync(receipt, `${JSON.stringify({ schema: 1, runtime, uninstalledAt: new Date().toISOString(), memoryPreserved: true, results }, null, 2)}\n`);
  return { runtime, status: results.some((item) => item.drift) ? "uninstalled-with-preserved-drift" : "uninstalled", memoryPreserved: true, receipt: path.relative(projectRoot, receipt), results };
}
