---
name: prompt-engineering
description: Advanced prompt engineering techniques for LLMs — CoT, ToT, ReAct, few-shot, system prompt design, and prompt evaluation. Load this skill when building any AI-powered feature or agent.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Prompt Engineering Skill

> Master the art of communicating with language models to get reliable, high-quality outputs.

---

## Core Prompting Techniques

| Technique | When to Use | Key Pattern |
|-----------|-------------|-------------|
| **Zero-shot** | Simple, well-defined tasks | Direct instruction only |
| **Few-shot** | Consistent format needed | 3-5 examples before the task |
| **Chain-of-Thought** | Math, logic, reasoning | "Think step by step" |
| **Tree-of-Thought** | Creative/complex planning | Generate → Evaluate → Select |
| **ReAct** | Agentic tool use | Thought → Action → Observation |
| **Self-Consistency** | Factual reliability | Generate N → Vote |

---

## System Prompt Template

```markdown
You are [SPECIFIC ROLE with personality and expertise].

## Objective
[ONE sentence: what you must do]

## Constraints (never violate)
- [Hard rule 1]
- [Hard rule 2]
- When uncertain → say "I don't know" rather than guessing

## Output Format
[Exact format specification with an example]

## Examples
User: [example]
Assistant: [ideal response]
```

---

## Anti-Hallucination Rules

```
1. Always ground answers in provided context
2. Use "Based on [source]..." to show grounding
3. Explicit uncertainty: "I'm not certain, but..."
4. Add: "If this information is critical, please verify with [source]"
5. Never extrapolate beyond what the context states
```

---

## Prompt Testing Checklist

- [ ] Happy path works
- [ ] Empty/null input handled
- [ ] Very long input handled (truncation?)
- [ ] Off-topic input rejected appropriately
- [ ] Adversarial/injection attempts blocked
- [ ] Output format always matches spec
- [ ] Tested with 10+ examples
