-- ═══════════════════════════════════════════════
-- Migration 002: Business Tables
-- LUNA OS v3.0 - Campanhas, Knowledge, Analytics
-- ═══════════════════════════════════════════════

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

-- INDEXES - Business Tables
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_dates ON campaigns(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge_base(category, key);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics_daily(date);

-- COMMENTS
COMMENT ON TABLE campaigns IS 'Campanhas sazonais e de follow-up';
COMMENT ON TABLE knowledge_base IS 'Base de conhecimento editável';
COMMENT ON TABLE analytics_daily IS 'Métricas agregadas por dia';
