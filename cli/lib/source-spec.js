import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "github:vudovn/ag-kit";
const here = path.dirname(fileURLToPath(import.meta.url));
const packageJson = JSON.parse(fs.readFileSync(path.join(here, "..", "package.json"), "utf8"));

export const cliVersion = String(packageJson.version);

export function runtimeSourceSpec(ref = "") {
  const requested = String(ref || "").trim();
  return `${REPO}#${requested || `v${cliVersion}`}`;
}
