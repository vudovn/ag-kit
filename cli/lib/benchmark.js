import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { addEvolvingMemory, recallEvolvingMemory, supersedeMemory } from "./memory-evolution.js";
import { routeTask } from "./efficiency.js";
import { compressArtifact } from "./context-artifacts.js";
import { doctorRuntime, finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "./runtime-lifecycle.js";
import { ensureDir, stateRoot } from "./project-state.js";

const stamp = () => new Date().toISOString().replace(/[:.]/g, "-");
const tempRoot = (label) => fs.mkdtempSync(path.join(os.tmpdir(), `ag-kit-bench-${label}-`));
const timed = async (name, fn) => {
  const started = Date.now();
  try {
    const evidence = await fn();
    return { name, passed: true, durationMs: Date.now() - started, evidence };
  } catch (error) {
    return { name, passed: false, durationMs: Date.now() - started, error: String(error?.message || error) };
  }
};
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const benchmarkMemory = async () => {
  const root = tempRoot("memory");
  try {
    const first = addEvolvingMemory({ root, text: "Use pnpm for workspace package management #tooling", kind: "convention", title: "Package manager", session: "bench-1", durable: true });
    const recalled = recallEvolvingMemory({ root, query: "pnpm workspace", limit: 3, session: "bench-2" });
    assert(recalled.some((item) => item.id === first.id), "memory recall did not return the inserted durable fact");
    const replacement = supersedeMemory({ root, id: first.id, text: "Use pnpm with frozen lockfile in CI #tooling", kind: "convention", title: "Package manager", session: "bench-3" });
    const after = recallEvolvingMemory({ root, query: "frozen lockfile", limit: 3, session: "bench-4" });
    assert(after.some((item) => item.id === replacement.replacement.id), "memory recall did not return the superseding fact");
    assert(!after.some((item) => item.id === first.id), "superseded memory remained active in temporal recall");
    return { inserted: first.id, supersededBy: replacement.replacement.id, recallHits: recalled.length, replacementHits: after.length, relations: first.relations };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

const benchmarkRouting = async () => {
  const root = tempRoot("routing");
  try {
    const architecture = routeTask("Design a cross-runtime production migration architecture", root);
    const research = routeTask("Research docs and inspect the repository", root);
    assert(architecture.role === "architect" && architecture.effort === "high" && architecture.mode === "deep", "architecture routing contract drifted");
    assert(research.role === "scout" && research.mode === "quick", "research routing contract drifted");
    return { architecture: { role: architecture.role, effort: architecture.effort, mode: architecture.mode }, research: { role: research.role, effort: research.effort, mode: research.mode } };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

const benchmarkCompression = async () => {
  const root = tempRoot("compression");
  try {
    const source = path.join(root, "context.md");
    const original = "# Context\n\nThis   paragraph   has   extra    spacing.\nIt continues on another line.\n\n\n- keep this item\n- keep this item\n\n```js\nconst value =   1;\n```\n";
    fs.writeFileSync(source, original);
    const result = compressArtifact({ root, file: "context.md" });
    assert(result.bytesSaved > 0 && result.bytesAfter < result.bytesBefore, "compression did not produce a measured byte reduction");
    assert(fs.readFileSync(source, "utf8") === original, "non-destructive compression modified the source artifact");
    assert(fs.existsSync(path.join(root, result.destination)), "compressed artifact was not written");
    return { bytesBefore: result.bytesBefore, bytesAfter: result.bytesAfter, bytesSaved: result.bytesSaved, reductionPct: result.reductionPct, sourcePreserved: true };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

const benchmarkLifecycle = async () => {
  const root = tempRoot("lifecycle");
  try {
    fs.writeFileSync(path.join(root, "CONVENTIONS.md"), "User-owned preface\n");
    const prepared = prepareRuntimeInstall({ root, runtime: "aider" });
    fs.writeFileSync(path.join(root, "CONVENTIONS.md"), "User-owned preface\n\n<!-- AG-KIT:CORE:START -->\nAG Kit managed block\n<!-- AG-KIT:CORE:END -->\n");
    fs.writeFileSync(path.join(root, ".aider.conf.yml"), "read: CONVENTIONS.md\n");
    finalizeRuntimeInstall({ prepared, mcp: { wired: false, status: "not-applicable" } });
    const live = doctorRuntime({ root, runtime: "aider" });
    assert(live.status === "live", `runtime doctor expected live, got ${live.status}`);
    const removed = uninstallRuntime({ root, runtime: "aider" });
    const untouched = doctorRuntime({ root, runtime: "aider" });
    assert(untouched.status === "untouched", `runtime doctor expected untouched after uninstall, got ${untouched.status}`);
    assert(fs.readFileSync(path.join(root, "CONVENTIONS.md"), "utf8").includes("User-owned preface"), "uninstall did not preserve user-owned content");
    assert(!fs.existsSync(path.join(root, ".aider.conf.yml")), "owned replacement file survived uninstall unexpectedly");
    return { installedStatus: live.status, uninstalledStatus: untouched.status, preservedUserState: true, uninstallActions: removed.results?.length || 0 };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

export async function runBenchmarks({ root = process.cwd(), writeReceipt = true } = {}) {
  const started = Date.now();
  const cases = [];
  for (const [name, fn] of [
    ["memory", benchmarkMemory],
    ["routing", benchmarkRouting],
    ["lifecycle", benchmarkLifecycle],
    ["compression", benchmarkCompression],
  ]) cases.push(await timed(name, fn));
  const receipt = {
    schema: 1,
    generatedAt: new Date().toISOString(),
    passed: cases.every((item) => item.passed),
    durationMs: Date.now() - started,
    environment: { node: process.version, platform: process.platform, arch: process.arch },
    methodology: "Deterministic local fixtures only; no model/network latency and no synthetic savings multiplier.",
    cases,
  };
  if (writeReceipt) {
    const dir = path.join(stateRoot(root), "benchmarks");
    ensureDir(dir);
    const file = path.join(dir, `${stamp()}.json`);
    fs.writeFileSync(file, `${JSON.stringify(receipt, null, 2)}\n`);
    fs.writeFileSync(path.join(dir, "latest.json"), `${JSON.stringify(receipt, null, 2)}\n`);
    receipt.receipt = path.relative(path.resolve(root), file).split(path.sep).join("/");
  }
  return receipt;
}
