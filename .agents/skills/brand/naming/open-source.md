# Open Source Project Naming

Open source naming has constraints that commercial products don't face. The name IS the marketing — there's no ad budget, no sales team, no brand campaign. Word-of-mouth is the only growth channel, so the name must do more work.

---

## CLI and Import Friendliness

The name will be typed thousands of times in terminals, import statements, config files, and documentation. Every character is a cost.

**Hard constraints:**

- **Lowercase only** — package registries normalize to lowercase. Mixed case creates confusion (`MyTool` vs `mytool` vs `myTool`)
- **No special characters** — hyphens are acceptable in package names but create friction in imports. Underscores work in Python, not in npm
- **Short** — under 8 characters ideal. Developers type `import [name]`, `[name] --help`, `[name] build` hundreds of times
- **No conflicts with common CLI commands** — avoid names that shadow system commands (`test`, `run`, `check`, `build`, `make`)

**Import conventions by ecosystem:**

| Ecosystem | Convention | Example |
| --------- | ---------- | ------- |
| **npm** | lowercase, hyphens OK | `npm install vite` |
| **PyPI** | lowercase, hyphens or underscores | `pip install flask` |
| **crates.io** | lowercase, hyphens or underscores | `cargo add serde` |
| **Go** | lowercase, no separator | `go get golang.org/x/tools` |
| **RubyGems** | lowercase, hyphens | `gem install rails` |

**The terminal test:** Type the name 10 times in a row in a terminal. If your fingers stumble, the name has a problem.

---

## Package Registry Conflicts

A name available on npm might be squatted on PyPI. Check ALL registries relevant to your project before committing.

**Cross-registry check order:**

1. Primary registry for your language (npm, PyPI, crates.io, etc.)
2. GitHub organization name
3. Secondary registries (your project may get ported — check where it would land)

**Scoped packages as escape hatch:**

- npm: `@org/name` — use your org scope
- Go: `github.com/org/name` — path-based, less conflict
- Python: namespace packages (`org.name`) — less common but available

**Reality:** Single-word names on major registries are almost all taken. Plan for:

- Compound names (`fastify`, `esbuild`, `turborepo`)
- Modified words (`svelte`, `astro`, `deno`)
- Unique invented words (`bun`, `zig`, `nim`)

---

## GitHub Organization vs. Repository Naming

Two different naming decisions with different trade-offs:

**Organization name:**

- Higher SEO weight — `github.com/[name]` ranks better than `github.com/someorg/[name]`
- Harder to get — popular names are taken as orgs
- Represents the project's identity, not just one repo
- Consider: will this project have multiple repos? (core, docs, plugins, website)

**Repository name:**

- Under your org's namespace — less competitive
- Can match the package name exactly
- Can be changed later (GitHub redirects old URLs, but external links break)

**Strategy:** If the project is significant enough, try to secure the org name. If not, use your personal or org namespace and make the repo name match the package name exactly.

---

## The Conference Talk Test

Open source names get said aloud constantly — in conference talks, meetup presentations, podcast episodes, YouTube tutorials, and hallway conversations.

**The test:** Imagine saying the name 50 times in a 30-minute talk. Does it:

- Flow naturally in sentences? ("Let me show you how Vite handles this")
- Sound distinct from similar tools? (Won't be confused when spoken)
- Work as a noun, verb, or adjective? ("a Rust project", "Deno-powered", "we use Bun")

**Names that pass:**

- Rust, Deno, Vite, Bun, Zig, Svelte, Astro — all short, punchy, distinctive when spoken
- React, Vue, Solid — common words but distinctive enough in technical context

**Names that struggle:**

- Projects with numbers or special characters (hard to say naturally)
- Names that sound like other popular tools (confusion in conversation)
- Very long names that get abbreviated unpredictably

---

## Community and Word-of-Mouth

Open source adoption is driven by developers telling other developers. The name must be:

**Easy to recommend:**

> "You should try [name]" — does this sentence feel natural?

**Easy to search:**

> Searching "[name] tutorial" or "[name] vs [competitor]" — do you find the right project?

**Easy to discuss:**

> "[Name] just released 2.0" — does this feel like a real sentence?

**Fork-friendliness:**

What happens when someone forks your project? Forks often add a prefix or suffix:

- `next-[name]`, `[name]-ng`, `[name]-plus`
- If the base name is already compound or long, fork names become unwieldy

---

## Case Studies: Why Great OSS Names Work

| Name | Why it works |
| ---- | ----------- |
| **Rust** | 1 syllable. Metaphor: rust fungi are resilient, persistent organisms. CLI-friendly. Unique enough to own search results (eventually). |
| **Deno** | Anagram of "Node." 2 syllables. The connection to its predecessor is clever but the name stands alone. |
| **Vite** | French for "fast." 1 syllable. Communicates the core value proposition through the word itself. |
| **Bun** | 1 syllable. Friendly, approachable, memorable. The playful name contrasts with the serious performance focus. |
| **Zig** | 1 syllable. 3 characters. Phonetically sharp. Implies quickness and directness. |
| **Svelte** | French for "slender." The name IS the philosophy — minimal, no bloat. 1 syllable. |
| **Astro** | Space metaphor. 2 syllables. Feels modern and exploratory. Easy to type, easy to say. |
| **Esbuild** | "es" (ECMAScript) + "build." Both halves earn their place. Descriptive but specific enough. |

**Pattern:** The most successful OSS names are 1-2 syllables, globally pronounceable, and either carry a metaphor or communicate the tool's philosophy through the word itself.

---

## Open Source Naming Checklist

Before committing to a name for an open source project:

- [ ] Can you type it 10 times fast without errors?
- [ ] Is it available on your primary package registry?
- [ ] Is the GitHub org or repo name available?
- [ ] Can you say it naturally in a conference talk?
- [ ] Does it work as an import/require statement?
- [ ] Is it searchable? (First page of results for "[name] [category]")
- [ ] Would someone remember it after hearing it once at a meetup?
- [ ] Does it work when forked? (Adding prefixes/suffixes doesn't make it absurd)
- [ ] Is it lowercase-friendly? (No mixed case dependencies)
- [ ] Does it avoid shadowing common CLI commands?
