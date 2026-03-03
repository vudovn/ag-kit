im - LUNA OS: Security Sprint - Phase 1 -- Habilitar RLS estrito e revogar acessos públicos de escrita
BEGIN;
-- 1. Habilitar RLS em todas as tabelas
ALTER TABLE public.knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dojo_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prompt_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversation_intelligence ENABLE ROW LEVEL SECURITY;
-- 2. Limpar políticas abertas (caso existam) para garantir que negamos por padrão
-- No script 01_infra_evolution.sql havia uma policy que deixava leitura/escrita aberta para todos
DROP POLICY IF EXISTS "Service role access" ON public.prompt_proposals;
DROP POLICY IF EXISTS "Service role access" ON public.conversation_intelligence;
DROP POLICY IF EXISTS "Service role access" ON public.dojo_edge_cases;
DROP POLICY IF EXISTS "Service role access" ON public.health_checks;
-- Drop qualquer policy publica existente
DROP POLICY IF EXISTS "Allow public read access" ON public.knowledge_base;
DROP POLICY IF EXISTS "Allow public read access" ON public.campaigns;
-- 3. Frontend (anon) - APENAS LEITURA nas tabelas públicas
CREATE POLICY "Allow public read access" ON public.knowledge_base FOR
SELECT TO anon USING (true);
CREATE POLICY "Allow public read access" ON public.campaigns FOR
SELECT TO anon USING (true);
-- 4. Backend (service_role) - ACESSO TOTAL
-- Service_role geralmente possui bypassrls, mas por garantia criamos a policy explícita
CREATE POLICY "Service Role Full Access" ON public.knowledge_base FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.campaigns FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.clients FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.conversations FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.messages FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.dojo_feedback FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.prompt_proposals FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.conversation_intelligence FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.dojo_edge_cases FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service Role Full Access" ON public.health_checks FOR ALL TO service_role USING (true) WITH CHECK (true);
COMMIT;