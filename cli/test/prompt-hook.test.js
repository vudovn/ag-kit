import test from "node:test";
import assert from "node:assert/strict";
import { promptHookEnvelope } from "../lib/prompt-hook.js";

test("Gemini BeforeAgent injects clarification context without blocking the turn", () => {
  const result = promptHookEnvelope("gemini", { prompt: "fix it" });
  assert.equal(result.decision, "allow");
  assert.equal(result.hookSpecificOutput.hookEventName, "BeforeAgent");
  assert.match(result.hookSpecificOutput.additionalContext, /Do not guess/i);
  assert.equal(result.hookSpecificOutput.additionalContext.includes("fix it"), false);
});

test("Claude UserPromptSubmit accepts both current prompt field spellings", () => {
  for (const payload of [{ user_prompt: "make this better" }, { prompt: "make this better" }]) {
    const result = promptHookEnvelope("claude", payload);
    assert.equal(result.continue, true);
    assert.equal(result.suppressOutput, true);
    assert.equal(result.hookSpecificOutput.hookEventName, "UserPromptSubmit");
    assert.match(result.hookSpecificOutput.additionalContext, /ask one concise clarification/i);
  }
});

test("clear prompts produce no injected prompt-quality context", () => {
  assert.deepEqual(promptHookEnvelope("gemini", { prompt: "review PR #124" }), { decision: "allow" });
  assert.deepEqual(promptHookEnvelope("claude", { user_prompt: "fix cli/lib/foo.js" }), { continue: true, suppressOutput: true });
});

test("unsupported hosts are rejected instead of guessing a hook protocol", () => {
  assert.throws(() => promptHookEnvelope("codex", { prompt: "fix it" }), /unsupported prompt hook runtime/);
});
