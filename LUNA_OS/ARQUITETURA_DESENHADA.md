# 🏗️ LUNA OS v3.0 - Arquitetura Desenhada

**Data:** 2026-03-03  
**Versão:** 3.0.0

---

# 📐 Índice de Diagramas

1. [Arquitetura Geral (Macro)](#1-arquitetura-geral-macro)
2. [Fluxo de Mensagens (End-to-End)](#2-fluxo-de-mensagens-end-to-end)
3. [Componentes do Backend](#3-componentes-do-backend)
4. [Infraestrutura Docker](#4-infraestrutura-docker)
5. [Diagrama de Sequência](#5-diagrama-de-sequência)
6. [Modelo de Dados](#6-modelo-de-dados)
7. [Pipeline de IA (Brain)](#7-pipeline-de-ia-brain)
8. [Guardrails Flow](#8-guardrails-flow)
9. [Fluxo de Agendamento](#9-fluxo-de-agendamento)
10. [Observabilidade Stack](#10-observabilidade-stack)

---

## 1. Arquitetura Geral (Macro)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           USUÁRIOS FINAIS                                       │
│                    📱 WhatsApp (Clientes da Haven)                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ Mensagens
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CAMADA DE COMUNICAÇÃO                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │              Evolution API (WhatsApp Gateway)                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │   │
│  │  │  Instância   │  │   Webhook    │  │  Send API    │                  │   │
│  │  │  WhatsApp    │  │   Receiver   │  │  Sender      │                  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ HTTP/Webhook
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CAMADA DE APLICAÇÃO (LUNA Backend)                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         FastAPI (Port 8000)                             │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    API Endpoints                                  │  │   │
│  │  │  /webhooks/evolution  /conversations  /clients  /health          │  │   │
│  │  └──────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                        │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │   │
│  │  │              CORE INTELLIGENCE MODULES                            │  │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │  │   │
│  │  │  │    Brain     │  │   Guardrails │  │   Campaign   │            │  │   │
│  │  │  │    Engine    │  │    Engine    │  │   Manager    │            │  │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘            │  │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │  │   │
│  │  │  │   Scheduler  │  │    Memory    │  │  Knowledge   │            │  │   │
│  │  │  │  (Belasis)   │  │   System     │  │    Base      │            │  │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘            │  │   │
│  │  └──────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   CAMADA DE DADOS    │  │   CAMADA DE FILAS    │  │   CAMADA DE ML       │
│  ┌────────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────────┐  │
│  │   Supabase     │  │  │  │    Redis       │  │  │  │    Milvus      │  │
│  │   (Postgres)   │  │  │  │  (Queue/Cache) │  │  │  │  (Vector DB)   │  │
│  │                │  │  │  │                │  │  │  │                │  │
│  │  - clients     │  │  │  │  - message_q   │  │  │  │  - customer    │  │
│  │  - conversations│ │  │  │  - analytics_q │  │  │  │    embeddings  │  │
│  │  - messages    │  │  │  │  - churn_q     │  │  │  │  - behavior    │  │
│  │  - campaigns   │  │  │  │                │  │  │  │    vectors     │  │
│  │  - knowledge   │  │  │  │                │  │  │  │                │  │
│  └────────────────┘  │  │  └────────────────┘  │  │  └────────────────┘  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
                    │
                    │ API REST
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      INTEGRAÇÕES EXTERNAS                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐             │
│  │   Belasis ERP    │  │   OpenRouter     │  │   Ntfy Alerts    │             │
│  │   (Agenda)       │  │   (IA Gateway)   │  │   (Push)         │             │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Fluxo de Mensagens (End-to-End)

```
┌──────────┐
│  Cliente │
│  WhatsApp│
└────┬─────┘
     │ 1. "Quero agendar uma escova para amanhã às 14h"
     ▼
┌──────────────────────────────────────────────────────────────────┐
│  Evolution API                                                    │
│  - Recebe mensagem                                               │
│  - Formata payload                                               │
│  - POST → /api/webhooks/evolution                                │
└────┬─────────────────────────────────────────────────────────────┘
     │ 2. Webhook Payload
     │ {phone: "5549999999999", message: "...", timestamp: 123}
     ▼
┌──────────────────────────────────────────────────────────────────┐
│  LUNA Backend - Webhook Handler                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. VALIDAÇÃO                                               │ │
│  │    - Verificar signature                                   │ │
│  │    - Rate limiting                                         │ │
│  │    - Log de entrada                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2. PERSISTÊNCIA                                            │ │
│  │    - Get or Create Client (Supabase)                       │ │
│  │    - Get or Create Conversation                            │ │
│  │    - Save Message (inbound)                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 3. CLASSIFICAÇÃO                                           │ │
│  │    - classify_intent() → (AGENDAR, 0.95)                   │ │
│  │    - Fast-path? Não (complexo)                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 4. CONTEXTO (RAG)                                          │ │
│  │    - Buscar campanhas ativas                               │ │
│  │    - Buscar knowledge base                                 │ │
│  │    - Buscar histórico do cliente                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 5. IA PROCESSING (2 passes)                                │ │
│  │    Pass 1: Logic Brain                                     │ │
│  │      - Analisar regras de negócio                          │ │
│  │      - Extrair campos (service, date, time)                │ │
│  │      - Gerar intelligence JSON                             │ │
│  │                                                            │ │
│  │    Pass 2: Voice Brain                                     │ │
│  │      - Gerar resposta natural                              │ │
│  │      - Tom: acolhedor, profissional                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 6. GUARDRAILS                                              │ │
│  │    - Verificar profissionais mencionados                   │ │
│  │    - Verificar preços                                      │ │
│  │    - Verificar horários confirmados                        │ │
│  │    → PASS: Resposta OK                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 7. PERSISTÊNCIA                                            │ │
│  │    - Save Message (outbound)                               │ │
│  │    - Update Conversation                                   │ │
│  │    - Save Intelligence                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└────┬─────────────────────────────────────────────────────────────┘
     │ 3. Resposta
     │ "Oi! Vou verificar a disponibilidade de escova para amanhã
     │  às 14h. Você já tem horário marcado com alguma profissional
     │  ou prefere que eu veja as disponíveis? 💇‍♀️"
     ▼
┌──────────────────────────────────────────────────────────────────┐
│  Evolution API                                                    │
│  - POST → /message/sendText                                    │
│  - WhatsApp entrega ao cliente                                  │
└────┬─────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────┐
│  Cliente │
│  Recebe  │
│  Resposta│
└──────────┘

Tempo Total: 1-3 segundos
```

---

## 3. Componentes do Backend

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           LUNA BACKEND                                   │
│                         (FastAPI Application)                            │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   API LAYER     │         │  CORE LAYER     │         │  DATA LAYER     │
│   (Endpoints)   │         │  (Business)     │         │  (Persistence)  │
├─────────────────┤         ├─────────────────┤         ├─────────────────┤
│                 │         │                 │         │                 │
│ webhooks.py     │────────▶│ brain.py        │────────▶│ supabase_       │
│ - evolution     │         │ - process_      │         │ client.py       │
│ - belasis       │         │   message()     │         │                 │
│                 │         │                 │         │ - get_supabase()│
│ conversations.py│────────▶│ guardrails.py   │────────▶│ - init_supabase()│
│ - list()        │         │ - validate()    │         │                 │
│ - get()         │         │ - check_        │         │ queue_          │
│                 │         │   professionals()│        │ manager.py      │
│ clients.py      │────────▶│ - check_prices()│         │                 │
│ - list()        │         │ - check_time()  │         │ - enqueue_job() │
│ - get()         │         │                 │         │ - schedule_job()│
│                 │         │ campaign_       │         │                 │
│ campaigns.py    │────────▶│ manager.py      │────────▶│ vector_db_      │
│ - list()        │         │ - sync_         │         │ manager.py      │
│ - create()      │         │   campaigns()   │         │                 │
│ - detect()      │         │ - detect_       │         │ - connect()     │
│                 │         │   campaign()    │         │ - search()      │
│ health.py       │────────▶│ scheduler.py    │────────▶│                 │
│ - health_check()│         │ - process_      │         │ tracing_        │
│                 │         │   booking()     │         │ setup.py        │
│ brain.py        │────────▶│                 │         │                 │
│ - test_brain()  │         │ memory.py       │────────▶│ - setup_tracing()│
│                 │         │ - get_client()  │         │ - trace_conv()  │
│ settings.py     │────────▶│ - get_history() │         │                 │
│ - get()         │         │                 │         │ alert_          │
│ - update()      │         │ intelligence.py │────────▶│ system.py       │
│                 │         │ - extract()     │         │                 │
│                 │         │ - classify()    │         │ - send_alert()  │
│                 │         │                 │         │ - churn_alert() │
│                 │         │ learning.py     │         │                 │
│                 │         │ - get_patterns()│         │                 │
│                 │         │ - save_learning()│        │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## 4. Infraestrutura Docker

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DOCKER HOST (Mac/Linux)                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    luna-network (bridge)                             │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  luna-backend    │  │  luna-frontend   │  │  luna-redis      │  │   │
│  │  │  Port: 8000      │  │  Port: 3000      │  │  Port: 6380      │  │   │
│  │  │  Health: ✅       │  │  Health: ✅       │  │  Health: ✅       │  │   │
│  │  │                  │  │                  │  │                  │  │   │
│  │  │  - FastAPI       │  │  - Next.js       │  │  - Redis         │  │   │
│  │  │  - OpenTelemetry │  │  - Dashboard     │  │  - Queue (RQ)    │  │   │
│  │  │  - RQ Worker     │  │  - Admin UI      │  │  - Cache         │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  luna-milvus     │  │  luna-postgres   │  │  luna-windmill   │  │   │
│  │  │  Port: 19530     │  │  Port: 5432      │  │  Port: 8001      │  │   │
│  │  │  Health: ✅       │  │  Health: ✅       │  │  Health: ✅       │  │   │
│  │  │                  │  │                  │  │                  │  │   │
│  │  │  - Vector DB     │  │  - PostgreSQL    │  │  - Workflows     │  │   │
│  │  │  - Embeddings    │  │  - App Data      │  │  - Automation    │  │   │
│  │  │  - Similarity    │  │  - Auth          │  │  - Schedules     │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  luna-prometheus │  │  luna-grafana    │  │  luna-pgadmin    │  │   │
│  │  │  Port: 9090      │  │  Port: 3001      │  │  Port: 5050      │  │   │
│  │  │  Health: ✅       │  │  Health: ✅       │  │  Health: ✅       │  │   │
│  │  │                  │  │                  │  │                  │  │   │
│  │  │  - Metrics       │  │  - Dashboards    │  │  - DB Admin      │  │   │
│  │  │  - Scraping      │  │  - Visualization │  │  - Query Editor  │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                         │   │
│  │  │  luna-jaeger     │  │  luna-jobs       │                         │   │
│  │  │  Port: 16686     │  │  (Worker)        │                         │   │
│  │  │  Health: ✅       │  │  Port: -         │                         │   │
│  │  │                  │  │                  │                         │   │
│  │  │  - Tracing       │  │  - RQ Worker     │                         │   │
│  │  │  - Spans         │  │  - Background    │                         │   │
│  │  └──────────────────┘  └──────────────────┘                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                  evolution-net (bridge - isolated)                   │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │  command-tower-  │  │  command-tower-  │  │  command-tower-  │  │   │
│  │  │  evo-api         │  │  evo-db          │  │  redis           │  │   │
│  │  │  Port: 8081      │  │  Port: -         │  │  Port: 6379      │  │   │
│  │  │  Health: ✅       │  │  Health: ✅       │  │  Health: ✅       │  │   │
│  │  │                  │  │                  │  │                  │  │   │
│  │  │  - Evolution     │  │  - Postgres      │  │  - Evolution     │  │   │
│  │  │  - WhatsApp      │  │  - Evo Data      │  │  - Cache         │  │   │
│  │  │  - Webhooks      │  │  - Sessions      │  │  - Queue         │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Volumes Persistentes:                                                       │
│  - postgres_data:/var/lib/postgresql/data                                    │
│  - redis_data:/data                                                          │
│  - milvus_data:/var/lib/milvus                                               │
│  - evo_db_data:/var/lib/postgresql/data                                      │
│  - grafana_data:/var/lib/grafana                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Diagrama de Sequência

```
Cliente     Evolution      LUNA         Supabase     OpenRouter   Belasis
  │            │            │              │             │           │
  │──Msg─────▶│            │              │             │           │
  │            │            │              │             │           │
  │            │─Webhook───▶│              │             │           │
  │            │  POST      │              │             │           │
  │            │            │              │             │           │
  │            │            │─Get Client──▶│             │           │
  │            │            │  SELECT      │             │           │
  │            │            │◀─Client Data─│             │           │
  │            │            │              │             │           │
  │            │            │─Save Msg────▶│             │           │
  │            │            │  INSERT      │             │           │
  │            │            │              │             │           │
  │            │            │Classify Intent              │           │
  │            │            │(local)                      │           │
  │            │            │              │             │           │
  │            │            │─Get Context─▶│             │           │
  │            │            │  SELECT      │             │           │
  │            │            │◀─Knowledge───│             │           │
  │            │            │              │             │           │
  │            │            │───────────────Complete────▶│           │
  │            │            │  POST /chat  │             │           │
  │            │            │◀──────────────Response─────│           │
  │            │            │  (2 passes)  │             │           │
  │            │            │              │             │           │
  │            │            │─Guardrails──▶│             │           │
  │            │            │  validate()  │             │           │
  │            │            │◀─OK/Corrected│             │           │
  │            │            │              │             │           │
  │            │            │─Check Availability─────────▶│           │
  │            │            │  GET /slots  │             │           │
  │            │            │◀─Slots───────│             │           │
  │            │            │              │             │           │
  │            │            │─Save Msg────▶│             │           │
  │            │            │  INSERT      │             │           │
  │            │            │              │             │           │
  │◀─Response──│────────────│              │             │           │
  │            │  sendText  │              │             │           │
  │            │            │              │             │           │
```

---

## 6. Modelo de Dados

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LUNA DATABASE SCHEMA                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│     clients      │       │  conversations   │       │     messages     │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (UUID) PK     │◀──────│ id (UUID) PK     │◀──────│ id (UUID) PK     │
│ phone (TEXT) UK  │  1:N  │ client_id (UUID) │  1:N  │ conversation_id  │
│ name (TEXT)      │       │ phone (TEXT)     │       │ direction (TEXT) │
│ email (TEXT)     │       │ status (TEXT)    │       │ content (TEXT)   │
│ tags (TEXT[])    │       │ intent (TEXT)    │       │ intent_detected  │
│ preferences      │       │ sentiment (TEXT) │       │ sentiment (TEXT) │
│   (JSONB)        │       │ extracted_data   │       │ model_used (TEXT)│
│ first_contact    │       │   (JSONB)        │       │ response_time_ms │
│   (TIMESTAMPTZ)  │       │ conversion_result│       │ created_at       │
│ last_contact     │       │ messages_count   │       └──────────────────┘
│   (TIMESTAMPTZ)  │       │ handoff_reason   │
│ total_visits     │       │ started_at       │       ┌──────────────────┐
│ total_spent      │       │ ended_at         │       │    campaigns     │
│ ltv_estimated    │       │ created_at       │       ├──────────────────┤
│ notes (TEXT)     │       └──────────────────┘       │ id (UUID) PK     │
│ created_at       │                                  │ name (TEXT)      │
└──────────────────┘       ┌──────────────────┐       │ type (TEXT)      │
                           │   appointments   │       │ status (TEXT)    │
┌──────────────────┐       ├──────────────────┤       │ start_date       │
│  knowledge_base  │       │ id (UUID) PK     │       │ end_date         │
├──────────────────┤       │ client_id (UUID) │       │ discount_percent │
│ id (UUID) PK     │       │ conversation_id  │       │ discount_fixed   │
│ category (TEXT)  │       │ service_id (TEXT)│       │ services (TEXT[])│
│ key (TEXT)       │       │ service_name     │       │ trigger_keywords │
│ data (JSONB)     │       │ professional_id  │       │   (TEXT[])       │
│ is_active (BOOL) │       │ professional_name│       │ message_template │
│ updated_at       │       │ date (DATE)      │       │ target_segment   │
│ created_at       │       │ time (TIME)      │       │ stats (JSONB)    │
└──────────────────┘       │ duration_min     │       │ created_at       │
                           │ price            │       └──────────────────┘
┌──────────────────┐       │ status (TEXT)    │
│  ml_models       │       │ belasis_id (TEXT)│       ┌──────────────────┐
├──────────────────┤       │ notes (TEXT)     │       │   handoffs       │
│ id (UUID) PK     │       │ created_by       │       ├──────────────────┤
│ model_type       │       │ created_at       │       │ id (UUID) PK     │
│ version (TEXT)   │       └──────────────────┘       │ conversation_id  │
│ storage_path     │                                  │ client_id (UUID) │
│ status (TEXT)    │       ┌──────────────────┐       │ reason (TEXT)    │
│ metrics (JSONB)  │       │    learnings     │       │ context_summary  │
│ training_samples │       ├──────────────────┤       │ priority (TEXT)  │
│ accuracy_score   │       │ id (UUID) PK     │       │ status (TEXT)    │
│ created_at       │       │ pattern_type     │       │ assigned_to      │
│ updated_at       │       │ trigger_pattern  │       │ resolved_at      │
└──────────────────┘       │ best_response    │       │ resolution_notes │
                           │ success_rate     │       │ created_at       │
┌──────────────────┐       │ times_used       │       └──────────────────┘
│  system_settings │       │ last_used        │
├──────────────────┤       │ created_at       │       ┌──────────────────┐
│ id (UUID) PK     │       └──────────────────┘       │guardrail_violations│
│ key (TEXT) UK    │                                  ├──────────────────┤
│ value (JSONB)    │       ┌──────────────────┐       │ id (UUID) PK     │
│ description      │       │ analytics_daily  │       │ phone (TEXT)     │
│ updated_at       │       ├──────────────────┤       │ conversation_id  │
│ created_at       │       │ id (UUID) PK     │       │ violation_type   │
└──────────────────┘       │ date (DATE) UK   │       │ original_response│
                           │ total_conversat. │       │ corrected_response│
┌──────────────────┐       │ total_messages   │       │ source_of_truth  │
│conversation_intell.│     │ conversions      │       │ severity (TEXT)  │
├──────────────────┤       │ abandonments     │       │ created_at       │
│ id (UUID) PK     │       │ handoffs         │       └──────────────────┘
│ conversation_id  │       │ avg_response_time│
│ client_id (UUID) │       │ avg_sentiment    │
│ services_req.    │       │ top_intents      │
│ services_done    │       │ top_services     │
│ professional_    │       │ top_questions    │
│   requested      │       │ hourly_dist.     │
│ total_value      │       │ created_at       │
│ funnel_stage     │       └──────────────────┘
│ conversion_prob  │
│ objections       │
│ sentiment_overall│
│ insights (JSONB) │
│ confidence_score │
│ processed_at     │
└──────────────────┘
```

---

## 7. Pipeline de IA (Brain)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BRAIN ENGINE PIPELINE                                │
│                      Processamento de Mensagens                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   MENSAGEM  │
                              │   ENTRADA   │
                              └──────┬──────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │  ESTÁGIO 1: CLASSIFICAÇÃO      │
                    │  ┌──────────────────────────┐  │
                    │  │ classify_intent()        │  │
                    │  │ - Pattern matching       │  │
                    │  │ - Retorna (intent, conf) │  │
                    │  └──────────────────────────┘  │
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────┐           ┌───────────────────┐
        │  INTENT + CONF    │           │  INTENT + CONF    │
        │  > 0.8 + QUICK    │           │  < 0.8 ou COMPLEX │
        └─────────┬─────────┘           └─────────┬─────────┘
                  │                               │
                  ▼                               │
        ┌───────────────────┐                     │
        │  FAST-PATH        │                     │
        │  ┌─────────────┐  │                     │
        │  │ KB Search   │  │                     │
        │  │ Resposta    │  │                     │
        │  │ Local       │  │                     │
        │  └─────────────┘  │                     │
        └─────────┬─────────┘                     │
                  │                               │
                  │                               ▼
                  │                     ┌───────────────────┐
                  │                     │  ESTÁGIO 2:       │
                  │                     │  CONTEXTO (RAG)   │
                  │                     │  ┌─────────────┐  │
                  │                     │  │ Campanhas   │  │
                  │                     │  │ Knowledge   │  │
                  │                     │  │ Memory      │  │
                  │                     │  └─────────────┘  │
                  │                     └─────────┬─────────┘
                  │                               │
                  │                               ▼
                  │                     ┌───────────────────┐
                  │                     │  ESTÁGIO 3: IA    │
                  │                     │  ┌─────────────┐  │
                  │                     │  │ Pass 1:     │  │
                  │                     │  │ Logic Brain │  │
                  │                     │  │ - Regras    │  │
                  │                     │  │ - Extração  │  │
                  │                     │  │ - Intell.   │  │
                  │                     │  └─────────────┘  │
                  │                     │         │          │
                  │                     │         ▼          │
                  │                     │  ┌─────────────┐  │
                  │                     │  │ Pass 2:     │  │
                  │                     │  │ Voice Brain │  │
                  │                     │  │ - Resposta  │  │
                  │                     │  │ - Tom       │  │
                  │                     │  └─────────────┘  │
                  │                     └─────────┬─────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────────┐
                    │  ESTÁGIO 4: GUARDRAILS         │
                    │  ┌──────────────────────────┐  │
                    │  │ validate()               │  │
                    │  │ - Profissionais ✓        │  │
                    │  │ - Preços ✓              │  │
                    │  │ - Horários ✓            │  │
                    │  │ - Serviços ✓            │  │
                    │  └──────────────────────────┘  │
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────┐           ┌───────────────────┐
        │  PASS ✅          │           │  FAIL ❌          │
        │  Resposta OK      │           │  Substituir       │
        │                   │           │  Corrigir         │
        └─────────┬─────────┘           └─────────┬─────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────────┐
                    │  ESTÁGIO 5: PERSISTÊNCIA       │
                    │  ┌──────────────────────────┐  │
                    │  │ Save Message (outbound)  │  │
                    │  │ Update Conversation      │  │
                    │  │ Save Intelligence        │  │
                    │  └──────────────────────────┘  │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                              ┌─────────────┐
                              │  RESPOSTA   │
                              │   FINAL     │
                              └─────────────┘

Tempo Total: 1-3 segundos
```

---

## 8. Guardrails Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GUARDRAILS VALIDATION FLOW                           │
│                      Sistema Anti-Alucinação                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │  RESPOSTA DA IA     │
                    │  (Voice Brain)      │
                    └──────────┬──────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │  CHECK 1: PROFISSIONAIS                      │
        │  ┌────────────────────────────────────────┐  │
        │  │ Regex: "com (a|o) ([A-Z][a-z]+)"       │  │
        │  │ Para cada nome encontrado:             │  │
        │  │   - Existe em PROFISSIONAIS?           │  │
        │  │   - Sim → OK                           │  │
        │  │   - Não → VIOLAÇÃO (HIGH)              │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │  CHECK 2: PREÇOS                             │
        │  ┌────────────────────────────────────────┐  │
        │  │ Regex: "R\$ (\d+[,.]\d+)"              │  │
        │  │ Para cada preço encontrado:            │  │
        │  │   - Existe no cardápio?                │  │
        │  │   - Sim → OK                           │  │
        │  │   - Não → VIOLAÇÃO (HIGH)              │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │  CHECK 3: CONFIRMAÇÃO DE HORÁRIO             │
        │  ┌────────────────────────────────────────┐  │
        │  │ Regex: "agendei|confirmado às"         │  │
        │  │ Detectou confirmação?                  │  │
        │  │   - Sim → VIOLAÇÃO (HIGH)              │  │
        │  │   - Não → OK                           │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │  CHECK 4: SERVIÇOS                           │
        │  ┌────────────────────────────────────────┐  │
        │  │ Regex: "oferecemos ([a-z]+)"           │  │
        │  │ Para cada serviço:                     │  │
        │  │   - Existe em SERVICOS?                │  │
        │  │   - Sim → OK                           │  │
        │  │   - Não → VIOLAÇÃO (MEDIUM)            │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │  CHECK 5: DATA NO PASSADO                    │
        │  ┌────────────────────────────────────────┐  │
        │  │ Regex: "(\d{1,2}/\d{1,2})"             │  │
        │  │ Data < hoje?                           │  │
        │  │   - Sim → VIOLAÇÃO (MEDIUM)            │  │
        │  │   - Não → OK                           │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │  RESULTADO                                   │
        │  ┌────────────────────────────────────────┐  │
        │  │ Violações HIGH?                        │  │
        │  │   - Sim → SUBSTITUIR RESPOSTA          │  │
        │  │   - Não → PASSAR                       │  │
        │  │                                        │  │
        │  │ Violações MEDIUM?                      │  │
        │  │   - Sim → LOG + CORRIGIR               │  │
        │  │   - Não → PASSAR                       │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────┬──────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────┐           ┌───────────────────┐
│  PASS ✅          │           │  FAIL ❌          │
│                   │           │                   │
│  Resposta:        │           │  Resposta:        │
│  Original         │           │  Substituída      │
│                   │           │                   │
│  Confidence:      │           │  Confidence:      │
│  -0.0             │           │  -0.4 (HIGH)      │
│                   │           │  -0.2 (MEDIUM)    │
│  Log: Info        │           │  Log: Warning     │
│                   │           │  Alert: Ntfy      │
└───────────────────┘           └───────────────────┘
```

---

## 9. Fluxo de Agendamento

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE AGENDAMENTO                                 │
│                    Integração com Belasis ERP                                │
└─────────────────────────────────────────────────────────────────────────────┘

Cliente: "Quero agendar uma escova para amanhã às 14h"
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │  1. EXTRAÇÃO DE DADOS                   │
        │  ┌───────────────────────────────────┐  │
        │  │ service: "escova"                 │  │
        │  │ professional: null                │  │
        │  │ date: "amanhã" → 2026-03-04       │  │
        │  │ time: "14h" → 14:00               │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  2. VALIDAR SERVIÇO (Cache)             │
        │  ┌───────────────────────────────────┐  │
        │  │ Buscar em services_cache          │  │
        │  │ "escova" → svc_123 ✅             │  │
        │  │ Não encontrado → Perguntar ❌     │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  3. VALIDAR PROFISSIONAL (Cache)        │
        │  ┌───────────────────────────────────┐  │
        │  │ null → Qualquer um ✅             │  │
        │  │ Nome específico → Buscar ID       │  │
        │  │ Não encontrado → Perguntar ❌     │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  4. VALIDAR DATA                        │
        │  ┌───────────────────────────────────┐  │
        │  │ null → Perguntar data ❌          │  │
        │  │ "amanhã" → 2026-03-04 ✅          │  │
        │  │ Data passada → Corrigir ❌        │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  5. CHECAR DISPONIBILIDADE (Belasis)    │
        │  ┌───────────────────────────────────┐  │
        │  │ GET /availability                 │  │
        │  │   ?service=svc_123                │  │
        │  │   &date=2026-03-04                │  │
        │  │                                   │  │
        │  │ Response:                         │  │
        │  │   ["09:00", "10:00", "14:00"]     │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────┐           ┌───────────────────┐
│  TEM 14:00 ✅     │           │  NÃO TEM 14:00 ❌ │
│                   │           │                   │
│  Resposta:        │           │  Resposta:        │
│  "Temos o horário │           │  "Não temos 14h.  │
│  às 14:00!        │           │  Temos 09:00 ou   │
│  Confirmo?        │           │  10:00. Qual      │
│  💇‍♀️"              │           │  prefere?"        │
└───────────────────┘           └───────────────────┘
            │
            ▼ (Cliente confirma)
        ┌─────────────────────────────────────────┐
        │  6. CONFIRMAR AGENDAMENTO (Belasis)     │
        │  ┌───────────────────────────────────┐  │
        │  │ POST /appointments                │  │
        │  │ {                                 │  │
        │  │   service_id: "svc_123",          │  │
        │  │   date: "2026-03-04",             │  │
        │  │   time: "14:00",                  │  │
        │  │   client_phone: "5549..."         │  │
        │  │ }                                 │  │
        │  │                                   │  │
        │  │ Response: {id: "apt_789"}         │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  7. PERSISTER (Supabase)                │
        │  ┌───────────────────────────────────┐  │
        │  │ INSERT appointments               │  │
        │  │ UPDATE conversation               │  │
        │  │   extracted_data.agendamento      │  │
        │  └───────────────────────────────────┘  │
        └───────────────────┬─────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────────┐
        │  8. CONFIRMAÇÃO AO CLIENTE              │
        │  ┌───────────────────────────────────┐  │
        │  │ "Agendado! ✅                      │  │
        │  │  Escova - 04/03 às 14:00          │  │
        │  │  Profissional: Ana Julia          │  │
        │  │  Valor: R$ 50,00                  │  │
        │  │                                   │  │
        │  │ Te envio um lembrete no dia! 💕"  │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
```

---

## 10. Observabilidade Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OBSERVABILIDADE STACK                                │
│                    Tracing + Metrics + Logs + Alerts                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CAMADA 1: TRACING (Jaeger)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  luna-backend (FastAPI Instrumented)                                │   │
│  │                                                                      │   │
│  │  Request: POST /api/webhooks/evolution                              │   │
│  │  Trace ID: abc123def456                                             │   │
│  │                                                                      │   │
│  │  Spans:                                                             │   │
│  │  ├─ webhook_handler (50ms)                                          │   │
│  │  │  └─ supabase.query: get_client (30ms)                           │   │
│  │  ├─ classify_intent (5ms)                                           │   │
│  │  ├─ build_context (50ms)                                            │   │
│  │  │  ├─ supabase.query: get_campaigns (20ms)                        │   │
│  │  │  └─ knowledge.search (30ms)                                     │   │
│  │  ├─ openrouter.complete (1100ms)                                    │   │
│  │  │  ├─ Pass 1: Logic Brain (400ms)                                 │   │
│  │  │  └─ Pass 2: Voice Brain (700ms)                                 │   │
│  │  ├─ guardrails.validate (50ms)                                      │   │
│  │  └─ supabase.query: save_message (40ms)                             │   │
│  │                                                                      │   │
│  │  Total: 1295ms                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Jaeger UI: http://localhost:16686                                         │
│  - Search by Trace ID                                                      │
│  - View Service Map                                                        │
│  - Identify Slow Spans                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CAMADA 2: METRICS (Prometheus)                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Metrics Coletadas:                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  http_requests_total{endpoint, method, status}                      │   │
│  │  http_request_duration_seconds{endpoint, quantile}                  │   │
│  │  active_conversations{status}                                       │   │
│  │  messages_processed_total{direction}                                │   │
│  │  openrouter_requests_total{model, status}                           │   │
│  │  openrouter_request_duration_seconds{model}                         │   │
│  │  supabase_queries_total{table, operation}                           │   │
│  │  supabase_query_duration_seconds{table}                             │   │
│  │  guardrail_violations_total{type, severity}                         │   │
│  │  churn_predictions_total{score_range}                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Prometheus UI: http://localhost:9090                                      │
│  - Query Browser                                                           │
│  - Targets Status                                                          │
│  - Alert Rules                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CAMADA 3: LOGS (Loguru + Grafana Loki)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Log Levels:                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  INFO:  "🧠 Brain: Processing message for 5549999999999 (João)"     │   │
│  │  INFO:  "🎯 Intent classified: AGENDAR (conf: 0.95)"                │   │
│  │  INFO:  "🤖 Model selected: anthropic/claude-3.5-sonnet"            │   │
│  │  INFO:  "✅ Agendamento confirmado: apt_789"                        │   │
│  │                                                                      │   │
│  │  WARN:  "⚠️ CampaignManager: Supabase não inicializado"             │   │
│  │  WARN:  "🛡️ GUARDRAIL [fake_price] | 'R$ 9999'"                     │   │
│  │                                                                      │   │
│  │  ERROR: "❌ Erro ao conectar ao Milvus: Connection refused"          │   │
│  │  ERROR: "🚨 Sovereign Error Captured: Timeout"                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Log Output:                                                                │
│  - Console (stdout) - Development                                          │
│  - JSON (stdout) - Production (parseable)                                  │
│  - File (logs/luna_core.log) - Backup                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CAMADA 4: ALERTS (Ntfy + Grafana)                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Alert Rules (Grafana):                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Error Rate > 5% em 5min → CRITICAL                               │   │
│  │  - Response Time p99 > 5s → HIGH                                    │   │
│  │  - Container Down → CRITICAL                                        │   │
│  │  - Churn Score > 80% → MEDIUM                                       │   │
│  │  - Queue Size > 1000 → MEDIUM                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Ntfy Alerts:                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Topic: luna-alerts                                                 │   │
│  │  Base URL: https://ntfy.sh                                          │   │
│  │                                                                      │   │
│  │  Rate Limits:                                                       │   │
│  │  - CRITICAL: 10/min                                                 │   │
│  │  - HIGH: 5/min                                                      │   │
│  │  - MEDIUM: 3/min                                                    │   │
│  │  - LOW: 1/min                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Grafana UI: http://localhost:3001                                         │
│  - Dashboards                                                              │
│  - Alert Rules                                                             │
│  - Notification Channels                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  FLUXO COMPLETO:                                                            │
│                                                                             │
│  Request → Tracing (Jaeger) → Spans                                         │
│          → Metrics (Prometheus) → Time Series                               │
│          → Logs (Loguru) → Files/Console                                    │
│          → Alerts (Grafana/Ntfy) → Push Notification                        │
│                                                                             │
│  Dashboard Unificado: Grafana                                               │
│  - Panel 1: Request Rate + Error Rate                                       │
│  - Panel 2: Response Time (p50, p95, p99)                                   │
│  - Panel 3: Active Conversations                                            │
│  - Panel 4: OpenRouter Usage                                                │
│  - Panel 5: Guardrail Violations                                            │
│  - Panel 6: System Resources (CPU, RAM)                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 📐 Legenda de Símbolos

| Símbolo | Significado |
|---------|-------------|
| `┌─┐`   | Container/Componente |
| `──▶`   | Fluxo de dados |
| `◀──`   | Resposta/Retorno |
| `│`     | Conexão vertical |
| `●`     | Ponto de decisão |
| `✅`    | Sucesso/Ativo |
| `❌`    | Falha/Inativo |
| `📊`    | Métrica/Dados |
| `🔔`    | Alerta |

---

**Documentação de Arquitetura Completa**  
**LUNA OS v3.0** | 2026-03-03
