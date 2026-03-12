-- ============================================================
-- LUNA OS + Multi-Brain V2 Integration
-- ============================================================
-- Apply these migrations to integrate Multi-Brain V2 features
-- into existing LUNA OS installation
-- ============================================================

-- ============================================================
-- 1. MULTI-BRAIN V2 TABLES (if not exists)
-- ============================================================

-- Cache entries for Smart Caching
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


-- Handoff requests for Human Handoff
CREATE TABLE IF NOT EXISTS handoff_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    reason VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    status VARCHAR(50) DEFAULT 'pending',
    context_summary TEXT,
    ai_attempts INTEGER DEFAULT 0,
    assigned_to VARCHAR(255),
    accepted_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_handoff_requests_conversation ON handoff_requests(conversation_id);
CREATE INDEX IF NOT EXISTS idx_handoff_requests_status ON handoff_requests(status);
CREATE INDEX IF NOT EXISTS idx_handoff_requests_priority ON handoff_requests(priority DESC);


-- Memory Chain for Audit Trail (SHA-256)
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


-- Behavioral DNA for Personalization
CREATE TABLE IF NOT EXISTS behavioral_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE UNIQUE,
    tone VARCHAR(50) DEFAULT 'professional',
    vocabulary VARCHAR(50) DEFAULT 'standard',
    emoji_usage VARCHAR(50) DEFAULT 'moderate',
    response_length VARCHAR(50) DEFAULT 'medium',
    formality_level INTEGER DEFAULT 6 CHECK (formality_level BETWEEN 1 AND 10),
    communication_style VARCHAR(50) DEFAULT 'balanced',
    interaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_behavioral_dna_contact ON behavioral_dna(contact_id);


-- Brain Decisions for Multi-Brain Routing
CREATE TABLE IF NOT EXISTS brain_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    brain_type VARCHAR(50) NOT NULL,
    model_used VARCHAR(100),
    confidence DECIMAL(5,4),
    actual_latency_ms INTEGER,
    actual_cost DECIMAL(10,6),
    outcome_status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_brain_decisions_conversation ON brain_decisions(conversation_id);
CREATE INDEX IF NOT EXISTS idx_brain_decisions_brain_type ON brain_decisions(brain_type);


-- Analytics Events
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


-- ============================================================
-- 2. FEATURE FLAGS
-- ============================================================

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
    ('FEATURE_ANALYTICS', TRUE, 'Analytics Dashboard')
ON CONFLICT (flag_name) DO NOTHING;


-- ============================================================
-- 3. VIEWS FOR ANALYTICS
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
    ) AS acceptance_rate_percent
FROM handoff_requests
GROUP BY DATE(created_at)
ORDER BY metric_date DESC;


-- ============================================================
-- 4. COMMENTS
-- ============================================================

COMMENT ON TABLE cache_entries IS 'Smart Caching - Reduces API calls by 100x';
COMMENT ON TABLE handoff_requests IS 'Human Handoff - Automatic escalation to humans';
COMMENT ON TABLE memory_chain IS 'Memory Chain - SHA-256 audit trail (LGPD compliance)';
COMMENT ON TABLE behavioral_dna IS 'Behavioral DNA - Customer personalization';
COMMENT ON TABLE brain_decisions IS 'Multi-Brain Router - Intelligent AI routing';
COMMENT ON TABLE analytics_events IS 'Analytics Dashboard - Real-time metrics';
COMMENT ON TABLE feature_flags IS 'Feature Flags - Runtime configuration';


-- ============================================================
-- END OF MIGRATION
-- ============================================================

COMMENT ON SCHEMA public IS 'LUNA OS + Multi-Brain V2 Integrated';
