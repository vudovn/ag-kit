# Getting Started with Antigravity Awesome Skills (V6.5.0)

**New here? This guide will help you supercharge your AI Agent in 5 minutes.**

> **💡 Confused about what to do after installation?** Check out the [**Complete Usage Guide**](USAGE.md) for detailed explanations and examples!

---

## 🤔 What Are "Skills"?

AI Agents (like **Claude Code**, **Gemini**, **Cursor**) are smart, but they lack specific knowledge about your tools.
**Skills** are specialized instruction manuals (markdown files) that teach your AI how to perform specific tasks perfectly, every time.

**Analogy:** Your AI is a brilliant intern. **Skills** are the SOPs (Standard Operating Procedures) that make them a Senior Engineer.

---

## ⚡️ Quick Start: The "Starter Packs"

Don't panic about the 954+ skills. You don't need them all at once.
We have curated **Starter Packs** to get you running immediately.

You **install the full repo once** (npx or clone); Starter Packs are curated lists to help you **pick which skills to use** by role (e.g. Web Wizard, Hacker Pack)—they are not a different way to install.

### 1. Install the Repo

**Option A — npx (easiest):**

```bash
npx antigravity-awesome-skills
```

This clones to `~/.gemini/antigravity/skills` by default. Use `--cursor`, `--claude`, `--gemini`, `--codex`, or `--kiro` to install for a specific tool, or `--path <dir>` for a custom location. Run `npx antigravity-awesome-skills --help` for details.

If you see a 404 error, use: `npx github:sickn33/antigravity-awesome-skills`

**Option B — git clone:**

```bash
# Universal (works for most agents)
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### 2. Pick Your Persona

Find the bundle that matches your role (see [BUNDLES.md](BUNDLES.md)):

| Persona               | Bundle Name    | What's Inside?                                    |
| :-------------------- | :------------- | :------------------------------------------------ |
| **Web Developer**     | `Web Wizard`   | React Patterns, Tailwind mastery, Frontend Design |
| **Security Engineer** | `Hacker Pack`  | OWASP, Metasploit, Pentest Methodology            |
| **Manager / PM**      | `Product Pack` | Brainstorming, Planning, SEO, Strategy            |
| **Everything**        | `Essentials`   | Clean Code, Planning, Validation (The Basics)     |

---

## 🧭 Bundles vs Workflows

Bundles and workflows solve different problems:

- **Bundles** = curated sets by role (what to pick).
- **Workflows** = step-by-step playbooks (how to execute).

Start with bundles in [BUNDLES.md](BUNDLES.md), then run a workflow from [WORKFLOWS.md](WORKFLOWS.md) when you need guided execution.

Example:

> "Use **@antigravity-workflows** and run `ship-saas-mvp` for my project idea."

---

## 🚀 How to Use a Skill

Once installed, just talk to your AI naturally.

### Example 1: Planning a Feature (**Essentials**)

> "Use **@brainstorming** to help me design a new login flow."

**What happens:** The AI loads the brainstorming skill, asks you structured questions, and produces a professional spec.

### Example 2: Checking Your Code (**Web Wizard**)

> "Run **@lint-and-validate** on this file and fix errors."

**What happens:** The AI follows strict linting rules defined in the skill to clean your code.

### Example 3: Security Audit (**Hacker Pack**)

> "Use **@api-security-best-practices** to review my API endpoints."

**What happens:** The AI audits your code against OWASP standards.

---

## 🔌 Supported Tools

| Tool            | Status          | Path                                                                  |
| :-------------- | :-------------- | :-------------------------------------------------------------------- |
| **Claude Code** | ✅ Full Support | `.claude/skills/`                                                     |
| **Gemini CLI**  | ✅ Full Support | `.gemini/skills/`                                                     |
| **Codex CLI**   | ✅ Full Support | `.codex/skills/`                                                      |
| **Kiro CLI**    | ✅ Full Support | Global: `~/.kiro/skills/` · Workspace: `.kiro/skills/`                |
| **Kiro IDE**    | ✅ Full Support | Global: `~/.kiro/skills/` · Workspace: `.kiro/skills/`                |
| **Antigravity** | ✅ Native       | Global: `~/.gemini/antigravity/skills/` · Workspace: `.agent/skills/` |
| **Cursor**      | ✅ Native       | `.cursor/skills/`                                                     |
| **OpenCode**    | ✅ Full Support | `.agents/skills/`                                                     |
| **AdaL CLI**    | ✅ Full Support | `.adal/skills/`                                                       |
| **Copilot**     | ⚠️ Text Only    | Manual copy-paste                                                     |

---

## 🛡️ Trust & Safety (New in V4)

We classify skills so you know what you're running:

- 🟣 **Official**: Maintained by Anthropic/Google/Vendors (High Trust).
- 🔵 **Safe**: Community skills that are non-destructive (Read-only/Planning).
- 🔴 **Risk**: Skills that modify systems or perform security tests (Authorized Use Only).

_Check the [Skill Catalog](../CATALOG.md) for the full list._

---

## ❓ FAQ

**Q: Do I need to install all 954+ skills?**
A: You clone the whole repo once; your AI only _reads_ the skills you invoke (or that are relevant), so it stays lightweight. **Starter Packs** in [BUNDLES.md](BUNDLES.md) are curated lists to help you discover the right skills for your role—they don't change how you install.

**Q: Can I make my own skills?**
A: Yes! Use the **@skill-creator** skill to build your own.

**Q: Is this free?**
A: Yes, MIT License. Open Source forever.

---

## ⏭️ Next Steps

1. [Browse the Bundles](BUNDLES.md)
2. [See Real-World Examples](EXAMPLES.md)
3. [Contribute a Skill](../CONTRIBUTING.md)
