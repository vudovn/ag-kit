# Storage & Network Diagnosis — OpenShift Platform

## PVC Issues

### PVC Pending
1. Check StorageClass: `oc get sc`.
2. Check PVC events: `oc describe pvc <name> -n <ns>`.
3. Check provisioner pod health.
4. Check capacity and access mode.
5. Check node affinity constraints for local volumes.

### Mount Failures
1. Check Pod events for mount errors.
2. Check volume plugin and CSI driver.
3. Check filesystem permissions and SELinux context.
4. Check for stale NFS handles or iSCSI sessions.

## Network Issues

### Service Not Reachable
1. Check Service selector matches Pod labels.
2. Check endpoints: `oc get endpoints <svc> -n <ns>`.
3. Check target port matches container port.
4. Check NetworkPolicy blocking traffic.

### Route Issues
1. Check Route host and path.
2. Check TLS termination configuration.
3. Check router pods: `oc get pods -n openshift-ingress`.
4. Check DNS resolution for the route hostname.
5. Check certificate validity.

### DNS Failures
1. Check CoreDNS pods: `oc get pods -n openshift-dns`.
2. Check resolv.conf inside the pod.
3. Check upstream DNS configuration.

## Read-Only Evidence Commands

```bash
oc get pvc -n <ns>
oc describe pvc <name> -n <ns>
oc get sc
oc get svc -n <ns>
oc get endpoints <svc> -n <ns>
oc get route -n <ns>
oc get networkpolicy -n <ns>
oc get pods -n openshift-dns
oc get pods -n openshift-ingress
```
