import { dashboardStatus, stopDashboard } from "./observability.js";

const optionValue = (argv, name, fallback) => {
  const index = argv.indexOf(name);
  return index >= 0 && argv[index + 1] ? argv[index + 1] : fallback;
};

export function canHandleDashboardControl(argv = process.argv) {
  return argv[2] === "dashboard" && ["status", "stop"].includes(argv[3]);
}

export async function runDashboardControl(argv = process.argv) {
  const action = argv[3];
  const root = optionValue(argv, "--path", optionValue(argv, "-p", process.cwd()));
  const result = action === "stop" ? stopDashboard(root) : dashboardStatus(root);
  console.log(JSON.stringify(result, null, 2));
  return result;
}
