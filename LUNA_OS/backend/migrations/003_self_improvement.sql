-- ═══════════════════════════════════════════════
-- LUNA OS — Self-Improvement Tables
-- Padrão MCT: Truth in Data
-- ═══════════════════════════════════════════════
-- Padrões de aprendizado (correções, golden examples, auto-rules)
CREATE TABLE IF NOT EXISTS learning_patterns (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    pattern_type TEXT NOT NULL CHECK (
        pattern_type IN ('correction', 'golden', 'violation', 'auto_rule')
    ),
    trigger_text TEXT,
    wrong_response TEXT,
    correct_response TEXT,
    intent TEXT,
    phone TEXT,
    conversation_id UUID REFERENCES conversations(id) ON DELETE
    SET NULL,
        times_applied INTEGER DEFAULT 0,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMPTZ DEFAULT NOW()
);
-- Violações de guardrails (auditoria de segurança)
CREATE TABLE IF NOT EXISTS guardrail_violations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    phone TEXT,
    conversation_id UUID REFERENCES conversations(id) ON DELETE
    SET NULL,
        violation_type TEXT NOT NULL,
        original_response TEXT,
        corrected_response TEXT,
        source_of_truth TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
);
-- Índices para queries frequentes
CREATE INDEX IF NOT EXISTS idx_learning_patterns_type ON learning_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_learning_patterns_intent ON learning_patterns(intent);
CREATE INDEX IF NOT EXISTS idx_learning_patterns_active ON learning_patterns(active);
CREATE INDEX IF NOT EXISTS idx_guardrail_violations_type ON guardrail_violations(violation_type);
CREATE INDEX IF NOT EXISTS idx_guardrail_violations_phone ON guardrail_violations(phone);
-- RLS (Row Level Security) — opcional, habilitar se necessário
-- ALTER TABLE learning_patterns ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE guardrail_violations ENABLE ROW LEVEL SECURITY;