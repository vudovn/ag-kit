---
name: brand-extractor
description: Extract comprehensive brand profiles from URLs, descriptions, or existing assets using a multi-tier AI analysis with web search fallback. Use when "extracting brand identity", "brand analysis", "brand profiling", or "creating brand profiles".
metadata:
  mcpmarket-version: 1.0.0
---
# Brand Extractor

## Quick Reference
| Category | Trigger | Complexity | Source |
|----------|---------|------------|--------|
| brand-design | "brand analysis", "extract brand", "brand profile", "brand identity" | Medium | 6 projects |

Extract structured brand profiles from any input — a URL, a text description, uploaded assets, or a company name. The skill produces a typed `BrandProfile` object with tone, values, colors, typography, and positioning, plus optional supporting brand documentation files. It uses a multi-tier fallback strategy to maximize extraction quality regardless of input quality.

## When to Use
- User provides a URL and wants brand identity extracted from the live site
- User describes a brand verbally and needs it formalized into a profile
- User has existing brand assets (logos, PDFs, screenshots) to analyze
- A downstream skill (brand-css-generator, generative-page-pipeline) needs a BrandProfile as input
- User wants to generate a full brand documentation package (identity, voice, visual, etc.)

## Instructions

### Step 1: Determine the Input Type

Classify the user's input into one of four categories. This determines which extraction tier to start with.

| Input Type | Example | Starting Tier |
|------------|---------|---------------|
| URL | `https://acme.com` | Tier 1 (web search) |
| Company name | "Stripe" | Tier 1 (web search) |
| Verbal description | "A playful fintech startup for Gen Z" | Tier 2 (training knowledge) |
| Uploaded assets | Logo PNG, brand PDF, screenshot | Tier 2 (training knowledge) |

### Step 2: Execute the Multi-Tier Fallback Strategy

Run through the tiers in order. Stop at the first tier that produces a confidence score above 0.6. If a tier fails or returns low confidence, fall through to the next.

#### Tier 1: Claude + Web Search (confidence target: 0.85)

Use web search to gather live brand information. Search for the company's homepage, About page, press/media kit, brand guidelines PDF (`"{brand name}" brand guidelines filetype:pdf`), social media profiles (for tone calibration), press coverage (for positioning context), and competitor landscape. This tier produces the highest confidence because it uses real, current brand signals.

#### Tier 2: Claude Training Knowledge (confidence target: 0.7)

For well-known brands, rely on training knowledge. For verbal descriptions, infer attributes from the description. Works well for major brands (Apple, Nike, Airbnb) but degrades for smaller companies. If the description is too vague, ask: "What industry?", "Who is the audience?", "Name 2-3 brands this should feel similar to (and 2-3 it should NOT feel like)."

#### Tier 3: Local Knowledge Base — lookupBrand (confidence target: 0.6)

Check if a local brand profile already exists in the project's brand directory (typically `brands/` or `brand-profiles/`). If found, load and validate it against the BrandProfile schema. Merge with any new information from higher tiers.

#### Tier 4: URL Parse / Description Fallback (confidence target: 0.3)

Last resort: extract from URL structure (domain, TLD, paths), visible meta tags, or the raw description. This tier produces a skeleton profile with many inferred fields. Flag to the user that the profile needs manual review.

### Step 3: Construct the BrandProfile Object

The output must conform to this interface:

```typescript
interface BrandProfile {
  name: string;                    // Official brand name
  url?: string;                    // Primary URL if available
  industry: string;                // Industry or sector
  tone: string[];                  // 4-5 evocative tone attributes
  values: string[];                // 3-5 core brand values
  audience: string;                // Primary audience description
  colorPalette: string[];          // 3-6 hex color codes
  typography: string;              // Typography description
  personality: string;             // Brand personality summary
  positioning: string;             // Strategic positioning statement
  visualStyle?: string;            // Visual style description
  competitors?: string[];          // Key competitors
  confidence: number;              // 0-1 extraction confidence score
  tier: number;                    // Which tier produced the result
}
```

#### Writing Effective Tone Attributes

Tone attributes are the single most reused field in downstream skills. They must be evocative and specific — avoid generic descriptors that could apply to any brand.

**DO — use evocative, ownable attributes:**
- "quietly confident" (not "professional")
- "irreverent but warm" (not "friendly")
- "editorial precision" (not "clean")
- "restrained optimism" (not "positive")
- "intellectually playful" (not "smart")

**DON'T — use attributes that describe every brand:**
- ~~"professional"~~ — this is table stakes, not a tone
- ~~"innovative"~~ — every tech company claims this
- ~~"trustworthy"~~ — too generic to guide design decisions
- ~~"modern"~~ — relative to what era?

Think about the brand's reason for existing before writing tone attributes. What makes this brand's voice recognizable in a blind test? Those are your tone words.

#### Writing Effective Values

Values should feel owned by this brand, not borrowed from a corporate template.

**DO:** "Radical transparency", "Design as respect", "Accessible luxury"
**DON'T:** "Innovation", "Excellence", "Integrity" — these are corporate wallpaper.

#### Writing Effective Positioning

Positioning is a strategic insight, not a tagline. It should answer: "Why does this brand win against alternatives?"

**DO:** "Stripe wins by making complex financial infrastructure feel like a simple developer tool — the brand promises that payments can be as elegant as a well-documented API."
**DON'T:** "Stripe is a leading payment platform." — this is a Wikipedia summary, not positioning.

#### Writing Effective Visual Style

Use specific cultural and design references to anchor the visual style.

**DO:** "Swiss modernism meets California warmth — Helvetica precision but with generous whitespace and soft photography"
**DON'T:** "Clean and modern design" — meaningless without reference points.

### Step 4: Validate the Profile

Before returning the profile, run these validation checks:

1. **Tone array length**: Must have 4-5 attributes. Fewer is too vague; more dilutes the voice.
2. **Color palette length**: Must have 3-6 hex codes. Fewer limits design; more creates incoherence.
3. **No generic values**: Scan for "innovation", "excellence", "integrity", "quality" — replace with brand-specific alternatives.
4. **Positioning is not a tagline**: Must be 1-3 sentences of strategic analysis, not a slogan.
5. **Confidence score is honest**: Do not inflate. If you guessed at colors, confidence drops below 0.5.

### Step 5: Generate Supporting Brand Documentation (Optional)

If the user requests a full brand package, generate up to 9 supporting documents in a `brand-docs/` directory adjacent to the profile:

| File | Purpose | Key Content |
|------|---------|-------------|
| `identity.md` | Core brand identity | Mission, vision, values, positioning, brand story |
| `visual.md` | Visual identity system | Color palette, usage rules, spacing, imagery style |
| `voice.md` | Voice and tone guidelines | Writing principles, do/don't examples, tone spectrum |
| `accessibility.md` | Accessibility standards | WCAG targets, color contrast ratios, alt text rules |
| `iconography.md` | Icon system | Icon style, grid, stroke weight, metaphor rules |
| `photography.md` | Photography direction | Subject matter, lighting, color treatment, composition |
| `content.md` | Content strategy | Content pillars, editorial calendar themes, CTAs |
| `social.md` | Social media guidelines | Platform-specific voice, posting cadence, visual rules |
| `logo.md` | Logo usage | Clear space, minimum size, color variations, misuse examples |

Each file should be 500-1000 words of actionable guidelines, not generic brand theory. Reference the BrandProfile fields directly — tone attributes become voice guidelines, color palette becomes visual rules, positioning becomes content strategy.

### Step 6: Output the Result

Return the BrandProfile as a JSON object and summarize key findings for the user. If confidence is below 0.6, explicitly flag which fields are inferred and need human review.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| All tone attributes are generic | Skipped the "reason for existing" analysis | Spend more time on positioning first, then derive tone from positioning |
| Color palette looks wrong | Web search returned outdated brand colors | Check the live site's CSS custom properties or meta theme-color tag directly |
| Confidence is very low (< 0.3) | Brand is too new or too niche for any tier | Ask the user for brand guidelines PDF or existing assets to analyze |
| Profile feels interchangeable | Values and tone could apply to any competitor | Add the competitor list and explicitly differentiate: "Unlike X, this brand..." |
| Visual style is vague | No specific cultural references | Force yourself to complete: "This looks like [specific reference] meets [specific reference]" |

## Cross-References

- **brand-css-generator**: Consumes BrandProfile to generate CSS custom properties and design tokens
- **figma-token-sync**: Pushes brand color tokens to Figma variables
- **generative-page-pipeline**: Uses BrandProfile for page generation with brand-consistent styling
