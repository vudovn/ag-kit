-- 🎯 LUNA OS - Marketing Campaigns & Upsell Migration
-- Data: 2026-03-01
-- Descrição: Cria tabelas para campanhas de marketing e upsell automático
-- ═══════════════════════════════════════════════
-- 0. FUNÇÕES COMPARTILHADAS
-- ═══════════════════════════════════════════════
CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now();
RETURN NEW;
END;
$$ language 'plpgsql';
-- ═══════════════════════════════════════════════
-- 1. TABELA: marketing_campaigns
-- ═══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS marketing_campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  discount_percent DECIMAL(5, 2) DEFAULT 0,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  target_services TEXT [],
  -- Serviços alvo da campanha
  add_on_services TEXT [],
  -- Serviços complementares para upsell
  campaign_script TEXT,
  -- Script de vendas para a campanha
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
-- Index para buscar campanhas ativas por data
CREATE INDEX idx_campaigns_active_dates ON marketing_campaigns(is_active, start_date, end_date);
CREATE INDEX idx_campaigns_target_services ON marketing_campaigns USING GIN(target_services);
-- Trigger para atualizar updated_at
CREATE TRIGGER update_campaigns_updated_at BEFORE
UPDATE ON marketing_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- ═══════════════════════════════════════════════
-- 2. TABELA: upsell_opportunities
-- ═══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS upsell_opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  service_id TEXT NOT NULL,
  service_name TEXT NOT NULL,
  recommended_services TEXT [],
  -- IDs dos serviços recomendados
  recommendation_text TEXT NOT NULL,
  -- Script de vendas
  priority INTEGER DEFAULT 1,
  -- Ordem de prioridade (1 = mais importante)
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
-- Index para buscar upsell por serviço
CREATE INDEX idx_upsell_service_id ON upsell_opportunities(service_id);
CREATE INDEX idx_upsell_active ON upsell_opportunities(is_active);
-- Trigger para atualizar updated_at
CREATE TRIGGER update_upsell_updated_at BEFORE
UPDATE ON upsell_opportunities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- ═══════════════════════════════════════════════
-- 3. DADOS DE EXEMPLO - CAMPANHAS
-- ═══════════════════════════════════════════════
-- Campanha 1: Combo Beleza Completa (Março 2026)
INSERT INTO marketing_campaigns (
    name,
    description,
    discount_percent,
    start_date,
    end_date,
    target_services,
    add_on_services,
    campaign_script
  )
VALUES (
    'Combo Beleza Completa',
    'Faça escova + manicure e ganhe 15% de desconto no pacote!',
    15.00,
    '2026-03-01',
    '2026-03-31',
    ARRAY ['escova_lisa', 'escova_modelada'],
    ARRAY ['manicure', 'pedicure', 'design_sobrancelha'],
    'Enquanto consulto os horários de escova, você sabia que estamos com uma campanha especial? Fazendo escova + manicure juntas, você ganha 15% de desconto! Consigo encaixar tudo no mesmo horário. O que acha?'
  );
-- Campanha 2: Dia da Noiva (Março 2026)
INSERT INTO marketing_campaigns (
    name,
    description,
    discount_percent,
    start_date,
    end_date,
    target_services,
    add_on_services,
    campaign_script
  )
VALUES (
    'Dia da Noiva',
    'Pacote completo noiva com 20% de desconto',
    20.00,
    '2026-03-01',
    '2026-03-31',
    ARRAY ['penteado_premium', 'make_premium'],
    ARRAY ['manicure', 'pedicure', 'design_sobrancelha', 'lash_lifting'],
    'Para seu dia especial, temos o pacote noiva completo! Penteado + make + unhas + sobrancelha com 20% de desconto. Quer que eu verifique a disponibilidade?'
  );
-- Campanha 3: Sobrancelha Perfeita (Março 2026)
INSERT INTO marketing_campaigns (
    name,
    description,
    discount_percent,
    start_date,
    end_date,
    target_services,
    add_on_services,
    campaign_script
  )
VALUES (
    'Sobrancelha Perfeita',
    'Design + Brow Lamination com 10% de desconto',
    10.00,
    '2026-03-01',
    '2026-03-31',
    ARRAY ['design_sobrancelha'],
    ARRAY ['brow_lamination', 'lash_lifting'],
    'Enquanto isso, você sabia que o Brow Lamination está com 10% de desconto? Fica incrível junto com o design! Quer adicionar?'
  );
-- ═══════════════════════════════════════════════
-- 4. DADOS DE EXEMPLO - UPSELL OPPORTUNITIES
-- ═══════════════════════════════════════════════
-- Upsell para Escova Lisa
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'escova_lisa',
    'Escova Lisa',
    ARRAY ['manicure', 'pedicure', 'design_sobrancelha'],
    'Enquanto consulto os horários de escova, você sabia que conseguimos encaixar também sua manicure e pedicure no mesmo horário? Assim você já sai completa! O que acha?',
    1
  );
-- Upsell para Escova Modelada
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'escova_modelada',
    'Escova Modelada',
    ARRAY ['manicure', 'design_sobrancelha', 'lash_lifting'],
    'Perfeito! Enquanto verifico os horários de escova modelada, que tal já deixar as unhas e sobrancelhas em dia? Consigo encaixar tudo junto!',
    1
  );
-- Upsell para Penteado
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'penteado_basico',
    'Penteado',
    ARRAY ['make_basica', 'design_sobrancelha', 'manicure'],
    'Ótima escolha! Para seu evento ficar perfeito, que tal adicionar maquiagem e sobrancelha? Temos um pacote especial para eventos!',
    1
  );
-- Upsell para Manicure
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'manicure',
    'Manicure',
    ARRAY ['pedicure', 'gel_maos'],
    'Já que vai fazer as unhas das mãos, que tal aproveitar e fazer os pés também? E temos o gel que dura até 3 semanas! Quer que eu verifique os horários?',
    1
  );
-- Upsell para Design de Sobrancelha
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'design_sobrancelha',
    'Design de Sobrancelha',
    ARRAY ['brow_lamination', 'lash_lifting'],
    'Perfeito! Enquanto isso, você conheceu nosso Brow Lamination? Dura até 6 semanas e deixa as sobrancelhas perfeitas! Quer adicionar?',
    2
  );
-- Upsell para Progressiva
INSERT INTO upsell_opportunities (
    service_id,
    service_name,
    recommended_services,
    recommendation_text,
    priority
  )
VALUES (
    'progressiva_curtos',
    'Progressiva',
    ARRAY ['manicure', 'pedicure', 'design_sobrancelha', 'hidratacao'],
    'Excelente escolha! A progressiva leva um tempinho, que tal já deixar unhas e sobrancelhas prontas? E temos hidratação especial pós-progressiva com 15% de desconto!',
    1
  );
-- ═══════════════════════════════════════════════
-- 5. FUNÇÕES UTILITÁRIAS
-- ═══════════════════════════════════════════════
-- Função para buscar campanhas ativas
CREATE OR REPLACE FUNCTION get_active_campaigns() RETURNS TABLE (
    id UUID,
    name TEXT,
    description TEXT,
    discount_percent DECIMAL,
    start_date DATE,
    end_date DATE,
    campaign_script TEXT
  ) AS $$ BEGIN RETURN QUERY
SELECT mc.id,
  mc.name,
  mc.description,
  mc.discount_percent,
  mc.start_date,
  mc.end_date,
  mc.campaign_script
FROM marketing_campaigns mc
WHERE mc.is_active = true
  AND mc.start_date <= CURRENT_DATE
  AND mc.end_date >= CURRENT_DATE
ORDER BY mc.discount_percent DESC;
END;
$$ LANGUAGE plpgsql;
-- Função para buscar upsell por serviço
CREATE OR REPLACE FUNCTION get_upsell_for_service(p_service_id TEXT) RETURNS TABLE (
    service_name TEXT,
    recommended_services TEXT [],
    recommendation_text TEXT,
    priority INTEGER
  ) AS $$ BEGIN RETURN QUERY
SELECT uo.service_name,
  uo.recommended_services,
  uo.recommendation_text,
  uo.priority
FROM upsell_opportunities uo
WHERE uo.service_id = p_service_id
  AND uo.is_active = true
ORDER BY uo.priority ASC;
END;
$$ LANGUAGE plpgsql;
-- ═══════════════════════════════════════════════
-- 6. PERMISSÕES (se necessário)
-- ═══════════════════════════════════════════════
-- Conceder permissão de leitura para service_role
GRANT SELECT ON marketing_campaigns TO service_role;
GRANT SELECT ON upsell_opportunities TO service_role;
-- ═══════════════════════════════════════════════
-- FIM DA MIGRATION
-- ═══════════════════════════════════════════════
-- Verificar se tudo foi criado
SELECT 'marketing_campaigns' as table_name,
  COUNT(*) as row_count
FROM marketing_campaigns
UNION ALL
SELECT 'upsell_opportunities',
  COUNT(*)
FROM upsell_opportunities;