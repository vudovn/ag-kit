import { Command } from "commander";
import { checkPromptQuality } from "./prompt-quality.js";

const joined = (value) => Array.isArray(value) ? value.join(" ") : String(value || "");

export const buildPromptProgram = () => {
  const program = new Command().name("ag-kit prompt-check").description("Deterministically check whether a task has enough concrete context to act without guessing.");
  program
    .argument("<prompt...>", "Task or prompt to inspect")
    .option("--json", "Print structured JSON", false)
    .option("--force", "Explicitly bypass the quality gate", false)
    .action((prompt, options) => {
      const result = checkPromptQuality(joined(prompt), { force: options.force });
      if (options.json) console.log(JSON.stringify(result, null, 2));
      else {
        console.log(`[ag-kit] prompt ${result.status}: ${result.summary}`);
        for (const question of result.questions) console.log(`- ${question}`);
        if (result.signals.length) console.log(`[ag-kit] signals: ${result.signals.join(", ")}`);
      }
      if (!result.ok) process.exitCode = 2;
    });
  return program;
};

export const runPromptCli = async (argv = process.argv) => buildPromptProgram().parseAsync([argv[0], argv[1], ...argv.slice(3)]);
