# Legacy knowledge: design-spec

> **Cold reference only.** Migrated from AG Kit v1 for knowledge preservation. Current v2 skill, flow, safety, runtime, and path contracts override any legacy activation/tool/agent/workflow instructions below. Supporting files are preserved only as on-demand reference assets; scripts are never auto-executed by the migration contract.

Source: `.agents/skills/design-spec/` at `549ba3dc2eb1`.

---

# DESIGN.md Specification

> A DESIGN.md is the **single source of truth** for a project's visual language. Create it BEFORE building UI.
> Two layers: machine-readable **design tokens** (YAML front matter) + human-readable **rationale** (markdown body).
> Tokens are normative; prose gives context. Prose may use descriptive names ("Midnight Forest Green") that map to systematic token names (`primary`).
>
> _Format adapted from the [DESIGN.md spec](https://github.com/google-labs-code/design.md) (Google Labs, Apache-2.0). A linter/exporter exists: `npx @google/design.md`._
>
> 📚 **Reference library:** [collection.md](collection.md) — 70+ real-world DESIGN.md files (Airbnb, Stripe, Linear, Vercel, Apple…) to study or adapt as a starting point.

---

## When to produce a DESIGN.md

This is a **hard gate** for UI work (see `.agents/rules/design-rules.md`): before writing components, pages, or styles, a `DESIGN.md` must exist at the project root. If absent, create it first from the brief; if present, read it and conform.

The token block converts cleanly to/from `tokens.json`, Figma variables, and Tailwind theme config — so it is the bridge between design intent and code.

---

## 1. File structure

```
---
<YAML token front matter>
---

# Project Name (optional title)

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

Front matter MUST begin and end with a line containing exactly `---`. Sections use `##` headings, appear in the order above, and may be omitted if irrelevant. Domain-specific sections may be added.

---

## 2. Token schema (YAML front matter)

```yaml
version: alpha            # optional
name: Daylight Prestige
description: ...          # optional
colors:
  <token-name>: "#RRGGBB"
typography:
  <token-name>:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
rounded:
  <scale>: 8px
spacing:
  <scale>: 16px           # Dimension or unitless number
components:
  <component-name>:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px
```

`<scale>` is a named level: `xs sm md lg xl full` (any descriptive key is valid).

---

## 3. Type system

| Type | Format | Example |
|------|--------|---------|
| Color | `#` + hex (sRGB) | `"#1A1C1E"` |
| Dimension | number + unit (`px`/`em`/`rem`) | `48px`, `-0.02em` |
| Token Reference | `{path.to.token}` | `{colors.primary}` |
| Typography | composite object | see §4 |

**Typography properties:** `fontFamily` (string), `fontSize` (Dimension), `fontWeight` (number — bare or quoted are equivalent in YAML), `lineHeight` (Dimension or unitless multiplier — unitless recommended), `letterSpacing` (Dimension), `fontFeature` (string), `fontVariation` (string).

**Token references:** wrapped in `{}` pointing to another value in the tree. Most groups must reference a **primitive** (`{colors.primary-60}`), not a group. Inside `components`, references to **composite** values are allowed (`{typography.label-md}`).

**Component property tokens:** `backgroundColor`, `textColor` (Color); `typography` (Typography); `rounded`, `padding`, `size`, `height`, `width` (Dimension).

**Variants:** define UI states as separate entries with a related key — `button-primary`, `button-primary-hover`.

---

## 4. Sections (canonical order)

| # | Section | Aliases | Purpose |
|---|---------|---------|---------|
| 1 | Overview | Brand & Style | Brand personality, audience, emotional tone. Fallback context when a token isn't defined. |
| 2 | Colors | | Palettes; at least `primary`. Common: primary/secondary/tertiary/neutral. |
| 3 | Typography | | 9–15 levels, each a semantic role (headline/body/label) × size. |
| 4 | Layout | Layout & Spacing | Grid model, spacing scale, containment. |
| 5 | Elevation & Depth | Elevation | Shadows, OR for flat designs the alternative (borders, tonal layers, contrast). |
| 6 | Shapes | | Corner radii, edge treatment, shape language. |
| 7 | Components | | Per-atom guidance: Buttons, Inputs, Cards, Chips, Lists, etc. |
| 8 | Do's and Don'ts | | Guardrails during generation. |

---

## 5. Recommended token names (guidance, not required)

- **Colors:** `primary secondary tertiary neutral surface on-surface error`
- **Typography:** `headline-display headline-lg headline-md body-lg body-md body-sm label-lg label-md label-sm`
- **Rounded:** `none sm md lg xl full`

---

## 6. Consumer behavior for unknown content

The spec is extensible. When encountering content it doesn't define:

| Scenario | Behavior |
|----------|----------|
| Unknown section heading (`## Iconography`) | Preserve; do not error |
| Unknown color token name | Accept if value is valid |
| Unknown typography token name | Accept as valid typography |
| Unknown spacing value | Accept; store as string if not a valid dimension |
| Unknown component property | Accept with warning |
| **Duplicate section heading** (two `## Colors`) | **Error; reject the file** |

---

## 7. Minimal example

```markdown
---
name: Calm Scheduler
colors:
  primary: "#1A1C1E"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1: { fontFamily: Public Sans, fontSize: 48px, fontWeight: 600, lineHeight: 1.1 }
  body-md: { fontFamily: Public Sans, fontSize: 16px, fontWeight: 400, lineHeight: 1.6 }
rounded: { sm: 4px, md: 8px }
spacing: { sm: 8px, md: 16px, lg: 32px }
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    rounded: "{rounded.md}"
    padding: 12px
---

# Calm Scheduler

## Overview
A calm, professional interface for a healthcare scheduling platform.
Accessibility-first: high contrast, generous touch targets.

## Colors
- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Tertiary (#B8422E):** The sole driver for interaction.
- **Neutral (#F7F5F2):** Warm limestone foundation.

## Do's and Don'ts
- Do use the tertiary color only for the single most important action per screen.
- Don't mix rounded and sharp corners in the same view.
- Do maintain WCAG AA contrast (4.5:1 for normal text).
```

---

## Workflow

1. Read the brief and infer the design direction (see `frontend-design` / `mobile-design`).
2. **ALWAYS read [collection.md](collection.md) first** — 70+ real-world DESIGN.md files. Find the 1–2 closest in vibe/industry to the brief, open their `DESIGN.md` on GitHub, and study how they structure tokens. Adapt, never blindly copy.
3. **Write `DESIGN.md` at the project root** — tokens first, then rationale prose.
4. Build UI strictly against the tokens. Descriptive names in prose must map to token names.
5. Keep DESIGN.md in sync when the visual language changes — it stays the source of truth.
