# 🌬️ Windmill no LUNA OS

> **Workflow Automation & AI Orchestration para LUNA OS v3.0**

---

## 🚀 Quick Start

```bash
# 1. Validar instalação
./validate-windmill.sh

# 2. Iniciar Windmill
./windmill-start.sh

# 3. Acessar UI
# http://localhost:8001

# 4. Testar MCP
cd windmill-mcp && ./test-mcp.sh
```

---

## 📁 O Que Foi Instalado

| Componente | Descrição | Localização |
|------------|-----------|-------------|
| **Docker Stack** | Windmill Server + DB + Workers | `docker-compose.windmill.yml` |
| **Scripts** | Start/Stop/Validate | `windmill-*.sh` |
| **MCP Server** | Integração com IA | `windmill-mcp/` |
| **Exemplos** | Scripts e Flows prontos | `windmill/examples/luna_os/` |
| **Docs** | Manuais completos | `WINDMILL_*.md` |

---

## 📚 Documentação

| Arquivo | Propósito |
|---------|-----------|
| [`WINDMILL_SETUP_GUIDE.md`](./WINDMILL_SETUP_GUIDE.md) | Guia completo de instalação e uso |
| [`WINDMILL_MCP_INTEGRATION.md`](./WINDMILL_MCP_INTEGRATION.md) | Integração MCP para IA |
| [`WINDMILL_INSTALLATION_SUMMARY.md`](./WINDMILL_INSTALLATION_SUMMARY.md) | Resumo e checklist |
| [`windmill/examples/README.md`](./windmill/examples/README.md) | Exemplos de scripts |

---

## 🛠️ Comandos

### Scripts Shell

```bash
./windmill-start.sh        # Iniciar
./windmill-stop.sh         # Parar
./validate-windmill.sh     # Validar instalação
```

### Docker Compose

```bash
# Status
docker-compose -f docker-compose.windmill.yml ps

# Logs
docker-compose -f docker-compose.windmill.yml logs -f

# Restart
docker-compose -f docker-compose.windmill.yml restart

# Clean (remove dados!)
docker-compose -f docker-compose.windmill.yml down -v
```

### Makefile (Opcional)

```bash
make -f Makefile.windmill help
make -f Makefile.windmill start
make -f Makefile.windmill logs
make -f Makefile.windmill mcp
make -f Makefile.windmill health
```

---

## 🔗 URLs

| Serviço | URL |
|---------|-----|
| Windmill UI | http://localhost:8001 |
| Windmill API | http://localhost:8001/api |
| Windmill DB | localhost:5433 |

---

## 🔐 Configuração

### .env (LUNA OS)

```bash
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

## 🌬️ MCP Server (IA Integration)

### Configurar Claude Desktop

Edite `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "windmill-luna": {
      "command": "node",
      "args": ["/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/windmill-mcp/windmill-mcp-server.js"],
      "env": {
        "WINDMILL_BASE_URL": "http://localhost:8001",
        "WINDMILL_API_TOKEN": "wm_token_luna_2026_change_me"
      }
    }
  }
}
```

### Ferramentas MCP (12)

- `list_flows` - Listar workflows
- `list_scripts` - Listar scripts
- `run_flow` - Executar flow
- `run_script` - Executar script
- `get_job_status` - Status do job
- `list_jobs` - Listar jobs
- `cancel_job` - Cancelar job
- `list_resources` - Listar recursos
- `get_resource` - Obter recurso
- `list_schedules` - Listar schedules
- `create_schedule` - Criar schedule
- `get_health` - Health check

---

## 📝 Exemplos de Scripts

### 1. Process Conversation

```python
# windmill/examples/luna_os/process_conversation.py
# Processa conversas com LLM + Milvus

def main(conversation_id: str, force_reprocess: bool = False):
    # Extrai entidades com LLM
    # Gera embeddings
    # Salva no Milvus
    # Atualiza Supabase
    pass
```

### 2. Sync Customer CRM

```python
# windmill/examples/luna_os/sync_customer_crm.py
# Sincroniza cliente entre Supabase, Belasis e CRM

def main(phone: str, sync_belasis: bool = True, sync_crm: bool = True):
    # Busca dados no Supabase
    # Busca no Belasis ERP
    # Envia para CRM externo
    pass
```

### 3. Health Monitor

```python
# windmill/examples/luna_os/health_monitor.py
# Monitora saúde de todos os serviços

def main(send_alerts: bool = True):
    # Check: Backend, Redis, Milvus, etc.
    # Alerta via Ntfy se down
    pass
```

---

## ✅ Checklist de Validação

```bash
# Rodar validação automática
./validate-windmill.sh
```

**Esperado:**
- [x] Arquivos de configuração
- [x] Dependências (Docker, Node, npm)
- [x] Rede Docker
- [ ] Serviços (após start)
- [ ] MCP Server

---

## 🐛 Troubleshooting

### Windmill não inicia

```bash
# Ver logs
docker-compose -f docker-compose.windmill.yml logs

# Verificar rede
docker network ls | grep luna

# Recriar
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

### Erro de porta

```bash
# Verificar portas em uso
lsof -i :8001
lsof -i :5433

# Matar processo
kill -9 <PID>
```

---

## 📞 Suporte

1. **Documentação**: Veja os arquivos `WINDMILL_*.md`
2. **Logs**: `docker-compose -f docker-compose.windmill.yml logs -f`
3. **Validação**: `./validate-windmill.sh`

---

## 🎯 Próximos Passos

1. **Explorar UI**: http://localhost:8001
2. **Criar conta**: Primeiro usuário é admin
3. **Gerar token**: Settings → Tokens
4. **Testar scripts**: UI → Scripts → Run
5. **Configurar MCP**: Adicionar ao Claude Desktop
6. **Automatizar**: Criar workflows para LUNA OS

---

**Versão:** 1.0  
**Data:** 2026-03-11  
**Status:** ✅ Pronto para uso
