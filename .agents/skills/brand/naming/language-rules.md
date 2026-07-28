# Language Rules — Working With Foreign Words in Naming

Foreign words are one of the most powerful naming tools. Kaizen, Algorithm, Ansible, Svelte — all came from non-English sources. But borrowing across languages is high-risk without guardrails. This file covers the mechanics of using foreign words in naming, regardless of the specific source language.

For language-specific phonosemantics, word formation, and cultural conventions, see the locale files in `languages/`.

---

## Pronunciation Accessibility

A foreign word only works as a name if your target audience can say it. Different source languages have different phoneme compatibility with English (and with each other).

### High compatibility (most phonemes map to English)

| Language | Why it works | Watch out for |
| ---------- | ------------- | --------------- |
| **Japanese** | CV syllable structure, no clusters, familiar vowels | Long vowels (ō vs o) lost in English; pitch accent ignored |
| **Italian** | Open syllables, vowel-final words, familiar consonants | Geminate consonants (ll, tt) often ignored by English speakers |
| **Spanish** | Similar vowel system, regular stress | Trilled r, ñ may be simplified |
| **Hawaiian** | Tiny phoneme inventory, all sounds exist in English | Glottal stop (ʻokina) consistently dropped |

### Medium compatibility (some unfamiliar sounds)

| Language | Usable with care | Common failure points |
| ---------- | ----------------- | ---------------------- |
| **French** | Nasal vowels, uvular r — recognizable but not natural | Silent letters create spelling confusion |
| **German** | Most consonants familiar, compounds readable | ch (/x/), ü, ö, umlauts dropped internationally |
| **Portuguese** | Mostly accessible, nasal vowels distinctive | ão, nh, lh are beautiful but unfamiliar |
| **Hindi/Sanskrit** | Retroflexes simplified to nearest English sound | Aspirated/unaspirated distinction lost entirely |

### Low compatibility (major barriers for English speakers)

| Language | Why it's hard | Workaround |
| ---------- | -------------- | ------------ |
| **Mandarin/Cantonese** | Tones don't survive transliteration | Use meaning-based translation, not phonetic borrowing |
| **Arabic** | Pharyngeals (ʿ, ḥ), emphatics have no English equivalent | Simplify transliteration; choose words without pharyngeals |
| **Polish/Czech** | Consonant clusters (szcz, přž) feel unpronounceable | Pick words with simpler clusters or modify spelling |
| **Georgian** | Ejectives, extreme clusters | Nearly unusable for international names without heavy modification |

**The rule:** If more than one phoneme in the word has no English equivalent, the word needs modification before it can work as an international name. One unfamiliar sound is distinctive. Two is friction. Three is a wall.

---

## Cross-Language Meaning Checks

Before committing to a foreign word, verify it doesn't carry unfortunate meanings in languages your audience speaks.

### The check process

1. **Primary language check** — Does the word mean what you think it means? Verify with a native speaker or authoritative dictionary, not just Google Translate.

2. **Major-language scan** — Check for problems in the top languages by speaker count that your audience might speak:
   - English, Spanish, Mandarin, Hindi, Arabic, Portuguese, French, German, Japanese, Russian
   - Prioritize languages spoken in your target markets

3. **Neighbor-language check** — Check languages closely related to your source language. They share vocabulary but meanings diverge:
   - Spanish ↔ Portuguese ↔ Italian
   - Czech ↔ Slovak ↔ Polish
   - Hindi ↔ Urdu ↔ Punjabi
   - Norwegian ↔ Swedish ↔ Danish

4. **Sound-alike check** — Does the word SOUND like something offensive in another language, even if spelled differently? Say it aloud with different accents.

### Famous failures

| Name | Source | Problem |
| ------ | -------- | --------- |
| **Nova** (Chevy) | Latin (new) | "No va" = "doesn't go" in Spanish. The car sold fine anyway, but the story persists as a cautionary tale |
| **Pinto** (Ford) | English (horse marking) | Slang for small penis in Brazilian Portuguese |
| **Mist Stick** (Clairol) | English | "Mist" = manure in German |
| **Siri** | Norse (beautiful woman who leads to victory) | Slang for buttocks in Japanese; "shiri" (尻) |
| **Lume** | Latin (light) | "Lume" is close to "lume" (candle/light) in Romanian — fine. But pronunciation varies |

**Note:** Some of these are disputed or exaggerated (the Nova story is largely urban legend — the car sold well in Latin America). The point isn't that every cross-language collision is fatal, but that checking is cheap and not checking is reckless.

---

## Diacritics and Special Characters

### When to keep diacritics

- **The name is for a single-language market** where the diacritics are standard keyboard characters
- **The diacritic IS the brand identity** — removing it would strip distinctiveness (e.g., the ñ in a Spanish brand)
- **The word changes meaning without the diacritic** — Vietnamese without tone marks is ambiguous; some Polish words change meaning without their marks

### When to drop diacritics

- **The name needs to work as a domain, handle, or package name** — most platforms strip diacritics. Register the ASCII version as primary.
- **The target audience doesn't have the characters on their keyboard** — typing friction kills daily use
- **The diacritic doesn't affect pronunciation for the target audience** — English speakers won't pronounce café differently from cafe

### The domain/handle rule

Always register the ASCII-stripped version of the name as the primary domain and handle. Use the diacriticked version as a redirect or display name:

```text
Primary: kuznia.com / @kuznia
Display: Kuźnia
```

### Special characters to avoid in names

- **ß** (German eszett) — renders as "ss" in many systems, no uppercase form until 2017 (ẞ), still inconsistently supported
- **ð, þ** (Icelandic) — no keyboard support outside Iceland, often rendered as "d" and "th"
- **ł** (Polish) — frequently rendered as "l", losing the /w/ pronunciation
- **ø** (Danish/Norwegian) — often confused with "o" or rendered as "oe"

---

## Transliteration

When borrowing from non-Latin scripts, you must choose a romanization. Multiple systems often exist, and the choice affects how the name looks and sounds.

### Guiding principles

1. **Pick the romanization that English speakers will pronounce closest to the original.** Academic accuracy matters less than audience pronunciation.
2. **Be consistent.** Don't mix romanization systems within a brand family.
3. **Check what's conventional.** If the word already has a well-known English romanization (e.g., "karate" not "karate-do" or "空手"), use it.

### Common decisions

| Language | Multiple systems | Recommendation for naming |
| ---------- | ----------------- | -------------------------- |
| **Japanese** | Hepburn vs Kunrei vs Nihon-shiki | Hepburn — it's what English speakers expect (sushi, karate, tsunami) |
| **Mandarin** | Pinyin vs Wade-Giles | Pinyin — it's the international standard. Wade-Giles is outdated except in historical contexts |
| **Korean** | Revised Romanization vs McCune-Reischauer | Revised Romanization — it's the South Korean government standard |
| **Arabic** | Multiple informal systems | No single standard. Prioritize readability: use "sh" not "š", "kh" not "x̌" |
| **Russian** | BGN/PCGN vs ISO 9 vs informal | BGN/PCGN for US audiences, informal for casual/brand contexts. Avoid ISO 9 (uses diacritics) |
| **Hindi** | IAST vs Hunterian vs informal | Informal for brand naming — IAST uses too many diacritics (ā, ī, ū). Use the spelling that looks most natural to English readers |

---

## Productive Language Families for Tech Naming

Some languages reliably produce usable names for international audiences. Others are rich naming sources for domestic markets but don't travel well.

### Best for international borrowing

| Language | Why | Examples |
| ---------- | ----- | --------- |
| **Japanese** | Short words, CV structure, familiar sounds, rich concept vocabulary | Kaizen, emoji, tsunami, origami, bokeh |
| **Latin** | Root of most English technical vocabulary, familiar morphemes | Nexus, vertex, apex, cipher, alias |
| **Sanskrit** | Root of many English words, prestigious associations | Avatar, guru, mantra, yoga, nirvana |
| **Italian** | Musical, vowel-final, globally associated with design quality | Svelte, tempo, studio, allegro |
| **Arabic** | Mathematical/scientific heritage, distinctive sound | Algorithm, algebra, zenith, nadir |
| **French** | Prestige associations, many words already in English | Rapport, cache, depot, renaissance |

### Best for domestic market naming

| Language | Why it works domestically | Why it doesn't travel |
| ---------- | -------------------------- | ---------------------- |
| **Polish** | Rich morphology, Slavic mythology, distinctive identity | Consonant clusters, diacritics, unfamiliar phonemes |
| **Finnish** | Unique sound, cultural pride, productive morphology | Double vowels/consonants confuse non-Finns |
| **Georgian** | World's most distinctive script, unique sounds | Ejectives and clusters are unpronounceable internationally |
| **Vietnamese** | Rich meaning, monosyllabic compounds | 6 tones and diacritics don't survive export |

### The hybrid approach

Many successful international products use a foreign word that's been **adapted** rather than directly borrowed:

- **Figma** — from "figure" (Latin/English), shortened and modified
- **Grafana** — from "graph" (Greek) + Romance-language suffix
- **Vercel** — blended from "versatile" + "accelerate" (Latin roots)
- **Svelte** — French word meaning "slender", no modification needed because it's already in English dictionaries

The pattern: start from a foreign root, then modify until it's pronounceable and spellable by your target audience while retaining a trace of the original meaning.

---

## The Exoticism Trap

A foreign word must do **work** in the name — it must add meaning, metaphor, or cultural depth that an English word couldn't provide. If the only reason to use a foreign word is that it sounds "cool" or "exotic," it's costume jewelry.

### The work test

Ask: **Why this language?** If the answer connects to the product, the reference works:

- "We used the Japanese word **kaizen** (continuous improvement) because our product is a continuous improvement tool" — **the word does work**
- "We used a Japanese word because Japanese sounds cool and technical" — **the word is decoration**

### Signs of the exoticism trap

- You chose the language before you chose the word (language tourism)
- You can't explain the connection between the word's meaning and your product
- The word is from a culture you have no connection to and your audience won't recognize the reference
- You're using a foreign word primarily to seem sophisticated or global
- The word means something generic in the source language ("power," "light," "flow") — you just moved the thesaurus to another language

### When borrowing is legitimate

- The source language has a concept with no English equivalent (Japanese *wabi-sabi*, Danish *hygge*, Portuguese *saudade*)
- The word's etymology maps to your product's function (Arabic *algorithm* from al-Khwarizmi)
- Your product targets speakers of that language
- The word is already partially naturalized in English (French *cache*, Japanese *emoji*, Hindi *avatar*)

---

## Quick Reference Checklist

Before using a foreign word as a product name:

- [ ] Can your target audience pronounce it after hearing it once?
- [ ] Can they spell it (or get close enough to search for it)?
- [ ] Does the word mean what you think it means? (Verified with a native speaker or authoritative source, not Google Translate)
- [ ] Have you checked for offensive meanings in major languages your audience speaks?
- [ ] Have you checked neighbor languages of the source language?
- [ ] Does the word do WORK (adds meaning/metaphor), or is it just exotic decoration?
- [ ] If it has diacritics, do you have an ASCII-safe version for domains and handles?
- [ ] Is the romanization/transliteration the one your audience will expect?
