import { Command } from "commander";
import { downloadTemplate } from "giget";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { detectRuntimes } from "./runtime-detect.js";
import { installRuntimeTarget } from "./runtime-registry.js";
import { finalizeRuntimeInstall, prepareRuntimeInstall, restorePreparedInstall } from "./runtime-lifecycle.js";
import { wireRuntimeMcp } from "./runtime-mcp.js";

const REPO = "github:vudovn/ag-kit";
const withSource = async (branch, fn) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-source-"));
  try {
    await downloadTemplate(branch ? `${REPO}#${branch}` : REPO, { dir, force: true });
    return await fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
};

const installOne = ({ sourceRoot, targetRoot, runtime }) => {
  const prepared = prepareRuntimeInstall({ root: targetRoot, runtime });
  try {
    const installed = installRuntimeTarget({ sourceRoot, targetRoot, runtime });
    const mcp = wireRuntimeMcp({ root: targetRoot, runtime });
    const lifecycle = finalizeRuntimeInstall({ prepared, mcp });
    return { runtime, status: "installed", installed, mcp, installedAt: lifecycle.installedAt };
  } catch (error) {
    const recovery = restorePreparedInstall(prepared);
    return { runtime, status: "failed", error: error.message, restoredPaths: recovery.results.length };
  }
};

export const buildRuntimeAutoProgram = () => {
  const program = new Command().name("ag-kit").description("AG Kit runtime discovery");
  const runtime = program.command("runtime");

  runtime.command("detect")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--no-home", "Do not use user-home runtime markers")
    .action((options) => {
      const results = detectRuntimes({ root: options.path, includeHome: options.home !== false });
      console.log(JSON.stringify({ detected: results.filter((item) => item.detected), untouched: results.filter((item) => !item.detected).map((item) => item.runtime) }, null, 2));
    });

  runtime.command("install-present")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("-b, --branch <name>", "AG Kit source branch")
    .option("--no-home", "Do not use user-home runtime markers")
    .option("--force", "Reinstall runtimes already managed by AG Kit", false)
    .action(async (options) => {
      const detected = detectRuntimes({ root: options.path, includeHome: options.home !== false }).filter((item) => item.detected);
      const pending = detected.filter((item) => options.force || !item.lifecycle);
      const skipped = detected.filter((item) => !options.force && item.lifecycle).map((item) => ({ runtime: item.runtime, status: "already-managed" }));
      if (!pending.length) {
        console.log(JSON.stringify({ detected: detected.map((item) => item.runtime), results: skipped }, null, 2));
        return;
      }
      const installed = await withSource(options.branch, async (sourceRoot) => pending.map((item) => installOne({ sourceRoot, targetRoot: options.path, runtime: item.runtime })));
      console.log(JSON.stringify({ detected: detected.map((item) => item.runtime), results: [...skipped, ...installed] }, null, 2));
      if (installed.some((item) => item.status === "failed")) process.exitCode = 1;
    });

  return program;
};

export const runRuntimeAutoCli = async (argv = process.argv) => buildRuntimeAutoProgram().parseAsync(argv);
