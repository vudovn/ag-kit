# Framework Selection (2025)

> Deep-dive reference for Go web framework selection. Load when user needs to choose or compare frameworks.

## Decision Tree

```
What are you building?
│
├── API with simple routing (Go 1.22+)
│   └── net/http (ServeMux now supports patterns!)
│
├── REST API with middleware needs
│   └── Chi (lightweight, net/http compatible)
│
├── High-performance API / Microservice
│   └── Gin or Echo (battle-tested, fast)
│
├── Maximum performance (benchmarks matter)
│   └── Fiber (fasthttp-based, Express-like API)
│
├── gRPC service
│   └── google.golang.org/grpc + protobuf
│
└── CLI tool
    └── cobra + viper
```

## Comparison Principles

| Factor | net/http | Chi | Gin | Fiber |
|--------|----------|-----|-----|-------|
| **Best for** | Simple APIs, Go 1.22+ | Composable middleware | Production REST APIs | Max throughput |
| **Dependencies** | Zero | Minimal | Moderate | fasthttp (non-std) |
| **net/http compatible** | ✅ | ✅ | ❌ (own context) | ❌ (fasthttp) |
| **Middleware ecosystem** | Manual | Rich, composable | Rich, built-in | Growing |
| **Learning curve** | Low | Low | Low | Low |

## Selection Questions to Ask:
1. Does the project need to stay net/http compatible?
2. Is raw throughput critical (>100K req/s)?
3. Does the team already know a specific framework?
4. How important is the middleware ecosystem?

> **Default recommendation for new projects**: `net/http` (Go 1.22+) or `Chi` for composability. Only reach for Gin/Fiber when justified.

## Go 1.22+ ServeMux Patterns

```
New routing capabilities:
├── mux.HandleFunc("GET /users/{id}", handler.GetUser)
├── mux.HandleFunc("POST /users", handler.CreateUser)
├── Method + path in one string
├── Path parameters via r.PathValue("id")
├── Precedence rules: more specific patterns win
└── No need for Chi/Gorilla for simple routing anymore
```

## Middleware Pattern

```
Standard middleware signature:
├── func Middleware(next http.Handler) http.Handler
├── Compose: Logger(Auth(RateLimit(handler)))
├── Use for: logging, auth, CORS, recovery, metrics
└── Keep middleware focused (single responsibility)
```
