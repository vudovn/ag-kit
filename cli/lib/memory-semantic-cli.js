import { Command } from "commander";
import { installSemanticProvider, rebuildSemanticIndex, semanticRecall, semanticStatus, setSemanticEnabled } from "./memory-semantic.js";

const overrides = (options = {}) => ({
  ...(options.allowDownload ? { allowDownload: true } : {}),
  ...(options.model ? { model: options.model } : {}),
});

export const buildSemanticMemoryProgram = () => {
  const program = new Command().name("ag-kit memory semantic").description("Optional project-local semantic cold tier. Provider install and model download each require explicit network approval.");

  program.command("status")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--model <id-or-path>", "Embedding model id or local path")
    .action(async (options) => console.log(JSON.stringify(await semanticStatus(options.path, { overrides: overrides(options) }), null, 2)));

  program.command("on")
    .description("Enable semantic retrieval for this project without downloading anything")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--model <id-or-path>", "Persist an embedding model id or local path")
    .action((options) => console.log(JSON.stringify(setSemanticEnabled({ root: options.path, enabled: true, model: options.model || "" }), null, 2)));

  program.command("off")
    .description("Disable semantic retrieval while preserving rebuildable local state")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .action((options) => console.log(JSON.stringify(setSemanticEnabled({ root: options.path, enabled: false }), null, 2)));

  program.command("setup")
    .description("Install the optional Transformers.js provider into project-local AG Kit state")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--allow-network", "Explicitly allow npm network access for the pinned provider package", false)
    .action((options) => {
      const result = installSemanticProvider({ root: options.path, allowNetwork: Boolean(options.allowNetwork) });
      console.log(JSON.stringify(result, null, 2));
      if (!result.installed) process.exitCode = 2;
    });

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
