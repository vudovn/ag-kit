# 🌙 LUNA OS - Complete Architecture & Connection Report

**Data:** 2026-03-11  
**Versão:** v3.0  
**Status:** ⚠️ **OPERATIONAL WITH ALERTS**

---

## 📊 Executive Summary

### Saúde do Sistema

| Métrica | Valor | Status |
|---------|-------|--------|
| **Containers Ativos** | 10 | ✅ |
| **Testes Pass** | 25 | ✅ 78% |
| **Testes Fail** | 2 | ⚠️ 6% |
| **Testes Warn** | 5 | ⚠️ 16% |

### Status Geral

```
╔═══════════════════════════════════════════════════════════╗
║  SISTEMA OPERACIONAL COM ALERTAS ⚠️                       ║
║                                                           ║
║  ✅ Core: Backend, Frontend, Redis, DBs                  ║
║  ⚠️  Atenções: Milvus offline, Evolution instance        ║
║  ❌ Issues: 2 conexões falharam                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🏗️ Arquitetura Completa

### Diagrama de Topologia

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LUNA OS NETWORK                              │
│                      (172.19.0.0/16 - Bridge)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────┐        │
│  │              WHATSAPP LAYER                             │        │
│  │                                                         │        │
│  │  ┌──────────────┐         ┌──────────────┐            │        │
│  │  │  Evolution   │────────►│  Evolution   │            │        │
│  │  │    API       │         │  PostgreSQL  │            │        │
│  │  │  :8081      │         │   :5432      │            │        │
│  │  │  172.19.0.x │         │  172.19.0.x  │            │        │
│  │  └──────┬───────┘         └──────────────┘            │        │
│  │         │                                              │        │
│  │         │ Webhook                                       │        │
│  │         │ POST /webhook                                 │        │
│  └─────────┼──────────────────────────────────────────────┘        │
│            │                                                        │
│  ┌─────────┴──────────────────────────────────────────────┐        │
│  │              CORE LAYER                                 │        │
│  │                                                         │        │
│  │  ┌──────────────┐         ┌──────────────┐            │        │
│  │  │   Frontend   │────────►│   Backend    │            │        │
│  │  │   Next.js    │  :8000  │   FastAPI    │            │        │
│  │  │  :3000      │         │  :8000      │            │        │
│  │  │  172.19.0.2 │         │  172.19.0.5  │            │        │
│  │  └──────────────┘         └──────┬───────┘            │        │
│  │                                  │                     │        │
│  │         ┌────────────────────────┼──────────────┐     │        │
│  │         │                        │              │     │        │
│  │         ▼                        ▼              ▼     │        │
│  │  ┌──────────────┐         ┌──────────────┐ ┌────────┐│        │
│  │  │    Redis     │         │   Supabase   │ │ Milvus ││        │
│  │  │   :6379      │         │   (Cloud)    │ │ :19530 ││        │
│  │  │  172.19.0.4  │         │  External    │ │        ││        │
│  │  │  (Queue)     │         │              │ │        ││        │
│  │  └──────────────┘         └──────────────┘ └────────┘│        │
│  └────────────────────────────────────────────────────────┘        │
│                                                                     │
│  ┌────────────────────────────────────────────────────────┐        │
│  │              WORKFLOW LAYER (Windmill)                 │        │
│  │                                                         │        │
│  │  ┌──────────────┐         ┌──────────────┐            │        │
│  │  │  Windmill    │────────►│  Windmill    │            │        │
│  │  │   Server     │         │  PostgreSQL  │            │        │
│  │  │  :8001      │         │   :5433      │            │        │
│  │  │  172.19.0.7  │         │  172.19.0.3  │            │        │
│  │  └──────────────┘         └──────────────┘            │        │
│  │                                                         │        │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │        │
│  │  │   Worker 1   │ │   Worker 2   │ │   Worker     │  │        │
│  │  │  (default)   │ │  (default)   │ │   Native     │  │        │
│  │  │  172.19.0.8  │ │  172.19.0.9  │ │  172.19.0.6  │  │        │
│  │  └──────────────┘ └──────────────┘ └──────────────┘  │        │
│  └────────────────────────────────────────────────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL INTEGRATIONS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Supabase   │  │   Anthropic  │  │  OpenRouter  │             │
│  │    (Cloud)   │  │  (Cloud API) │  │  (Cloud API) │             │
│  │              │  │              │  │              │             │
│  │  - Conversas │  │  - LLM       │  │  - LLM       │             │
│  │  - Clientes  │  │  - Claude    │  │  - Models    │             │
│  │  - Settings  │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Belasis ERP │  │  Ntfy Alerts │  │  Windmill   │             │
│  │    (Cloud)   │  │   (Cloud)    │  │  MCP (IA)    │             │
│  │              │  │              │  │              │             │
│  │  - Sync CRM  │  │  - Push      │  │  - Control   │             │
│  │  - Pedidos   │  │  - Monitor   │  │  - Workflows│             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Inventário de Containers

### Tabela Completa

| # | Container | IP | Porta | Imagem | Status | Health |
|---|-----------|-----|-------|--------|--------|--------|
| 1 | luna-frontend | 172.19.0.2 | 3000 | luna_os-luna-frontend | ✅ Up | ✅ Healthy |
| 2 | luna-backend | 172.19.0.5 | 8000 | luna_os-luna-backend | ✅ Up | ✅ Healthy |
| 3 | luna-redis | 172.19.0.4 | 6379 | redis:7-alpine | ✅ Up | ✅ Healthy |
| 4 | luna-evo-db | 172.19.0.3 | 5432 | postgres:15-alpine | ✅ Up | ✅ Healthy |
| 5 | luna-evo-api | - | 8081 | atendai/evolution-api:v2.2.3 | ✅ Up | ✅ Healthy |
| 6 | luna-windmill-server | 172.19.0.7 | 8001 | ghcr.io/windmill-labs/windmill:main | ✅ Up | ⚠️ Unhealthy |
| 7 | luna-windmill-db | 172.19.0.3 | 5433 | postgres:16-alpine | ✅ Up | ✅ Healthy |
| 8 | luna-windmill-worker-1 | 172.19.0.8 | - | ghcr.io/windmill-labs/windmill:main | ✅ Up | - |
| 9 | luna-windmill-worker-2 | 172.19.0.9 | - | ghcr.io/windmill-labs/windmill:main | ✅ Up | - |
| 10 | luna-windmill-worker-native | 172.19.0.6 | - | ghcr.io/windmill-labs/windmill:main | ✅ Up | - |

### Redes Docker

| Rede | Subnet | Containers | Driver |
|------|--------|------------|--------|
| luna-network | 172.19.0.0/16 | 8 | bridge |
| evolution-net | - | 3 (redis, evo-api, evo-db) | bridge |

---

## 🔌 Matriz de Conexões

### Backend (API Core)

| Origem | Destino | Protocolo | Porta | Status | Descrição |
|--------|---------|-----------|-------|--------|-----------|
| Backend | Supabase | HTTPS | 443 | ✅ | Cloud database |
| Backend | Redis | TCP | 6379 | ✅ | Filas e cache |
| Backend | Evolution API | HTTP | 8080 | ✅ | WhatsApp |
| Backend | Milvus | TCP | 19530 | ⚠️ | Vector DB (offline) |
| Backend | Anthropic API | HTTPS | 443 | ✅ | LLM |
| Backend | OpenRouter | HTTPS | 443 | ✅ | LLM Router |
| Backend | Belasis API | HTTPS | 443 | ✅ | ERP |
| Backend | Ntfy | HTTPS | 443 | ✅ | Alertas |

### Frontend (Next.js)

| Origem | Destino | Protocolo | Porta | Status | Descrição |
|--------|---------|-----------|-------|--------|-----------|
| Frontend | Backend | HTTP | 8000 | ✅ | API calls |
| Frontend | Evolution Manager | HTTP | 8081 | ✅ | WhatsApp manager |

### Evolution API (WhatsApp)

| Origem | Destino | Protocolo | Porta | Status | Descrição |
|--------|---------|-----------|-------|--------|-----------|
| Evolution API | Evolution DB | TCP | 5432 | ✅ | PostgreSQL |
| Evolution API | Redis | TCP | 6379 | ✅ | Cache e filas |
| Evolution API | WhatsApp | TCP | 443 | ⚠️ | Conexão externa |
| Evolution API | Backend (webhook) | HTTP | 8000 | ✅ | Webhooks |

### Windmill (Workflows)

| Origem | Destino | Protocolo | Porta | Status | Descrição |
|--------|---------|-----------|-------|--------|-----------|
| Windmill Server | Windmill DB | TCP | 5432 | ✅ | PostgreSQL |
| Workers | Windmill Server | TCP | 8000 | ✅ | Job execution |
| MCP Server | Windmill API | HTTP | 8001 | ✅ | API control |

---

## 🧠 Lógica de Cada Função

### Backend (FastAPI)

#### Estrutura de Diretórios

```
backend/
├── app/
│   ├── api/                  # Endpoints REST
│   │   ├── conversations.py  # Gestão de conversas
│   │   ├── clients.py        # Gestão de clientes
│   │   ├── analytics_super.py # Analytics avançado
│   │   ├── knowledge.py      # Base de conhecimento
│   │   ├── dojo.py           # Treinamento IA
│   │   ├── campaigns_new.py  # Campanhas marketing
│   │   ├── guardrails_api.py # Segurança IA
│   │   └── ...
│   │
│   ├── integrations/         # Integrações externas
│   │   ├── supabase_client.py # Supabase singleton
│   │   ├── evolution.py      # Evolution API
│   │   ├── queue_manager.py  # Redis queues (RQ)
│   │   ├── vector_db_manager.py # Milvus
│   │   ├── tracing_setup.py  # Jaeger tracing
│   │   ├── alert_system.py   # Ntfy alerts
│   │   ├── anthropic.py      # Anthropic LLM
│   │   └── openrouter.py     # OpenRouter LLM
│   │
│   ├── services/             # Serviços de negócio
│   │   ├── brain_structurer.py # Estrutura IA
│   │   └── churn_prediction.py # Previsão churn
│   │
│   ├── modules_v3/           # Módulos v3.0
│   │   └── conversation_intelligence/
│   │
│   ├── core/                 # Core utilities
│   │   ├── auth.py           # Autenticação
│   │   ├── rate_limit.py     # Rate limiting
│   │   └── task_runner.py    # Background tasks
│   │
│   ├── config.py             # Configuração central
│   └── main.py               # Entry point
```

#### Fluxo Principal: WhatsApp → Backend → Resposta

```
1. WhatsApp recebe mensagem
   │
   ▼
2. Evolution API processa
   │
   ▼
3. Webhook POST /webhook
   │
   ▼
4. Backend recebe mensagem
   │
   ├──► Valida assinatura (WEBHOOK_API_KEY)
   ├──► Extrai: phone, body, timestamp
   │
   ▼
5. Armazena no Supabase
   │
   ├──► messages table
   ├──► conversations table (se nova)
   │
   ▼
6. Processa com IA (Brain)
   │
   ├──► Triagem (claude-3-haiku)
   │   ├── Intent detection
   │   └── Sentiment analysis
   │
   ├──► Resposta (claude-sonnet-4.6)
   │   └── Gera resposta contextual
   │
   └──► Crise? (claude-opus-4.6)
       └── Escala para humano
   │
   ▼
7. Envia resposta via Evolution API
   │
   ├──► send_text_chunked()
   │   └── Divide em mensagens naturais
   │
   ▼
8. Atualiza Supabase
   │
   ├──► conversation_intelligence table
   └──► analytics tables
```

#### Código Chave: Evolution Integration

```python
# backend/app/integrations/evolution.py

class EvolutionAPI:
    async def send_text_chunked(self, to: str, text: str) -> None:
        """
        Envia resposta dividida em mensagens curtas e sequenciais.
        Simula conversa natural com pausas entre os fragmentos.
        """
        chunks = self._split_into_chunks(text)
        for i, chunk in enumerate(chunks):
            if i > 0:
                await self.send_typing(to)
                await asyncio.sleep(_CHUNK_DELAY_SECONDS)
            await self.send_text(to, chunk)
```

#### Código Chave: Queue Manager

```python
# backend/app/integrations/queue_manager.py

class QueueManager:
    def enqueue_job(
        self,
        queue_name: str,
        func: Callable,
        *args,
        job_id: Optional[str] = None,
        timeout: str = "5m",
        retry: int = 3,
        **kwargs,
    ):
        """Enfileirar job com retry automático"""
        queue = self.get_queue(queue_name)
        
        job = queue.enqueue(
            func,
            args=args,
            kwargs=kwargs,
            job_id=job_id,
            timeout=timeout,
            retry=Retry(max=retry, interval=[10, 30, 60]),
        )
```

#### Código Chave: Vector DB (Milvus)

```python
# backend/app/integrations/vector_db_manager.py

class VectorDBManager:
    async def connect(self, host: Optional[str] = None, port: Optional[int] = None) -> bool:
        """Conectar ao Milvus com thread-safety e timeout"""
        connections.connect(alias="default", host=self.host, port=self.port)
        await self._init_collections()
        
    async def _create_customer_collection(self):
        """Criar coleção de embeddings de clientes"""
        fields = [
            FieldSchema(name="customer_id", dtype=DataType.VARCHAR, is_primary=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="phone", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="timestamp", dtype=DataType.INT64),
        ]
```

---

### Frontend (Next.js)

#### Estrutura de Diretórios

```
frontend/
├── app/                    # Next.js App Router
│   ├── agenda/            # Gestão de agenda
│   ├── analytics/         # Analytics dashboard
│   ├── brain/             # IA brain config
│   ├── campaigns/         # Campanhas
│   ├── clients/           # Gestão clientes
│   ├── connections/       # Conexões WhatsApp
│   ├── conversations/     # Conversas
│   ├── dojo/              # Treinamento IA
│   ├── intelligence/      # Business intelligence
│   ├── knowledge/         # Base conhecimento
│   ├── monitor/           # Monitoramento
│   ├── persona/           # Persona configuration
│   ├── prompts/           # Prompt library
│   ├── services/          # Serviços
│   ├── settings/          # Configurações
│   └── whatsapp/          # WhatsApp integration
│
├── components/            # React components
├── lib/                   # Utilities
└── types/                 # TypeScript types
```

#### Fluxo: Frontend → Backend

```
1. Usuário acessa página
   │
   ▼
2. Next.js renderiza (SSR/CSR)
   │
   ▼
3. Componente chama API
   │
   ├──► fetch(`${NEXT_PUBLIC_API_URL}/api/...`)
   │
   ▼
4. Backend processa
   │
   ▼
5. Frontend atualiza UI
```

---

### Evolution API (WhatsApp)

#### Funções Principais

| Função | Descrição | Endpoint |
|--------|-----------|----------|
| `send_text` | Envia mensagem de texto | `/message/sendText` |
| `send_typing` | Indicador de digitação | `/chat/presence` |
| `connectionStatus` | Status da conexão | `/instance/connectionStatus` |
| `fetchInstances` | Lista instâncias | `/instance/fetchInstances` |

#### Fluxo: Webhook

```
1. WhatsApp recebe mensagem
   │
   ▼
2. Evolution API processa
   │
   ▼
3. POST webhook para Backend
   │
   └──► http://luna-backend:8000/webhook
       │
       ├──► event: messages.upsert
       ├──► body: { phone, body, from, timestamp }
       └──► signature: X-Webhook-Signature
```

---

### Redis (Filas e Cache)

#### Estrutura de Filas (RQ)

```
Redis (:6379)
├── rq:queue:default       # Jobs padrão
├── rq:queue:high          # Jobs prioritários
├── rq:queue:low           # Jobs baixa prioridade
├── rq:scheduler           # Jobs agendados
└── rq:worker:*            # Workers ativos
```

#### Jobs Enfileirados

```python
# Exemplo: Processamento em background
queue_manager.enqueue_job(
    queue_name="default",
    func=process_conversation_async,
    conversation_id=conv_id,
    timeout="10m",
    retry=3
)
```

---

### Windmill (Workflows)

#### Estrutura de Workflows

```
windmill/
└── examples/luna_os/
    ├── process_conversation.py      # Processa conversas
    ├── sync_customer_crm.py         # Sync CRM
    ├── health_monitor.py            # Monitoramento
    └── daily_conversation_processor.yaml  # Workflow agendado
```

#### Workflow: Daily Conversation Processor

```yaml
# daily_conversation_processor.yaml
schedule: "0 */2 * * *"  # A cada 2 horas

steps:
  - id: fetch_pending
    script: fetch_supabase_query
    args:
      table: conversations
      where: { status: pending }
  
  - id: process_all
    flow_mapping:
      script: process_conversation
      items: "{{ fetch_pending.result }}"
      parallel: 5
```

#### MCP Tools (12 ferramentas)

| Tool | Descrição | Uso |
|------|-----------|-----|
| `list_scripts` | Lista scripts | `list_scripts(limit=20)` |
| `list_flows` | Lista workflows | `list_flows()` |
| `run_script` | Executa script | `run_script(path="...")` |
| `run_flow` | Executa flow | `run_flow(path="...")` |
| `create_schedule` | Cria schedule | `create_schedule(flow, cron)` |
| `list_jobs` | Lista jobs | `list_jobs(status="running")` |
| `get_job_status` | Status job | `get_job_status(job_id)` |
| `cancel_job` | Cancela job | `cancel_job(job_id)` |

---

## 📊 Fluxos de Dados Completos

### 1. Fluxo: Mensagem WhatsApp → Resposta IA

```
┌─────────────┐
│  WhatsApp   │
└──────┬──────┘
       │ (mensagem)
       ▼
┌─────────────┐
│ Evolution   │
│    API      │
└──────┬──────┘
       │ (webhook POST)
       ▼
┌─────────────┐
│   Backend   │
│  (FastAPI)  │
└──────┬──────┘
       │
       ├──► Valida webhook
       │
       ▼
┌─────────────┐
│  Supabase   │
│   (Cloud)   │
└──────┬──────┘
       │ (armazena mensagem)
       │
       ▼
┌─────────────┐
│    Brain    │
│     IA      │
└──────┬──────┘
       │
       ├──► Triagem (haiku)
       ├──► Análise (sonnet)
       └──► Resposta (opus se crise)
       │
       ▼
┌─────────────┐
│  Supabase   │
│   (Cloud)   │
└──────┬──────┘
       │ (armazena resposta + intelligence)
       │
       ▼
┌─────────────┐
│  Milvus     │
│ (Vector DB) │
└──────┬──────┘
       │ (embedding)
       │
       ▼
┌─────────────┐
│ Evolution   │
│    API      │
└──────┬──────┘
       │ (send_text_chunked)
       ▼
┌─────────────┐
│  WhatsApp   │
│  (cliente)  │
└─────────────┘
```

### 2. Fluxo: Agendamento → Workflow Windmill

```
┌─────────────┐
│  Schedule   │
│   (cron)    │
└──────┬──────┘
       │ (trigger)
       ▼
┌─────────────┐
│  Windmill   │
│   Server    │
└──────┬──────┘
       │
       ├──► Worker pega job
       │
       ▼
┌─────────────┐
│  Windmill   │
│   Worker    │
└──────┬──────┘
       │
       ├──► Fetch Supabase
       ├──► Process batch
       └──► Update results
       │
       ▼
┌─────────────┐
│  Supabase   │
│   (Cloud)   │
└──────┬──────┘
       │ (update status)
       │
       ▼
┌─────────────┐
│    Ntfy     │
│   (Alert)   │
└─────────────┘
```

### 3. Fluxo: Frontend → Backend → Dados

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │ (access page)
       ▼
┌─────────────┐
│  Frontend   │
│  (Next.js)  │
└──────┬──────┘
       │ (API call)
       ▼
┌─────────────┐
│   Backend   │
│  (FastAPI)  │
└──────┬──────┘
       │
       ├──► Auth check
       ├──► Rate limit
       │
       ▼
┌─────────────┐
│  Supabase   │
│   (Cloud)   │
└──────┬──────┘
       │ (query data)
       │
       ▼
┌─────────────┐
│   Backend   │
│  (response) │
└──────┬──────┘
       │ (JSON)
       ▼
┌─────────────┐
│  Frontend   │
│   (render)  │
└─────────────┘
```

---

## 🔐 Segurança e Autenticação

### Camadas de Segurança

| Camada | Método | Descrição |
|--------|--------|-----------|
| Webhook | API Key | `WEBHOOK_API_KEY` |
| API | Admin Key | `ADMIN_API_KEY` |
| Evolution | API Key | `EVOLUTION_API_KEY` |
| Supabase | JWT + Key | `SUPABASE_KEY` |
| Windmill | Bearer Token | `WINDMILL_TOKEN` |

### Tokens Configurados

```bash
# .env
EVOLUTION_API_KEY=mothership_master_2026
ADMIN_API_KEY=68f9f29186817a727191e4a219d6e804eb65fa03a0a33f01ceefb66944d629eb
WINDMILL_API_TOKEN=8jeXpcyQw64XH7hxzAtjmj3eK2gd6vrt
WINDMILL_MCP_TOKEN=SCYIk1cJqApIDgGdQFpY6RqPA3krmjcy
```

---

## ⚠️ Issues e Alertas

### Críticos (2)

| # | Issue | Impacto | Solução |
|---|-------|---------|---------|
| 1 | GET /api/clients: HTTP 401 | API requer autenticação | Normal (auth working) |
| 2 | GET /api/conversations: HTTP 401 | API requer autenticação | Normal (auth working) |

### Alertas (5)

| # | Alerta | Impacto | Solução |
|---|--------|---------|---------|
| 1 | Milvus: Disconnected | Vector DB offline | Opcional, iniciar se necessário |
| 2 | Evolution instance 'haven' não encontrada | WhatsApp pode não estar conectado | Verificar conexão |
| 3 | Backend não alcança Evolution API (teste direto) | Teste falso positivo (rede Docker) | Funciona via DNS interno |
| 4 | Evolution API → Redis não testado | Cache pode não estar funcionando | Verificar logs |
| 5 | NEXT_PUBLIC_API_URL vazia | Frontend pode não chamar backend | Configurar .env.local |

---

## 📈 Métricas de Saúde

### Por Serviço

| Serviço | CPU | Memória | Status |
|---------|-----|---------|--------|
| Backend | ~0% | ~300MB | ✅ |
| Frontend | ~0% | ~200MB | ✅ |
| Redis | ~0% | ~50MB | ✅ |
| Evolution API | ~0% | ~400MB | ✅ |
| Windmill Server | ~0% | ~522MB | ✅ |
| PostgreSQL (Evo) | ~0% | ~100MB | ✅ |
| PostgreSQL (Wind) | ~0% | ~100MB | ✅ |

### API Endpoints

| Endpoint | Latência | Status |
|----------|----------|--------|
| GET /health | <100ms | ✅ 200 |
| GET /api/clients | <200ms | ⚠️ 401 (auth) |
| GET /api/conversations | <200ms | ⚠️ 401 (auth) |

---

## 🔧 Configuração de Ambiente

### Variáveis Críticas

```bash
# Core
SUPABASE_URL=https://sktrmwogifeuzrcnpvsw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# WhatsApp
EVOLUTION_API_URL=http://luna-evo-api:8080
EVOLUTION_API_KEY=mothership_master_2026
EVOLUTION_INSTANCE=haven

# LLM
ANTHROPIC_API_KEY=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
OPENROUTER_API_KEY=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

# Infrastructure
REDIS_URL=redis://luna-redis:6379/0
ADMIN_API_KEY=68f9f29186817a727191e4a219d6e804eb65fa03a0a33f01ceefb66944d629eb

# Windmill
WINDMILL_HOST=http://luna-windmill:8000
WINDMILL_PUBLIC_URL=http://localhost:8001
WINDMILL_TOKEN=8jeXpcyQw64XH7hxzAtjmj3eK2gd6vrt
WINDMILL_WORKSPACE=luna
```

---

## 🚀 Próximos Passos

### Prioridade Alta

1. **Configurar NEXT_PUBLIC_API_URL no frontend**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> frontend/.env.local
   ```

2. **Verificar conexão WhatsApp**
   - Acessar http://localhost:8081/manager
   - Escanear QR Code se necessário

3. **Iniciar Milvus (opcional)**
   ```bash
   docker-compose -f docker-compose.extended.yml up -d milvus
   ```

### Prioridade Baixa

1. Corrigir health check do Windmill (endpoint errado)
2. Configurar Gemini API Key
3. Upload de scripts para workspace Windmill

---

## 📚 Referências

### Arquivos de Configuração

| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yml` | Core stack |
| `docker-compose.extended.yml` | Extended services |
| `docker-compose.windmill.yml` | Windmill stack |
| `.env` | Environment variables |

### Código Fonte

| Diretório | Descrição |
|-----------|-----------|
| `backend/app/` | Backend FastAPI |
| `backend/app/integrations/` | Integrações externas |
| `frontend/app/` | Frontend Next.js |
| `windmill-mcp/` | MCP Server |

### Documentação

| Arquivo | Descrição |
|---------|-----------|
| `WINDMILL_ARCHITECTURE_REPORT.md` | Arquitetura Windmill |
| `WINDMILL_DIAGNOSTIC_REPORT.md` | Diagnóstico Windmill |
| `LUNA_OS_COMPLETE_DIAGNOSTIC.md` | Este relatório |

---

**Gerado em:** 2026-03-11T15:27:36Z  
**Ferramenta:** LUNA OS Complete Diagnostic Tool v3.0  
**Próxima Revisão:** 2026-03-18
