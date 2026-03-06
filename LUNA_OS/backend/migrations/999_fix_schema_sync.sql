-- ═══════════════════════════════════════════════
-- Migration 999: Fix Schema Sync (Emergency Patch)
-- LUNA OS v3.0 - Correção de campos faltantes
-- ═══════════════════════════════════════════════
-- 1. CORREÇÃO: appointments.campaign_id
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'appointments'
        AND COLUMN_NAME = 'campaign_id'
) THEN
ALTER TABLE appointments
ADD COLUMN campaign_id UUID REFERENCES campaigns(id) ON DELETE
SET NULL;
END IF;
END $$;
-- 2. CORREÇÃO: dojo_simulations
CREATE TABLE IF NOT EXISTS dojo_simulations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scenario_name TEXT NOT NULL,
    scenario_type TEXT DEFAULT 'custom',
    customer_profile JSONB,
    conversation_flow JSONB DEFAULT '[]',
    expected_outcomes JSONB,
    actual_outcomes JSONB,
    score DECIMAL(5, 2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);
-- 3. CORREÇÃO: funnel_stage em conversation_intelligence
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'conversation_intelligence'
) THEN CREATE TABLE conversation_intelligence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    funnel_stage TEXT DEFAULT 'awareness',
    conversion_probability DECIMAL(5, 4) DEFAULT 0,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ELSIF NOT EXISTS (
    SELECT 1
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'conversation_intelligence'
        AND COLUMN_NAME = 'funnel_stage'
) THEN
ALTER TABLE conversation_intelligence
ADD COLUMN funnel_stage TEXT DEFAULT 'awareness';
END IF;
END $$;
-- 4. RE-CRIAR VIEW campaign_stats_summary (Fix 010)
DROP VIEW IF EXISTS campaign_stats_summary;
CREATE OR REPLACE VIEW campaign_stats_summary AS
SELECT c.id,
    c.name,
    c.status,
    c.discount_percent,
    COUNT(
        DISTINCT CASE
            WHEN a.campaign_id = c.id THEN a.id
        END
    ) AS appointments_count,
    COALESCE(SUM(a.price), 0) AS total_revenue
FROM campaigns c
    LEFT JOIN appointments a ON a.campaign_id = c.id
GROUP BY c.id,
    c.name,
    c.status,
    c.discount_percent;
-- 5. NOTA: O erro de 'category' em query SQL pode referir-se a knowledge_base.
-- Garantindo integridade de knowledge_base:
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'knowledge_base'
        AND COLUMN_NAME = 'category'
) THEN
ALTER TABLE knowledge_base
ADD COLUMN category TEXT NOT NULL DEFAULT 'general';
END IF;
END $$;