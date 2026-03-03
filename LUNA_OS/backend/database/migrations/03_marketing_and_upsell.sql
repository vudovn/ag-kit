-- 🎯 LUNA OS - Marketing Campaigns & Upsell Migration
-- Data: 2026-03-01
-- Descrição: Cria tabelas para campanhas de marketing e upsell automático
-- ═══════════════════════════════════════════════
-- 0. FUNÇÕES COMPARTILHADAS (Garantir existência)
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
    add_on_services TEXT [],
    campaign_script TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
-- Index para buscar campanhas ativas por data (CORRIGIDO COM IF NOT EXISTS)
CREATE INDEX IF NOT EXISTS idx_campaigns_active_dates ON marketing_campaigns(is_active, start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_campaigns_target_services ON marketing_campaigns USING GIN(target_services);
-- Trigger para atualizar updated_at (DROP FIRST TO BE IDEMPOTENT)
DROP TRIGGER IF EXISTS update_campaigns_updated_at ON marketing_campaigns;
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
    recommendation_text TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
-- Index para buscar upsell por serviço (CORRIGIDO COM IF NOT EXISTS)
CREATE INDEX IF NOT EXISTS idx_upsell_service_id ON upsell_opportunities(service_id);
CREATE INDEX IF NOT EXISTS idx_upsell_active ON upsell_opportunities(is_active);
-- Trigger para atualizar updated_at (DROP FIRST TO BE IDEMPOTENT)
DROP TRIGGER IF EXISTS update_upsell_updated_at ON upsell_opportunities;
CREATE TRIGGER update_upsell_updated_at BEFORE
UPDATE ON upsell_opportunities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- ═══════════════════════════════════════════════
-- 3. DADOS DE EXEMPLO - CAMPANHAS (IDEMPOTENTE COM DELETE PREVIOUS)
-- ═══════════════════════════════════════════════
-- Limpar exemplos anteriores para evitar duplicidade no re-run
DELETE FROM marketing_campaigns
WHERE name IN (
        'Combo Beleza Completa',
        'Dia da Noiva',
        'Sobrancelha Perfeita'
    );
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
    ),
    (
        'Dia da Noiva',
        'Pacote completo noiva com 20% de desconto',
        20.00,
        '2026-03-01',
        '2026-03-31',
        ARRAY ['penteado_premium', 'make_premium'],
        ARRAY ['manicure', 'pedicure', 'design_sobrancelha', 'lash_lifting'],
        'Para seu dia especial, temos o pacote noiva completo! Penteado + make + unhas + sobrancelha com 20% de desconto. Quer que eu verifique a disponibilidade?'
    ),
    (
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
-- 4. DADOS DE EXEMPLO - UPSELL OPPORTUNITIES (IDEMPOTENTE)
-- ═══════════════════════════════════════════════
DELETE FROM upsell_opportunities
WHERE service_id IN (
        'escova_lisa',
        'escova_modelada',
        'penteado_basico',
        'manicure',
        'design_sobrancelha',
        'progressiva_curtos'
    );
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
    ),
    (
        'escova_modelada',
        'Escova Modelada',
        ARRAY ['manicure', 'design_sobrancelha', 'lash_lifting'],
        'Perfeito! Enquanto verifico os horários de escova modelada, que tal já deixar as unhas e sobrancelhas em dia? Consigo encaixar tudo junto!',
        1
    ),
    (
        'penteado_basico',
        'Penteado',
        ARRAY ['make_basica', 'design_sobrancelha', 'manicure'],
        'Ótima escolha! Para seu evento ficar perfeito, que tal adicionar maquiagem e sobrancelha? Temos um pacote especial para eventos!',
        1
    ),
    (
        'manicure',
        'Manicure',
        ARRAY ['pedicure', 'gel_maos'],
        'Já que vai fazer as unhas das mãos, que tal aproveitar e fazer os pés também? E temos o gel que dura até 3 semanas! Quer que eu verifique os horários?',
        1
    ),
    (
        'design_sobrancelha',
        'Design de Sobrancelha',
        ARRAY ['brow_lamination', 'lash_lifting'],
        'Perfeito! Enquanto isso, você conheceu nosso Brow Lamination? Dura até 6 semanas e deixa as sobrancelhas perfeitas! Quer adicionar?',
        2
    ),
    (
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
DROP FUNCTION IF EXISTS get_active_campaigns();
CREATE OR REPLACE FUNCTION get_active_campaigns() RETURNS TABLE (
        id UUID,
        name TEXT,
        description TEXT,
        discount_percent DECIMAL,
        start_date DATE,
        end_date DATE,
        campaign_script TEXT,
        target_services TEXT [],
        add_on_services TEXT []
    ) AS $$ BEGIN RETURN QUERY
SELECT mc.id,
    mc.name,
    mc.description,
    mc.discount_percent,
    mc.start_date,
    mc.end_date,
    mc.campaign_script,
    mc.target_services,
    mc.add_on_services
FROM marketing_campaigns mc
WHERE mc.is_active = true
    AND mc.start_date <= CURRENT_DATE
    AND mc.end_date >= CURRENT_DATE
ORDER BY mc.discount_percent DESC;
END;
$$ LANGUAGE plpgsql;
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
-- 6. PERMISSÕES
-- ═══════════════════════════════════════════════
GRANT SELECT ON marketing_campaigns TO service_role;
GRANT SELECT ON upsell_opportunities TO service_role;