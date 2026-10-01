# Security Checklists

> Quick reference checklists for security audits. Use alongside vulnerability-scanner principles.

---

## OWASP Top 10 Audit Checklist

> Aligned to OWASP Top 10:2025.

### A01: Broken Access Control
- [ ] Authorization on all protected routes
- [ ] Deny by default
- [ ] Rate limiting implemented
- [ ] CORS properly configured

### A02: Security Misconfiguration
- [ ] Unnecessary features disabled
- [ ] Error messages sanitized
- [ ] Security headers configured
- [ ] Default credentials changed

### A03: Software Supply Chain Failures
- [ ] Dependencies up to date, no known vulnerabilities
- [ ] Dependency integrity verified (lockfiles, checksums)
- [ ] Unused dependencies removed
- [ ] Build/CI pipeline and third-party scripts vetted

### A04: Cryptographic Failures
- [ ] Passwords hashed (bcrypt/argon2, cost 12+)
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ for all connections
- [ ] No secrets in code/logs

### A05: Injection
- [ ] Parameterized queries
- [ ] Input validation on all user data
- [ ] Output encoding for XSS
- [ ] No eval() or dynamic code execution

### A06: Insecure Design
- [ ] Threat modeling done
- [ ] Security requirements defined
- [ ] Business logic validated

### A07: Authentication Failures
- [ ] MFA available
- [ ] Session invalidation on logout
- [ ] Session timeout implemented
- [ ] Brute force protection

### A08: Software or Data Integrity Failures
- [ ] Dependency integrity verified
- [ ] CI/CD pipeline secured
- [ ] Update mechanism secured

### A09: Security Logging and Alerting Failures
- [ ] Security events logged
- [ ] Logs protected
- [ ] No sensitive data in logs
- [ ] Alerting configured

### A10: Mishandling of Exceptional Conditions
- [ ] Errors handled explicitly (no silent catch/empty handlers)
- [ ] Fail closed, not open, on unexpected state
- [ ] No sensitive detail leaked in error responses

---

## Authentication Checklist

- [ ] Strong password policy
- [ ] Account lockout
- [ ] Secure password reset
- [ ] Session management
- [ ] Token expiration
- [ ] Logout invalidation

---

## API Security Checklist

- [ ] Authentication required
- [ ] Authorization per endpoint
- [ ] Input validation
- [ ] Rate limiting
- [ ] Output sanitization
- [ ] Error handling

---

## Data Protection Checklist

- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management
- [ ] Data minimization
- [ ] Secure deletion

---

## Security Headers

| Header | Purpose |
|--------|---------|
| **Content-Security-Policy** | XSS prevention |
| **X-Content-Type-Options** | MIME sniffing |
| **X-Frame-Options** | Clickjacking |
| **Strict-Transport-Security** | Force HTTPS |
| **Referrer-Policy** | Referrer control |

---

## Quick Audit Commands

| Check | What to Look For |
|-------|------------------|
| Secrets in code | password, api_key, secret |
| Dangerous patterns | eval, innerHTML, SQL concat |
| Dependency issues | npm audit, snyk |

---

> **Usage:** Copy relevant checklists into your PLAN.md or security report.
