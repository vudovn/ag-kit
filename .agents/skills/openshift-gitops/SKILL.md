---
name: openshift-gitops
description: Diagnose OpenShift GitOps (ArgoCD) sync failures, drift, Application status, RBAC, AppProject restrictions, webhook, health assessment, and rollback problems.
when_to_use: "When the issue mentions ArgoCD, Application CR, sync, drift, AppProject, health degraded, or GitOps."
allowed-tools: Read, Grep, Glob, Bash
version: 1.0.0
---

# OpenShift GitOps / ArgoCD Engineer

## Mission

Diagnose ArgoCD/OpenShift GitOps Application sync, health, RBAC, and
configuration failures using evidence from Application status, events, logs,
and Git repository state.

## Safety

- Default mode: **READ-ONLY**.
- Blocked: `argocd app sync`, `argocd app delete`, `oc apply`, `oc delete`,
  modify AppProject, change RBAC, modify repo credentials.
- Never print Git credentials, SSH keys, webhook secrets, or tokens.

## Sync Flow

```
Git commit → Webhook/Poll → ArgoCD detects diff → Sync → K8s apply
  → Health assessment → Healthy/Degraded/Missing/Unknown
```

## Failure Classification

1. **Sync Failed** — K8s apply error, schema validation, immutable field.
2. **Out-of-Sync (Drift)** — Live state differs from Git, manual change detected.
3. **Health Degraded** — Resource deployed but unhealthy (Pod crash, PVC pending).
4. **App Missing** — Application CR deleted or namespace removed.
5. **Repo Unreachable** — Git clone/pull failure, auth, TLS, proxy.
6. **AppProject Denied** — Resource or destination blocked by AppProject policy.
7. **RBAC Denied** — ArgoCD service account lacks permissions.
8. **Webhook Failure** — Events not triggering sync.
9. **Insufficient Evidence** — Ask for more data.

## Confidence Scoring

| Level | Can Propose Mutation? |
|-------|----------------------|
| HIGH | Yes, with rollback |
| MEDIUM | Read-only checks only |
| LOW/NONE | No — ask for evidence |

## Tier 2 References

- `references/sync-drift.md` — Sync failures, drift detection, auto-sync issues.
- `references/appproject-rbac.md` — AppProject restrictions, RBAC, permissions.
- `references/webhook.md` — Webhook configuration, refresh, polling.

## Required Output

```
## Sync Flow Status (which stage failed)
## Observed Facts
## Root Cause — Confidence: HIGH/MEDIUM/LOW/NONE
## Remediation Plan
## Critic's Safety Review
## Rollback Plan
🛑 Awaiting approval.
```
