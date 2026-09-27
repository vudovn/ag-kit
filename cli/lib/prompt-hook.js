import { checkPromptQuality } from "./prompt-quality.js";

const MAX_STDIN_BYTES = 256 * 1024;
const SUPPORTED = new Set(["claude", "gemini"]);

const additionalContext = (result) => [
  "<ag-kit-prompt-quality>",
  "The request may be underspecified. Do not guess missing scope or acceptance criteria.",
  "First recover context from the current conversation or project when that is safe and obvious; otherwise ask one concise clarification before making changes.",
  ...result.questions.map((question) => `- ${question}`),
  `Signals: ${result.signals.join(", ")}`,
  "</ag-kit-prompt-quality>",
].join("\n");

export function promptHookEnvelope(runtime, payload = {}) {
  if (!SUPPORTED.has(runtime)) throw new Error(`unsupported prompt hook runtime: ${runtime}`);
  const prompt = String(payload.prompt ?? payload.user_prompt ?? "");
  const result = checkPromptQuality(prompt);

  if (runtime === "gemini") {
    if (result.ok) return { decision: "allow" };
    return {
      decision: "allow",
      hookSpecificOutput: {
        hookEventName: "BeforeAgent",
        additionalContext: additionalContext(result),
      },
    };
  }

  if (result.ok) return { continue: true, suppressOutput: true };
  return {
    continue: true,
    suppressOutput: true,
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: additionalContext(result),
    },
  };
}

const readBoundedStdin = async (stream = process.stdin) => {
  const chunks = [];
  let size = 0;
  for await (const chunk of stream) {
    const buffer = Buffer.from(chunk);
    size += buffer.length;
    if (size > MAX_STDIN_BYTES) throw new Error(`prompt hook input exceeds ${MAX_STDIN_BYTES} bytes`);
    chunks.push(buffer);
  }
  return Buffer.concat(chunks).toString("utf8");
};

export async function runPromptHookCli(argv = process.argv) {
  const runtime = String(argv[3] || "").toLowerCase();
  if (!SUPPORTED.has(runtime)) throw new Error("usage: ag-kit prompt-hook <claude|gemini>");
  try {
    const raw = await readBoundedStdin();
    const payload = raw.trim() ? JSON.parse(raw) : {};
    process.stdout.write(`${JSON.stringify(promptHookEnvelope(runtime, payload))}\n`);
  } catch {
    const fallback = runtime === "gemini" ? { decision: "allow" } : { continue: true, suppressOutput: true };
    process.stdout.write(`${JSON.stringify(fallback)}\n`);
  }
}

export const PROMPT_HOOK_MAX_STDIN_BYTES = MAX_STDIN_BYTES;
