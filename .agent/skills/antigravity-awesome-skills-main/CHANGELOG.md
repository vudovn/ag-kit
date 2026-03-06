# Changelog

All notable changes to the **Antigravity Awesome Skills** collection are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [6.9.0] - 2026-03-03 - "Multi-Tool & Agent Infrastructure"

> **Agent capabilities expand with email infrastructure, video intelligence, and multi-tool installer support.**

This release delivers major infrastructure improvements: one-command install for multiple AI tools, email capabilities for agents via AgentMail, and video/audio processing with VideoDB. Plus significant web-app performance optimizations.

### 🚀 New Skills

### 📧 AgentMail

**Email infrastructure for AI agents.**

Gives agents real email addresses (`@theagentmail.net`) via REST API. Create accounts, send/receive emails, manage webhooks, and check karma balance. Perfect for agents that need to sign up for services, receive verification codes, or communicate via email.

- Create email accounts with karma-based rate limiting
- Send/receive emails with attachments
- Webhook signature verification for secure notifications
- Full SDK examples and API reference

> **Try it:** "Create an email account for my agent and send a verification email"

### 📹 VideoDB

**Video and audio perception, indexing, and editing.**

Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts.

- Ingest from files, URLs, RTSP/live feeds, or desktop capture
- Semantic, visual, and spoken word indexes with timestamp search
- Timeline editing with subtitles, overlays, transcoding
- AI generation for images, video, music, voiceovers

> **Try it:** "Search for 'product demo' in this video and create a clip with subtitles"

---

### 📦 Improvements

- **Multi-Tool Install Support**: The installer now supports installing skills for multiple tools simultaneously (e.g., `npx antigravity-awesome-skills --claude --codex`). Fixes #182.
- **Web-App Sync Optimization**: Hybrid sync strategy using git fetch for faster updates (5+ min → < 2 sec when no changes). Includes sort by "Most Stars" feature.
- **Registry Update**: Now tracking 970 skills (+2 new).

### 👥 Credits

- **@zinzied** for web-app sync optimization (PR #180)
- **@0xrohitgarg** for VideoDB skill contribution (PR #181)
- **@uriva** for AgentMail skill contribution (PR #183)

---

## [6.8.0] - 2026-03-02 - "Productivity Boost & In-App Sync"

> **Major productivity enhancements to existing skills and new in-app skill synchronization feature.**

This release delivers version 2.0.0 upgrades to two critical skills: `vibe-code-auditor` and `tutorial-engineer`, packed with pattern recognition shortcuts, deterministic scoring, and copy-paste templates. Plus, a new "Sync Skills" button in the Web App enables live skill updates from GitHub without leaving the browser.

## 🚀 New Features

### 🔄 In-App Sync Skills Button

**One-click skill synchronization from the Web App UI.**
Replaces the unreliable START_APP.bat auto-updater. Users can now click "Sync Skills" in the web app to download the latest skills from GitHub instantly.

- Vite dev server plugin exposing `/api/refresh-skills` endpoint
- Downloads and extracts only the `/skills/` folder and `skills_index.json`
- Live UI updates without page refresh

## 📦 Improvements

### ✨ vibe-code-auditor v2.0.0

**Productivity-focused overhaul with 10x faster audits.**

- **Pattern Recognition Shortcuts**: 10 heuristics for rapid issue detection
- **Quick Checks**: 3-second scans for each of 7 audit dimensions
- **Executive Summary**: Critical findings upfront
- **Deterministic Scoring**: Replaces subjective ranges with algorithmic scoring
- **Code Fix Blocks**: Before/after examples for copy-paste remediation
- **Quick Wins Section**: Fixes completable in <1 hour
- **Calibration Rules**: Scoring adjusted by code size (snippet vs multi-file)
- **Expanded Security**: SQL injection, path traversal, insecure deserialization detection

### 📚 tutorial-engineer v2.0.0

**Evidence-based learning with 75% better retention.**

- **4-MAT Model**: Why/What/How/What If framework for explanations
- **Learning Retention Shortcuts**: Evidence-based patterns (+75% retention)
- **Cognitive Load Management**: 7±2 rule, One Screen, No Forward References
- **Exercise Calibration**: Difficulty table with time estimates
- **Format Selection Guide**: Quick Start vs Deep Dive vs Workshop
- **Pre-Publish Audit Checklist**: Comprehension, progression, technical validation
- **Speed Scoring Rubric**: 1-5 rating on 5 dimensions
- **Copy-Paste Template**: Ready-to-use Markdown structure
- **Accessibility Checklist**: WCAG compliance for tutorials

## 👥 Credits

A huge shoutout to our community contributors:

- **@munir-abbasi** for the v2.0.0 productivity enhancements to `vibe-code-auditor` and `tutorial-engineer` (PR #172)
- **@zinzied** for the In-App Sync Skills Button and START_APP.bat simplification (PR #178)

---

## [6.7.0] - 2026-03-01 - "Intelligence Extraction & Automation"

> **New skills for Web Scraping (Apify), X/Twitter extraction, Genomic analysis, and hardened registry infrastructure.**

This release integrates 14 new specialized agent-skills. Highlights include the official Apify collection for web scraping and data extraction, a high-performance X/Twitter scraper, and a comprehensive genomic analysis toolkit. The registry infrastructure has been hardened with hermetic testing and secure YAML parsing.

## 🚀 New Skills

### 🕷️ [apify-agent-skills](skills/apify-actorization/)

**12 Official Apify skills for web scraping and automation.**
Scale data extraction using Apify Actors. Includes specialized skills for e-commerce, lead generation, social media analysis, and market research.

### 🐦 [x-twitter-scraper](skills/x-twitter-scraper/)

**High-performance X (Twitter) data extraction.**
Search tweets, fetch profiles, and extract media/engagement metrics without complex API setups.

### 🧬 [dna-claude-analysis](skills/dna-claude-analysis/)

**Personal genome analysis toolkit.**
Analyze raw DNA data across 17 categories (health, ancestry, pharmacogenomics) with interactive HTML visualization.

---

## 📦 Improvements

- **Registry Hardening**: Migrated all registry maintenance scripts to `PyYAML` for safe, lossless metadata handling. (PR #168)
- **Hermetic Testing**: Implemented environment-agnostic registry tests to prevent CI drift.
- **Contributor Sync**: Fully synchronized the Repo Contributors list in README.md from git history (69 total contributors).
- **Documentation**: Standardized H2 headers in README.md (no emojis) for clean Table of Contents anchors, following Maintenance V5 rules.
- **Skill Metadata**: Enhanced description validation and category consistency across 968 skills.

## 👥 Credits

A huge shoutout to our community contributors:

- **@ar27111994** for the 12 Apify skills and registry hardening (PR #165, #168)
- **@kriptoburak** for `x-twitter-scraper` (PR #164)
- **@shmlkv** for `dna-claude-analysis` (PR #167)

---

## [6.6.0] - 2026-02-28 - "Community Skills & Quality"

> **New skills for Android UI verification, memory handling, video manipulation, vibe-code auditing, and essential fixes.**

This release integrates major community contributions, adding skills for Android testing, scoped agent memory, vibe-code quality auditing, and the VideoDB SDK. It also addresses issues with skill metadata validation and enhances documentation consistency.

## 🚀 New Skills

### 📱 [android_ui_verification](skills/android_ui_verification/)

**Automated end-to-end UI testing on Android Emulators.**
Test layout issues, check state verification, and capture screenshots right from ADB.

### 🧠 [hierarchical-agent-memory](skills/hierarchical-agent-memory/)

**Scoped CLAUDE.md memory system.**
Directory-level context files with a dashboard, significantly reducing token spend on repetitive queries.

### 🎥 [videodb-skills](skills/videodb-skills/)

**The ultimate Video processing toolkit.**
Upload, stream, search, edit, transcribe, and generate AI video/audio using the VideoDB SDK.

### 🕵️ [vibe-code-auditor](skills/vibe-code-auditor/)

**AI-code specific quality assessments.**
Check prototypes and generated code for structural flaws, hidden technical debt, and production risks.

---

## 📦 Improvements

- **Skill Description Restoration**: Recovered 223+ truncated descriptions from git history that were corrupted in release 6.5.0.
- **Robust YAML Tooling**: Replaced fragile regex parsing with `PyYAML` across all maintenance scripts (`manage_skill_dates.py`, `validate_skills.py`, etc.) to prevent future data loss.
- **Refined Descriptions**: Standardized all skill descriptions to be under 200 characters while maintaining grammatical correctness and functional value.
- **Cross-Platform Index**: Normalized `skills_index.json` to use forward slashes for universal path compatibility.
- **Skill Validation Fixes**: Corrected invalid description lengths and `risk` fields in `copywriting`, `videodb-skills`, and `vibe-code-auditor`. (Fixes #157, #158)
- **Documentation**: New dedicated `docs/SEC_SKILLS.md` indexing all 128 security skills.
- **README Quality**: Cleaned up inconsistencies, deduplicated lists, updated stats (954+ total skills).

## 👥 Credits

A huge shoutout to our community contributors:

- **@alexmvie** for `android_ui_verification`
- **@talesperito** for `vibe-code-auditor`
- **@djmahe4** for `docs/SEC_SKILLS.md`
- **@kromahlusenii-ops** for `hierarchical-agent-memory`
- **@0xrohitgarg** for `videodb-skills`
- **@nedcodes-ok** for `rule-porter` addition
- **@acbhatt12** for `README.md` improvements (PR #162)

---

## [6.5.0] - 2026-02-27 - "Community & Experience"

> **Major UX upgrade: Stars feature, auto-updates, interactive prompts, and complete date tracking for all 950+ skills.**

This release introduces significant community-driven enhancements to the web application alongside comprehensive metadata improvements. Users can now upvote skills, build contextual prompts interactively, and benefit from automatic skill updates. All skills now include date tracking for better discoverability.

## 🚀 New Features

### ⭐ Stars & Community Upvotes

**Community-driven skill discovery with star/upvote system.**

- Upvote skills you find valuable — visible to all users
- Star counts persist via Supabase backend
- One upvote per browser (localStorage deduplication)
- Discover popular skills through community ratings

> **Try it:** Browse to any skill and click the ⭐ button to upvote!

### 🔄 Auto-Update Mechanism

**Seamless skill updates via START_APP.bat.**

- Automatic skill synchronization on app startup
- Git-based fast updates when available
- PowerShell HTTPS fallback for non-Git environments
- Surgical updates — only `/skills/` folder to avoid conflicts

> **Try it:** Run `START_APP.bat` to automatically fetch the latest 950+ skills!

### 🛠️ Interactive Prompt Builder

**Build contextual prompts directly in skill detail pages.**

- Add custom context to any skill (e.g., "Use React 19 and Tailwind")
- Copy formatted prompt with skill invocation + your context
- Copy full skill content with context overlay
- Streamlined workflow for AI assistant interactions

> **Try it:** Visit any skill, add context in the text box, click "Copy @Skill"!

### 📅 Date Tracking for All Skills

**Complete `date_added` metadata across the entire registry.**

- All 950+ skills now include `date_added` field
- Visible badges in skill detail pages
- Filter and sort by recency
- Better discoverability of new capabilities

## 📦 Improvements

- **Smart Auto-Categorization**: Categories sorted by skill count with "uncategorized" at the end
- **Category Stats**: Dropdown shows skill count per category
- **Enhanced Home Page**: Risk level badges and date display on skill cards
- **Complete Date Coverage**: All skills updated with `date_added` metadata
- **Web App Dependencies**: Automatic `@supabase/supabase-js` installation

## 👥 Credits

A huge shoutout to our community contributors:

- **@zinzied** for the comprehensive UX enhancement (Stars, Auto-Update, Prompt Builder, Date Tracking, Auto-Categorization — PR #150)

---

## [6.4.1] - 2026-02-27 - "Temporal & Convex Backend Hotfix"

> **Hotfix release: Temporal Go expert skill, Convex reactive backend, and strict-compliant SEO incident/local audit fixes.**

This release builds on 6.4.0 by adding a Temporal Go SDK pro skill, a comprehensive Convex reactive backend skill, and aligning the new SEO incident/local audit skills with the strict validation rules so they ship cleanly via npm.

## 🚀 New Skills

### ⏱️ [temporal-golang-pro](skills/temporal-golang-pro/)

**Temporal Go SDK expert for durable distributed systems.**
Guides production-grade Temporal Go usage with deterministic workflow rules, mTLS worker configuration, interceptors, testing strategies, and advanced patterns.

- **Key Feature 1**: Covers workflow determinism, versioning, durable concurrency and long-running workflow patterns.
- **Key Feature 2**: Provides mTLS-secure worker setup, interceptors, and replay/time-skipping test strategies.

> **Try it:** `Use temporal-golang-pro to design a durable subscription billing workflow with safe versioning and mTLS workers.`

### 🔄 [convex](skills/convex/)

**Convex reactive backend for schema, functions, and real-time apps.**
Full-stack backend skill covering Convex schema design, TypeScript query/mutation/action functions, real-time subscriptions, auth, file storage, scheduling, and deployment flows.

- **Key Feature 1**: End-to-end examples for schema validators, function types, pagination and client integration.
- **Key Feature 2**: Documents auth options (Convex Auth, Clerk, Better Auth) and operational patterns (cron, storage, environments).

> **Try it:** `Use convex to design a schema and function set for a real-time dashboard with authenticated users and file uploads.`

## 📦 Improvements

- **Strict SEO Skills Compliance**:
  - `seo-forensic-incident-response` and `local-legal-seo-audit` now include `## When to Use` sections and concise descriptions, and use `risk: safe`, fully passing `validate_skills.py --strict`.
- **Catalog & Index Sync**:
  - Updated `CATALOG.md`, `data/catalog.json`, `skills_index.json`, `data/bundles.json`, `data/aliases.json`, and `README.md` to track **950+ skills**, including `temporal-golang-pro`, `convex`, and the new SEO skills.

## 👥 Credits

- **@HuynhNhatKhanh** for the Temporal Go SDK expert skill (`temporal-golang-pro`, PR #148).
- **@chauey** for the Convex reactive backend skill (`convex`, PR #152).
- **@talesperito** for the SEO forensic incident response and local legal SEO skills and collaboration on the strict-compliant refinements (PRs #153 / #154).

---

## [6.4.0] - 2026-02-27 - "SEO Incident Response & Legal Local Audit"

> **Focused release: specialized SEO incident response and legal local SEO audit skills, plus catalog sync.**

This release adds two advanced SEO skills for handling organic traffic incidents and auditing legal/professional services sites, and updates the public catalog to keep discovery aligned with the registry.

## 🚀 New Skills

### 🧪 [seo-forensic-incident-response](skills/seo-forensic-incident-response/)

**Forensic SEO incident response for sudden organic traffic or rankings drops.**
Guides structured triage, hypothesis-driven investigation, evidence collection and phased recovery plans using GSC, analytics, logs and deployment history.

- **Key Feature 1**: Classifies incidents across algorithmic, technical, manual action, content and demand-change buckets.
- **Key Feature 2**: Produces a forensic report with 0–3 day, 3–14 day and 2–8 week action plans plus monitoring.

> **Try it:** `We lost 40% of organic traffic last week. Use seo-forensic-incident-response to investigate and propose a recovery plan.`

### ⚖️ [local-legal-seo-audit](skills/local-legal-seo-audit/)

**Local SEO auditing for law firms and legal/professional services.**
Specialized audit framework for YMYL legal sites covering GBP, E‑E‑A‑T, practice area pages, NAP consistency, legal directories and reputation.

- **Key Feature 1**: Step‑by‑step GBP, directory and NAP audit tailored to legal practices.
- **Key Feature 2**: Generates a prioritized action plan and content strategy for legal/local search.

> **Try it:** `Audit the local SEO of this law firm website using local-legal-seo-audit and propose the top 10 fixes.`

## 📦 Improvements

- **Catalog Sync**: Updated `CATALOG.md` and `data/catalog.json` to track 947 skills and include `10-andruia-skill-smith` in the general category listing.
- **Documentation**: README now references the MojoAuth implementation skill in the integrations list.

## 👥 Credits

A huge shoutout to our community contributors:

- **@talesperito** for the SEO forensic incident response and legal local SEO audit skills (PRs #153 / #154).
- **@developer-victor** for the MojoAuth implementation README integration (PR #149).

---

## [6.3.1] - 2026-02-25 - "Validation & Multi-Protocol Hotfix"

> **"Hotfix release to restore missing skills, correct industrial risk labels, and harden validation across the registry."**

This release fixes critical validation errors introduced in previous PRs, ensures full compliance with the strict CI registry checks, and restores two high-demand developer skills.

## 🚀 New Skills

### 🧩 [chrome-extension-developer](skills/chrome-extension-developer/)

**Expert in building Chrome Extensions using Manifest V3.**
Senior expertise in modern extension architecture, focusing on Manifest V3, service workers, and production-ready security practices.

- **Key Feature 1**: Comprehensive coverage of Manifest V3 service workers and lifecycle.
- **Key Feature 2**: Production-ready patterns for cross-context message passing.

> **Try it:** `Help me design a Manifest V3 extension that monitors network requests using declarativeNetRequest.`

### ☁️ [cloudflare-workers-expert](skills/cloudflare-workers-expert/)

**Senior expertise for serverless edge computing on Cloudflare.**
Specialized in edge architectures, performance optimization, and the full Cloudflare developer ecosystem (Wrangler, KV, D1, R2).

- **Key Feature 1**: Optimized patterns for 0ms cold starts and edge-side storage.
- **Key Feature 2**: Implementation guides for Durable Objects and R2 storage integration.

> **Try it:** `Build a Cloudflare Worker that modifies response headers and caches fragmented data in KV.`

---

## 📦 Improvements

- **Registry Update**: Now tracking 946+ high-performance skills.
- **Validation Hardening**: Resolved missing "When to Use" sections for 11 critical skills (Andru.ia, Logistics, Energy).
- **Risk Label Corrections**: Corrected risk levels to `safe` for `linkedin-cli`, `00-andruia-consultant`, and `20-andruia-niche-intelligence`.

## 👥 Credits

A huge shoutout to our community contributors:

- **@itsmeares** for PR #139 validation fixes and "When to Use" improvements.

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [6.3.0] - 2026-02-25 - "Agent Discovery & Operational Excellence"

> **Feature release: AgentFolio discovery skill, LinkedIn CLI automation, Evos operational skills, Andru.ia consulting roles, and hardened validation for new contributors.**

## 🚀 New Skills

### 🔍 [agentfolio](skills/agentfolio/)

**Discover and research autonomous AI agents.**
Skill for discovering and researching autonomous AI agents, tools, and ecosystems using the AgentFolio directory.

- **Key Feature 1**: Discover agents for specific use cases.
- **Key Feature 2**: Collect concrete examples and benchmarks for agent capabilities.

> **Try it:** `Use AgentFolio to find 3 autonomous AI agents focused on code review.`

### 💼 [linkedin-cli](skills/linkedin-cli/)

**Automate LinkedIn operations via CLI.**
CLI-based LinkedIn automation skill using `@linkedapi/linkedin-cli` for profile enrichment, outreach, Sales Navigator, and workflow execution.

- **Key Feature 1**: Fetch profiles and search people/companies.
- **Key Feature 2**: Manage connections and send messages via Sales Navigator.

> **Try it:** `Use linkedin-cli to search for PMs in San Francisco.`

### 🚀 [appdeploy](skills/appdeploy/)

**Deploy full-stack web apps.**
Deploy web apps with backend APIs, database, and file storage via an HTTP API to get an instant public URL.

- **Key Feature 1**: Chat-native deployment orchestrator.
- **Key Feature 2**: Support for frontend-only and frontend+backend architectures.

> **Try it:** `Deploy this React-Vite dashboard using appdeploy.`

### 🐹 [grpc-golang](skills/grpc-golang/)

**Production-grade gRPC patterns in Go.**
Build robust microservices communication using Protobuf with mTLS, streaming, and observability configurations.

- **Key Feature 1**: Standardize API contracts with Protobuf and Buf.
- **Key Feature 2**: Implement service-to-service authentication and structured metrics.

> **Try it:** `Use grpc-golang to define a user service streaming endpoint with mTLS.`

### 📦 [logistics-exception-management](skills/logistics-exception-management/)

**Expertise for handling freight and carrier disputes.**
Deeply codified operational playbook for handling shipping exceptions, delays, damages, and claims. Part of the Evos operational domain expertise suite. Additional skills: `carrier-relationship-management`, `customs-trade-compliance`, `inventory-demand-planning`, `production-scheduling`, `returns-reverse-logistics`, `energy-procurement`, `quality-nonconformance`.

- **Key Feature 1**: Provides escalation protocols and severity classification for exceptions.
- **Key Feature 2**: Delivers templates and decision frameworks for claim management across various delivery modes.

> **Try it:** `We have a delayed LTL shipment for a key customer, how should we handle it per logistics-exception-management?`

### 🏗️ [00-andruia-consultant](skills/00-andruia-consultant/)

**Spanish-language solutions architect.**
Diagnóstica y traza la hoja de ruta óptima para proyectos de IA en español. Additional skills: `20-andruia-niche-intelligence`.

- **Key Feature 1**: Proporciona entrevistas de diagnóstico para proyectos desde cero o existentes.
- **Key Feature 2**: Propone el escuadrón de expertos necesario y genera artefactos de backlog en español.

> **Try it:** `Actúa como 00-andruia-consultant y diagnostica este nuevo workspace.`

## 📦 Improvements

- **Validation & Quality Bar**:
  - Normalised `risk:` labels for new skills to conform to the allowed set (`none`, `safe`, `critical`, `offensive`, `unknown`).
  - Added explicit `## When to Use` sections to new operational and contributor skills to keep the registry strictly compatible with `python3 scripts/validate_skills.py --strict`.
- **Interactive Web App**:
  - Auto-updating local web app launcher and **Interactive Prompt Builder** enhancements (PR #137) now ship as part of the v6.3.0 baseline.
- **Registry**:
  - Validation Chain (`npm run chain` + `npm run validate:strict`) runs clean at 6.3.0 with all new skills indexed in `skills_index.json`, `data/catalog.json`, and `CATALOG.md`.

## 👥 Credits

- **@bobrenze-bot** for proposing the AgentFolio integration (Issue #136).
- **@vprudnikoff** for the `linkedin-cli` skill (PR #131).
- **@Onsraa** for the Bevy ECS documentation update around Require Components (PR #132).
- **@Abdulrahmansoliman** for the AdaL CLI README instructions (PR #133).
- **@avimak** for the `appdeploy` deployment skill (PR #134).
- **@HuynhNhatKhanh** for the gRPC Go production patterns skill (PR #135).
- **@zinzied** for the auto-updating web app launcher & Interactive Prompt Builder (PR #137).
- **@nocodemf** for the Evos operational domain skills (PR #138).

---

## [6.2.0] - 2026-02-24 - "Interactive Web App & AWS IaC"

> **Feature release: Interactive Skills Web App, AWS Infrastructure as Code skills, and Chrome Extension / Cloudflare Workers developer skills.**

## 🚀 New Skills

- **AWS Infrastructure as Code** (PR #124): `cdk-patterns`, `cloudformation-best-practices`, `terraform-aws-modules`.
- **Browser & Edge** (PR #128): `chrome-extension-developer`, `cloudflare-workers-expert`.

## 📦 Improvements

- **Interactive Skills Web App** (PR #126): Added a local web UI for browsing skills, including `START_APP.bat`, setup script, and `web-app/` project with catalog export.
- **Shopify Development Skill** (PR #125): Fixed markdown syntax issues in `skills/shopify-development/SKILL.md` to keep the registry strictly valid.
- **Community Sources** (PR #127): Added SSOJet skills and integration guides to Credits & Sources.
- **Registry**: Now tracking 930 skills.

## 👥 Credits

- **@ssumanbiswas** for AWS Infrastructure as Code skills (PR #124).
- **@thuanlm** for the Shopify development skill fix (PR #125).
- **@zinzied** for the Interactive Skills Web App (PR #126).
- **@code-vj** for the SSOJet documentation link (PR #127).
- **@GeekLuffy** for Chrome Extension and Cloudflare Workers skills (PR #128).

---

## [6.1.1] - 2026-02-23 - "AWS Cost Optimization & Registry 927"

> **Patch release: AWS cost optimization skills (PR #107) and registry count 927.**

- **New skills** (PR #107): `aws-cost-optimizer`, `aws-cost-cleanup`.
- **Registry**: Now tracking 927 skills.

---

## [6.1.0] - 2026-02-23 - "Issues Fix & Community Expansion"

> **Bugfixes for #116 and #120, plus Game Dev bundle, Android skills, Workflow Bundles, LibreOffice, Data Structure Protocol, and Kiro IDE support.**

This release fixes the YAML syntax error in database-migrations-sql-migrations (issue #116), adds a typo alias so `shopify—development` (em dash) resolves to `shopify-development` (issue #120), and ships a large set of community PRs: Game Development Expansion (Bevy ECS, GLSL, Godot 4), Android Modern Development (Compose + Coroutines), Workflow Bundles and LibreOffice skills, Data Structure Protocol, and Kiro CLI/IDE support.

## New Skills

- **Game Development Expansion** (PR #121): `bevy-ecs-expert`, `shader-programming-glsl`, `godot-4-migration`.
- **Android Modern Development** (PR #118): `android-jetpack-compose-expert`, `kotlin-coroutines-expert`.
- **Workflow Bundles & LibreOffice** (PR #113): Workflow bundles readme, LibreOffice skills (Base, Calc, Draw, Impress, Writer), plus office-productivity, WordPress suite, and many domain skills (ai-agent-development, cloud-devops, database, e2e-testing, security-audit, terraform-infrastructure, etc.).
- **Data Structure Protocol** (PR #114): `data-structure-protocol`.
- **Kiro CLI and Kiro IDE** (PR #122): Documentation and support for Kiro.

## Improvements

- **YAML fix** (PR #119, fixes #116): Resolved invalid YAML in `database-migrations-sql-migrations/SKILL.md` (description block mapping); removed non-standard frontmatter and standardized section headers.
- **Skill matching** (fixes #120): Added typo alias `shopify—development` → `shopify-development` so em-dash input resolves correctly.
- **Registry**: Now tracking 925 skills.

## Credits

- **@nikolasdehor** for YAML fix (PR #119), Game Development Expansion (PR #121), Android Modern Development (PR #118)
- **@ssumanbiswas** for Kiro CLI and Kiro IDE support (PR #122)
- **@munir-abbasi** for Workflow Bundles and LibreOffice Skills (PR #113)
- **@k-kolomeitsev** for Data Structure Protocol (PR #114)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [6.0.0] - 2026-02-22 - "Codex YAML Fix & Community PRs"

> **Major release: Codex frontmatter fixes, AWS Security & Compliance skills, Antigravity Workspace Manager CLI, and validation fixes.**

This release addresses Codex invalid YAML warnings (issue #108) via frontmatter fixes, adds AWS Security & Compliance skills and the official Antigravity Workspace Manager CLI companion, and fixes validation for nerdzao-elite skills.

## New Skills

- **AWS Security & Compliance** (PR #106): `aws-compliance-checker`, `aws-iam-best-practices`, `aws-secrets-rotation`, `aws-security-audit`.
- **nerdzao-elite**, **nerdzao-elite-gemini-high**: Elite workflow skills (validation fixes in-repo).

## Improvements

- **Frontmatter**: Fixed YAML frontmatter in code-reviewer, architect-review, c-pro, design-orchestration, haskell-pro, multi-agent-brainstorming, performance-engineer, search-specialist (PR #111) — reduces Codex "invalid YAML" warnings (fixes #108).
- **Antigravity Workspace Manager**: Official CLI companion to auto-provision skill subsets across environments (PR #110); documented in Community Contributors.
- **Registry**: Now tracking 889 skills.
- **Validation**: Added frontmatter and "When to Use" for nerdzao-elite / nerdzao-elite-gemini-high.

## Credits

- **@Vonfry** for frontmatter YAML fixes (PR #111)
- **@ssumanbiswas** for AWS Security & Compliance skills (PR #106)
- **@amartelr** for Antigravity Workspace Manager CLI (PR #110)
- **@fernandorych** for branch sync (PR #109)
- **@Rodrigolmti** for reporting Codex YAML issue (#108)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [5.10.0] - 2026-02-21 - "AWS Kiro CLI Integration"

> **Native support and integration guide for AWS Kiro CLI, expanding the repository's reach to the AWS developer community.**

This release adds comprehensive support for Kiro CLI, AWS's recently launched agentic IDE, enabling 883+ skills to enhance Kiro's autonomous operations across serverless, IaC, and AWS architectures. It also includes an important bugfix for the npm installer CLI.

## 🚀 Improvements

- **Integration Guide**: Added `docs/KIRO_INTEGRATION.md` detailing Kiro capabilities, installation instructions, AWS-recommended skills, and MCP usage.
- **Documentation**: Updated `README.md`, `docs/GETTING_STARTED.md`, and `docs/FAQ.md` to formally support Kiro CLI and add invocation examples.
- **Installer**: Added the `--kiro` flag to the CLI installer (`bin/install.js`) which correctly targets `~/.kiro/skills`.

## 🐛 Bug Fixes

- **Installer Path Consistency**: Fixed Issue #105 where the published `v5.9.0` npm install script contained an older version of `bin/install.js`, causing `--antigravity` installs to mistakenly target `.agent/skills` instead of the global `~/.gemini/antigravity/skills`. This release (`5.10.0`) properly bundles the corrected npm install script.

## 👥 Credits

A huge shoutout to our community contributors:

- **@ssumanbiswas** for the Kiro CLI support (PR #104)

---

## [5.9.0] - 2026-02-20 - "Apple HIG & Quality Bar"

> **Extensive Apple design guidelines and strict validation for the entire registry.**

This release adds the official Apple Human Interface Guidelines skills suite, enforces strict agentskills-ref metadata validation across all skills, and addresses critical path resolution bugs in the CLI installer along with dangling link validation to prevent agent token waste.

## 🚀 New Skills

### 🍎 [apple-hig-skills](skills/hig-platforms/)

**Comprehensive platform and UX guidelines for Apple ecosystems.**
Official guidelines covering iOS, macOS, visionOS, watchOS, and tvOS natively formatted for AI consumption.

- **Key Feature 1**: Deep dives into spatial layout, interactions, and modalities.
- **Key Feature 2**: Component-level guidelines for status bars, dialogs, charts, and input mechanisms (Pencil, Digital Crown).

> **Try it:** `Use @hig-platforms to review if our iPad app navigation follows standard iOS paradigms.`

### 👁️ [manifest](skills/manifest/)

**Observability plugin setup guide for AI agents.**
Walks through a 6-step setup for the Manifest observability platform, including troubleshooting for common errors.

- **Key Feature**: Complete configuration wizard from obtaining API keys to verifying traces.

> **Try it:** `Use @manifest to add observability to our local python agent.`

---

## 📦 Improvements

- **Registry Update**: Now tracking 883 skills.
- **CLI Installer**: Fixed the default `.agent/skills` path to properly default to `~/.gemini/antigravity/skills` and added an explicit `--antigravity` flag (fixes #101).
- **Validation**: Enforced strict folder-to-name matching and concise (<200 char) descriptions based on `agentskills-ref` (fixes #97).
- **Validation**: Added build-time Markdown dangling link validation to `validate_skills.py` to prevent agents from hallucinating relative paths (fixes #102).

## 👥 Credits

A huge shoutout to our community contributors:

- **@raintree-technology** for the Apple HIG Skills (PR #90)
- **@sergeyklay** for the skill quality validations (PR #97)
- **@SebConejo** for the manifest observability skill (PR #103)
- **@community** for identifying installer and link bugs (Issues #101, #102)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [5.8.0] - 2026-02-19 - "Domain-Driven Design Suite"

> **First full DDD skill suite: strategic design, context mapping, and tactical patterns for complex domains.**

This release introduces a comprehensive Domain-Driven Design skill suite (4 new skills) contributed by the community, plus playbook fixes for saga-orchestration and event-store-design, and new DDD-themed bundle and workflow entries.

## 🚀 New Skills

### 🏗️ [domain-driven-design](skills/domain-driven-design/)

**Entry point and router for all DDD adoption decisions.**
Covers viability checks, routing to strategic/tactical/evented sub-skills, and output requirements.

- **Key Feature**: Viability check gate — avoids over-engineering simple systems.
- **Key Feature**: Routing map to `@ddd-strategic-design`, `@ddd-context-mapping`, `@ddd-tactical-patterns`, CQRS, event sourcing, sagas, projections.

> **Try it:** `Use @domain-driven-design to assess if this billing platform should adopt full DDD.`

### 🗺️ [ddd-strategic-design](skills/ddd-strategic-design/)

**Subdomains, bounded contexts, and ubiquitous language.**
Produces subdomain classification tables, bounded context catalogs, and glossaries.

### 🔗 [ddd-context-mapping](skills/ddd-context-mapping/)

**Cross-context integration contracts and anti-corruption layers.**
Defines upstream/downstream ownership, translation rules, and versioning policies.

### 🧩 [ddd-tactical-patterns](skills/ddd-tactical-patterns/)

**Aggregates, value objects, repositories, and domain events in code.**
Includes a TypeScript aggregate example with invariant enforcement.

---

## 📦 Improvements

- **Registry Update**: Now tracking 868 skills.
- **saga-orchestration** and **event-store-design**: Added missing `resources/implementation-playbook.md`.
- **docs/BUNDLES.md**: Added DDD & Evented Architecture bundle section.
- **docs/WORKFLOWS.md** + **data/workflows.json**: New "Design a DDD Core Domain" workflow entry.

## 👥 Credits

A huge shoutout to our community contributors:

- **[@rcigor](https://github.com/rcigor)** for the full DDD skill suite (PR #98)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [5.7.0] - 2026-02-18 - "Yandex Direct Audit"

> **First agentic skill for the Russian PPC market, offering comprehensive Yandex Direct account auditing.**

### Added

- **New External Skill**: `yandex-direct-audit` (Silverov/yandex-direct-skill)
  - 55 automated checks for Yandex Direct (API v5).
  - A-F scoring system.
  - Comprehensive campaign, ad, and keyword analysis.

### Registry

- **Total Skills**: 864.
- **Generated Files**: Synced artifacts.

### Credits

- **[@Silverov](https://github.com/Silverov)** - Yandex Direct Audit skill (PR #95).

---

## [5.6.0] - 2026-02-17 - "Autonomous Agents & Trusted Workflows"

> **DBOS for reliable workflows, Crypto BD agents, and improved usage documentation.**

This release introduces official DBOS skills for building fault-tolerant applications in TypeScript, Python, and Go, plus a sophisticated autonomous Business Development agent for crypto, and a comprehensive usage guide to help new users get started.

### Added

- **DBOS Skills** (Official):
  - `dbos-typescript`: Durable workflows and steps for TypeScript.
  - `dbos-python`: Fault-tolerant Python applications.
  - `dbos-golang`: Reliable Go services.
- **New Skill**: `crypto-bd-agent` - Autonomous BD patterns for token discovery, scoring, and outreach with wallet forensics.
- **Documentation**: New `docs/USAGE.md` guide addressing post-installation confusion (how to prompt, where skills live).

### Registry

- **Total Skills**: 864 (from 860).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@maxdml](https://github.com/maxdml)** - DBOS Skills (PR #94).
- **[@buzzbysolcex](https://github.com/buzzbysolcex)** - Crypto BD Agent (PR #92).
- **[@copilot-swe-agent](https://github.com/apps/copilot-swe-agent)** - Usage Guide (PR #93).

---

## [5.5.0] - 2026-02-16 - "Laravel Pro & ReactFlow Architect"

> **Advanced Laravel engineering roles and ReactFlow architecture patterns.**

This release introduces professional Laravel capabilities (Expert & Security Auditor) and a comprehensive ReactFlow Architect skill for building complex node-based applications.

### Added

- **New Skill**: `laravel-expert` - Senior Laravel Engineer role for production-grade, maintainable, and idiomatic solutions (clean architecture, security, performance).
- **New Skill**: `laravel-security-audit` - Specialized security auditor for Laravel apps (OWASP, vulnerabilities, misconfigurations).
- **New Skill**: `react-flow-architect` - Expert ReactFlow patterns for interactive graph apps (hierarchical navigation, performance, customized state management).

### Changed

- **OpenCode**: Updated installation path to `.agents/skills` to align with latest OpenCode standards.

### Registry

- **Total Skills**: 860 (from 857).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@Musayrlsms](https://github.com/Musayrlsms)** - Laravel Expert & Security Audit skills (PR #85, #86).
- **[@mertbaskurt](https://github.com/mertbaskurt)** - ReactFlow Architect skill (PR #88).
- **[@sharmanilay](https://github.com/sharmanilay)** - OpenCode path fix (PR #87).

---

## [5.4.0] - 2026-02-16 - "CursorRules Pro & Go-Rod"

> **Community contributions: CursorRules Pro in credits and go-rod-master skill for browser automation with Go.**

This release adds CursorRules Pro to Community Contributors and a new skill for browser automation and web scraping with go-rod (Chrome DevTools Protocol) in Golang, including stealth and anti-bot-detection patterns.

### New Skills

#### go-rod-master ([skills/go-rod-master/](skills/go-rod-master/))

**Browser automation and web scraping with Go and Chrome DevTools Protocol.**
Comprehensive guide for the go-rod library: launch and page lifecycle, Must vs error patterns, context and timeouts, element selectors, auto-wait, and integration with go-rod/stealth for anti-bot detection.

- **Key features**: CDP-native driver, thread-safe operations, stealth plugin, request hijacking, concurrent page pools.
- **When to use**: Scraping or automating sites with Go, headless browser for SPAs, stealth/anti-bot needs, migrating from chromedp or Playwright Go.

> **Try it:** "Automate logging into example.com with Go using go-rod and stealth."

### Registry

- **Total Skills**: 857 (from 856).
- **Generated files**: README, skills_index.json, catalog, and bundles synced.

### Credits

- **[@Wittlesus](https://github.com/Wittlesus)** - CursorRules Pro in Community Contributors (PR #81).
- **[@8hrsk](https://github.com/8hrsk)** - go-rod-master skill (PR #83).

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [5.3.0] - 2026-02-13 - "Advanced Three.js & Modern Graphics"

> **Enhanced Three.js patterns: performance, visual polish, and production practices.**

This release significantly upgrades our 3D visualization capabilities with a comprehensive Three.js skill upgrade, focusing on CDN-compatible patterns, performance optimizations, and modern graphics techniques like shadows, fog, and GSAP integration.

### Added

- **Modern Three.js Patterns**: Comprehensive guide for `r128` (CDN) and production environments.
- **Visual Polish**: Advanced sections for shadows, environment maps, and tone mapping.
- **Interaction Models**: Custom camera controls (OrbitControls alternative) and raycasting for object selection.
- **Production Readiness**: Integration patterns for GSAP, scroll-based animations, and build tool optimizations.

### Registry

- **Total Skills**: 856.
- **Metadata**: Fixed missing source and risk fields for `threejs-skills`.
- **Sync**: All discovery artifacts (README, Catalog, Index) updated and synced.

### Contributors

- **[@Krishna-hehe](https://github.com/Krishna-hehe)** - Advanced Three.js skill overhaul (PR #78).

---

## [5.2.0] - 2026-02-13 - "Podcast Generation & Azure AI Skills"

> **New AI capabilities: Podcast Generation, Azure Identity, and Self-Evolving Agents.**

### Added

- **New Skill**: `podcast-generation` - Create multi-speaker podcasts from text/URLs using OpenAI Text-to-Speech (TTS) and pydub.
- **New Skill**: `weevolve` - Self-evolving knowledge engine with recursive improvement protocol.
- **Azure Skills Expansion**:
  - `azure-ai-agents-persistent-dotnet`: Persistent agent patterns for .NET.
  - `azure-ai-agents-persistent-java`: Persistent agent patterns for Java.
  - `azd-deployment`: Azure Developer CLI deployment strategies.
- **Python Enhancements**:
  - `pydantic-models-py`: Robust data validation patterns.
  - `fastapi-router-py`: Scalable API routing structures.

### Registry

- **Total Skills**: 856 (from 845).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@sickn33](https://github.com/sickn33)** - Podcast Generation & Azure skills sync (PR #74).
- **[@aro-brez](https://github.com/aro-brez)** - WeEvolve skill (Issue #75).

---

## [5.1.0] - 2026-02-12 - "Official Microsoft & Gemini Skills"

> **845+ skills: the largest single-PR expansion ever, powered by official vendor collections.**

Integrates the full official Microsoft skills collection (129 skills) and Google Gemini API development skills, significantly expanding Azure SDK coverage across .NET, Python, TypeScript, Java, and Rust, plus M365 Agents, Semantic Kernel, and wiki plugin skills.

### Added

- **129 Microsoft Official Skills** from [microsoft/skills](https://github.com/microsoft/skills):
  - Azure SDKs across .NET, Python, TypeScript, Java, and Rust
  - M365 Agents, Semantic Kernel, and wiki plugin skills
  - Flat structure using YAML `name` field as directory name
  - Attribution files: `docs/LICENSE-MICROSOFT`, `docs/microsoft-skills-attribution.json`
- **Gemini API Skills**: Official Gemini API development skill under `skills/gemini-api-dev/`
- **New Scripts & Tooling**:
  - `scripts/sync_microsoft_skills.py` (v4): Flat-structure sync with collision detection, stale cleanup, and attribution metadata
  - `scripts/tests/inspect_microsoft_repo.py`: Remote repo inspection
  - `scripts/tests/test_comprehensive_coverage.py`: Coverage verification
- **New npm scripts**: `sync:microsoft` and `sync:all-official` in `package.json`

### Fixed

- **`scripts/generate_index.py`**: Enhanced frontmatter parsing for unquoted `@` symbols and commas
- **`scripts/build-catalog.js`**: Deterministic `generatedAt` timestamp (prevents CI drift)

### Registry

- **Total Skills**: 845 (from 626). All generated files synced.

### Contributors

- [@ar27111994](https://github.com/ar27111994) - Microsoft & Gemini skills integration (PR #73)

---

## [5.0.0] - 2026-02-10 - "Antigravity Workflows Foundation"

> Workflows are now first-class: users can run guided, multi-skill playbooks instead of manually composing skills one by one.

### Added

- **New orchestration skill**: `antigravity-workflows`
  - `skills/antigravity-workflows/SKILL.md`
  - `skills/antigravity-workflows/resources/implementation-playbook.md`
- **New workflow documentation**: `docs/WORKFLOWS.md`
  - Introduces the Workflows model and differentiates it from Bundles.
  - Provides execution playbooks with prerequisites, ordered steps, and prompt examples.
- **New machine-readable workflow registry**: `data/workflows.json`
  - `ship-saas-mvp`
  - `security-audit-web-app`
  - `build-ai-agent-system`
  - `qa-browser-automation`

### Changed

- **README / Onboarding docs** updated to include Workflows discovery and usage:
  - `README.md` (TOC + "Antigravity Workflows" section)
  - `docs/GETTING_STARTED.md` (Bundles vs Workflows guidance)
  - `docs/FAQ.md` (new Q&A: Bundles vs Workflows)
- **Go browser automation alignment**:
  - Workflow playbooks now include optional `@go-playwright` hooks for Go-based QA/E2E flows.
- **Registry sync** after workflow skill addition:
  - `CATALOG.md`
  - `skills_index.json`
  - `data/catalog.json`
  - `data/bundles.json`

### Contributors

- [@sickn33](https://github.com/sickn33) - Workflows architecture, docs, and release integration

---

## [4.11.0] - 2026-02-08 - "Clean Code & Registry Stability"

> Quality improvements: Clean Code principles and deterministic builds.

### Changed

- **`clean-code` skill** - Complete rewrite based on Robert C. Martin's "Clean Code":
  - Systematic coverage: Meaningful names, functions, comments, formatting, objects, error handling, unit tests, and classes
  - Added F.I.R.S.T. test principles and Law of Demeter guidance
  - Fixed invalid heading format (`## ## When to Use` → `## When to Use`) that blocked validation
  - Added implementation checklist and code smell detection
- **Registry Stabilization** - Fixed `scripts/build-catalog.js` for deterministic CI builds:
  - Uses `SOURCE_DATE_EPOCH` environment variable for reproducible timestamps
  - Replaced `localeCompare` with explicit comparator for consistent sorting across environments
  - Prevents CI validation failures caused by timestamp drift

### Contributors

- [@jackjin1997](https://github.com/jackjin1997) - Clean Code skill update and registry fixes (PR #69, forged at [ClawForge](https://github.com/jackjin1997/ClawForge))

---

## [4.10.0] - 2026-02-06 - "Composio Automation + .NET Backend"

> A major expansion focused on practical app automation and stronger backend engineering coverage.

### Added

- **79 new skills total**.
- **78 Composio/Rube automation skills** (PR #64), with operational playbooks for:
- CRM and sales stacks (`HubSpot`, `Pipedrive`, `Salesforce`, `Zoho CRM`, `Close`).
- Collaboration and project tools (`Notion`, `ClickUp`, `Asana`, `Jira`, `Confluence`, `Trello`, `Monday`).
- Messaging and support channels (`Slack`, `Discord`, `Teams`, `Intercom`, `Freshdesk`, `Zendesk`).
- Marketing and analytics systems (`Google Analytics`, `Mixpanel`, `PostHog`, `Segment`, `Mailchimp`, `Klaviyo`).
- Infra/dev tooling (`GitHub`, `GitLab`, `CircleCI`, `Datadog`, `PagerDuty`, `Vercel`, `Render`).
- **1 new `dotnet-backend` skill** (PR #65) with:
- ASP.NET Core 8+ API patterns (Minimal APIs + controller-based).
- EF Core usage guidance, JWT auth examples, and background worker templates.
- Explicit trigger guidance and documented limitations.
- **Registry size increased to 713 skills** (from 634).

### Changed

- Regenerated and synced discovery artifacts after merging both PRs:
- `README.md` (counts + contributor updates)
- `skills_index.json`
- `CATALOG.md`
- `data/catalog.json`
- `data/bundles.json`
- `data/aliases.json`
- Release metadata updated for `v4.10.0`:
- `package.json` / `package-lock.json` version bump
- GitHub Release object published with release notes

### Contributors

- [@sohamganatra](https://github.com/sohamganatra) - 78 Composio automation skills (PR #64)
- [@Nguyen-Van-Chan](https://github.com/Nguyen-Van-Chan) - .NET backend skill (PR #65)

## [4.9.0] - 2026-02-05 - "OSS Hunter & Universal Skills"

> Automated contribution hunting and universal CLI AI skills (Audio, YouTube, Prompt Engineering).

### Added

- **New Skill**: `oss-hunter` – Automated tool for finding high-impact Open Source contributions (Good First Issues, Help Wanted) in trending repositories.
- **New Skill**: `audio-transcriber` – Transform audio recordings into professional Markdown with Whisper integration.
- **New Skill**: `youtube-summarizer` – Generate comprehensive summaries/notes from YouTube videos.
- **New Skill**: `prompt-engineer` (Enhanced) – Now includes 11 optimization frameworks (RTF, RISEN, etc.).
- **Registry**: 634 skills (from 626). Catalog regenerated.

### Changed

- **CLI AI Skills**: Merged core skills from `ericgandrade/cli-ai-skills`.

### Contributors

- [@jackjin1997](https://github.com/jackjin1997) - OSS Hunter (PR #61)
- [@ericgandrade](https://github.com/ericgandrade) - CLI AI Skills (PR #62)

## [4.7.0] - 2026-02-03 - "Installer Fix & OpenCode Docs"

> Critical installer fix for Windows and OpenCode documentation completion.

### Fixed

- **Installer**: Resolved `ReferenceError` for `tagArg` variable in `bin/install.js` ensuring correct execution on Windows/PowerShell (PR #53).

### Documentation

- **OpenCode**: Completed documentation for OpenCode integration in `README.md`.

---

## [4.6.0] - 2026-02-01 - "SPDD & Radix UI Design System"

> Agent workflow docs (SPDD) and Radix UI design system skill.

### Added

- **New Skill**: `radix-ui-design-system` – Build accessible design systems with Radix UI primitives (headless, theming, WCAG, examples).
- **Docs**: `skills/SPDD/` – Research, spec, and implementation workflow docs (1-research.md, 2-spec.md, 3-implementation.md).

### Registry

- **Total Skills**: 626 (from 625). Catalog regenerated.

---

## [4.5.0] - 2026-01-31 - "Stitch UI Design"

> Expert prompting guide for Google Stitch AI-powered UI design tool.

### Added

- **New Skill**: `stitch-ui-design` – Expert guide for creating effective prompts for Google Stitch AI UI design tool (Gemini 2.5 Flash). Covers prompt structure, specificity techniques, iteration strategies, design-to-code workflows, and 10+ examples for landing pages, mobile apps, and dashboards.

### Changed

- **Documentation**: Clarified in README.md and GETTING_STARTED.md that installation means cloning the full repo once; Starter Packs are curated lists to discover skills by role, not a different installation method (fixes [#44](https://github.com/sickn33/antigravity-awesome-skills/issues/44)).

### Registry

- **Total Skills**: 625 (from 624). Catalog regenerated.

### Credits

- [@ALEKGG1](https://github.com/ALEKGG1) – stitch-ui-design (PR #45)
- [@CypherPoet](https://github.com/CypherPoet) – Documentation clarity (#44)

---

## [4.4.0] - 2026-01-30 - "fp-ts skills for TypeScript"

> Three practical fp-ts skills for TypeScript functional programming.

### Added

- **New Skills** (from [whatiskadudoing/fp-ts-skills](https://github.com/whatiskadudoing/fp-ts-skills)):
  - `fp-ts-pragmatic` – Pipe, Option, Either, TaskEither without academic jargon.
  - `fp-ts-react` – Patterns for fp-ts with React 18/19 and Next.js 14/15 (state, forms, data fetching).
  - `fp-ts-errors` – Type-safe error handling with Either and TaskEither.

### Registry

- **Total Skills**: 624 (from 621). Catalog regenerated.

---

## [4.3.0] - 2026-01-29 - "VoltAgent Integration & Context Engineering Suite"

> 61 new skills from VoltAgent/awesome-agent-skills: official team skills and context engineering suite.

### Added

- **61 new skills** from [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills):
  - **Official (27)**: Sentry (commit, create-pr, find-bugs, iterate-pr), Trail of Bits (culture-index, fix-review, sharp-edges), Expo (expo-deployment, upgrading-expo), Hugging Face (hugging-face-cli, hugging-face-jobs), Vercel, Google Stitch (design-md), Neon (using-neon), n8n (n8n-code-python, n8n-mcp-tools-expert, n8n-node-configuration), SwiftUI, fal.ai (fal-audio, fal-generate, fal-image-edit, fal-platform, fal-upscale, fal-workflow), deep-research, imagen, readme.
  - **Community (34)**: Context suite (context-fundamentals, context-degradation, context-compression, context-optimization, multi-agent-patterns, memory-systems, evaluation), frontend-slides, linear-claude-skill, skill-rails-upgrade, terraform-skill, tool-design, screenshots, automate-whatsapp, observe-whatsapp, aws-skills, ui-skills, vexor, pypict-skill, makepad-skills, threejs-skills, claude-scientific-skills, claude-win11-speckit-update-skill, security-bluebook-builder, claude-ally-health, clarity-gate, beautiful-prose, claude-speed-reader, skill-seekers, varlock-claude-skill, superpowers-lab, nanobanana-ppt-skills, x-article-publisher-skill, ffuf-claude-skill.

### Registry

- **Total Skills**: 614 (from 553). Catalog and SOURCES.md updated.

### Credits

- VoltAgent/awesome-agent-skills and official teams (Sentry, Trail of Bits, Expo, Hugging Face, Vercel Labs, Google Labs, Neon, fal.ai).

---

## [4.0.0] - 2026-01-28 - "The Enterprise Era"

> **A massive integration of 300+ Enterprise skills, transforming Antigravity into a complete operating system for AI agents.**

### Added

- **Massive Skill Injection**: Merged 300+ Enterprise skills from `rmyndharis/antigravity-skills`.
- **New Categories**:
  - **Architecture & Design**: `backend-architect`, `c4-architecture`.
  - **Data & AI**: `rag-engineer`, `langchain-architecture`.
  - **Security**: `security-auditor`, `cloud-pentesting`.
- **Catalog System**: Introduced `CATALOG.md` and `scripts/build-catalog.js` for automated, table-based skill discovery.

### Changed

- **Documentation Overhaul**:
  - Removed the legacy 250+ row skill table from `README.md`.
  - Restructured `README.md` to focus on high-level domains.
  - Replaced static registry with dynamic `CATALOG.md`.
- **Version Bump**: Major version update to 4.0.0 reflecting the doubling of skill capacity (247 -> 550+).

### Credits

- **[@rmyndharis](https://github.com/rmyndharis)** - For the massive contribution of 300+ Enterprise skills and valid catalog logic.
- **[@sstklen](https://github.com/sstklen)** & **[@rookie-ricardo](https://github.com/rookie-ricard)** - Continued community support.

## [3.4.0] - 2026-01-27 - "Voice Intelligence & Categorization"

### Added

- **New Skill**: `voice-ai-engine-development` - Complete toolkit for building real-time voice agents (OpenAI Realtime, Vapi, Deepgram, ElevenLabs).
- **Categorization**: Major README update introducing a concise "Features & Categories" summary table.

### Changed

- **README**: Replaced text-heavy category lists with a high-level summary table.
- **Registry**: Synced generic skill count (256) across documentation.

### Contributors

- [@sickn33](https://github.com/sickn33) - Voice AI Engine (PR #33)
- [@community](https://github.com/community) - Categorization Initiative (PR #32)

## [3.3.0] - 2026-01-26 - "News & Research"

### Added

- **New Skills**:
  - `last30days`: Research any topic from the last 30 days on Reddit + X + Web.
  - `daily-news-report`: Generate daily news reports from multiple sources.

### Changed

- **Registry**: Updated `skills_index.json` and `README.md` registry (Total: 255 skills).

## [3.2.0] - 2026-01-26 - "Clarity & Consistency"

### Changed

- **Skills Refactoring**: Significant overhaul of `backend-dev-guidelines`, `frontend-design`, `frontend-dev-guidelines`, and `mobile-design`.
  - **Consolidation**: Merged fragmented documentation into single, authoritative `SKILL.md` files.
  - **Final Laws**: Introduced "Final Laws" sections to provide strict, non-negotiable decision frameworks.
  - **Simplification**: Removed external file dependencies to improve context retrieval for AI agents.

### Fixed

- **Validation**: Fixed critical YAML frontmatter formatting issues in `seo-fundamentals`, `programmatic-seo`, and `schema-markup` that were blocking strict validation.
- **Merge Conflicts**: Resolved text artifact conflicts in SEO skills.

## [3.1.0] - 2026-01-26 - "Stable & Deterministic"

### Fixed

- **CI/CD Drift**: Resolved persistent "Uncommitted Changes" errors in CI by making the index generation script deterministic (sorting by name + ID).
- **Registry Sync**: Synced `README.md` and `skills_index.json` to accurately reflect all 253 skills.

### Added (Registry Restore)

The following skills are now correctly indexed and visible in the registry:

- **Marketing & Growth**: `programmatic-seo`, `schema-markup`, `seo-fundamentals`, `form-cro`, `popup-cro`, `analytics-tracking`.
- **Security**: `windows-privilege-escalation`, `wireshark-analysis`, `wordpress-penetration-testing`, `writing-plans`.
- **Development**: `tdd-workflow`, `web-performance-optimization`, `webapp-testing`, `workflow-automation`, `zapier-make-patterns`.
- **Maker Tools**: `telegram-bot-builder`, `telegram-mini-app`, `viral-generator-builder`.

### Changed

- **Documentation**: Added `docs/CI_DRIFT_FIX.md` as a canonical reference for resolving drift issues.
- **Guidance**: Updated `docs/GETTING_STARTED.md` counts to match the full registry (253+ skills).
- **Maintenance**: Updated `MAINTENANCE.md` with strict protocols for handling generated files.

## [3.0.0] - 2026-01-25 - "The Governance Update"

### Added

- **Governance & Security**:
  - `docs/QUALITY_BAR.md`: Defined 5-point validation standard (Metadata, Risk, Triggers).
  - `docs/SECURITY_GUARDRAILS.md`: Enforced "Authorized Use Only" for offensive skills.
  - `CODE_OF_CONDUCT.md`: Adhered to Contributor Covenant v2.1.
- **Automation**:
  - `scripts/validate_skills.py`: Automated Quality Bar enforcement (Soft Mode supported).
  - `.github/workflows/ci.yml`: Automated PR checks.
  - `scripts/generate_index.py`: Registry generation with Risk & Source columns.
- **Experience**:
  - `docs/BUNDLES.md`: 9 Starter Packs (Essentials, Security, Web, Agent, Game Dev, DevOps, Data, Testing, Creative).
  - **Interactive Registry**: README now features Risk Levels (🔴/🟢/🟣) and Collections.
- **Documentation**:
  - `docs/EXAMPLES.md`: Cookbook with 3 real-world scenarios.
  - `docs/SOURCES.md`: Legal ledger for attributions and licenses.
  - Release announcements are documented in this CHANGELOG.

### Changed

- **Standardization**: All 250+ skills are now validated against the new Quality Bar schema.
- **Project Structure**: Introduced `docs/` folder for scalable documentation.

## [2.14.0] - 2026-01-25 - "Web Intelligence & Windows"

### Added

- **New Skill**:
  - `context7-auto-research`: Auto-research capability for Claude Code.
  - `codex-review`: Professional code review with AI integration.
  - `exa-search`: Semantic search and discovery using Exa API.
  - `firecrawl-scraper`: Deep web scraping and PDF parsing.
  - `tavily-web`: Content extraction and research using Tavily.
  - `busybox-on-windows`: UNIX tool suite for Windows environments.

### Changed

- **Documentation**: Updated `obsidian-clipper-template-creator` docs and templates.
- **Index & Registry**: Updated `skills_index.json` and `README.md` registry.

### Fixed

- **Skills**: Fixed YAML frontmatter quoting in `lint-and-validate`.

## [2.13.0] - 2026-01-24 - "NoSQL Expert"

### Added

- **New Skill**:
  - `nosql-expert`: Expert guidance for distributed NoSQL databases (Cassandra, DynamoDB), focusing on query-first modeling and anti-patterns.

### Changed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry.

### Contributors

- [@sickn33](https://github.com/sickn33) - PR #23

## [2.12.0] - 2026-01-23 - "Enterprise & UI Power"

### Added

- **New Skills**:
  - `production-code-audit`: Comprehensive enterprise auditing skill for production readiness.
  - `avalonia-layout-zafiro`: Zafiro layout guidelines for Avalonia UI.
  - `avalonia-viewmodels-zafiro`: ViewModel composition patterns for Avalonia.
  - `avalonia-zafiro-development`: Core development rules for Avalonia Zafiro applications.

### Changed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 243 skills).

### Contributors

- [@SuperJMN](https://github.com/SuperJMN) - PR #20
- [@Mohammad-Faiz-Cloud-Engineer](https://github.com/Mohammad-Faiz-Cloud-Engineer) - PR #21

## [2.11.0] - 2026-01-23 - "Postgres Performance"

### Added

- **New Skill**:
  - `postgres-best-practices`: Comprehensive Supabase PostgreSQL performance optimization guide with 30+ rules covering query performance, connection management, RLS security, schema design, locking, and monitoring.

### Changed

- **Official Sources**: Added [supabase/agent-skills](https://github.com/supabase/agent-skills) to Credits & Sources.
- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 239 skills).

### Contributors

- [@ar27111994](https://github.com/ar27111994) - PR #19

---

## [2.10.0] - 2026-01-22 - "Developer Excellence"

### Added

- **New Skills**:
  - `api-security-best-practices`: Comprehensive guide for secure API design and defense.
  - `environment-setup-guide`: Systematic approach to project onboarding and tool configuration.
  - `web-performance-optimization`: Methodologies for optimizing Core Web Vitals and loading speed.

### Changed

- **Enhanced Skill**:
  - `code-review-checklist`: Replaced with a much more detailed and systematic version covering functionality, security, and quality.

### Fixed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 238 skills).

### Added

- **Automation Support**:
  - `scripts/update_readme.py`: Automated script to sync skill counts and regenerate the registry table.
  - Updated `MAINTENANCE.md` to reflect the new automated workflow.
- **Repository Quality**:
  - `MAINTENANCE.md` is now tracked in the repository (removed from `.gitignore`).
  - Improved contribution guidelines.

## [2.8.0] - 2026-01-22 - "Documentation Power"

### Added

- **API Documentation Generator**: New skill to automatically generate comprehensive API documentation (`skills/api-documentation-generator`).
- **Remotion Best Practices**: 28 modular rules for programmatic video creation (`skills/remotion-best-practices`).

## [2.7.0] - 2026-01-22 - "Agent Memory"

### Added

- **Agent Memory MCP**: New skill providing persistent, searchable knowledge management for AI agents (`skills/agent-memory-mcp`).

### Changed

- **Renamed Skill**: `agent-memory` was renamed to `agent-memory-mcp` to avoid naming conflicts.

---

## [2.6.0] - 2026-01-21 - "Everything Skills Edition"

### Added

- **8 Verified Skills** from [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code):
  - `cc-skill-backend-patterns`
  - `cc-skill-clickhouse-io`
  - `cc-skill-coding-standards`
  - `cc-skill-continuous-learning`
  - `cc-skill-frontend-patterns`
  - `cc-skill-project-guidelines-example`
  - `cc-skill-security-review`
  - `cc-skill-strategic-compact`
- **Documentation**: New `docs/WALKTHROUGH.md` for import process details.

### Changed

- **Skill Cleanup**: Removed 27 unwanted agents, commands, and rules from the `everything-claude-code` import to focus strictly on skills.
- **Index**: Regenerated `skills_index.json` (Total: 233 skills).
- **Credits**: Updated README credits and registry.

## [1.0.0] - 2026-01-19 - "Marketing Edition"

### Added

- **23 Marketing & Growth skills** from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills):
  - **CRO**: `page-cro`, `signup-flow-cro`, `onboarding-cro`, `form-cro`, `popup-cro`, `paywall-upgrade-cro`
  - **Content**: `copywriting`, `copy-editing`, `email-sequence`
  - **SEO**: `seo-audit`, `programmatic-seo`, `schema-markup`, `competitor-alternatives`
  - **Paid**: `paid-ads`, `social-content`
  - **Growth**: `referral-program`, `launch-strategy`, `free-tool-strategy`
  - **Analytics**: `ab-test-setup`, `analytics-tracking`
  - **Strategy**: `pricing-strategy`, `marketing-ideas`, `marketing-psychology`
- New "Marketing & Growth" category in Features table

### Changed

- Total skills count: **179**

---

## [0.7.0] - 2026-01-19 - "Education Edition"

### Added

- **Moodle External API Development** skill via PR #6
- Comprehensive Moodle LMS web service API development

### Changed

- Total skills count: **156**

---

## [0.6.0] - 2026-01-19 - "Vibeship Integration"

### Added

- **57 skills** from [vibeforge1111/vibeship-spawner-skills](https://github.com/vibeforge1111/vibeship-spawner-skills):
  - AI Agents category (~30 skills)
  - Integrations & APIs (~25 skills)
  - Maker Tools (~11 skills)
- Alphabetically sorted skill registry

### Changed

- Total skills count: **155**

---

## [0.5.0] - 2026-01-18 - "Agent Manager"

### Added

- **Agent Manager Skill** - Multi-agent orchestration via tmux
- Major repository expansion with community contributions

### Changed

- Total skills count: **131**

---

## [0.4.0] - 2026-01-18 - "Security Fortress"

### Added

- **60+ Cybersecurity skills** from [zebbern/claude-code-guide](https://github.com/zebbern/claude-code-guide):
  - Ethical Hacking Methodology
  - Metasploit Framework
  - Burp Suite Testing
  - SQLMap, Active Directory, AWS Pentesting
  - OWASP Top 100 Vulnerabilities
  - Red Team Tools
- `claude-code-guide` skill

### Changed

- Total skills count: ~90

---

## [0.3.0] - 2026-01-17 - "First Stable Registry"

### Added

- Complete skill registry table in README
- GitHub workflow automation
- SEO optimizations

### Changed

- Total skills count: **71**

---

## [0.2.0] - 2026-01-16 - "Official Skills"

### Added

- **Official Anthropic skills** integration
- **Vercel Labs skills** integration
- BlockRun: Agent Wallet for LLM Micropayments
- 7 new skills from GitHub analysis

### Changed

- Total skills count: **~65**

---

## [0.1.0] - 2026-01-15 - "Initial Release"

### Added

- **58 core skills** aggregated from community:
  - [obra/superpowers](https://github.com/obra/superpowers) - Original Superpowers
  - [guanyang/antigravity-skills](https://github.com/guanyang/antigravity-skills) - Core extensions
  - [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Infrastructure skills
  - [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) - React UI patterns
  - [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Loki Mode
  - [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) - Senior Engineering
- Universal **SKILL.md** format
- Compatibility with Claude Code, Gemini CLI, Cursor, Copilot, Antigravity

---

## Credits

See [README.md](README.md#credits--sources) for full attribution.

## License

MIT License - See [LICENSE](LICENSE) for details.
