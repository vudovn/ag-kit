# Playbook Diagnosis — OpenShift Ansible

## Task Failure Investigation

1. Read the full task output — identify the failing module.
2. Check module return code, msg, and stderr.
3. Distinguish: module error vs target host error vs connection error.
4. Check if the task is conditional (`when:`) — condition may be wrong.
5. Check variable resolution — undefined vars cause template failures.

## Handler Issues

1. Handlers only run if notified by a changed task.
2. If task reports `ok` (no change), handler won't fire.
3. `force_handlers: yes` runs handlers even on failure — use cautiously.
4. Handler order depends on definition order, not notification order.

## Variable Precedence

```
Command line > Playbook vars > Role vars > Inventory vars > Defaults
```

Check for variable shadowing when unexpected values appear.

## Common Module Errors

| Module | Common Issue |
|--------|-------------|
| `yum`/`dnf` | Repository not available, proxy, subscription |
| `copy`/`template` | Permission denied, SELinux label |
| `service`/`systemd` | Service not found, dependency issue |
| `command`/`shell` | Exit code non-zero, missing binary |
| `k8s` | Kubeconfig missing, RBAC, API version |

## Evidence

- Job output log (full, not truncated).
- Playbook YAML.
- Inventory (redacted credentials).
- Variable files.
