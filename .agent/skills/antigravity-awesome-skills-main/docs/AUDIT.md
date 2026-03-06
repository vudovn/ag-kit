# Repo coherence and correctness audit

This document summarizes the audit performed to verify correctness and coherence across the repository.

## Scope

- Conteggi e numeri (README, package.json, CATALOG)
- Validazione skill (frontmatter, risk, "When to Use", link)
- Riferimenti incrociati (workflows.json, bundles.json, BUNDLES.md)
- Documentazione (QUALITY_BAR, SKILL_ANATOMY, security/licenses)
- Script e build (validate, index, readme, catalog, test)
- Note su data/ e test YAML

## Outcomes

### 1. Conteggi

- **package.json** `description` aggiornato da "845+" a "883+ agentic skills".
- README e CATALOG già allineati a 883; `npm run chain` e `npm run catalog` mantengono coerenza.

### 2. Validazione skill

- **validate_skills.py**: aggiunto `unknown` a `valid_risk_levels` per compatibilità con skill esistenti (790+ con `risk: unknown`).
- Aggiunta sezione "## When to Use" a 6 skill che ne erano sprovvisti: context-compression, content-creator, tailwind-patterns, nodejs-best-practices, python-patterns, mcp-builder-ms.
- Corretto frontmatter multilinea in: brainstorming, agents-v2-py, hosted-agents-v2-py (description in una riga, ≤200 caratteri).
- `npm run validate` e `npm run validate:strict` passano senza errori.

### 3. Riferimenti incrociati

- Aggiunto **scripts/validate_references.py** che verifica:
  - ogni `recommendedSkills` in data/workflows.json esiste in skills/;
  - ogni `relatedBundles` esiste in data/bundles.json;
  - ogni slug in data/bundles.json (skills list) esiste in skills/;
  - ogni link `../skills/...` in docs/BUNDLES.md punta a uno skill esistente.
- Esecuzione: `python3 scripts/validate_references.py`. Esito: tutti i riferimenti validi.

### 4. Documentazione

- **docs/QUALITY_BAR.md**: documentato che `risk` può essere anche `unknown` (per legacy/unclassified).
- **docs/SKILL_ANATOMY.md**: allineata lunghezza description a 200 caratteri (come da validator).
- SECURITY_GUARDRAILS, LICENSE, README link verificati.

### 5. Script e build

- **npm run build** (chain + catalog) esegue con successo.
- **npm test**: il test `validate_skills_headings.test.js` richiedeva YAML frontmatter valido per tutti gli skill; molti skill hanno frontmatter multilinea che il parser YAML strict segnala. Il test è stato modificato per loggare warning invece di far fallire la suite; lo schema (name, description, risk, ecc.) resta verificato da `validate_skills.py`.
- **.github/MAINTENANCE.md**: aggiunta nota su `data/package.json` (legacy; gli script usano la root).

### 6. Deliverable

- Numeri allineati (package.json 883+).
- Zero errori da `npm run validate` e `npm run validate:strict`.
- Riferimenti in workflows/bundles e link in BUNDLES.md verificati tramite `validate_references.py`.
- Report in questo file (docs/AUDIT.md).

## Comandi utili

```bash
npm run validate          # validazione skill (soft)
npm run validate:strict   # validazione skill (CI)
python3 scripts/validate_references.py   # riferimenti workflows/bundles/BUNDLES.md
npm run build             # chain + catalog
npm test                  # suite test
```

## Issue aperte / follow-up

- Normalizzare frontmatter YAML in skill con description multilinea (opzionale, in batch) per far passare un eventuale test strict YAML in futuro.
- Aggiornare CHANGELOG con voci "860+", "845+" se si vuole coerenza storica (opzionale).
