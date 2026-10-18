---
name: ag-preflight
version: 2.0.0
resident: false
triggers: ["preflight", "before ship", "release gate", "production check"]
---
# AG Preflight
Run blocking quality gates before publish or production deployment. Missing optional tools may warn; missing required project checks must not silently pass.
