-- 🌙🥋 LUNA OS DOJO ARENA — Schema Supabase
-- Tabela de Feedback para Evolução
-- 1. Tabela de Feedback do Dojo
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
-- 2. Índices para Performance
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_scenario ON dojo_feedback(scenario_id);
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_persona ON dojo_feedback(persona_id);
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_created ON dojo_feedback(created_at);
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_success ON dojo_feedback(success);
CREATE INDEX IF NOT EXISTS idx_dojo_feedback_rating ON dojo_feedback(rating);
-- 3. View para Estatísticas por Cenário
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
-- 4. View para Estatísticas por Persona
CREATE OR REPLACE VIEW dojo_persona_stats AS
SELECT persona_id,
    COUNT(*) as total_attempts,
    SUM(
        CASE
            WHEN success THEN 1
            ELSE 0
        END
    ) as success_count,
    ROUND(AVG(rating)::numeric, 2) as avg_rating,
    ROUND(
        AVG((metrics->>'empathy_score')::FLOAT)::numeric,
        1
    ) as avg_empathy
FROM dojo_feedback
GROUP BY persona_id;
-- 5. View para Leaderboard Geral
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
-- 6. Comentário de Documentação
COMMENT ON TABLE public.dojo_feedback IS '🥋 Registro de testes e feedback da Dojo Arena para evolução da LUNA.';
COMMENT ON COLUMN dojo_feedback.scenario_id IS 'ID do cenário testado';
COMMENT ON COLUMN dojo_feedback.persona_id IS 'ID da persona usada';
COMMENT ON COLUMN dojo_feedback.rating IS 'Nota do humano (1-5)';
COMMENT ON COLUMN dojo_feedback.metrics IS 'JSON com métricas detalhadas (empathy, clarity, actionability)';