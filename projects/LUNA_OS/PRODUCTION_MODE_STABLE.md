# 🚀 LUNA OS - Modo de Produção Estável

## ✅ **Problema Resolvido**

O modo da Luna voltava para "observe" após restart ou aleatoriamente.

**Causa:** Cache do `dynamic_settings` não era atualizado corretamente.

---

## 🔧 **Soluções Aplicadas**

### 1. **Refresh Automático do Cache**

**Arquivo:** `app/api/webhooks.py`

Sempre que o modo é alterado via `/mode`, o cache é refreshado automaticamente:

```python
# Forçar refresh do cache
from app.config import refresh_dynamic_settings
refresh_dynamic_settings()
```

---

### 2. **Endpoint de Refresh Manual**

**Novo endpoint:** `POST /api/webhooks/gate/refresh-cache`

```bash
curl -X POST "http://localhost:8000/api/webhooks/gate/refresh-cache" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Uso:** Quando o modo não atualizar imediatamente.

---

### 3. **Logs de Debug**

Endpoint `/mode` agora loga o valor lido:

```
📖 GET /mode: luna_mode=active (from dynamic_settings)
```

---

## 📋 **Comandos Úteis**

### **Ver Modo Atual:**

```bash
curl "http://localhost:8000/api/webhooks/mode" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Esperado:**
```json
{
  "mode": "active",
  "responding": true,
  "source": "dynamic_settings"
}
```

---

### **Mudar para Modo Produção:**

```bash
curl -X POST "http://localhost:8000/api/webhooks/mode" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: YOUR_KEY" \
  -d '{"mode": "active"}'
```

---

### **Forçar Refresh do Cache:**

```bash
curl -X POST "http://localhost:8000/api/webhooks/gate/refresh-cache" \
  -H "X-Admin-Key: YOUR_KEY"
```

---

### **Debug do Gate:**

```bash
curl "http://localhost:8000/api/webhooks/gate/debug?phone=5549999999999@s.whatsapp.net" \
  -H "X-Admin-Key: YOUR_KEY"
```

---

## 🔍 **Logs em Tempo Real:**

```bash
# Ver logs do gate/mode
docker logs -f luna-backend | grep -E "(mode|Mode|gate|Gate)"

# Ver logs de respostas
docker logs -f luna-backend | grep -E "(Response sent|GATE)"
```

---

## ✅ **Checklist: Luna Pronta para Produção**

- [ ] Modo设置为 "active"
  ```bash
  curl "http://localhost:8000/api/webhooks/mode"
  # Deve retornar "mode": "active"
  ```

- [ ] Tabela `luna_activations` criada (para modo manual)
  ```sql
  -- Executar no Supabase SQL Editor
  cat backend/scripts/sql/create_luna_activations_table.sql
  ```

- [ ] Webhook registrado na Evolution
  ```bash
  # Verificar na Evolution API
  curl "http://localhost:8081/webhook/find/Haven" \
    -H "apikey: YOUR_EVO_KEY"
  ```

- [ ] Testar resposta no WhatsApp
  ```bash
  # Enviar mensagem para o número do salão
  # Ver logs:
  docker logs -f luna-backend | grep "Response sent"
  ```

---

## 🐛 **Troubleshooting**

### **Problema: Modo volta para "observe"**

**Solução 1: Forçar refresh**
```bash
curl -X POST "http://localhost:8000/api/webhooks/gate/refresh-cache" \
  -H "X-Admin-Key: YOUR_KEY"
```

**Solução 2: Reiniciar backend**
```bash
docker restart luna-backend
sleep 10
curl -X POST "http://localhost:8000/api/webhooks/mode" \
  -d '{"mode": "active"}' \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: YOUR_KEY"
```

---

### **Problema: Luna não responde mesmo em modo active**

**Verificar:**

1. **Gate está permitindo?**
   ```bash
   curl "http://localhost:8000/api/webhooks/gate/debug?phone=SEU_NUMERO"
   # Deve retornar "allowed": true
   ```

2. **Webhook está chegando?**
   ```bash
   docker logs luna-backend | grep "Webhook received"
   # Deve aparecer quando mensagem chega
   ```

3. **LID resolution funcionando?**
   ```bash
   docker logs luna-backend | grep "LID resolved"
   # Deve aparecer para números multi-device
   ```

4. **Evolution está conectada?**
   ```bash
   curl "http://localhost:8000/api/health/status" \
     -H "X-Admin-Key: YOUR_KEY"
   # Deve retornar "evolution": {"status": "connected"}
   ```

---

## 📊 **Status Atual**

| Componente | Status | Notas |
|------------|--------|-------|
| Backend | ✅ Healthy | Rodando há 10+ minutos |
| Modo | ✅ Active | Respondendo |
| Cache | ✅ Estável | Refresh automático |
| Gate | ✅ Funcionando | Fallback se tabela não existir |
| Webhook | ✅ Registrado | Haven instance |

---

## 🎯 **Próximo Teste: WhatsApp**

1. **Enviar mensagem** para o número do salão
2. **Ver logs em tempo real:**
   ```bash
   docker logs -f luna-backend | grep -E "(Webhook|Gate|Response)"
   ```
3. **Esperar ver:**
   ```
   📩 Webhook received: messages.upsert
   🔍 LID resolved: ...
   💬 Processing: ...
   📤 Response sent | gate=active
   ```

---

**Criado:** 2026-03-12  
**LUNA OS v3.0**
