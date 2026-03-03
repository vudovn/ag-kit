-- 🌙 Camada de Inteligência Estratégica (CEO Insights)
-- 1. Tabela de Inteligência de Negócio
CREATE TABLE IF NOT EXISTS public.business_intelligence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    phone TEXT,
    conversation_id UUID REFERENCES public.conversations(id),
    insight_text TEXT,
    -- Insight qualitativo profundo
    objections TEXT [],
    -- Array de objeções (preço, horário, confiança, etc)
    customer_mood TEXT,
    -- 'happy', 'frustrated', 'hurry', 'hesistant'
    urgency_level INTEGER DEFAULT 3,
    -- 1 (Baixa) a 5 (Crítica)
    potential_value TEXT,
    -- 'high', 'medium', 'low'
    metadata JSONB DEFAULT '{}'::jsonb
);
-- 2. Índices para Analytics
CREATE INDEX IF NOT EXISTS idx_bi_phone ON public.business_intelligence(phone);
CREATE INDEX IF NOT EXISTS idx_bi_objections ON public.business_intelligence USING GIN(objections);
CREATE INDEX IF NOT EXISTS idx_bi_mood ON public.business_intelligence(customer_mood);
-- 3. Comentário de Governança
COMMENT ON TABLE public.business_intelligence IS '💎 Inteligência estratégica extraída semânticamente das conversas para visão de CEO.';