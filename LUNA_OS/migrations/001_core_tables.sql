-- ═══════════════════════════════════════════════
-- Migration 001: Core Tables
-- LUNA OS v3.0 - Tabelas principais
-- ═══════════════════════════════════════════════

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
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
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
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
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
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
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

-- INDEXES - Core Tables
CREATE INDEX IF NOT EXISTS idx_clients_phone ON clients(phone);
CREATE INDEX IF NOT EXISTS idx_conversations_client ON conversations(client_id);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_started ON conversations(started_at);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
CREATE INDEX IF NOT EXISTS idx_appointments_client ON appointments(client_id);

-- COMMENTS
COMMENT ON TABLE clients IS 'Perfis de clientes com memória de longo prazo';
COMMENT ON TABLE conversations IS 'Conversas com clientes via WhatsApp';
COMMENT ON TABLE messages IS 'Mensagens individuais das conversas';
COMMENT ON TABLE appointments IS 'Agendamentos realizados';
