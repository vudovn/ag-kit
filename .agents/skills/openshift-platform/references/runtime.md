# Runtime Diagnosis — OpenShift Platform

## Investigation Order

```
Pod status → Container state → Exit code → Logs → Events → Previous container
```

## CrashLoopBackOff

1. Check container exit code and reason.
2. Check `oc logs <pod> -c <container> --previous --timestamps`.
3. Check events: `oc get events -n <ns> --sort-by=.lastTimestamp`.
4. Check resource limits (OOMKilled = exit 137).
5. Check image compatibility and entrypoint.
6. Check ConfigMap/Secret mount references.

## OOMKilled (Exit 137)

1. Check container memory limits vs actual usage.
2. Check if JVM/runtime heap exceeds container limit.
3. Check node memory pressure.
4. Do NOT just increase limits — measure first.

## ImagePullBackOff

1. Image name and tag (typo? missing tag?).
2. Registry DNS resolution.
3. ImagePullSecret bound to ServiceAccount.
4. Registry TLS/proxy.
5. Registry rate limiting.
6. Image architecture (amd64 vs arm64).

## Exit Code Reference

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Application error |
| 126 | Permission denied / not executable |
| 127 | Command not found |
| 137 | OOMKilled or SIGKILL |
| 139 | Segfault |
| 143 | SIGTERM (graceful shutdown) |

## Read-Only Evidence Commands

```bash
oc get pods -n <ns> -o wide
oc describe pod <pod> -n <ns>
oc logs <pod> -c <container> -n <ns> --timestamps
oc logs <pod> -c <container> -n <ns> --previous --timestamps
oc get events -n <ns> --sort-by=.lastTimestamp
```
