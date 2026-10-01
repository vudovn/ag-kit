import { Command } from "commander";
import { compressArtifact, createHandoff, readHandoff } from "./context-artifacts.js";

const collect = (value, previous) => [...previous, value];
const joined = (value) => Array.isArray(value) ? value.join(" ") : String(value || "");

export const buildContextProgram = () => {
  const program = new Command().name("ag-kit").description("AG Kit context continuity tools");

  program.command("compress <file>")
    .description("Compact a project Markdown/context artifact without inventing a summary")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--write", "Replace the source after creating a timestamped backup", false)
    .option("-o, --output <file>", "Output path inside the project")
    .action((file, options) => console.log(JSON.stringify(compressArtifact({ root: options.path, file, write: options.write, output: options.output || "" }), null, 2)));

  const handoff = program.command("handoff").description("Create or read a compact session continuity artifact");
  handoff.command("create")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--goal <text>", "Goal to continue", "")
    .option("--state <text>", "Current state", "")
    .option("--decision <text>", "Decision to preserve", collect, [])
    .option("--evidence <text>", "Verification evidence", collect, [])
    .option("--risk <text>", "Open risk", collect, [])
    .option("--next <text>", "Next concrete action", "")
    .action((options) => {
      const result = createHandoff({ root: options.path, goal: options.goal, state: options.state, decisions: options.decision, evidence: options.evidence, risks: options.risk, next: options.next });
      console.log(JSON.stringify({ ...result, content: undefined }, null, 2));
    });
  handoff.command("show")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .action((options) => {
      const result = readHandoff(options.path);
      if (!result.exists) { console.log("No AG Kit handoff found."); process.exitCode = 1; return; }
      process.stdout.write(result.content);
    });

  handoff.command("quick <summary...>")
    .description("Create a minimal handoff from one summary and an optional next action")
    .option("-p, --path <dir>", "Project directory", process.cwd())
    .option("--next <text>", "Next concrete action", "")
    .action((summary, options) => console.log(JSON.stringify(createHandoff({ root: options.path, state: joined(summary), next: options.next }), null, 2)));

  return program;
};

export const runContextCli = async (argv = process.argv) => buildContextProgram().parseAsync(argv);
