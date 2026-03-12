# 🗄️ INSTRUÇÕES CORRIGIDAS — SUPABASE

**Data:** 2026-03-12  
**Problema:** Erro `column "contact_id" does not exist`

---

## 🔍 **PASSO 1: DEBUG (Execute Primeiro)**

**Arquivo:** `migrations/000_debug_check.sql`

**Como:**
1. Copie o conteúdo do arquivo
2. Cole no SQL Editor do Supabase
3. Execute

**Resultado:** Vai mostrar quais tabelas já existem

**Envie o resultado para eu saber o que existe no seu banco!**

---

## ✅ **PASSO 2: MIGRATION MINIMALISTA (Seguro)**

**Arquivo:** `migrations/002_minimal_safe.sql`

**Este SQL:**
- ✅ **NÃO tem foreign keys**
- ✅ **NÃO referencia outras tabelas**
- ✅ **Cria apenas 2 tabelas:** `cache_entries` + `feature_flags`
- ✅ **À prova de falhas**

**Como:**
1. Copie o conteúdo
2. Cole no SQL Editor
3. Execute

**Resultado Esperado:**
```
NOTICE: ✅ TABLES CREATED SUCCESSFULLY!
Tables: cache_entries, feature_flags
Feature flags: 7
```

---

## 📋 **ARQUIVOS CRIADOS**

| Arquivo | Finalidade | Use? |
|---------|-----------|------|
| `000_debug_check.sql` | Verificar tabelas existentes | ✅ **SIM (primeiro)** |
| `001_multi_brain_v2_fixed.sql` | Migration completo | ⏳ Depois |
| `002_minimal_safe.sql` | Migration mínimo seguro | ✅ **SIM (segundo)** |

---

## 🎯 **ORDEM CORRETA**

```
1. Execute: 000_debug_check.sql
   → Envie o resultado para mim

2. Execute: 002_minimal_safe.sql
   → Deve funcionar sem erros

3. Me envie o resultado
```

---

## 🆘 **SE AINDA DER ERRO**

**Me envie:**
1. Print do erro completo
2. Resultado do `000_debug_check.sql`
3. Qual arquivo você executou

---

**MCT LTDA 2026** | LUNA OS Migration  
**Status:** 🔧 **DEBUGGING**  
**Próximo:** **EXECUTE 000_debug_check.sql PRIMEIRO!**
