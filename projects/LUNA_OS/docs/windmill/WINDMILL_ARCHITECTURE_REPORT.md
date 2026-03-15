# 🌙 LUNA OS - Windmill Architecture Report

**Data:** 2026-03-11  
**Versão:** v3.0  
**Status:** ✅ Production Ready

---

## 📊 Executive Summary

### Visão Geral

O **Windmill** é a plataforma de automação de workflows do LUNA OS, integrada via **Model Context Protocol (MCP)** para controle por IA.

| Métrica | Valor |
|---------|-------|
| Status | ✅ Online |
| Workers | 10 ativos |
| Database | ✅ Healthy |
| API Token | ✅ Configurado |
| MCP Server | ✅ Funcionando |

---

## 🏗️ Arquitetura

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        LUNA OS NETWORK                          │
│                      (luna-network: 172.19.0.0/16)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Frontend   │  │   Backend    │  │    Redis     │          │
│  │  :3000       │  │   :8000      │  │    :6379     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │           WINDMILL STACK                            │        │
│  │                                                     │        │
│  │  ┌──────────────┐                                  │        │
│  │  │   Windmill   │  :8001 (UI)                      │        │
│  │  │   Server     │  :2525 (SMTP)                    │        │
│  │  └──────┬───────┘                                  │        │
│  │         │                                          │        │
│  │  ┌──────┴───────┐  ┌──────────────┐               │        │
│  │  │   Worker 1   │  │   Worker 2   │               │        │
│  │  │  (default)   │  │  (default)   │               │        │
│  │  └──────────────┘  └──────────────┘               │        │
│  │                                                     │        │
│  │  ┌──────────────┐  ┌──────────────┐               │        │
│  │  │   Worker     │  │  Windmill    │               │        │
│  │  │   Native     │  │  PostgreSQL  │               │        │
│  │  │  (native)    │  │  :5433       │               │        │
│  │  └──────────────┘  └──────────────┘               │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │           EVOLUTION API STACK                      │        │
│  │  ┌──────────────┐  ┌──────────────┐               │        │
│  │  │  Evolution   │  │  Evolution   │               │        │
│  │  │    API       │  │   PostgreSQL │               │        │
│  │  │   :8081      │  │   :5432      │               │        │
│  │  └──────────────┘  └──────────────┘               │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  MCP Server  │  │    Claude    │  │   LLM APIs   │          │
│  │   (stdio)    │◄─┤   Desktop    │◄─┤  (Anthropic) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │  Windmill    │                                           │
│  │  MCP Endpoint│                                           │
│  │  /api/mcp/...│                                           │
│  └──────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Topologia de Rede Docker

| Container | IP | Porta | Status |
|-----------|-----|-------|--------|
| `luna-frontend` | 172.19.0.2 | 3000 | ✅ |
| `luna-windmill-db` | 172.19.0.3 | 5433 | ✅ |
| `luna-redis` | 172.19.0.4 | 6379 | ✅ |
| `luna-backend` | 172.19.0.5 | 8000 | ✅ |
| `luna-windmill-worker-native` | 172.19.0.6 | - | ✅ |
| `luna-windmill-server` | 172.19.0.7 | 8001 | ✅ |
| `luna-windmill-worker-1` | 172.19.0.8 | - | ✅ |
| `luna-windmill-worker-2` | 172.19.0.9 | - | ✅ |

---

## 📁 Estrutura de Arquivos

```
LUNA_OS/
├── .env                              # Variáveis principais
├── docker-compose.windmill.yml       # Stack Windmill
├── deploy.sh                         # Deploy completo (inclui Windmill)
│
├── windmill-start.sh                 # Inicialização rápida
├── windmill-stop.sh                  # Parada
├── windmill-setup.sh                 # Setup interativo
├── windmill-setup-auto.sh            # Setup automático
├── validate-windmill.sh              # Validação
│
├── WINDMILL_ARCHITECTURE_REPORT.md   # Este relatório
├── WINDMILL_INSTALLATION_SUMMARY.md  # Resumo instalação
├── WINDMILL_MCP_INTEGRATION.md       # Integração MCP
├── WINDMILL_SETUP_GUIDE.md           # Guia completo
│
├── windmill-mcp/                     # MCP Server
│   ├── .env                          # Configuração MCP
│   ├── windmill-mcp-server.js        # Servidor MCP (12 tools)
│   ├── package.json
│   ├── test-mcp.sh                   # Script de teste
│   │
│   └── src/
│       ├── generator/                # Geração de código
│       │   ├── config.json
│       │   ├── fetch-spec.js
│       │   ├── generate.js
│       │   └── generate-tool-list.js
│       │
│       ├── runtime/                  # Runtime MCP
│       │   ├── cache.js
│       │   ├── downloader.js
│       │   ├── generator.js
│       │   └── index.js
│       │
│       ├── overrides/                # Customizações
│       └── utils/                    # Utilitários
│
└── windmill/                         # Windmill Core (submodule)
    └── examples/luna_os/             # Exemplos LUNA OS
        ├── process_conversation.py   # Processa conversas
        ├── sync_customer_crm.py      # Sync CRM
        ├── health_monitor.py         # Monitoramento
        └── daily_conversation_processor.yaml  # Workflow agendado
```

---

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```bash
# Windmill (Workflow Automation)
WINDMILL_HOST=http://luna-windmill:8000
WINDMILL_PUBLIC_URL=http://localhost:8001
WINDMILL_TOKEN=8jeXpcyQw64XH7hxzAtjmj3eK2gd6vrt
WINDMILL_WORKSPACE=luna
WINDMILL_DATABASE_URL=postgresql://luna_user:change_me_db_password@windmill_db:5432/windmill
WINDMILL_MCP_URL=http://localhost:8001/api/mcp/w/luna/mcp?token=SCYIk1cJqApIDgGdQFpY6RqPA3krmjcy
```

### MCP Server (windmill-mcp/.env)

```bash
# Windmill Instance
WINDMILL_BASE_URL=http://localhost:8001
WINDMILL_API_TOKEN=8jeXpcyQw64XH7hxzAtjmj3eK2gd6vrt

# Workspace
WINDMILL_WORKSPACE=luna

# MCP Endpoint
WINDMILL_MCP_URL=http://localhost:8001/api/mcp/w/luna/mcp?token=SCYIk1cJqApIDgGdQFpY6RqPA3krmjcy

# Timeouts
TEST_TIMEOUT=30000
```

### Docker Compose

```yaml
# docker-compose.windmill.yml
services:
  windmill_db:
    image: postgres:16-alpine
    container_name: luna-windmill-db
    ports:
      - "5433:5432"
    environment:
      POSTGRES_DB: windmill
      POSTGRES_USER: luna_user
      POSTGRES_PASSWORD: change_me_db_password

  windmill_server:
    image: ghcr.io/windmill-labs/windmill:main
    container_name: luna-windmill-server
    ports:
      - "8001:8000"
      - "2525:2525"
    environment:
      - DATABASE_URL=postgresql://luna_user:change_me_db_password@windmill_db:5432/windmill
      - MODE=server
      - BASE_URL=http://localhost:8001

  windmill_worker_1:
    image: ghcr.io/windmill-labs/windmill:main
    container_name: luna-windmill-worker-1
    environment:
      - DATABASE_URL=postgresql://luna_user:change_me_db_password@windmill_db:5432/windmill
      - MODE=worker
      - WORKER_GROUP=default

  windmill_worker_2:
    image: ghcr.io/windmill-labs/windmill:main
    container_name: luna-windmill-worker-2
    environment:
      - DATABASE_URL=postgresql://luna_user:change_me_db_password@windmill_db:5432/windmill
      - MODE=worker
      - WORKER_GROUP=default

  windmill_worker_native:
    image: ghcr.io/windmill-labs/windmill:main
    container_name: luna-windmill-worker-native
    environment:
      - DATABASE_URL=postgresql://luna_user:change_me_db_password@windmill_db:5432/windmill
      - MODE=worker
      - WORKER_GROUP=native
      - NATIVE_MODE=true
      - NUM_WORKERS=4
```

---

## 🔑 Tokens e Segurança

### Tokens Ativos

| Token | Tipo | Escopos | Uso |
|-------|------|---------|-----|
| `8jeX...6vrt` | API Token | scripts, flows, schedules, jobs | API REST |
| `SCYI...jcy` | MCP Token | MCP endpoint | Integração MCP |

### Permissões do Token API

- ✅ `scripts:read`, `scripts:write`
- ✅ `flows:read`, `flows:write`
- ✅ `schedules:read`, `schedules:write`
- ✅ `jobs:read`
- ⚠️ `resources:read` (pendente)
- ⚠️ `users:read` (pendente)

### Best Practices de Segurança

1. **Nunca commite tokens** no Git (`.env` está no `.gitignore`)
2. **Rotação periódica** de tokens (recomendado: 30 dias)
3. **Workspace isolation** para ambientes diferentes
4. **Limite permissões** do token MCP

---

## 🛠️ Ferramentas MCP (12)

O MCP Server fornece 12 ferramentas para controle do Windmill:

| # | Ferramenta | Descrição | Parâmetros |
|---|------------|-----------|------------|
| 1 | `list_flows` | Lista workflows | limit, offset |
| 2 | `list_scripts` | Lista scripts | limit, offset |
| 3 | `run_flow` | Executa workflow | flow_path, args |
| 4 | `run_script` | Executa script | script_path, args |
| 5 | `get_job_status` | Status do job | job_id |
| 6 | `list_jobs` | Lista jobs | limit, status |
| 7 | `cancel_job` | Cancela job | job_id |
| 8 | `list_resources` | Lista recursos | limit |
| 9 | `get_resource` | Obtém recurso | resource_name |
| 10 | `list_schedules` | Lista schedules | limit |
| 11 | `create_schedule` | Cria schedule | flow_path, cron, name |
| 12 | `get_health` | Health check | - |

### Implementação (windmill-mcp-server.js)

```javascript
// Estrutura da ferramenta
{
  name: 'list_flows',
  description: 'List all workflows/flows in the workspace',
  inputSchema: {
    type: 'object',
    properties: {
      limit: { type: 'number', default: 20 },
      offset: { type: 'number', default: 0 }
    }
  }
}

// Implementação
async function callTool(name, args) {
  switch (name) {
    case 'list_flows':
      return await windmillRequest(
        `/api/windmill/workspace/${WINDMILL_WORKSPACE}/flows?limit=${limit}&offset=${offset}`
      );
    // ... outras ferramentas
  }
}
```

---

## 📚 Scripts e Workflows de Exemplo

### 1. process_conversation.py

**Descrição:** Processa conversas do WhatsApp, extrai entidades e salva embeddings no Milvus.

**Funcionalidades:**
- Integração com Supabase
- Análise com LLM (Anthropic/OpenRouter)
- Geração de embeddings
- Armazenamento no Milvus
- Extração de: estado emocional, nível de confiança, intenções, action items

**Parâmetros:**
```python
def main(
    conversation_id: str,
    force_reprocess: bool = False
) -> dict
```

**Retorno:**
```json
{
  "status": "success",
  "conversation_id": "test-123",
  "intelligence": {
    "emotional_state": "calm",
    "trust_level": "new",
    "intent": "agendamento",
    "summary": "...",
    "action_items": []
  },
  "embedding_dimension": 384
}
```

### 2. daily_conversation_processor.yaml

**Descrição:** Workflow agendado para processamento em lote de conversas pendentes.

**Schedule:** `0 */2 * * *` (a cada 2 horas)

**Steps:**
1. `fetch_pending` - Busca conversas pendentes no Supabase
2. `filter_valid` - Filtra conversas com ≥3 mensagens
3. `process_all` - Processa em paralelo (5 threads)
4. `consolidate` - Consolida resultados
5. `send_report` - Envia relatório via Ntfy (se erros)

### 3. sync_customer_crm.py

**Descrição:** Sincroniza dados de clientes entre Supabase e CRM externo.

**Funcionalidades:**
- Sync bidirecional
- Detecção de conflitos
- Atualização incremental

### 4. health_monitor.py

**Descrição:** Monitora saúde dos serviços LUNA OS.

**Serviços monitorados:**
- Backend API
- Redis
- Milvus
- Supabase
- Evolution API

**Ações:**
- Envia alertas via Ntfy
- Registra métricas

---

## 🔗 Integrações

### Supabase

```python
SUPABASE_URL = "https://sktrmwogifeuzrcnpvsw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Uso:**
- Armazenamento de conversas
- Mensagens do WhatsApp
- Metadados de inteligência

### Milvus (Vector Database)

```python
MILVUS_HOST = "http://luna-milvus:19530"
MILVUS_PORT = "19530"
```

**Uso:**
- Embeddings de conversas
- Busca semântica
- Similaridade

### Evolution API (WhatsApp)

```python
EVOLUTION_API_URL = "http://luna-evo-api:8080"
EVOLUTION_API_KEY = "mothership_master_2026"
```

**Uso:**
- Envio/recebimento de mensagens
- Gestão de instâncias
- Webhooks

### Ntfy (Alertas)

```python
NTFY_TOPIC = "luna-alerts"
NTFY_BASE_URL = "https://ntfy.sh"
```

**Uso:**
- Alertas de falhas
- Relatórios de processamento
- Notificações de saúde

---

## 🚀 Comandos Úteis

### Inicialização

```bash
# Iniciar apenas Windmill
./windmill-start.sh

# Iniciar LUNA OS completo
./deploy.sh

# Verificar status
docker-compose -f docker-compose.windmill.yml ps
```

### Logs

```bash
# Logs em tempo real
docker-compose -f docker-compose.windmill.yml logs -f

# Logs do servidor
docker-compose -f docker-compose.windmill.yml logs windmill_server --tail=50

# Logs de workers
docker-compose -f docker-compose.windmill.yml logs windmill_worker_1
```

### Parada

```bash
# Parar Windmill
./windmill-stop.sh

# Parar + remover volumes (perde dados!)
docker-compose -f docker-compose.windmill.yml down -v
```

### Validação

```bash
# Validar instalação
./validate-windmill.sh

# Testar saúde
curl http://localhost:8001/api/health/status

# Testar API com token
curl -H "Authorization: Bearer 8jeXpcyQw64XH7hxzAtjmj3eK2gd6vrt" \
  http://localhost:8001/api/w/luna/scripts/list
```

---

## 🧪 Testes e Validação

### Health Checks

```bash
# Health status
curl http://localhost:8001/api/health/status
# {"status":"healthy","database_healthy":true,"workers_alive":10}

# API version
curl http://localhost:8001/api/version
# CE v1.654.0-3-g2aef01d18c

# MCP endpoint
curl -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  "http://localhost:8001/api/mcp/w/luna/mcp?token=SCYIk1cJqApIDgGdQFpY6RqPA3krmjcy"
```

### Validação de Scripts

```bash
# Validar Python
python3 -m py_compile windmill/examples/luna_os/*.py

# Validar YAML
python3 -c "import yaml; yaml.safe_load(open('windmill/examples/luna_os/daily_conversation_processor.yaml'))"
```

---

## 📊 Monitoramento

### Métricas de Saúde

| Métrica | Valor | Threshold | Status |
|---------|-------|-----------|--------|
| Database | ✅ | - | Healthy |
| Workers | 10 | ≥1 | ✅ |
| Memory | ~200MB | <1GB | ✅ |
| CPU | - | - | - |

### Logs de Monitoramento

```
luna-windmill-server | health check completed status="healthy" database_healthy=true workers_alive=10
luna-windmill-server | 198.19 mb allocated/221.87 mb resident
```

---

## 🐛 Troubleshooting

### Problema: Windmill não inicia

**Sintoma:** Container em loop de reinicialização

**Solução:**
```bash
# Ver logs
docker-compose -f docker-compose.windmill.yml logs windmill_server

# Verificar database
docker-compose -f docker-compose.windmill.yml logs windmill_db

# Recriar containers
docker-compose -f docker-compose.windmill.yml down
docker-compose -f docker-compose.windmill.yml up -d
```

### Problema: MCP não conecta

**Sintoma:** Claude não vê o servidor MCP

**Solução:**
```bash
# Verificar token
cat windmill-mcp/.env | grep WINDMILL_API_TOKEN

# Testar conexão
curl -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/w/luna/scripts/list

# Reiniciar MCP
cd windmill-mcp && npm install
```

### Problema: 404 em endpoints

**Sintoma:** Endpoints retornam 404

**Causa:** Workspace não existe ou token sem permissão

**Solução:**
1. Acesse http://localhost:8001
2. Verifique se workspace `luna` existe
3. Gere novo token com escopos adequados

---

## 📈 Roadmap

### Implementado ✅

- [x] Stack Docker completa
- [x] MCP Server com 12 ferramentas
- [x] Scripts de exemplo
- [x] Workflows agendados
- [x] Integração com Supabase
- [x] Integração com Milvus
- [x] Validação automática

### Em Progresso 🚧

- [ ] Recursos (resources:read)
- [ ] Usuários (users:read)
- [ ] Dashboard de métricas
- [ ] Alertas avançados

### Planejado 📋

- [ ] Multi-workspace (dev/prod)
- [ ] CI/CD para scripts
- [ ] Versionamento de flows
- [ ] Backup automático

---

## 📚 Referências

### Documentação Oficial

- [Windmill Docs](https://www.windmill.dev/docs)
- [Windmill MCP Repo](https://github.com/rothnic/windmill-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenAPI Spec](https://app.windmill.dev/api/openapi.json)

### Arquivos Internos

| Arquivo | Descrição |
|---------|-----------|
| `WINDMILL_SETUP_GUIDE.md` | Guia completo de instalação |
| `WINDMILL_MCP_INTEGRATION.md` | Integração MCP |
| `WINDMILL_INSTALLATION_SUMMARY.md` | Resumo da instalação |
| `validate-windmill.sh` | Script de validação |

---

## ✅ Checklist de Validação

### Infraestrutura

- [x] Docker instalado e rodando
- [x] Rede `luna-network` criada
- [x] Containers Windmill online
- [x] Database PostgreSQL saudável
- [x] Workers ativos (10)

### Configuração

- [x] `.env` com variáveis Windmill
- [x] `windmill-mcp/.env` configurado
- [x] Tokens de API válidos
- [x] MCP endpoint funcional

### Funcional

- [x] UI acessível (http://localhost:8001)
- [x] API REST respondendo
- [x] Scripts listados (vazio)
- [x] Flows listados (vazio)
- [x] Schedules listados (vazio)
- [x] MCP tools/list funcionando

### Exemplos

- [x] `process_conversation.py` disponível
- [x] `sync_customer_crm.py` disponível
- [x] `health_monitor.py` disponível
- [x] `daily_conversation_processor.yaml` disponível

### Documentação

- [x] `WINDMILL_SETUP_GUIDE.md` existe
- [x] `WINDMILL_MCP_INTEGRATION.md` existe
- [x] `WINDMILL_INSTALLATION_SUMMARY.md` existe
- [x] `WINDMILL_ARCHITECTURE_REPORT.md` existe

---

## 📞 Contato e Suporte

### Equipe LUNA OS

- **Dev Team:** franciscotaveira.rios@gmail.com
- **Workspace:** luna
- **Versão:** v3.0

### Próxima Revisão

**Data:** 2026-03-18

---

**Gerado automaticamente em:** 2026-03-11T17:59:00Z  
**Ferramenta:** LUNA OS Architecture Analyzer
