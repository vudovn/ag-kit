# 🛠️ Gemini Tools Integration — LUNA OS

> **Status**: ✅ CONCLUÍDO  
> **Data**: 2026-02-27  
> **Versão**: Gemini 3.1 MCP Style

---

## 📋 Visão Geral

Implementação de ferramentas estilo **MCP (Model Context Protocol)** para integração com **Google Gemini 3.1**.

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    GEMINI 3.1 API                            │
│  (Function Calling / Tool Use)                               │
└────────────────────┬────────────────────────────────────────┘
                     │ Tool Calls (JSON)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              GeminiToolExecutor                              │
│  • Parse tool calls                                          │
│  • Validate parameters                                       │
│  • Execute tools                                             │
│  • Return results                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Tool Registry                               │
│  • search_knowledge                                          │
│  • check_availability                                        │
│  • schedule_appointment                                      │
│  • send_whatsapp                                             │
│  • send_reminder                                             │
│  • get_client_history                                        │
│  • get_analytics                                             │
│  • get_system_status                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Ferramentas Disponíveis

### 1. **search_knowledge** (KNOWLEDGE)

Busca na base de conhecimento da Haven.

**Parâmetros:**
```json
{
  "query": "escova progressiva",
  "category": "servicos",  // opcional: servicos, faq, profissionais
  "limit": 5
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "query": "escova progressiva",
    "results": {
      "services": [{"name": "Escova", "price": 50}],
      "faq": [...],
      "professionals": [...]
    },
    "total_found": 3
  }
}
```

---

### 2. **check_availability** (SCHEDULING)

Verifica horários disponíveis na agenda.

**Parâmetros:**
```json
{
  "service": "Escova",
  "date": "2024-01-20",
  "time": "14:00",  // opcional
  "professional": "Ana"  // opcional
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "date": "2024-01-20",
    "available_times": ["08:00", "09:00", "14:00", "15:00"],
    "total_available": 8
  }
}
```

---

### 3. **schedule_appointment** (SCHEDULING)

Agenda um horário na Haven.

**Parâmetros:**
```json
{
  "client_id": "client_123",
  "service": "Unha de gel",
  "date": "2024-01-20",
  "time": "15:00",
  "professional": "Carla",
  "notes": "Primeira vez"
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "appointment": {...},
    "message": "Agendamento confirmado para 2024-01-20 às 15:00"
  }
}
```

---

### 4. **send_whatsapp** (COMMUNICATION)

Envia mensagem via WhatsApp (Evolution API).

**Parâmetros:**
```json
{
  "phone": "5511999999999",
  "message": "Olá! Confirme seu agendamento.",
  "instance": "haven"
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "message": "Mensagem enviada com sucesso",
    "phone": "5511999999999",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

---

### 5. **send_reminder** (COMMUNICATION)

Envia lembrete de agendamento.

**Parâmetros:**
```json
{
  "appointment_id": "apt_123",
  "reminder_type": "confirmation"  // confirmation, reminder, followup
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "message": "Lembrete enviado",
    "phone": "5511999999999"
  }
}
```

---

### 6. **get_client_history** (ANALYTICS)

Obtém histórico completo do cliente.

**Parâmetros:**
```json
{
  "phone": "5511999999999",
  "days": 90
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "client": {...},
    "history": {
      "total_conversations": 5,
      "total_appointments": 3,
      "services_done": ["Escova", "Unha"]
    },
    "recent_conversations": [...],
    "engagement_score": 75.0
  }
}
```

---

### 7. **get_analytics** (ANALYTICS)

Obtém métricas de negócio.

**Parâmetros:**
```json
{
  "metric": "appointments",  // revenue, appointments, satisfaction
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "metric": "appointments",
    "total": 45,
    "by_status": {
      "confirmed": 30,
      "completed": 10,
      "cancelled": 5
    }
  }
}
```

---

### 8. **get_system_status** (SYSTEM)

Obtém status dos componentes.

**Parâmetros:**
```json
{
  "component": null  // all, brain, memory, evolution
}
```

**Retorno:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2024-01-15T10:30:00",
    "components": {
      "brain": {"status": "healthy"},
      "memory": {"status": "healthy"},
      "evolution": {"status": "healthy"}
    },
    "overall": "healthy"
  }
}
```

---

## 🔧 Como Usar

### 1. **Uso Direto**

```python
from app.tools.gemini_tools import search_knowledge, SearchKnowledgeParams

result = await search_knowledge(
    SearchKnowledgeParams(query="escova", limit=5)
)

print(result.data)
```

### 2. **Via Gemini Executor**

```python
from app.tools.gemini_tools import gemini_executor

result = await gemini_executor.execute_tool_call(
    tool_name="search_knowledge",
    tool_args={"query": "escova", "limit": 5}
)

print(result)
```

### 3. **Listar Ferramentas**

```python
from app.tools.gemini_tools import registry

tools = registry.list_tools()
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")
```

---

## 🧪 Testes

```bash
cd LUNA_OS/backend

# Rodar testes das ferramentas
pytest tests/test_gemini_tools.py -v

# Com coverage
pytest tests/test_gemini_tools.py --cov=app.tools
```

---

## 📊 Schema Gemini API

Para configurar function calling na API do Gemini:

```python
from app.tools.gemini_tools import gemini_executor

tools_schema = gemini_executor.get_gemini_tools_schema()

# Usar na chamada Gemini
response = gemini_client.generate_content(
    messages=messages,
    tools=[
        {
            "function_declarations": tools_schema
        }
    ]
)
```

---

## 🎯 Categorias de Ferramentas

| Categoria | Ferramentas | Descrição |
|-----------|-------------|-----------|
| **KNOWLEDGE** | search_knowledge | Busca em serviços, FAQ, profissionais |
| **SCHEDULING** | check_availability, schedule_appointment | Agenda e horários |
| **COMMUNICATION** | send_whatsapp, send_reminder | Mensagens e lembretes |
| **ANALYTICS** | get_client_history, get_analytics | Métricas e histórico |
| **SYSTEM** | get_system_status | Saúde do sistema |

---

## 🔐 Tratamento de Erros

Todas as ferramentas seguem padrão MCT:

```python
{
  "success": false,
  "error": "Error message",
  "status": "error",  // success, error, timeout, not_found
  "execution_time_ms": 150
}
```

### Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Timeout` | Execução > 30s | Aumentar timeout_seconds |
| `Validation error` | Parâmetros inválidos | Validar schema Pydantic |
| `Tool not found` | Nome incorreto | Usar registry.list_tools() |

---

## 🚀 Exemplo Completo

```python
import asyncio
from app.tools.gemini_tools import (
    gemini_executor,
    search_knowledge,
    check_availability,
    schedule_appointment,
)

async def main():
    # 1. Buscar serviço
    search_result = await search_knowledge({
        "query": "manicure",
        "limit": 3
    })
    
    # 2. Verificar disponibilidade
    avail_result = await check_availability({
        "service": "Manicure",
        "date": "2024-01-20"
    })
    
    # 3. Agendar
    schedule_result = await schedule_appointment({
        "client_id": "client_123",
        "service": "Manicure",
        "date": "2024-01-20",
        "time": avail_result.data["available_times"][0]
    })
    
    print(f"Agendado: {schedule_result.data}")

asyncio.run(main())
```

---

## 📚 Próximos Passos

1. ✅ Implementar ferramentas básicas
2. ✅ Adicionar testes unitários
3. 🔄 Integrar com Gemini API (function calling)
4. 🔄 Adicionar mais ferramentas (pagamentos, feedback)
5. 🔄 Implementar caching de resultados
6. 🔄 Adicionar rate limiting

---

## 🔗 Referências

- [Gemini Function Calling](https://ai.google.dev/docs/function_calling)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Pydantic Validation](https://docs.pydantic.dev/)

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**
