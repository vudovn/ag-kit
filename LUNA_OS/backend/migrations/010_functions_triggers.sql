-- ═══════════════════════════════════════════════
-- Migration 010: Functions & Triggers
-- LUNA OS v3.0 - Funções utilitárias e automações
-- ═══════════════════════════════════════════════

-- Função: Atualizar timestamp automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger em tabelas com updated_at
CREATE TRIGGER update_knowledge_base_updated_at
  BEFORE UPDATE ON knowledge_base
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ml_models_updated_at
  BEFORE UPDATE ON ml_models
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at
  BEFORE UPDATE ON system_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Função: Incrementar contador de mensagens na conversa
CREATE OR REPLACE FUNCTION increment_conversation_messages_count()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations 
  SET messages_count = messages_count + 1 
  WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_message_insert
  AFTER INSERT ON messages
  FOR EACH ROW EXECUTE FUNCTION increment_conversation_messages_count();

-- Função: Calcular idade do cliente em dias
CREATE OR REPLACE FUNCTION client_age_days(client clients)
RETURNS BIGINT AS $$
BEGIN
  RETURN EXTRACT(EPOCH FROM (NOW() - client.first_contact)) / 86400;
END;
$$ LANGUAGE plpgsql STABLE;

-- Função: Buscar última conversa de um cliente
CREATE OR REPLACE FUNCTION get_last_conversation(client_phone TEXT)
RETURNS TABLE (
  id UUID,
  status TEXT,
  started_at TIMESTAMPTZ,
  messages_count INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT c.id, c.status, c.started_at, c.messages_count
  FROM conversations c
  WHERE c.phone = client_phone
  ORDER BY c.started_at DESC
  LIMIT 1;
END;
$$ LANGUAGE plpgsql STABLE;

-- View: Conversas ativas com dados do cliente
CREATE OR REPLACE VIEW active_conversations_with_clients AS
SELECT 
  c.id,
  c.phone,
  c.status,
  c.intent,
  c.sentiment,
  c.messages_count,
  c.started_at,
  cl.name AS client_name,
  cl.tags,
  cl.total_visits,
  cl.total_spent
FROM conversations c
LEFT JOIN clients cl ON c.client_id = cl.id
WHERE c.status = 'active'
ORDER BY c.started_at DESC;

-- View: Agendamentos do dia
CREATE OR REPLACE VIEW todays_appointments AS
SELECT 
  a.id,
  a.date,
  a.time,
  a.service_name,
  a.professional_name,
  a.status,
  a.price,
  cl.name AS client_name,
  cl.phone AS client_phone
FROM appointments a
LEFT JOIN clients cl ON a.client_id = cl.id
WHERE a.date = CURRENT_DATE
ORDER BY a.time;

-- View: Estatísticas de campanhas
CREATE OR REPLACE VIEW campaign_stats_summary AS
SELECT 
  c.id,
  c.name,
  c.status,
  c.discount_percent,
  COUNT(DISTINCT CASE WHEN a.campaign_id = c.id THEN a.id END) AS appointments_count,
  COALESCE(SUM(a.price), 0) AS total_revenue
FROM campaigns c
LEFT JOIN appointments a ON a.campaign_id = c.id
GROUP BY c.id, c.name, c.status, c.discount_percent;

COMMENT ON FUNCTION update_updated_at_column() IS 'Atualiza coluna updated_at automaticamente';
COMMENT ON FUNCTION increment_conversation_messages_count() IS 'Incrementa contador de mensagens na conversa';
COMMENT ON FUNCTION client_age_days(clients) IS 'Calcula idade do cliente em dias desde primeiro contato';
COMMENT ON FUNCTION get_last_conversation(TEXT) IS 'Retorna última conversa de um cliente pelo phone';
COMMENT ON VIEW active_conversations_with_clients IS 'Conversas ativas com dados completos do cliente';
COMMENT ON VIEW todays_appointments IS 'Agendamentos do dia atual';
COMMENT ON VIEW campaign_stats_summary IS 'Estatísticas resumidas de campanhas';
