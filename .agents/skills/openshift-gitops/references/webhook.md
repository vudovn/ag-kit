# Webhook & Refresh — OpenShift GitOps

## Webhook Not Triggering Sync

1. Verify webhook URL configured in Git provider (GitHub/GitLab/Bitbucket).
2. Check ArgoCD webhook secret matches Git provider configuration.
3. Check ArgoCD server pod logs for incoming webhook requests.
4. Check network: Route, firewall, proxy between Git and ArgoCD.
5. Check TLS certificate on ArgoCD Route.

## Polling vs Webhook

- Default poll interval: 3 minutes.
- Webhook provides instant detection.
- If webhook fails, ArgoCD falls back to polling.

## Manual Refresh

- `argocd app get <app> --refresh` (read-only, triggers diff check).
- Useful for debugging without sync.

## Evidence Commands

```bash
oc logs -n openshift-gitops -l app.kubernetes.io/name=argocd-server --tail=100
oc get route -n openshift-gitops
```
