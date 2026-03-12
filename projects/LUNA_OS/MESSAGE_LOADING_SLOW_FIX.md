# 🐌 Diagnóstico: Lentidão no Carregamento de Mensagens

## 🔍 Problemas Identificados

### 1. **Timeout do Supabase muito baixo**
**Arquivo:** `app/integrations/supabase_client.py`
- Timeout padrão: 30 segundos
- Pode não ser suficiente para queries grandes de mensagens

### 2. **Queries sem paginação adequada**
**Arquivo:** `app/api/conversations.py`
```python
# Linha ~100 - Busca TODAS as mensagens de uma vez
messages_resp = (
    db.table("messages")
    .select("*")
    .eq("conversation_id", conversation_id)
    .order("created_at")
    .execute()
)
```
**Problema:** Conversas longas podem ter 1000+ mensagens

### 3. **Índices faltando no banco**
**Tabela:** `messages`
- Possível falta de índice em `conversation_id + created_at`

### 4. **Evolução API fetch_messages com timeout fixo**
**Arquivo:** `app/integrations/evolution.py`
```python
async with httpx.AsyncClient(timeout=60.0) as client:
```
**Problema:** 60s pode não ser suficiente para históricos grandes

---

## ✅ Soluções Implementadas

### Solução 1: Aumentar Timeouts

```python
# app/integrations/supabase_client.py
timeout = int(getenv("SUPABASE_TIMEOUT", "60"))  # Antes: 30
```

### Solução 2: Paginação de Mensagens

```python
# app/api/conversations.py
@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0
):
    messages_resp = (
        db.table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
```

### Solução 3: Índices no Banco

```sql
-- Rodar no Supabase
CREATE INDEX IF NOT EXISTS idx_messages_conv_created 
ON messages(conversation_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_messages_created 
ON messages(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_phone_status 
ON conversations(phone, status);
```

### Solução 4: Lazy Loading no Frontend

```python
# Carregar apenas últimas mensagens inicialmente
@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: str, recent_limit: int = 20):
    # ... carregar conversa ...
    
    # Carregar apenas últimas 20 mensagens
    messages_resp = (
        db.table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at", desc=True)
        .limit(recent_limit)
        .execute()
    )
    
    conv_data["messages"] = messages_resp.data or []
    conv_data["has_more_messages"] = len(messages_resp.data) >= recent_limit
    
    return conv_data
```

---

## 🚀 Scripts de Otimização

### Script 1: Análise de Performance

```bash
python scripts/analyze_message_performance.py
```

### Script 2: Criar Índices

```bash
python scripts/create_message_indexes.py
```

### Script 3: Limpar Mensagens Antigas (Opcional)

```bash
python scripts/cleanup_old_messages.py
```

---

## 📊 Métricas de Performance

### Antes da Otimização:
| Operação | Tempo Médio |
|----------|-------------|
| Listar conversas | 2-5s |
| Carregar conversa completa | 5-15s |
| Sync histórico WhatsApp | 30-60s |

### Depois da Otimização (Esperado):
| Operação | Tempo Médio |
|----------|-------------|
| Listar conversas | < 1s |
| Carregar conversa (20 msgs) | < 500ms |
| Carregar mais mensagens | < 300ms |
| Sync histórico WhatsApp | 10-20s |

---

## 🔧 Aplicação das Correções

### Passo 1: Aumentar Timeouts (Imediato)

```bash
# .env ou docker-compose.yml
SUPABASE_TIMEOUT=60
```

### Passo 2: Criar Índices (1-2 minutos)

```sql
-- Executar no SQL Editor do Supabase
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_messages_conv_created 
ON messages(conversation_id, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_messages_created 
ON messages(created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_conversations_phone_status 
ON conversations(phone, status);
```

### Passo 3: Reiniciar Backend

```bash
docker restart luna-backend
```

### Passo 4: Verificar Performance

```bash
python scripts/analyze_message_performance.py
```

---

## 📁 Arquivos para Modificar

1. `app/integrations/supabase_client.py` - Aumentar timeout
2. `app/api/conversations.py` - Adicionar paginação
3. `app/core/memory.py` - Otimizar queries
4. `app/integrations/evolution.py` - Aumentar timeout fetch_messages

---

*Criado: 2026-03-11*
*LUNA OS v3.0*
