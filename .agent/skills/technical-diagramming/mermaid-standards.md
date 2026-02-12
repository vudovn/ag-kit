# Mermaid Diagramming Standards

Expert guidance for creating high-quality Mermaid diagrams in Antigravity Kit.

## 📋 General Syntax Rules
- Use `sequenceDiagram`, `graph TD` (Top Down), or `classDiagram`.
- For graphs, prefer `TD` or `LR` only.
- Ensure all nodes have IDs and labels: `A[Component Name]`.

## 🔄 Sequence Diagrams
- Define participants clearly: `participant A as Agent`.
- Use correct arrows: `->>` for synchronous calls, `-->>` for responses.
- Use `alt/else` for conditional logic.

## 🏗 Component Diagrams (Graph)
- Use subgraphs for boundaries: `subgraph "Context Name"`.
- Style nodes with `style A fill:#f9f,stroke:#333`. (Avoid purple/violet per specialist rules).

## 📄 Class Diagrams
- Include fields and methods: `ClassName : +field`.
- Define relationships clearly: `A <|-- B` (inheritance), `A *-- B` (composition).
