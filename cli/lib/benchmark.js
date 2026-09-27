import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory, recallEvolvingMemory } from "./memory-evolution.js";
import { compactMarkdown } from "./context-artifacts.js";
import { routeTask } from "./efficiency.js";
import { installRuntimeTarget } from "./runtime-registry.js";
import { doctorRuntime, finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "./runtime-lifecycle.js";
import { ensureDir, resolveSafeProjectRoot, stateRoot } from "./project-state.js";
import { traceFields } from "./trace-context.js";

const stamp = () => new Date().toISOString().replace(/[:.]/g, "-");
const benchmarkDir = (root) => path.join(stateRoot(root), "benchmarks");
const bytes = (value) => Buffer.byteLength(String(value));
const tempProject = () => fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-bench-"));

const benchmarkMemory = () => {
  const root = tempProject();
  try {
    addEvolvingMemory({ root, text: "Runtime adapters must never silently mutate user-global configuration.", title: "Runtime safety", kind: "decision", session: "bench", durable: true });
    addEvolvingMemory({ root, text: "Markdown is the canonical memory store; indexes must remain rebuildable.", title: "Memory source of truth", kind: "architecture", session: "bench", durable: true });
    addEvolvingMemory({ root, text: "Cross-audit reviewers receive read-only snapshots without a writable repository mount.", title: "Audit isolation", kind: "security", session: "bench", durable: true });
    const cases = [
      ["user-global configuration", "Runtime safety"],
      ["canonical memory store", "Memory source of truth"],
      ["read-only snapshots", "Audit isolation"],
    ];
    const results = cases.map(([query, expectedTitle]) => {
      const recalled = recallEvolvingMemory({ root, query, limit: 3, session: "benchmark" });
      const hit = recalled.some((item) => String(item.title || item.preview || "").includes(expectedTitle) || String(item.text || "").includes(expectedTitle));
      return { query, expectedTitle, hit, count: recalled.length };
    });
    const hits = results.filter((item) => item.hit).length;
    return { name: "memory-recall", passed: hits === results.length, score: hits / results.length, cases: results };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

const benchmarkRouting = () => {
  const root = tempProject();
  try {
    const cases = [
      { task: "find docs for the runtime adapter", role: "scout", mode: "quick" },
      { task: "review security regression risk", role: "reviewer", mode: "standard" },
      { task: "architecture migration across runtime platforms", role: "architect", mode: "deep" },
      { task: "implement the settings form", role: "builder", mode: "standard" },
    ];
    const results = cases.map((item) => {
      const actual = routeTask(item.task, root);
      return { ...item, actualRole: actual.role, actualMode: actual.mode, hit: actual.role === item.role && actual.mode === item.mode };
    });
    const hits = results.filter((item) => item.hit).length;
    return { name: "routing", passed: hits === results.length, score: hits / results.length, cases: results };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

const benchmarkCompression = () => {
  const input = `# Release plan\n\n\nThis   paragraph explains the release goal.\nIt continues on another line and should compact safely.\n\nThis paragraph is duplicated.\n\nThis paragraph is duplicated.\n\n- Keep memory local-first\n- Keep runtime adapters thin\n\n\`\`\`js\nconst invariant = "evidence beats claims";\nconsole.log(invariant);\n\`\`\`\n`;
  const output = compactMarkdown(input);
  const before = bytes(input);
  const after = bytes(output);
  const anchors = ["# Release plan", "Keep memory local-first", "const invariant = \"evidence beats claims\";"];
  const anchorsPreserved = anchors.every((anchor) => output.includes(anchor));
  const reduced = after < before;
  return { name: "compression", passed: reduced && anchorsPreserved, bytesBefore: before, bytesAfter: after, bytesSaved: Math.max(0, before - after), reductionPct: before ? Number((((before - after) / before) * 100).toFixed(1)) : 0, anchorsPreserved };
};

const minimalSource = (root) => {
  const source = path.join(root, "source");
  ensureDir(path.join(source, "shared", "core"));
  ensureDir(path.join(source, "shared", "flows"));
  ensureDir(path.join(source, "packs"));
  fs.writeFileSync(path.join(source, "shared", "core", "CORE.md"), "# AG Kit Core\n\nEvidence beats completion claims.\n");
  return source;
};

const benchmarkLifecycle = () => {
  const workspace = tempProject();
  const target = path.join(workspace, "project");
  fs.mkdirSync(target, { recursive: true });
  fs.writeFileSync(path.join(target, "package.json"), "{\"name\":\"ag-kit-benchmark-project\"}\n");
  const source = minimalSource(workspace);
  try {
    const prepared = prepareRuntimeInstall({ root: target, runtime: "pi" });
    installRuntimeTarget({ sourceRoot: source, targetRoot: target, runtime: "pi" });
    finalizeRuntimeInstall({ prepared, mcp: { wired: false, reason: "not-applicable" } });
    const installed = doctorRuntime({ root: target, runtime: "pi" });
    const removed = uninstallRuntime({ root: target, runtime: "pi" });
    const after = doctorRuntime({ root: target, runtime: "pi" });
    const passed = installed.status === "live" && removed.status === "uninstalled" && after.status === "untouched";
    return { name: "runtime-lifecycle", passed, installStatus: installed.status, uninstallStatus: removed.status, finalStatus: after.status, checks: installed.checks.length };
  } finally { fs.rmSync(workspace, { recursive: true, force: true }); }
};

export function runLocalBenchmarks({ root = process.cwd(), write = true } = {}) {
  const project = resolveSafeProjectRoot(root);
  const started = Date.now();
  const benchmarks = [benchmarkMemory(), benchmarkRouting(), benchmarkCompression(), benchmarkLifecycle()];
  const report = {
    schema: 1,
    ts: new Date().toISOString(),
    ...traceFields(project),
    methodology: "Deterministic local fixtures only. No network/model benchmark and no synthetic token-savings claim.",
    passed: benchmarks.every((item) => item.passed),
    durationMs: Date.now() - started,
    benchmarks,
  };
  if (!write) return report;
  const dir = benchmarkDir(project);
  ensureDir(dir);
  const file = path.join(dir, `${stamp()}-local.json`);
  fs.writeFileSync(file, `${JSON.stringify(report, null, 2)}\n`);
  fs.writeFileSync(path.join(dir, "latest.json"), `${JSON.stringify(report, null, 2)}\n`);
  return { ...report, receipt: path.relative(project, file).split(path.sep).join("/") };
}
