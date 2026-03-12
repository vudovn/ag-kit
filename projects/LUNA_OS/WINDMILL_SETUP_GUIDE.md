# 🌬️ Windmill no LUNA OS - Guia de Uso

**Data:** 2026-03-11
**Versão:** v3.0
**Status:** ✅ Implementado

---

## 📋 Visão Geral

Windmill é uma plataforma de automação de workflows que permite criar scripts Python/TypeScript e fluxos de trabalho visuais. No LUNA OS, ele é usado para:

- **Automação de processos** (ex: processamento de dados, ETL)
- **Orquestração de tarefas** (ex: pipelines de ML, agendamentos)
- **Integração entre serviços** (ex: conectar Supabase → LLM → WhatsApp)
- **Jobs agendados** (ex: relatórios diários, limpeza de dados)

---

## 🚀 Inicialização Rápida

### Opção 1: Script Dedicado (Recomendado)

```bash
# Iniciar Windmill
./windmill-start.sh

# Parar Windmill
./windmill-stop.sh
```

### Opção 2: Docker Compose Direto

```bash
# Iniciar
docker-compose -f docker-compose.windmill.yml up -d

# Parar
docker-compose -f docker-compose.windmill.yml down

# Ver logs
docker-compose -f docker-compose.windmill.yml logs -f
```

### Opção 3: Deployment Completo (com LUNA OS)

```bash
./deploy.sh
```

---

## 🔧 Configuração

### 1. Variáveis de Ambiente (.env)

```bash
# Windmill (Workflow Automation)
WINDMILL_HOST=http://luna-windmill:8000
WINDMILL_PUBLIC_URL=http://localhost:8001
WINDMILL_TOKEN=wm_token_luna_2026_change_me
WINDMILL_WORKSPACE=luna
WINDMILL_DATABASE_URL=postgresql://luna_user:change_me_db_password@postgres:5432/windmill
```

### 2. Primeiro Acesso

1. Acesse **http://localhost:8001**
2. Crie sua conta (primeiro usuário é admin automaticamente)
3. Crie um workspace (ex: `luna`)
4. Gere um token em **Settings → Tokens**

---

## 📁 Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                  LUNA OS Network                     │
│                                                      │
│  ┌────────────────┐    ┌──────────────────────┐     │
│  │  Windmill DB   │───▶│   Windmill Server    │     │
│  │  (Postgres)    │    │   (Port 8000/8001)   │     │
│  │  Port 5433     │    │                      │     │
│  └────────────────┘    └──────────┬───────────┘     │
│                                   │                 │
│                    ┌──────────────┼──────────────┐  │
│                    │              │              │  │
│           ┌────────▼────┐ ┌──────▼──────┐ ┌────▼───┐│
│           │  Worker 1   │ │  Worker 2   │ │Native  ││
│           │  (Python)   │ │  (Python)   │ │Worker  ││
│           └─────────────┘ └─────────────┘ └────────┘│
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           External Services                   │   │
│  │  - Supabase  - Evolution API  - Redis        │   │
│  │  - Milvus    - LLM APIs      - Webhooks      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Componentes

| Serviço | Container | Porta | Descrição |
|---------|-----------|-------|-----------|
| Windmill DB | `luna-windmill-db` | 5433 | Banco de dados interno |
| Windmill Server | `luna-windmill-server` | 8001 | API e UI web |
| Worker 1 | `luna-windmill-worker-1` | - | Executa jobs Python/Bash |
| Worker 2 | `luna-windmill-worker-2` | - | Executa jobs Python/Bash |
| Worker Native | `luna-windmill-worker-native` | - | Jobs leves em-processo |

---

## 💻 Casos de Uso no LUNA OS

### 1. Pipeline de Processamento de Conversas

```python
# @windmill/script
# Processa conversas do WhatsApp e salva no Milvus

import requests
from milvus import MilvusClient

def main(conversation_id: str):
    # 1. Buscar conversa do Supabase
    conv = fetch_from_supabase(conversation_id)
    
    # 2. Extrair entidades com LLM
    entities = call_llm(conv['messages'])
    
    # 3. Salvar embeddings no Milvus
    client = MilvusClient("http://luna-milvus:19530")
    client.insert("conversations", [{
        "id": conversation_id,
        "vector": entities['embedding'],
        "metadata": entities
    }])
    
    return {"status": "processed", "id": conversation_id}
```

### 2. Agendamento de Relatórios Diários

```yaml
# Schedule: 0 7 * * * (todo dia às 07:00)
# Trigger: Cron

steps:
  - id: fetch_metrics
    script: fetch_daily_metrics
    args:
      date: "{{ schedule.date }}"
  
  - id: generate_summary
    script: generate_ai_summary
    args:
      metrics: "{{ fetch_metrics.result }}"
  
  - id: send_whatsapp
    script: send_whatsapp_message
    args:
      to: "+5511999999999"
      message: "{{ generate_summary.result }}"
```

### 3. Webhook para Eventos Externos

```python
# Webhook endpoint: /api/windmill/webhook/luna/event
# Trigger: Webhook

def main(request: dict):
    event = request['body']
    
    if event['type'] == 'new_customer':
        # Criar perfil no CRM
        create_customer_profile(event['data'])
        
        # Enviar mensagem de boas-vindas
        send_welcome_message(event['data']['phone'])
        
    elif event['type'] == 'payment_received':
        # Atualizar status no Supabase
        update_payment_status(event['data']['id'])
        
    return {"status": "ok"}
```

---

## 🔗 Integração com LUNA OS

### Conectar ao Supabase

```python
from supabase import create_client

def get_supabase_client():
    url = "https://sktrmwogifeuzrcnpvsw.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    return create_client(url, key)
```

### Conectar ao Milvus

```python
from pymilvus import MilvusClient

def get_milvus_client():
    return MilvusClient("http://luna-milvus:19530")
```

### Conectar ao Redis

```python
import redis

def get_redis_client():
    return redis.Redis(host="luna-redis", port=6379, db=0)
```

### Chamar Backend LUNA

```python
import requests

def call_luna_backend(endpoint: str, data: dict = None):
    response = requests.post(
        f"http://luna-backend:8000{endpoint}",
        json=data
    )
    return response.json()
```

---

## 📊 Monitoramento

### Logs em Tempo Real

```bash
# Todos os serviços
docker-compose -f docker-compose.windmill.yml logs -f

# Apenas workers
docker-compose -f docker-compose.windmill.yml logs -f windmill_worker

# Apenas server
docker-compose -f docker-compose.windmill.yml logs -f windmill_server
```

### Health Check

```bash
curl http://localhost:8001/api/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "version": "1.5.x"
}
```

### Métricas (via API)

```bash
# Listar workflows
curl -H "Authorization: Bearer $WINDMILL_TOKEN" \
  http://localhost:8001/api/windmill/workspace/luna/flows

# Listar jobs recentes
curl -H "Authorization: Bearer $WINDMILL_TOKEN" \
  http://localhost:8001/api/windmill/workspace/luna/jobs
```

---

## 🛠️ Comandos Úteis

### Gerenciar Containers

```bash
# Reiniciar
docker-compose -f docker-compose.windmill.yml restart

# Parar e remover volumes (perde dados!)
docker-compose -f docker-compose.windmill.yml down -v

# Ver status
docker-compose -f docker-compose.windmill.yml ps
```

### Atualizar Windmill

```bash
# Pull nova imagem
docker-compose -f docker-compose.windmill.yml pull

# Rebuild e restart
docker-compose -f docker-compose.windmill.yml up -d --build
```

### Backup do Banco

```bash
# Exportar
docker exec luna-windmill-db pg_dump \
  -U luna_user windmill > windmill_backup.sql

# Importar
docker exec -i luna-windmill-db psql \
  -U luna_user windmill < windmill_backup.sql
```

---

## 🔐 Segurança

### 1. Token de API

Sempre use autenticação nas chamadas API:

```bash
export WINDMILL_TOKEN="seu_token_aqui"
curl -H "Authorization: Bearer $WINDMILL_TOKEN" http://localhost:8001/api/...
```

### 2. Isolar Workers

Para produção, considere:

```yaml
# No docker-compose.windmill.yml
services:
  windmill_worker_1:
    privileged: false  # Remover privilégio se não usar Docker-in-Docker
    user: "1000:1000"  # Rodar como usuário não-root
```

### 3. HTTPS (Produção)

Descomente o serviço `windmill_caddy` e configure:

```yaml
windmill_caddy:
  environment:
    - BASE_URL=windmill.seudominio.com
```

---

## 🐛 Troubleshooting

### Windmill não inicia

**Sintoma:** Container fica em `restarting`

**Solução:**
```bash
# Ver logs
docker-compose -f docker-compose.windmill.yml logs windmill_server

# Verificar conexão com DB
docker exec luna-windmill-db psql -U luna_user -d windmill -c "SELECT 1"
```

### Workers não executam jobs

**Sintoma:** Jobs ficam em `waiting`

**Solução:**
```bash
# Verificar se workers estão online
docker-compose -f docker-compose.windmill.yml ps

# Checar logs dos workers
docker-compose -f docker-compose.windmill.yml logs windmill_worker_1
```

### Erro de conexão com serviços LUNA

**Sintoma:** `Connection refused` ao conectar em `luna-redis`, `luna-milvus`, etc.

**Solução:**
```bash
# Verificar se rede existe
docker network ls | grep luna_os_luna-network

# Se não existir, criar
docker network create luna_os_luna-network

# Reiniciar Windmill
./windmill-start.sh
```

### Banco de dados corrompido

**Sintoma:** Erros de migration ou tabelas faltando

**Solução:**
```bash
# Resetar banco (perde dados!)
docker-compose -f docker-compose.windmill.yml down -v
docker-compose -f docker-compose.windmill.yml up -d
```

---

## 📚 Recursos

- [Documentação Oficial](https://www.windmill.dev/docs)
- [Biblioteca de Scripts](https://app.windmill.dev/library)
- [Exemplos de Workflows](https://github.com/windmill-labs/windmill/tree/main/examples)
- [API Reference](https://www.windmill.dev/docs/api)

---

## ✅ Checklist de Validação

- [ ] Windmill UI acessível em http://localhost:8001
- [ ] Health check retorna `{"status": "ok"}`
- [ ] Pelo menos 1 worker online
- [ ] Conexão com banco de dados funcionando
- [ ] Primeiro script criado e executado
- [ ] Token de API gerado e salvo no `.env`

---

**Próxima Revisão:** 2026-03-18
**Responsável:** Dev Team
