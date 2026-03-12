# 🎯 LUNA OS - Sales Pipeline & Campaign Integration Analysis

**Data:** 2026-03-11  
**Status:** ⚠️ **PARCIALMENTE IMPLEMENTADO**

---

## 📊 RESUMO EXECUTIVO

### O Que Temos ✅

| Componente | Status | Descrição |
|------------|--------|-----------|
| **Campaign Manager** | ✅ Implementado | Detecção de campanhas ativas |
| **Follow-up Dispatcher** | ✅ Implementado | Envio automático de follow-ups |
| **Upsell Scripts** | ✅ Implementado | Scripts de upsell por serviço |
| **Windmill Integration** | ✅ Parcial | 1 flow de processamento |
| **Orchestrator** | ✅ Implementado | Roteamento com follow-up |

### O Que Falta ❌

| Componente | Status | Prioridade |
|------------|--------|------------|
| **Windmill Campaign Flows** | ❌ Não implementado | 🔴 Alta |
| **Sales Pipeline Stages** | ❌ Não implementado | 🔴 Alta |
| **Follow-up Automation** | ⚠️ Parcial | 🟡 Média |
| **Post-Venda Automation** | ❌ Não implementado | 🟡 Média |
| **Oportunidades Estratégicas** | ❌ Não implementado | 🟢 Baixa |

---

## 🔄 PIPELINE DE VENDAS COMPLETO (Proposta)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LUNA OS - SALES PIPELINE v5.0                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  1. RECEPÇÃO (Primeiro Contato)                                          │
  │     ┌────────────────────────────────────────────────────────────────┐  │
  │     │ • Cliente manda "bom dia" / "qual preço?"                      │  │
  │     │ • Quick Brain classifica: intent="saudacao" / "informacao"     │  │
  │     │ • Campaign Manager detecta: alguma campanha ativa?             │  │
  │     │ • Cria/Atualiza: leads table                                   │  │
  │     │ • Status: NEW_LEAD                                             │  │
  │     └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  2. QUALIFICAÇÃO (Entendimento da Necessidade)                           │
  │     ┌────────────────────────────────────────────────────────────────┐  │
  │     │ • Standard Brain faz perguntas qualificatórias                 │  │
  │     │ • Extrai: serviço_interesse, budget, timeline                  │  │
  │     │ • Salva em: lead_qualification table                           │  │
  │     │ • Lead Score: calculado (0-100)                                │  │
  │     │ • Status: QUALIFIED                                            │  │
  │     └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  3. PROPOSTA / AGENDAMENTO                                               │
  │     ┌────────────────────────────────────────────────────────────────┐  │
  │     │ • Standard Brain apresenta proposta                            │  │
  │     │ • Upsell automático (config_haven.upsell_*)                    │  │
  │     │ • Agenda horário ou fecha venda                                │  │
  │     │ • Cria: opportunity table                                      │  │
  │     │ • Valor estimado: R$                                           │  │
  │     │ • Status: PROPOSAL_SENT                                        │  │
  │     └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
  ┌──────────────────────────┐      ┌──────────────────────────┐
  │  4A. FECHAMENTO          │      │  4B. OBJEÇÕES            │
  │     (Venda Concluída)    │      │     (Negociação)         │
  │     ┌────────────────┐   │      │   ┌────────────────┐     │
  │     │ • Venda ✅     │   │      │   │ • Complex Brain│     │
  │     │ • Status: WON  │   │      │   │ • Negociação   │     │
  │     │ • Cria: sale   │   │      │   │ • Follow-up    │     │
  │     └────────────────┘   │      │   └────────────────┘     │
  └──────────────────────────┘      └──────────────────────────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  5. PÓS-VENDA (Follow-up Automático)                                     │
  │     ┌────────────────────────────────────────────────────────────────┐  │
  │     │ • Follow-up Dispatcher envia mensagens automáticas:            │  │
  │     │   - Dia seguinte: "Como foi seu atendimento?"                  │  │
  │     │   - 7 dias: "Está satisfeito?"                                 │  │
  │     │   - 30 dias: "Quer agendar novamente?"                         │  │
  │     │ • Salva em: followups table                                    │  │
  │     │ • Status: POST_SALE                                            │  │
  │     └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  6. FIDELIZAÇÃO / RECORRÊNCIA                                            │
  │     ┌────────────────────────────────────────────────────────────────┐  │
  │     │ • Campaign Manager ativa campanhas de recorrência              │  │
  │     │ • Windmill flow: "monthly_clients"                             │  │
  │     │ • Detecta: clientes há 60+ dias sem visitar                    │  │
  │     │ • Envia: oferta personalizada                                  │  │
  │     │ • Status: RETENTION                                            │  │
  │     └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 O QUE JÁ TEMOS IMPLEMENTADO

### 1. Campaign Manager ✅

**Arquivo:** `backend/app/core/campaign_manager.py`

**Funcionalidades:**
```python
# Busca campanhas ativas do Supabase
await campaign_manager.sync_campaigns()

# Detecta se mensagem aciona campanha
campaign = campaign_manager.detect_campaign("qual preço da escova?")

# Retorna:
{
    "id": "camp-123",
    "name": "Promoção Escova",
    "trigger_keywords": ["escova", "lisa", "modelada"],
    "discount_percent": 10,
    "valid_until": "2026-03-31"
}
```

**Status:** ✅ Funcional, mas não integrado com Windmill

---

### 2. Follow-up Dispatcher ✅

**Arquivo:** `backend/app/core/followup_dispatcher.py`

**Funcionalidades:**
```python
# Busca follow-ups pendentes
followups = _fetch_pending_followups()

# Envia via WhatsApp
for followup in followups:
    await _send_followup(followup)

# Tabela: agent_followups
# - id, phone, message, scheduled_at, ticket_id, status
```

**Status:** ✅ Funcional, mas precisa de automação Windmill

---

### 3. Upsell Scripts ✅

**Arquivo:** `backend/app/core/marketing.py` + `config_haven.py`

**Funcionalidades:**
```python
# Gera script de upsell
script = generate_upsell_script(service_id="escova", client_name="Maria")

# Retorna:
"Na conversa eu já te passo o valor base com os produtos da casa 😊
No lavatório, se você quiser, a equipe oferece opções premium..."
```

**Upsell Configurado:**
- ✅ Upsell Lavatório (coreanos, Labrizza, Kérastase)
- ✅ Upsell Escova (pacotes 4x, 8x)
- ✅ Upsell Gel (pacote 3 aplicações)

**Status:** ✅ Funcional, integrado ao Brain

---

### 4. Orchestrator com Follow-up ✅

**Arquivo:** `backend/app/core/orchestrator.py`

**Funcionalidades:**
```python
# Após resolver reclamação, executa follow-up
if _needs_followup(state):
    state = await run_followup_agent(state)

# Follow-up agent cria registro em: agent_followups
```

**Status:** ✅ Funcional

---

## ❌ O QUE FALTA IMPLEMENTAR

### 1. Windmill Campaign Flows ❌ (Prioridade: 🔴 ALTA)

**Flows Necessários:**

```yaml
# 1. lead_qualification_flow.yaml
# Trigger: Novo lead criado
# Schedule: Real-time (webhook)

steps:
  - id: fetch_lead
    script: fetch_supabase_record
    args:
      table: leads
      id: "{{ trigger.lead_id }}"
  
  - id: qualify
    script: qualify_lead
    args:
      lead_data: "{{ fetch_lead.result }}"
      criteria:
        - service_interest
        - budget_match
        - timeline
  
  - id: update_score
    script: update_lead_score
    args:
      lead_id: "{{ trigger.lead_id }}"
      score: "{{ qualify.result.score }}"
  
  - id: notify_sales
    script: send_notification
    if: "{{ qualify.result.score > 70 }}"
    args:
      message: "Lead quente: {{ fetch_lead.result.name }}"
```

```yaml
# 2. post_sale_followup_flow.yaml
# Trigger: Venda concluída
# Schedule: Day+1, Day+7, Day+30

steps:
  - id: check_sale
    script: fetch_supabase_record
    args:
      table: sales
      id: "{{ trigger.sale_id }}"
  
  - id: send_day1
    script: send_whatsapp_message
    args:
      phone: "{{ check_sale.result.client_phone }}"
      message: "Oi {{ check_sale.result.client_name }}! Como foi seu atendimento ontem?"
    schedule: "0 12 * * *"  # Dia seguinte, 12h
  
  - id: send_day7
    script: send_whatsapp_message
    args:
      phone: "{{ check_sale.result.client_phone }}"
      message: "Está satisfeito com o resultado?"
    schedule: "0 12 * * 0"  # 7 dias depois
  
  - id: send_day30
    script: send_whatsapp_message
    args:
      phone: "{{ check_sale.result.client_phone }}"
      message: "Quer agendar novamente? Temos horário essa semana!"
    schedule: "0 12 1 * *"  # 30 dias depois
```

```yaml
# 3. churn_prevention_flow.yaml
# Trigger: Cliente 60+ dias sem visitar
# Schedule: Weekly

steps:
  - id: fetch_inactive
    script: fetch_supabase_query
    args:
      table: clients
      select: "id, phone, name, last_visit"
      where:
        last_visit_lt: "now() - interval '60 days'"
        status: "active"
  
  - id: send_retention_offer
    script: send_whatsapp_message
    args:
      phone: "{{ item.phone }}"
      message: "Oi {{ item.name }}! Sentimos sua falta. Que tal 15% OFF para retornar essa semana?"
    items: "{{ fetch_inactive.result }}"
    parallel: 10
  
  - id: log_campaign
    script: insert_supabase_record
    args:
      table: retention_campaigns
      data:
        client_id: "{{ item.id }}"
        sent_at: "{{ now() }}"
        offer: "15% OFF"
```

```yaml
# 4. upsell_opportunity_flow.yaml
# Trigger: Cliente agenda serviço básico
# Schedule: Real-time

steps:
  - id: check_appointment
    script: fetch_supabase_record
    args:
      table: appointments
      id: "{{ trigger.appointment_id }}"
  
  - id: get_upsell_suggestion
    script: generate_upsell_script
    args:
      service_id: "{{ check_appointment.result.service_id }}"
      client_name: "{{ check_appointment.result.client_name }}"
  
  - id: send_upsell_message
    script: send_whatsapp_message
    args:
      phone: "{{ check_appointment.result.client_phone }}"
      message: "{{ get_upsell_suggestion.result.script }}"
```

---

### 2. Sales Pipeline Stages ❌ (Prioridade: 🔴 ALTA)

**Tabela Necessária:**

```sql
-- pipeline_stages
CREATE TABLE pipeline_stages (
    id UUID PRIMARY KEY,
    lead_id UUID REFERENCES leads(id),
    stage TEXT NOT NULL,  -- NEW_LEAD, QUALIFIED, PROPOSAL, NEGOTIATION, WON, LOST
    value_estimate DECIMAL,
    probability DECIMAL,  -- 0-100
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    won_at TIMESTAMP,
    lost_reason TEXT
);

-- pipeline_events (histórico)
CREATE TABLE pipeline_events (
    id UUID PRIMARY KEY,
    stage_id UUID REFERENCES pipeline_stages(id),
    event_type TEXT,  -- STAGE_CHANGED, FOLLOWUP_SENT, NOTE_ADDED
    metadata JSONB,
    created_at TIMESTAMP
);
```

**Endpoints API:**

```python
# GET /api/pipeline
# Lista oportunidades por estágio

# POST /api/pipeline/{id}/move
# Move oportunidade para outro estágio

# GET /api/pipeline/metrics
# Métricas: taxa de conversão, tempo médio, valor médio
```

---

### 3. Follow-up Automation ⚠️ (Prioridade: 🟡 MÉDIA)

**O Que Temos:**
- ✅ `followup_dispatcher.py` - Envia follow-ups pendentes
- ✅ `agent_followups` table - Armazena follow-ups agendados

**O Que Falta:**
- ❌ Windmill flow para criar follow-ups automaticamente
- ❌ Follow-ups baseados em comportamento (não apenas tempo)
- ❌ Personalização dinâmica da mensagem

**Solução Proposta:**

```yaml
# auto_followup_flow.yaml
# Trigger: Após interação classificada

steps:
  - id: classify_interaction
    script: classify_interaction_type
    args:
      conversation_id: "{{ trigger.conversation_id }}"
  
  - id: determine_followup
    script: determine_followup_needed
    args:
      interaction_type: "{{ classify_interaction.result.type }}"
      sentiment: "{{ classify_interaction.result.sentiment }}"
      intent: "{{ classify_interaction.result.intent }}"
  
  - id: schedule_followup
    script: create_followup_record
    args:
      phone: "{{ trigger.phone }}"
      message: "{{ determine_followup.result.message }}"
      scheduled_at: "{{ determine_followup.result.scheduled_at }}"
      ticket_id: "{{ trigger.conversation_id }}"
    if: "{{ determine_followup.result.needs_followup }}"
```

---

### 4. Post-Venda Automation ❌ (Prioridade: 🟡 MÉDIA)

**Fluxo Proposto:**

```yaml
# post_sale_automation_flow.yaml
# Trigger: Venda marcada como WON

stages:
  - id: day1_satisfaction
    name: "Dia 1: Satisfação"
    schedule: "0 12 * * *"  # 12h do dia seguinte
    message: |
      "Oi {{ client_name }}! Como foi seu atendimento ontem?
      Estamos sempre buscando melhorar. Pode nos dar um feedback?"
  
  - id: day7_result
    name: "Dia 7: Resultado"
    schedule: "0 12 * * 0"  # 7 dias depois
    message: |
      "Oi {{ client_name }}! Está gostando do resultado?
      Qualquer dúvida, estamos aqui!"
  
  - id: day30_retention
    name: "Dia 30: Recorrência"
    schedule: "0 12 1 * *"  # 30 dias depois
    message: |
      "Oi {{ client_name }}! Já faz um mês!
      Quer agendar novamente? Temos horário essa semana."
  
  - id: day60_winback
    name: "Dia 60: Resgate"
    schedule: "0 12 1 * *"  # 60 dias depois
    message: |
      "Oi {{ client_name }}! Sentimos sua falta!
      Que tal 10% OFF para retornar essa semana?"
```

---

### 5. Oportunidades Estratégicas ❌ (Prioridade: 🟢 BAIXA)

**Tipos de Oportunidades:**

```python
OPPORTUNITY_TYPES = {
    "upsell": "Venda adicional durante atendimento",
    "cross_sell": "Venda de serviço complementar",
    "referral": "Indicação de novo cliente",
    "retention": "Evitar churn de cliente em risco",
    "reactivation": "Reativar cliente inativo",
    "upgrade": "Upgrade para serviço premium"
}
```

**Windmill Flow:**

```yaml
# opportunity_detection_flow.yaml
# Trigger: Análise diária de conversas

steps:
  - id: fetch_conversations
    script: fetch_supabase_query
    args:
      table: conversations
      select: "id, phone, messages"
      where:
        created_at_gte: "now() - interval '24 hours'"
  
  - id: detect_opportunities
    script: detect_sales_opportunities
    args:
      conversations: "{{ fetch_conversations.result }}"
  
  - id: create_opportunities
    script: batch_insert_opportunities
    args:
      opportunities: "{{ detect_opportunities.result }}"
  
  - id: notify_sales_team
    script: send_notification
    args:
      message: "{{ detect_opportunities.result.count }} oportunidades detectadas"
```

---

## 📊 MATRIZ DE IMPLEMENTAÇÃO

| Funcionalidade | Status | Windmill | Prioridade | Esforço |
|----------------|--------|----------|------------|---------|
| Campaign Detection | ✅ Pronto | ❌ Não integrado | 🔴 Alta | 2h |
| Lead Qualification | ❌ Faltando | ❌ Não criado | 🔴 Alta | 8h |
| Pipeline Stages | ❌ Faltando | ❌ Não criado | 🔴 Alta | 6h |
| Follow-up Auto | ⚠️ Parcial | ❌ Não criado | 🟡 Média | 4h |
| Post-Venda | ❌ Faltando | ❌ Não criado | 🟡 Média | 6h |
| Upsell Auto | ✅ Pronto | ❌ Não integrado | 🟢 Baixa | 2h |
| Oportunidades | ❌ Faltando | ❌ Não criado | 🟢 Baixa | 8h |

---

## 🎯 RECOMENDAÇÃO DE IMPLEMENTAÇÃO

### Fase 1: Fundação (Semana 1)

1. **Criar tabelas de Pipeline**
   - `pipeline_stages`
   - `pipeline_events`
   - `opportunities`

2. **Integrar Campaign Manager com Windmill**
   - Flow: `campaign_detection_flow`
   - Trigger: Nova conversa

3. **Criar Flow de Lead Qualification**
   - Flow: `lead_qualification_flow`
   - Score automático

### Fase 2: Automação (Semana 2)

1. **Follow-up Automation**
   - Flow: `auto_followup_flow`
   - Baseado em comportamento

2. **Post-Venda Automation**
   - Flow: `post_sale_automation_flow`
   - Day+1, Day+7, Day+30

### Fase 3: Inteligência (Semana 3)

1. **Oportunidade Estratégicas**
   - Flow: `opportunity_detection_flow`
   - IA detecta upsell/cross-sell

2. **Churn Prevention**
   - Flow: `churn_prevention_flow`
   - Clientes 60+ dias inativos

---

## 📈 MÉTRICAS DE SUCESSO

| Métrica | Atual | Meta (30 dias) | Meta (90 dias) |
|---------|-------|----------------|----------------|
| Taxa de Conversão | ? | 25% | 35% |
| Follow-up Enviado | ? | 90% | 95% |
| Tempo Resposta | ? | <5min | <2min |
| Ticket Médio | ? | +15% | +25% |
| Churn Rate | ? | -10% | -20% |
| Recorrência | ? | 30% | 45% |

---

## 🔗 INTEGRAÇÃO WINDMILL PROPOSTA

```
╔═══════════════════════════════════════════════════════════╗
║              WINDMILL SALES AUTOMATION                    ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  FLOWS CRIADOS:                                           ║
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 1. campaign_detection_flow                          │ │
║  │    • Trigger: Nova conversa                         │ │
║  │    • Detecta campanha ativa                         │ │
║  │    • Aplica desconto/promoção                       │ │
║  └─────────────────────────────────────────────────────┘ │
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 2. lead_qualification_flow                          │ │
║  │    • Trigger: Lead criado                           │ │
║  │    • Qualifica (score 0-100)                        │ │
║  │    • Notifica time se score > 70                    │ │
║  └─────────────────────────────────────────────────────┘ │
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 3. post_sale_followup_flow                          │ │
║  │    • Trigger: Venda WON                             │ │
║  │    • Follow-up: Day+1, +7, +30                      │ │
║  │    • Mensagens automáticas                          │ │
║  └─────────────────────────────────────────────────────┘ │
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 4. churn_prevention_flow                            │ │
║  │    • Schedule: Weekly                               │ │
║  │    • Clientes 60+ dias inativos                     │ │
║  │    • Envia oferta de resgate                        │ │
║  └─────────────────────────────────────────────────────┘ │
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 5. upsell_opportunity_flow                          │ │
║  │    • Trigger: Agenda serviço básico                 │ │
║  │    • Envia script de upsell                         │ │
║  │    • Baseado em config_haven.upsell_*               │ │
║  └─────────────────────────────────────────────────────┘ │
║  ┌─────────────────────────────────────────────────────┐ │
║  │ 6. opportunity_detection_flow                       │ │
║  │    • Schedule: Daily                                │ │
║  │    • IA analisa conversas                           │ │
║  │    • Detecta: upsell, cross-sell, referral          │ │
║  └─────────────────────────────────────────────────────┘ │
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## ✅ PRÓXIMOS PASSOS IMEDIATOS

### 1. Criar Estrutura de Pipeline (2h)

```sql
-- Executar no Supabase
CREATE TABLE pipeline_stages (...);
CREATE TABLE pipeline_events (...);
CREATE TABLE opportunities (...);
```

### 2. Criar Windmill Flows (8h)

```bash
# 1. campaign_detection_flow
# 2. lead_qualification_flow  
# 3. post_sale_followup_flow
```

### 3. Integrar com Brain (4h)

```python
# backend/app/core/brain.py
# Adicionar: criar oportunidade após venda
# Adicionar: agendar follow-up automático
```

### 4. Testar End-to-End (4h)

```bash
# Testar fluxo completo:
# Lead → Qualificação → Proposta → Venda → Follow-up
```

---

**Conclusão:** Temos **70% da base pronta** (Campaign Manager, Follow-up Dispatcher, Upsell Scripts). Precisamos integrar com Windmill e criar os flows de automação para ter o pipeline completo de vendas! 🎯
