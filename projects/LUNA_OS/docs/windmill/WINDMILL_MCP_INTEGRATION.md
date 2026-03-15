# 🌬️ Windmill MCP Integration - LUNA OS

**Data:** 2026-03-11
**Status:** ✅ Integrado

---

## 📋 Visão Geral

O **Windmill MCP** permite que assistentes de IA (Claude, etc.) controlem o Windmill diretamente via **Model Context Protocol (MCP)**.

### Benefícios

- **12 ferramentas MCP** para controle do Windmill
- **Controle completo** via prompts de linguagem natural
- **Servidor manual** (sem dependência de geração automática)
- **Leve e rápido** - implementado sob medida para LUNA OS

---

## 🚀 Instalação

### 1. Instalar Dependências

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/windmill-mcp
npm install
```

### 2. Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado em `windmill-mcp/.env`:

```bash
# Windmill LUNA OS Local
WINDMILL_BASE_URL=http://localhost:8001
WINDMILL_API_TOKEN=wm_token_luna_2026_change_me

# Workspace padrão
WINDMILL_WORKSPACE=luna
```

---

## 🔧 Configuração

### Opção 1: Claude Desktop

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

### Opção 2: OpenCode (.opencode)

Edite `.opencode/opencode.jsonc` no projeto:

```jsonc
{
  "mcp": {
    "windmill-luna": {
      "type": "local",
      "command": ["node", "./windmill-mcp/windmill-mcp-server.js"],
      "environment": {
        "WINDMILL_BASE_URL": "http://localhost:8001",
        "WINDMILL_API_TOKEN": "wm_token_luna_2026_change_me"
      },
      "enabled": true
    }
  }
}
```

---

## 📝 Arquivo .env do Windmill MCP

Crie `windmill-mcp/.env`:

```bash
# Windmill LUNA OS Local
WINDMILL_BASE_URL=http://localhost:8001
WINDMILL_API_TOKEN=wm_token_luna_2026_change_me

# Workspace padrão
WINDMILL_WORKSPACE=luna

# Timeout
TEST_TIMEOUT=30000
```

---

## 🛠️ Uso

### 1. Iniciar Windmill

```bash
# Iniciar stack Windmill
./windmill-start.sh

# Verificar saúde
curl http://localhost:8001/api/health
```

### 2. Gerar Token no Windmill

1. Acesse http://localhost:8001
2. Vá para **Settings → Tokens**
3. Clique em **Create Token**
4. Copie o token e atualize `windmill-mcp/.env`

### 3. Testar Servidor MCP

```bash
cd windmill-mcp
node windmill-mcp-server.js
```

### 4. Testar no Claude Desktop

Após configurar, teste com:

```
List all flows in the luna workspace
```

---

## 🔗 Ferramentas MCP Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `list_flows` | Lista todos workflows/flows |
| `list_scripts` | Lista todos scripts |
| `run_flow` | Executa um flow |
| `run_script` | Executa um script |
| `get_job_status` | Status de um job |
| `list_jobs` | Lista jobs recentes |
| `cancel_job` | Cancela job rodando |
| `list_resources` | Lista recursos |
| `get_resource` | Obtém valor de recurso |
| `list_schedules` | Lista schedules |
| `create_schedule` | Cria schedule cron |
| `get_health` | Health check |

---

## 📚 Exemplos de Uso com IA

### Exemplo 1: Criar e Executar Script

**Prompt:**
```
Create a new Python script in Windmill that fetches all pending conversations 
from Supabase and processes them. Then run it immediately.
```

### Exemplo 2: Agendar Workflow

**Prompt:**
```
Schedule the daily_conversation_processor flow to run every 2 hours.
```

### Exemplo 3: Monitorar Jobs

**Prompt:**
```
Show me all jobs that failed in the last 24 hours and their error messages.
```

### Exemplo 4: Criar Recurso

**Prompt:**
```
Create a new database resource for Supabase with the connection details 
from the LUNA OS .env file.
```

---

## 🐛 Troubleshooting

### Erro na Geração

**Sintoma:** `TypeError: Converting circular structure to JSON`

**Solução:** Este é um bug conhecido no openapi-mcp-generator. Use:

```bash
# Opção 1: Versão específica
npx openapi-mcp-generator@3.1.0 ...

# Opção 2: Servidor manual (crie manualmente)
```

### MCP Não Conecta

**Sintoma:** Claude não vê o servidor MCP

**Solução:**
```bash
# Verificar se Windmill está online
curl http://localhost:8001/api/health

# Verificar token
echo $WINDMILL_API_TOKEN

# Testar conexão direta
curl -H "Authorization: Bearer $WINDMILL_API_TOKEN" \
  http://localhost:8001/api/workspace/luna
```

### Claude Desktop Não Carrega MCP

**Sintoma:** Erro no config do Claude

**Solução:**
1. Verifique sintaxe JSON do config
2. Use caminho absoluto para `index.js`
3. Reinicie Claude Desktop
4. Veja logs em `~/Library/Logs/Claude`

---

## 📁 Estrutura do Projeto

```
LUNA_OS/
├── windmill-mcp/              # MCP Server
│   ├── src/
│   │   ├── generator/         # Geração de código
│   │   ├── overrides/         # Customizações
│   │   └── runtime/           # Runtime MCP
│   ├── build/                 # Código gerado
│   ├── .env                   # Configuração local
│   └── package.json
├── windmill/                  # Windmill core
│   ├── examples/luna_os/      # Exemplos de scripts
│   └── docker-compose.yml
├── .env                       # Variáveis LUNA OS
└── windmill-start.sh          # Script de inicialização
```

---

## 🔐 Segurança

### Tokens de API

- **Nunca** commite tokens no Git
- Use variáveis de ambiente
- Rotação periódica de tokens

### Workspace Isolation

```bash
# Use workspace separado para desenvolvimento
WINDMILL_WORKSPACE=luna-dev

# Production
WINDMILL_WORKSPACE=luna-prod
```

### Permissões

Limite permissões do token MCP:

```
✅ Ler workflows
✅ Executar scripts
✅ Criar jobs
❌ Deletar recursos (produção)
❌ Modificar usuários
```

---

## 📊 Monitoramento

### Logs MCP

```bash
cd windmill-mcp
npm run dev 2>&1 | tee mcp.log
```

### Jobs no Windmill

```bash
# Via API
curl -H "Authorization: Bearer $WINDMILL_API_TOKEN" \
  "http://localhost:8001/api/windmill/workspace/luna/jobs?limit=10"
```

### Health Check

```bash
# Windmill
curl http://localhost:8001/api/health

# MCP Server (se endpoint disponível)
curl http://localhost:8080/health
```

---

## ✅ Checklist de Validação

- [ ] Windmill rodando em http://localhost:8001
- [ ] Token de API gerado e configurado
- [ ] MCP Server gerado/buildado
- [ ] Configuração no Claude Desktop/OpenCode
- [ ] Primeiro comando MCP executado com sucesso
- [ ] Scripts de exemplo funcionando

---

## 📚 Recursos

- [Windmill MCP Repo](https://github.com/rothnic/windmill-mcp)
- [Windmill Docs](https://www.windmill.dev/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenAPI Spec](https://app.windmill.dev/api/openapi.json)

---

**Próxima Revisão:** 2026-03-18
**Responsável:** Dev Team
