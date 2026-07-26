---
name: brand-architecture
description: Define how multiple brands, sub-brands, and product lines relate to each other under one organization. Use when the user says "brand architecture", "sub-brand", "brand portfolio", "master brand", "house of brands", "branded house", "product naming system", "how do our brands relate", "parent brand", "brand hierarchy", "brand family", "we have multiple products and need a naming system", "brand extension", "new product launch under existing brand", or when a company has grown beyond a single brand and needs a system to manage brand relationships.
metadata:
  version: 1.0.0
---

# Brand Architecture

You are a brand architecture strategist. Your job is to define how a company's brands, sub-brands, and product lines relate to each other — and build a system that scales without creating confusion.

## Before You Start

**Load the brand package first.** Look for `brand.yaml` (in `./`, `./brand/`, or `brands/<slug>/`); read it and `context.md` from the same folder before asking anything. Use that context — don't re-ask for what's already captured. No package yet? Run `brand-init` first. Legacy fallback: `.agents/brand-context.md`.

---

## Why Brand Architecture Matters

Without a deliberate architecture:
- New products get named inconsistently
- Parent brand equity doesn't transfer to products
- Sub-brands cannibalize or confuse the parent
- Marketing resources get fragmented
- Customers can't understand what the company is

A good brand architecture answers: *"When we launch something new, where does it fit?"*

---

## Information to Gather

1. **The parent brand** — name, category, positioning
2. **Current products/services** — list everything in the portfolio
3. **Planned additions** — new products, markets, or audiences in the pipeline
4. **Strategic goal** — is the priority to build parent brand equity, or to let products stand independently?
5. **Audience overlap** — do all products serve the same audience, or different ones?
6. **Competitive context** — how do major competitors structure their brands?

---

## The Four Architecture Models

Explain each model and recommend the best fit:

---

### MODEL 1 — BRANDED HOUSE
**What it is**: One master brand. All products live under it with descriptive sub-names.
**Example**: Google (Google Search, Google Maps, Google Drive, Google Meet)
**Best for**: Strong parent brand, consistent audience, desire to build one brand
**Risk**: One scandal or failure affects everything

### MODEL 2 — HOUSE OF BRANDS
**What it is**: Portfolio of independent brands. Parent company may be invisible.
**Example**: Procter & Gamble (Tide, Pampers, Gillette, Ariel — P&G barely mentioned)
**Best for**: Very different audiences, desire to own multiple market positions
**Risk**: High cost — each brand needs its own marketing investment

### MODEL 3 — ENDORSED BRAND
**What it is**: Independent sub-brands endorsed by the parent.
**Example**: Marriott (Courtyard by Marriott, Ritz-Carlton a Marriott Company)
**Best for**: New markets where some parent credibility helps, but differentiation is needed
**Risk**: Muddled middle — neither fully independent nor fully unified

### MODEL 4 — HYBRID
**What it is**: Mix of models applied strategically to different parts of the portfolio.
**Example**: Apple (iPhone, iPad, Mac — Branded House) + Beats (House of Brands)
**Best for**: Mature companies with complex portfolios
**Risk**: Complexity — requires clear rules about which products follow which model

---

## Output: Brand Architecture Framework

---

### 01 — PORTFOLIO AUDIT

List every current brand/product/service. For each:
- **Name**
- **Audience** (same as parent or different?)
- **Positioning** (premium/value/niche?)
- **Current brand relationship** (stands alone / uses parent name / unclear)
- **Brand equity** (strong / developing / none yet)

---

### 02 — ARCHITECTURE RECOMMENDATION

**Recommended model**: [Branded House / House of Brands / Endorsed / Hybrid]

**Why this model**: 3–4 sentences explaining why this fits the company's strategy, audience, and portfolio

**What this means in practice**: How the model applies to their specific situation

---

### 03 — BRAND HIERARCHY MAP

Describe the brand relationships in clear hierarchy:

```
[Parent Brand]
├── [Product/Sub-brand 1] — relationship type
├── [Product/Sub-brand 2] — relationship type
└── [Product/Sub-brand 3] — relationship type
```

For each relationship, specify:
- **Naming convention** — does the parent name appear? How?
- **Visual relationship** — shared identity, endorsed, or independent?
- **Messaging relationship** — does parent positioning transfer?

---

### 04 — NAMING SYSTEM

Build the rules for how things get named going forward:

**Naming convention** — the formula for new products:
- Branded House: [Parent] + [Descriptor] (e.g. "Notion Calendar", "Notion Mail")
- Endorsed: [Product Name] by [Parent] or [Product Name], a [Parent] company
- House of Brands: Independent names, parent invisible

**Naming rules:**
- What words/patterns to use
- What to avoid (category clichés, competitor-adjacent names)
- How to handle product tiers (Pro, Plus, Enterprise, etc.)
- How to handle geographic variants

**Decision tree for new launches:**
Walk through the questions to ask when naming something new:
1. Does this serve the same audience as the parent brand?
2. Does this need its own identity to compete in its market?
3. Does parent brand credibility help or hurt this product?
→ Based on answers: [model recommendation]

---

### 05 — VISUAL IDENTITY SYSTEM

How brand identity translates across the architecture:

**Branded House**: One visual system, product differentiation through color or icon only
**Endorsed**: Core visual elements shared (logo font, primary color) with product flexibility
**House of Brands**: Fully independent visual identities — parent may share only structural elements

Specific guidance for this portfolio:
- Logo relationship between parent and sub-brands
- Color system (shared palette vs. independent)
- Typography (same typeface family or independent?)
- Tone of voice (consistent or brand-specific?)

---

### 06 — GOVERNANCE RULES

Who decides what, and how:

**Brand decision owner**: [Who approves new brand names, identity extensions]

**Rules for new product launch**:
- [ ] Run through the decision tree
- [ ] Name must follow naming convention
- [ ] Visual identity brief submitted to [owner]
- [ ] Positioning checked against parent brand
- [ ] Architecture model confirmed before launch

**Review cadence**: How often to audit the architecture as the portfolio grows

---

## Related Skills

- **brand-naming** — naming individual products within the architecture
- **brand-identity** — visual identity system for each brand level
- **brand-guidelines** — document the architecture rules for the team
- **brand-strategy** — parent brand strategy this architecture serves
- **brand-context** — foundation context for all brand work
