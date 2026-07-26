# Evaluation — Scoring and Comparing Names

After filtering candidates through anti-patterns and principles, you need a structured way to compare finalists. Gut feeling matters, but it should be informed by criteria, not replace them.

---

## Pre-Scoring Gate

Before scoring any candidate on the rubric, run it through the Red Flags Checklist in [anti-patterns.md](anti-patterns.md). Any candidate with two or more "yes" answers is disqualified — do not score it. Only candidates that clear this gate proceed to numerical scoring.

This prevents wasting evaluation effort on names that are dead on arrival.

---

## Scoring Rubric

Rate each finalist on these criteria. Use a 1-5 scale where:
- **5** = Exceptional, best-in-class
- **4** = Strong, no concerns
- **3** = Adequate, some trade-offs
- **2** = Weak, notable problems
- **1** = Fails this criterion

### Core Criteria (Weight: High)

| Criterion | What to evaluate | Weight |
| ----------- | ----------------- | -------- |
| **Metaphor strength** | Does the name plant a concrete image? Does the metaphor connect to the product's function? | 3x |
| **Memorability** | After hearing it once, would someone remember it tomorrow? | 3x |
| **Story** | Can you tell a 15-second origin story? Does it produce a "that's clever" reaction? | 2x |
| **Distinctiveness** | Does it stand out from competitors? Would someone confuse it with another product? | 2x |

### Practical Criteria (Weight: Medium)

| Criterion | What to evaluate | Weight |
| ----------- | ----------------- | -------- |
| **Phone test** | Can someone spell it after hearing it? Can they say it after reading it? | 2x |
| **Length** | 1-2 syllables ideal, 3 acceptable, 4+ problematic. Character count under 7 ideal. | 1x |
| **Sound alignment** | Do the sounds match the product's character? (See phonosemantics.md) | 1x |
| **Availability** | Is it available on critical platforms? | 1x |

### Context Criteria (Weight: Situational)

| Criterion | What to evaluate | Weight |
| ----------- | ----------------- | -------- |
| **Brand fit** | If part of a family, does it feel like it belongs? | 1x |
| **Global friendliness** | Can speakers of other languages pronounce it? Any negative meanings in other languages? | 1x |
| **Longevity** | Will the name still work in 5-10 years? Does it reference anything that will date it? | 1x |
| **Searchability** | Can someone Google it and find you? Does the word have Wikipedia or major brand competition? See the searchability scoring guide in [availability.md](availability.md) | 2x |
| **Competitive density** | How many other organizations in the same or adjacent industries use this name? Names that passed the availability gate (no direct competitor) can still face varying degrees of competitive noise from adjacent-space usage (schools, foundations, agencies, consulting firms). Score: 5 = no other orgs in same/adjacent spaces; 4 = 1-2 uses in clearly different industries; 3 = a few uses in adjacent spaces; 2 = multiple orgs in the same broad category; 1 = crowded, word is established in the target industry by multiple entities. | 1x |

### Scoring Template

```text
NAME: _______________

CORE (high weight):
  Metaphor strength    [1-5] × 3 = ___
  Memorability         [1-5] × 3 = ___
  Story                [1-5] × 2 = ___
  Distinctiveness      [1-5] × 2 = ___

PRACTICAL (medium weight):
  Phone test           [1-5] × 2 = ___
  Length               [1-5] × 1 = ___
  Sound alignment      [1-5] × 1 = ___
  Availability         [1-5] × 1 = ___

CONTEXT (situational):
  Brand fit            [1-5] × 1 = ___
  Global friendliness  [1-5] × 1 = ___
  Longevity            [1-5] × 1 = ___
  Searchability        [1-5] × 2 = ___
  Competitive density  [1-5] × 1 = ___

TOTAL: ___ / 110
```

Maximum possible score: 110 (all 5s). In practice, anything above 75 is strong. Above 85 is exceptional.

---

## Contextual Sentence Tests

Names live in sentences, not in isolation. Test every finalist in these contexts:

### Introduction
> "Have you tried `___`?"
> "We just launched `___`."
> "I've been using `___` for a month."

Does the name sound natural in casual recommendation?

### Explanation
> "We built `___` to solve [problem]."
> "`___` is a [category] that [does what]."

Does the name sit comfortably next to its description, or does it feel disconnected?

### Daily Use
> "Check the `___` dashboard."
> "The `___` API is down."
> "`___` just sent an alert."
> "Let me push this to `___`."

Does the name work as a noun in technical conversation?

### Marketing
> "`___` — [tagline]"
> "Get started with `___` in 5 minutes."
> "Why teams switch to `___`."

Does the name work in headlines and calls to action?

### Word of Mouth
> "You should try this thing called `___`."
> "Our team switched to `___` last quarter."

This is the most important test. Would someone actually say this name in conversation to a colleague? If the name feels awkward spoken aloud, word-of-mouth growth is crippled.

---

## Side-by-Side Comparison

When comparing finalists, use this format:

```text
┌─────────────┬──────────┬──────────┬──────────┐
│ Criterion   │ Name A   │ Name B   │ Name C   │
├─────────────┼──────────┼──────────┼──────────┤
│ Metaphor    │ ████░ 4  │ █████ 5  │ ███░░ 3  │
│ Memorability│ █████ 5  │ ████░ 4  │ ████░ 4  │
│ Story       │ ████░ 4  │ █████ 5  │ ██░░░ 2  │
│ Distinct.   │ ████░ 4  │ ███░░ 3  │ █████ 5  │
│ Phone test  │ █████ 5  │ ████░ 4  │ ██░░░ 2  │
│ Length      │ █████ 5  │ ███░░ 3  │ ████░ 4  │
│ Sound       │ ████░ 4  │ ████░ 4  │ ███░░ 3  │
│ Available   │ ███░░ 3  │ ████░ 4  │ █████ 5  │
├─────────────┼──────────┼──────────┼──────────┤
│ TOTAL       │ 82       │ 79       │ 68       │
└─────────────┴──────────┴──────────┴──────────┘
```

Visualizing scores side-by-side makes trade-offs explicit. A name that scores highest overall might have a critical weakness (phone test = 2) that disqualifies it despite a high total.

---

## The 24-Hour Test

After scoring and comparing, sit with your top 2-3 names for at least 24 hours. First impressions are unreliable for names — what feels exciting at 2am in a brainstorm session may feel hollow the next morning.

During the 24 hours:
- **Say the name aloud** in different contexts throughout the day
- **Tell someone** the name and watch their face (not their words — their face)
- **Type the name** as if you were writing about the product
- **Imagine the name on a homepage**, in a tweet, in a conference talk title
- **Sleep on it** — literally. The name that feels most natural after sleeping on it is usually the right one

The name that feels increasingly right over 24 hours is stronger than the name that was most exciting in the moment.

---

## When Scores Are Close

If two or more names score within 5 points of each other, use these tiebreakers (in order):

1. **Which has the stronger metaphor?** Metaphor is the hardest thing to retrofit. You can work around availability, length, and even sound — but a weak metaphor can't be fixed.

2. **Which passes the phone test more cleanly?** A name that's perfectly metaphorical but unspellable will create daily friction forever.

3. **Which has the better origin story?** The story will be told thousands of times — in pitches, in blog posts, in conference talks, in casual conversations. The more satisfying the story, the more it gets retold.

4. **Which has better availability?** All else equal, the name with cleaner availability has lower activation energy.

5. **Which do YOU like more?** After all analysis is done, trust your instinct. You'll be living with this name for years.

---

## Decision Presentation Format

When presenting finalists to stakeholders or making a final decision, use this structure:

```text
FINALIST: [Name]

Origin: [15-second story — why it's called this]
Metaphor: [What concrete image it plants]
Sound: [How it feels spoken aloud, key phonetic features]
Score: [Total] / 100

Strengths:
- [Strongest quality]
- [Second strongest quality]

Risks:
- [Any concerns or trade-offs]

Availability:
- Domain: [status]
- GitHub: [status]
- [Other relevant platforms]: [status]

Sentence test: "Have you tried [Name]? It [does what]."
```

Present 3-5 finalists maximum. More than 5 causes decision paralysis. Fewer than 3 doesn't give enough comparison.

---

## Final Decision Checklist

Before committing to a name, confirm:

- [ ] The name has a clear, satisfying origin story
- [ ] It scored above 70 on the rubric
- [ ] It passes the phone test (say → spell → remember)
- [ ] It survived the 24-hour test
- [ ] It's available on the platforms that matter
- [ ] It doesn't match anti-patterns
- [ ] It doesn't have problematic meanings in major languages
- [ ] You can imagine saying it 1,000 times without cringing
- [ ] At least one other person (not involved in the naming) liked it on first hearing
