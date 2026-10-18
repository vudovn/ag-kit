---
name: python-fastapi
description: FastAPI REST API template principles. SQLAlchemy, Pydantic, Alembic.
---

# FastAPI API Template

> Versions reflect the latest stable line verified 2026-05. Pin to the current stable when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.12+ (current stable 3.14) |
| ORM | SQLAlchemy 2.0 (async) |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Auth | JWT + passlib |

---

## Directory Structure

> Domain/module layout (scales better than file-type for non-trivial apps). Each domain owns its router, schemas, models, service.

```
project-name/
├── alembic/             # Migrations
├── src/
│   ├── auth/
│   │   ├── router.py    # APIRouter
│   │   ├── schemas.py   # Pydantic models
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── service.py   # Business logic
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   ├── posts/           # Same shape per domain
│   ├── config.py        # Global settings (BaseSettings)
│   ├── database.py      # Async engine / session
│   ├── models.py        # Shared base models
│   ├── exceptions.py    # Global exceptions
│   └── main.py          # FastAPI() + include_router
├── tests/
├── requirements/        # base.txt / dev.txt / prod.txt
├── alembic.ini
└── .env
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Domain modules | Each feature folder owns router + schemas + models + service |
| Async | async/await throughout (AsyncSession, async_sessionmaker) |
| Dependency Injection | FastAPI Depends (validation, auth, DB session) |
| Pydantic v2 | Validation + serialization |
| SQLAlchemy 2.0 | Async sessions |

---

## API Structure

| Layer | Responsibility |
|-------|---------------|
| Routers | HTTP handling |
| Dependencies | Auth, validation |
| Services | Business logic |
| Models | Database entities |
| Schemas | Request/response |

---

## Setup Steps

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install fastapi uvicorn "sqlalchemy[asyncio]" alembic pydantic pydantic-settings`
4. Create `.env`
5. `alembic upgrade head`
6. `uvicorn src.main:app --reload`

---

## Best Practices

- Use async everywhere (AsyncSession, async dependencies; wrap sync SDKs in `run_in_threadpool`)
- Per-module `BaseSettings` over one global config
- Pydantic v2 for validation
- SQLAlchemy 2.0 async sessions
- Alembic migrations: static, reversible, descriptive slugs
- pytest-asyncio for tests; use `dependency_overrides` to mock
