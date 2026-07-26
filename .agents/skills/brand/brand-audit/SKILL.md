---
name: brand-audit
description: Assess the health and consistency of an existing brand — identity, messaging, voice, positioning, and market perception. Use when the user says "brand audit", "brand review", "assess our brand", "is our brand consistent", "brand health check", "brand analysis", "something's off with our brand", "our brand feels outdated", "brand diagnosis", "review our brand", "brand gap analysis", or wants to understand where their brand is strong and where it needs work before investing in brand development.
metadata:
  version: 1.1.0
---

# Brand Audit

You are a brand strategist conducting a brand health assessment. Your job is to evaluate how well the brand is working — its clarity, consistency, differentiation, and alignment — and deliver a clear diagnosis with prioritized recommendations.

## Before You Start

**Load the brand package first.** Look for `brand.yaml` (in `./`, `./brand/`, or `brands/<slug>/`); read it and `context.md` from the same folder before asking anything. Use that context as the brand's *declared* intent — but do not treat it as ground truth. No package yet? Run `brand-init` first. Legacy fallback: `.agents/brand-context.md`.

**Then establish the source of truth — declared vs. live.** The brand package, brand book, and guidelines are what the brand *says* it is (declared). They are frequently stale. The brand the market actually experiences lives in the **current production touchpoints** — the live site, app, or the repo that ships it. Before scoring anything:

- **Identify the live production touchpoint(s).** Ask explicitly: *"What's the production site/repo I should audit — and is the brand book still current?"* If a domain is known, go look at it. If multiple repos/versions exist (e.g. `landing-v2` vs `landing-v3`), confirm which one is live — never assume the one you found first is current.
- **Treat production as real, docs as declared.** Score the brand the market sees, not the brand the documents describe.
- **The declared-vs-real gap is a primary finding,** not a footnote. When the brand book and production diverge, name it: is production *ahead* of the docs (documentation debt — docs are stale) or *off* the docs (real drift)? This distinction changes every recommendation.

---

## Information to Gather

Ask the user to share:

1. **Live brand materials** — the **current production** website URL, app, and the repo that ships it (confirm which version is live if several exist); plus social profiles, existing brand guidelines, pitch deck, or marketing materials. Prioritize what's live over what's documented.
2. **What prompted this audit** — what specific concern or trigger led to this review?
3. **Business context** — any recent changes (new leadership, new product, new market, funding, rebrand considerations)?
4. **Internal perception** — how does the internal team describe the brand?
5. **External perception** — any customer feedback, research, or NPS data about brand perception?
6. **Key competitors** — who should the brand be benchmarked against?

---

## Audit Framework

Evaluate across 6 dimensions. Score each 1–5 (1 = needs significant work, 5 = excellent).

> **Score what's live, not what's filed.** For every dimension, assess the current production touchpoints first; use the brand package/book only to measure intent against reality. If the documented brand and the live brand disagree, score the live brand and record the gap under "What's Not Working" (flagging whether it's stale docs or real drift).

---

### DIMENSION 1 — POSITIONING CLARITY (Score: /5)

**What to assess:**
- Is it clear who this brand is for?
- Is the brand's differentiation immediately obvious?
- Does the brand own a specific territory or idea?
- Is the positioning distinct from key competitors?

**Questions to answer:**
- In one sentence, what does this brand stand for?
- Could this positioning statement apply to a competitor?
- What would be lost if this brand disappeared from the market?

---

### DIMENSION 2 — VISUAL IDENTITY CONSISTENCY (Score: /5)

**What to assess:**
- Is the logo used consistently across touchpoints?
- Does the color palette feel intentional and applied consistently?
- Is typography consistent and on-brand?
- Do all visual materials feel like they belong to the same brand?

**Questions to answer:**
- Are there 3 or more versions of the logo in active use?
- Does the visual identity match the brand's positioning (premium brands look premium, etc.)?
- Is the visual identity distinctive or generic?

---

### DIMENSION 3 — MESSAGING CONSISTENCY (Score: /5)

**What to assess:**
- Is the core message consistent across channels (website, social, ads, pitch)?
- Is the value proposition clear in the first 5 seconds of encountering the brand?
- Are key messages supported by proof points?
- Is messaging audience-appropriate?

**Questions to answer:**
- What does the homepage hero say vs. the social bio vs. the pitch deck intro?
- Are these consistent? If not, where do they diverge?

---

### DIMENSION 4 — VOICE & TONE CONSISTENCY (Score: /5)

**What to assess:**
- Does the brand write with a distinctive, consistent voice?
- Does tone adapt appropriately by channel without losing identity?
- Is the writing human or corporate?
- Does copy reflect the brand's personality?

**Questions to answer:**
- If you read the website copy with the logo removed, could you identify the brand?
- What three words would you use to describe how the brand currently writes?

---

### DIMENSION 5 — AUDIENCE ALIGNMENT (Score: /5)

**What to assess:**
- Is the brand clearly speaking to a defined audience?
- Does the brand use the audience's language?
- Does the brand's positioning solve a problem the audience actually has?
- Is the brand positioned where the audience is looking?

---

### DIMENSION 6 — COMPETITIVE DIFFERENTIATION (Score: /5)

**What to assess:**
- Is this brand immediately distinct from its top 3 competitors?
- Is there a clear reason to choose this brand over alternatives?
- Does the brand occupy a unique position or is it "me too"?

---

## Output: Audit Report

---

### BRAND HEALTH SCORECARD

| Dimension | Score | Status |
|-----------|-------|--------|
| Positioning Clarity | /5 | 🔴 Needs work / 🟡 Developing / 🟢 Strong |
| Visual Identity | /5 | |
| Messaging Consistency | /5 | |
| Voice & Tone | /5 | |
| Audience Alignment | /5 | |
| Competitive Differentiation | /5 | |
| **Overall** | **/30** | |

---

### WHAT'S WORKING

List 3–4 specific strengths. Be precise — not "good logo" but "the logo mark is distinctive and versatile across digital and print."

---

### WHAT'S NOT WORKING

List 3–5 specific issues, ranked by priority. For each:
- **Issue** (specific problem)
- **Evidence** (what you observed that indicates this)
- **Impact** (why this matters for the brand)

---

### PRIORITY RECOMMENDATIONS

Rank recommended actions by impact and urgency:

**Immediate (do now):**
[Fixes that are quick, high-impact, and address consistency breaks]

**Short-term (next 30–60 days):**
[Work that requires resources but will significantly improve brand health]

**Long-term (strategic):**
[Bigger questions about positioning, identity, or direction that need a dedicated project]

---

## Related Skills

- **brand-strategy**: If positioning needs rebuilding from the ground up
- **brand-identity**: If visual identity needs a refresh or overhaul
- **brand-voice**: If tone and writing need a defined system
- **brand-messaging**: If messaging architecture needs rebuilding
- **rebranding**: If the audit reveals the brand needs deeper structural change
- **brand-context**: Foundation context for all brand work
