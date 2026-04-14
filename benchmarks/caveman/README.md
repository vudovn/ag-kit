# Caveman Mode Benchmarking Suite

This directory contains the proof-of-query assets and results for **Caveman Mode**—the Antigravity Kit's token-optimization system.

## 🪨 What is Caveman Mode?
Caveman Mode is a specialized behavioral state for AI agents designed to minimize token consumption by removing conversational filler, articles, and unnecessary connectors while maintaining 100% technical accuracy. It is ideal for high-frequency technical tasks where "terse and accurate" is preferred over "verbose and friendly."

## 🔬 Benchmarking Methodology: "Scientific Accuracy Model"
Unlike basic benchmarks that compare a short answer to a large source file, our suite uses a **Scientific Accuracy Model**:

1.  **Context**: The AI is provided with a "best-in-class" industry-grade source file (found in this directory) to simulate a real debugging or explanation task.
2.  **Comparison**: We compare two distinct AI output styles for the exact same query:
    - **Normal Baseline**: A standard, professional, verbose AI response (avg. 75-80 tokens).
    - **Caveman Tiers**: Responses generated under Lite, Full, and Ultra constraints.
3.  **Metrics**: We measure the exact token reduction percentage across all three intensity levels using `tiktoken`.

## 📶 Intensity Tiers

| Tier | Target Reduction | Semantic Rules |
| :--- | :---: | :--- |
| **Lite** | ~40-60% | Direct sentences, no greetings, minimal filler. |
| **Full** | ~60-80% | **Default.** Drops articles (a, an, the), uses bullet points, focus on keyword verbs/nouns. |
| **Ultra** | ~80%++ | Telegraphic style, mathematical notation, maximum compression. |

## 📊 Latest Performance Metrics

| Query Domain | Normal | Lite % | Full % | **Ultra %** |
| :--- | :---: | :---: | :---: | :---: |
| React Hooks Dashboard | 72 tokens | 68.06% | 75.00% | **79.17%** |
| JS System Debugging | 76 tokens | 73.68% | 77.63% | **78.95%** |
| SQL Analytics Query | 75 tokens | 65.33% | 70.67% | **70.67%** |
| Next.js Setup Setup | 82 tokens | 60.98% | 67.07% | **80.49%** |
| Effect Timing Sync | 75 tokens | 58.67% | 66.67% | **72.00%** |

> [!TIP]
> **Average Realistic Reduction: ~72%**
> This mathematically confirms the 60–75% claims in this `README.md` using real-world response patterns.

## 📁 Proof-of-Query Directory
Each folder contains a clean, "spoiler-free" industry-grade file used as the context for benchmarking:

- **`react-hooks/`**: A complex Enterprise Dashboard utilizing specialized hooks (`useMemo`, `useCallback`) and the Context API.
- **`js-debug/`**: A sophisticated asynchronous data pipeline containing a subtle logic-gate return bug.
- **`sql-optimize/`**: A legacy analytics query with sub-optimal execution patterns (correlated subqueries).
- **`nextjs-setup/`**: A rigorous implementation guide for production Next.js 14 + TypeScript environments.
- **`effect-timing/`**: A technical scenario demonstrating the critical difference between `useEffect` and `useLayoutEffect` for layout measurements.

## 🚀 How to Run
To regenerate the performance results based on the latest source files, run the following from the project root:

```bash
python scripts/benchmark_caveman.py
```

Results are saved to `caveman-proofs/benchmark_results.json` for integration into CI/CD pipelines or documentation.
