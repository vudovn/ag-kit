import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const legacyEntry = path.resolve(here, "..", "bin", "index.js");

test("legacy init/update uses the shared version-pinned runtime source helper", () => {
  const source = fs.readFileSync(legacyEntry, "utf8");
  assert.match(source, /import \{ runtimeSourceSpec \} from "\.\.\/lib\/source-spec\.js";/);
  assert.match(source, /const repoSource = runtimeSourceSpec\(branch\);/);
  assert.doesNotMatch(source, /const REPO = "github:vudovn\/ag-kit"/);
  assert.doesNotMatch(source, /branch \? `\$\{REPO\}#\$\{branch\}` : REPO/);
});
