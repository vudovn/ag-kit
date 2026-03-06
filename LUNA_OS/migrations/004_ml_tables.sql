-- ═══════════════════════════════════════════════
-- Migration 004: ML & Vector Tables
-- LUNA OS v3.0 - DEBT #7: Persistência de Modelos ML
-- ═══════════════════════════════════════════════

-- ML MODELS (para persistência de modelos de ML)
-- DEBT #7: Tabela para versionamento de modelos
CREATE TABLE IF NOT EXISTS ml_models (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  model_type TEXT NOT NULL,
  version TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  metrics JSONB DEFAULT '{}',
  training_samples INT DEFAULT 0,
  accuracy_score DECIMAL(5,4),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(model_type, version)
);

-- Index para busca rápida do modelo ativo
CREATE INDEX IF NOT EXISTS idx_ml_models_type_status 
ON ml_models(model_type, status, created_at DESC);

-- GUARDRAIL VIOLATIONS (para auditoria de anti-alucinação)
CREATE TABLE IF NOT EXISTS guardrail_violations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  phone TEXT NOT NULL,
  conversation_id UUID,
  violation_type TEXT NOT NULL,
  original_response TEXT,
  corrected_response TEXT,
  source_of_truth TEXT,
  severity TEXT DEFAULT 'medium',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index para auditoria
CREATE INDEX IF NOT EXISTS idx_guardrail_violations_phone ON guardrail_violations(phone);
CREATE INDEX IF NOT EXISTS idx_guardrail_violations_type ON guardrail_violations(violation_type);
CREATE INDEX IF NOT EXISTS idx_guardrail_violations_created ON guardrail_violations(created_at);

-- COMMENTS
COMMENT ON TABLE ml_models IS 'Versionamento de modelos de Machine Learning';
COMMENT ON TABLE guardrail_violations IS 'Auditoria de violações do sistema anti-alucinação';
