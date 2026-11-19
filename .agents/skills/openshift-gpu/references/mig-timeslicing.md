# MIG & Time-Slicing — OpenShift GPU

## Multi-Instance GPU (MIG)

- Splits a single GPU into isolated instances (only A100, A30, H100+).
- Configured via ClusterPolicy `mig.strategy` field.
- Each MIG instance appears as a separate resource (e.g., `nvidia.com/mig-1g.5gb`).
- Requires GPU Feature Discovery to label MIG profiles.
- NEVER enable MIG without verifying GPU model supports it.

## Time-Slicing

- Shares a GPU across multiple pods via time-multiplexing.
- Configured via ConfigMap referenced in ClusterPolicy.
- Does NOT provide memory isolation — pods can interfere.
- Suitable for development/testing, NOT guaranteed for production inference.

## Common Failures

| Symptom | Cause |
|---------|-------|
| MIG resources not appearing | MIG not enabled in ClusterPolicy or unsupported GPU |
| Pod requesting MIG resource stays Pending | Wrong MIG profile name or profile not created |
| Time-sliced GPU OOM | Too many pods sharing, no memory isolation |
| ClusterPolicy stuck after MIG change | Nodes need GPU reset — requires drain + reboot |

## Safety

- NEVER modify ClusterPolicy MIG settings without explicit approval.
- MIG changes may require node drain and GPU reset.
- Always verify GPU model before suggesting MIG.
