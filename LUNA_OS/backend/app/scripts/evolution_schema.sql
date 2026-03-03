-- 🌙 Camada 6: Evolução Contínua (Learning Log)
-- 1. Tabela de Logs de Aprendizado (Learning Log)
CREATE TABLE IF NOT EXISTS public.learning_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    phone TEXT,
    conversation_id UUID REFERENCES public.conversations(id),
    intent TEXT,
    response_content TEXT,
    confidence_score FLOAT,
    audit_flag TEXT,
    -- 'validated', 'uncertain', 'needs_human_review'
    metadata JSONB DEFAULT '{}'::jsonb
);
-- 2. Campos Extras na Tabela de Conversas para Auditoria Rápida
ALTER TABLE public.conversations
ADD COLUMN IF NOT EXISTS audit_status TEXT DEFAULT 'pending',
    ADD COLUMN IF NOT EXISTS maturity_impact FLOAT DEFAULT 0.0;
-- 3. Índices para Performance de Analytics de Evolução
CREATE INDEX IF NOT EXISTS idx_learning_log_audit_flag ON public.learning_log(audit_flag);
CREATE INDEX IF NOT EXISTS idx_learning_log_created_at ON public.learning_log(created_at);
CREATE INDEX IF NOT EXISTS idx_learning_log_phone ON public.learning_log(phone);
-- 4. Comentário de Auditoria
COMMENT ON TABLE public.learning_log IS '🌙 Registro de aprendizado contínuo e auditoria de alma da LUNA.';