-- ═══════════════════════════════════════════════
-- Migration 006: Conversation Intelligence Tables
-- LUNA OS v3.0 - Pipeline de Intelligence
-- ═══════════════════════════════════════════════

-- CONVERSATION INTELLIGENCE
CREATE TABLE IF NOT EXISTS conversation_intelligence (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  
  -- Extrações
  services_requested TEXT[],
  services_completed TEXT[],
  professional_requested TEXT,
  professional_completed TEXT,
  total_value DECIMAL(10,2),
  
  -- Funnel
  funnel_stage TEXT DEFAULT 'awareness',
  conversion_probability DECIMAL(5,4) DEFAULT 0,
  objections_raised TEXT[],
  objections_handled TEXT[],
  
  -- Sentimento
  sentiment_overall DECIMAL(3,2) DEFAULT 0,
  sentiment_progression JSONB,
  urgency_level INT DEFAULT 1,
  
  -- Intelligence
  insights JSONB,
  recommended_actions TEXT[],
  risk_factors TEXT[],
  
  -- Metadata
  processed_at TIMESTAMPTZ DEFAULT NOW(),
  model_version TEXT,
  confidence_score DECIMAL(5,4),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CONVERSATION METRICS
CREATE TABLE IF NOT EXISTS conversation_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID UNIQUE REFERENCES conversations(id) ON DELETE CASCADE,
  
  -- Tempo
  total_duration_seconds INT,
  avg_response_time_ms INT,
  first_response_time_ms INT,
  
  -- Volume
  total_messages INT,
  customer_messages INT,
  luna_messages INT,
  
  -- Qualidade
  resolution_rate DECIMAL(5,4),
  customer_satisfaction DECIMAL(3,2),
  handoff_required BOOLEAN DEFAULT FALSE,
  
  -- IA
  model_used TEXT,
  tokens_consumed INT,
  cost_estimate DECIMAL(10,6),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- INDEXES - Intelligence Tables
CREATE INDEX IF NOT EXISTS idx_conv_intelligence_conversation ON conversation_intelligence(conversation_id);
CREATE INDEX IF NOT EXISTS idx_conv_intelligence_client ON conversation_intelligence(client_id);
CREATE INDEX IF NOT EXISTS idx_conv_intelligence_funnel ON conversation_intelligence(funnel_stage);
CREATE INDEX IF NOT EXISTS idx_conv_metrics_conversation ON conversation_metrics(conversation_id);

-- COMMENTS
COMMENT ON TABLE conversation_intelligence IS 'Análise intelligence de conversas (pipeline)';
COMMENT ON TABLE conversation_metrics IS 'Métricas detalhadas de performance por conversa';
