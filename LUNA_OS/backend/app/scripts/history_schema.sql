-- 🌙 Camada de Memória Profunda: Histórico Massivo WhatsApp
-- 1. Tabela de Histórico Bruto (Raw History)
CREATE TABLE IF NOT EXISTS public.whatsapp_messages_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    message_id TEXT UNIQUE,
    -- ID único da mensagem vindo da Evolution API
    phone TEXT NOT NULL,
    sender_name TEXT,
    content TEXT,
    direction TEXT CHECK (direction IN ('inbound', 'outbound')),
    message_timestamp TIMESTAMPTZ NOT NULL,
    is_group BOOLEAN DEFAULT FALSE,
    instance_name TEXT DEFAULT 'haven',
    metadata JSONB DEFAULT '{}'::jsonb
);
-- 2. Tabela de Consolidação de Diagnóstico Financeiro
CREATE TABLE IF NOT EXISTS public.financial_diagnostic (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    period_start DATE,
    period_end DATE,
    total_leads INTEGER,
    converted_leads INTEGER,
    potential_revenue NUMERIC(12, 2),
    actual_revenue NUMERIC(12, 2),
    estimated_loss NUMERIC(12, 2),
    top_lost_services TEXT [],
    -- Array de serviços mais mencionados em perdas
    diagnostic_report TEXT,
    -- Relatório qualitativo gerado por IA
    metadata JSONB DEFAULT '{}'::jsonb
);
-- 3. Índices Estratégicos
CREATE INDEX IF NOT EXISTS idx_wmh_phone ON public.whatsapp_messages_history(phone);
CREATE INDEX IF NOT EXISTS idx_wmh_timestamp ON public.whatsapp_messages_history(message_timestamp);
CREATE INDEX IF NOT EXISTS idx_wmh_is_group ON public.whatsapp_messages_history(is_group);
-- 4. Governança
COMMENT ON TABLE public.whatsapp_messages_history IS '📜 Repositório de histórico massivo sincronizado da Evolution API.';
COMMENT ON TABLE public.financial_diagnostic IS '📊 Resultados de auditoria financeira e diagnóstico de perdas históricas.';