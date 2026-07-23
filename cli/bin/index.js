#!/usr/bin/env node
import { Command, Option } from "commander";
import chalk from "chalk";
import ora from "ora";
import { downloadTemplate } from "giget";
import fs from "node:fs";
import path from "node:path";
import fse from "fs-extra";
import readline from "node:readline";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
    applyUpdatePlan,
    createRunId,
    createUpdatePlan,
    installFreshTree,
    listBackups,
    loadManifest,
    restoreBackup,
    snapshotTree,
} from "../lib/managed-tree.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const pkg = await fse.readJson(path.join(__dirname, "..", "package.json"));

const REPO = "github:vudovn/ag-kit";
const AGENT_FOLDER = ".agents";
const TEMP_FOLDER = ".temp_ag_kit";

const showBanner = (quiet = false) => {
    if (quiet) return;
    console.log(
        chalk.blueBright(`
    ╔══════════════════════════════════════╗
    ║        ANTIGRAVITY KIT CLI           ║
    ╚══════════════════════════════════════╝
    `),
    );
};

const log = (message, quiet = false) => {
    if (!quiet) console.log(message);
};

const confirm = (question) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    return new Promise((resolve) => {
        rl.question(chalk.yellow(`? ${question} (y/N) `), (answer) => {
            rl.close();
            const normalized = answer.trim().toLowerCase();
            resolve(normalized === "y" || normalized === "yes");
        });
    });
};

const cleanup = async (tempDir) => {
    if (tempDir) await fse.remove(tempDir);
};

const checkUpdate = async (quiet = false) => {
    if (quiet) return null;
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1500);
        const response = await fetch("https://registry.npmjs.org/@vudovn/ag-kit/latest", {
            signal: controller.signal,
        });
        clearTimeout(timeoutId);
        if (!response.ok) return null;
        const data = await response.json();
        return data.version && data.version !== pkg.version ? data.version : null;
    } catch {
        return null;
    }
};

const showUpdateNotification = (latestVersion) => {
    if (!latestVersion) return;
    console.log(
        chalk.yellow(`
  ┌────────────────────────────────────────────────────────┐
  │  Update available: ${chalk.red(pkg.version)} → ${chalk.green(latestVersion)}
  │  Run: ${chalk.cyan("npm install -g @vudovn/ag-kit")}
  └────────────────────────────────────────────────────────┘
  `),
    );
};

const readIncomingVersion = async (tempDir) => {
    try {
        const packageJson = await fse.readJson(path.join(tempDir, "package.json"));
        return packageJson.version || pkg.version;
    } catch {
        return pkg.version;
    }
};

const downloadToolkit = async ({ tempDir, branch, spinner }) => {
    await cleanup(tempDir);
    const repoSource = branch ? `${REPO}#${branch}` : REPO;
    if (spinner) spinner.text = `Downloading ${repoSource}...`;
    await downloadTemplate(repoSource, { dir: tempDir, force: true });

    const incomingDir = path.join(tempDir, AGENT_FOLDER);
    if (!(await fse.pathExists(incomingDir))) {
        throw new Error(`Could not find ${AGENT_FOLDER} in the downloaded repository`);
    }
    return incomingDir;
};

const printPlan = (plan, { dryRun = false, quiet = false } = {}) => {
    if (quiet) return;
    const prefix = dryRun ? "[Dry Run] " : "";
    console.log(chalk.gray("────────────────────────────────────────"));
    console.log(`${prefix}Strategy:  ${chalk.cyan(plan.strategy)}`);
    console.log(`${prefix}Changes:   ${chalk.green(plan.actions.length)}`);
    console.log(`${prefix}Preserved: ${chalk.yellow(plan.preserved.length)}`);
    console.log(`${prefix}Conflicts: ${plan.conflicts.length ? chalk.red(plan.conflicts.length) : chalk.green(0)}`);
    console.log(`${prefix}Unchanged: ${chalk.gray(plan.unchanged.length)}`);
    console.log(chalk.gray("────────────────────────────────────────"));

    if (dryRun && plan.conflicts.length) {
        console.log(chalk.yellow("Files requiring manual review:"));
        for (const conflict of plan.conflicts.slice(0, 20)) {
            console.log(`  - ${conflict.file}: ${conflict.reason}`);
        }
        if (plan.conflicts.length > 20) {
            console.log(chalk.gray(`  ...and ${plan.conflicts.length - 20} more`));
        }
    }
};

const requireConfirmation = async ({ exists, strategy, force, quiet, dryRun }) => {
    if (dryRun || !exists || force) return true;
    if (quiet) {
        throw new Error("Existing installation requires --force when --quiet is used");
    }

    const question = strategy === "replace"
        ? `Replace the entire ${AGENT_FOLDER} folder? A backup will be created.`
        : `Apply a merge-aware update to ${AGENT_FOLDER}? Local changes will be preserved.`;
    return confirm(question);
};

export const installOrUpdate = async (options = {}, mode = "init") => {
    const quiet = Boolean(options.quiet);
    const dryRun = Boolean(options.dryRun);
    const strategy = options.strategy || "merge";
    const backup = options.backup !== false;
    const targetDir = path.resolve(options.path || process.cwd());
    const tempDir = path.join(targetDir, TEMP_FOLDER);
    const agentDir = path.join(targetDir, AGENT_FOLDER);
    const exists = await fse.pathExists(agentDir);

    if (mode === "update" && !exists) {
        throw new Error(`Could not find ${AGENT_FOLDER} at ${targetDir}. Run ag-kit init first.`);
    }

    const approved = await requireConfirmation({
        exists,
        strategy,
        force: Boolean(options.force),
        quiet,
        dryRun,
    });
    if (!approved) {
        log(chalk.gray("Operation cancelled."), quiet);
        return { cancelled: true };
    }

    const spinner = quiet
        ? null
        : ora({ text: "Preparing...", color: "cyan" }).start();

    try {
        const incomingDir = await downloadToolkit({
            tempDir,
            branch: options.branch,
            spinner,
        });
        const toolkitVersion = await readIncomingVersion(tempDir);
        const runId = createRunId();

        if (!exists) {
            const incomingSnapshot = await snapshotTree(incomingDir);
            if (dryRun) {
                if (spinner) spinner.stop();
                printPlan(
                    {
                        strategy: "install",
                        actions: Object.keys(incomingSnapshot).map((file) => ({ type: "add", file })),
                        conflicts: [],
                        preserved: [],
                        unchanged: [],
                    },
                    { dryRun, quiet },
                );
                return { dryRun: true, toolkitVersion };
            }

            if (spinner) spinner.text = "Installing toolkit...";
            const report = await installFreshTree({
                projectDir: targetDir,
                incomingDir,
                currentDir: agentDir,
                toolkitVersion,
                runId,
            });
            if (spinner) spinner.succeed(chalk.green("Installation successful!"));
            return report;
        }

        const manifest = await loadManifest(agentDir);
        const plan = await createUpdatePlan({
            currentDir: agentDir,
            incomingDir,
            strategy,
            manifest,
        });

        if (dryRun) {
            if (spinner) spinner.stop();
            printPlan(plan, { dryRun, quiet });
            return { dryRun: true, plan, toolkitVersion };
        }

        if (spinner) spinner.text = "Applying safe update...";
        const report = await applyUpdatePlan({
            projectDir: targetDir,
            currentDir: agentDir,
            incomingDir,
            plan,
            toolkitVersion,
            backup,
            runId,
            conflictReportPath: options.conflictReport,
        });

        if (spinner) {
            if (report.summary.conflicts) {
                spinner.warn(chalk.yellow("Update completed with conflicts preserved for review."));
            } else {
                spinner.succeed(chalk.green("Update successful!"));
            }
        }
        printPlan(plan, { quiet });

        if (!quiet) {
            if (report.backupDir) console.log(`Backup: ${chalk.cyan(report.backupDir)}`);
            console.log(`Report: ${chalk.cyan(report.reportPath)}`);
            if (report.summary.conflicts) {
                console.log(
                    chalk.yellow(
                        `Incoming conflict copies are stored under ${AGENT_FOLDER}/.ag-kit/conflicts/${runId}`,
                    ),
                );
            }
        }

        return report;
    } finally {
        await cleanup(tempDir);
    }
};

export const initCommand = async (options) => {
    const quiet = Boolean(options.quiet);
    showBanner(quiet);
    const updatePromise = checkUpdate(quiet);

    try {
        const result = await installOrUpdate(options, "init");
        const latestVersion = await updatePromise;
        showUpdateNotification(latestVersion);
        if (result?.summary?.conflicts) process.exitCode = 2;
    } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exitCode = 1;
    }
};

export const updateCommand = async (options) => {
    const quiet = Boolean(options.quiet);
    showBanner(quiet);
    try {
        const result = await installOrUpdate(options, "update");
        if (result?.summary?.conflicts) process.exitCode = 2;
    } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exitCode = 1;
    }
};

export const rollbackCommand = async (options) => {
    const quiet = Boolean(options.quiet);
    showBanner(quiet);
    const targetDir = path.resolve(options.path || process.cwd());
    const agentDir = path.join(targetDir, AGENT_FOLDER);

    try {
        const backups = await listBackups(targetDir);
        const selected = options.backup
            ? backups.find((item) => item.id === options.backup)
            : backups[0];

        if (!selected) throw new Error(options.backup ? `Backup not found: ${options.backup}` : "No backups found");

        if (options.dryRun) {
            console.log(chalk.blueBright("[Dry Run] No changes will be made"));
            console.log(`Would restore: ${chalk.cyan(selected.path)}`);
            return;
        }

        if (!options.force) {
            if (quiet) throw new Error("Rollback requires --force when --quiet is used");
            const approved = await confirm(`Restore backup ${selected.id}?`);
            if (!approved) return;
        }

        const result = await restoreBackup({
            projectDir: targetDir,
            agentDir,
            backupId: selected.id,
            keepCurrent: options.keepCurrent !== false,
        });
        log(chalk.green(`Restored backup ${result.restoredBackupId}`), quiet);
        if (result.safetyBackupDir) log(`Pre-rollback backup: ${result.safetyBackupDir}`, quiet);
    } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exitCode = 1;
    }
};

export const statusCommand = async (options) => {
    const targetDir = path.resolve(options.path || process.cwd());
    const agentDir = path.join(targetDir, AGENT_FOLDER);
    const updatePromise = checkUpdate(options.quiet);

    console.log(chalk.blueBright("\nAntigravity Kit Status\n"));
    console.log(`CLI version: ${chalk.cyan(pkg.version)}`);

    if (await fse.pathExists(agentDir)) {
        const stats = await fse.stat(agentDir);
        const manifest = await loadManifest(agentDir);
        const backups = await listBackups(targetDir);
        console.log(chalk.green("[OK] Installed"));
        console.log(chalk.gray("────────────────────────────────────────"));
        console.log(`Path:        ${chalk.cyan(agentDir)}`);
        console.log(`Modified:    ${chalk.gray(stats.mtime.toLocaleString("en-US"))}`);
        console.log(`Managed:     ${manifest ? chalk.green("yes") : chalk.yellow("legacy/no manifest")}`);
        console.log(`Kit version: ${chalk.cyan(manifest?.toolkitVersion || "unknown")}`);
        console.log(`Backups:     ${chalk.yellow(backups.length)}`);
        console.log(chalk.gray("────────────────────────────────────────\n"));
    } else {
        console.log(chalk.red("[X] Not installed"));
        console.log(chalk.yellow(`Run ${chalk.cyan("ag-kit init")} to install.\n`));
    }

    const latestVersion = await updatePromise;
    if (latestVersion) showUpdateNotification(latestVersion);
    else if (!options.quiet) console.log(chalk.green("[OK] CLI is on the latest version.\n"));
};

export const buildProgram = () => {
    const program = new Command();
    const strategyOption = () => new Option(
        "--strategy <mode>",
        "Update strategy: merge preserves local changes; replace restores the upstream tree",
    ).choices(["merge", "replace"]).default("merge");

    program
        .name("ag-kit")
        .description("CLI tool to install and safely manage Antigravity Kit")
        .version(pkg.version, "-v, --version", "Display version number");

    program
        .command("init")
        .description("Install .agents into a project; safely merges when it already exists")
        .option("-f, --force", "Skip confirmation prompt", false)
        .option("-p, --path <dir>", "Path to the project directory", process.cwd())
        .option("-b, --branch <name>", "Select repository branch")
        .option("-q, --quiet", "Suppress non-error output", false)
        .option("--dry-run", "Download and calculate changes without applying them", false)
        .option("--no-backup", "Do not create a pre-update backup")
        .option("--conflict-report <file>", "Write the update report to a custom path")
        .addOption(strategyOption())
        .action(initCommand);

    program
        .command("update")
        .description("Safely update .agents while preserving local changes")
        .option("-f, --force", "Skip confirmation prompt", false)
        .option("-p, --path <dir>", "Path to the project directory", process.cwd())
        .option("-b, --branch <name>", "Select repository branch")
        .option("-q, --quiet", "Suppress non-error output", false)
        .option("--dry-run", "Download and calculate changes without applying them", false)
        .option("--no-backup", "Do not create a pre-update backup")
        .option("--conflict-report <file>", "Write the update report to a custom path")
        .addOption(strategyOption())
        .action(updateCommand);

    program
        .command("rollback")
        .description("Restore a pre-update .agents backup")
        .option("--backup <id>", "Backup ID; defaults to the newest backup")
        .option("-f, --force", "Skip confirmation prompt", false)
        .option("-p, --path <dir>", "Path to the project directory", process.cwd())
        .option("-q, --quiet", "Suppress non-error output", false)
        .option("--dry-run", "Show which backup would be restored", false)
        .option("--no-keep-current", "Do not back up the current tree before rollback")
        .action(rollbackCommand);

    program
        .command("status")
        .description("Check installation, managed-tree status, backups, and CLI updates")
        .option("-p, --path <dir>", "Path to the project directory", process.cwd())
        .option("-q, --quiet", "Suppress network update check", false)
        .action(statusCommand);

    return program;
};

export const runCli = async (argv = process.argv) => {
    const program = buildProgram();
    if (!argv.slice(2).length) {
        program.outputHelp();
        return;
    }
    await program.parseAsync(argv);
};

let isDirectRun = false;
if (process.argv[1]) {
    try {
        const resolvedPath = fs.realpathSync(process.argv[1]);
        isDirectRun = pathToFileURL(resolvedPath).href === import.meta.url;
    } catch {
        isDirectRun = pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
    }
}

if (isDirectRun) {
    process.on("SIGINT", async () => {
        const tempDir = path.join(process.cwd(), TEMP_FOLDER);
        await cleanup(tempDir);
        console.log(chalk.gray("\nOperation aborted by user."));
        process.exit(130);
    });
    await runCli();
}
