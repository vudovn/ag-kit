-- 🌙🛡️ LUNA OS: Produção Hardening (Goal 100/100)
-- 1. EXTENSÕES NECESSÁRIAS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 2. ÍNDICES DE PERFORMANCE (Resolvendo Latência >9s)
CREATE INDEX IF NOT EXISTS idx_conversations_phone ON conversations(phone);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_intent ON messages(intent_detected);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category_key ON knowledge_base(category, key);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
-- 3. CAMADA 6: EVOLUÇÃO (Learning Log)
CREATE TABLE IF NOT EXISTS public.learning_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    phone TEXT,
    conversation_id UUID REFERENCES public.conversations(id),
    intent TEXT,
    response_content TEXT,
    confidence_score FLOAT,
    audit_flag TEXT DEFAULT 'pending',
    -- 'validated', 'uncertain', 'needs_human_review'
    metadata JSONB DEFAULT '{}'::jsonb
);
ALTER TABLE public.conversations
ADD COLUMN IF NOT EXISTS audit_status TEXT DEFAULT 'pending',
    ADD COLUMN IF NOT EXISTS maturity_impact FLOAT DEFAULT 0.0;
CREATE INDEX IF NOT EXISTS idx_learning_log_audit_flag ON public.learning_log(audit_flag);
CREATE INDEX IF NOT EXISTS idx_learning_log_created_at ON public.learning_log(created_at);
CREATE INDEX IF NOT EXISTS idx_learning_log_phone ON public.learning_log(phone);
-- 4. CAMADA 7: INTELIGÊNCIA ESTRATÉGICA (CEO Insights)
CREATE TABLE IF NOT EXISTS public.business_intelligence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    phone TEXT,
    conversation_id UUID REFERENCES public.conversations(id),
    insight_text TEXT,
    objections TEXT [],
    -- Array de objeções
    customer_mood TEXT,
    -- 'happy', 'frustrated', 'hurry', 'hesistant'
    urgency_level INTEGER DEFAULT 3,
    -- 1 a 5
    potential_value TEXT,
    -- 'high', 'medium', 'low'
    metadata JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_bi_phone ON public.business_intelligence(phone);
CREATE INDEX IF NOT EXISTS idx_bi_objections ON public.business_intelligence USING GIN(objections);
CREATE INDEX IF NOT EXISTS idx_bi_mood ON public.business_intelligence(customer_mood);
-- 5. DOJO ARENA (Feedback Certificado)
CREATE TABLE IF NOT EXISTS public.dojo_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    scenario_id TEXT NOT NULL,
    persona_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    intent_detected TEXT,
    confidence_score FLOAT,
    success BOOLEAN DEFAULT FALSE,
    rating INTEGER CHECK (
        rating >= 1
        AND rating <= 5
    ),
    comment TEXT,
    metrics JSONB DEFAULT '{}'::jsonb,
    processing_time_ms FLOAT
);
-- 6. VIEWS ANALÍTICAS DO DOJO
CREATE OR REPLACE VIEW dojo_scenario_stats AS
SELECT scenario_id,
    COUNT(*) as total_attempts,
    SUM(
        CASE
            WHEN success THEN 1
            ELSE 0
        END
    ) as success_count,
    ROUND(
        AVG(
            CASE
                WHEN success THEN 100.0
                ELSE 0.0
            END
        )::numeric,
        1
    ) as success_rate,
    ROUND(AVG(rating)::numeric, 2) as avg_rating,
    ROUND(AVG(processing_time_ms)::numeric, 2) as avg_response_time,
    ROUND(
        AVG((metrics->>'empathy_score')::FLOAT)::numeric,
        1
    ) as avg_empathy,
    ROUND(
        AVG((metrics->>'clarity_score')::FLOAT)::numeric,
        1
    ) as avg_clarity,
    ROUND(
        AVG((metrics->>'actionability_score')::FLOAT)::numeric,
        1
    ) as avg_actionability
FROM dojo_feedback
GROUP BY scenario_id;
CREATE OR REPLACE VIEW dojo_leaderboard AS
SELECT scenario_id,
    COUNT(*) as attempts,
    SUM(
        CASE
            WHEN success THEN 1
            ELSE 0
        END
    ) as completions,
    ROUND(
        (
            SUM(
                CASE
                    WHEN success THEN 1
                    ELSE 0
                END
            ) * 100.0 / COUNT(*)
        )::numeric,
        1
    ) as success_rate,
    ROUND(AVG(rating)::numeric, 2) as avg_rating
FROM dojo_feedback
GROUP BY scenario_id
ORDER BY completions DESC,
    success_rate DESC;
-- 7. HEALTH LOGS (Pulse Check)
CREATE TABLE IF NOT EXISTS public.health_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    service TEXT,
    status TEXT,
    details TEXT
);
-- 8. PERMISSÕES BÁSICAS (RLS com Idempotência)
ALTER TABLE public.learning_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.business_intelligence ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dojo_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.health_logs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all for authenticated users" ON public.learning_log;
CREATE POLICY "Enable all for authenticated users" ON public.learning_log FOR ALL USING (true);
DROP POLICY IF EXISTS "Enable all for authenticated users" ON public.business_intelligence;
CREATE POLICY "Enable all for authenticated users" ON public.business_intelligence FOR ALL USING (true);
DROP POLICY IF EXISTS "Enable all for authenticated users" ON public.dojo_feedback;
CREATE POLICY "Enable all for authenticated users" ON public.dojo_feedback FOR ALL USING (true);
DROP POLICY IF EXISTS "Enable all for authenticated users" ON public.health_logs;
CREATE POLICY "Enable all for authenticated users" ON public.health_logs FOR ALL USING (true);
COMMIT;