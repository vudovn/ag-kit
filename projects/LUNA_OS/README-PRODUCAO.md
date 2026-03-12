# 🌙 LUNA OS v2.0 — Produção

**Sistema de Atendimento IA para Haven Escovaria & Esmalteria**

---

## 🚀 Quick Start

### 1. Pré-requisitos

```bash
# Docker e Docker Compose
docker --version
docker-compose --version

# Python 3.11+ (para scripts)
python3 --version
```

### 2. Configuração Rápida

```bash
# Navegar para pasta LUNA OS
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS

# Copiar .env.example e editar
cp .env.example .env
# Editar .env com suas chaves (SUPABASE, OPENROUTER, etc)

# Rodar script de recovery (opcional - limpa tudo)
./luna-recovery-complete.sh

# OU subir diretamente
docker-compose up -d
```

### 3. Verificar Status

```bash
# Ver containers rodando
docker-compose ps

# Ver logs
docker-compose logs -f

# Testar health check
curl http://localhost:8000/health
curl http://localhost:8000/api/health/status
```

### 4. Acessar

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Health Check | http://localhost:8000/health |
| Evolution API | http://localhost:8081 |

---

## 📋 Configuração de Produção

### Variáveis de Ambiente Obrigatórias

Edite o arquivo `.env`:

```bash
# Supabase (obrigatório)
SUPABASE_URL=https://seu-project.supabase.co
SUPABASE_KEY=sk-xxx-sua-chave-service-role
SUPABASE_ANON_KEY=eyJxxx-sua-chave-anon

# OpenRouter (obrigatório para IA)
OPENROUTER_API_KEY=sk-or-v1-xxx

# Evolution API (obrigatório para WhatsApp)
EVOLUTION_API_URL=http://luna-backend:8000
EVOLUTION_API_KEY=mothership_master_2026
EVOLUTION_INSTANCE=haven

# CORS (produção)
ALLOWED_ORIGINS=https://luna.seudominio.com

# Modo (active=responde, observe=só registra)
LUNA_MODE=active
```

### Executar Migration no Supabase

1. Acesse Supabase Dashboard → SQL Editor
2. Copie o conteúdo de `supabase-migration.sql`
3. Execute no SQL Editor
4. Verifique se 9 tabelas foram criadas

### Popular Banco (Opcional)

```bash
# Dentro do container do backend
docker-compose exec luna-backend python scripts/seed_data.py
```

---

## 🔧 Comandos Úteis

### Containers

```bash
# Subir tudo
docker-compose up -d

# Parar tudo
docker-compose down

# Parar e remover volumes (limpa dados)
docker-compose down -v

# Rebuild completo
docker-compose up -d --build --force-recreate

# Ver logs
docker-compose logs -f
docker-compose logs luna-backend
docker-compose logs luna-frontend

# Acessar container
docker-compose exec luna-backend bash
docker-compose exec luna-frontend sh
```

### Scripts

```bash
# Recovery completo (limpa + rebuild)
./luna-recovery-complete.sh

# Seed data (dados de exemplo)
docker-compose exec luna-backend python scripts/seed_data.py

# Testar health
curl http://localhost:8000/health
curl http://localhost:8000/api/health/status
```

---

## 🏗️ Arquitetura

### Serviços Docker

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| `luna-backend` | 8000 | FastAPI (Python 3.11) |
| `luna-frontend` | 3000 | Next.js 14 (React) |
| `command-tower-evo-db` | 5433 | PostgreSQL (Evolution) |
| `command-tower-evo-api` | 8081 | Evolution API (WhatsApp) |
| `command-tower-redis` | 6379 | Redis (Cache) |

### Redes

- `luna-network`: Backend ↔ Frontend ↔ Redis
- `evolution-net`: Evolution API ↔ PostgreSQL

### Backend APIs

```
/api/webhooks      - Webhooks Evolution
/api/conversations - Conversas
/api/clients       - Clientes
/api/analytics     - Analytics
/api/campaigns     - Campanhas
/api/knowledge     - Base de conhecimento
/api/settings      - Configurações
/api/health        - Health check
/api/brain         - Simulador IA
/api/evolution     - Proxy Evolution API
```

---

## 🔒 Segurança

### CORS em Produção

No `.env`:
```bash
ALLOWED_ORIGINS=https://luna.seudominio.com
```

### Rate Limiting

- `/` : 30 req/min
- `/health` : 60 req/min
- Webhooks: Sem limite (Evolution API confiável)

### Environment Variables

Nunca commitar `.env` no Git!

```bash
# .gitignore já inclui:
.env
*.log
node_modules/
__pycache__/
```

---

## 🐛 Troubleshooting

### Containers não sobem

```bash
# Limpar containers órfãos
docker rm -f command-tower-redis command-tower-evo-db command-tower-evo-api

# Rebuild
docker-compose up -d --build
```

### Erro de CORS

Verifique `ALLOWED_ORIGINS` no `.env`:
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Health check falha

```bash
# Ver logs do backend
docker-compose logs luna-backend

# Testar Supabase
docker-compose exec luna-backend python -c "from app.integrations.supabase_client import get_supabase; print(get_supabase())"
```

### Evolution API não conecta

1. Verifique se `command-tower-evo-api` está rodando
2. Acesse http://localhost:8081/instance/fetchInstances
3. Configure webhook: `http://luna-backend:8000/api/webhooks/evolution`

---

## 📊 Monitoramento

### Logs

```bash
# Logs em tempo real
docker-compose logs -f

# Logs do backend (últimas 100 linhas)
docker-compose logs --tail=100 luna-backend

# Logs salvos (dentro do container)
docker-compose exec luna-backend cat logs/luna_core.log
```

### Health Endpoints

```bash
# Health simples
curl http://localhost:8000/health

# Health completo (integrações)
curl http://localhost:8000/api/health/status
```

### Métricas

Acesse `/api/analytics/dashboard` para:
- Total de conversas
- Taxa de conversão
- Tempo médio de resposta
- Serviços mais pedidos
- Distribuição por horário

---

## 🔄 Deploy em Produção

### 1. Servidor (VPS/Cloud)

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clonar repositório
git clone <repo> luna-os
cd luna-os/LUNA_OS

# Configurar .env
cp .env.example .env
# Editar com chaves de produção

# Subir
docker-compose up -d
```

### 2. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name luna.seudominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d luna.seudominio.com
```

---

## 📝 Changelog

### v2.0.0 (2026-02-26)

**Correções:**
- ✅ Import `settings` em webhooks.py
- ✅ CORS configurável via env
- ✅ Save .env multi-path (Docker + local)
- ✅ Rate limiting (slowapi)
- ✅ Dockerfile production-ready
- ✅ Seed data script
- ✅ Recovery script completo

**Melhorias:**
- ✅ next.config.js com output: standalone
- ✅ .env.example atualizado
- ✅ Documentação completa

---

## 🌙 MCT OS

**Poder invisível, simplicidade visível.**

---

## 📞 Suporte

- **DEBUG_LOG.md**: Erros conhecidos e soluções
- **CODEBASE.md**: Estrutura do código
- **ANALISE_COMPLETA.md**: Avaliação técnica detalhada
