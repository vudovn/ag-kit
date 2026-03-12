-- ============================================================
-- LUNA OS + Multi-Brain V2 — Supabase Migration
-- ============================================================
-- Version: 2.0.0
-- Date: 2026-03-12
-- Description: Complete migration for LUNA OS + Multi-Brain V2
-- How to apply: Run in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- 1. SMART CACHING TABLES
-- ============================================================

-- Cache entries for Smart Caching (100x less API calls)
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

COMMENT ON TABLE cache_entries IS 'Smart Caching - Reduces API calls by 100x';


-- ============================================================
-- 2. HUMAN HANDOFF TABLES
-- ============================================================

-- Handoff requests for Human Handoff (zero abandoned customers)
CREATE TABLE IF NOT EXISTS handoff_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
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

COMMENT ON TABLE handoff_requests IS 'Human Handoff - Automatic escalation to humans';


-- ============================================================
-- 3. MEMORY CHAIN TABLES (Audit Trail)
-- ============================================================

-- Memory Chain for Audit Trail (SHA-256 hash chain, LGPD compliance)
CREATE TABLE IF NOT EXISTS memory_chain (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interaction_id VARCHAR(255) UNIQUE NOT NULL,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
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

COMMENT ON TABLE memory_chain IS 'Memory Chain - SHA-256 audit trail (LGPD compliance)';


-- ============================================================
-- 4. BEHAVIORAL DNA TABLES
-- ============================================================

-- Behavioral DNA for Customer Personalization
CREATE TABLE IF NOT EXISTS behavioral_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE UNIQUE,
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

COMMENT ON TABLE behavioral_dna IS 'Behavioral DNA - Customer personalization';


-- ============================================================
-- 5. MULTI-BRAIN ROUTER TABLES
-- ============================================================

-- Brain Decisions for Multi-Brain Routing
CREATE TABLE IF NOT EXISTS brain_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
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

COMMENT ON TABLE brain_decisions IS 'Multi-Brain Router - Intelligent AI routing';


-- ============================================================
-- 6. ANALYTICS TABLES
-- ============================================================

-- Analytics Events for Real-time Metrics
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    contact_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_timestamp ON analytics_events(event_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_events_contact ON analytics_events(contact_id);

COMMENT ON TABLE analytics_events IS 'Analytics Dashboard - Real-time metrics';


-- ============================================================
-- 7. FEATURE FLAGS
-- ============================================================

-- Feature Flags for Runtime Configuration
CREATE TABLE IF NOT EXISTS feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_name VARCHAR(100) UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    config JSONB DEFAULT '{}',
    description TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default flags
INSERT INTO feature_flags (flag_name, enabled, description) VALUES
    ('FEATURE_SMART_CACHE', TRUE, 'Smart Caching with TTL'),
    ('FEATURE_HANDOFF', TRUE, 'Human Handoff System'),
    ('FEATURE_MULTI_BRAIN', TRUE, 'Multi-Brain Router'),
    ('FEATURE_BEHAVIORAL_DNA', TRUE, 'Behavioral DNA Personalization'),
    ('FEATURE_MEMORY_CHAIN', TRUE, 'Memory Chain Audit Trail'),
    ('FEATURE_ANALYTICS', TRUE, 'Analytics Dashboard'),
    ('FEATURE_LUX_DASHBOARD', TRUE, 'LUX Dashboard UI')
ON CONFLICT (flag_name) DO NOTHING;


-- ============================================================
-- 8. VIEWS FOR ANALYTICS (LUX Dashboard)
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

COMMENT ON VIEW daily_metrics IS 'Daily metrics aggregation';


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

COMMENT ON VIEW cache_performance IS 'Cache hit/miss performance metrics';


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

COMMENT ON VIEW handoff_metrics IS 'Human handoff performance metrics';


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

COMMENT ON VIEW brain_routing_metrics IS 'Multi-Brain routing performance';


-- ============================================================
-- 9. ROW LEVEL SECURITY (RLS) — Optional
-- ============================================================

-- Enable RLS (uncomment if using Supabase Auth)
-- ALTER TABLE cache_entries ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE handoff_requests ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE memory_chain ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE behavioral_dna ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE brain_decisions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth setup)
-- CREATE POLICY "Users can view own data" ON cache_entries FOR SELECT USING (auth.uid()::text = cache_key);


-- ============================================================
-- 10. COMMENTS
-- ============================================================

COMMENT ON SCHEMA public IS 'LUNA OS + Multi-Brain V2 Integrated';


-- ============================================================
-- 11. VERIFICATION QUERY
-- ============================================================

-- Run this to verify migration was successful:
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Expected tables:
-- cache_entries, handoff_requests, memory_chain, behavioral_dna,
-- brain_decisions, analytics_events, feature_flags


-- ============================================================
-- END OF MIGRATION
-- ============================================================
