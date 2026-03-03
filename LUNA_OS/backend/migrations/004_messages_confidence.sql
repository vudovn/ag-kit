-- Migration 004: Add confidence, guardrail and feedback fields to messages
-- Execute no Supabase SQL Editor
-- Campos de automelhoria nas mensagens outbound da LUNA
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(4, 3);
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS guardrail_passed BOOLEAN DEFAULT TRUE;
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS feedback TEXT CHECK (feedback IN ('positive', 'negative'));
-- Comentários
COMMENT ON COLUMN messages.confidence_score IS 'Score 0-1 calculado pelo pipeline de IA';
COMMENT ON COLUMN messages.guardrail_passed IS 'Se a resposta passou na validação dos guardrails';
COMMENT ON COLUMN messages.feedback IS 'Feedback do operador: positive ou negative';
-- Index para queries de feedback (analytics)
CREATE INDEX IF NOT EXISTS idx_messages_feedback ON messages(feedback)
WHERE feedback IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_messages_confidence ON messages(confidence_score)
WHERE confidence_score IS NOT NULL;