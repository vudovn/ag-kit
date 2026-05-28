---
name: verify-changes
description: Prove code works by running it, not just checking it exists. Verification through execution rather than inspection. Use after writing or modifying code to ensure it actually functions correctly.
when_to_use: "After writing code, completing a feature, or fixing a bug. When the user says 'does this work?', 'test this', 'verify', or when /verify workflow is invoked. NOT for writing new code — for proving existing code works."
allowed-tools: Read, Bash, Grep, Glob
effort: medium
---

# Verify Changes — Prove Code Works

> "Code that exists" ≠ "Code that works." This skill ensures changes are verified through execution.

## Core Principle

```
❌ Verification by inspection:  "I can see the function exists, it should work"
❌ Verification by assumption:  "The types check out, so it's correct"
✅ Verification by execution:   "I ran it, here's the output, it works because [evidence]"
```

---

## Verification Protocol

### Step 1: Identify What Changed
```
- Which files were modified?
- What behavior should be different now?
- What was the original bug/requirement?
```

### Step 2: Determine Verification Method

| Change Type | Verification Method |
|---|---|
| **Bug fix** | Reproduce the original bug scenario → confirm it no longer occurs |
| **New feature** | Run the feature → confirm expected output |
| **Refactor** | Run existing tests → confirm nothing broke |
| **API change** | Call the endpoint → confirm response shape |
| **UI change** | Render the component → confirm visual output |
| **Config change** | Load the config → confirm values applied |
| **Build/infra** | Run build command → confirm success |

### Step 3: Execute Verification

```bash
# For Node.js projects
npm run build          # Does it compile?
npm run test           # Do tests pass?
npm run dev            # Does it start?

# For specific files
node -e "require('./path/to/module'); console.log('✅ Loads correctly')"

# For API endpoints
curl http://localhost:3000/api/endpoint

# For scripts
python script.py --test
```

### Step 4: Report Evidence

```markdown
## Verification Report

### What was changed
- [File list and summary]

### How it was verified
- [Exact commands run]

### Evidence
- Build: ✅ Compiled without errors
- Tests: ✅ 42/42 passing
- Runtime: ✅ Server starts, endpoint returns expected JSON
- Edge case: ✅ Empty input handled correctly

### Not yet verified
- [Anything that couldn't be tested automatically]
```

---

## Verification Checklist by Project Type

### Web Application
- [ ] `npm run build` — compiles without errors
- [ ] `npm run lint` — no linting errors
- [ ] `npm run test` — all tests pass
- [ ] Dev server starts successfully
- [ ] Changed pages render correctly
- [ ] No console errors in browser

### API / Backend
- [ ] Server starts without errors
- [ ] Changed endpoints respond correctly
- [ ] Error cases return appropriate status codes
- [ ] Database queries execute successfully

### CLI / Script
- [ ] Script runs without errors
- [ ] Expected output matches actual output
- [ ] Error handling works (bad input test)
- [ ] Help/usage text is correct

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| "It should work" | No evidence | Run it and show output |
| Only checking happy path | Bugs hide in edge cases | Test error paths too |
| Verifying only compilation | Compiles ≠ correct | Test runtime behavior |
| Skipping verification for "trivial" changes | Trivial changes cause real bugs | Verify everything |

---

## Integration with Other Skills

| After Using | Verify With |
|---|---|
| `frontend-design` → UI changes | Render in browser, check console |
| `backend-specialist` → API changes | curl endpoints, check responses |
| `database-design` → Schema changes | Run migrations, query data |
| `testing-patterns` → New tests | Run test suite, check coverage |
