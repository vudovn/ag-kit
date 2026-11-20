# NFD & Driver Diagnosis — OpenShift GPU

## NFD Checks

1. NFD Operator installed: `oc get csv -A | grep -i nfd`.
2. NodeFeatureDiscovery CR exists: `oc get nodefeaturediscovery -A`.
3. GPU nodes labeled: `oc get nodes -l feature.node.kubernetes.io/pci-10de.present`.
4. If no labels → NFD is not detecting GPU hardware.

## GPU Operator Install

1. GPU Operator CSV: `oc get csv -A | grep -i gpu`.
2. GPU Operator namespace: `oc get pods -n nvidia-gpu-operator -o wide`.
3. ClusterPolicy CRD: `oc get crd clusterpolicies.nvidia.com`.
4. ClusterPolicy resource: `oc get clusterpolicy -A`.
5. ClusterPolicy conditions: `oc describe clusterpolicy gpu-cluster-policy -n nvidia-gpu-operator`.

## Driver DaemonSet

1. Check DaemonSet: `oc get ds -n nvidia-gpu-operator`.
2. Check driver pods: `oc get pods -n nvidia-gpu-operator -l app=nvidia-driver-daemonset`.
3. Check driver pod logs: `oc logs <pod> -n nvidia-gpu-operator -c nvidia-driver-ctr`.
4. Check Driver Toolkit compatibility with current kernel.
5. Check events: `oc get events -n nvidia-gpu-operator --sort-by=.lastTimestamp`.

## Common Failures

| Symptom | Likely Cause |
|---------|-------------|
| No GPU labels on nodes | NFD not installed or not running |
| ClusterPolicy not ready | Operator install incomplete |
| Driver pod CrashLoopBackOff | Kernel/driver mismatch or Driver Toolkit issue |
| Driver pod ImagePullBackOff | Registry access or disconnected install |
