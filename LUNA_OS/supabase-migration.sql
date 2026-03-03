-- LUNA CORE v2.0 - Supabase Migration
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
