#!/usr/bin/env python3
"""
LUNA OS Project Creator - Part 5
Creates Supabase migration SQL and README.md
"""

import os

BASE_DIR = "/Users/franciscotaveira.ads/LUNA OS"

def create_file(path: str, content: str):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {os.path.relpath(path, BASE_DIR)}")

def main():
    print("\n🌙 Creating LUNA OS v2.0 - Part 5 (Supabase Migration & README)...\n")
    
    # ========== supabase-migration.sql ==========
    create_file(f"{BASE_DIR}/supabase-migration.sql", '''-- LUNA CORE v2.0 - Supabase Migration
-- Execute este SQL no Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CLIENTS (memória longo prazo)
CREATE TABLE IF NOT EXISTS clients (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  phone TEXT UNIQUE NOT NULL,
  name TEXT,
  email TEXT,
  tags TEXT[] DEFAULT '{}',
  persona_type TEXT,
  preferences JSONB DEFAULT '{}',
  first_contact TIMESTAMPTZ,
  last_contact TIMESTAMPTZ,
  total_visits INT DEFAULT 0,
  total_spent DECIMAL(10,2) DEFAULT 0,
  ltv_estimated DECIMAL(10,2),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CONVERSATIONS
CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  client_id UUID REFERENCES clients(id),
  phone TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  intent TEXT,
  sentiment TEXT,
  extracted_data JSONB DEFAULT '{}',
  conversion_result TEXT,
  handoff_reason TEXT,
  messages_count INT DEFAULT 0,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- MESSAGES
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id),
  direction TEXT NOT NULL,
  content TEXT NOT NULL,
  message_type TEXT DEFAULT 'text',
  intent_detected TEXT,
  sentiment TEXT,
  response_time_ms INT,
  model_used TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- APPOINTMENTS
CREATE TABLE IF NOT EXISTS appointments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  client_id UUID REFERENCES clients(id),
  conversation_id UUID REFERENCES conversations(id),
  service_id TEXT NOT NULL,
  service_name TEXT,
  professional_id TEXT,
  professional_name TEXT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  duration_min INT,
  price DECIMAL(10,2),
  status TEXT DEFAULT 'scheduled',
  belasis_id TEXT,
  notes TEXT,
  created_by TEXT DEFAULT 'luna',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CAMPAIGNS
CREATE TABLE IF NOT EXISTS campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT DEFAULT 'draft',
  start_date DATE,
  end_date DATE,
  discount_percent INT,
  discount_fixed DECIMAL(10,2),
  services TEXT[],
  trigger_keywords TEXT[],
  message_template TEXT,
  target_segment TEXT DEFAULT 'all',
  stats JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- KNOWLEDGE BASE
CREATE TABLE IF NOT EXISTS knowledge_base (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category TEXT NOT NULL,
  key TEXT NOT NULL,
  data JSONB NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(category, key)
);

-- ANALYTICS DAILY
CREATE TABLE IF NOT EXISTS analytics_daily (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  date DATE UNIQUE NOT NULL,
  total_conversations INT DEFAULT 0,
  total_messages INT DEFAULT 0,
  conversions INT DEFAULT 0,
  abandonments INT DEFAULT 0,
  handoffs INT DEFAULT 0,
  avg_response_time_ms INT,
  avg_sentiment_score DECIMAL(3,2),
  top_intents JSONB,
  top_services JSONB,
  top_questions JSONB,
  hourly_distribution JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- LEARNINGS
CREATE TABLE IF NOT EXISTS learnings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pattern_type TEXT NOT NULL,
  trigger_pattern TEXT,
  best_response TEXT,
  success_rate DECIMAL(3,2),
  times_used INT DEFAULT 0,
  last_used TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- HANDOFFS
CREATE TABLE IF NOT EXISTS handoffs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id),
  client_id UUID REFERENCES clients(id),
  reason TEXT NOT NULL,
  context_summary TEXT,
  priority TEXT DEFAULT 'normal',
  status TEXT DEFAULT 'pending',
  assigned_to TEXT,
  resolved_at TIMESTAMPTZ,
  resolution_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_clients_phone ON clients(phone);
CREATE INDEX IF NOT EXISTS idx_conversations_client ON conversations(client_id);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_started ON conversations(started_at);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
CREATE INDEX IF NOT EXISTS idx_appointments_client ON appointments(client_id);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics_daily(date);
CREATE INDEX IF NOT EXISTS idx_handoffs_status ON handoffs(status);

-- RLS (Row Level Security) - Opcional
-- ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE clients IS 'Perfis de clientes com memória de longo prazo';
COMMENT ON TABLE conversations IS 'Conversas com clientes via WhatsApp';
COMMENT ON TABLE messages IS 'Mensagens individuais das conversas';
COMMENT ON TABLE appointments IS 'Agendamentos realizados';
COMMENT ON TABLE campaigns IS 'Campanhas sazonais e de follow-up';
COMMENT ON TABLE knowledge_base IS 'Base de conhecimento editável';
COMMENT ON TABLE analytics_daily IS 'Métricas agregadas por dia';
COMMENT ON TABLE learnings IS 'Padrões aprendidos para melhoria contínua';
COMMENT ON TABLE handoffs IS 'Transferências para atendimento humano';
''')
    
    # ========== README.md ==========
    create_file(f"{BASE_DIR}/README.md", '''# 🌙 Luna Core v2.0

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
''')
    
    print("\n✅ Supabase Migration and README created!")
    print("\n" + "="*50)
    print("🌙 LUNA OS v2.0 project created successfully!")
    print("="*50)
    print(f"\n📁 Project location: {BASE_DIR}")
    print("\n📋 Next steps:")
    print("   1. cd luna-core")
    print("   2. cp .env.example .env")
    print("   3. Edit .env with your credentials")
    print("   4. Run supabase-migration.sql in Supabase SQL Editor")
    print("   5. docker-compose up -d")
    print("   6. Open http://localhost:3000")
    print()

if __name__ == "__main__":
    main()
