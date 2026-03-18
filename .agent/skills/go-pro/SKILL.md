---
name: go-pro
description: Go development principles and decision-making. Idiomatic patterns, concurrency, clean architecture, project structure, testing, and performance. Teaches thinking, not copying.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Go Pro

> Go development principles and decision-making for 2025.
> **Learn to THINK like a Go developer, not memorize syntax.**

---

## ⚠️ How to Use This Skill

This skill teaches **decision-making principles**, not fixed code to copy.

- ASK user for framework/library preference when unclear
- Choose pattern based on PROJECT CONTEXT (scale, team, lifetime)
- Standard Library first—add dependencies only when justified

### 📁 Deep-Dive References

Load these **only when the specific topic is relevant** to the user's request:

| Reference | When to Load |
|-----------|------|
| `references/concurrency.md` | Goroutines, channels, errgroup, context patterns |
| `references/frameworks.md` | Framework selection (net/http vs Chi vs Gin vs Fiber) |
| `references/database.md` | ORM/driver selection, sqlc, migrations, connection pooling |
| `references/testing.md` | Table-driven tests, benchmarks, fuzz, mocking |
| `references/performance.md` | pprof, escape analysis, memory layout, GC tuning |
| `references/clean-architecture.md` | Layered architecture, DI, domain-driven structure |
| `references/api-design.md` | HTTP handlers, JSON, middleware, graceful shutdown |

---

## 1. Go Philosophy (Non-Negotiable)

### Core Tenets

```
"Simplicity is complicated." — Rob Pike

├── Clear is better than clever
├── A little copying is better than a little dependency
├── Don't panic (literally—avoid panic in library code)
├── Accept interfaces, return structs
├── Make the zero value useful
└── Errors are values, not exceptions
```

### Standard Library First

```
Before adding a dependency, ask:
├── Can `net/http` handle this? (Go 1.22+ has pattern routing)
├── Can `encoding/json` handle this?
├── Can `database/sql` handle this?
├── Can `log/slog` handle this? (Go 1.21+ structured logging)
└── Will this dependency survive 5 years?

Add dependency ONLY when:
├── Significant complexity reduction (e.g., sqlc, pgx)
├── Non-trivial to implement (e.g., JWT validation)
└── Well-maintained with clear ownership
```

---

## 2. Project Structure

### Decision Tree

```
How big is the project?
│
├── Single binary / Script / CLI tool
│   └── Flat layout
│       ├── main.go
│       ├── handler.go
│       ├── store.go
│       └── go.mod
│
├── Medium service (1 team, 1 domain)
│   └── Standard layout
│       ├── cmd/server/main.go
│       ├── internal/
│       │   ├── handler/
│       │   ├── service/
│       │   ├── repository/
│       │   └── model/
│       ├── pkg/            # Only if reuse is real
│       └── go.mod
│
└── Large system (multi-domain, multi-team)
    └── Domain-driven layout
        ├── cmd/
        │   ├── api/main.go
        │   └── worker/main.go
        ├── internal/
        │   ├── user/        # Domain package
        │   │   ├── handler.go
        │   │   ├── service.go
        │   │   ├── repository.go
        │   │   └── model.go
        │   ├── order/       # Domain package
        │   └── platform/    # Shared infra
        │       ├── database/
        │       ├── logger/
        │       └── middleware/
        └── go.mod
```

### Key Rules

```
├── cmd/        → Entry points ONLY (wire up, start server)
├── internal/   → Private application code (compiler-enforced)
├── pkg/        → Truly reusable libraries (use sparingly!)
│
├── NEVER put business logic in cmd/
├── NEVER put HTTP concerns in service layer
├── NEVER import internal/ from another module
└── Keep main.go thin (< 50 lines ideally)
```

---

## 3. Error Handling

### Idiomatic Error Handling

```
Core patterns:
├── if err != nil { return fmt.Errorf("doing X: %w", err) }
├── Wrap errors with context using %w verb
├── Use errors.Is() for sentinel error comparison
├── Use errors.As() for type assertion on errors
├── Return errors, don't panic (except truly unrecoverable)
└── Handle errors at the right level (don't swallow!)

Error wrapping chain:
├── Repository:  fmt.Errorf("query user %d: %w", id, err)
├── Service:     fmt.Errorf("get user profile: %w", err)
├── Handler:     Log full error, return sanitized HTTP error
└── Client sees: {"error": "user not found"} (no internals!)
```

### Custom Error Types

```
When to create custom errors:
├── Need to carry structured data (error code, field name)
├── Need to distinguish error categories (NotFound, Conflict)
├── Need to map to HTTP status codes
└── Shared across multiple packages

When sentinel errors are enough:
├── Simple "not found" / "already exists" cases
├── Single package usage
└── No extra data needed
```

### Error Design Principles

```
├── Errors should be opaque to callers (use Is/As, not string matching)
├── Package-level sentinel: var ErrNotFound = errors.New("not found")
├── Don't log AND return the same error (pick one per layer)
├── Handler layer: log + return HTTP response
├── Service layer: wrap + return
└── Repository layer: wrap + return
```

---

## 4. Interface Design

### Core Principles

```
"The bigger the interface, the weaker the abstraction." — Rob Pike

├── Accept interfaces, return concrete types
├── Define interfaces where they are USED, not implemented
├── Keep interfaces small (1-3 methods ideal)
├── Use implicit satisfaction (no "implements" keyword needed)
└── io.Reader / io.Writer are the gold standard

Interface location:
├── Consumer package defines the interface
├── Producer package returns concrete struct
├── This allows testing without mocks of the whole world
└── Example: service/ defines Repository interface,
    repository/ returns *PostgresRepo struct
```

---

## 5. Logging & Observability

### Structured Logging (Go 1.21+)

```
Use log/slog (stdlib):
├── slog.Info("user created", "user_id", id, "email", email)
├── Structured key-value pairs
├── JSON output for production
├── Text output for development
├── Create child loggers with With()
└── No need for zerolog/zap unless specific features needed

Logging levels:
├── Debug → Development diagnostics
├── Info  → Normal operations
├── Warn  → Recoverable issues
├── Error → Failures requiring attention
└── NEVER log sensitive data (passwords, tokens, PII)
```

---

## 6. Go Modules & Dependencies

```
├── go mod init → Start new module
├── go mod tidy → Clean up go.mod/go.sum
├── go mod vendor → Vendor dependencies (optional)
├── go mod verify → Verify integrity
│
├── Pin major versions in go.mod
├── Review go.sum changes in code review
├── Use govulncheck for vulnerability scanning
├── Prefer fewer, well-maintained dependencies
└── Check license compatibility
```

### Build & Release

```
├── go build -ldflags "-s -w" → Strip debug for smaller binary
├── CGO_ENABLED=0 → Static binary (no C dependencies)
├── Use multi-stage Docker builds
├── Cross-compile: GOOS=linux GOARCH=amd64 go build
└── Use goreleaser for automated releases
```

---

## 7. Anti-Patterns to Avoid

### ❌ DON'T:
- Use `init()` for complex initialization (hard to test, surprising)
- Use `panic` in library code (return errors instead)
- Ignore errors with `_ = someFunc()` without explicit comment
- Use global mutable state (use dependency injection)
- Use `interface{}` / `any` when generics (Go 1.18+) work better
- Import from another project's `internal/` package
- Use Gin/Fiber for simple APIs where `net/http` suffices
- Store `context.Context` in struct fields
- Start goroutines without lifecycle management
- Use `sync.Mutex` when a channel is more appropriate

### ✅ DO:
- Choose framework based on actual project needs
- Write table-driven tests for all business logic
- Use `context.Context` for cancellation and timeouts
- Profile before optimizing
- Keep interfaces small (1-3 methods)
- Use `errgroup` for concurrent operations
- Run `go vet`, `staticcheck`, `golangci-lint` in CI
- Use `sqlc` or `pgx` for database interactions
- Document exported functions and types
- Use `go generate` for code generation workflows

---

## 8. Decision Checklist

Before implementing:

- [ ] **Asked user about framework preference?**
- [ ] **Chosen net/http vs framework for THIS context?**
- [ ] **Decided project structure scale?** (flat / standard / domain-driven)
- [ ] **Planned error handling strategy?** (sentinel / custom types / wrapping)
- [ ] **Identified concurrency needs?** (goroutines, channels, errgroup)
- [ ] **Chosen database approach?** (raw SQL, sqlc, GORM)
- [ ] **Planned testing strategy?** (table-driven, integration, benchmarks)
- [ ] **Considered clean architecture necessity?** (skip if simple CRUD)
- [ ] **Set up linting?** (golangci-lint with project config)

---

> **Remember**: Go's power is in its simplicity. Don't fight the language—embrace `if err != nil`, small interfaces, explicit code, and the standard library. The best Go code looks boring—and that's the point.
