# 🌙 Luna Core v2.0

> **"Inteligência completa. Complexidade invisível."**

Sistema de Atendimento IA para Haven Escovaria & Esmalteria

## Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 14 (React)
- **Database**: Supabase (PostgreSQL)
- **WhatsApp**: Evolution API
- **AI**: Anthropic Claude

## Quick Start

### 1. Clone e configure

```bash
cd luna-core
cp .env.example .env
# Edite .env com suas credenciais
```

### 2. Execute Supabase Migration

- Acesse seu projeto Supabase
- Vá em SQL Editor
- Execute o conteúdo de `supabase-migration.sql`

### 3. Inicie os containers

```bash
docker-compose up -d
```

### 4. Configure Webhook no Evolution

- URL: `http://seu-servidor:8000/api/webhooks/evolution`
- Events: `messages.upsert`

### 5. Acesse o Dashboard

- http://localhost:3000

## Estrutura

```
luna-core/
├── backend/          # FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── core/     # Brain, Memory
│   │   ├── analytics/
│   │   ├── campaigns/
│   │   └── integrations/
│   └── Dockerfile
├── frontend/         # Next.js
│   ├── app/          # Pages
│   ├── components/   # UI Components
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Features

- ✅ Atendimento automático via WhatsApp
- ✅ Memória curto/médio/longo prazo
- ✅ Analytics e insights
- ✅ Campanhas sazonais
- ✅ Knowledge Base editável
- ✅ Handoff para humanos
- ✅ Dashboard em tempo real

## API Endpoints

### Webhooks
- `POST /api/webhooks/evolution` - Recebe mensagens do WhatsApp

### Conversations
- `GET /api/conversations` - Lista conversas
- `GET /api/conversations/{id}` - Detalhes da conversa
- `GET /api/conversations/active` - Conversas ativas
- `GET /api/conversations/handoffs` - Handoffs pendentes

### Clients
- `GET /api/clients` - Lista clientes
- `GET /api/clients/{id}` - Detalhes do cliente

### Analytics
- `GET /api/analytics/dashboard?days=7` - Métricas do dashboard
- `GET /api/analytics/hourly` - Distribuição por horário
- `GET /api/analytics/services` - Serviços mais pedidos
- `GET /api/analytics/professionals` - Profissionais mais pedidos
- `GET /api/analytics/intents` - Distribuição de intents
- `GET /api/analytics/sentiment` - Distribuição de sentiment

### Campaigns
- `GET /api/campaigns` - Lista campanhas
- `POST /api/campaigns` - Cria campanha
- `GET /api/campaigns/active` - Campanhas ativas
- `PATCH /api/campaigns/{id}/status` - Atualiza status

### Knowledge
- `GET /api/knowledge` - Lista base de conhecimento
- `GET /api/knowledge/{category}` - Categoria específica
- `POST /api/knowledge/upload` - Upload de arquivo
- `PUT /api/knowledge/{category}/{key}` - Atualiza item

## Environment Variables

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8081
EVOLUTION_API_KEY=your-evolution-key
EVOLUTION_INSTANCE=haven

# Anthropic (Claude)
ANTHROPIC_API_KEY=your-anthropic-key

# OpenRouter (alternativa)
OPENROUTER_API_KEY=your-openrouter-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Desenvolvimento

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Checklists

### Deploy
- [ ] .env configurado com credenciais
- [ ] Supabase migration executado
- [ ] Evolution API conectada
- [ ] Webhook configurado
- [ ] docker-compose up -d
- [ ] Testar /health
- [ ] Testar envio de mensagem
- [ ] Verificar Dashboard

## Made with 💜 by MCT

**"Inteligência completa. Complexidade invisível."** 🌙
