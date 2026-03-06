-- ═══════════════════════════════════════════════
-- Migration 008: Storage Buckets
-- LUNA OS v3.0 - Configuração de Storage
-- ═══════════════════════════════════════════════

-- Criar bucket para modelos de ML (DEBT #7)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'models',
  'models',
  false,
  104857600, -- 100MB max
  ARRAY['application/octet-stream', 'application/octet-stream']
)
ON CONFLICT (id) DO NOTHING;

-- Criar bucket para áudio de conversas (opcional)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'conversations',
  'conversations',
  false,
  52428800, -- 50MB max
  ARRAY['audio/*', 'text/plain']
)
ON CONFLICT (id) DO NOTHING;

-- Criar bucket para exports de relatórios
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'exports',
  'exports',
  false,
  10485760, -- 10MB max
  ARRAY['application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv']
)
ON CONFLICT (id) DO NOTHING;

-- Policy: Service role tem acesso total aos buckets
CREATE POLICY "Service role has full access to models"
ON storage.objects FOR ALL
USING (bucket_id = 'models' AND auth.jwt() ->> 'role' = 'service_role')
WITH CHECK (bucket_id = 'models' AND auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role has full access to conversations"
ON storage.objects FOR ALL
USING (bucket_id = 'conversations' AND auth.jwt() ->> 'role' = 'service_role')
WITH CHECK (bucket_id = 'conversations' AND auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role has full access to exports"
ON storage.objects FOR ALL
USING (bucket_id = 'exports' AND auth.jwt() ->> 'role' = 'service_role')
WITH CHECK (bucket_id = 'exports' AND auth.jwt() ->> 'role' = 'service_role');
