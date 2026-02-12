---
description: Create technical diagrams and architectural visualizations using Mermaid or PlantUML. Guided process for software-architect.
---

# /diagram - Technical Drawing Workflow

$ARGUMENTS

---

## 🛑 CRITICAL RULES

1. **Agent Selection**: Use `software-architect` with the `technical-diagramming` skill.
2. **Text-First**: Always generate diagrams in Mermaid (markdown-compatible) unless PlantUML is specifically requested.
3. **Context**: Provide clear labels, a title, and a legend for every diagram.
4. **Validation**: Before finishing, verify that the diagram accurately reflects the logic described in the code/requirements.

---

## Workflow Steps

### Step 1: Requirements Discovery
The `software-architect` will ask:
*   What is the goal of this diagram? (e.g., Sequence of Auth, Component Overview)
*   What is the required level of abstraction? (C4 Level 1, 2, or 3)

### Step 2: Draft Generation
Generate the diagram code block.
*   **Mermaid**: Use ` ```mermaid ` blocks.
*   **PlantUML**: Use ` ```plantuml ` (if supported by the environment).

### Step 3: Refinement
*   Add metadata enrichment (labels, notes).
*   Ensure the flow is logical (Top-to-Bottom or Left-to-Right).

---

## Expected Deliverables

| Artifact | Format |
|----------|--------|
| **Architecture Diagram** | Mermaid/PlantUML Code Block |
| **Brief Explanation** | Text summarizing the key flow/components |
| **Logic Verification** | 1-line statement confirming alignment with requirements |

---

## Usage Examples

```
/diagram create a sequence diagram for the JWT refresh token flow
/diagram design a class diagram for the Order management domain
/diagram show the interaction between the Frontend, API, and Redis cache
```
