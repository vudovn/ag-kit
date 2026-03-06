-- ═══════════════════════════════════════════════
-- LUNA CORE v3.0 - Migrations Index
-- ═══════════════════════════════════════════════
-- Execute as migrations em ordem numérica
-- 
-- Uso:
--   1. No Supabase SQL Editor
--   2. Execute cada arquivo em ordem (001 → 010)
--   3. Ou execute: psql -f migrations/001_*.sql
-- ═══════════════════════════════════════════════

-- Enable UUID extension (obrigatório)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
