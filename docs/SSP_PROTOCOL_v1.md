# 📡 Secretaria Social Protocol v1.0 (SSP/1.0)

## Protocolo Aberto para Secretárias de IA

**Status:** Draft  
**Versão:** 1.0.0  
**Data:** 2026-03-12  
**Licença:** MIT (Open Source)

---

## 🎯 Visão Geral

SSP/1.0 é um protocolo aberto para padronizar a comunicação entre secretárias de IA e sistemas externos (WhatsApp, CRM, Calendar, Payment, Handoff).

### Por Que SSP/1.0?

**Problema Atual:**
- Cada secretaria de IA usa formato próprio
- Integrações são caóticas e frágeis
- Não há interoperabilidade entre sistemas
- Handoff entre IAs é impossível

**Solução SSP/1.0:**
- Formato canônico único
- Integrações padronizadas
- Interoperabilidade total
- Handoff IA-IA possível

---

## 📋 Casos de Uso

### 1. Agendamento de Consulta

```json
{
  "action": "schedule_appointment",
  "contact": {
    "id": "contact_123",
    "name": "João Silva",
    "phone": "+5511999999999",
    "email": "joao@example.com"
  },
  "appointment": {
    "service": "Consulta Inicial",
    "duration_minutes": 60,
    "preferred_datetime": "2026-03-15T14:00:00-03:00",
    "notes": "Primeira consulta"
  },
  "metadata": {
    "source": "whatsapp",
    "campaign": "google_ads",
    "ltv": 5000
  }
}
```

### 2. Handoff para Humano

```json
{
  "action": "handoff_to_human",
  "contact": {
    "id": "contact_123",
    "name": "Maria Santos"
  },
  "handoff": {
    "reason": "customer_requested",
    "priority": 7,
    "context_summary": "Cliente quer falar com atendente humano",
    "ai_attempts": 2,
    "last_ai_response": "Entendo, vou transferir você"
  },
  "conversation": {
    "id": "conv_456",
    "messages_count": 15,
    "sentiment": "frustrated"
  }
}
```

### 3. Envio de Invoice

```json
{
  "action": "send_invoice",
  "contact": {
    "id": "contact_123",
    "name": "João Silva",
    "email": "joao@example.com"
  },
  "invoice": {
    "id": "inv_789",
    "amount": 500.00,
    "currency": "BRL",
    "due_date": "2026-04-01",
    "items": [
      {
        "description": "Consulta",
        "quantity": 1,
        "unit_price": 500.00
      }
    ]
  },
  "payment": {
    "methods": ["pix", "credit_card", "boleto"],
    "pix_key": "luna@example.com"
  }
}
```

---

## 🔧 Especificação Técnica

### Endpoint Well-Known

```
GET /.well-known/ssp.json
```

**Resposta:**
```json
{
  "version": "1.0.0",
  "name": "LUNA Secretaria",
  "capabilities": [
    "schedule_appointment",
    "cancel_appointment",
    "send_invoice",
    "handoff_to_human",
    "get_contact_info",
    "update_contact_info"
  ],
  "channels": ["whatsapp", "instagram", "telegram"],
  "integrations": {
    "crm": "sankhya",
    "calendar": "google_calendar",
    "payment": "asaas",
    "handoff": "chatwoot"
  },
  "auth": {
    "type": "bearer_token",
    "endpoint": "/auth/token"
  },
  "webhook": {
    "endpoint": "/webhook/ssp",
    "events": [
      "appointment.scheduled",
      "appointment.cancelled",
      "invoice.sent",
      "handoff.created"
    ]
  }
}
```

---

## 📡 Ações Padrão

### 1. `schedule_appointment`

Agendar consulta.

**Request:**
```json
POST /api/v1/appointments
{
  "contact": { "id": "string", "name": "string", "phone": "string" },
  "service": "string",
  "duration_minutes": "number",
  "preferred_datetime": "ISO8601",
  "notes": "string"
}
```

**Response:**
```json
{
  "success": true,
  "appointment": {
    "id": "string",
    "datetime": "ISO8601",
    "professional": "string",
    "location": "string"
  },
  "confirmation_code": "string"
}
```

---

### 2. `cancel_appointment`

Cancelar consulta.

**Request:**
```json
POST /api/v1/appointments/{id}/cancel
{
  "reason": "string",
  "reschedule": {
    "preferred_datetime": "ISO8601"
  }
}
```

**Response:**
```json
{
  "success": true,
  "cancelled": true,
  "rescheduled": {
    "new_appointment_id": "string",
    "datetime": "ISO8601"
  }
}
```

---

### 3. `send_invoice`

Enviar invoice.

**Request:**
```json
POST /api/v1/invoices
{
  "contact": { "id": "string", "email": "string" },
  "amount": "number",
  "currency": "string",
  "due_date": "ISO8601",
  "items": [{"description": "string", "quantity": "number", "unit_price": "number"}]
}
```

**Response:**
```json
{
  "success": true,
  "invoice": {
    "id": "string",
    "url": "string",
    "pix_code": "string",
    "boleto_url": "string"
  }
}
```

---

### 4. `handoff_to_human`

Transferir para humano.

**Request:**
```json
POST /api/v1/handoffs
{
  "contact": { "id": "string", "name": "string" },
  "reason": "customer_requested|low_confidence|high_risk|complaint",
  "priority": "number (1-10)",
  "context_summary": "string",
  "conversation_id": "string"
}
```

**Response:**
```json
{
  "success": true,
  "handoff": {
    "id": "string",
    "assigned_to": "string",
    "estimated_wait_minutes": "number"
  }
}
```

---

### 5. `get_contact_info`

Obter informações do contato.

**Request:**
```json
GET /api/v1/contacts/{id}
```

**Response:**
```json
{
  "contact": {
    "id": "string",
    "name": "string",
    "phone": "string",
    "email": "string",
    "ltv": "number",
    "tags": ["string"],
    "preferences": {
      "tone": "string",
      "channel": "string"
    }
  },
  "history": {
    "total_appointments": "number",
    "total_invoices": "number",
    "last_interaction": "ISO8601"
  }
}
```

---

### 6. `update_contact_info`

Atualizar informações do contato.

**Request:**
```json
PUT /api/v1/contacts/{id}
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "preferences": {
    "tone": "string",
    "channel": "string"
  }
}
```

**Response:**
```json
{
  "success": true,
  "contact": {
    "id": "string",
    "updated_at": "ISO8601"
  }
}
```

---

## 🔐 Autenticação

### Bearer Token

```bash
# Obter token
POST /auth/token
{
  "api_key": "your_api_key"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}

# Usar token
GET /api/v1/contacts/123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## 📡 Webhooks

### Eventos Disponíveis

| Evento | Payload |
|--------|---------|
| `appointment.scheduled` | `{appointment_id, contact_id, datetime}` |
| `appointment.cancelled` | `{appointment_id, contact_id, reason}` |
| `invoice.sent` | `{invoice_id, contact_id, amount}` |
| `invoice.paid` | `{invoice_id, contact_id, amount}` |
| `handoff.created` | `{handoff_id, contact_id, reason}` |
| `handoff.accepted` | `{handoff_id, operator_id}` |
| `handoff.resolved` | `{handoff_id, resolution_notes}` |

### Configurar Webhook

```json
POST /api/v1/webhooks
{
  "url": "https://your-server.com/webhook",
  "events": ["appointment.scheduled", "invoice.paid"],
  "secret": "your_webhook_secret"
}
```

---

## 📊 Implementações de Referência

### LUNA Multi-Brain V2

**Implementação:**
```python
from brain.ssp import SSPServer

server = SSPServer(
    name="LUNA Secretaria",
    version="1.0.0",
    capabilities=["schedule_appointment", "handoff_to_human"]
)

@server.action("schedule_appointment")
def schedule(data):
    # Implementação
    return {"success": True, "appointment": {...}}
```

**Repo:** https://github.com/antigravity-kit/ssp-reference

---

## 🤝 Como Implementar

### Passo 1: Registrar Protocolo

```json
PUT /.well-known/ssp.json
{
  "version": "1.0.0",
  "name": "Sua Secretaria IA",
  "capabilities": ["schedule_appointment"]
}
```

### Passo 2: Implementar Ações

```python
# Python
from ssp import SSPHandler

class MinhaSecretaria(SSPHandler):
    @action("schedule_appointment")
    def schedule(self, data):
        # Sua implementação
        return {"success": True}
```

### Passo 3: Testar

```bash
# Testar endpoint
curl https://sua-secretaria.com/.well-known/ssp.json

# Testar ação
curl -X POST https://sua-secretaria.com/api/v1/appointments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"contact": {...}, "service": "Consulta"}'
```

---

## ✅ Checklist de Conformidade

Para ser SSP/1.0 compliant:

- [ ] Implementar `/.well-known/ssp.json`
- [ ] Suportar pelo menos 3 ações padrão
- [ ] Implementar autenticação Bearer Token
- [ ] Suportar webhooks
- [ ] Seguir formato canônico de requests/responses
- [ ] Documentar capacidades
- [ ] Testar com implementação de referência

---

## 🔗 Links

- **Repo Oficial:** https://github.com/antigravity-kit/ssp-protocol
- **Implementação LUNA:** `brain/ssp.py`
- **Test Suite:** `brain/tests/test_ssp.py`
- **Exemplos:** `examples/ssp-examples/`

---

## 📝 Changelog

### v1.0.0 (2026-03-12)

**Added:**
- 6 ações padrão
- Autenticação Bearer Token
- Webhooks
- Well-known endpoint
- Formato canônico

---

**SSP/1.0 - Open Source Protocol**  
**Licença:** MIT  
**Mantido por:** Antigravity Kit Community
