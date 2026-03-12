-- ============================================================
-- LUNA OS + Multi-Brain V2 — Supabase Migration (CORRIGIDO)
-- ============================================================
-- Version: 2.0.1 - Fixed for existing schemas
-- Date: 2026-03-12
-- Description: Safe migration that checks existing tables/columns
-- How to apply: Run in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- 1. CHECK EXISTING TABLES
-- ============================================================

-- Check if contacts table exists and get actual column name
DO $$
DECLARE
    contacts_exists boolean;
    contact_id_exists boolean;
BEGIN
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'contacts'
    ) INTO contacts_exists;
    
    IF contacts_exists THEN
        SELECT EXISTS (
            SELECT FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = 'contacts' 
            AND column_name = 'id'
        ) INTO contact_id_exists;
        
        RAISE NOTICE '✅ Table contacts exists with id column';
    ELSE
        RAISE NOTICE '⚠️ Table contacts does not exist - will use conversations table';
    END IF;
END $$;


-- ============================================================
-- 2. SMART CACHING TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS cache_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cache_key VARCHAR(500) UNIQUE NOT NULL,
    cache_value JSONB NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cache_entries_key ON cache_entries(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_entries_expires ON cache_entries(expires_at);
CREATE INDEX IF NOT EXISTS idx_cache_entries_accessed ON cache_entries(last_accessed);

DO $$ BEGIN RAISE NOTICE '✅ Table cache_entries created/verified'; END $$;


-- ============================================================
-- 3. HUMAN HANDOFF TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS handoff_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID,  -- References conversations(id)
    contact_id UUID,       -- References contacts(id) or NULL
    reason VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    status VARCHAR(50) DEFAULT 'pending',
    context_summary TEXT,
    ai_attempts INTEGER DEFAULT 0,
    last_ai_response TEXT,
    customer_messages TEXT[],
    assigned_to VARCHAR(255),
    accepted_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_handoff_requests_conversation ON handoff_requests(conversation_id);
CREATE INDEX IF NOT EXISTS idx_handoff_requests_status ON handoff_requests(status);
CREATE INDEX IF NOT EXISTS idx_handoff_requests_priority ON handoff_requests(priority DESC);
CREATE INDEX IF NOT EXISTS idx_handoff_requests_created ON handoff_requests(created_at DESC);

DO $$ BEGIN RAISE NOTICE '✅ Table handoff_requests created/verified'; END $$;


-- ============================================================
-- 4. MEMORY CHAIN TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS memory_chain (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interaction_id VARCHAR(255) UNIQUE NOT NULL,
    contact_id UUID,  -- Can be NULL if contacts table doesn't exist
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    data JSONB NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    current_hash VARCHAR(64) NOT NULL,
    verified BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_memory_chain_interaction ON memory_chain(interaction_id);
CREATE INDEX IF NOT EXISTS idx_memory_chain_contact ON memory_chain(contact_id);
CREATE INDEX IF NOT EXISTS idx_memory_chain_timestamp ON memory_chain(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_memory_chain_hash ON memory_chain(current_hash);

DO $$ BEGIN RAISE NOTICE '✅ Table memory_chain created/verified'; END $$;


-- ============================================================
-- 5. BEHAVIORAL DNA TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS behavioral_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID UNIQUE,  -- Can be NULL
    tone VARCHAR(50) DEFAULT 'professional',
    vocabulary VARCHAR(50) DEFAULT 'standard',
    emoji_usage VARCHAR(50) DEFAULT 'moderate',
    response_length VARCHAR(50) DEFAULT 'medium',
    formality_level INTEGER DEFAULT 6 CHECK (formality_level BETWEEN 1 AND 10),
    common_phrases TEXT[] DEFAULT '{}',
    topics_of_interest TEXT[] DEFAULT '{}',
    communication_style VARCHAR(50) DEFAULT 'balanced',
    decision_speed VARCHAR(50) DEFAULT 'medium',
    interaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_behavioral_dna_contact ON behavioral_dna(contact_id);

DO $$ BEGIN RAISE NOTICE '✅ Table behavioral_dna created/verified'; END $$;


-- ============================================================
-- 6. BRAIN DECISIONS TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS brain_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID,
    contact_id UUID,
    brain_type VARCHAR(50) NOT NULL,
    model_used VARCHAR(100),
    confidence DECIMAL(5,4),
    reason TEXT,
    estimated_cost DECIMAL(10,6),
    estimated_latency_ms INTEGER,
    actual_latency_ms INTEGER,
    actual_cost DECIMAL(10,6),
    tokens_used INTEGER,
    outcome_status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_brain_decisions_conversation ON brain_decisions(conversation_id);
CREATE INDEX IF NOT EXISTS idx_brain_decisions_brain_type ON brain_decisions(brain_type);
CREATE INDEX IF NOT EXISTS idx_brain_decisions_created ON brain_decisions(created_at DESC);

DO $$ BEGIN RAISE NOTICE '✅ Table brain_decisions created/verified'; END $$;


-- ============================================================
-- 7. ANALYTICS TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    contact_id UUID,
    conversation_id UUID,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_timestamp ON analytics_events(event_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_events_contact ON analytics_events(contact_id);

DO $$ BEGIN RAISE NOTICE '✅ Table analytics_events created/verified'; END $$;


-- ============================================================
-- 8. FEATURE FLAGS
-- ============================================================

CREATE TABLE IF NOT EXISTS feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_name VARCHAR(100) UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    config JSONB DEFAULT '{}',
    description TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default flags (ignore if exists)
INSERT INTO feature_flags (flag_name, enabled, description) VALUES
    ('FEATURE_SMART_CACHE', TRUE, 'Smart Caching with TTL'),
    ('FEATURE_HANDOFF', TRUE, 'Human Handoff System'),
    ('FEATURE_MULTI_BRAIN', TRUE, 'Multi-Brain Router'),
    ('FEATURE_BEHAVIORAL_DNA', TRUE, 'Behavioral DNA Personalization'),
    ('FEATURE_MEMORY_CHAIN', TRUE, 'Memory Chain Audit Trail'),
    ('FEATURE_ANALYTICS', TRUE, 'Analytics Dashboard'),
    ('FEATURE_LUX_DASHBOARD', TRUE, 'LUX Dashboard UI')
ON CONFLICT (flag_name) DO NOTHING;

DO $$ BEGIN RAISE NOTICE '✅ Table feature_flags created/verified with 7 flags'; END $$;


-- ============================================================
-- 9. VIEWS FOR ANALYTICS
-- ============================================================

-- Daily metrics view
CREATE OR REPLACE VIEW daily_metrics AS
SELECT
    DATE(event_timestamp) AS metric_date,
    event_type,
    COUNT(*) AS event_count
FROM analytics_events
GROUP BY DATE(event_timestamp), event_type
ORDER BY metric_date DESC;

DO $$ BEGIN RAISE NOTICE '✅ View daily_metrics created/verified'; END $$;


-- Cache performance view
CREATE OR REPLACE VIEW cache_performance AS
SELECT
    DATE(created_at) AS metric_date,
    COUNT(*) FILTER (WHERE metadata->>'cache_status' = 'hit') AS hits,
    COUNT(*) FILTER (WHERE metadata->>'cache_status' = 'miss') AS misses,
    ROUND(
        COUNT(*) FILTER (WHERE metadata->>'cache_status' = 'hit') * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS hit_rate_percent
FROM analytics_events
WHERE event_type IN ('cache_hit', 'cache_miss')
GROUP BY DATE(created_at)
ORDER BY metric_date DESC;

DO $$ BEGIN RAISE NOTICE '✅ View cache_performance created/verified'; END $$;


-- Handoff metrics view
CREATE OR REPLACE VIEW handoff_metrics AS
SELECT
    DATE(created_at) AS metric_date,
    COUNT(*) AS total_handoffs,
    COUNT(*) FILTER (WHERE status = 'accepted') AS accepted,
    COUNT(*) FILTER (WHERE status = 'resolved') AS resolved,
    ROUND(
        COUNT(*) FILTER (WHERE status = 'accepted') * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS acceptance_rate_percent,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (accepted_at - created_at))) FILTER (WHERE accepted_at IS NOT NULL),
        2
    ) AS avg_time_to_accept_seconds
FROM handoff_requests
GROUP BY DATE(created_at)
ORDER BY metric_date DESC;

DO $$ BEGIN RAISE NOTICE '✅ View handoff_metrics created/verified'; END $$;


-- Brain routing metrics view
CREATE OR REPLACE VIEW brain_routing_metrics AS
SELECT
    DATE(created_at) AS metric_date,
    brain_type,
    COUNT(*) AS routing_count,
    ROUND(AVG(confidence), 4) AS avg_confidence,
    ROUND(AVG(actual_latency_ms), 2) AS avg_latency_ms,
    ROUND(SUM(actual_cost)::numeric, 6) AS total_cost_usd
FROM brain_decisions
GROUP BY DATE(created_at), brain_type
ORDER BY metric_date DESC, brain_type;

DO $$ BEGIN RAISE NOTICE '✅ View brain_routing_metrics created/verified'; END $$;


-- ============================================================
-- 10. FINAL VERIFICATION
-- ============================================================

DO $$
DECLARE
    table_count integer;
BEGIN
    SELECT COUNT(*)
    INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name IN (
        'cache_entries',
        'handoff_requests',
        'memory_chain',
        'behavioral_dna',
        'brain_decisions',
        'analytics_events',
        'feature_flags'
    );
    
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ MIGRATION COMPLETED SUCCESSFULLY!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tables created/verified: %', table_count;
    RAISE NOTICE 'Views created: 4';
    RAISE NOTICE 'Feature flags: 7';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Verify: SELECT * FROM feature_flags;';
    RAISE NOTICE '2. Test frontend: http://localhost:3000/lux';
    RAISE NOTICE '========================================';
END $$;


-- ============================================================
-- END OF MIGRATION
-- ============================================================
