# Availability — Checking and Securing Names

A great name that's unavailable is just a word. Availability checking should happen after filtering (not before — don't let availability dictate creative direction), but before emotional investment.

---

## Checking Workflow

Check in this order. Stop investing time in a name if it fails an early step.

### 1. Quick Disqualification (30 seconds)

Before any platform-specific checks:

- **Search "[name] + your industry/category"** — Are there direct competitors with this name?
- **Search just "[name]"** — Is it a major existing brand in ANY industry?
- **Check Wikipedia** — Does the word have problematic associations you missed?

If there's a direct competitor with the same name in the same space, the name is dead. Move on.

- **AI-namespace land-grab gate** (2024+): also search `"[name]" AI` and the exact name on GitHub by stars (`api.github.com/search/repositories?q=[name]+in:name&sort=stars`). Nearly every short, evocable word in the memory / knowledge / trust / agent space has already been taken by an AI startup or a high-star AI repo (Signet-AI, vellum-ai, Onyx, Tome, Engram…). A free npm/GitHub *handle* does NOT mean the name is clear — check what *exists*, not just whether the slug is free.

If there's a large brand in a different industry (e.g., "Apex" is a hundred things), you CAN still use the name — but you'll be fighting for search visibility forever. Weigh whether that fight is worth it.

### 2. Domain Availability

**Priority order:**
1. `[name].com` — Still the gold standard for credibility, especially with non-technical audiences
2. `[name].dev` — Excellent for developer tools. Google-managed, requires HTTPS
3. `[name].io` — Established in tech, but long-term future uncertain (Chagos Islands sovereignty transfer)
4. `[name].app` — Google-managed, requires HTTPS. Good for consumer apps
5. `[name].co` — Short, professional, no stigma
6. `[name].sh` — Popular for CLI tools and developer products
7. `[name].so` — Uncommon but clean

**If exact .com is taken (it probably is):**

*Prefix variants (generic — work for any product):*
- `get[name].com` — Established pattern (getbootstrap.com)
- `use[name].com` — Common for SaaS tools
- `try[name].com` — For products with free tiers
- `[name]hq.com` — Professional alternative
- `[name]app.com` — For mobile/web apps

*Suffix variants (audience-specific — reinforce positioning):*

When the product targets a specific audience, suffix patterns that include the audience descriptor are often more natural and more available than generic prefixes. The domain itself communicates who the product is for.

- `[name]dev.com` / `[name]devs.com` — Developer tools
- `[name]team.com` / `[name]teams.com` — Team/collaboration products
- `[name]guide.com` — Educational/content products
- `[name]studio.com` — Creative tools
- `[name]shop.com` — E-commerce/retail
- `[name]dad.com` / `[name]mom.com` — Parenting products
- `[name]fit.com` — Health/fitness products
- `[name]for[audience].com` — General pattern (e.g., `groveforteachers.com`)

**Domain landscape reality:**
- 350M+ domain registrations globally. Good single-word .com is essentially impossible without purchasing
- For developer tools and SaaS: .dev, .io, and .sh carry zero stigma
- For consumer products: .com still matters for trust, but .co and .app are gaining acceptance
- Avoid novelty TLDs (.xyz, .ninja, .guru, .io.cool) for serious products — they signal impermanence
- Don't negotiate with domain squatters unless you're prepared to pay $5k-$50k+

**Meaningful-TLD domain-hack (the category-brand move):** instead of fighting for a squatted `.com`, let the TLD *carry meaning* so the brand + URL are one string. Two patterns that read as intentional, not novelty:
- **The TLD signals the medium/category:** `obsidian.md` (markdown), `npmjs.com`→tools. A markdown/docs product on `.md` reads on-brand AND `.md` is far less squatted than `.com`/`.ai`.
- **The TLD completes a phrase:** `here.now` = "here now", the name spans SLD+TLD into a meaningful phrase. Pairs well with the product's value prop.
This sidesteps the squatter war AND can solve verbability/recall in one move. Register the namespace handle as the dotless spelling (`heredotnow`) for npm/GitHub where dots are illegal. **Reality check (learned 2026-06-19):** for ANY short evocable word, exact `.com` AND `.ai` are both gone — don't hard-gate creative direction on a free exact domain; pick the name, then solve the domain via meaningful-TLD / variant / purchase.

**Shortcut for common dictionary words:**

If your candidate is a common English dictionary word (e.g., "vault", "flint", "ward"), skip exact `.com`/`.dev`/`.io` checks — they are taken. Go directly to:

1. **Prefix variants:** `get[name].com`, `use[name].com`, `try[name].com`, `[name]hq.com`, `[name]app.com`
2. **Suffix variants (if targeting a specific audience):** `[name]dev.com`, `[name]team.com`, `[name]guide.com`, etc.
3. **Alternative TLDs:** `[name].site`, `[name].sh` (CLI tools), `[name].co`
4. **Compound domains:** `[name]check.com`, `[name]kit.com`, `[name]site.com`

The same applies to npm packages and GitHub org names — common English words are all taken. Use scoped packages (`@org/name`) and your own GitHub org (`yourorg/name`) instead.

Focus availability effort on platform-specific checks where the exact name may actually be free (plugin directory slugs, lesser-used package registries, social handles with bot suffixes).

### 3. Code Platform Availability

**GitHub:**
- Check organization name: `github.com/[name]`
- Check repository: `github.com/[yourorg]/[name]`
- For open source, the org name matters more than the repo name

**Package registries:**
- **npm:** `npm view [name]` or check npmjs.com/package/[name]
- **PyPI:** pypi.org/project/[name]
- **crates.io:** crates.io/crates/[name]
- **Go modules:** pkg.go.dev/[name]
- **RubyGems:** rubygems.org/gems/[name]

For package names, prefixing is acceptable (`@org/name`, `org-name`) and often required anyway.

### 4. Social Media Handles

**Priority depends on your audience:**

| Platform | Priority for | Check |
| ---------- | ------------- | ------- |
| X/Twitter | Most products | x.com/[name] |
| GitHub | Developer tools | github.com/[name] |
| LinkedIn | Enterprise/B2B | linkedin.com/company/[name] |
| Instagram | Consumer/creative | instagram.com/[name] |
| YouTube | Content-heavy products | youtube.com/@[name] |
| Reddit | Community-driven products | reddit.com/r/[name] |
| Telegram | Bot/channel products | @[name] on Telegram |
| Discord | Community products | Check if [name] servers exist |

**Handle strategies when exact match is taken:**
- `@get[name]` or `@use[name]`
- `@[name]hq` or `@[name]app`
- `@[name]_official` (last resort — looks defensive)

### 5. Trademark Search

For serious products, do a basic trademark search. You don't need a lawyer for initial screening.

**Resources:**
- **USPTO TESS** (US trademarks): tmsearch.uspto.gov
- **EUIPO TMview** (EU trademarks): tmdn.org/tmview
- **WIPO Global Brand Database** (international): branddb.wipo.int
- **Google Patents / Trademarks:** Quick supplementary search

**What to look for:**
- Exact matches in your product category (Nice Classification)
- Phonetically identical names with different spellings
- Names that would be confusingly similar to consumers

**Reality check:** For small projects, indie products, and open source, a basic search is sufficient. For products you plan to scale commercially, consult a trademark attorney before investing heavily in brand assets.

---

### WordPress Naming Restrictions

The WordPress Foundation enforces trademark rules that affect plugin and theme naming:

- **"WordPress" cannot be used** in commercial product names (plugin, theme, SaaS)
- **"WP" is allowed** but discouraged — signals commodity, not premium
- **"for WordPress" is acceptable** as a descriptor, not a name component
- **Check:** [WordPress Trademark Policy](https://wordpressfoundation.org/trademark-policy/)

---

## Availability Decision Framework

Not every platform needs to be available. Prioritize based on your product type:

| Product Type | Must have | Nice to have | Don't worry about |
| --- | --- | --- | --- |
| **SaaS product** | Domain, GitHub | X/Twitter, LinkedIn | Instagram, TikTok |
| **Developer tool** | GitHub org/repo, package registry | Domain, X/Twitter | Instagram, LinkedIn |
| **Consumer app** | Domain, app store name | Instagram, X/Twitter | GitHub, npm |
| **Open source** | GitHub org, package name | Domain | Social handles |
| **Telegram bot** | Telegram @handle | GitHub repo | Domain, social |
| **Content brand** | Social handles | Domain | Package registries |

---

## When to Compromise vs. When to Pivot

### Compromise (the name is worth fighting for):
- Exact .com is taken but a good prefix variant is available (get[name].com)
- One social handle is taken but all others are available
- Package name is taken but you can use an org prefix (@org/name)
- The name has strong metaphor, story, and sound

### Pivot (find a different name):
- A direct competitor has the name
- Multiple critical platforms are unavailable
- The domain squatter wants $50k+ and you're bootstrapped
- Trademark conflict in your product category
- The name is available everywhere but only because nobody wants it (red flag)

---

## Availability-Proof Naming Strategies

Some naming approaches are inherently more likely to have availability:

**Higher availability:**
- Compound words (two real words combined in an original way)
- Modified real words (truncated, blended, or suffixed)
- Cross-language borrowing (words from less-pillaged languages)
- Cultural references (specific, not obvious ones)

**Lower availability:**
- Single common English words (almost all taken as .com)
- Tech buzzwords (cloud, smart, data, AI — all combinations exhausted)
- Trending cultural references (whatever's popular right now)

**The paradox:** The more creative and specific your naming process, the more likely your name is to be available — because genuinely original combinations don't exist yet. This is another reason to invest in metaphor exploration rather than word generation.

---

## SEO and Searchability

A name that's available on every platform but impossible to find on Google is still broken. Searchability is a practical, post-launch concern that compounds over time.

### The Google Test

Before committing to a name, search it:

1. **"[name]"** — What dominates the first page? If Wikipedia, a major brand, or a well-known concept owns it, you'll fight for visibility indefinitely
2. **"[name] [your category]"** — How many pages deep before a new entrant could realistically appear?
3. **"[name] app"** or **"[name] tool"** — Does adding a generic qualifier help? If the name only works with a qualifier, the name is weak

### Wikipedia Collision

If the word has a Wikipedia article, you'll struggle for the Google knowledge panel. Wikipedia articles rank for single-word searches almost permanently.

**High collision risk:**

- Dictionary words with Wikipedia entries (Apex, Forge, Atlas, Pulse, Orbit)
- Historical figures, places, or concepts
- Scientific terms

**Lower collision risk:**

- Compound words with unique combinations (Mailchimp, Datadog, PagerDuty)
- Modified or invented words (Figma, Vercel, Grafana)
- Words from less-common languages

### Disambiguation Cost

How much qualifier does someone need to add to find your product?

| Disambiguation level | Example | Search cost |
| -------------------- | ------- | ----------- |
| **None needed** | "Figma" finds the product immediately | Ideal |
| **Category qualifier** | "Linear app" or "Linear issue tracker" | Acceptable |
| **Multiple qualifiers** | "Bear notes app iOS" | Expensive -- too many words needed |
| **Impossible** | Generic word in a crowded category | Dead on arrival |

The goal: own your name as a branded search term within 6-12 months. Shorter, more unique names achieve this faster.

### Domain-Search Alignment

Your domain affects search visibility:

- **Exact match .com** helps search ranking (declining factor, but still real)
- **Common TLDs** (.com, .dev, .io) are treated normally by search engines
- **Obscure TLDs** (.xyz, .ninja, .guru) carry no SEO penalty but signal impermanence to users
- **Prefix domains** (get[name].com, use[name].com) work fine for search -- Google treats the brand portion as the entity

### Searchability Scoring Guide

When scoring searchability in the evaluation rubric:

- **5** -- Name is unique or near-unique. First-page results within weeks of launch. No Wikipedia collision
- **4** -- Name has some competition but "[name] [category]" finds you immediately. Manageable disambiguation
- **3** -- Name competes with other entities but in clearly different industries. Needs consistent qualifier
- **2** -- Name competes with well-known brands or concepts. Multiple qualifiers needed. Knowledge panel blocked
- **1** -- Name is a common word dominated by Wikipedia, major brands, or saturated categories. Unsearchable without extensive qualifier chains

---

## Quick Availability Check Script

For technical users, automate the tedious parts:

```bash
NAME="yourname"

# Domain check (requires 'whois' or API)
whois ${NAME}.com | grep -i "no match\|not found"
whois ${NAME}.dev | grep -i "no match\|not found"
whois ${NAME}.io | grep -i "no match\|not found"

# GitHub org check
curl -s -o /dev/null -w "%{http_code}" https://github.com/${NAME}
# 404 = available, 200 = taken

# npm check
npm view ${NAME} 2>&1 | grep -i "not found"
# "not found" = available
```

Note: Automate for speed but always verify manually before committing. Automated checks can give false positives.
