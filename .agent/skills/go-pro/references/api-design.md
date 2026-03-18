# API Design Principles

> Deep-dive reference for Go HTTP API design. Load when user builds REST APIs, middleware, or JSON handlers.

## HTTP Handler Patterns

```
Go 1.22+ ServeMux patterns:
├── mux.HandleFunc("GET /users/{id}", handler.GetUser)
├── mux.HandleFunc("POST /users", handler.CreateUser)
├── Method + path in one string
└── Path parameters via r.PathValue("id")

Middleware chain:
├── func Middleware(next http.Handler) http.Handler
├── Compose: Logger(Auth(RateLimit(handler)))
├── Use for: logging, auth, CORS, recovery, metrics
└── Keep middleware focused (single responsibility)
```

## JSON Handling

```
Encoding/Decoding:
├── Use json.NewDecoder(r.Body) for requests (streaming)
├── Use json.NewEncoder(w) for responses
├── Define struct tags: `json:"field_name,omitempty"`
├── Use json.RawMessage for deferred parsing
├── Limit request body size: http.MaxBytesReader
└── Set Content-Type header: "application/json"

Validation:
├── Validate after decoding, not during
├── Use struct tags + validator package for complex rules
├── Return 422 for validation errors with field-level details
└── Sanitize output (never expose internal struct fields)
```

## Response Format

```
Consistent API response:
├── Success: { "data": {...} }
├── Error:   { "error": { "code": "NOT_FOUND", "message": "..." } }
├── List:    { "data": [...], "pagination": { "total": N, "page": 1 } }
│
├── Always return JSON (even for errors)
├── Use appropriate HTTP status codes
└── Include request ID in response headers
```

## Error Response Mapping

| Domain Error | HTTP Status | Error Code |
|-------------|-------------|------------|
| Not found | 404 | `NOT_FOUND` |
| Validation failed | 422 | `VALIDATION_ERROR` |
| Already exists | 409 | `CONFLICT` |
| Unauthorized | 401 | `UNAUTHORIZED` |
| Forbidden | 403 | `FORBIDDEN` |
| Internal error | 500 | `INTERNAL_ERROR` |

## Graceful Shutdown

```
Production servers must handle shutdown:
├── Listen for os.Signal (SIGINT, SIGTERM)
├── Call server.Shutdown(ctx) with timeout
├── Finish in-flight requests
├── Close database connections
├── Flush logs
└── Exit cleanly
```
