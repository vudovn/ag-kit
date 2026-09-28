import { runBenchmarks } from "./benchmark.js";

const argValue = (argv, name, fallback = "") => {
  const index = argv.indexOf(name);
  return index >= 0 && index + 1 < argv.length ? argv[index + 1] : fallback;
};

export async function runBenchmarkCli(argv = process.argv) {
  const root = argValue(argv, "--path", argValue(argv, "-p", process.cwd()));
  const noReceipt = argv.includes("--no-receipt");
  const result = await runBenchmarks({ root, writeReceipt: !noReceipt });
  console.log(JSON.stringify(result, null, 2));
  if (!result.passed) process.exitCode = 1;
  return result;
}
