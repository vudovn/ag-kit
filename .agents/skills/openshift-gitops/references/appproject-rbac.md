# AppProject & RBAC — OpenShift GitOps

## AppProject Restrictions

1. Check allowed source repos: `spec.sourceRepos`.
2. Check allowed destinations: `spec.destinations` (server + namespace).
3. Check allowed cluster resources: `spec.clusterResourceWhitelist`.
4. Check allowed namespace resources: `spec.namespaceResourceWhitelist`.
5. Denied resources appear in sync failure with "not permitted" message.

## ArgoCD RBAC

1. Check ArgoCD ConfigMap RBAC: `oc get cm argocd-rbac-cm -n openshift-gitops -o yaml`.
2. Check ArgoCD user/group mappings.
3. Default policy may deny project creation or sync.

## ServiceAccount Permissions

1. ArgoCD application-controller SA needs permissions in target namespace.
2. Check ClusterRoleBinding for `openshift-gitops-argocd-application-controller`.
3. Managed-by annotations can prevent ArgoCD from modifying resources.

## Evidence Commands

```bash
oc get appproject -n openshift-gitops
oc describe appproject <proj> -n openshift-gitops
oc get cm argocd-rbac-cm -n openshift-gitops -o yaml
```
