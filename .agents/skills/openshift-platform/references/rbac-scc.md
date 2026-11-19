# RBAC & SCC Diagnosis — OpenShift Platform

## RBAC Investigation

### Permission Denied
1. Identify the ServiceAccount used by the Pod.
2. Check Role and RoleBinding in the namespace.
3. Check ClusterRole and ClusterRoleBinding if cluster-scoped.
4. Use: `oc auth can-i --list --as=system:serviceaccount:<ns>:<sa> -n <ns>`.
5. Check if the action requires a ClusterRole vs namespace Role.

### Common RBAC Mistakes
- ServiceAccount in wrong namespace.
- RoleBinding references non-existent Role.
- ClusterRoleBinding used when RoleBinding is sufficient.
- Missing verb (get vs list vs watch vs create vs delete).

## SCC Investigation

### SCC Violation
1. Check Pod security context requirements.
2. Check assigned SCC: `oc get pod <pod> -n <ns> -o yaml | grep scc`.
3. Check ServiceAccount SCC annotations.
4. Check if `runAsUser`, `fsGroup`, or `supplementalGroups` conflict.
5. OpenShift assigns random UIDs by default — do NOT set fixed UIDs.

### SCC Priority
- `restricted` → `restricted-v2` → `nonroot` → `anyuid` → `privileged`.
- Always use the LEAST privileged SCC that works.
- WARN before recommending `anyuid` or `privileged`.

## Read-Only Evidence Commands

```bash
oc get sa -n <ns>
oc get role,rolebinding -n <ns>
oc get clusterrole,clusterrolebinding | grep <name>
oc auth can-i --list --as=system:serviceaccount:<ns>:<sa> -n <ns>
oc get pod <pod> -n <ns> -o yaml | grep scc
oc describe scc <scc-name>
```
