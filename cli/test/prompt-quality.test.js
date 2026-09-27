import test from "node:test";
import assert from "node:assert/strict";
import { checkPromptQuality } from "../lib/prompt-quality.js";

const needsContext = [
  "fix",
  "fix it",
  "make this better",
  "deploy",
  "review the issue",
  "update everything",
];

const clear = [
  "fix cli/lib/foo.js",
  "review PR #124",
  "test login",
  "debug auth failure in login",
  "improve performance of `recallMemory`",
  "update issue #42 without changing the API contract",
];

test("prompt quality flags only multi-signal underspecified tasks", () => {
  for (const prompt of needsContext) {
    const result = checkPromptQuality(prompt);
    assert.equal(result.status, "needs-context", prompt);
    assert.equal(result.ok, false, prompt);
    assert.ok(result.signals.length >= 2, prompt);
    assert.ok(result.questions.length >= 1 && result.questions.length <= 3, prompt);
  }
});

test("prompt quality permits short prompts with a concrete target", () => {
  for (const prompt of clear) {
    const result = checkPromptQuality(prompt);
    assert.equal(result.status, "clear", `${prompt}: ${JSON.stringify(result)}`);
    assert.equal(result.ok, true, prompt);
    assert.equal(result.questions.length, 0, prompt);
  }
});

test("prompt quality never returns or stores the raw prompt", () => {
  const secret = "fix it secret-token-123";
  const result = checkPromptQuality(secret);
  assert.equal(JSON.stringify(result).includes(secret), false);
  assert.deepEqual(Object.keys(result.metadata).sort(), ["characters", "hasTarget", "tokens"]);
});

test("explicit bypass is auditable without preserving prompt content", () => {
  const result = checkPromptQuality("fix it", { force: true });
  assert.equal(result.status, "bypassed");
  assert.equal(result.ok, true);
  assert.equal(result.metadata.characters, 6);
  assert.equal("hasTarget" in result.metadata, false);
});
