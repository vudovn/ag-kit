---
name: universal-rules
description: Always-active rules for language handling, clean code, and STE output tone
priority: 0
version: 1.0.0
trigger: always_on
globs: "*"
alwaysApply: true
---

# Universal Rules (TIER 0) - AG Kit

> Always-active rules that apply to every request, regardless of domain.

---

## 🌐 Language Handling

When user's prompt is NOT in English:

1. **Internally translate** for better comprehension
2. **Respond in user's language** - match their communication
3. **Code comments/variables** remain in English

---

## 🧹 Clean Code (Global Mandatory)

**ALL code MUST follow `@[skills/clean-code]` rules. No exceptions.**

- **Code**: Concise, direct, no over-engineering. Self-documenting.
- **Testing**: Mandatory. Pyramid (Unit > Int > E2E) + AAA Pattern.
- **Performance**: Measure first. Adhere to current Core Web Vitals standards.
- **Infra/Safety**: 5-Phase Deployment. Verify secrets security.

---

## ✍️ Output Tone & Technical Writing

**ALL English documentation, code comments, commit messages, and technical explanations MUST follow `@[skills/simple-english]`.**

- Apply ASD-STE100 rules: max 20 words/instruction, active voice, simple tenses, no AI filler/buzzwords.
- When responding in a non-English language, maintain STE principles: direct structure, active voice, and zero fluff.