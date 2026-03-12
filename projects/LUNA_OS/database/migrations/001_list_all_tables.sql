-- ============================================================
-- DEBUG COMPLETO: Check ALL tables
-- ============================================================
-- Run this to see ALL existing tables
-- ============================================================

-- List all tables in public schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
