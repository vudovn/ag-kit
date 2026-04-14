---
name: caveman
description: Toggle caveman mode for terse, token-efficient responses.
---

# /caveman Command

## 📌 Usage
- `/caveman on`: Enable caveman mode.
- `/caveman off`: Disable caveman mode.
- `/caveman lite`: Enable lite caveman mode (moderate terseness).
- `/caveman full`: Enable full caveman mode (default).
- `/caveman ultra`: Enable ultra caveman mode (maximum compression).

## 🔄 Behavior
- Toggles caveman-mode skill globally.
- Affects all subsequent agent responses until disabled.
- Persists for the duration of the session.

## 📝 Example
```
User: /caveman on
AI: Caveman mode enabled. Responses now terse.

User: Explain React hooks.
AI: Hooks let functional components use state, lifecycle. useState, useEffect, useContext. No classes needed.
```