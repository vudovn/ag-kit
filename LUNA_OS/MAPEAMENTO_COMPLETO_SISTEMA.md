# 🗺️ LUNA OS - MAPEAMENTO COMPLETO DO SISTEMA

**Data:** 2026-03-01  
**Versão:** 3.0  
**Status:** ✅ **MAPEADO COMPLETAMENTE**

---

## 1. ESTRUTURA DE ARQUIVOS COMPLETA

### 📁 Visão Geral

```
LUNA_OS/
├── backend/                          # Backend Python (FastAPI)
│   ├── app/
│   │   ├── api/                      # 12 endpoints API
│   │   │   ├── webhooks.py           # Webhook Evolution API
│   │   │   ├── conversations.py      # Listagem de conversas
│   │   │   ├── clients.py            # Gestão de clientes
│   │   │   ├── analytics_super.py    # Analytics avançado
│   │   │   ├── campaigns.py          # Campanhas
│   │   │   ├── knowledge.py          # Base de conhecimento
│   │   │   ├── settings.py           # Configurações
│   │   │   ├── health.py             # Health checks
│   │   │   ├── dojo.py               # Dojo Arena API
│   │   │   ├── dojo_simulator.py     # Dojo Simulator API (NOVO)
│   │   │   ├── brain.py              # Brain simulator
│   │   │   └── evolution_proxy.py    # Proxy Evolution
│   │   │
│   │   ├── core/                     # Core Business Logic
│   │   │   ├── brain.py              # 835 linhas - Cérebro LUNA
│   │   │   ├── memory.py             # 582 linhas - Gestão memória
│   │   │   ├── scheduler.py          # Scheduler agendamentos
│   │   │   ├── evolution.py          # Integração WhatsApp
│   │   │   ├── campaign_manager.py   # Gestão campanhas
│   │   │   ├── resilience.py         # Resiliência e retry
│   │   │   ├── config_haven.py       # Configurações Haven
│   │   │   └── schemas_brain.py      # Schemas de dados
│   │   │
│   │   ├── modules_v3/               # Módulos Inteligentes (NOVO)
│   │   │   ├── conversation_intelligence/  # IA de análise
│   │   │   │   ├── agents/           # 8 agentes especializados
│   │   │   │   │   ├── extractor_agent.py
│   │   │   │   │   ├── psychology_agent.py
│   │   │   │   │   ├── sales_agent.py
│   │   │   │   │   ├── behavior_agent.py
│   │   │   │   │   ├── insights_agent.py
│   │   │   │   │   ├── storage_agent.py
│   │   │   │   │   ├── learning_agent.py
│   │   │   │   │   └── coordinator_agent.py
│   │   │   │   ├── knowledge/        # Frameworks psicologia/vendas
│   │   │   │   └── tests/
│   │   │   │
│   │   │   ├── agenda_viva/          # Otimização agenda
│   │   │   ├── ai_coach/             # Coaching IA
│   │   │   ├── churn_detector/       # Detecção churn
│   │   │   ├── heat_map/             # Mapa de calor
│   │   │   ├── mystery_shopper/      # Mystery shopper
│   │   │   ├── orquestrador/         # Orquestração
│   │   │   ├── revenue_optimizer/    # Otimização receita
│   │   │   └── simulador/            # Simulador
│   │   │
│   │   ├── dojo/                     # Dojo Arena
│   │   │   ├── personas.py           # 8 personas
│   │   │   ├── scenarios.py          # 15 cenários
│   │   │   ├── metrics.py            # Métricas de avaliação
│   │   │   └── simulator.py          # Simulador (NOVO)
│   │   │
│   │   ├── integrations/             # Integrações Externas
│   │   │   ├── supabase_client.py    # Supabase (DB)
│   │   │   ├── evolution.py          # Evolution API (WhatsApp)
│   │   │   ├── openrouter.py         # OpenRouter (LLMs)
│   │   │   ├── anthropic.py          # Anthropic (Claude)
│   │   │   ├── belasis.py            # Belasis ERP (agendamentos)
│   │   │   └── wascript.py           # WAScript CRM
│   │   │
│   │   ├── knowledge/                # Base de Conhecimento
│   │   │   ├── obsidian_vault/       # 1,041 arquivos Markdown
│   │   │   │   ├── _Active/
│   │   │   │   │   ├── 00-INDEX/
│   │   │   │   │   ├── 01-CRM/
│   │   │   │   │   │   ├── Clients/        (758 clientes)
│   │   │   │   │   │   └── Journals/       (204 journals)
│   │   │   │   │   ├── 02-KNOWLEDGE/
│   │   │   │   │   │   ├── Services/       (38 serviços)
│   │   │   │   │   │   ├── FAQs/           (4 FAQs)
│   │   │   │   │   │   └── Business-Info/  (Profissionais, Regras)
│   │   │   │   │   ├── 03-INTELLIGENCE/
│   │   │   │   │   └── 04-SYSTEM/
│   │   │   │   │       ├── Templates/      (5 templates)
│   │   │   │   │       ├── Prompts/        (2 prompts)
│   │   │   │   │       ├── Dashboards/     (2 dashboards)
│   │   │   │   │       └── Workflows/      (19 workflows Copilot)
│   │   │   │   └── Intelligence/
│   │   │   │
│   │   │   ├── data/
│   │   │   │   ├── haven.json        # Dados Haven (38 serviços, 4 FAQs)
│   │   │   │   └── haven_updated.json
│   │   │   └── loader.py             # Carregamento KB
│   │   │
│   │   ├── scripts/                  # 40+ scripts utilitários
│   │   │   ├── whatsapp_extraction.py    # Extração WhatsApp (NOVO)
│   │   │   ├── seed_haven.py             # Seed dados
│   │   │   ├── batch_dojo_test.py        # Testes Dojo
│   │   │   ├── dojo_historico_real.py    # Dojo com dados reais
│   │   │   ├── analyze_conversations.py  # Análise conversas
│   │   │   └── ... (36+ scripts)
│   │   │
│   │   ├── config.py               # Configurações
│   │   ├── main.py                 # Ponto de entrada
│   │   └── schemas.py              # Schemas Pydantic
│   │
│   ├── tests/                      # Testes unitários
│   ├── venv/                       # Virtual environment
│   ├── Dockerfile
│   └── requirements.txt            # 30+ dependências
│
├── frontend/                       # Frontend Next.js 14
│   ├── app/
│   │   ├── page.tsx                # Dashboard principal
│   │   ├── layout.tsx              # Layout root
│   │   ├── providers.tsx           # Context providers
│   │   ├── dojo/
│   │   │   └── page.tsx            # Dojo Arena (100% funcional)
│   │   ├── conversations/          # Listagem conversas
│   │   ├── clients/                # Gestão clientes
│   │   ├── analytics-super/        # Analytics avançado
│   │   ├── campaigns/              # Campanhas
│   │   ├── knowledge/              # Base conhecimento
│   │   ├── settings/               # Configurações
│   │   ├── brain/                  # Simulador Brain
│   │   ├── whatsapp/               # Gestão WhatsApp
│   │   ├── connections/            # Status conexões
│   │   ├── intelligence/           # Intelligence (NOVO)
│   │   └── persona/                # Gestão personas
│   │
│   ├── components/
│   │   ├── Sidebar.tsx
│   │   ├── PageShell.tsx
│   │   ├── MetricCard.tsx
│   │   ├── ConversionChart.tsx
│   │   ├── HourlyChart.tsx
│   │   └── TopServicesChart.tsx
│   │
│   ├── lib/
│   │   └── api.ts                  # Cliente API
│   │
│   ├── Dockerfile
│   ├── package.json                # 20+ dependências
│   └── next.config.js
│
├── docker-compose.yml              # Orquestração Docker
├── .env                            # Variáveis ambiente
├── task.md                         # Task tracker
└── docs/                           # 80+ documentos técnicos
```

---

## 2. FLUXO DE DADOS - JORNADA DA MENSAGEM

### 📱 WhatsApp → LUNA → WhatsApp

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CLIENTE envia mensagem no WhatsApp                           │
│    "Oi, quero agendar uma escova para amanhã"                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Evolution API recebe mensagem                                │
│    - Instância: haven                                           │
│    - Porta: 8081                                                │
│    - Formato: JSON webhook                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ Webhook POST
                         │ /api/webhooks/evolution
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Backend LUNA (FastAPI) processa                              │
│    a) Sanitização (resilience.py)                               │
│    b) Extrai: phone, name, content                              │
│    c) Verifica modo (observe/active)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Brain Pipeline (brain.py - 5 camadas)                        │
│                                                                 │
│    CAMADA 1: Classificação Intenções                            │
│    - Pattern matching (INTENT_PATTERNS)                         │
│    - Detecta: "agendar" → IntentType.AGENDAR                    │
│    - Confiança: 0.95                                            │
│                                                                 │
│    CAMADA 2: Extração Dados                                     │
│    - Serviço: "escova"                                          │
│    - Data: "amanhã" → 2026-03-02                                │
│    - Horário: (não informado)                                   │
│    - Profissional: (não informado)                              │
│                                                                 │
│    CAMADA 3: Context Building (RAG)                             │
│    - Busca histórico no Supabase (memory.py)                    │
│    - Busca serviços em haven.json                               │
│    - Busca profissionais em config_haven.py                     │
│                                                                 │
│    CAMADA 4: System Prompt                                      │
│    - Monta prompt com:                                          │
│      * Contexto da conversa                                     │
│      * Dados extraídos                                          │
│      * Regras de negócio                                        │
│      * Personalidade LUNA                                       │
│                                                                 │
│    CAMADA 5: LLM (OpenRouter)                                   │
│    - Modelo: google/gemini-2.0-flash-001 (quick)                │
│    - Ou: anthropic/claude-3.5-sonnet (complex)                  │
│    - Gera resposta natural                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Scheduler (scheduler.py)                                     │
│    - Verifica se é agendamento                                  │
│    - Valida dados necessários                                   │
│    - Se faltam dados: pede complemento                          │
│    - Se completo: consulta Belasis/Evolution                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Memory Manager (memory.py)                                   │
│    - Salva mensagem inbound no Supabase                         │
│    - Atualiza conversation                                      │
│    - Atualiza client profile                                    │
│    - Extrai dados para extracted_data                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. Resposta enviada via Evolution API                           │
│    POST /message/sendText/haven                                 │
│    {                                                            │
│      "number": "5549991112233",                                 │
│      "text": "Oi! Tenho horários amanhã. Qual horário prefere?" │
│    }                                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. Cliente recebe resposta no WhatsApp                          │
│    "Oi! Tenho horários amanhã. Qual horário prefere?"           │
└─────────────────────────────────────────────────────────────────┘
```

### 💾 Onde fica gravado

| Dado | Tabela Supabase | Local |
|------|-----------------|-------|
| **Cliente** | `clients` | Supabase + Obsidian (`_Active/01-CRM/Clients/`) |
| **Conversa** | `conversations` | Supabase + Obsidian (`_Active/01-CRM/Journals/`) |
| **Mensagens** | `messages` | Supabase |
| **Dados Extraídos** | `extracted_data` | Supabase + Obsidian |
| **Business Intelligence** | `business_intelligence` | Supabase + Obsidian (`_Active/03-INTELLIGENCE/`) |
| **Agendamentos** | `appointments` | Supabase + Belasis ERP |

---

## 3. INTEGRAÇÕES ATIVAS

### ✅ 100% Funcionais

| Integração | Provider | Status | Dados Consumidos |
|------------|----------|--------|------------------|
| **WhatsApp** | Evolution API v2.2.3 | ✅ Online | Mensagens, status, QR Code |
| **Database** | Supabase (PostgreSQL) | ✅ Conectado | clients, conversations, messages, appointments |
| **LLM Router** | OpenRouter | ✅ Configurado | google/gemini-2.0-flash-001, claude-3.5-sonnet |
| **Knowledge Base** | Obsidian Vault | ✅ 1,041 arquivos | Serviços, FAQs, Clientes, Journals |
| **Dojo Arena** | Local | ✅ Operacional | 8 personas, 15 cenários |

### ⚠️ Parciais / Mock

| Integração | Provider | Status | Observação |
|------------|----------|--------|------------|
| **Belasis ERP** | Belasis API | ⚠️ MOCK | `BELASIS_MOCK=true` - Dados simulados |
| **Anthropic** | Anthropic API | ⚠️ Key faltando | Fallback para OpenRouter |
| **WAScript CRM** | WAScript | ⚠️ Token vazio | Não configurado |

### 🔌 Endpoints Externos

```bash
# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8081
EVOLUTION_API_KEY=mothership_master_2026
EVOLUTION_INSTANCE=haven

# Supabase (Database)
SUPABASE_URL=https://sktrmwogifeuzrcnpvsw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OpenRouter (LLMs)
OPENROUTER_API_KEY=sk-or-v1-7cea47208a3f...
```

---

## 4. FLUXO DO DOJO ARENA

### 🥋 Como funciona o Dojo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Usuário acessa painel                                        │
│    http://localhost:3000/dojo                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Seleciona Cenário (15 opções)                                │
│    - beginner: "Saudação Simples", "Pergunta de Horário"        │
│    - intermediate: "Objeção de Preço", "Múltiplos Serviços"     │
│    - advanced: "Reclamação", "Handoff", "Cancelamento"          │
│    - expert: "Indicação"                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Seleciona Persona (8 opções)                                 │
│    - Cliente Apressada (🔥 hurry)                               │
│    - Cliente Sensível a Preço (💰 hesitant)                     │
│    - Cliente Insatisfeita (😤 frustrated)                       │
│    - Cliente Feliz (😊 happy)                                   │
│    - Cliente Indecisa (🤔 hesitant)                             │
│    - Cliente Exigente (💅 frustrated)                           │
│    - Cliente Primeira Vez (🌟 happy)                            │
│    - Cliente Fidelizada (💜 happy)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Clica em "Testar"                                            │
│    POST /api/dojo/test                                          │
│    {                                                            │
│      "scenario_id": "scenario_002",                             │
│      "persona_id": "persona_002",                               │
│      "message": "Quanto custa uma progressiva?"                 │
│    }                                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Backend processa                                             │
│    a) Brain classifica intenção                                 │
│    b) Scheduler verifica contexto                               │
│    c) Memory busca histórico                                    │
│    d) LLM gera resposta                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Métricas calculadas (metrics.py)                             │
│    - Empatia: 0.9 (0-1)                                         │
│    - Clareza: 0.85 (0-1)                                        │
│    - Acionabilidade: 0.8 (0-1)                                  │
│    - Overall: 0.85                                              │
│    - Success: true (≥0.8)                                       │
│    - Points: 15                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. Frontend mostra resultado                                    │
│    - Resposta da LUNA                                           │
│    - Intenção detectada                                         │
│    - Confiança                                                  │
│    - Métricas (barras)                                          │
│    - Success/Fail                                               │
│    - Pontos ganhos                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. Usuário dá feedback (opcional)                               │
│    - Rating: 1-5 estrelas                                       │
│    - Comentário                                                 │
│    POST /api/dojo/feedback                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Métricas do Dojo

**Calculadas por:** `backend/app/dojo/metrics.py`

| Métrica | Como é calculada | Peso |
|---------|------------------|------|
| **Empatia** | Keywords: "entendo", "compreendo", "sei" + tom acolhedor | 30% |
| **Clareza** | Frases curtas (<20 palavras) + informação direta | 25% |
| **Acionabilidade** | Call-to-action presente + próximo passo claro | 25% |
| **Tom Adequado** | Compatível com humor da persona | 20% |

**Success:** ≥80% em todas métricas  
**Partial:** 50-79% em alguma métrica  
**Fail:** <50% em alguma métrica

---

## 5. GESTÃO DE CONTEXTO DA LUNA

### 🧠 Como LUNA mantém contexto

#### 5.1 Memória de Sessão (Curto Prazo)

**Tabela:** `conversations` (Supabase)

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  phone TEXT,
  client_id UUID,
  status TEXT,  -- active, ended, handed_off
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  messages_count INTEGER,
  intent TEXT,
  sentiment TEXT,
  extracted_data JSONB
);
```

**Durante conversa ativa:**
- LUNA busca últimas 15 mensagens
- Mantém contexto da conversa atual
- Atualiza `messages_count` a cada mensagem

#### 5.2 Memória de Cliente (Longo Prazo)

**Tabela:** `clients` (Supabase)

```sql
CREATE TABLE clients (
  id UUID PRIMARY KEY,
  phone TEXT UNIQUE,
  name TEXT,
  first_contact TIMESTAMP,
  last_contact TIMESTAMP,
  tags TEXT[],
  preferences JSONB,
  total_visits INTEGER,
  total_spent DECIMAL,
  conversation_count INTEGER
);
```

**Dados armazenados:**
- Nome e telefone
- Histórico de contatos
- Tags (ex: "nova", "fiel", "escova_semanal")
- Preferências (profissional favorita, horário preferido)
- Total de visitas e gastos
- Contagem de conversas

#### 5.3 Extração de Dados

**Tabela:** `extracted_data` (via `conversations.extracted_data`)

```json
{
  "service": "progressiva",
  "professional": "carla",
  "date": "2026-03-02",
  "time": "14:00",
  "name": "Maria Silva",
  "phone": "5549991112233"
}
```

**Extraído automaticamente por:**
- `brain.py` (camada 2)
- Regex e NLP básico
- Armazenado em `conversations.extracted_data`

#### 5.4 Como LUNA sabe quem é a cliente

```python
# 1. Phone number é a chave primária
phone = message_data.get("key", {}).get("remoteJid", "")
# "5549991112233@s.whatsapp.net" → "5549991112233"

# 2. Busca ou cria cliente
client = await memory.get_or_create_client(phone)
# SELECT * FROM clients WHERE phone = '5549991112233'

# 3. Se existe, carrega perfil
if client:
    context = {
        "name": client.get("name"),
        "preferences": client.get("preferences", {}),
        "total_visits": client.get("total_visits", 0),
        "last_contact": client.get("last_contact")
    }

# 4. Se não existe, cria novo
else:
    client = {
        "phone": phone,
        "first_contact": datetime.utcnow(),
        "last_contact": datetime.utcnow(),
        "tags": ["nova"],
        "preferences": {}
    }
```

#### 5.5 Obsidian Vault (Memória Rica)

**Local:** `backend/app/knowledge/obsidian_vault/_Active/01-CRM/`

**Clientes:** 758 arquivos `.md`
```markdown
---
type: client
phone: "5549991112233"
name: "Maria Teste"
created_at: 2026-02-28
last_contact: 2026-02-28
lifetime_value: 0.0
tags: [cliente, nova]
---

# Maria Teste

## Notas
Nenhuma

## Preferências
{}
```

**Journals:** 204 arquivos `.md`
```markdown
---
type: journal
client_phone: "5549991112233"
last_interaction: 2026-02-28
tags: [journal, log]
---

# Journal Log: 5549991112233

## Histórico de Mensagens
**[2026-02-28 14:30] CLIENTE:** Oi, quero agendar
**[2026-02-28 14:31] LUNA:** Oi! Qual dia você prefere?
```

---

## 6. SISTEMA DE AGENDAMENTO

### 📅 Como funciona

#### 6.1 Fluxo de Agendamento

```
1. Cliente: "Quero agendar uma progressiva"
   ↓
2. Brain classifica: IntentType.AGENDAR
   ↓
3. Scheduler valida dados necessários:
   - ✅ Serviço: "progressiva"
   - ❌ Data: (não informado)
   - ❌ Horário: (não informado)
   - ❌ Profissional: (não informado)
   ↓
4. LUNA pede complemento:
   "Para qual dia você gostaria de agendar?"
   ↓
5. Cliente: "Amanhã às 14h"
   ↓
6. Scheduler extrai:
   - date: "2026-03-02"
   - time: "14:00"
   ↓
7. Scheduler consulta disponibilidade:
   - Se MOCK: retorna horários fixos
   - Se Belasis real: POST /availability
   ↓
8. Se disponível:
   "Perfeito! Seu agendamento foi pré-confirmado!"
   ↓
9. Se indisponível:
   "Infelizmente não temos horário. Quer outro dia?"
```

#### 6.2 Integração Belasis

**Arquivo:** `backend/app/integrations/belasis.py`

**Status atual:** ⚠️ **MOCK**

```python
BELASIS_MOCK=true  # No .env

# Mock data
services = [
    {"id": "svc_1", "name": "Escova Lisa", "price": 59.0},
    {"id": "svc_5", "name": "Progressiva Perfecta", "price": 350.0},
]

professionals = [
    {"id": "prof_1", "name": "Ju", "specialties": ["Escova", "Corte"]},
    {"id": "prof_4", "name": "Carla", "specialties": ["Progressiva"]},
]

availability = ["09:00", "10:30", "14:00", "15:30", "17:00"]
```

**Para produção:**
```python
# 1. Obter chave de API real
BELASIS_API_KEY=sua_chave_aqui

# 2. Mudar .env
BELASIS_MOCK=false

# 3. Belasis fará requests reais
async def check_availability(service_id, professional_id, date):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{self.base_url}/availability",
            headers=self.headers,
            params={"service_id": service_id, "date": date}
        )
        return response.json().get("slots", [])
```

#### 6.3 Conflitos de Horário

**Tratamento:**
```python
# Scheduler verifica último horário
if time_raw not in available_slots:
    # Oferece alternativas
    alternatives = slots[:3]  # Primeiros 3 horários
    return f"Temos estes horários: {alternatives}. Qual prefere?"

# Se cliente insiste em horário indisponível
if conflict_detected:
    # Handoff para humano
    return "Vou verificar com a equipe e te retorno!"
```

#### 6.4 Quando não há horário

**Fluxo:**
1. Scheduler retorna lista vazia
2. LUNA oferece alternativas:
   - Outros horários no mesmo dia
   - Outros dias
   - Outra profissional
3. Se cliente não aceita:
   - Handoff para humano
   - Agenda callback

---

## 7. O QUE NÃO EXISTE AINDA

### ❌ Planejados mas não implementados

| Feature | Status | Observação |
|---------|--------|------------|
| **Belasis Real** | ❌ Mock | Precisa de chave de API |
| **Anthropic API** | ❌ Key faltando | Fallback OpenRouter |
| **WAScript CRM** | ❌ Token vazio | Não configurado |
| **Pagamentos** | ❌ Não implementado | Apenas registro |
| **Confirmação SMS** | ❌ Não implementado | Apenas WhatsApp |
| **Lembretes automáticos** | ❌ Não implementado | Planejamento |
| **Reagendamento online** | ❌ Parcial | Precisa Belasis real |
| **Avaliação pós-serviço** | ❌ Não implementado | Planejamento |
| **Programa fidelidade** | ❌ Não implementado | Apenas tags no DB |
| **Relatórios PDF** | ❌ Não implementado | Apenas JSON/MD |

### ⚠️ Parciais / Em desenvolvimento

| Feature | Status | Faltando |
|---------|--------|----------|
| **Conversation Intelligence** | ⚠️ 90% | Frontend da Intelligence |
| **Dojo Simulator (Ollama)** | ⚠️ 90% | Integração completa |
| **Modules V3** | ⚠️ 80% | Alguns módulos sem frontend |
| **WhatsApp Extraction** | ⚠️ Script pronto | Executar em produção |
| **Obsidian Sync** | ⚠️ Parcial | Daemon de sync |

### 🔮 Roadmap (próximos 30 dias)

**Semana 1:**
- [ ] Integrar Belasis real
- [ ] Configurar WAScript CRM
- [ ] Frontend da Intelligence

**Semana 2:**
- [ ] Lembretes automáticos
- [ ] Confirmação SMS
- [ ] Avaliação pós-serviço

**Semana 3:**
- [ ] Programa fidelidade
- [ ] Relatórios PDF
- [ ] Reagendamento online

**Semana 4:**
- [ ] Monitoring (Prometheus)
- [ ] CI/CD pipeline
- [ ] Score 80+ (produção)

---

## 8. STACK TÉCNICA COMPLETA

### 🐍 Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.109+ | Framework web |
| **Uvicorn** | 0.27+ | ASGI server |
| **Pydantic** | 2.5+ | Validação de dados |
| **Pydantic Settings** | 2.1+ | Configurações |
| **Supabase** | 1.0+ | Database client |
| **HTTPX** | 0.26+ | HTTP client assíncrono |
| **Aiohttp** | 3.9+ | HTTP client |
| **Anthropic** | 0.8+ | Claude API |
| **Loguru** | 0.7+ | Logging |
| **SlowAPI** | 0.1+ | Rate limiting |
| **Python-dateutil** | 2.8+ | Datas |
| **Pytz** | 2024.1+ | Timezones |
| **Openpyxl** | 3.1+ | Excel |
| **Python-docx** | 1.1+ | Word |
| **PyPDF2** | 3.0+ | PDF |
| **Pandas** | 2.2+ | Data analysis |

### 🌐 Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Next.js** | 14.1.0 | Framework React |
| **React** | 18.2.0 | UI library |
| **TypeScript** | 5.3+ | Tipagem |
| **Tailwind CSS** | 3.4+ | Estilização |
| **Framer Motion** | 11.18+ | Animações |
| **Lucide React** | 0.312+ | Ícones |
| **SWR** | 2.4+ | Data fetching |
| **Recharts** | 2.10+ | Gráficos |
| **Axios** | 1.6+ | HTTP client |
| **clsx** | 2.1+ | Classes CSS |
| **date-fns** | 3.3+ | Datas |

### 🗄️ Database

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Supabase** | Latest | PostgreSQL gerenciado |
| **PostgreSQL** | 15+ | Database |
| **Realtime** | Latest | WebSockets |
| **RLS** | Latest | Row Level Security |

### 📱 WhatsApp

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Evolution API** | 2.2.3 | Gateway WhatsApp |
| **Docker** | Latest | Containerização |
| **Redis** | 7+ | Cache/session |

### 🤖 IA / LLMs

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **OpenRouter** | Latest | Router de LLMs |
| **Google Gemini** | 2.0 Flash | LLM rápido |
| **Anthropic Claude** | 3.5 Sonnet | LLM complexo |
| **DeepSeek** | R1 | LLM lógico |

### 🐳 Infraestrutura

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Docker** | Latest | Containers |
| **Docker Compose** | Latest | Orquestração |
| **Nginx** | Latest | Reverse proxy (produção) |

### 📊 Obsidian (Knowledge)

| Plugin | Versão | Uso |
|--------|--------|-----|
| **Dataview** | Latest | Queries no vault |
| **Templater** | Latest | Templates |
| **Copilot** | Latest | IA local |
| **Calendar** | Latest | Navegação temporal |
| **Tasks** | Latest | Gestão tarefas |
| **Kanban** | Latest | Kanban boards |
| **Icon Folder** | Latest | Ícones |

### 🧪 Testing

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Pytest** | 8.0+ | Testes Python |
| **Jest** | 29.0+ | Testes TypeScript |

---

## 📈 MÉTRICAS ATUAIS

| Métrica | Valor |
|---------|-------|
| **Arquivos Backend** | 132 Python |
| **Arquivos Frontend** | 17 TypeScript/TSX |
| **Arquivos Obsidian** | 1,041 Markdown |
| **Clientes no DB** | 758 |
| **Journals** | 204 |
| **Serviços** | 38 |
| **FAQs** | 4 |
| **Personas Dojo** | 8 |
| **Cenários Dojo** | 15 |
| **Scripts** | 40+ |
| **Documentação** | 80+ arquivos |

---

**Fim do Mapeamento Completo**

*Documento gerado via Agent Flow - 2026-03-01*
