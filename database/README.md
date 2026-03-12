# 🗄️ LUNA Multi-Brain V2 - Database

## Visão Geral

Estrutura de banco de dados completa para o LUNA Multi-Brain V2, incluindo migrations, seeds, schemas e functions.

---

## 📁 Estrutura

```
database/
├── migrations/              # Migrations do banco
│   ├── 001_multi_brain_v2.sql    # Schema completo v2.0.0
│   └── ...
├── seeds/                   # Dados iniciais
│   ├── 001_initial_data.sql      # Dados de exemplo
│   └── ...
├── schemas/                 # Definições de schema
└── functions/               # Funções stored procedures
```

---

## 🚀 Quick Start

### **1. Subir Migrations**

```bash
# PostgreSQL
psql -U postgres -d luna_brain -f database/migrations/001_multi_brain_v2.sql

# Ou via psql interativo
psql -U postgres -d luna_brain
\i database/migrations/001_multi_brain_v2.sql
```

### **2. Carregar Seeds (Opcional)**

```bash
# Dados iniciais para desenvolvimento
psql -U postgres -d luna_brain -f database/seeds/001_initial_data.sql
```

### **3. Verificar Instalação**

```bash
# Verificar tabelas
psql -U postgres -d luna_brain -c "\dt"

# Verificar feature flags
psql -U postgres -d luna_brain -c "SELECT * FROM feature_flags;"

# Verificar dados seed
psql -U postgres -d luna_brain -c "SELECT COUNT(*) FROM contacts;"
```

---

## 📊 Schema do Banco

### **Core Tables**

| Tabela | Descrição | Colunas Principais |
|--------|-----------|-------------------|
| `contacts` | Clientes/Leads | id, external_id, name, phone, email, ltv, tags, preferences |
| `conversations` | Conversas ativas | id, contact_id, channel, status, mode, intent, risk_score |
| `messages` | Mensagens | id, conversation_id, direction, type, content, transcription |

### **Feature Tables**

| Tabela | Feature | Descrição |
|--------|---------|-----------|
| `cache_entries` | Smart Caching | Cache persistente com TTL |
| `handoff_requests` | Human Handoff | Requests de handoff para humanos |
| `memory_chain` | Memory Chain | Audit trail imutável SHA-256 |
| `behavioral_dna` | Behavioral DNA | Perfis de personalização por cliente |
| `brain_decisions` | Multi-Brain Router | Decisões de roteamento de IA |
| `analytics_events` | Analytics | Eventos de analytics |
| `feature_flags` | Feature Flags | Configuração de features |

---

## 🔧 Configuração

### **Variáveis de Ambiente**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/luna_brain
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=luna_brain
DATABASE_USER=luna_user
DATABASE_PASSWORD=secure_password

# Pool Settings
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30
```

### **Conexão Python**

```python
# brain/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/luna_brain")

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 📖 Migrations

### **Criar Nova Migration**

```bash
# Nomear migration com versão e descrição
# Ex: 002_add_new_feature.sql

# Template
-- ============================================================
-- LUNA Multi-Brain V2 - Migration 002
-- ============================================================
-- Description: [O que esta migration faz]
-- Date: 2026-03-XX
-- ============================================================

-- Your SQL here
CREATE TABLE IF NOT EXISTS new_table (...);

-- Update version
COMMENT ON SCHEMA public IS 'LUNA Multi-Brain V2 - Migration 002 Applied';
```

### **Rollback Migration**

```bash
# Criar migration de rollback
# Ex: 002_rollback.sql

DROP TABLE IF EXISTS new_table CASCADE;
```

---

## 🌱 Seeds

### **Criar Novo Seed**

```sql
-- ============================================================
-- LUNA Multi-Brain V2 - Seed: [Nome]
-- ============================================================
-- Description: [O que este seed faz]
-- Date: 2026-03-XX
-- ============================================================

INSERT INTO table_name (columns) VALUES
    ('value1', 'value2'),
    ('value3', 'value4')
ON CONFLICT (unique_column) DO NOTHING;
```

### **Carregar Seeds em Produção**

```bash
# Nunca carregar seeds em produção!
# Seeds são apenas para desenvolvimento/testing

# Development
psql -U postgres -d luna_brain_dev -f database/seeds/001_initial_data.sql

# Staging (apenas dados específicos)
psql -U postgres -d luna_brain_staging -f database/seeds/002_staging_data.sql
```

---

## 🔍 Queries Úteis

### **Ver Feature Flags**

```sql
SELECT flag_name, enabled, config->>'description' as description
FROM feature_flags
ORDER BY flag_name;
```

### **Ver Performance do Cache**

```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) FILTER (WHERE cache_key IS NOT NULL) as hits,
    ROUND(AVG(access_count), 2) as avg_access_count
FROM cache_entries
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 7;
```

### **Ver Handoff Metrics**

```sql
SELECT 
    reason,
    COUNT(*) as total,
    ROUND(AVG(EXTRACT(EPOCH FROM (accepted_at - created_at))), 2) as avg_accept_time_sec,
    ROUND(COUNT(*) FILTER (WHERE status = 'resolved') * 100.0 / NULLIF(COUNT(*), 0), 2) as resolution_rate
FROM handoff_requests
GROUP BY reason
ORDER BY total DESC;
```

### **Ver Brain Usage**

```sql
SELECT 
    brain_type,
    model_used,
    COUNT(*) as usage_count,
    ROUND(AVG(confidence), 4) as avg_confidence,
    ROUND(AVG(actual_latency_ms), 2) as avg_latency_ms,
    ROUND(SUM(actual_cost)::numeric, 6) as total_cost_usd
FROM brain_decisions
GROUP BY brain_type, model_used
ORDER BY usage_count DESC;
```

### **Ver Memory Chain Integrity**

```sql
SELECT 
    COUNT(*) as total_entries,
    COUNT(*) FILTER (WHERE verified = TRUE) as verified_entries,
    MIN(timestamp) as oldest_entry,
    MAX(timestamp) as newest_entry
FROM memory_chain;
```

---

## 🔐 Segurança

### **RLS Policies (Row Level Security)**

```sql
-- Enable RLS
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own contacts
CREATE POLICY contacts_isolation ON contacts
    USING (auth.uid() = user_id);

-- Policy: Admins can see all
CREATE POLICY contacts_admin ON contacts
    USING (current_setting('app.current_user_role') = 'admin');
```

### **Grant Permissions**

```sql
-- Create read-only user
CREATE USER luna_readonly WITH PASSWORD 'readonly_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO luna_readonly;

-- Create app user
CREATE USER luna_app WITH PASSWORD 'app_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO luna_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO luna_app;

-- Create admin user
CREATE USER luna_admin WITH PASSWORD 'admin_password';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO luna_admin;
```

---

## 📊 Backup & Restore

### **Backup**

```bash
# Full backup
pg_dump -U postgres -d luna_brain -F c -b -v -f luna_brain.backup

# Schema only
pg_dump -U postgres -d luna_brain --schema-only -f luna_brain_schema.sql

# Data only
pg_dump -U postgres -d luna_brain --data-only -f luna_brain_data.sql
```

### **Restore**

```bash
# From backup file
pg_restore -U postgres -d luna_brain -v luna_brain.backup

# From SQL file
psql -U postgres -d luna_brain -f luna_brain_schema.sql
psql -U postgres -d luna_brain -f luna_brain_data.sql
```

---

## 🔧 Troubleshooting

### **Problema: Migration falha**

```sql
-- Verificar migrations aplicadas
SELECT * FROM pg_description 
WHERE description LIKE '%LUNA Multi-Brain%';

-- Reset schema (CUIDADO: apaga tudo!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Re-aplicar migration
\i database/migrations/001_multi_brain_v2.sql
```

### **Problema: Performance lenta**

```sql
-- Verificar índices faltando
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Analisar tabelas
ANALYZE contacts;
ANALYZE conversations;
ANALYZE messages;

-- Verificar queries lentas
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

---

## 📈 Monitoramento

### **Database Health**

```sql
-- Connection count
SELECT count(*) as active_connections
FROM pg_stat_activity
WHERE datname = 'luna_brain';

-- Table sizes
SELECT 
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Cache hit ratio
SELECT 
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

---

## 🔗 Links Relacionados

- `brain/cache.py` - Smart Caching implementation
- `brain/handoff.py` - Human Handoff implementation
- `brain/memory_chain.py` - Memory Chain implementation
- `docs/FINAL_IMPLEMENTATION_REPORT.md` - Complete documentation

---

**MCT LTDA 2026** | LUNA Multi-Brain V2 Database  
**Version:** 2.0.0  
**Last Updated:** 2026-03-12
