# 🌬️ LUNA Automation Hub - Gerencie Tudo sem Sair do LUNA!

**Data:** 2026-03-11  
**Status:** ✅ **IMPLEMENTADO**

---

## 🎯 VISÃO GERAL

Agora você pode **criar, editar e gerenciar** todas as automações do Windmill **diretamente da interface do LUNA**, sem precisar acessar o Windmill separadamente!

```
╔═══════════════════════════════════════════════════════════╗
║              LUNA AUTOMATION HUB                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  📝 CRIAR                                                 ║
║     • Scripts Python/JS                                   ║
║     • Workflows (Flows)                                   ║
║     • Agendamentos (Schedules)                            ║
║     • Recursos (Resources)                                ║
║                                                           ║
║  ▶️ EXECUTAR                                              ║
║     • Rodar scripts imediatamente                         ║
║     • Executar workflows                                  ║
║     • Agendar para depois                                 ║
║                                                           ║
║  📊 MONITORAR                                             ║
║     • Ver execuções em tempo real                         ║
║     • Ver logs de jobs                                    ║
║     • Ver histórico                                       ║
║                                                           ║
║  ⚙️ GERENCIAR                                             ║
║     • Editar scripts/flows                                ║
║     • Ativar/desativar schedules                          ║
║     • Deletar recursos                                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 📁 ARQUIVOS CRIADOS

### Backend

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `backend/app/integrations/windmill_client.py` | Cliente API Windmill | ✅ |
| `backend/app/api/windmill_management.py` | Endpoints de automação | ✅ |
| `backend/app/main.py` | Router registrado | ✅ |

### Frontend (Em Implementação)

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `frontend/app/automations/page.tsx` | Dashboard principal | 🚧 |
| `frontend/app/automations/scripts/page.tsx` | Gerenciar scripts | 🚧 |
| `frontend/app/automations/flows/page.tsx` | Gerenciar flows | 🚧 |
| `frontend/app/automations/schedules/page.tsx` | Gerenciar schedules | 🚧 |
| `frontend/app/automations/jobs/page.tsx` | Monitorar jobs | 🚧 |

---

## 🔌 API ENDPOINTS

### Scripts

```bash
# Listar scripts
GET /api/windmill/scripts

# Criar script
POST /api/windmill/scripts/create
{
  "path": "u/admin/my_script",
  "content": "def main():\n    return 'Hello!'",
  "language": "python3",
  "summary": "Meu script",
  "description": "Descrição detalhada"
}

# Obter script
GET /api/windmill/scripts/u/admin/my_script

# Atualizar script
POST /api/windmill/scripts/u/admin/my_script/update
{
  "content": "def main():\n    return 'Updated!'",
  "deployment_message": "Updated version"
}

# Executar script
POST /api/windmill/scripts/u/admin/my_script/run
{
  "args": {"param1": "value1"},
  "scheduled_for": "2026-03-12T10:00:00Z"  # Opcional
}

# Deletar script
DELETE /api/windmill/scripts/u/admin/my_script
```

### Flows (Workflows)

```bash
# Listar flows
GET /api/windmill/flows

# Criar flow
POST /api/windmill/flows/create
{
  "path": "u/admin/my_flow",
  "value": {
    "steps": [
      {
        "id": "step1",
        "script": "my_script",
        "args": {}
      }
    ]
  },
  "summary": "Meu workflow",
  "description": "Descrição do flow"
}

# Executar flow
POST /api/windmill/flows/u/admin/my_flow/run
{
  "args": {"param1": "value1"}
}
```

### Schedules (Agendamentos)

```bash
# Listar schedules
GET /api/windmill/schedules

# Criar schedule
POST /api/windmill/schedules/create
{
  "path": "u/admin/daily_reminder",
  "schedule": "0 9 * * *",  # Cron: Diário às 9h
  "timezone": "America/Sao_Paulo",
  "flow_path": "u/admin/my_flow",
  "args": {},
  "enabled": true,
  "summary": "Lembrete diário"
}

# Ativar/Desativar
POST /api/windmill/schedules/u/admin/daily_reminder/toggle?enabled=false

# Deletar
DELETE /api/windmill/schedules/u/admin/daily_reminder
```

### Jobs (Execuções)

```bash
# Listar jobs
GET /api/windmill/jobs?limit=50&status=running

# Obter job
GET /api/windmill/jobs/{job_id}

# Cancelar job
POST /api/windmill/jobs/{job_id}/cancel

# Ver logs
GET /api/windmill/jobs/{job_id}/logs
```

### Resources (Recursos)

```bash
# Listar resources
GET /api/windmill/resources

# Criar resource
POST /api/windmill/resources/create
{
  "path": "u/admin/my_credentials",
  "value": {"api_key": "secret"},
  "resource_type": "credentials",
  "description": "Minhas credenciais"
}

# Obter resource
GET /api/windmill/resources/u/admin/my_credentials

# Deletar
DELETE /api/windmill/resources/u/admin/my_credentials
```

---

## 🖥️ INTERFACE DO USUÁRIO

### Dashboard Principal

```
╔═══════════════════════════════════════════════════════════╗
║  🌬️ LUNA AUTOMATION HUB                                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        ║
║  │   SCRIPTS   │ │    FLOWS    │ │ SCHEDULES   │        ║
║  │     15      │ │     8       │ │     12      │        ║
║  │  ▶️ Criar    │ │  ▶️ Criar    │ │  ▶️ Criar    │        ║
║  └─────────────┘ └─────────────┘ └─────────────┘        ║
║                                                           ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │  JOBS RECENTES                                  │    ║
║  ├─────────────────────────────────────────────────┤    ║
║  │  ✅ daily_conversation_processor  2min ago      │    ║
║  │  ✅ appointment_reminder         15min ago      │    ║
║  │  ⏳ post_sale_followup           Running...     │    ║
║  │  ❌ upsell_detection             Failed         │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                           ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │  HEALTH STATUS                                  │    ║
║  │  🟢 Windmill: Healthy                           │    ║
║  │  🟢 Workers: 10 online                          │    ║
║  │  🟢 Database: Connected                         │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Criar Script

```
╔═══════════════════════════════════════════════════════════╗
║  📝 CRIAR NOVO SCRIPT                                     ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Path: u/admin/[my_script]                                ║
║                                                           ║
║  Language: [Python 3 ▼]                                   ║
║                                                           ║
║  Summary: [Meu script de automação]                       ║
║                                                           ║
║  Description:                                             ║
║  ┌───────────────────────────────────────────────────┐  ║
║  │ Descrição detalhada do que o script faz...        │  ║
║  │                                                   │  ║
║  └───────────────────────────────────────────────────┘  ║
║                                                           ║
║  Content:                                                 ║
║  ┌───────────────────────────────────────────────────┐  ║
║  │ # @windmill/script                                │  ║
║  │ def main(name: str = "World"):                    │  ║
║  │     return f"Hello {name}!"                       │  ║
║  │                                                   │  ║
║  │                                                   │  ║
║  └───────────────────────────────────────────────────┘  ║
║                                                           ║
║  [💾 Salvar]  [▶️ Testar]  [❌ Cancelar]                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Criar Flow (Workflow)

```
╔═══════════════════════════════════════════════════════════╗
║  🔄 CRIAR NOVO WORKFLOW                                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Path: u/admin/[my_workflow]                              ║
║                                                           ║
║  Summary: [Processamento de Conversas]                    ║
║                                                           ║
║  Steps:                                                   ║
║  ┌───────────────────────────────────────────────────┐  ║
║  │  + Adicionar Step                                 │  ║
║  │                                                   │  ║
║  │  Step 1: fetch_conversations                      │  ║
║  │    Script: [fetch_supabase_query ▼]               │  ║
║  │    Args: {table: "conversations"}                 │  ║
║  │    [✏️] [🗑️]                                      │  ║
║  │                                                   │  ║
║  │  Step 2: process_all                              │  ║
║  │    Script: [process_conversation ▼]               │  ║
║  │    Args: {force: false}                           │  ║
║  │    [✏️] [🗑️]                                      │  ║
║  └───────────────────────────────────────────────────┘  ║
║                                                           ║
║  [💾 Salvar]  [▶️ Testar]  [❌ Cancelar]                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Criar Schedule (Agendamento)

```
╔═══════════════════════════════════════════════════════════╗
║  ⏰ CRIAR NOVO AGENDAMENTO                                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Path: u/admin/[daily_reminder]                           ║
║                                                           ║
║  Type: [Flow ▼]  [Script ▼]                               ║
║                                                           ║
║  Flow: [u/admin/my_flow ▼]                                ║
║                                                           ║
║  Cron Expression: [0 9 * * *]                             ║
║  ┌───────────────────────────────────────────────────┐  ║
║  │  ┌─┬─┬─┬─┬─┐                                      │  ║
║  │  ││ │ │ │ │  Minuto (0-59)                        │  ║
║  │  ││ │ │ │ └─ Hora (0-23)                          │  ║
║  │  ││ │ │ └─── Dia do mês (1-31)                    │  ║
║  │  ││ │ └───── Mês (1-12)                           │  ║
║  │  ││ └─────── Dia da semana (0-6)                  │  ║
║  │  └┴─┴─┴─┴─┘                                       │  ║
║  │                                                   │  ║
║  │  Exemplos:                                        │  ║
║  │  • 0 9 * * *     → Diário às 9h                   │  ║
║  │  • 0 */2 * * *   → A cada 2 horas                 │  ║
║  │  • 0 9 * * 1     → Segunda às 9h                  │  ║
║  └───────────────────────────────────────────────────┘  ║
║                                                           ║
║  Timezone: [America/Sao_Paulo ▼]                          ║
║  Enabled: [✓]                                             ║
║                                                           ║
║  [💾 Salvar]  [▶️ Testar]  [❌ Cancelar]                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Monitorar Jobs

```
╔═══════════════════════════════════════════════════════════╗
║  📊 JOBS - EXECUÇÕES                                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Filter: [All ▼]  [Running] [Success] [Failed]           ║
║                                                           ║
║  ┌───────────────────────────────────────────────────┐  ║
║  │ ID       │ Script/Flow      │ Status │ Time      │  ║
║  ├───────────────────────────────────────────────────┤  ║
║  │ abc123   │ daily_processor  │ ✅     │ 2min ago  │  ║
║  │ def456   │ appointment_rem  │ ⏳     │ Running   │  ║
║  │ ghi789   │ upsell_detect    │ ❌     │ 1h ago    │  ║
║  └───────────────────────────────────────────────────┘  ║
║                                                           ║
║  Selected: abc123                                         ║
║  [📋 Ver Logs] [❌ Cancelar] [🔄 Reexecutar]             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🚀 COMO USAR

### 1. Acessar Dashboard

```
http://localhost:3000/automations
```

### 2. Criar Script

1. Clique em **Scripts** → **Criar**
2. Preencha path, linguagem, conteúdo
3. Clique em **Salvar**
4. Teste com **▶️ Executar**

### 3. Criar Workflow

1. Clique em **Flows** → **Criar**
2. Defina path e descrição
3. Adicione steps (scripts)
4. Configure args de cada step
5. **Salvar** e **Testar**

### 4. Agendar Execução

1. Clique em **Schedules** → **Criar**
2. Selecione Script ou Flow
3. Defina expressão cron
4. **Salvar**

### 5. Monitorar

1. Clique em **Jobs**
2. Veja execuções em tempo real
3. Clique para ver logs
4. Cancele se necessário

---

## 📋 EXEMPLOS PRÁTICOS

### Exemplo 1: Criar Script de Lembrete

```python
# Path: u/admin/appointment_reminder
# Language: python3

from datetime import datetime, timedelta

def main(hours_before: int = 24):
    """
    Envia lembretes de agendamento.
    """
    # Buscar agendamentos
    # Enviar WhatsApp
    # Retornar resumo
    
    return {
        "sent": 25,
        "failed": 2,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Exemplo 2: Criar Workflow de Campanha

```yaml
# Path: u/admin/campaign_send
# Summary: Envio de campanha

steps:
  - id: fetch_clients
    script: fetch_supabase_query
    args:
      table: clients
      where: {status: "active"}
  
  - id: send_messages
    script: send_campaign_message
    args:
      clients: "{{ fetch_clients.result }}"
      campaign_id: "camp-mulher-2026"
  
  - id: consolidate
    script: |
      def main(results):
          return {
              "total": len(results),
              "sent": sum(1 for r in results if r.success)
          }
    args:
      results: "{{ send_messages.results }}"

outputs:
  summary: "{{ consolidate.result }}"
```

### Exemplo 3: Agendar Workflow

```
Path: u/admin/campaign_daily
Flow: u/admin/campaign_send
Schedule: 0 10 * * *  (Diário às 10h)
Timezone: America/Sao_Paulo
Enabled: ✓
```

---

## 🔗 INTEGRAÇÕES

### Supabase

```python
# Resources → Credenciais Supabase
{
  "path": "u/admin/supabase_credentials",
  "value": {
    "url": "https://xxx.supabase.co",
    "key": "eyJhbGc..."
  },
  "resource_type": "credentials"
}
```

### Evolution API

```python
# Resources → Credenciais WhatsApp
{
  "path": "u/admin/evolution_credentials",
  "value": {
    "url": "http://luna-evo-api:8080",
    "apikey": "mothership_master_2026",
    "instance": "haven"
  }
}
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Backend
- [x] Windmill Client
- [x] API Endpoints
- [x] Router registrado
- [x] Autenticação

### Frontend
- [ ] Dashboard principal
- [ ] Página de Scripts
- [ ] Página de Flows
- [ ] Página de Schedules
- [ ] Página de Jobs
- [ ] Editor de código
- [ ] Builder de flows
- [ ] Cron builder

### Integração
- [ ] Testar CRUD scripts
- [ ] Testar CRUD flows
- [ ] Testar CRUD schedules
- [ ] Testar execução de jobs
- [ ] Testar logs

---

**Implementado:** 2026-03-11  
**Versão:** 3.0 (Automation Hub)  
**Próximo:** Implementar UI frontend
