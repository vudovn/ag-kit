-- ═══════════════════════════════════════════════
-- Migration 003: Support Tables
-- LUNA OS v3.0 - Handoffs, Learnings, Settings
-- ═══════════════════════════════════════════════

-- HANDOFFS
CREATE TABLE IF NOT EXISTS handoffs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  reason TEXT NOT NULL,
  context_summary TEXT,
  priority TEXT DEFAULT 'normal',
  status TEXT DEFAULT 'pending',
  assigned_to TEXT,
  resolved_at TIMESTAMPTZ,
  resolution_notes TEXT,
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

-- SYSTEM SETTINGS
CREATE TABLE IF NOT EXISTS system_settings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  key TEXT UNIQUE NOT NULL,
  value JSONB NOT NULL,
  description TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- INDEXES - Support Tables
CREATE INDEX IF NOT EXISTS idx_handoffs_status ON handoffs(status);
CREATE INDEX IF NOT EXISTS idx_handoffs_conversation ON handoffs(conversation_id);
CREATE INDEX IF NOT EXISTS idx_learnings_pattern ON learnings(pattern_type);
CREATE INDEX IF NOT EXISTS idx_settings_key ON system_settings(key);

-- COMMENTS
COMMENT ON TABLE handoffs IS 'Transferências para atendimento humano';
COMMENT ON TABLE learnings IS 'Padrões aprendidos para melhoria contínua';
COMMENT ON TABLE system_settings IS 'Configurações dinâmicas do sistema (runtime)';
