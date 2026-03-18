# Database Patterns

> Deep-dive reference for Go database access. Load when user works with SQL, ORM, or database design.

## ORM/Driver Selection

| Tool | Best For |
|------|----------|
| `database/sql` + raw SQL | Full control, simple queries |
| `sqlc` | Type-safe SQL → Go code generation |
| `pgx` | PostgreSQL-specific features, performance |
| `GORM` | Rapid prototyping, complex relations |
| `Bun` | Modern ORM, good performance |
| `ent` | Graph-based schema, code generation |

## Database Principles

```
├── Use connection pooling (sql.DB handles this)
├── Always use context-aware queries (QueryContext, ExecContext)
├── Use prepared statements for repeated queries
├── Close rows immediately: defer rows.Close()
├── Scan into structs, not individual variables
├── Use transactions for multi-step operations
├── Set reasonable timeouts via context
└── Monitor connection pool metrics

sqlc recommendation (for most projects):
├── Write SQL → Generate type-safe Go code
├── No runtime reflection
├── Catches SQL errors at compile time
├── Works with PostgreSQL, MySQL, SQLite
└── Pairs perfectly with pgx driver
```

## Migration Strategy

```
├── golang-migrate/migrate  → SQL-based, simple
├── goose                   → SQL or Go-based
├── atlas                   → Declarative, modern
│
├── ALWAYS use versioned migrations
├── NEVER modify existing migration files
├── Test migrations up AND down
└── Run migrations separately from app startup
```

## Connection Pool Tuning

```
sql.DB configuration:
├── SetMaxOpenConns()     → Match your DB max connections
├── SetMaxIdleConns()     → ~25% of max open
├── SetConnMaxLifetime()  → 5-15 minutes
├── SetConnMaxIdleTime()  → 1-3 minutes
└── Monitor with db.Stats()
```
