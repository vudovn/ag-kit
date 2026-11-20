# Scheduling Diagnosis — OpenShift Platform

## Pod Pending Investigation

```
Pod Pending → Check events → Node capacity → Taints → Selectors → Quotas → PVC
```

### Step-by-Step
1. `oc describe pod <pod> -n <ns>` — look at Events section.
2. Check scheduling failure reason in events.
3. Check node capacity: `oc describe node <node>` → Allocatable vs Allocated.
4. Check taints: `oc get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints`.
5. Check Pod tolerations match node taints.
6. Check nodeSelector and nodeAffinity.
7. Check ResourceQuota: `oc get resourcequota -n <ns>`.
8. Check LimitRange: `oc get limitrange -n <ns>`.
9. Check if PVC is pending (volume affinity).

## Node Issues

### Node NotReady
1. Check node conditions: `oc get nodes`.
2. Check kubelet: `oc describe node <node>` → Conditions.
3. Check disk pressure, memory pressure, PID pressure.
4. Check network unreachable.
5. Check machine-config-daemon if MachineConfig was recently applied.

### Node Drain
- NEVER drain without explicit approval.
- Always check workload impact before drain.
- Verify PodDisruptionBudgets: `oc get pdb -A`.

## Read-Only Evidence Commands

```bash
oc get nodes -o wide
oc describe node <node>
oc get pods -n <ns> --field-selector=status.phase=Pending
oc get resourcequota -n <ns>
oc get limitrange -n <ns>
oc get pdb -A
```
