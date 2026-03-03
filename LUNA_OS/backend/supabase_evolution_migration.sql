-- LUNA OS Evolution - Migration Script
-- Data: 2026-03-01
-- Descrição: Cria tabelas para Dojo Learning Cycle, Conversation Intelligence e Edge Cases
-- ============================================
-- TABELA 1: prompt_proposals (Dojo Learning)
-- ============================================
CREATE TABLE IF NOT EXISTS prompt_proposals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  week_reference TEXT NOT NULL,
  -- ex: "2026-W09"
  failure_category TEXT NOT NULL,
  -- INTENT, TONE, INFORMATION, FLOW, ESCALATION
  failure_count INTEGER NOT NULL DEFAULT 0,
  affected_scenarios TEXT [],
  -- IDs dos cenários que falharam
  current_prompt_excerpt TEXT,
  -- trecho atual do system prompt relacionado
  proposed_change TEXT NOT NULL,
  -- o que mudar e por quê
  proposed_text TEXT,
  -- texto pronto para inserir no prompt
  insert_after TEXT,
  -- título da seção onde inserir
  justification TEXT,
  -- por que essa mudança resolve as falhas
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  approved_by TEXT,
  approved_at TIMESTAMP WITH TIME ZONE,
  rejected_by TEXT,
  rejected_at TIMESTAMP WITH TIME ZONE,
  rejection_reason TEXT
);
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_prompt_proposals_status ON prompt_proposals(status);
CREATE INDEX IF NOT EXISTS idx_prompt_proposals_week ON prompt_proposals(week_reference);
CREATE INDEX IF NOT EXISTS idx_prompt_proposals_category ON prompt_proposals(failure_category);
CREATE INDEX IF NOT EXISTS idx_prompt_proposals_created ON prompt_proposals(created_at DESC);
-- Comments
COMMENT ON TABLE prompt_proposals IS 'Propostas de melhoria do system prompt da LUNA baseadas em falhas do Dojo';
COMMENT ON COLUMN prompt_proposals.failure_category IS 'Categoria da falha: INTENT, TONE, INFORMATION, FLOW, ESCALATION';
COMMENT ON COLUMN prompt_proposals.status IS 'Status: pending (aguardando revisão), approved (aplicado), rejected (rejeitado)';
-- ============================================
-- TABELA 2: conversation_intelligence
-- ============================================
CREATE TABLE IF NOT EXISTS conversation_intelligence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  processed_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  -- extractor_agent
  services_mentioned TEXT [],
  professionals_mentioned TEXT [],
  dates_mentioned TEXT [],
  times_mentioned TEXT [],
  price_sensitivity TEXT CHECK (price_sensitivity IN ('low', 'medium', 'high')),
  -- psychology_agent  
  emotional_state TEXT CHECK (
    emotional_state IN (
      'happy',
      'frustrated',
      'anxious',
      'neutral',
      'angry',
      'hesitant'
    )
  ),
  communication_style TEXT,
  trust_level TEXT CHECK (
    trust_level IN ('new', 'building', 'established', 'loyal')
  ),
  personality_type TEXT,
  -- DISC type: D, I, S, C
  -- behavior_agent
  preferred_professional TEXT,
  preferred_time_of_day TEXT,
  booking_pattern TEXT CHECK (
    booking_pattern IN ('spontaneous', 'planner', 'last_minute')
  ),
  -- sales_agent
  upsell_opportunities TEXT [],
  objections_raised TEXT [],
  conversion_likelihood TEXT CHECK (
    conversion_likelihood IN ('low', 'medium', 'high')
  ),
  funnel_stage TEXT,
  -- insights_agent
  key_insights TEXT [],
  recommended_actions TEXT [],
  -- learning_agent
  luna_performance_notes TEXT,
  improvement_suggestions TEXT [],
  -- metadata
  processing_time_ms INTEGER,
  agents_executed TEXT [],
  processing_errors TEXT []
);
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_conversation ON conversation_intelligence(conversation_id);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_client ON conversation_intelligence(client_id);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_processed ON conversation_intelligence(processed_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_emotional ON conversation_intelligence(emotional_state);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_trust ON conversation_intelligence(trust_level);
-- Comments
COMMENT ON TABLE conversation_intelligence IS 'Análise inteligente de conversas via agentes especializados';
COMMENT ON COLUMN conversation_intelligence.price_sensitivity IS 'Sensibilidade do cliente a preço: low (não se importa), medium (compara), high (sempre pede desconto)';
COMMENT ON COLUMN conversation_intelligence.trust_level IS 'Nível de confiança na LUNA: new (primeira interação), building, established, loyal';
-- ============================================
-- TABELA 3: dojo_edge_cases
-- ============================================
CREATE TABLE IF NOT EXISTS dojo_edge_cases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  source_conversation_id UUID REFERENCES conversations(id),
  client_phone TEXT,
  situation_description TEXT NOT NULL,
  -- o que aconteceu
  why_luna_failed TEXT,
  -- por que a LUNA não resolveu
  expected_behavior TEXT,
  -- como deveria ter respondido
  suggested_scenario_name TEXT,
  -- nome sugerido para o cenário
  suggested_scenario_level TEXT CHECK (
    suggested_scenario_level IN ('beginner', 'intermediate', 'advanced', 'expert')
  ),
  status TEXT DEFAULT 'new' CHECK (
    status IN (
      'new',
      'under_review',
      'added_to_dojo',
      'dismissed'
    )
  ),
  scenario_id TEXT,
  -- ID do cenário criado no Dojo, se aplicável
  reviewed_by TEXT,
  reviewed_at TIMESTAMP WITH TIME ZONE,
  review_notes TEXT
);
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_status ON dojo_edge_cases(status);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_created ON dojo_edge_cases(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_conversation ON dojo_edge_cases(source_conversation_id);
-- Comments
COMMENT ON TABLE dojo_edge_cases IS 'Casos extremos onde a LUNA falhou e precisam virar cenários de treino no Dojo';
COMMENT ON COLUMN dojo_edge_cases.status IS 'new (aguardando revisão), under_review (sendo analisado), added_to_dojo (virou cenário), dismissed (não será usado)';
-- ============================================
-- TABELA 4: health_checks (Monitoramento)
-- ============================================
CREATE TABLE IF NOT EXISTS health_checks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  service_name TEXT NOT NULL,
  -- evolution, supabase, openrouter, belasis
  status TEXT NOT NULL CHECK (status IN ('healthy', 'degraded', 'unhealthy')),
  response_time_ms INTEGER,
  error_message TEXT,
  details JSONB
);
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_health_checks_service ON health_checks(service_name);
CREATE INDEX IF NOT EXISTS idx_health_checks_created ON health_checks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_health_checks_status ON health_checks(status);
-- Comments
COMMENT ON TABLE health_checks IS 'Health checks periódicos das integrações externas';
-- ============================================
-- TABELA 5: dojo_feedback (para Learning Cycle)
-- ============================================
-- Esta tabela pode já existir, mas vamos garantir que tem os campos necessários
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS failure_category TEXT;
-- ex: INTENT, TONE, etc.
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS scenario_name TEXT;
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS persona_name TEXT;
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS luna_response TEXT;
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS metrics JSONB;
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS processed_for_learning BOOLEAN DEFAULT FALSE;
ALTER TABLE dojo_feedback
ADD COLUMN IF NOT EXISTS processed_at TIMESTAMP WITH TIME ZONE;
-- Index para feedbacks não processados
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_unprocessed ON dojo_feedback(processed_for_learning)
WHERE processed_for_learning = FALSE;
-- Comments
COMMENT ON COLUMN dojo_feedback.processed_for_learning IS 'Se true, este feedback já foi processado pelo Learning Cycle';
-- ============================================
-- VIEW: conversation_intelligence_summary
-- ============================================
CREATE OR REPLACE VIEW conversation_intelligence_summary AS
SELECT DATE_TRUNC('day', ci.processed_at) AS day,
  ci.emotional_state,
  ci.trust_level,
  ci.conversion_likelihood,
  COUNT(*) AS count,
  AVG(
    CASE
      WHEN ci.conversion_likelihood = 'high' THEN 3
      WHEN ci.conversion_likelihood = 'medium' THEN 2
      WHEN ci.conversion_likelihood = 'low' THEN 1
      ELSE 0
    END
  ) AS avg_conversion_score
FROM conversation_intelligence ci
GROUP BY DATE_TRUNC('day', ci.processed_at),
  ci.emotional_state,
  ci.trust_level,
  ci.conversion_likelihood
ORDER BY day DESC,
  count DESC;
COMMENT ON VIEW conversation_intelligence_summary IS 'Resumo diário das inteligências de conversas para dashboards';
-- ============================================
-- VIEW: weekly_failure_summary
-- ============================================
CREATE OR REPLACE VIEW weekly_failure_summary AS
SELECT DATE_TRUNC('week', df.created_at) AS week_start,
  TO_CHAR(DATE_TRUNC('week', df.created_at), 'YYYY-"W"IW') AS week_reference,
  df.failure_category,
  COUNT(*) AS failure_count,
  AVG(df.rating) AS avg_rating,
  ARRAY_AGG(DISTINCT df.scenario_id) AS affected_scenarios
FROM dojo_feedback df
WHERE df.rating <= 3
GROUP BY DATE_TRUNC('week', df.created_at),
  TO_CHAR(DATE_TRUNC('week', df.created_at), 'YYYY-"W"IW'),
  df.failure_category
ORDER BY week_start DESC,
  failure_count DESC;
COMMENT ON VIEW weekly_failure_summary IS 'Resumo semanal de falhas do Dojo para gerar propostas de melhoria';
-- ============================================
-- FUNÇÃO: update_client_from_intelligence
-- ============================================
CREATE OR REPLACE FUNCTION update_client_from_intelligence() RETURNS TRIGGER AS $$ BEGIN -- Atualiza preferências do cliente baseado na inteligência
UPDATE clients
SET preferences = COALESCE(preferences, '{}'::JSONB) || jsonb_build_object(
    'professional',
    NEW.preferred_professional,
    'time_of_day',
    NEW.preferred_time_of_day,
    'communication_style',
    NEW.communication_style,
    'last_updated',
    NOW()
  ),
  tags = ARRAY_CAT(
    COALESCE(tags, '{}'::TEXT []),
    CASE
      WHEN NEW.trust_level = 'loyal' THEN ARRAY ['cliente_fiel']
      WHEN NEW.trust_level = 'established' THEN ARRAY ['cliente_estabelecido']
      ELSE '{}'::TEXT []
    END
  )
WHERE id = NEW.client_id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION update_client_from_intelligence IS 'Trigger function para atualizar perfil do cliente quando nova inteligência é processada';
-- ============================================
-- TRIGGER: auto_update_client_on_intelligence
-- ============================================
CREATE TRIGGER auto_update_client_on_intelligence
AFTER
INSERT ON conversation_intelligence FOR EACH ROW
  WHEN (
    NEW.preferred_professional IS NOT NULL
    OR NEW.trust_level IS NOT NULL
  ) EXECUTE FUNCTION update_client_from_intelligence();
-- ============================================
-- INSERT: Dados iniciais de exemplo
-- ============================================
-- Inserir um health check inicial para cada serviço
INSERT INTO health_checks (service_name, status, details)
VALUES (
    'evolution',
    'healthy',
    '{"message": "Service initialized"}'
  ),
  (
    'supabase',
    'healthy',
    '{"message": "Database connected"}'
  ),
  (
    'openrouter',
    'healthy',
    '{"message": "API configured"}'
  ),
  (
    'belasis',
    'degraded',
    '{"message": "Mock mode active"}'
  ) ON CONFLICT DO NOTHING;
-- ============================================
-- PERMISSÕES (RLS - Row Level Security)
-- ============================================
-- Habilitar RLS nas tabelas novas
ALTER TABLE prompt_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_intelligence ENABLE ROW LEVEL SECURITY;
ALTER TABLE dojo_edge_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_checks ENABLE ROW LEVEL SECURITY;
-- Políticas de leitura (service_role pode ler tudo)
CREATE POLICY "Service role has full access to prompt_proposals" ON prompt_proposals FOR ALL USING (auth.jwt()->>'role' = 'service_role');
CREATE POLICY "Service role has full access to conversation_intelligence" ON conversation_intelligence FOR ALL USING (auth.jwt()->>'role' = 'service_role');
CREATE POLICY "Service role has full access to dojo_edge_cases" ON dojo_edge_cases FOR ALL USING (auth.jwt()->>'role' = 'service_role');
CREATE POLICY "Service role has full access to health_checks" ON health_checks FOR ALL USING (auth.jwt()->>'role' = 'service_role');
-- ============================================
-- FIM DA MIGRAÇÃO
-- ============================================
-- Verificar se tudo foi criado
DO $$
DECLARE table_count INTEGER;
BEGIN
SELECT COUNT(*) INTO table_count
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'prompt_proposals',
    'conversation_intelligence',
    'dojo_edge_cases',
    'health_checks'
  );
IF table_count = 4 THEN RAISE NOTICE '✅ Migration completed successfully! 4 tables created.';
ELSE RAISE WARNING '⚠️ Migration may be incomplete. Only % of 4 tables found.',
table_count;
END IF;
END $$;