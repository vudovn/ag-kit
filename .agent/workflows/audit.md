---
description: 360° project audit across security, performance, accessibility, SEO, and code quality. Produces an executive report with severity ratings and a prioritized remediation roadmap.
---

# /audit — 360° Project Audit

$ARGUMENTS

---

## When to Use

- Before a production deployment
- After a security incident
- Quarterly health check
- Before onboarding a new team
- When something "feels off" but you can't pinpoint it

---

## Task

Execute a comprehensive audit across all dimensions of project health.

### Audit Protocol

#### Step 1: Load Skills

- `vulnerability-scanner`
- `performance-profiling`
- `seo-fundamentals`
- `frontend-design`
- `clean-code`

#### Step 2: Automated Scans (run all)

```bash
# Security
python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
python .agent/skills/vulnerability-scanner/scripts/dependency_analyzer.py .

# Code Quality
python .agent/skills/lint-and-validate/scripts/lint_runner.py .
python .agent/skills/lint-and-validate/scripts/type_coverage.py .

# Frontend
python .agent/skills/frontend-design/scripts/ux_audit.py .
python .agent/skills/frontend-design/scripts/accessibility_checker.py .

# SEO
python .agent/skills/seo-fundamentals/scripts/seo_checker.py .

# Performance
python .agent/skills/performance-profiling/scripts/lighthouse_audit.py <url>
python .agent/skills/performance-profiling/scripts/bundle_analyzer.py .

# Testing
python .agent/skills/testing-patterns/scripts/test_runner.py .
```

#### Step 3: Severity Classification

| Level | Definition | SLA to Fix |
|-------|-----------|-----------|
| 🔴 **Critical** | Active security vulnerability, data breach risk | Immediately (24h) |
| 🟠 **High** | Significant performance issue, auth flaw, major UX failure | This sprint |
| 🟡 **Medium** | Code quality issue, minor performance, missing tests | Next sprint |
| 🟢 **Low** | Best practice deviation, style issue | Backlog |
| 🔵 **Info** | Observation, improvement opportunity | Optional |

---

## Audit Dimensions

### 1. Security Audit

- [ ] Dependency vulnerabilities (CVEs)
- [ ] Secrets/API keys not in code
- [ ] Authentication hardened (MFA, rate limiting)
- [ ] SQL/NoSQL injection protected
- [ ] CORS configured correctly
- [ ] CSP headers present
- [ ] HTTPS enforced

### 2. Performance Audit

- [ ] Lighthouse score > 90 (Performance)
- [ ] Core Web Vitals: LCP < 2.5s, CLS < 0.1, FID < 100ms
- [ ] Bundle size reasonable (< 200KB initial JS)
- [ ] Images optimized (WebP, lazy loading)
- [ ] No N+1 database queries
- [ ] Caching strategy in place

### 3. Accessibility Audit (WCAG 2.2 AA)

- [ ] All images have alt text
- [ ] Form labels associated with inputs
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Keyboard-navigable
- [ ] Focus management correct
- [ ] ARIA roles correct

### 4. SEO Audit

- [ ] Title tags unique and descriptive
- [ ] Meta descriptions on all pages
- [ ] H1 present and unique per page
- [ ] Canonical URLs set
- [ ] Sitemap.xml and robots.txt exist
- [ ] Structured data (JSON-LD) for rich snippets

### 5. Code Quality Audit

- [ ] Zero ESLint errors
- [ ] TypeScript strict mode, no `any`
- [ ] Test coverage > 70%
- [ ] No dead code
- [ ] No console.logs in production
- [ ] Environment variables documented

---

## Output Format — Executive Report

```markdown
# 360° Audit Report
**Project:** [name]
**Date:** [date]
**Auditor:** audit workflow via Antigravity Kit

---

## Executive Summary
[3-4 sentence overall health assessment]

**Overall Health Score: [X]/100**

| Dimension | Score | Top Issue |
|-----------|-------|-----------|
| Security | [X]/20 | [issue] |
| Performance | [X]/20 | [issue] |
| Accessibility | [X]/20 | [issue] |
| SEO | [X]/20 | [issue] |
| Code Quality | [X]/20 | [issue] |

---

## 🔴 Critical Issues ([N])
1. [Issue] — **[File/Area]** — Fix: [recommendation]

## 🟠 High Issues ([N])
1. [Issue] — **[File/Area]** — Fix: [recommendation]

## 🟡 Medium Issues ([N])
...

## Remediation Roadmap
| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 1 | [Critical issue] | [Sm/Md/Lg] | [High/Med/Low] |
| 2 | [High issue] | [Sm/Md/Lg] | [High/Med/Low] |

## Next Audit
Recommended: [date / after resolving critical items]
```
