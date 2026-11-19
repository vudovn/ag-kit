# Sync & Drift — OpenShift GitOps

## Sync Failure Investigation

1. Check Application status: `oc get application -n openshift-gitops`.
2. Check sync status details: `oc describe application <app> -n openshift-gitops`.
3. Look at `status.operationState.syncResult.resources` for per-resource errors.
4. Common causes: immutable field change, invalid schema, missing CRD, namespace mismatch.

## Drift Detection

1. Drift = live state differs from Git source.
2. Check `status.sync.status` = `OutOfSync`.
3. Check `status.sync.comparedTo` for source revision.
4. Causes: manual `oc apply`, mutating webhooks, controllers modifying resources.
5. Use `argocd app diff <app>` (read-only) to see exact differences.

## Auto-Sync Issues

1. Auto-sync enabled but not syncing → check Application annotations.
2. Auto-prune disabled → orphaned resources not removed.
3. Self-heal disabled → manual changes not reverted.
4. Retry not configured → transient failures not retried.

## Evidence Commands

```bash
oc get application -n openshift-gitops
oc describe application <app> -n openshift-gitops
oc get application <app> -n openshift-gitops -o yaml
```
