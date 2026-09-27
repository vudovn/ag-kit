import { Command } from "commander";
import { rebuildSemanticIndex, semanticRecall, semanticStatus } from "./memory-semantic.js";

const overrides = (options = {}) => ({
  enabled: true,
  allowDownload: Boolean(options.allowDownload),
  ...(options.model ? { model: options.model } : {}),
});

export const buildSemanticMemoryProgram = () => {
  const program = new Command().name("ag-kit memory semantic").description("Optional project-local semantic cold tier. No model download occurs unless --allow-download is explicit.");

  program.command("status")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--model <id-or-path>", "Embedding model id or local path")
    .action(async (options) => console.log(JSON.stringify(await semanticStatus(options.path, { overrides: { enabled: true, ...(options.model ? { model: options.model } : {}) } }), null, 2)));

  program.command("rebuild")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--model <id-or-path>", "Embedding model id or local path")
    .option("--allow-download", "Explicitly allow a model download into project-local cache", false)
    .action(async (options) => {
      const result = await rebuildSemanticIndex({ root: options.path, overrides: overrides(options) });
      console.log(JSON.stringify(result, null, 2));
      if (!result.available) process.exitCode = 2;
    });

  program.command("recall <query...>")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--limit <n>", "Maximum results", "5")
    .option("--model <id-or-path>", "Embedding model id or local path")
    .option("--allow-download", "Explicitly allow a model download into project-local cache", false)
    .action(async (query, options) => {
      const result = await semanticRecall({ root: options.path, query: query.join(" "), limit: Number(options.limit), overrides: overrides(options) });
      console.log(JSON.stringify(result, null, 2));
      if (!result.available) process.exitCode = 2;
    });

  return program;
};

export const runSemanticMemoryCli = async (argv = process.argv) => buildSemanticMemoryProgram().parseAsync([argv[0], argv[1], ...argv.slice(4)]);
