# Changelog

All notable changes to AG Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/).
Starting with `2026.5.13`, this project uses calendar versioning in `YYYY.M.D` format.

## [Unreleased]

No unreleased changes.

## [2026.5.13] - 2026-05-13

### Added
- **Code Review Graph Skill**: Added a skill for token-efficient code review using Tree-sitter AST graphs and MCP blast radius analysis. It documents installation, workflow usage, alternatives, and token-savings scenarios for large codebases.
- **New AG Kit logo**: Added a new AG Kit brand mark as both PNG and SVG assets for the website and Open Graph metadata.

### Changed
- **Release versioning**: Switched project releases from semantic versioning to calendar versioning in `YYYY.M.D` format. The first calendar-versioned release is `2026.5.13`.
- **Package versions**: Set the root package and docs app package versions to `2026.5.13`.
- **Project rebrand**: Renamed public-facing references from the previous product name to **AG Kit** across package metadata, README files, docs pages, app metadata, `.agent` templates, scripts, workflows, and repository links.
- **Landing page**: Simplified the home page, removed the embedded external wordmark, and switched the hero identity to the new AG Kit logo.
- **Docs content**: Updated documentation titles, examples, installation copy, footer links, and guide metadata to use the AG Kit brand and `ag-kit` package/repository naming.
- **Font loading**: Removed the Google-hosted font import from the app layout and switched the global font tokens to local system font stacks.

### Fixed
- **Docs lint issues**: Escaped JSX apostrophes, fixed inline `// turbo` rendering, and adjusted React Compiler lint violations in theme, mobile menu, and sidebar skeleton components.

### Removed
- **External brand dependency**: Removed old Google-linked product references and the embedded external wordmark from the web app.

## [3.0.0] - 2026-04-01

### Added
- **Coordinator Mode Skill**: Multi-agent orchestration with parallel workers, synthesis protocol, fork semantics, and phase-based workflow (Research -> Synthesis -> Implementation -> Verification).
- **Memory System Skill**: Persistent cross-session memory with `MEMORY.md` index, 4-type taxonomy (`user`, `feedback`, `project`, `reference`), topic files, and auto-recall at session start.
- **Context Compression Skill**: Auto-compress context in long sessions with micro-compact tool output, phase summaries, and session checkpoints.
- **Verify Changes Skill**: Prove code works by running it instead of only inspecting it.
- **Batch Operations Skill**: Multi-file pattern-based modifications with preview-before-execute safety.
- **Simplify Code Skill**: Detect and reduce over-engineered complexity, unnecessary abstractions, dead code, and deep nesting.
- **Skillify Skill**: Auto-create new skills from repetitive multi-step workflows.
- **New Workflow `/coordinate`**: Advanced multi-agent coordination with coordinator protocol.
- **New Workflow `/remember`**: Save information to persistent cross-session memory.
- **New Workflow `/verify`**: Verify code changes through execution.

### Changed
- **Orchestrator Agent**: Major upgrade with coordinator mode patterns, phase-based workflow, worker prompt synthesis guide, fork semantics, concurrency rules, memory integration, and context compression awareness.
- **Parallel Agents Skill**: Enhanced with `when_to_use` frontmatter and concurrency classification.
- **All 44 Skills**: Added `when_to_use` frontmatter field for conditional and intelligent skill loading to reduce token waste.
- **README.md**: Complete rewrite with v2 vs v3 comparison table, pros and cons, migration guide, and attribution.

### Token Impact
- **+1,500 tokens** upfront from memory index and enhanced agents.
- **-3,000 to -15,000 tokens** saved per session through memory, compression, and better prompts.
- **Net: 13-33% more token-efficient** depending on session type.

### Inspired By
- Advanced AI agent source code analysis, including production coordinator, memory, and context management patterns.
- Patterns distilled into original markdown-based templates. No external code copied.

## [2.0.2] - 2026-02-04

### Added
- **New Skill `rust-pro`**: Rust 1.75+ expertise.

### Changed
- **Agent Workflows**: Updated `orchestrate.md` to fix Turkish output.

## [2.0.1] - 2026-01-26

### Added
- **Agent Flow Documentation**: Added comprehensive workflow documentation in `.agent/AGENT_FLOW.md`.
- **Agent Routing Checklist**: Documented mandatory steps before code or design work.
- **Socratic Gate Protocol**: Documented requirement clarification flow.
- **Cross-Skill References**: Added cross-skill reference pattern documentation.
- **New Skill `react-best-practices`**: Consolidated Next.js and React expertise.
- **New Skill `web-design-guidelines`**: Professional web design standards and patterns.

### Changed
- **Skill Consolidation**: Merged `nextjs-best-practices` and `react-patterns` into `react-best-practices`.
- **Architecture Updates**: Enhanced `.agent/ARCHITECTURE.md` with improved flow diagrams.
- **Rules Update**: Updated `.agent/rules/GEMINI.md` with Agent Routing Checklist.
- **Agent Updates**: Updated `frontend-specialist.md` and `qa-automation-engineer.md` with enhanced skill references and testing workflows.
- **Frontend Design Skill**: Enhanced `frontend-design/SKILL.md` with cross-references to `web-design-guidelines`.

### Removed
- Deprecated `nextjs-best-practices` skill after consolidation.
- Deprecated `react-patterns` skill after consolidation.

### Fixed
- **Agent Flow Accuracy**: Corrected misleading terminology in `AGENT_FLOW.md`.
- Changed "Parallel Execution" to "Sequential Multi-Domain Execution".
- Changed "Integration Layer" to "Code Coherence" with a more accurate description.
- Added reality notes about AI sequential processing versus simulated multi-agent behavior.
- Clarified that scripts require user approval and are not auto-executed.

## [2.0.0] - Unreleased

### Initial Release
- Initial release of AG Kit.
- 20 specialized AI agents.
- 37 domain-specific skills.
- 11 workflow slash commands.
- CLI tool for easy installation and updates.
- Comprehensive documentation and architecture guide.

[Unreleased]: https://github.com/vudovn/ag-kit/compare/2026.5.13...HEAD
[2026.5.13]: https://github.com/vudovn/ag-kit/compare/v3.0.0...2026.5.13
[3.0.0]: https://github.com/vudovn/ag-kit/compare/v2.0.2...v3.0.0
[2.0.2]: https://github.com/vudovn/ag-kit/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/vudovn/ag-kit/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/vudovn/ag-kit/releases/tag/v2.0.0
