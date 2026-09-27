import { Command } from "commander";
import { brainStatus, listRegisteredProjects, registerProject, searchAcrossProjects, unregisterProject } from "./memory-registry.js";

const joined = (value) => Array.isArray(value) ? value.join(" ") : String(value || "");

export const buildBrainProgram = () => {
  const program = new Command().name("ag-kit").description("AG Kit opt-in cross-project brain");
  const brain = program.command("brain").description("Register projects and search local memory across them");

  brain.command("register [dir]")
    .option("--allow-outside-home", "Explicitly allow this one project outside the home directory", false)
    .action((dir = process.cwd(), options) => console.log(JSON.stringify(registerProject({ root: dir, allowOutsideHome: options.allowOutsideHome }), null, 2)));

  brain.command("unregister [dir]")
    .action((dir = process.cwd()) => console.log(JSON.stringify(unregisterProject({ root: dir }), null, 2)));

  brain.command("list")
    .action(() => console.log(JSON.stringify(listRegisteredProjects(), null, 2)));

  brain.command("status")
    .action(() => console.log(JSON.stringify(brainStatus(), null, 2)));

  brain.command("search <query...>")
    .option("--limit <n>", "Maximum results", "10")
    .option("--at <iso>", "Search memory valid at this timestamp", new Date().toISOString())
    .option("--exclude-current", "Exclude the current project from cross-project results", false)
    .action((query, options) => console.log(JSON.stringify(searchAcrossProjects({ query: joined(query), limit: Number(options.limit), at: options.at, currentRoot: options.excludeCurrent ? process.cwd() : "" }), null, 2)));

  return program;
};

export const runBrainCli = async (argv = process.argv) => buildBrainProgram().parseAsync(argv);
