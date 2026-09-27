#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { performance } from "node:perf_hooks";
import { addEvolvingMemory, recallEvolvingMemory } from "../cli/lib/memory-evolution.js";
import { routeTask } from "../cli/lib/efficiency.js";
import { compactMarkdown } from "../cli/lib/context-artifacts.js";
import { installRuntimeTarget } from "../cli/lib/runtime-registry.js";
import { doctorRuntime, finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "../cli/lib/runtime-lifecycle.js";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const round = (value) => Number(Number(value).toFixed(3));
const timed = async (fn) => {
  const started = performance.now();
  const value = await fn();
  return { value, durationMs: round(performance.now() - started) };
};

const ensure = (condition, message) => {
  if (!condition) throw new Error(message);
};

const parseOutput = (argv) => {
  const index = argv.indexOf("--output");
  return index >= 0 && argv[index + 1] ? path.resolve(argv[index + 1]) : null;
};

const isDirectRun = () => {
  try {
    return Boolean(process.argv[1]) && import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href;
  } catch {
    return false;
  }
};

export async function runBenchmark({ sourceRoot = repoRoot } = {}) {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-benchmark-"));
  const project = path.join(fixtureRoot, "project");
  fs.mkdirSync(project, { recursive: true });
  fs.writeFileSync(path.join(project, "package.json"), '{"name":"ag-kit-benchmark-fixture","private":true}\n');
  const started = performance.now();

  try {
    const memory = await timed(() => {
      addEvolvingMemory({ root: project, text: "Use Zod for schema validation #validation [[API]]", kind: "convention", title: "Validation", session: "bench", durable: true });
      addEvolvingMemory({ root: project, text: "Wrap PostgreSQL writes in transactions #database", kind: "convention", title: "Database", session: "bench", durable: true });
      addEvolvingMemory({ root: project, text: "Prefer accessible semantic HTML for interactive controls #frontend", kind: "convention", title: "Frontend", session: "bench", durable: true });
      return recallEvolvingMemory({ root: project, query: "Zod schema validation", limit: 3, session: "bench-recall" });
    });
    ensure(memory.value.length > 0, "memory benchmark returned no results");
    ensure(/zod/i.test(memory.value[0].preview || ""), "memory benchmark did not rank the expected Zod entry first");

    const routing = await timed(() => {
      const cases = [
        ["inspect docs and find the configuration", "scout", "low", "quick"],
        ["review this security regression", "reviewer", "medium", "standard"],
        ["design a cross-runtime architecture migration", "architect", "high", "deep"],
      ];
      return cases.map(([task, role, effort, mode]) => ({ task, expected: { role, effort, mode }, actual: routeTask(task, project) }));
    });
    const routingPassed = routing.value.filter((item) => item.actual.role === item.expected.role && item.actual.effort === item.expected.effort && item.actual.mode === item.expected.mode).length;
    ensure(routingPassed === routing.value.length, "routing benchmark failed a deterministic routing case");

    const compressionInput = `# Release notes\n\nThis   paragraph   contains   repeated     spacing.\nThe next line belongs to the same paragraph and should compact safely.\n\n\n- Keep this list item\n\n\n\`\`\`js\nconst exact = "  preserve code spacing  ";\n\`\`\`\n`;
    const compression = await timed(() => compactMarkdown(compressionInput));
    const bytesBefore = Buffer.byteLength(compressionInput);
    const bytesAfter = Buffer.byteLength(compression.value);
    ensure(bytesAfter < bytesBefore, "compression benchmark did not reduce bytes");
    ensure(compression.value.includes('const exact = "  preserve code spacing  ";'), "compression benchmark changed fenced code");

    const lifecycle = await timed(() => {
      const prepared = prepareRuntimeInstall({ root: project, runtime: "aider" });
      installRuntimeTarget({ sourceRoot, targetRoot: project, runtime: "aider" });
      finalizeRuntimeInstall({ prepared });
      const live = doctorRuntime({ root: project, runtime: "aider" });
      const removed = uninstallRuntime({ root: project, runtime: "aider" });
      const after = doctorRuntime({ root: project, runtime: "aider" });
      return { live, removed, after };
    });
    ensure(lifecycle.value.live.status === "live", `lifecycle benchmark expected live, got ${lifecycle.value.live.status}`);
    ensure(lifecycle.value.after.status === "untouched", `lifecycle benchmark expected untouched after uninstall, got ${lifecycle.value.after.status}`);

    return {
      schema: 1,
      generatedAt: new Date().toISOString(),
      source: {
        commit: process.env.GITHUB_SHA || null,
        ref: process.env.GITHUB_HEAD_REF || process.env.GITHUB_REF_NAME || null,
      },
      environment: { node: process.version, platform: process.platform, arch: process.arch },
      methodology: "Local deterministic fixture evidence only; timings are machine-specific and are not a synthetic comparison against a no-AG-Kit baseline.",
      passed: true,
      totalDurationMs: round(performance.now() - started),
      benchmarks: {
        memoryRecall: { durationMs: memory.durationMs, resultCount: memory.value.length, topHit: memory.value[0].file, expectedTopHit: true },
        routing: { durationMs: routing.durationMs, cases: routing.value.length, passed: routingPassed, results: routing.value },
        compression: { durationMs: compression.durationMs, bytesBefore, bytesAfter, bytesSaved: bytesBefore - bytesAfter, reductionPct: round(((bytesBefore - bytesAfter) / bytesBefore) * 100), fencedCodePreserved: true },
        lifecycle: { durationMs: lifecycle.durationMs, runtime: "aider", installedStatus: lifecycle.value.live.status, uninstallStatus: lifecycle.value.removed.status, finalStatus: lifecycle.value.after.status, memoryPreserved: lifecycle.value.removed.memoryPreserved === true },
      },
    };
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
}

if (isDirectRun()) {
  const result = await runBenchmark();
  const output = parseOutput(process.argv.slice(2));
  if (output) {
    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, `${JSON.stringify(result, null, 2)}\n`);
  }
  console.log(JSON.stringify(result, null, 2));
}
