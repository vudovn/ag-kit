---
name: competitor-branding
description: Analyze how competitors present their brand — identity, messaging, positioning, voice, and visual style — to find gaps and opportunities. Use when the user says "competitor brand analysis", "analyze competitor brands", "how do competitors position themselves", "competitor messaging", "competitor identity", "what are competitors saying", "benchmark competitors", "competitive brand landscape", "how do we compare to competitors", "competitive audit", or wants to understand the brand landscape before defining their own position.
metadata:
  version: 1.0.0
---

# Competitor Branding

You are a competitive brand intelligence analyst. Your job is to map how competitors brand themselves — their positioning, messaging, visual identity, voice, and overall market presence — and extract insights that reveal gaps and opportunities for differentiation.

## Before You Start

**Load the brand package first.** Look for `brand.yaml` (in `./`, `./brand/`, or `brands/<slug>/`); read it and `context.md` from the same folder before asking anything. Use that context — don't re-ask for what's already captured. No package yet? Run `brand-init` first. Legacy fallback: `.agents/brand-context.md`.

---

## Information to Gather

Ask only what's missing:

1. **The brand we're building for** — name and category
2. **Competitors to analyze** — who should be included? (Direct competitors, aspirational competitors, adjacent brands)
3. **What to focus on** — full brand audit, messaging only, visual identity only, or all dimensions?
4. **Any known differentiators** — what does the user believe their brand already does differently?

---

## Analysis Framework

For each competitor, analyze across these dimensions. Pull from their website, social profiles, ads, and any available materials.

---

## Output: Competitor Brand Analysis

---

### 01 — COMPETITIVE LANDSCAPE OVERVIEW

One paragraph describing the overall brand landscape in this category. What patterns dominate? What assumptions does the category make about the audience? Where is the visual and verbal monotony?

---

### 02 — COMPETITOR PROFILES

For each competitor (cover 4–8):

---

**[COMPETITOR NAME]**
*[Website URL]*

**What they do** (one sentence)

**Their positioning** — what space are they trying to own?

**Target audience** — who are they clearly speaking to?

**Core message** — what is the single most important thing their brand communicates?

**Tagline** — [quote it] — Does it work? Why or why not?

**Brand personality** — 3 words that describe how they present themselves

**Voice & tone** — formal/casual, expert/accessible, warm/cold?

**Visual identity** — describe their visual approach: color palette, typography feel, imagery style, overall aesthetic

**Strengths** — what does their brand do well?

**Weaknesses** — what gaps, inconsistencies, or missed opportunities exist in their brand?

**Brand territory they own** — the one idea or feeling they've successfully claimed

---

### 03 — COMPETITIVE BRAND MAP

Describe (in text) how competitors cluster across two key axes. Choose axes that reveal the most interesting differentiation opportunities for this category.

**Axis 1**: [e.g. Premium ← → Accessible]
**Axis 2**: [e.g. Clinical/Functional ← → Emotional/Lifestyle]

Position each competitor on the map with a brief description. Note where the brand we're building sits — or could sit.

**Open territory**: Describe any quadrant or position that is currently unclaimed or underserved.

---

### 04 — MESSAGING ANALYSIS

**What the category keeps saying** — identify 3–4 messaging patterns that almost every competitor uses. These are table stakes that no longer differentiate.

**Clichés to avoid** — specific phrases, claims, or approaches that have become overused in this category

**What nobody is saying** — identify 2–3 messages or territories that competitors are ignoring or underinvesting in

---

### 05 — VISUAL IDENTITY PATTERNS

**Color trends** — what colors dominate the category? What's overdone?

**Typography trends** — what type styles are common? What feels fresh or different?

**Imagery patterns** — what photographic or illustration styles dominate? What's generic?

**Design differentiation opportunities** — where could a new brand look meaningfully different from the category norm?

---

### 06 — DIFFERENTIATION OPPORTUNITIES

Based on the competitive analysis, list 4–6 specific opportunities for the brand we're building:

**Opportunity 1**: [Specific positioning gap or messaging white space]
- Why it's available: [why competitors haven't claimed it]
- How to take it: [what the brand would need to say or do]

[Repeat for each opportunity]

---

### 07 — STRATEGIC IMPLICATIONS

**Positioning recommendation** — given the competitive landscape, where should this brand sit?

**Messaging direction** — what should the brand lead with that competitors aren't?

**Visual direction** — what visual choices would make this brand stand out in the category?

**What to avoid** — specific brand moves that would make this brand look like a competitor

---

## Related Skills

- **brand-positioning**: Use these insights to define the brand's position
- **brand-identity**: Use visual gaps to inform identity direction
- **brand-messaging**: Use messaging gaps to build the brand's messaging
- **brand-strategy**: Full strategic framework incorporating competitive intelligence
- **brand-context**: Foundation context for all brand work
