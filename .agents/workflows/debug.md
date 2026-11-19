---
name: debug
description: Unified debugging command with progressive layered triage, empirical verification, and a 2-pass circuit breaker.
version: 1.1.0
requires_agents: debugger
requires_skills: systematic-debugging, verify-changes
artifact_outputs: root-cause, fix-summary, verification-report, escalation-report
---

# /debug - Unified Progressive Problem Investigation

$ARGUMENTS

---

## Purpose

Activates **DEBUG mode** for systematic investigation and resolution of software bugs, runtime failures, and infrastructure incidents. Operates in progressive layers to minimize token consumption and enforces a bounded verification gate to prevent infinite retry loops.

---

## 4-Layer Progressive Debug Architecture

### Layer 0: Signal Triage & Domain Routing (Zero Skill Overhead)
Before loading deep domain knowledge, classify failure signals from provided logs, error messages, and context:

| Observed Signal Keywords | Domain Category | Specialist Agent Dispatch |
|--------------------------|-----------------|----------------------------|
| UI, React, Vue, CSS, DOM, syntax error, TypeError, null pointer, client crash | Application Code | `@debugger` + `systematic-debugging` |
| REST, GraphQL, 500/502, schema mismatch, SQL, ORM, connection pool | Backend & Database | `@backend-specialist` + `api-patterns` / `database-design` |
| Pod, CrashLoopBackOff, OOMKilled, SCC, RBAC, PVC, Route, ClusterOperator, GPU | OpenShift & Kubernetes | `@openshift-sre` + `openshift-platform` |
| KVM, libvirt, virsh, QEMU, domain XML, hugepages, Satellite, Capsule, Content View | Linux Virtualization & Satellite | `@linux-infra-sre` + `kvm-linux-virtualization` |
| PipelineRun, TaskRun, Jenkinsfile, Shared Library, webhook, ArgoCD drift | CI/CD & GitOps | `@devops-engineer` + `cicd-architecture` |

---

### Layer 1: Systematic Investigation (Hypothesis Formulation)
1. **Gather Evidence**: Extract exact stack traces, exit codes, recent git diffs, and configuration state.
2. **Form Ordered Hypotheses**: Formulate 2-3 prioritized root-cause hypotheses based strictly on observed facts.
3. **Progressive Reference Loading**: If deeper schema definitions or failure catalogs are needed, load **at most one** targeted reference document.

---

### Layer 2: Safe Root-Cause Remediation
1. **Creator Mode**: Draft minimal, surgical code or configuration remediation.
2. **Critic Self-Review**:
   - Are destructive or unverified commands proposed?
   - Does this fix address the root cause or merely mask symptoms?
   - Is there a clear rollback path?
3. **Production Safety Guard**: On infrastructure incidents, mutating commands (`oc apply`, `oc delete`, `virsh destroy`, `hammer content-view publish`) are strictly blocked without prior confirmation.

---

### Layer 3: Empirical Verification Gate & Bounded Circuit Breaker
Never assume a fix works based on code inspection alone. Every fix must be proven empirically:

```
[ Apply Targeted Fix ]
         │
         ▼
[ Run Verification (Test / Build / Dry-Run / Lint) ]
         │
    ┌────┴────┐
    ▼         ▼
 [PASS]    [FAIL]
    │         │
    │    [ Check Iteration Count ]
    │         │
    │    ┌────┴───────────────────────────┐
    │    ▼                                ▼
    │  Attempt 1 (Auto-Remediate)       Attempt 2 (LIMIT REACHED)
    │  - Ingest exact error log         🛑 TRIP CIRCUIT BREAKER
    │  - Refine fix once                - Halt mutations immediately
    │                                   - Generate escalation-report.md
    ▼                                   - Escalate to user
[ Generate verification-report.md ]
```

#### Circuit Breaker Rules:
- **Hard Limit:** Exactly **`max_iterations: 2`**. Under no circumstances may an automated retry loop run a 3rd iteration.
- **Circuit Breaker Action:** If Attempt 2 fails verification:
  1. Halt all workspace modifications.
  2. Emit `escalation-report.md` detailing:
     - Initial symptom and root cause hypothesis.
     - Fix attempted in Iteration 1 and subsequent failure message.
     - Fix attempted in Iteration 2 and why it did not pass verification.
     - Concrete manual troubleshooting recommendations.
  3. Yield control to the human developer.

---

## Output Format

```markdown
## 🔍 Debug: [Issue Title]

### 1. Triage & Classification
- **Domain:** [Application | Backend/DB | OpenShift/K8s | Virtualization | CI/CD]
- **Target Specialist:** `@[agent-name]`
- **Signal Summary:** [Key signals matched]

### 2. Evidence Gathered
- **Error / Log:** `[exact error string]`
- **Location:** `[file:line / namespace:resource]`
- **Observed Behavior:** [What occurred]
- **Expected Behavior:** [What should occur]

### 3. Hypotheses Tested
1. ❓ [Primary hypothesis] → [Validation test result]
2. ❓ [Secondary hypothesis] → [Validation test result]

### 4. Root Cause
🎯 **[Precise technical explanation of why the failure occurred]**

### 5. Surgical Remediation
```[language]
// Before
[broken state]

// After
[fixed state]
```

### 6. Empirical Verification
- **Verification Command:** `[test / build / validation command executed]`
- **Result:** [PASS ✅ | ATTEMPT 1 FAILED (Auto-Remediated) | CIRCUIT BREAKER TRIPPED 🛑]
- **Exit Code / Output:** `[summary]`

### 7. Prevention & Resilience
🛡️ [Structural change, test case, or guardrail added to prevent recurrence]
```

---

## Examples

```
/debug login button unresponsive in production
/debug CrashLoopBackOff on payment-api pod
/debug KVM domain fails to boot after hugepages reconfiguration
/debug ArgoCD Application OutOfSync due to schema drift
```

---

## 🔗 Next Step

Once verification passes:
- To run full test regression suite: `/test`
- If ready for deployment: `/deploy`
- If circuit breaker tripped: `/brainstorm` (re-assess architecture)
