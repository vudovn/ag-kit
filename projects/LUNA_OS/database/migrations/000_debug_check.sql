-- ============================================================
-- DEBUG: Check what tables/columns exist
-- ============================================================
-- Run this FIRST to see what exists
-- ============================================================

-- Check if contacts table exists
SELECT 
    'contacts table exists' as check_name,
    EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'contacts'
    ) as exists;

-- Check if conversations table exists
SELECT 
    'conversations table exists' as check_name,
    EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'conversations'
    ) as exists;

-- Check all existing tables
SELECT
    'existing_tables' as check_name,
    array_agg(table_name) as tables
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE';

-- Check if cache_entries already exists
SELECT 
    'cache_entries exists' as check_name,
    EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'cache_entries'
    ) as exists;
