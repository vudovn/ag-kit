# GPU Workload Scheduling — OpenShift GPU

## Workload Checklist

For every GPU workload, verify:

1. `nodeSelector` matches GPU node labels.
2. `tolerations` match GPU node taints.
3. `resources.limits` includes `nvidia.com/gpu: 1` (or MIG profile).
4. `resources.requests` matches limits for GPU.
5. Image is CUDA-compatible with the installed driver version.
6. RuntimeClass if applicable (e.g., `nvidia`).

## Pod Stuck in Pending

1. Check if `nvidia.com/gpu` capacity exists on any node.
2. Check if all GPU resources are already allocated.
3. Check nodeSelector/affinity constraints.
4. Check taints and tolerations.
5. Check ResourceQuota in the namespace.
6. Check if the requested GPU count exceeds available.

## GPU Visibility Inside Container

1. Run `nvidia-smi` inside the container (if image supports it).
2. Check `NVIDIA_VISIBLE_DEVICES` environment variable.
3. Check `NVIDIA_DRIVER_CAPABILITIES`.
4. Verify the runtime class and device plugin are functioning.

## Evidence Commands

```bash
oc describe pod <pod> -n <ns>
oc get nodes -o custom-columns=NAME:.metadata.name,GPU:.status.capacity.nvidia\\.com/gpu
oc get pods -n <ns> -o yaml | grep -A5 resources
```
