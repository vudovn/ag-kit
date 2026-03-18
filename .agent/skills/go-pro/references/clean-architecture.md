# Clean Architecture in Go

> Deep-dive reference for layered architecture and dependency injection in Go. Load when user designs service structure or needs DI patterns.

## Layer Separation

```
Request Flow:
│
├── Handler (Transport Layer)
│   ├── HTTP/gRPC specifics
│   ├── Parse request, validate input
│   ├── Call service method
│   └── Format response
│
├── Service (Business Logic Layer)
│   ├── Pure business rules
│   ├── Depends on repository INTERFACES
│   ├── No HTTP, no SQL
│   └── Testable in isolation
│
├── Repository (Data Access Layer)
│   ├── Database queries
│   ├── Implements repository interface
│   ├── No business logic
│   └── Returns domain models
│
└── Model (Domain Layer)
    ├── Structs representing business entities
    ├── No dependencies on other layers
    └── Validation methods optional
```

## Dependency Injection

```
DI in Go (no magic, no framework needed):
├── Constructor injection via New* functions
│   func NewUserService(repo UserRepository) *UserService
│
├── Wire up in cmd/main.go:
│   db := database.Connect(cfg)
│   userRepo := postgres.NewUserRepository(db)
│   userService := service.NewUserService(userRepo)
│   userHandler := handler.NewUserHandler(userService)
│
├── For large projects, consider google/wire
│   (compile-time DI code generation)
│
└── AVOID runtime DI containers (not idiomatic Go)
```

## When Clean Architecture is Overkill

```
Skip full layering when:
├── Simple CRUD with < 5 entities
├── CLI tools or scripts
├── Prototypes / POCs
└── Single-person, short-lived projects

Use full layering when:
├── Multiple developers
├── Complex business rules
├── Long-lived project (> 1 year)
├── Need to swap infrastructure
└── Extensive testing required
```

## Directory Mapping

```
Clean architecture → Go project:
├── Domain/Model     → internal/domain/ or internal/model/
├── Use Cases        → internal/service/
├── Interfaces       → internal/handler/ (HTTP), internal/grpc/ (gRPC)
├── Infrastructure   → internal/repository/, internal/platform/
└── Entry point      → cmd/server/main.go (wiring)
```
