# Testing

> Deep-dive reference for Go testing patterns. Load when user writes tests, benchmarks, or fuzz tests.

## Table-Driven Tests (Idiomatic Go)

```
Pattern:
├── Define test cases as slice of structs
├── Loop through cases with t.Run(name, func)
├── Each case: input → expected output
├── Name each case descriptively
├── Add edge cases and error cases
└── Use t.Parallel() when tests are independent

Benefits:
├── Easy to add new cases
├── Clear what's being tested
├── Consistent structure across codebase
└── Great for debugging (run single case)
```

## Testing Strategy

| Type | Purpose | Tools |
|------|---------|-------|
| **Unit** | Business logic, pure functions | `testing` (stdlib) |
| **Integration** | Database, external services | `testcontainers-go` |
| **Benchmark** | Performance measurement | `testing.B` |
| **Fuzz** | Input discovery (Go 1.18+) | `testing.F` |
| **E2E** | Full API workflows | `net/http/httptest` |

## Testing Principles

```
├── Use stdlib testing package first
├── testify is OK for assertions (require/assert)
├── Use httptest.NewServer for HTTP tests
├── Use t.TempDir() for file-based tests
├── Use testcontainers for real database tests
├── Mock at interface boundaries only
├── Benchmark before optimizing: go test -bench=.
├── Fuzz test parsers and validators: go test -fuzz=.
└── Use t.Helper() in test helper functions
```

## Test Organization

```
Where to put tests:
├── Unit tests:        same package (foo_test.go)
├── Black-box tests:   package foo_test (external perspective)
├── Integration tests: //go:build integration tag
├── Test fixtures:     testdata/ directory (auto-ignored by go build)
└── Test helpers:      internal/testutil/ package
```

## Mocking Strategy

```
├── Define interfaces at consumer side
├── Generate mocks: mockgen, moq, or hand-written
├── Prefer hand-written fakes for simple interfaces
├── Use mockgen for complex interfaces (many methods)
├── NEVER mock what you don't own (wrap external deps first)
└── Integration test > mocking when feasible
```
