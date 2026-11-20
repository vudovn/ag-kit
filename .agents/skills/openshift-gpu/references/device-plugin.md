# Device Plugin & DCGM — OpenShift GPU

## Container Toolkit

1. Check toolkit pods are running in `nvidia-gpu-operator` namespace.
2. Toolkit configures the container runtime to expose GPUs to containers.
3. If toolkit fails, device plugin and all downstream operands fail.

## Device Plugin

1. Check device-plugin DaemonSet: `oc get ds -n nvidia-gpu-operator`.
2. Check device-plugin pods on GPU nodes.
3. Verify `nvidia.com/gpu` appears in node capacity:
   `oc get nodes -o json | jq '.items[].status.capacity["nvidia.com/gpu"]'`.
4. If capacity is 0 or missing → device plugin not functioning.

## GPU Feature Discovery

1. Check GFD pods on GPU nodes.
2. GFD adds GPU model, driver version, CUDA labels to nodes.
3. Labels used by workload nodeSelectors.

## DCGM & Validator

1. DCGM Exporter exposes GPU metrics.
2. Validator pods run health checks on each GPU node.
3. Check validator pod logs for pass/fail.
4. Failed validators indicate upstream operand issues.

## Evidence Commands

```bash
oc get ds -n nvidia-gpu-operator
oc get pods -n nvidia-gpu-operator -o wide
oc describe node <gpu-node> | grep nvidia
oc get events -n nvidia-gpu-operator --sort-by=.lastTimestamp
```
