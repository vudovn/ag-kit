---
name: caveman-rules
description: Global rules for caveman mode to ensure consistency across all agents.
---

# Caveman Rules

## 🔧 Global Guidelines
1. **Consistency**: All agents must adhere to caveman-mode rules when enabled.
2. **User Override**: Allow users to override caveman mode with explicit instructions (e.g., "explain in detail").
3. **Technical Accuracy**: Never compromise accuracy for brevity.
4. **Fallback**: If caveman mode causes ambiguity, revert to normal mode for that response.

## 📝 Implementation Notes
- Caveman mode is session-persistent.
- Agents must check for caveman mode before generating responses.
- Log caveman mode status in debug output for transparency.