-- ═══════════════════════════════════════════════
-- Migration 009: Seed Data
-- LUNA OS v3.0 - Dados iniciais
-- ═══════════════════════════════════════════════

-- System Settings defaults
INSERT INTO system_settings (key, value, description) VALUES
  ('luna_mode', '"active"', 'Modo de operação: active ou observe'),
  ('debug', 'false', 'Habilitar debug mode'),
  ('rate_limit_public', '"30/minute"', 'Rate limit para endpoints públicos'),
  ('rate_limit_webhook', '"1000/minute"', 'Rate limit para webhooks'),
  ('cache_ttl_seconds', '5', 'TTL do cache de settings dinâmicos')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();

-- Knowledge Base - FAQ básica
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
  ('faq', 'saudacao', '{
    "question": "Oi / Olá / Bom dia",
    "answer": "Oi! Sou a Luna, assistente da Haven Escovaria & Esmalteria. Em que posso te ajudar hoje? ✨"
  }'::jsonb, true),
  ('faq', 'localizacao', '{
    "question": "Onde fica / Endereço",
    "answer": "Estamos na Rua Mato Grosso, 837E - Jardim Itália, Chapecó-SC. Temos estacionamento em frente! 🚗"
  }'::jsonb, true),
  ('faq', 'horario_funcionamento', '{
    "question": "Horário de funcionamento",
    "answer": "Funcionamos de Segunda a Sábado, das 8h às 20h. 🕒"
  }'::jsonb, true),
  ('faq', 'servicos', '{
    "question": "Quais serviços vocês oferecem?",
    "answer": "Oferecemos: Escovas, Penteados, Tratamentos, Unhas (Manicure/Pedicure/Gel), Maquiagem, Sobrancelhas, Cílios (Lash Lifting), e muito mais! Qual serviço você gostaria de agendar? 💅"
  }'::jsonb, true),
  ('services', 'escova_simples', '{
    "name": "Escova Simples",
    "description": "Escova modeladora básica",
    "duration_min": 30,
    "price": 50.00
  }'::jsonb, true),
  ('services', 'manicure', '{
    "name": "Manicure",
    "description": "Cutilagem e esmaltação",
    "duration_min": 40,
    "price": 35.00
  }'::jsonb, true)
ON CONFLICT (category, key) DO UPDATE SET data = EXCLUDED.data, is_active = EXCLUDED.is_active, updated_at = NOW();

-- Campaigns exemplo (opcionais)
INSERT INTO campaigns (name, type, status, discount_percent, trigger_keywords, message_template) VALUES
  ('Primeira Visita', 'acquisition', 'draft', 15, 
   ARRAY['primeira vez', 'conhecer', 'indicacao'],
   'Que bom te ter aqui! 🌸 Para sua primeira visita, temos 15% de desconto. Vamos agendar?')
ON CONFLICT DO NOTHING;
