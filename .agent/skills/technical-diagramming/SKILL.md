---
name: technical-diagramming
description: Specialized skill for creating technical drawings and architectural visualizations. Includes patterns for Mermaid, PlantUML, UML, and visual design tools.
allowed-tools: Read, Write, Edit
---

# Technical Diagramming Skill

> "A picture is worth a thousand lines of code, but only if it's drawn correctly."

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the diagram type you need!**

| File | Description | When to Read |
|------|-------------|--------------|
| `mermaid-standards.md` | Sequence, Class, Flowchart syntax for Mermaid | Creating quick in-line documentation |
| `uml-foundations.md` | Core UML principles and PlantUML reference | Designing deep system interactions |
| `visual-design.md` | Best practices for Draw.io, Excalidraw, and Layouts | Preparing high-level stakeholder presentations |

---

## 🏗 Core Principles

1.  **Text-to-Diagram First**: Prioritize tools that can be version-controlled (Mermaid/PlantUML).
2.  **Clarity over Complexity**: Avoid "spiderweb" diagrams. Use abstractions and C4 nesting.
3.  **Consistency**: Use standard notation (UML) to ensure universal understanding.
4.  **Actionable**: Every diagram must solve a specific question (e.g., "How does this auth flow work?").

---

## 📝 Quality Checklist

- [ ] Diagram has a clear Title and Legend.
- [ ] Flow moves from Top-to-Bottom or Left-to-Right logically.
- [ ] Components are clearly labeled with their Role/Technology.
- [ ] Arrows indicate data flow or dependency direction.
- [ ] Level of abstraction matches the intended audience.
