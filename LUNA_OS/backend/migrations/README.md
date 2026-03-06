# 🗄️ LUNA OS v3.0 - Migrations do Supabase

Esta pasta contém todas as migrations do banco de dados Supabase, organizadas em ordem de execução.

**Localização:** `LUNA_OS/backend/migrations/`

---

## 📋 Estrutura das Migrations

| Arquivo | Descrição | Tabelas Criadas |
|---------|-----------|-----------------|
| `000_init_extensions.sql` | Extensões necessárias | uuid-ossp |
| `001_core_tables.sql` | Tabelas principais | clients, conversations, messages, appointments |
| `002_business_tables.sql` | Tabelas de negócio | campaigns, knowledge_base, analytics_daily |
| `003_support_tables.sql` | Tabelas de suporte | handoffs, learnings, system_settings |
| `004_ml_tables.sql` | Tabelas de ML (DEBT #7) | ml_models, guardrail_violations |
| `005_dojo_tables.sql` | Tabelas do Dojo Arena | dojo_simulations, dojo_edge_cases, dojo_learning_cycles |
| `006_intelligence_tables.sql` | Conversation Intelligence | conversation_intelligence, conversation_metrics |
| `007_rls_policies.sql` | Row Level Security | Policies para todas as tabelas |
| `008_storage_buckets.sql` | Storage Buckets | models, conversations, exports |
| `009_seed_data.sql` | Dados iniciais | Settings, FAQ, Services |
| `010_functions_triggers.sql` | Funções e Triggers | Views, Functions, Triggers |

**Total:** 17 tabelas + views + functions + triggers + RLS policies

---

## 🚀 Como Executar

### **Opção 1: Python Script (Recomendado para Dev)**

```bash
cd LUNA_OS/backend

# Execute via Python (requer supabase-py instalado)
python -m app.scripts.run_migrations
```

### **Opção 2: Bash Script**

```bash
cd LUNA_OS/backend/migrations

# Exporte a URL do banco (pegue no Supabase Dashboard → Settings → Database)
export SUPABASE_DB_URL="postgresql://postgres.xxx:senha@db.xxx.supabase.co:5432/postgres"

# Execute todas as migrations
./run_migrations.sh
```

---

## ✅ Validação Pós-Migration

Execute estas queries para validar:

```sql
-- 1. Contar tabelas criadas (deve ser 17+)
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'public';

-- 2. Verificar tabelas principais
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- 3. Validar seed data
SELECT key, value FROM system_settings LIMIT 5;
SELECT category, key FROM knowledge_base LIMIT 5;

-- 4. Testar views
SELECT * FROM active_conversations_with_clients LIMIT 1;
SELECT * FROM todays_appointments LIMIT 1;

-- 5. Verificar RLS habilitado
SELECT tablename, rowsecurity FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = true;
```

---

## 📝 Notas Importantes

1. **Ordem de Execução:** Execute as migrations em ordem numérica (000 → 010)
2. **RLS Policies:** As policies de segurança são aplicadas na migration 007
3. **Storage Buckets:** A migration 008 requer permissões de admin
4. **Seed Data:** A migration 009 pode ser customizada conforme necessidade
5. **Backward Compatible:** Todas as migrations usam `IF NOT EXISTS`

---

## 🔧 Troubleshooting

### **Erro: "relation already exists"**
```sql
-- As migrations são idempotentes. Se já existe, pule para a próxima.
-- Ou drop e recrie (apenas em desenvolvimento):
DROP TABLE IF EXISTS clients CASCADE;
```

### **Erro: "permission denied for table storage.buckets"**
```sql
-- Execute no SQL Editor como admin
-- Ou crie os buckets manualmente via UI do Supabase:
-- Storage → New Bucket → "models" (private)
```

### **Erro: "function uuid_generate_v4() does not exist"**
```sql
-- Execute manualmente:
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

## 📚 Referências

- [Supabase Migrations Docs](https://supabase.com/docs/guides/database/migrations)
- [Supabase RLS Docs](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase Storage Docs](https://supabase.com/docs/guides/storage)

---

**Última atualização:** 2026-03-03  
**Versão:** LUNA OS v3.0
