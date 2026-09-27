import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import fse from "fs-extra";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..", "..");

const read = (relativePath) => fse.readFile(path.join(repoRoot, relativePath), "utf8");
const readJson = (relativePath) => fse.readJson(path.join(repoRoot, relativePath));
const mentionsCount = (content, count, labelPattern) => new RegExp(`(?:${count}[^\\n]*(?:${labelPattern})|(?:${labelPattern})[^\\n]*${count})`, "i").test(content);

test("all GitHub Actions are pinned to immutable commit SHAs", async () => {
    const workflowDir = path.join(repoRoot, ".github", "workflows");
    const workflowFiles = (await fse.readdir(workflowDir)).filter((name) => name.endsWith(".yml") || name.endsWith(".yaml"));
    const unpinned = [];
    for (const workflowFile of workflowFiles) {
        const lines = (await read(path.join(".github", "workflows", workflowFile))).split("\n");
        for (const [index, line] of lines.entries()) {
            const match = line.match(/uses:\s*[^@\s]+@([^\s#]+)/);
            if (match && !/^[0-9a-f]{40}$/.test(match[1])) unpinned.push(`${workflowFile}:${index + 1}:${match[1]}`);
        }
    }
    assert.deepEqual(unpinned, []);
});

test("release workflows do not disable TLS or use a long-lived npm token", async () => {
    const deploy = await read(".github/workflows/deploy.yml");
    const publish = await read(".github/workflows/publish.yml");
    assert.doesNotMatch(deploy, /NODE_TLS_REJECT_UNAUTHORIZED/);
    assert.doesNotMatch(publish, /NPM_TOKEN|NODE_AUTH_TOKEN/);
    assert.match(publish, /id-token:\s*write/);
    assert.match(publish, /Trusted Publishing/);
});

test("release versions stay aligned across packages, locks, and toolkit", async () => {
    const manifests = await Promise.all([readJson("package.json"), readJson("cli/package.json"), readJson("web/package.json"), readJson("package-lock.json"), readJson("cli/package-lock.json"), readJson("web/package-lock.json")]);
    const toolkitVersion = (await read(".agents/VERSION")).trim();
    const expected = manifests[0].version;
    for (const manifest of manifests) {
        assert.equal(manifest.version, expected);
        if (manifest.packages?.[""]?.version) assert.equal(manifest.packages[""].version, expected);
    }
    assert.equal(toolkitVersion, expected);
});

test("public and runtime instruction docs reflect the lean v2 inventory", async () => {
    const capabilities = await readJson("platform-capabilities.json");
    const runtimeCount = Object.keys(capabilities.platforms).length;
    assert.equal(capabilities.targets.residentSkills, 1);
    assert.equal(capabilities.targets.permanentAgents, 4);
    assert.equal(capabilities.targets.workflowEngines, 1);
    assert.equal(runtimeCount, 16);

    const inventoryDocs = ["README.md", "README-VI.md", "web/README.md", "AGENT_FLOW.md"];
    for (const file of inventoryDocs) {
        const content = await read(file);
        assert.equal(mentionsCount(content, 18, "skills?"), true, `${file} should mention the 18-skill v2 surface`);
        assert.equal(mentionsCount(content, 4, "(?:permanent\\s+)?agents?"), true, `${file} should mention the four-agent v2 surface`);
        assert.equal(mentionsCount(content, runtimeCount, "runtime(?:s|\\s+targets?)?"), true, `${file} should mention all ${runtimeCount} runtimes`);
    }

    for (const file of ["README.md", "README-VI.md", "web/README.md", "AGENTS.md", "CLAUDE.md", "MIGRATION.md", "AGENT_FLOW.md"]) {
        const content = await read(file);
        assert.doesNotMatch(content, /47\s+(?:skills|kỹ năng)|20\s+(?:specialist\s+agents|agent\s+chuyên)|13\s+(?:workflows|quy trình)|45\s+(?:skills|skill)/i, `${file} must not restore the legacy inventory`);
        assert.doesNotMatch(content, /ln -s ~\/\.ag-kit\/\.agents \.agent(?:\s|$)/, `${file} must not restore the legacy symlink setup`);
    }

    const claude = await read("CLAUDE.md");
    assert.doesNotMatch(claude, /npm\s+run\s+(?:generate:agents|check:agents|test:toolkit)|python[^\n]*validate_kit\.py/i, "CLAUDE.md must not instruct running removed v1 validation steps");
    assert.match(claude, /check:docs/);

    for (const file of ["README.md", "README-VI.md"]) {
        assert.match(await read(file), /ag-kit rollback/);
    }
});

test("published CLI package includes its runtime library", async () => {
    const cliPackage = await readJson("cli/package.json");
    assert.ok(cliPackage.files.includes("bin"));
    assert.ok(cliPackage.files.includes("lib"));
});
