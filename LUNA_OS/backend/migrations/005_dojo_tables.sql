-- ═══════════════════════════════════════════════
-- Migration 005: Dojo Arena Tables
-- LUNA OS v3.0 - Simulação e Treinamento
-- ═══════════════════════════════════════════════

-- DOJO SIMULATIONS
CREATE TABLE IF NOT EXISTS dojo_simulations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scenario_name TEXT NOT NULL,
  scenario_type TEXT DEFAULT 'custom',
  customer_profile JSONB,
  conversation_flow JSONB DEFAULT '[]',
  expected_outcomes JSONB,
  actual_outcomes JSONB,
  score DECIMAL(5,2),
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- DOJO EDGE CASES
CREATE TABLE IF NOT EXISTS dojo_edge_cases (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category TEXT NOT NULL,
  trigger_pattern TEXT,
  expected_response TEXT,
  actual_response TEXT,
  difficulty_level INT DEFAULT 1,
  is_resolved BOOLEAN DEFAULT FALSE,
  resolution_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- DOJO LEARNING CYCLES
CREATE TABLE IF NOT EXISTS dojo_learning_cycles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cycle_number INT UNIQUE NOT NULL,
  start_date TIMESTAMPTZ NOT NULL,
  end_date TIMESTAMPTZ,
  conversations_analyzed INT DEFAULT 0,
  patterns_discovered INT DEFAULT 0,
  learnings_applied INT DEFAULT 0,
  status TEXT DEFAULT 'pending',
  summary JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- INDEXES - Dojo Tables
CREATE INDEX IF NOT EXISTS idx_dojo_simulations_status ON dojo_simulations(status);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_category ON dojo_edge_cases(category);
CREATE INDEX IF NOT EXISTS idx_dojo_edge_cases_resolved ON dojo_edge_cases(is_resolved);
CREATE INDEX IF NOT EXISTS idx_dojo_learning_cycles_number ON dojo_learning_cycles(cycle_number);

-- COMMENTS
COMMENT ON TABLE dojo_simulations IS 'Simulações de atendimento para treinamento';
COMMENT ON TABLE dojo_edge_cases IS 'Casos extremos detectados para melhoria';
COMMENT ON TABLE dojo_learning_cycles IS 'Ciclos semanais de aprendizado automático';
