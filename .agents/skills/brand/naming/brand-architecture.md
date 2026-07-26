# Brand Architecture — Naming Within Families

When a product exists within a larger brand, naming isn't just about the individual product — it's about how names relate to each other. Brand architecture determines how much of the parent brand each product carries.

---

## Architecture Models

### 1. Monolithic (Branded House)

Every product carries the parent brand name.

**Pattern:** `[Parent] [Descriptor]`

| Parent | Products |
| -------- | ---------- |
| Apple | Apple Pay, Apple Watch, Apple Music, Apple TV |
| Google | Google Maps, Google Drive, Google Photos |
| Microsoft | Microsoft Teams, Microsoft Edge |

**When to use:**
- The parent brand is the primary asset
- Products share a common platform or ecosystem
- Brand trust transfers directly (the parent name IS the selling point)
- Maximum brand reinforcement is the goal

**Trade-offs:**
- Every product's reputation affects the parent
- Individual products can't develop distinct personalities
- The parent name becomes load-bearing — if it weakens, everything weakens

**Naming implications:** The descriptor word matters enormously because it's doing all the differentiation work. "Apple Watch" works because "Watch" is concrete. "Apple Experience Platform" would be meaningless.

### 2. Endorsed (Sub-brands)

Products have their own names but visibly connect to the parent.

**Pattern:** `[Product Name] by [Parent]` or `[Parent]'s [Product Name]`

| Parent | Products |
| -------- | ---------- |
| Marriott | Courtyard by Marriott, Residence Inn by Marriott |
| Amazon | Kindle by Amazon, Alexa by Amazon |
| Salesforce | Slack (by Salesforce), Tableau (by Salesforce) |

**When to use:**
- Products serve different audiences than the parent
- You want brand trust transfer but also distinct identity
- Products might be acquired (they already had their own name)

**Trade-offs:**
- More complex naming — two brands to manage
- The "by" connection can feel forced if the product and parent are culturally mismatched

**Naming implications:** The product name needs to stand alone. "Courtyard" works without "Marriott." "Slack" works without "Salesforce." The parent endorsement is a safety net, not a crutch.

### 3. Independent (House of Brands)

Products have completely independent names. The parent brand is invisible to consumers.

**Pattern:** Each product has its own name, no visible connection

| Parent | Products |
| -------- | ---------- |
| Atlassian | Jira, Confluence, Trello, Bitbucket |
| JetBrains | PyCharm, WebStorm, GoLand, IntelliJ |
| Procter & Gamble | Tide, Pampers, Gillette, Old Spice |

**When to use:**
- Products serve completely different audiences
- You want each product to own its category
- Product failure shouldn't contaminate siblings
- You're building a portfolio, not an ecosystem

**Trade-offs:**
- No brand transfer between products — each must build awareness from zero
- Higher marketing cost per product
- Risk of incoherence if there's no unifying logic

**Naming implications:** Each name must be fully self-sufficient. It needs its own metaphor, its own story, its own personality. This gives maximum creative freedom but maximum naming effort.

### 4. Hybrid

A mix of strategies across the portfolio.

| Parent | Monolithic | Independent |
| -------- | ----------- | ------------- |
| Google | Google Maps, Google Drive | YouTube, Waze, Fitbit |
| Amazon | Amazon Prime, Amazon Fresh | Kindle, Alexa, Twitch |
| Meta | Meta Quest | Instagram, WhatsApp, Threads |

**When to use:**
- Some products benefit from parent association, others don't
- Acquired products keep their existing brand equity
- Different product tiers serve different strategic goals

**Naming implications:** Each new product requires an explicit decision about which tier it belongs to. The decision should be based on audience overlap with the parent brand.

---

## Conventions Within Brand Families

When you're creating multiple products under one parent, establishing a naming convention creates coherence without being formulaic.

### Pattern-Based Conventions

**JetBrains model:** `[Tech hint] + [Evocative word]`
- PyCharm (Python + charm/enchantment)
- WebStorm (Web + storm/power)
- GoLand (Go + land/territory)
- Each name telegraphs its language while maintaining personality

**Consistent suffix:** All products share an ending
- Shopify, Spotify (not related, but the -ify pattern)
- HashiCorp: Terraform, Consul, Vault, Nomad (no suffix — each is an independent word, but they share a "Roman/ancient" territory)

**Consistent metaphor territory:** All names draw from the same conceptual world
- Cloudflare products: Workers, Pages, Warp, Tunnel, Stream — all infrastructure/engineering metaphors
- GitHub: Actions, Copilot, Codespaces, Pages — all developer workflow metaphors

### Namespace Conventions

For technical products (bots, APIs, CLI tools), the username/handle convention creates family connection:

```text
Product name    Handle/Username         Repo name
─────────────   ──────────────────────  ─────────────
Sentry          @sentry                 getsentry/sentry
Vault           @hashicorp              hashicorp/vault
Linear          @linear                 linearapp/linear
```

Common patterns:
- `@[name]_bot` — Telegram bots
- `[org]/[name]` — GitHub repositories
- `[name]-cli` — Command-line tools
- `get[name].com` — Domains when exact match is taken

---

## Sub-Brand vs. Feature Naming

Not everything deserves a name. Distinguish between:

### Deserves a Name (Sub-brand)
- It could exist independently
- It has its own audience or use case
- It's marketed separately
- Users might use it without using the parent product

### Deserves a Label (Feature)
- It only exists within the parent product
- It's part of a shared workflow
- Users discover it through the parent
- Naming it separately would confuse more than clarify

**Example:**
- GitHub **Copilot** — deserves a name. It's a distinct product with its own audience.
- GitHub **Pull Requests** — a label is fine. It's a core feature, not a separate product.
- GitHub **Actions** — borderline. It's deeply integrated but has its own identity and use case.

**The test:** Would someone say "I use [name]" without mentioning the parent? If yes, it deserves a name.

---

## Naming for Different Product Tiers

### Internal Tools
- Clarity over cleverness
- The audience is your team — they'll use the name daily, so avoid friction
- Descriptive compounds are fine (LogViewer, BuildRunner)
- Internal jokes can work if the team is small and stable

### Open Source Projects
- Must work globally (pronounceable across languages)
- The name IS the marketing — there's no ad campaign behind it
- Cultural references are powerful because the community enjoys discovering the connection
- Avoid names that are hard to search for (common words without distinctive context)

### Consumer Products
- Maximum memorability, minimum friction
- The name must work for people who don't care about the technology
- Warmth and approachability matter more than cleverness
- The phone test is critical — consumers discover products through word of mouth

### Enterprise Products
- Credibility and professionalism are primary
- The name should feel established, not trendy
- Avoid anything that would make a procurement officer hesitate
- Simple, clean, serious — but NOT boring corporate language

### Developer Tools
- Technical references are appreciated by the audience
- Cleverness is valued — developers enjoy discovering cultural connections
- Command-line friendliness matters (short, typeable, no special characters)
- The name will be typed thousands of times — every character counts

---

## Family Coherence Checklist

When naming a new product within an existing family:

- [ ] Does it feel like it belongs alongside the existing names?
- [ ] Is the architecture model clear (monolithic, endorsed, independent)?
- [ ] Does it follow the established convention without being formulaic?
- [ ] Could it be confused with an existing product in the family?
- [ ] Does it maintain the family's tone (serious, playful, technical)?
- [ ] Does the name work at the right level (sub-brand vs. feature)?
