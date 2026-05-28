#!/usr/bin/env node
import { Command } from "commander";
import chalk from "chalk";
import ora from "ora";
import { downloadTemplate } from "giget";
import path from "path";
import fse from "fs-extra";
import readline from "readline";
import { fileURLToPath } from "url";

// Get package.json for version
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const pkg = await fse.readJson(path.join(__dirname, "..", "package.json"));

// ============================================================================
// CONSTANTS
// ============================================================================
const REPO = "github:vudovn/ag-kit";
const AGENT_FOLDER = ".agents";
const TEMP_FOLDER = ".temp_ag_kit";

// ============================================================================
// UTILITIES
// ============================================================================

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
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise((resolve) => {
        rl.on("SIGINT", async () => {
            rl.close();
            console.log(chalk.gray("\nOperation aborted by user."));
            const tempDir = path.join(path.resolve(process.cwd()), TEMP_FOLDER);
            if (await fse.pathExists(tempDir)) {
                await fse.remove(tempDir);
            }
            process.exit(0);
        });

        rl.question(chalk.yellow(`? ${question} (y/N) `), (answer) => {
            rl.close();
            const val = answer.trim().toLowerCase();
            resolve(val === "y" || val === "yes");
        });
    });
};

const checkUpdate = async (quiet = false) => {
    if (quiet) return null;
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1500);

        const res = await fetch("https://registry.npmjs.org/@vudovn/ag-kit/latest", {
            signal: controller.signal,
        });
        clearTimeout(timeoutId);

        if (res.ok) {
            const data = await res.json();
            if (data.version && data.version !== pkg.version) {
                return data.version;
            }
        }
    } catch (e) {
        // Silently ignore update check errors
    }
    return null;
};

const showUpdateNotification = (latestVersion) => {
    if (!latestVersion) return;
    console.log(
        chalk.yellow(`
  ┌────────────────────────────────────────────────────────┐
  │  Update available: ${chalk.red(pkg.version)} → ${chalk.green(latestVersion)}               │
  │  Run: ${chalk.cyan("npm install -g @vudovn/ag-kit")}                 │
  └────────────────────────────────────────────────────────┘
  `)
    );
};

// Global SIGINT Handler for graceful cleanup
process.on("SIGINT", async () => {
    console.log(chalk.gray("\n\nOperation aborted by user. Cleaning up..."));
    const targetDir = process.cwd();
    const tempDir = path.join(path.resolve(targetDir), TEMP_FOLDER);
    if (await fse.pathExists(tempDir)) {
        await fse.remove(tempDir);
    }
    process.exit(0);
});

const cleanup = async (tempDir) => {
    await fse.remove(tempDir);
};

const copyAgentFolder = async (tempDir, destDir) => {
    const sourceAgent = path.join(tempDir, AGENT_FOLDER);

    if (!(await fse.pathExists(sourceAgent))) {
        throw new Error(
            `Could not find ${AGENT_FOLDER} folder in source repository!`,
        );
    }

    await fse.copy(sourceAgent, destDir, { overwrite: true });
};

// ============================================================================
// COMMANDS
// ============================================================================

const initCommand = async (options) => {
    const quiet = options.quiet || false;
    const dryRun = options.dryRun || false;

    showBanner(quiet);

    // Run non-blocking check update in parallel background
    const updatePromise = checkUpdate(quiet);

    const targetDir = path.resolve(options.path || process.cwd());
    const tempDir = path.join(targetDir, TEMP_FOLDER);
    const agentDir = path.join(targetDir, AGENT_FOLDER);

    if (dryRun) {
        console.log(chalk.blueBright("\n[Dry Run] No changes will be made\n"));
        console.log(chalk.white("Would perform the following actions:"));
        console.log(chalk.gray("────────────────────────────────────────"));
        console.log(
            `  1. Download from: ${chalk.cyan(REPO)}${options.branch ? "#" + options.branch : ""}`,
        );
        console.log(`  2. Install to: ${chalk.cyan(agentDir)}`);

        if (await fse.pathExists(agentDir)) {
            console.log(`  3. ${chalk.yellow("Overwrite existing .agents folder")}`);
        }

        console.log(chalk.gray("────────────────────────────────────────\n"));
        return;
    }

    if (await fse.pathExists(agentDir)) {
        if (!options.force) {
            log(
                chalk.yellow(
                    `Warning: Folder ${AGENT_FOLDER} already exists at: ${agentDir}`,
                ),
                quiet,
            );
            const shouldOverwrite = await confirm("Do you want to overwrite it?");

            if (!shouldOverwrite) {
                log(chalk.gray("Operation cancelled."), quiet);
                process.exit(0);
            }
        }
        log(chalk.gray(`Overwriting ${AGENT_FOLDER} folder...`), quiet);
    }

    const spinner = quiet
        ? null
        : ora({
            text: "Downloading...",
            color: "cyan",
        }).start();

    try {
        const repoSource = options.branch ? `${REPO}#${options.branch}` : REPO;
        await downloadTemplate(repoSource, {
            dir: tempDir,
            force: true,
        });

        if (spinner) spinner.text = "Installing...";

        // fse.remove handles Windows locks gracefully
        await fse.remove(agentDir);

        await copyAgentFolder(tempDir, agentDir);
        await cleanup(tempDir);

        if (spinner) {
            spinner.succeed(chalk.green("Installation successful!"));
        }

        if (!quiet) {
            console.log(chalk.gray("\n────────────────────────────────────────"));
            console.log(chalk.white("Result:"));
            console.log(`   ${chalk.cyan(AGENT_FOLDER)} → ${chalk.gray(agentDir)}`);
            console.log(chalk.gray("────────────────────────────────────────"));
            console.log(chalk.green("\nHappy coding!\n"));
        }

        // Show update notification if available
        const latestVersion = await updatePromise;
        showUpdateNotification(latestVersion);
    } catch (error) {
        let errorMsg = error.message;
        if (error.code === "ENOTFOUND" || error.message.includes("fetch failed")) {
            errorMsg = "Network connection failed. Please check your internet connection and try again.";
        } else if (error.message.includes("Could not find")) {
            errorMsg = `Source repository mismatch. Ensure the branch or repo exists. Details: ${error.message}`;
        }

        if (spinner) {
            spinner.fail(chalk.red(`Error: ${errorMsg}`));
        } else {
            console.error(chalk.red(`Error: ${errorMsg}`));
        }

        await cleanup(tempDir);
        process.exit(1);
    }
};

const updateCommand = async (options) => {
    const quiet = options.quiet || false;

    showBanner(quiet);

    const targetDir = path.resolve(options.path || process.cwd());
    const agentDir = path.join(targetDir, AGENT_FOLDER);

    if (!(await fse.pathExists(agentDir))) {
        console.log(
            chalk.red(
                `Error: Could not find ${AGENT_FOLDER} folder at: ${targetDir}`,
            ),
        );
        console.log(
            chalk.yellow(`Tip: Run ${chalk.cyan("ag-kit init")} to install first.`),
        );
        process.exit(1);
    }

    if (!options.force && !quiet) {
        log(
            chalk.yellow(
                `Warning: Update will overwrite the entire ${AGENT_FOLDER} folder`,
            ),
            quiet,
        );
        const shouldUpdate = await confirm("Are you sure you want to continue?");

        if (!shouldUpdate) {
            log(chalk.gray("Operation cancelled."), quiet);
            process.exit(0);
        }
    }

    await initCommand({ ...options, force: true });
};

const statusCommand = async (options) => {
    const targetDir = path.resolve(options.path || process.cwd());
    const agentDir = path.join(targetDir, AGENT_FOLDER);

    console.log(chalk.blueBright("\nAntigravity Kit Status\n"));

    if (await fse.pathExists(agentDir)) {
        const stats = await fse.stat(agentDir);
        const files = await fse.readdir(agentDir);

        console.log(chalk.green("[OK] Installed"));
        console.log(chalk.gray("────────────────────────────────────────"));
        console.log(`Path:     ${chalk.cyan(agentDir)}`);
        console.log(`Modified: ${chalk.gray(stats.mtime.toLocaleString("en-US"))}`);
        console.log(`Files:    ${chalk.yellow(files.length)} items at root`);
        console.log(chalk.gray("────────────────────────────────────────\n"));
    } else {
        console.log(chalk.red("[X] Not installed"));
        console.log(chalk.yellow(`Run ${chalk.cyan("ag-kit init")} to install.\n`));
    }
};

// ============================================================================
// CLI DEFINITION
// ============================================================================
const program = new Command();

program
    .name("ag-kit")
    .description("CLI tool to install and manage Antigravity Kit")
    .version(pkg.version, "-v, --version", "Display version number");

program
    .command("init")
    .description("Install .agents folder into your project")
    .option("-f, --force", "Overwrite if folder already exists", false)
    .option("-p, --path <dir>", "Path to the project directory", process.cwd())
    .option("-b, --branch <name>", "Select repository branch")
    .option("-q, --quiet", "Suppress output (for CI/CD)", false)
    .option("--dry-run", "Show what would be done without executing", false)
    .action(initCommand);

program
    .command("update")
    .description("Update .agents folder to the latest version")
    .option("-f, --force", "Skip confirmation prompt", false)
    .option("-p, --path <dir>", "Path to the project directory", process.cwd())
    .option("-b, --branch <name>", "Select repository branch")
    .option("-q, --quiet", "Suppress output (for CI/CD)", false)
    .option("--dry-run", "Show what would be done without executing", false)
    .action(updateCommand);

program
    .command("status")
    .description("Check installation status")
    .option("-p, --path <dir>", "Path to the project directory", process.cwd())
    .action(statusCommand);

program.parse(process.argv);

if (!process.argv.slice(2).length) {
    program.outputHelp();
}
