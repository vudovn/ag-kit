import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { doctorRuntime, finalizeRuntimeInstall, prepareRuntimeInstall, uninstallRuntime } from "../lib/runtime-lifecycle.js";
import { wireRuntimeMcp } from "../lib/runtime-mcp.js";

const cases = [
  { runtime: "claude", settings: ".claude/settings.json", event: "UserPromptSubmit" },
  { runtime: "gemini", settings: ".gemini/settings.json", event: "BeforeAgent" },
];

for (const { runtime, settings, event } of cases) {
  test(`${runtime} prompt hook is owned, doctorable, and surgically removable`, (t) => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), `ag-kit-${runtime}-prompt-lifecycle-`));
    t.after(() => fs.rmSync(root, { recursive: true, force: true }));

    const settingsFile = path.join(root, settings);
    fs.mkdirSync(path.dirname(settingsFile), { recursive: true });
    const initial = {
      userSetting: true,
      hooks: { Custom: [{ hooks: [{ type: "command", command: "echo user" }] }] },
      ...(runtime === "gemini" ? { mcpServers: { user: { command: "user-mcp", args: [] } } } : {}),
    };
    fs.writeFileSync(settingsFile, `${JSON.stringify(initial, null, 2)}\n`);

    const prepared = prepareRuntimeInstall({ root, runtime });
    const wired = wireRuntimeMcp({ root, runtime });
    assert.equal(wired.promptQuality?.wired, true);
    assert.equal(wired.promptQuality?.event, event);
    finalizeRuntimeInstall({ prepared, mcp: wired });

    const doctor = doctorRuntime({ root, runtime });
    const settingsCheck = doctor.checks.find((check) => check.path === settings);
    assert.ok(settingsCheck, `${runtime}: lifecycle manifest must track prompt hook settings`);
    assert.equal(settingsCheck.ok, true);
    assert.equal(settingsCheck.state, "wired");

    const installed = JSON.parse(fs.readFileSync(settingsFile, "utf8"));
    const command = `ag-kit prompt-hook ${runtime}`;
    assert.ok(installed.hooks[event].some((group) => group.hooks.some((hook) => hook.command === command)));
    assert.ok(installed.hooks.Custom.some((group) => group.hooks.some((hook) => hook.command === "echo user")));

    installed.userAfterInstall = true;
    installed.hooks.Custom.push({ hooks: [{ type: "command", command: "echo later-user-hook" }] });
    if (runtime === "gemini") installed.mcpServers.later = { command: "later-mcp", args: [] };
    fs.writeFileSync(settingsFile, `${JSON.stringify(installed, null, 2)}\n`);

    const result = uninstallRuntime({ root, runtime });
    assert.ok(["uninstalled", "uninstalled-with-preserved-drift"].includes(result.status));
    assert.equal(doctorRuntime({ root, runtime }).status, "untouched");

    const remaining = JSON.parse(fs.readFileSync(settingsFile, "utf8"));
    assert.equal(remaining.userSetting, true);
    assert.equal(remaining.userAfterInstall, true);
    assert.ok(remaining.hooks.Custom.some((group) => group.hooks.some((hook) => hook.command === "echo user")));
    assert.ok(remaining.hooks.Custom.some((group) => group.hooks.some((hook) => hook.command === "echo later-user-hook")));
    assert.equal(remaining.hooks?.[event]?.some((group) => group.hooks?.some((hook) => hook.command === command)) ?? false, false);

    if (runtime === "gemini") {
      assert.equal(Boolean(remaining.mcpServers?.["ag-kit"]), false);
      assert.equal(remaining.mcpServers.user.command, "user-mcp");
      assert.equal(remaining.mcpServers.later.command, "later-mcp");
    }
  });
}
