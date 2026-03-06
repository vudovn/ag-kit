# 📖 Usage Guide: How to Actually Use These Skills

> **Confused after installation?** This guide walks you through exactly what to do next, step by step.

---

## 🤔 "I just installed the repository. Now what?"

Great question! Here's what just happened and what to do next:

### What You Just Did

When you ran `npx antigravity-awesome-skills` or cloned the repository, you:

✅ **Downloaded 954+ skill files** to your computer (default: `~/.gemini/antigravity/skills/`; or `~/.agent/skills/` if you used `--path`)  
✅ **Made them available** to your AI assistant  
❌ **Did NOT enable them all automatically** (they're just sitting there, waiting)

Think of it like installing a toolbox. You have all the tools now, but you need to **pick which ones to use** for each job.

---

## 🎯 Step 1: Understanding "Bundles" (This is NOT Another Install!)

**Common confusion:** "Do I need to download each skill separately?"

**Answer: NO!** Here's what bundles actually are:

### What Bundles Are

Bundles are **recommended lists** of skills grouped by role. They help you decide which skills to start using.

**Analogy:**

- You installed a toolbox with 954+ tools (✅ done)
- Bundles are like **labeled organizer trays** saying: "If you're a carpenter, start with these 10 tools"
- You don't install bundles—you **pick skills from them**

### What Bundles Are NOT

❌ Separate installations  
❌ Different download commands  
❌ Something you need to "activate"

### Example: The "Web Wizard" Bundle

When you see the [Web Wizard bundle](BUNDLES.md#-the-web-wizard-pack), it lists:

- `frontend-design`
- `react-best-practices`
- `tailwind-patterns`
- etc.

These are **recommendations** for which skills a web developer should try first. They're already installed—you just need to **use them in your prompts**.

---

## 🚀 Step 2: How to Actually Execute/Use a Skill

This is the part that should have been explained better! Here's how to use skills:

### The Simple Answer

**Just mention the skill name in your conversation with your AI assistant.**

### Different Tools, Different Syntax

The exact syntax varies by tool, but it's always simple:

#### Claude Code (CLI)

```bash
# In your terminal/chat with Claude Code:
>> Use @brainstorming to help me design a todo app
```

#### Cursor (IDE)

```bash
# In the Cursor chat panel:
@brainstorming help me design a todo app
```

#### Gemini CLI

```bash
# In your conversation with Gemini:
Use the brainstorming skill to help me plan my app
```

#### Codex CLI

```bash
# In your conversation with Codex:
Apply @brainstorming to design a new feature
```

#### Antigravity IDE

```bash
# In agent mode:
Use @brainstorming to plan this feature
```

> **Pro Tip:** Most modern tools use the `@skill-name` syntax. When in doubt, try that first!

---

## 💬 Step 3: What Should My Prompts Look Like?

Here are **real-world examples** of good prompts:

### Example 1: Starting a New Project

**Bad Prompt:**

> "Help me build a todo app"

**Good Prompt:**

> "Use @brainstorming to help me design a todo app with user authentication and cloud sync"

**Why it's better:** You're explicitly invoking the skill and providing context.

---

### Example 2: Reviewing Code

**Bad Prompt:**

> "Check my code"

**Good Prompt:**

> "Use @lint-and-validate to check `src/components/Button.tsx` for issues"

**Why it's better:** Specific skill + specific file = precise results.

---

### Example 3: Security Audit

**Bad Prompt:**

> "Make my API secure"

**Good Prompt:**

> "Use @api-security-best-practices to review my REST endpoints in `routes/api/users.js`"

**Why it's better:** The AI knows exactly which skill's standards to apply.

---

### Example 4: Combining Multiple Skills

**Good Prompt:**

> "Use @brainstorming to design a payment flow, then apply @stripe-integration to implement it"

**Why it's good:** You can chain skills together in a single prompt!

---

## 🎓 Step 4: Your First Skill (Hands-On Tutorial)

Let's actually use a skill right now. Follow these steps:

### Scenario: You want to plan a new feature

1. **Pick a skill:** Let's use `brainstorming` (from the "Essentials" bundle)

2. **Open your AI assistant** (Claude Code, Cursor, etc.)

3. **Type this exact prompt:**

   ```
   Use @brainstorming to help me design a user profile page for my app
   ```

4. **Press Enter**

5. **What happens next:**
   - The AI loads the brainstorming skill
   - It will start asking you structured questions (one at a time)
   - It will guide you through understanding, requirements, and design
   - You answer each question, and it builds a complete spec

6. **Result:** You'll end up with a detailed design document—without writing a single line of code yet!

---

## 🗂️ Step 5: Picking Your First Skills (Practical Advice)

Don't try to use all 954+ skills! Here's a sensible approach:

### Start with "The Essentials" (5 skills, everyone needs these)

1. **`@brainstorming`** - Plan before you build
2. **`@lint-and-validate`** - Keep code clean
3. **`@git-pushing`** - Save work safely
4. **`@systematic-debugging`** - Fix bugs faster
5. **`@concise-planning`** - Organize tasks

**How to use them:**

- Before writing new code → `@brainstorming`
- After writing code → `@lint-and-validate`
- Before committing → `@git-pushing`
- When stuck → `@systematic-debugging`

### Then Add Role-Specific Skills (5-10 more)

Find your role in [BUNDLES.md](BUNDLES.md) and pick 5-10 skills from that bundle.

**Example for Web Developer:**

- `@frontend-design`
- `@react-best-practices`
- `@tailwind-patterns`
- `@seo-audit`

**Example for Security Engineer:**

- `@api-security-best-practices`
- `@vulnerability-scanner`
- `@ethical-hacking-methodology`

### Finally, Add On-Demand Skills (as needed)

Keep the [CATALOG.md](../CATALOG.md) open as reference. When you need something specific:

> "I need to integrate Stripe payments"  
> → Search catalog → Find `@stripe-integration` → Use it!

---

## 🔄 Complete Example: Building a Feature End-to-End

Let's walk through a realistic scenario:

### Task: "Add a blog to my Next.js website"

#### Step 1: Plan (use @brainstorming)

```
You: Use @brainstorming to design a blog system for my Next.js site

AI: [Asks structured questions about requirements]
You: [Answer questions]
AI: [Produces detailed design spec]
```

#### Step 2: Implement (use @nextjs-best-practices)

```
You: Use @nextjs-best-practices to scaffold the blog with App Router

AI: [Creates file structure, sets up routes, adds components]
```

#### Step 3: Style (use @tailwind-patterns)

```
You: Use @tailwind-patterns to make the blog posts look modern

AI: [Applies Tailwind styling with responsive design]
```

#### Step 4: SEO (use @seo-audit)

```
You: Use @seo-audit to optimize the blog for search engines

AI: [Adds meta tags, sitemaps, structured data]
```

#### Step 5: Test & Deploy

```
You: Use @test-driven-development to add tests, then @vercel-deployment to deploy

AI: [Creates tests, sets up CI/CD, deploys to Vercel]
```

**Result:** Professional blog built with best practices, without manually researching each step!

---

## 🆘 Common Questions

### "Which tool should I use? Claude Code, Cursor, Gemini?"

**Any of them!** Skills work universally. Pick the tool you already use or prefer:

- **Claude Code** - Best for terminal/CLI workflows
- **Cursor** - Best for IDE integration
- **Gemini CLI** - Best for Google ecosystem
- **Codex CLI** - Best for OpenAI ecosystem

### "Can I see all available skills?"

Yes! Three ways:

1. Browse [CATALOG.md](../CATALOG.md) (searchable list)
2. Run `ls ~/.agent/skills/` (if installed there)
3. Ask your AI: "What skills do you have for [topic]?"

### "Do I need to restart my IDE after installing?"

Usually no, but if your AI doesn't recognize a skill:

1. Try restarting your IDE/CLI
2. Check the installation path matches your tool
3. Try the explicit path: `npx antigravity-awesome-skills --claude` (or `--cursor`, `--gemini`, etc.)

### "Can I create my own skills?"

Yes! Use the `@skill-creator` skill:

```
Use @skill-creator to help me build a custom skill for [your task]
```

### "What if a skill doesn't work as expected?"

1. Check the skill's SKILL.md file directly: `~/.agent/skills/[skill-name]/SKILL.md`
2. Read the description to ensure you're using it correctly
3. [Open an issue](https://github.com/sickn33/antigravity-awesome-skills/issues) with details

---

## 🎯 Quick Reference Card

**Save this for quick lookup:**

| Task             | Skill to Use                   | Example Prompt                                      |
| ---------------- | ------------------------------ | --------------------------------------------------- |
| Plan new feature | `@brainstorming`               | `Use @brainstorming to design a login system`       |
| Review code      | `@lint-and-validate`           | `Use @lint-and-validate on src/app.js`              |
| Debug issue      | `@systematic-debugging`        | `Use @systematic-debugging to fix login error`      |
| Security audit   | `@api-security-best-practices` | `Use @api-security-best-practices on my API routes` |
| SEO check        | `@seo-audit`                   | `Use @seo-audit on my landing page`                 |
| React component  | `@react-patterns`              | `Use @react-patterns to build a form component`     |
| Deploy app       | `@vercel-deployment`           | `Use @vercel-deployment to ship this to production` |

---

## 🚦 Next Steps

Now that you understand how to use skills:

1. ✅ **Try one skill right now** - Start with `@brainstorming` on any idea you have
2. 📚 **Pick 3-5 skills** from your role's bundle in [BUNDLES.md](BUNDLES.md)
3. 🔖 **Bookmark** [CATALOG.md](../CATALOG.md) for when you need something specific
4. 🎯 **Try a workflow** from [WORKFLOWS.md](WORKFLOWS.md) for a complete end-to-end process

---

## 💡 Pro Tips for Maximum Effectiveness

### Tip 1: Start Every Feature with @brainstorming

> Before writing code, use `@brainstorming` to plan. You'll save hours of refactoring.

### Tip 2: Chain Skills in Order

> Don't try to do everything at once. Use skills sequentially: Plan → Build → Test → Deploy

### Tip 3: Be Specific in Prompts

> Bad: "Use @react-patterns"  
> Good: "Use @react-patterns to build a modal component with animations"

### Tip 4: Reference File Paths

> Help the AI focus: "Use @security-auditor on routes/api/auth.js"

### Tip 5: Combine Skills for Complex Tasks

> "Use @brainstorming to design, then @test-driven-development to implement with tests"

---

## 📞 Still Confused?

If something still doesn't make sense:

1. Check the [FAQ](FAQ.md)
2. See [Real-World Examples](EXAMPLES.md)
3. [Open a Discussion](https://github.com/sickn33/antigravity-awesome-skills/discussions)
4. [File an Issue](https://github.com/sickn33/antigravity-awesome-skills/issues) to help us improve this guide!

Remember: You're not alone! The whole point of this project is to make AI assistants easier to use. If this guide didn't help, let us know so we can fix it. 🙌
