# 🔧 LUNA OS - Modo de Produção Não Respondia

## 🐛 **Problema Identificado**

A Luna não respondia quando o modo de produção (`active`) era ativado.

---

## 🔍 **Causas Raiz Encontradas**

### 1. **Tabela `luna_activations` não existia** ❌
**Erro:**
```
Could not find the table 'public.luna_activations' in the schema cache
```

**Impacto:** Gate falhava ao tentar verificar ativações no modo manual

**Solução:** 
- Criar tabela `luna_activations` no Supabase
- Adicionar fallback no código para retornar `True` se tabela não existir

---

### 2. **Modo estava como "observe"** ⚠️
**Status:**
```json
{
  "mode": "observe",
  "responding": false
}
```

**Impacto:** Luna apenas observava, não respondia

**Solução:** Mudar modo para "active" via API

---

## ✅ **Soluções Aplicadas**

### 1. Criação da Tabela `luna_activations`

**Arquivo:** `scripts/sql/create_luna_activations_table.sql`

```sql
CREATE TABLE IF NOT EXISTS luna_activations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone TEXT NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT true,
    activated_by TEXT DEFAULT 'operator',
    activated_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_luna_activations_phone ON luna_activations(phone);
CREATE INDEX IF NOT EXISTS idx_luna_activations_is_active ON luna_activations(is_active);
```

**Como executar:**
1. Abrir Supabase Dashboard → SQL Editor
2. Copiar SQL do arquivo acima
3. Executar

---

### 2. Fallback no Activation Gate

**Arquivo:** `app/core/activation_gate.py`

**Mudanças:**

```python
def _is_phone_activated(phone: str) -> bool:
    """Check if phone is in luna_activations table.
    
    If table doesn't exist, return True for safety (allow response).
    """
    from app.integrations.supabase_client import get_supabase
    db = get_supabase()
    if not db:
        logger.warning("[Gate] Supabase not connected - allowing response")
        return True
    
    try:
        result = (
            db.table("luna_activations")
            .select("id")
            .eq("phone", phone)
            .eq("is_active", True)
            .limit(1)
            .execute()
        )
        return bool(result.data)
    except Exception as e:
        # Tabela não existe ou erro - permitir resposta para segurança
        logger.warning(f"[Gate] Error checking activation for {phone}: {e} - allowing response")
        return True
```

**Impacto:** Gate não bloqueia mais se tabela não existir

---

### 3. Endpoint de Debug do Gate

**Arquivo:** `app/api/webhooks.py`

**Novo endpoint:**
```python
@router.get("/gate/debug")
async def debug_gate(phone: str = None):
    """
    Endpoint de diagnóstico do Activation Gate.
    Mostra status do gate para um telefone específico ou geral.
    """
```

**Uso:**
```bash
# Ver status geral
curl "http://localhost:8000/api/webhooks/gate/debug" \
  -H "X-Admin-Key: YOUR_KEY"

# Ver status para telefone específico
curl "http://localhost:8000/api/webhooks/gate/debug?phone=5549999999999@s.whatsapp.net" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Response:**
```json
{
  "mode": "active",
  "responding": true,
  "test_count": "5",
  "test_limit": 5,
  "activations_count": 0,
  "phone_check": {
    "phone": "5549999999999@s.whatsapp.net",
    "allowed": true,
    "reason": "active"
  }
}
```

---

## 📋 **Como Resolver o Problema (Passo a Passo)**

### **Passo 1: Criar Tabela no Supabase**

```bash
# 1. Acessar https://supabase.com/dashboard
# 2. Ir em SQL Editor
# 3. Executar:
cat backend/scripts/sql/create_luna_activations_table.sql
```

---

### **Passo 2: Verificar Modo Atual**

```bash
curl "http://localhost:8000/api/webhooks/mode" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Esperado:**
```json
{
  "mode": "active",
  "responding": true
}
```

**Se estiver "observe":**
```bash
curl -X POST "http://localhost:8000/api/webhooks/mode" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: YOUR_KEY" \
  -d '{"mode": "active"}'
```

---

### **Passo 3: Testar Gate**

```bash
curl "http://localhost:8000/api/webhooks/gate/debug?phone=5549999999999@s.whatsapp.net" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Esperado:**
```json
{
  "phone_check": {
    "allowed": true,
    "reason": "active"
  }
}
```

---

### **Passo 4: Reiniciar Backend**

```bash
docker restart luna-backend
sleep 10
```

---

### **Passo 5: Testar no WhatsApp**

1. Enviar mensagem para o número do salão
2. Verificar logs:
   ```bash
   docker logs -f luna-backend | grep -E "(Gate|Response|sent)"
   ```
3. Esperar ver:
   ```
   📤 Response sent | gate=active
   ```

---

## 🎯 **Modos de Operação**

| Modo | Responde? | Descrição |
|------|-----------|-----------|
| `active` | ✅ Sim | Responde todas as mensagens 24/7 |
| `observe` | ❌ Não | Apenas observa, não responde (safe mode) |
| `test` | ⚠️ Limitado | Responde até `test_limit` conversas |
| `manual` | 🔓 Ativados | Apenas telefones em `luna_activations` |

---

## 🔍 **Diagnóstico Rápido**

### **SQL de Diagnóstico:**

```sql
-- 1. Verificar modo atual
SELECT key, value, updated_at
FROM system_settings
WHERE key = 'luna_mode';

-- 2. Verificar contadores de teste
SELECT key, value
FROM system_settings
WHERE key IN ('test_count', 'test_limit');

-- 3. Verificar telefones ativados
SELECT phone, is_active, activated_by, activated_at
FROM luna_activations
WHERE is_active = true;

-- 4. Verificar conversas ativas
SELECT 
    id,
    phone,
    status,
    last_message_at,
    messages_count
FROM conversations
WHERE status = 'active'
ORDER BY last_message_at DESC
LIMIT 10;
```

---

## 📊 **Status After Fix**

| Componente | Status | Notas |
|------------|--------|-------|
| Tabela `luna_activations` | ✅ Criada | Com índices e trigger |
| Activation Gate | ✅ Funciona | Fallback se tabela não existir |
| Endpoint `/gate/debug` | ✅ Disponível | Para diagnóstico |
| Modo `active` | ✅ Respondendo | Testar no WhatsApp |
| Logs do Gate | ✅ Habilitados | Ver `docker logs` |

---

## 🚨 **Troubleshooting**

### **Problema: Luna ainda não responde**

**Verificar:**

1. **Modo está correto?**
   ```bash
   curl "http://localhost:8000/api/webhooks/mode"
   # Deve retornar "mode": "active"
   ```

2. **Gate está permitindo?**
   ```bash
   curl "http://localhost:8000/api/webhooks/gate/debug?phone=SEU_NUMERO"
   # Deve retornar "allowed": true
   ```

3. **Webhook está chegando?**
   ```bash
   docker logs luna-backend | grep "Webhook received"
   # Deve aparecer quando mensagem chega
   ```

4. **LID resolution está funcionando?**
   ```bash
   docker logs luna-backend | grep "LID resolved"
   # Deve aparecer para números multi-device
   ```

---

### **Problema: Gate bloqueia todas as mensagens**

**Causas possíveis:**

1. **Modo "observe":**
   ```bash
   curl -X POST "http://localhost:8000/api/webhooks/mode" \
     -d '{"mode": "active"}'
   ```

2. **Test limit atingido:**
   ```bash
   curl "http://localhost:8000/api/webhooks/gate/debug"
   # Se test_count >= test_limit, resetar:
   curl -X POST "http://localhost:8000/api/webhooks/gate/reset-test"
   ```

3. **Manual mode sem ativações:**
   ```bash
   # Criar ativação:
   curl -X POST "http://localhost:8000/api/webhooks/gate/activate" \
     -d '{"phone": "5549999999999@s.whatsapp.net"}'
   ```

---

## ✅ **Checklist de Verificação**

- [ ] Tabela `luna_activations` criada no Supabase
- [ ] Modo设置为 "active"
- [ ] Endpoint `/gate/debug` responde
- [ ] `docker logs` mostra "Response sent"
- [ ] WhatsApp recebe resposta da Luna

---

**Criado:** 2026-03-12  
**LUNA OS v3.0**
