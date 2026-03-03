-- LUNA OS Evolution - Migration Script
-- Data: 2026-03-01
-- Descrição: Cria tabelas para Dojo Learning Cycle, Conversation Intelligence e Edge Cases
-- ============================================
-- 0. FUNÇÕES COMPARTILHADAS
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now();
RETURN NEW;
END;
$$ language 'plpgsql';
-- ============================================
-- TABELA 0: knowledge_base (Garantir estrutura e unicidade)
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
-- Garantir unicidade da coluna 'key' para permitir UPSERT
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'knowledge_base_key_unique'
) THEN -- Limpeza preventiva de possíveis duplicatas antes de criar a restrição
DELETE FROM knowledge_base a USING knowledge_base b
WHERE a.id < b.id
    AND a.key = b.key;
ALTER TABLE knowledge_base
ADD CONSTRAINT knowledge_base_key_unique UNIQUE (key);
END IF;
END $$;
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category_key ON knowledge_base(category, key);
-- ============================================
-- TABELA 1: prompt_proposals (Dojo Learning)
-- ============================================
CREATE TABLE IF NOT EXISTS prompt_proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    week_reference TEXT NOT NULL,
    failure_category TEXT NOT NULL,
    failure_count INTEGER NOT NULL DEFAULT 0,
    affected_scenarios TEXT [],
    current_prompt_excerpt TEXT,
    proposed_change TEXT NOT NULL,
    proposed_text TEXT,
    insert_after TEXT,
    justification TEXT,
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
-- ============================================
-- TABELA 2: conversation_intelligence
-- ============================================
CREATE TABLE IF NOT EXISTS conversation_intelligence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID,
    -- Removido FK rigoroso para facilitar seed inicial
    client_id UUID,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    services_mentioned TEXT [],
    professionals_mentioned TEXT [],
    dates_mentioned TEXT [],
    times_mentioned TEXT [],
    price_sensitivity TEXT CHECK (price_sensitivity IN ('low', 'medium', 'high')),
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
    preferred_professional TEXT,
    preferred_time_of_day TEXT,
    booking_pattern TEXT CHECK (
        booking_pattern IN ('spontaneous', 'planner', 'last_minute')
    ),
    upsell_opportunities TEXT [],
    objections_raised TEXT [],
    conversion_likelihood TEXT CHECK (
        conversion_likelihood IN ('low', 'medium', 'high')
    ),
    funnel_stage TEXT,
    key_insights TEXT [],
    recommended_actions TEXT [],
    luna_performance_notes TEXT,
    improvement_suggestions TEXT [],
    processing_time_ms INTEGER,
    agents_executed TEXT [],
    processing_errors TEXT []
);
-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_processed ON conversation_intelligence(processed_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_emotional ON conversation_intelligence(emotional_state);
CREATE INDEX IF NOT EXISTS idx_conversation_intelligence_trust ON conversation_intelligence(trust_level);
-- ============================================
-- TABELA 3: dojo_edge_cases
-- ============================================
CREATE TABLE IF NOT EXISTS dojo_edge_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    source_conversation_id UUID,
    client_phone TEXT,
    situation_description TEXT NOT NULL,
    why_luna_failed TEXT,
    expected_behavior TEXT,
    suggested_scenario_name TEXT,
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
    reviewed_by TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_status ON dojo_edge_cases(status);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_created ON dojo_edge_cases(created_at DESC);
-- ============================================
-- TABELA 4: health_checks
-- ============================================
CREATE TABLE IF NOT EXISTS health_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    service_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('healthy', 'degraded', 'unhealthy')),
    response_time_ms INTEGER,
    error_message TEXT,
    details JSONB
);
CREATE INDEX IF NOT EXISTS idx_health_checks_service ON health_checks(service_name);
CREATE INDEX IF NOT EXISTS idx_health_checks_created ON health_checks(created_at DESC);
-- ============================================
-- TABELA 5: dojo_feedback
-- ============================================
CREATE TABLE IF NOT EXISTS dojo_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    rating INTEGER,
    feedback TEXT,
    scenario_id TEXT,
    failure_category TEXT,
    scenario_name TEXT,
    persona_name TEXT,
    luna_response TEXT,
    metrics JSONB,
    processed_for_learning BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_unprocessed ON dojo_feedback(processed_for_learning)
WHERE processed_for_learning = FALSE;
-- ============================================
-- PERMISSÕES
-- ============================================
ALTER TABLE prompt_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_intelligence ENABLE ROW LEVEL SECURITY;
ALTER TABLE dojo_edge_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_checks ENABLE ROW LEVEL SECURITY;
-- Políticas simplificadas para service_role
DROP POLICY IF EXISTS "Service role access" ON prompt_proposals;
CREATE POLICY "Service role access" ON prompt_proposals FOR ALL USING (true);
DROP POLICY IF EXISTS "Service role access" ON conversation_intelligence;
CREATE POLICY "Service role access" ON conversation_intelligence FOR ALL USING (true);
DROP POLICY IF EXISTS "Service role access" ON dojo_edge_cases;
CREATE POLICY "Service role access" ON dojo_edge_cases FOR ALL USING (true);
DROP POLICY IF EXISTS "Service role access" ON health_checks;
CREATE POLICY "Service role access" ON health_checks FOR ALL USING (true);