import { Command } from "commander";
import { routeTask, runSandboxedCommand } from "./efficiency.js";

const joined = (value) => Array.isArray(value) ? value.join(" ") : String(value || "");

export const buildEfficiencyProgram = () => {
  const program = new Command().name("ag-kit").description("AG Kit context-efficiency controls");

  program.command("route <task...>")
    .description("Classify a task into the smallest core role/effort/flow mode")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .action((task, options) => console.log(JSON.stringify(routeTask(joined(task), options.path), null, 2)));

  program.command("run <command> [args...]")
    .description("Run a command while keeping full output on disk and returning a bounded summary")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--timeout <ms>", "Timeout in milliseconds", "120000")
    .option("--summary-lines <n>", "Maximum lines returned to context", "40")
    .action((command, args = [], options) => {
      const result = runSandboxedCommand({
        root: options.path,
        command,
        args,
        timeoutMs: Number(options.timeout),
        maxSummaryLines: Number(options.summaryLines),
      });
      process.stdout.write(`${result.summary}\n`);
      process.stdout.write(`\n[ag-kit] full log: ${result.log} · exit=${result.exitCode ?? "null"} · ${result.durationMs}ms\n`);
      if (!result.ok) process.exitCode = Number.isInteger(result.exitCode) ? result.exitCode : 1;
    });

  return program;
};

export const runEfficiencyCli = async (argv = process.argv) => buildEfficiencyProgram().parseAsync(argv);
