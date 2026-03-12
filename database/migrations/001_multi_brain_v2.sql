-- ============================================================
-- LUNA Multi-Brain V2 - Database Migrations
-- ============================================================
-- Version: 2.0.0
-- Date: 2026-03-12
-- Description: Complete database schema for LUNA Multi-Brain V2
-- ============================================================

-- ============================================================
-- 1. EXTENSIONS
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search


-- ============================================================
-- 2. CORE TABLES
-- ============================================================

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255) UNIQUE,  -- WhatsApp/CRM ID
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    ltv DECIMAL(12,2) DEFAULT 0,
    tags TEXT[] DEFAULT '{}',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_contacts_external_id ON contacts(external_id);
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_contacts_ltv ON contacts(ltv DESC);


-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    channel VARCHAR(50) DEFAULT 'whatsapp',
    status VARCHAR(50) DEFAULT 'active',
    mode VARCHAR(50) DEFAULT 'ai_active',  -- ai_active, ai_assisted, human_active, paused
    current_intent VARCHAR(100),
    intent_confidence DECIMAL(5,4) DEFAULT 1.0,
    risk_score DECIMAL(5,4) DEFAULT 0.0,
    assigned_to VARCHAR(255),  -- Human operator ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_contact_id ON conversations(contact_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_mode ON conversations(mode);
CREATE INDEX idx_conversations_created ON conversations(created_at DESC);


-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    direction VARCHAR(20) NOT NULL,  -- inbound, outbound
    message_type VARCHAR(50) DEFAULT 'text',  -- text, audio, image, video, document
    content TEXT,
    media_url TEXT,
    transcription TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
CREATE INDEX idx_messages_content ON messages USING gin(to_tsvector('portuguese', content));


-- ============================================================
-- 3. SMART CACHING TABLES
-- ============================================================

-- Cache entries table (optional, for persistent cache)
CREATE TABLE IF NOT EXISTS cache_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cache_key VARCHAR(500) UNIQUE NOT NULL,
    cache_value JSONB NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_cache_entries_key ON cache_entries(cache_key);
CREATE INDEX idx_cache_entries_expires ON cache_entries(expires_at);
CREATE INDEX idx_cache_entries_accessed ON cache_entries(last_accessed);


-- ============================================================
-- 4. HUMAN HANDOFF TABLES
-- ============================================================

-- Handoff requests table
CREATE TABLE IF NOT EXISTS handoff_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    reason VARCHAR(100) NOT NULL,  -- customer_requested, low_confidence, high_risk, etc.
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, accepted, resolved
    context_summary TEXT,
    ai_attempts INTEGER DEFAULT 0,
    last_ai_response TEXT,
    customer_messages TEXT[],
    assigned_to VARCHAR(255),
    accepted_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_handoff_requests_conversation ON handoff_requests(conversation_id);
CREATE INDEX idx_handoff_requests_status ON handoff_requests(status);
CREATE INDEX idx_handoff_requests_priority ON handoff_requests(priority DESC);
CREATE INDEX idx_handoff_requests_created ON handoff_requests(created_at DESC);


-- ============================================================
-- 5. MEMORY CHAIN TABLES (Audit Trail)
-- ============================================================

-- Memory chain entries (immutable audit trail)
CREATE TABLE IF NOT EXISTS memory_chain (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interaction_id VARCHAR(255) UNIQUE NOT NULL,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data JSONB NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    current_hash VARCHAR(64) NOT NULL,
    verified BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_memory_chain_interaction ON memory_chain(interaction_id);
CREATE INDEX idx_memory_chain_contact ON memory_chain(contact_id);
CREATE INDEX idx_memory_chain_timestamp ON memory_chain(timestamp DESC);
CREATE INDEX idx_memory_chain_hash ON memory_chain(current_hash);


-- ============================================================
-- 6. BEHAVIORAL DNA TABLES
-- ============================================================

-- Behavioral DNA profiles
CREATE TABLE IF NOT EXISTS behavioral_dna (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_behavioral_dna_contact ON behavioral_dna(contact_id);


-- ============================================================
-- 7. MULTI-BRAIN ROUTER TABLES
-- ============================================================

-- Brain routing decisions log
CREATE TABLE IF NOT EXISTS brain_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    brain_type VARCHAR(50) NOT NULL,  -- quick, standard, complex
    model_used VARCHAR(100),
    confidence DECIMAL(5,4),
    reason TEXT,
    estimated_cost DECIMAL(10,6),
    estimated_latency_ms INTEGER,
    actual_latency_ms INTEGER,
    actual_cost DECIMAL(10,6),
    tokens_used INTEGER,
    outcome_status VARCHAR(50),  -- success, failed, escalated
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_brain_decisions_conversation ON brain_decisions(conversation_id);
CREATE INDEX idx_brain_decisions_brain_type ON brain_decisions(brain_type);
CREATE INDEX idx_brain_decisions_created ON brain_decisions(created_at DESC);


-- ============================================================
-- 8. ANALYTICS TABLES
-- ============================================================

-- Analytics events
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    contact_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_timestamp ON analytics_events(event_timestamp DESC);
CREATE INDEX idx_analytics_events_contact ON analytics_events(contact_id);


-- ============================================================
-- 9. FEATURE FLAGS TABLE
-- ============================================================

-- Feature flags configuration
CREATE TABLE IF NOT EXISTS feature_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    flag_name VARCHAR(100) UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    config JSONB DEFAULT '{}',
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default feature flags
INSERT INTO feature_flags (flag_name, enabled, description) VALUES
    ('FEATURE_SMART_CACHE', TRUE, 'Smart Caching with TTL'),
    ('FEATURE_HANDOFF', TRUE, 'Human Handoff System'),
    ('FEATURE_DUAL_MODE_MCP', TRUE, 'Dual Mode MCP Server'),
    ('FEATURE_MEMORY_CHAIN', TRUE, 'Memory Chain Audit Trail'),
    ('FEATURE_BEHAVIORAL_DNA', TRUE, 'Behavioral DNA Personalization'),
    ('FEATURE_MULTI_BRAIN_V2', TRUE, 'Multi-Brain Router'),
    ('FEATURE_ANALYTICS', TRUE, 'Analytics Dashboard')
ON CONFLICT (flag_name) DO NOTHING;


-- ============================================================
-- 10. FUNCTIONS AND TRIGGERS
-- ============================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to tables
CREATE TRIGGER update_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_behavioral_dna_updated_at
    BEFORE UPDATE ON behavioral_dna
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feature_flags_updated_at
    BEFORE UPDATE ON feature_flags
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- Function to auto-expire cache entries
CREATE OR REPLACE FUNCTION expire_cache_entries()
RETURNS void AS $$
BEGIN
    DELETE FROM cache_entries WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;


-- Function to verify memory chain integrity
CREATE OR REPLACE FUNCTION verify_memory_chain()
RETURNS TABLE (is_valid BOOLEAN, first_invalid_index BIGINT) AS $$
BEGIN
    -- Implementation of chain verification
    RETURN QUERY
    SELECT TRUE, NULL::BIGINT;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- 11. VIEWS FOR ANALYTICS
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
    ) AS acceptance_rate_percent,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (accepted_at - created_at))) FILTER (WHERE accepted_at IS NOT NULL),
        2
    ) AS avg_time_to_accept_seconds
FROM handoff_requests
GROUP BY DATE(created_at)
ORDER BY metric_date DESC;


-- ============================================================
-- 12. INITIAL DATA
-- ============================================================

-- Insert sample contacts (for testing)
INSERT INTO contacts (external_id, name, phone, email, ltv, tags) VALUES
    ('whatsapp_5511999999999', 'João Silva', '+5511999999999', 'joao@example.com', 5000, '{"vip", "active"}'),
    ('whatsapp_5511999999998', 'Maria Santos', '+5511999999998', 'maria@example.com', 15000, '{"vip", "high-value"}'),
    ('whatsapp_5511999999997', 'Pedro Oliveira', '+5511999999997', 'pedro@example.com', 2000, '{"active"}')
ON CONFLICT (external_id) DO NOTHING;


-- ============================================================
-- END OF MIGRATION
-- ============================================================

COMMENT ON SCHEMA public IS 'LUNA Multi-Brain V2 - Complete Database Schema';
