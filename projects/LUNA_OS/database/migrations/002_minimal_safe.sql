-- ============================================================
-- LUNA OS — Multi-Brain V2 Tables (ULTRA SEGURO)
-- ============================================================
-- Version: 2.0.2 - Ultra Safe - NO foreign keys
-- Date: 2026-03-12
-- Description: Creates ONLY new tables without any dependencies
-- ============================================================

-- ============================================================
-- 1. CACHE ENTRIES (Smart Caching)
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

CREATE INDEX IF NOT EXISTS idx_cache_key ON cache_entries(cache_key);


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

-- Insert flags (ignore duplicates)
INSERT INTO feature_flags (flag_name, enabled, description) VALUES
    ('FEATURE_SMART_CACHE', TRUE, 'Smart Caching'),
    ('FEATURE_HANDOFF', TRUE, 'Human Handoff'),
    ('FEATURE_MULTI_BRAIN', TRUE, 'Multi-Brain Router'),
    ('FEATURE_BEHAVIORAL_DNA', TRUE, 'Behavioral DNA'),
    ('FEATURE_MEMORY_CHAIN', TRUE, 'Memory Chain'),
    ('FEATURE_ANALYTICS', TRUE, 'Analytics'),
    ('FEATURE_LUX_DASHBOARD', TRUE, 'LUX Dashboard')
ON CONFLICT (flag_name) DO NOTHING;


-- ============================================================
-- VERIFICATION
-- ============================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ TABLES CREATED SUCCESSFULLY!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tables: cache_entries, feature_flags';
    RAISE NOTICE 'Feature flags: 7';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Verify: SELECT * FROM feature_flags;';
    RAISE NOTICE '========================================';
END $$;
