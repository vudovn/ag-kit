const MAX_PROMPT_CHARS = 16 * 1024;
const ACTIONS = new Set(["fix", "refactor", "improve", "clean", "cleanup", "optimize", "update", "review", "check", "test", "debug", "analyze", "handle", "tidy"]);
const VAGUE_OBJECTS = new Set(["it", "this", "that", "these", "those", "thing", "things", "stuff", "issue", "problem", "bug", "code", "file", "files", "everything"]);

const words = (text) => String(text || "").trim().match(/[A-Za-z0-9_./:#@-]+/g) || [];
const normalize = (text) => String(text || "").trim();

const hasExplicitTarget = (text, tokens) => {
  if (/https?:\/\/\S+/i.test(text)) return true;
  if (/\b(?:PR|issue|ticket)\s*#?\d+\b/i.test(text) || /#\d+\b/.test(text)) return true;
  if (/\b[\w.-]+\/[\w./-]+\b/.test(text) || /\b[\w.-]+\.[A-Za-z0-9]{1,8}(?::\d+)?\b/.test(text)) return true;
  if (/`[^`]{2,}`/.test(text) || /\b[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+\b/.test(text)) return true;
  if (/\b[A-Za-z_$][\w$]*\([^)]*\)/.test(text)) return true;

  const first = (tokens[0] || "").toLowerCase();
  if (ACTIONS.has(first) && tokens.length >= 2) {
    const object = tokens[1].toLowerCase().replace(/[^a-z0-9_-]/g, "");
    if (object && !VAGUE_OBJECTS.has(object)) return true;
  }
  return false;
};

const questionPack = (signals) => {
  const questions = [];
  const add = (value) => { if (!questions.includes(value) && questions.length < 3) questions.push(value); };
  if (signals.includes("missing-target") || signals.includes("bare-action")) add("Which file, symbol, feature, test, PR, or issue is the target?");
  if (signals.includes("unbound-reference")) add("What does “this/that/it” refer to in concrete terms?");
  if (signals.includes("vague-outcome")) add("What observable result or acceptance check would count as done?");
  if (signals.includes("broad-scope")) add("Which concrete subset should be changed first?");
  if (signals.includes("ambiguous-operation")) add("What outcome do you mean by that operation: build, run, release, or deploy where?");
  if (!questions.length) add("What concrete target or acceptance condition should anchor the task?");
  return questions;
};

export function checkPromptQuality(input, { force = false } = {}) {
  const text = normalize(input);
  const tokens = words(text);
  const metadata = { characters: text.length, tokens: tokens.length };

  if (force) return { schema: 1, ok: true, status: "bypassed", signals: [], questions: [], summary: "Prompt quality check bypassed explicitly.", metadata };
  if (!text) return { schema: 1, ok: false, status: "needs-context", signals: ["empty"], questions: ["What would you like AG Kit to do?"], summary: "No task context was supplied.", metadata };
  if (text.length > MAX_PROMPT_CHARS || /```[\s\S]*```/.test(text)) {
    return { schema: 1, ok: true, status: "clear", signals: [], questions: [], summary: "Prompt contains substantial explicit context.", metadata: { ...metadata, bypass: text.length > MAX_PROMPT_CHARS ? "long-context" : "fenced-context" } };
  }

  const lower = text.toLowerCase();
  const signals = [];
  const hasTarget = hasExplicitTarget(text, tokens);
  const first = (tokens[0] || "").toLowerCase();
  const second = (tokens[1] || "").toLowerCase().replace(/[^a-z0-9_-]/g, "");

  if (!hasTarget) signals.push("missing-target");
  if (ACTIONS.has(first) && (tokens.length === 1 || VAGUE_OBJECTS.has(second))) signals.push("bare-action");
  if (/^(?:this|that|it|these|those)\b/i.test(text) || /^(?:the\s+)?(?:issue|problem|bug)\b/i.test(text)) signals.push("unbound-reference");
  if (/\b(?:make\s+(?:it|this|that)\s+)?(?:better|cleaner|nicer|proper|correct|production[- ]ready)|\bfix\s+(?:it|this|that)\s+(?:properly|right)\b/i.test(lower)) signals.push("vague-outcome");
  if (/\b(?:everything|stuff|things|all\s+(?:the\s+)?(?:files|tests|code|issues))\b/i.test(lower)) signals.push("broad-scope");
  if (/^(?:build|run|deploy|ship|release|setup|set\s+up)\.?$/i.test(text)) signals.push("ambiguous-operation");

  const uniqueSignals = [...new Set(signals)];
  const needsContext = tokens.length < 30 && !hasTarget && uniqueSignals.length >= 2;
  return {
    schema: 1,
    ok: !needsContext,
    status: needsContext ? "needs-context" : "clear",
    signals: uniqueSignals,
    questions: needsContext ? questionPack(uniqueSignals) : [],
    summary: needsContext
      ? "The task is underspecified enough that guessing could change the requested scope or outcome."
      : "The prompt has enough concrete context to proceed without a prompt-quality interruption.",
    metadata: { ...metadata, hasTarget },
  };
}

export const PROMPT_QUALITY_MAX_CHARS = MAX_PROMPT_CHARS;
