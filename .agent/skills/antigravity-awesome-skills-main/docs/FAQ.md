# ❓ Frequently Asked Questions (FAQ)

**Got questions?** You're not alone! Here are answers to the most common questions about Antigravity Awesome Skills.

---

## 🎯 General Questions

### What are "skills" exactly?

Skills are specialized instruction files that teach AI assistants how to handle specific tasks. Think of them as expert knowledge modules that your AI can load on-demand.
**Simple analogy:** Just like you might consult different experts (a lawyer, a doctor, a mechanic), these skills let your AI become an expert in different areas when you need them.

### Do I need to install all 700+ skills?

**No!** When you clone the repository, all skills are available, but your AI only loads them when you explicitly invoke them with `@skill-name`.
It's like having a library - all books are there, but you only read the ones you need.
**Pro Tip:** Use [Starter Packs](BUNDLES.md) to install only what matches your role.

### What is the difference between Bundles and Workflows?

- **Bundles** are curated recommendations grouped by role or domain.
- **Workflows** are ordered execution playbooks for concrete outcomes.

Use bundles when you are deciding *which skills* to include. Use workflows when you need *step-by-step execution*.

Start from:
- [BUNDLES.md](BUNDLES.md)
- [WORKFLOWS.md](WORKFLOWS.md)

### Which AI tools work with these skills?

- ✅ **Claude Code** (Anthropic CLI)
- ✅ **Gemini CLI** (Google)
- ✅ **Codex CLI** (OpenAI)
- ✅ **Cursor** (AI IDE)
- ✅ **Antigravity IDE**
- ✅ **OpenCode**
- ⚠️ **GitHub Copilot** (partial support via copy-paste)

### Are these skills free to use?

**Yes!** This repository is licensed under MIT License.

- ✅ Free for personal use
- ✅ Free for commercial use
- ✅ You can modify them

### Do skills work offline?

The skill files themselves are stored locally on your computer, but your AI assistant needs an internet connection to function.

---

## 🔒 Security & Trust (V4 Update)

### What do the Risk Labels mean?

We classify skills so you know what you're running:

- ⚪ **Safe (White/Blue)**: Read-only, planning, or benign skills.
- 🔴 **Risk (Red)**: Skills that modify files (delete), use network scanners, or perform destructive actions. **Use with caution.**
- 🟣 **Official (Purple)**: Maintained by trusted vendors (Anthropic, DeepMind, etc.).

### Can these skills hack my computer?

**No.** Skills are text files. However, they _instruct_ the AI to run commands. If a skill says "delete all files", a compliant AI might try to do it.
_Always check the Risk label and review the code._

---

## 📦 Installation & Setup

### Where should I install the skills?

The universal path that works with most tools is `.agent/skills/`.

**Using npx:** `npx antigravity-awesome-skills` (or `npx github:sickn33/antigravity-awesome-skills` if you get a 404).

**Using git clone:**

```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

**Tool-specific paths:**

- Claude Code: `.claude/skills/`
- Gemini CLI: `.gemini/skills/`
- Codex CLI: `.codex/skills/`
- Cursor: `.cursor/skills/` or project root

### Does this work with Windows?

**Yes**, but some "Official" skills use **symlinks** which Windows handles poorly by default.
Run git with:

```bash
git clone -c core.symlinks=true https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

Or enable "Developer Mode" in Windows Settings.

### How do I update skills?

Navigate to your skills directory and pull the latest changes:

```bash
cd .agent/skills
git pull origin main
```

---

## 🛠️ Using Skills

> **💡 For a complete guide with examples, see [USAGE.md](USAGE.md)**

### How do I invoke a skill?

Use the `@` symbol followed by the skill name:

```bash
@brainstorming help me design a todo app
```

### Can I use multiple skills at once?

**Yes!** You can invoke multiple skills:

```bash
@brainstorming help me design this, then use @writing-plans to create a task list.
```

### How do I know which skill to use?

1. **Browse the catalog**: Check the [Skill Catalog](../CATALOG.md).
2. **Search**: `ls skills/ | grep "keyword"`
3. **Ask your AI**: "What skills do you have for testing?"

---

## 🏗️ Troubleshooting

### My AI assistant doesn't recognize skills

**Possible causes:**

1. **Wrong installation path**: Check your tool's docs. Try `.agent/skills/`.
2. **Restart Needed**: Restart your AI/IDE after installing.
3. **Typos**: Did you type `@brain-storming` instead of `@brainstorming`?

### A skill gives incorrect or outdated advice

Please [Open an issue](https://github.com/sickn33/antigravity-awesome-skills/issues)!
Include:

- Which skill
- What went wrong
- What should happen instead

---

## 🤝 Contribution

### I'm new to open source. Can I contribute?

**Absolutely!** We welcome beginners.

- Fix typos
- Add examples
- Improve docs
  Check out [CONTRIBUTING.md](../CONTRIBUTING.md) for instructions.

### My PR failed "Quality Bar" check. Why?

V4 introduces automated quality control. Your skill might be missing:

1. A valid `description`.
2. Usage examples.
   Run `python3 scripts/validate_skills.py` locally to check before you push.

### Can I update an "Official" skill?

**No.** Official skills (in `skills/official/`) are mirrored from vendors. Open an issue instead.

---

## 💡 Pro Tips

- Start with `@brainstorming` before building anything new
- Use `@systematic-debugging` when stuck on bugs
- Try `@test-driven-development` for better code quality
- Explore `@skill-creator` to make your own skills

**Still confused?** [Open a discussion](https://github.com/sickn33/antigravity-awesome-skills/discussions) and we'll help you out! 🙌
