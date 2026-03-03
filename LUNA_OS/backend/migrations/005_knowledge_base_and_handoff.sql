-- Migration 005: Knowledge Base and Handoff Columns
-- Execute no Supabase SQL Editor
-- ═══════════════════════════════════════════════
-- LUNA OS — Knowledge Base
-- Centraliza serviços, preços, regras e dados de profissionais
-- ═══════════════════════════════════════════════
-- 1. Criação da tabela de base de conhecimento com Multi-tenancy support
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id TEXT NOT NULL DEFAULT 'default',
    -- Para Multi-tenancy
    category TEXT NOT NULL CHECK (
        category IN ('service', 'professional', 'rule', 'faq')
    ),
    title TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    -- Apenas para as categorias de serviço
    duration_minutes INTEGER,
    -- Apenas para as categorias de serviço
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
-- Indices
CREATE INDEX IF NOT EXISTS idx_knowledge_base_tenant ON knowledge_base(tenant_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category ON knowledge_base(category);
COMMENT ON TABLE knowledge_base IS 'Centraliza todo o conhecimento que a IA deve saber para responder aos clientes (substitui Obsidian)';
-- 2. Alterações adicionais nas mensagens para controle Handoff
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS handled_by TEXT DEFAULT 'ai' CHECK (handled_by IN ('ai', 'human'));
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS handoff_reason TEXT;
COMMENT ON COLUMN messages.handled_by IS 'Flag para identificar quem enviou a mensagem (IA ou Humano assumiu)';
COMMENT ON COLUMN messages.handoff_reason IS 'Motivo do handoff (caso a IA peça ajuda)';
-- 3. Atualizar a tabela de conversas para refletir estado de Handoff ativo
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS needs_human_intervention BOOLEAN DEFAULT FALSE;
COMMENT ON COLUMN conversations.needs_human_intervention IS 'Indica se a conversa está aguardando o operador assumir';