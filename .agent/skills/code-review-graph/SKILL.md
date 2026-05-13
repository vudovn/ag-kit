---
name: code-review-graph
description: Token-efficient code review using Tree-sitter AST graphs and MCP. Reduces AI assistant token usage by 6.8–49x by computing blast radius of changes instead of reading entire codebases. Uses SQLite graph database for structural analysis.
when_to_use: "When reviewing code in large codebases (500+ files), when token costs are high, when making multi-file changes with cross-module dependencies, or when working with monorepos. Also for dead code detection, architecture visualization, and refactoring previews. NOT for small projects under 200 files with isolated single-file changes."
allowed-tools: Read, Grep, Glob, Bash
effort: medium
---

# Code Review Graph — Token-Efficient Codebase Context via MCP

> Reduce AI token usage by **6.8x average** (up to **49x** on monorepos) by giving the AI a structural map of your codebase instead of letting it read everything.

## Overview

`code-review-graph` is an MCP server that uses **Tree-sitter** to parse your codebase into an AST graph stored in **SQLite**. When your AI assistant needs context for a task, it queries the graph first — getting only the files in the **blast radius** of your change — instead of reading every file in the directory.

**Token Impact:**

| Codebase Type | Without Graph | With Graph | Reduction |
|---------------|---------------|------------|-----------|
| FastAPI (3K files) | 138,585 tokens | 37,217 tokens | **3.7x** |
| httpx | 64,666 tokens | 14,090 tokens | **4.6x** |
| Next.js monorepo (27K files) | 739,352 tokens | 15,049 tokens | **49.1x** |
| Express.js (small) | Less benefit | Graph overhead > savings | **~1x** |
| **Average across 6 repos** | — | — | **8.2x** |

> **Quality also improves:** Graph-assisted reviews score **8.8/10** vs **7.2/10** for naive reviews. Less noise = better signal = more accurate output.

## 🛑 Auto-Bootstrap Protocol (MANDATORY TOOL USE For AI Agents)

When invoked during `/plan` or standard usage on a mid-to-large project, **proactively check** if the user can benefit from graph analysis:
1. **Step 1:** You MUST explicitly use your terminal/bash execution tool to run a quick check: `Get-Command code-review-graph` (Windows) or `which code-review-graph` (macOS/Linux).
2. **Step 2:** Check if `.code-review-graph/` directory exists in the workspace.
3. **Step 3:** If the exit code is 0 (INSTALLED) but the index does not exist, **you MUST use your terminal tool to auto-execute** `code-review-graph build` to proactively optimize your token usage before reading multi-file contexts.
4. **Step 4:** If exit code is non-zero (NOT INSTALLED) and the project is large, **proactively ask the user**: "Would you like me to run `pip install code-review-graph` to build a local map and optimize your token usage by ~8x for this project?"

---

## When to Use vs When to Skip

### ✅ Install it if:
- Codebase is **500+ files**
- You make **multi-file changes** with cross-module dependencies
- You spend **$20+/month** on AI assistant tokens
- You work with **monorepos**, microservices, or cross-package TypeScript
- You want **better review quality** in addition to cost savings

### ❌ Skip it if:
- Codebase is **under ~200 files** with isolated single-file changes
- Heavy use of **dynamic patterns** (reflection, runtime code gen, dynamic imports)
- You want **zero-maintenance** — the graph needs to stay in sync
- Team hasn't standardized on an AI coding tool yet

### ⚠️ Evaluate first if:
- Codebase is **200–500 files** — benchmark before committing
- Mix of **static and dynamic patterns** — test on representative commits

---

## How It Works (4 Layers)

```
Layer 1: PARSE    → Tree-sitter builds ASTs from 19 languages
Layer 2: STORE    → Nodes + edges saved in SQLite graph
Layer 3: TRACE    → BFS computes blast radius of changes
Layer 4: SERVE    → MCP exposes graph to AI assistants
```

### What the Graph Contains
- **Nodes:** Files, functions, methods, classes, imports, tests
- **Edges:** "A calls B", "X imports Y", "TestZ covers FunctionW", "ClassA extends ClassB"
- **Metadata:** Name, type, file path, line range per node
- **Privacy:** Structural metadata only — NO source code content in the graph

### Supported Languages (19)
Python, TypeScript, JavaScript, Go, Rust, Java, C#, Ruby, Kotlin, Swift, PHP, C/C++, Vue SFC, Solidity, Dart, R, Perl, Lua, Jupyter/Databricks notebooks.

---

## Installation

### Prerequisites
- Python 3.9+ (`python3 --version`)
- pip or pipx installed
- An MCP-compatible AI client (AG Kit, Claude Code, Cursor, Windsurf, Zed)
- Git-tracked codebase (for incremental updates)

### Step 1: Install the Package

```bash
# Recommended: isolated environment
pipx install code-review-graph

# Alternative: fastest, no permanent install
uvx code-review-graph install

# Alternative: global pip
pip install code-review-graph
```

### Step 2: Configure MCP Client

```bash
# Auto-detect all supported tools
code-review-graph install

# Or target a specific platform
code-review-graph install --platform claude-code
code-review-graph install --platform cursor
code-review-graph install --platform windsurf
```

> **Restart your editor** after this step. The MCP server activates on restart.

### Step 3: Build the Initial Graph

```bash
cd /your/project
code-review-graph build
```

| Codebase Size | Expected Build Time |
|---------------|---------------------|
| 500 files | 10–30 seconds |
| 5,000 files | 2–5 minutes |
| 27,000 files | 5–10 minutes |

### Step 4: Enable Watch Mode (Recommended)

```bash
# Keep graph current as you work
code-review-graph watch
```

Incremental updates complete in **under 2 seconds**. If you prefer manual updates:

```bash
code-review-graph update
```

### Step 5: Verify Integration

Open your AI client and check MCP connection. For Claude Code: run `/mcp` and confirm `code-review-graph` appears.

---

## Configuration

### Ignore File

Create `.code-review-graphignore` at project root (uses `.gitignore` syntax):

```
# Build artifacts
dist/**
.next/**
build/**

# Dependencies
node_modules/**
vendor/**

# Generated files
generated/**
*.generated.ts
*.min.js

# Test fixtures (if large)
__fixtures__/**
```

> Excluding generated files and build artifacts is critical — they inflate the graph with meaningless nodes.

### Multi-Repo Setup

For microservice architectures:

```bash
# Register additional repos
code-review-graph register /path/to/other/repo

# List all registered repos
code-review-graph repos
```

The MCP server serves context across all registered repositories.

---

## Core Workflows

### 1. Blast Radius Analysis (Primary Use)

This is automatic when the MCP server is active. Your AI assistant queries the graph before reading files, getting only the impacted files instead of everything.

```
Without graph:  Changed auth/middleware.py → AI reads 200+ files → 8,200 tokens
With graph:     Changed auth/middleware.py → Graph returns 12 impacted files → 1,000 tokens
```

### 2. Risk-Scored Change Analysis

```bash
code-review-graph detect-changes
```

Scores each uncommitted change by risk level:
- Number of dependents
- Test coverage gaps
- Whether changed functions are on critical paths
- High-risk changes flagged **before** you ask for review

### 3. Dead Code Detection

The graph finds nodes with **no incoming edges** — no callers, no importers, no test coverage:

```bash
# Surfaces functions/classes that are candidates for removal
# Useful on mature codebases to reduce cruft
```

### 4. Refactoring Preview

```bash
code-review-graph rename preview --from OldClassName --to NewClassName
```

Shows every file affected by a rename, and flags edge cases (dynamic string references that static analysis can't catch).

### 5. Architecture Visualization

```bash
code-review-graph visualize
```

Generates interactive visualization showing module clusters using community detection (Leiden algorithm). Useful for:
- Onboarding new contributors
- Identifying architectural drift
- Spotting overly-coupled modules

### 6. Wiki Generation

```bash
code-review-graph wiki
```

Generates markdown wiki of codebase structure — every module, its public API, dependencies, and test coverage.

---

## Known Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| **Dynamic imports** (`require(variable)`, `import(buildPath())`) | Dependencies invisible to parser | Manually note in `.code-review-graphignore` or accept over-prediction |
| **Reflection-based calls** (Django signals, `getattr()`, Java reflection) | Missed edges in graph | Serena (LSP-based) is better for these codebases |
| **Runtime-generated code** (`eval`, template engines) | Not parseable at static time | Accept limitation or exclude from graph |
| **Cross-language boundaries** (Python calling TypeScript API) | No edges between language runtimes | Use multi-repo registration as partial workaround |
| **Stale graph** (without watch mode) | Claude queries outdated relationships | Always run `code-review-graph update` before tasks, or use watch mode |
| **TypeScript path aliases** (`@/components/...`) | May require tsconfig resolution config | Check `tsconfig_resolver.py` handles your setup |

---

## Alternatives Comparison

| Tool | Approach | Pros | Cons | Best For |
|------|----------|------|------|----------|
| **code-review-graph** | Tree-sitter + SQLite | Fast, 19 languages, local, no deps | Static analysis only | General use, large codebases |
| **Claudette** | Go rewrite | Single binary, no Python | Fewer languages, simpler | Python-averse teams |
| **Serena** | LSP-based | Deep semantic precision, type resolution | Heavy setup, slower | Polymorphism-heavy codebases |
| **code-graph-rag** | RAG + vector search | Natural language queries | Complex setup | Codebase exploration |
| **Native IDE context** | Editor built-in | Zero setup | No explicit blast radius | Simple projects |

---

## Integration with AG Kit

### Complementary Skills

| AG Kit Skill | How It Complements |
|-------------------|--------------------|
| `context-compression` | Graph reduces input context; compression reduces output verbosity |
| `coordinator-mode` | Graph-aware workers can be dispatched with precise file lists |
| `verify-changes` | After graph-informed review, verify changes via execution |
| `batch-operations` | Graph's blast radius informs which files need batch updates |

### Recommended Session Architecture

```
1. Start fresh session for each distinct task
2. Graph pre-filters context → AI reads only blast radius
3. Context compression summarizes completed phases
4. Memory system saves key decisions for next session
5. Result: minimum tokens, maximum quality
```

---

## Best Practices

1. **Always run watch mode** in development — stale graphs produce stale context
2. **Exclude generated files** — they inflate the graph with noise
3. **Benchmark first** — measure token usage for 1 week without, 1 week with
4. **Combine with output constraints** — graph reduces input, prompt engineering reduces output
5. **Use `.code-review-graphignore`** for build artifacts, `node_modules`, `dist/`
6. **Keep sessions short** — fresh sessions + graph = optimal token efficiency
7. **Multi-repo registration** for microservice architectures
