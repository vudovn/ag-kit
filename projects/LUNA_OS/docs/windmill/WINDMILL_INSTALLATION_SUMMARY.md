# 🌙 LUNA OS - Windmill Installation Summary

**Data:** 2026-03-11
**Versão:** v3.0

---

## ✅ Instalação Completa

### Componentes Instalados

| Componente | Status | Localização |
|------------|--------|-------------|
| Docker Compose | ✅ | `docker-compose.windmill.yml` |
| Scripts Shell | ✅ | `windmill-start.sh`, `windmill-stop.sh` |
| Windmill MCP | ✅ | `windmill-mcp/` |
| Exemplos de Scripts | ✅ | `windmill/examples/luna_os/` |
| Documentação | ✅ | `WINDMILL_*.md` |

---

## 📁 Estrutura de Arquivos

```
LUNA_OS/
├── .env                              # Configurações Windmill
├── .env.example                      # Template atualizado
├── docker-compose.windmill.yml       # Stack Docker
├── deploy.sh                         # Atualizado com Windmill
├── windmill-start.sh                 # Inicialização rápida
├── windmill-stop.sh                  # Parada
├── WINDMILL_SETUP_GUIDE.md           # Guia completo
├── WINDMILL_MCP_INTEGRATION.md       # Integração MCP
├── windmill/
│   ├── examples/luna_os/
│   │   ├── process_conversation.py   # Processa conversas
│   │   ├── sync_customer_crm.py      # Sync CRM
│   │   ├── health_monitor.py         # Monitoramento
│   │   └── daily_conversation_processor.yaml  # Workflow
│   └── examples/README.md
└── windmill-mcp/
    ├── windmill-mcp-server.js        # Servidor MCP (12 tools)
    ├── .env                          # Config MCP
    ├── test-mcp.sh                   # Teste
    └── package.json
```

---

## 🚀 Quick Start

### 1. Iniciar Windmill

```bash
# Opção A: Apenas Windmill
./windmill-start.sh

# Opção B: LUNA OS completo
./deploy.sh
```

### 2. Acessar UI

```
http://localhost:8001
```

### 3. Gerar Token

1. Acesse http://localhost:8001
2. Settings → Tokens
3. Create Token
4. Copie o token

### 4. Configurar MCP

Edite `windmill-mcp/.env`:

```bash
WINDMILL_API_TOKEN=seu_token_aqui
```

### 5. Testar MCP

```bash
cd windmill-mcp
./test-mcp.sh
```

---

## 🔧 Comandos Úteis

### Docker

```bash
# Ver status
docker-compose -f docker-compose.windmill.yml ps

# Logs em tempo real
docker-compose -f docker-compose.windmill.yml logs -f

# Reiniciar
docker-compose -f docker-compose.windmill.yml restart

# Parar
docker-compose -f docker-compose.windmill.yml down

# Parar + remover volumes (perde dados!)
docker-compose -f docker-compose.windmill.yml down -v
```

### Scripts

```bash
# Iniciar
./windmill-start.sh

# Parar
./windmill-stop.sh

# Testar MCP
cd windmill-mcp && ./test-mcp.sh
```

---

## 📊 Serviços

| Serviço | Container | Porta | Status |
|---------|-----------|-------|--------|
| Windmill Server | `luna-windmill-server` | 8001 | ✅ |
| Windmill DB | `luna-windmill-db` | 5433 | ✅ |
| Worker 1 | `luna-windmill-worker-1` | - | ✅ |
| Worker 2 | `luna-windmill-worker-2` | - | ✅ |
| Worker Native | `luna-windmill-worker-native` | - | ✅ |

---

## 🔗 Ferramentas MCP (12)

| Tool | Descrição |
|------|-----------|
| `list_flows` | Lista workflows |
| `list_scripts` | Lista scripts |
| `run_flow` | Executa flow |
| `run_script` | Executa script |
| `get_job_status` | Status do job |
| `list_jobs` | Lista jobs |
| `cancel_job` | Cancela job |
| `list_resources` | Lista recursos |
| `get_resource` | Obtém recurso |
| `list_schedules` | Lista schedules |
| `create_schedule` | Cria schedule |
| `get_health` | Health check |

---

## 📝 Exemplos de Uso

### 1. Processar Conversa (Python)

```python
# windmill/examples/luna_os/process_conversation.py
# Uso: Execute via Windmill UI ou API

def main(conversation_id: str, force_reprocess: bool = False):
    # Processa conversa com LLM
    # Salva embeddings no Milvus
    # Atualiza Supabase
    pass
```

### 2. Workflow Agendado (YAML)

```yaml
# windmill/examples/luna_os/daily_conversation_processor.yaml
# Schedule: 0 */2 * * * (a cada 2 horas)

steps:
  - id: fetch_pending
    script: fetch_supabase_query
  - id: process_all
    flow_mapping:
      script: process_conversation
```

### 3. Monitor de Saúde

```python
# windmill/examples/luna_os/health_monitor.py
# Verifica: Backend, Redis, Milvus, Supabase, Evolution

def main(send_alerts: bool = True):
    # Check all services
    # Send Ntfy alerts if down
    pass
```

---

## 🔐 Variáveis de Ambiente

### .env (LUNA OS)

```bash
# Windmill (Workflow Automation)
WINDMILL_HOST=http://luna-windmill:8000
WINDMILL_PUBLIC_URL=http://localhost:8001
WINDMILL_TOKEN=wm_token_luna_2026_change_me
WINDMILL_WORKSPACE=luna
WINDMILL_DATABASE_URL=postgresql://luna_user:change_me_db_password@postgres:5432/windmill
```

### windmill-mcp/.env

```bash
WINDMILL_BASE_URL=http://localhost:8001
WINDMILL_API_TOKEN=wm_token_luna_2026_change_me
WINDMILL_WORKSPACE=luna
```

---

## 🐛 Troubleshooting

### Windmill não inicia

```bash
# Ver logs
docker-compose -f docker-compose.windmill.yml logs windmill_server

# Verificar DB
docker-compose -f docker-compose.windmill.yml logs windmill_db

# Recriar containers
docker-compose -f docker-compose.windmill.yml down
docker-compose -f docker-compose.windmill.yml up -d
```

### MCP não conecta

```bash
# Testar Windmill
curl http://localhost:8001/api/health

# Testar token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/health

# Verificar .env
cat windmill-mcp/.env
```

### Erro de rede

```bash
# Criar rede
docker network create luna_os_luna-network

# Reiniciar
./windmill-stop.sh && ./windmill-start.sh
```

---

## 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| `WINDMILL_SETUP_GUIDE.md` | Guia completo de instalação e uso |
| `WINDMILL_MCP_INTEGRATION.md` | Integração com MCP para IA |
| `windmill/examples/README.md` | Exemplos de scripts e workflows |

---

## ✅ Checklist Final

- [ ] Windmill UI acessível (http://localhost:8001)
- [ ] Health check retorna OK
- [ ] Pelo menos 1 worker online
- [ ] Token de API gerado
- [ ] MCP configurado no Claude Desktop
- [ ] Primeiro script executado
- [ ] Workflow de exemplo rodando

---

## 📞 Próximos Passos

1. **Explorar UI**: http://localhost:8001
2. **Criar primeiro script**: UI → Scripts → Create
3. **Agendar workflow**: UI → Flows → Schedule
4. **Configurar MCP**: Adicionar ao Claude Desktop
5. **Testar com IA**: "List all flows in luna workspace"

---

**Status:** ✅ Instalação Completa
**Próxima Revisão:** 2026-03-18
