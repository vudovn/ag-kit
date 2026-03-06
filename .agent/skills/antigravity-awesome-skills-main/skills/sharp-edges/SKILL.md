---
name: sharp-edges
description: "Identify error-prone APIs and dangerous configurations"
risk: safe
source: "https://github.com/trailofbits/skills/tree/main/plugins/sharp-edges"
date_added: "2026-02-27"
---

# Sharp Edges

## Overview

Identify error-prone APIs and dangerous configurations that could lead to bugs, security vulnerabilities, or system failures.

## When to Use This Skill

Use this skill when you need to identify error-prone APIs and dangerous configurations.

Use this skill when:
- Reviewing code for potentially dangerous API usage
- Identifying configurations that could cause issues
- Analyzing code for error-prone patterns
- Assessing risk in API design or configuration choices
- Performing security audits focused on API misuse

## Instructions

This skill helps identify problematic APIs and configurations:

1. **API Analysis**: Review API usage for error-prone patterns
2. **Configuration Review**: Identify dangerous or risky configurations
3. **Pattern Recognition**: Spot common mistakes and pitfalls
4. **Risk Assessment**: Evaluate the potential impact of identified issues

## Common Sharp Edges

### Error-Prone APIs

- APIs with complex parameter requirements
- APIs with non-obvious failure modes
- APIs that require careful resource management
- APIs with timing or concurrency issues
- APIs with unclear error handling

### Dangerous Configurations

- Default settings that are insecure
- Configurations that bypass security controls
- Settings that enable dangerous features
- Options that reduce system reliability
- Parameters that affect performance negatively

## Detection Strategies

1. **Code Review**: Look for known problematic patterns
2. **Static Analysis**: Use tools to identify risky API usage
3. **Configuration Audits**: Review configuration files for dangerous settings
4. **Documentation Review**: Check for warnings about API usage
5. **Experience-Based**: Leverage knowledge of common pitfalls

## Best Practices

- Document identified sharp edges
- Provide clear guidance on safe usage
- Create examples of correct vs incorrect usage
- Recommend safer alternatives when available
- Update documentation with findings

## Resources

For more information, see the [source repository](https://github.com/trailofbits/skills/tree/main/plugins/sharp-edges).
