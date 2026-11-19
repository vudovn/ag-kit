# Idempotency — OpenShift Ansible

## What Is Idempotency

A task is idempotent if running it multiple times produces the same result.
A playbook is healthy when second run reports all tasks as `ok` (no `changed`).

## Detecting Violations

1. Run playbook twice.
2. Second run should report 0 changed tasks.
3. If tasks report `changed` on second run → idempotency violation.

## Common Violations

| Pattern | Fix |
|---------|-----|
| `command:` / `shell:` always reports changed | Add `creates:` / `removes:` or use `changed_when:` |
| `template:` reports changed due to timestamps | Remove dynamic content like timestamps from templates |
| `lineinfile:` with regex matching multiple lines | Make regex more specific |
| `yum:` / `dnf:` with `latest` always changes | Pin versions for production |
| `service:` restarts on every run | Use `handler` with `notify`, not inline restart |

## Check Mode

- `ansible-playbook --check --diff` — shows what WOULD change without changing.
- Not all modules support check mode — verify module documentation.
- Always recommend check mode before live execution.

## Importance for Production

- Non-idempotent playbooks are dangerous in automation loops.
- Ansible Automation Controller retries may cause duplicate changes.
- Always verify idempotency before promoting a playbook to production.
