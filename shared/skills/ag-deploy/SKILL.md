---
name: ag-deploy
version: 2.0.0
resident: false
triggers: ["deploy", "release", "ship", "production"]
---
# AG Deploy
Prepare release, run preflight, verify rollback path, and preserve runtime approval boundaries. Shipping is a workflow phase, not an excuse to skip verification.
