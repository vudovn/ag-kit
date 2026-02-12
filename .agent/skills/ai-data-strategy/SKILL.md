---
name: ai-data-strategy
description: Strategic data management for AI, including RAG architectures, data readiness, vector databases, and governance.
allowed-tools: Read, Glob, Grep
---

# AI Data Strategy Skill

> "High-quality AI starts with high-quality data governance."

## 🎯 Selective Reading Rule

| File | Description | When to Read |
|------|-------------|--------------|
| `rag-readiness.md` | Data preparation for RAG systems | Designing LLM-based apps |
| `vector-architectures.md` | Selection and design of Vector DBs | Planning semantic search |
| `data-governance.md` | Privacy, LGPD/GDPR, and Lineage | Ensuring compliance for AI |

---

## 🏗 Core Principles

1.  **Garbage In, Garbage Out**: Data must be cleaned, deduplicated, and enriched before model ingestion.
2.  **Semantic Chunking**: Structure data based on meaning, not just character counts.
3.  **Privacy by Design**: Mask PII (Personally Identifiable Information) before embedding.
4.  **Traceability**: Maintain a clear lineage of how data reached the AI model.
