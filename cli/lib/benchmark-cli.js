import path from "node:path";
import { runLocalBenchmarks } from "./benchmark.js";

const valueAfter = (argv, flag, fallback) => {
  const index = argv.indexOf(flag);
  return index >= 0 && argv[index + 1] ? argv[index + 1] : fallback;
};

export async function runBenchmarkCli(argv = process.argv) {
  const args = argv.slice(3);
  const root = path.resolve(valueAfter(args, "--path", valueAfter(args, "-p", process.cwd())));
  const report = runLocalBenchmarks({ root, write: !args.includes("--no-write") });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (!report.passed) process.exitCode = 1;
  return report;
}
