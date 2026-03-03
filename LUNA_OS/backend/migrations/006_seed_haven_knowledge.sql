-- =============================================================================
-- LUNA OS — Master Reset & Seed Script
-- Haven Escovaria & Esmalteria — Chapecó/SC
-- =============================================================================
-- INSTRUÇÃO: Execute este arquivo inteiro no Supabase SQL Editor.
-- É SEGURO rodar múltiplas vezes — usa ON CONFLICT (key) DO UPDATE.
-- NÃO apaga dados de conversas, clientes ou mensagens.
-- =============================================================================
-- ─────────────────────────────────────────────────────────────────────────────
-- PARTE 1: GARANTIR QUE O SCHEMA ESTÁ CORRETO
-- (idempotente — não quebra se já existir)
-- ─────────────────────────────────────────────────────────────────────────────
-- Função de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now();
RETURN NEW;
END;
$$ language 'plpgsql';
-- Tabela principal do knowledge_base (schema original com key/data JSONB)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
-- Uniqueness na key (necessário para ON CONFLICT / UPSERT)
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'knowledge_base_key_unique'
) THEN -- Limpar duplicatas antes de criar constraint
DELETE FROM knowledge_base a USING knowledge_base b
WHERE a.id < b.id
    AND a.key = b.key;
ALTER TABLE knowledge_base
ADD CONSTRAINT knowledge_base_key_unique UNIQUE (key);
END IF;
END $$;
-- Indexes
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category_key ON knowledge_base(category, key);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category ON knowledge_base(category);
-- Tabela de campanhas (CREATE só roda se não existir)
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'reativacao',
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
-- Adicionar TODAS as colunas que podem estar faltando (idempotente)
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'target_segment'
) THEN
ALTER TABLE campaigns
ADD COLUMN target_segment TEXT;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'objective'
) THEN
ALTER TABLE campaigns
ADD COLUMN objective TEXT;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'objective_description'
) THEN
ALTER TABLE campaigns
ADD COLUMN objective_description TEXT;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'insights'
) THEN
ALTER TABLE campaigns
ADD COLUMN insights TEXT;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'start_date'
) THEN
ALTER TABLE campaigns
ADD COLUMN start_date DATE;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'end_date'
) THEN
ALTER TABLE campaigns
ADD COLUMN end_date DATE;
END IF;
IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'campaigns'
        AND column_name = 'tenant_id'
) THEN
ALTER TABLE campaigns
ADD COLUMN tenant_id TEXT NOT NULL DEFAULT 'haven_escovaria';
END IF;
END $$;
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
-- ─────────────────────────────────────────────────────────────────────────────
-- PARTE 2: SEED — KNOWLEDGE BASE REAL DO HAVEN
-- Usa ON CONFLICT (key) DO UPDATE → 100% idempotente
-- ─────────────────────────────────────────────────────────────────────────────
-- ═══════════════
-- 1. SERVIÇOS
-- ═══════════════
-- CABELO - ESCOVAS
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_escova_lisa',
        '{
  "name": "Escova Lisa",
  "price": 59.00,
  "promo_price_seg_qua": 49.00,
  "duration_min": 45,
  "subcategory": "cabelo",
  "includes_blowdry": true
}'
    ),
    (
        'services',
        'service_escova_modelada',
        '{
  "name": "Escova Modelada",
  "price": 69.00,
  "promo_price_seg_qua": 49.00,
  "duration_min": 60,
  "subcategory": "cabelo",
  "includes_blowdry": true
}'
    ),
    (
        'services',
        'service_adicional_mega',
        '{
  "name": "Adicional Mega Hair",
  "price": 20.00,
  "duration_min": 20,
  "subcategory": "cabelo",
  "type": "adicional"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- CABELO - PENTEADOS
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_penteado_basico',
        '{
  "name": "Penteado Básico",
  "price": 115.00,
  "promo_price_seg_qua": 99.00,
  "duration_min": 30,
  "subcategory": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_penteado_plus',
        '{
  "name": "Penteado Plus",
  "price": 139.00,
  "promo_price_seg_qua": 99.00,
  "duration_min": 35,
  "subcategory": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_penteado_premium',
        '{
  "name": "Penteado Premium",
  "price": 169.00,
  "duration_min": 45,
  "subcategory": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- CABELO - CORTE
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_corte_com_escova',
        '{
  "name": "Corte + Escova Lisa",
  "price": 170.00,
  "promo_price_seg_qua": 80.00,
  "duration_min": 80,
  "subcategory": "cabelo",
  "includes_blowdry": true
}'
    ),
    (
        'services',
        'service_corte_sem_escova',
        '{
  "name": "Corte Sem Escova",
  "price": 120.00,
  "promo_price_seg_qua": 80.00,
  "duration_min": 45,
  "subcategory": "cabelo",
  "includes_blowdry": false
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- CABELO - QUÍMICAS
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_progressiva_curtos',
        '{
  "name": "Progressiva Cabelos Curtos",
  "price": 250.00,
  "duration_min": 180,
  "subcategory": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 40,
  "chemical_pause_max": 70
}'
    ),
    (
        'services',
        'service_progressiva_medios',
        '{
  "name": "Progressiva Cabelos Médios",
  "price": 295.00,
  "duration_min": 210,
  "subcategory": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 50,
  "chemical_pause_max": 70
}'
    ),
    (
        'services',
        'service_progressiva_longos',
        '{
  "name": "Progressiva Cabelos Longos",
  "price": 380.00,
  "duration_min": 240,
  "subcategory": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 60,
  "chemical_pause_max": 90
}'
    ),
    (
        'services',
        'service_cauterizacao',
        '{
  "name": "Cauterização",
  "price_min": 180.00,
  "price_med": 210.00,
  "price_long": 230.00,
  "duration_min": 75,
  "subcategory": "cabelo",
  "includes_blowdry": false
}'
    ),
    (
        'services',
        'service_tintura_retoque',
        '{
  "name": "Tintura / Retoque de Raiz",
  "price": 179.00,
  "duration_min": 120,
  "subcategory": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 30,
  "chemical_pause_max": 40
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- CABELO - TRATAMENTOS
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_hidratacao',
        '{
  "name": "Hidratação",
  "price": 85.00,
  "promo_price_seg_qua": 50.00,
  "duration_min": 50,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_nutricao',
        '{
  "name": "Nutrição",
  "price": 95.00,
  "duration_min": 60,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_reconstrucao_truss',
        '{
  "name": "Reconstrução TRUSS",
  "price": 110.00,
  "duration_min": 75,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_tratamento_labrizza',
        '{
  "name": "Tratamentos LABRIZZA",
  "price": 125.00,
  "duration_min": 75,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_tratamento_coreano',
        '{
  "name": "Tratamentos Coreanos",
  "price": 135.00,
  "duration_min": 90,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_umectacao',
        '{
  "name": "Umectação",
  "price": 65.00,
  "promo_price_seg_qua": 30.00,
  "duration_min": 70,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_hidratacao_ozonio',
        '{
  "name": "Hidratação + Ozônio",
  "price": 50.00,
  "duration_min": 70,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ),
    (
        'services',
        'service_tratamento_detox',
        '{
  "name": "Tratamento DETOX",
  "price": 99.00,
  "duration_min": 80,
  "subcategory": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- CABELO - FINALIZAÇÃO
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_matizacao_loiros',
        '{
  "name": "Matização de Loiros",
  "price": 115.00,
  "duration_min": 80,
  "subcategory": "cabelo",
  "includes_blowdry": true,
  "alert": "EXCEÇÃO: esta matização INCLUI escova"
}'
    ),
    (
        'services',
        'service_fitagem',
        '{
  "name": "Fitagem (Definição de Cachos)",
  "price": 85.00,
  "promo_price_seg_qua": 59.00,
  "duration_min": 80,
  "subcategory": "cabelo",
  "includes_blowdry": false,
  "professional": "cintia",
  "alert": "Confirmar com Cíntia ANTES"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- UNHAS - TRADICIONAL
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_manicure',
        '{
  "name": "Manicure",
  "price_min": 42.00,
  "price_max": 50.00,
  "duration_min": 40,
  "subcategory": "unhas",
  "professionals": ["davila","luisa","edna"]
}'
    ),
    (
        'services',
        'service_pedicure',
        '{
  "name": "Pedicure",
  "price_min": 45.00,
  "price_max": 60.00,
  "duration_min": 45,
  "subcategory": "unhas",
  "professionals": ["davila","luisa","edna"]
}'
    ),
    (
        'services',
        'service_plastica_pes',
        '{
  "name": "Plástica dos Pés",
  "price": 140.00,
  "duration_min": 90,
  "subcategory": "unhas",
  "includes": ["pedicure_tradicional"],
  "alert": "INCLUI pedicure"
}'
    ),
    (
        'services',
        'service_manicure_russa',
        '{
  "name": "Manicure Russa",
  "price": 80.00,
  "duration_min": 50,
  "subcategory": "unhas",
  "professionals": ["davila","luisa"]
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- UNHAS - GEL
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_gel_maos',
        '{
  "name": "Esmaltação em Gel",
  "price_min": 120.00,
  "price_max": 140.00,
  "duration_min": 100,
  "subcategory": "unhas",
  "professionals": ["davila","luisa"],
  "maintenance_rule": "Mesmo valor da aplicação"
}'
    ),
    (
        'services',
        'service_manutencao_gel',
        '{
  "name": "Manutenção em Gel",
  "price_note": "Mesmo valor da aplicação",
  "duration_min": 70,
  "subcategory": "unhas",
  "professionals": ["davila","luisa"]
}'
    ),
    (
        'services',
        'service_remocao_gel',
        '{
  "name": "Remoção de Gel",
  "price": 30.00,
  "duration_min": 30,
  "subcategory": "unhas",
  "alert": "PERGUNTA OBRIGATÓRIA antes de agendar"
}'
    ),
    (
        'services',
        'service_remocao_alongamento',
        '{
  "name": "Remoção de Alongamento",
  "price": 30.00,
  "duration_min": 30,
  "subcategory": "unhas",
  "alert": "PERGUNTA OBRIGATÓRIA antes de agendar"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- UNHAS - ESPECIALIDADES
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_alongamento_suzana',
        '{
  "name": "Alongamento de Unhas (Suzana)",
  "price": 450.00,
  "duration_min": 160,
  "subcategory": "unhas",
  "professional": "suzana",
  "includes": ["gel","cutelagem_russa"],
  "alert": "EXCLUSIVO Suzana — confirmar disponibilidade antes"
}'
    ),
    (
        'services',
        'service_reconstrucao_individual',
        '{
  "name": "Reconstrução Individual",
  "price_note": "Adicional — confirmar no sistema",
  "duration_min": 25,
  "subcategory": "unhas",
  "professional": "davila"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- MAQUIAGEM
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_make_casual',
        '{
  "name": "Make Casual",
  "price": 120.00,
  "duration_min": 40,
  "subcategory": "maquiagem",
  "professionals": ["tay","mariana"],
  "always_last": true,
  "alert": "SEMPRE último serviço do dia"
}'
    ),
    (
        'services',
        'service_make_basica',
        '{
  "name": "Make Básica",
  "price": 149.00,
  "promo_price_seg_qua": 110.00,
  "duration_min": 55,
  "subcategory": "maquiagem",
  "professionals": ["tay","mariana"],
  "always_last": true,
  "alert": "SEMPRE último serviço do dia"
}'
    ),
    (
        'services',
        'service_make_premium',
        '{
  "name": "Make Premium",
  "price": 195.00,
  "duration_min": 75,
  "subcategory": "maquiagem",
  "professionals": ["tay","mariana"],
  "always_last": true,
  "alert": "SEMPRE último serviço do dia"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ESTÉTICA FACIAL
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'services',
        'service_design_sobrancelha',
        '{
  "name": "Design de Sobrancelha",
  "price": 60.00,
  "promo_price_seg_qua": 45.00,
  "duration_min": 30,
  "subcategory": "estetica",
  "professionals": ["tay","yujaira"]
}'
    ),
    (
        'services',
        'service_design_com_tintura',
        '{
  "name": "Design com Tintura",
  "price": 80.00,
  "promo_price_seg_qua": 65.00,
  "duration_min": 40,
  "subcategory": "estetica",
  "professional": "tay"
}'
    ),
    (
        'services',
        'service_brow_lamination',
        '{
  "name": "Brow Lamination",
  "price": 150.00,
  "duration_min": 60,
  "subcategory": "estetica",
  "professional": "tay",
  "adicional_tintura": 30.00
}'
    ),
    (
        'services',
        'service_lash_lifting',
        '{
  "name": "Lash Lifting",
  "price": 165.00,
  "duration_min": 40,
  "subcategory": "estetica",
  "professional": "tay"
}'
    ),
    (
        'services',
        'service_epilacao_facial',
        '{
  "name": "Epilação Facial",
  "price": 35.00,
  "duration_min": 20,
  "subcategory": "estetica",
  "professional": "tay"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════════
-- 2. PROFISSIONAIS (9 registros)
-- ═══════════════════════════════
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'professionals',
        'professional_yujaira',
        '{
  "name": "Yujaira",
  "nickname": "Ju",
  "subcategory": "cabelo",
  "level": "completa",
  "specialty": "Penteados e Tranças",
  "schedule": {
    "segunda": "08:00-20:00",
    "terca": "FOLGA",
    "quarta": "08:00-20:00",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00"
  }
}'
    ),
    (
        'professionals',
        'professional_carla',
        '{
  "name": "Carla",
  "nickname": "Carla",
  "subcategory": "cabelo_spa",
  "level": "senior",
  "specialty": "Progressiva",
  "schedule": {
    "segunda": "08:00-20:00 (eventual)",
    "terca": "08:00-20:00",
    "quarta": "08:00-20:00",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00"
  },
  "alert": "SEMPRE verificar agenda do Spa"
}'
    ),
    (
        'professionals',
        'professional_mariana',
        '{
  "name": "Mariana",
  "nickname": "Mariana",
  "subcategory": "cabelo",
  "level": "completa_avancada",
  "specialty": "Cores Complexas",
  "schedule": {
    "segunda": "NÃO ATENDE",
    "terca": "12:00-17:30",
    "quarta": "12:00-17:30",
    "quinta": "12:00-17:30",
    "sexta": "12:00-20:00",
    "sabado": "08:00-20:00"
  }
}'
    ),
    (
        'professionals',
        'professional_davila',
        '{
  "name": "Dávila",
  "nickname": "Dávila",
  "subcategory": "unhas",
  "level": "master_unhas",
  "specialty": "Manicure Avançada e Gel",
  "schedule": {
    "segunda": "08:00-17:00",
    "terca": "08:00-17:00",
    "quarta": "08:00-17:00",
    "quinta": "08:00-17:00",
    "sexta": "08:00-17:00",
    "sabado": "08:00-17:00"
  }
}'
    ),
    (
        'professionals',
        'professional_luisa',
        '{
  "name": "Luisa",
  "nickname": "Lu",
  "subcategory": "unhas",
  "level": "senior_unhas",
  "specialty": "Manicure e Gel",
  "schedule": {
    "segunda": "NÃO ATENDE",
    "terca": "08:00-20:00",
    "quarta": "08:00-20:00",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00"
  }
}'
    ),
    (
        'professionals',
        'professional_edna',
        '{
  "name": "Edna",
  "nickname": "Edna",
  "subcategory": "unhas",
  "level": "junior",
  "specialty": "Manicure Tradicional",
  "schedule": {
    "segunda": "08:00-20:00",
    "terca": "08:00-20:00",
    "quarta": "FOLGA",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00"
  }
}'
    ),
    (
        'professionals',
        'professional_tay',
        '{
  "name": "Tay",
  "nickname": "Tay",
  "subcategory": "estetica_facial",
  "level": "especialista",
  "specialty": "Maquiagem e Sobrancelhas",
  "schedule": {
    "segunda": "NÃO ATENDE",
    "terca": "08:00-20:00",
    "quarta": "08:00-20:00",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00"
  }
}'
    ),
    (
        'professionals',
        'professional_cintia',
        '{
  "name": "Cíntia",
  "nickname": "Cíntia",
  "subcategory": "freelancer",
  "level": "especialista_cachos",
  "specialty": "Fitagem (Cachos)",
  "schedule": {
    "segunda": "08:00-16:00",
    "terca": "08:00-16:00",
    "quarta": "08:00-16:00",
    "quinta": "08:00-16:00",
    "sexta": "08:00-16:00",
    "sabado": "08:00-16:00/17:00"
  },
  "alert": "NUNCA confirmar sem checar antes"
}'
    ),
    (
        'professionals',
        'professional_suzana',
        '{
  "name": "Suzana",
  "nickname": "Suzana",
  "subcategory": "proprietaria",
  "level": "especialista_alongamento",
  "specialty": "Alongamento (EXCLUSIVO)",
  "schedule": "Por confirmar",
  "alert": "Atende EXCLUSIVO alongamento"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════
-- 3. CUPONS (5 registros)
-- ═══════════════════════════
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'coupons',
        'coupon_PRISCILA10',
        '{"code":"PRISCILA10", "blogger":"Priscila Kuhn",      "discount":0.10,"type":"percentage"}'
    ),
    (
        'coupons',
        'coupon_EWYLIN10',
        '{"code":"EWYLIN10",  "blogger":"Ewylin Salvatori",    "discount":0.10,"type":"percentage"}'
    ),
    (
        'coupons',
        'coupon_SOLANGE10',
        '{"code":"SOLANGE10", "blogger":"Solange",             "discount":0.10,"type":"percentage"}'
    ),
    (
        'coupons',
        'coupon_CAROLINE10',
        '{"code":"CAROLINE10","blogger":"Caroline",            "discount":0.10,"type":"percentage"}'
    ),
    (
        'coupons',
        'coupon_KETLYN10',
        '{"code":"KETLYN10",  "blogger":"Ketlyn",              "discount":0.10,"type":"percentage"}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════
-- 4. PACOTES (4 registros)
-- ═══════════════════════════
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'packages',
        'package_gel_3_maos',
        '{
  "name": "Pacote Gel 3 Aplicações (Mãos)",
  "quantity": 3,
  "type": "gel_maos",
  "price_lu": 99.00,
  "price_davila": 120.00,
  "validity_days": 60,
  "payment": "vista_pix_ou_dinheiro"
}'
    ),
    (
        'packages',
        'package_gel_6_maos',
        '{
  "name": "Pacote Gel 6 Aplicações (Mãos)",
  "quantity": 6,
  "type": "gel_maos",
  "price_lu": 99.00,
  "price_davila": 120.00,
  "validity_days": 120,
  "payment": "vista_pix_ou_dinheiro"
}'
    ),
    (
        'packages',
        'package_escova_4',
        '{
  "name": "Pacote 4 Escovas",
  "quantity": 4,
  "type": "escovas",
  "price_lisa": 55.00,
  "price_modelada": 65.00,
  "validity_days": 30,
  "payment": "vista_pix_ou_dinheiro"
}'
    ),
    (
        'packages',
        'package_escova_8',
        '{
  "name": "Pacote 8 Escovas",
  "quantity": 8,
  "type": "escovas",
  "price_lisa": 52.00,
  "price_modelada": 59.00,
  "validity_days": 60,
  "payment": "vista_pix_ou_dinheiro"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════
-- 5. FAQs (8 registros)
-- ═══════════════════════════
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'faqs',
        'faq_horario_funcionamento',
        '{
  "question": "Qual o horário de funcionamento?",
  "answer": "Atendemos de segunda a sábado, das 8h às 20h, sem pausa para almoço!"
}'
    ),
    (
        'faqs',
        'faq_precisa_agendar',
        '{
  "question": "Precisa agendar?",
  "answer": "Sim! Trabalhamos somente com horário agendado para melhor atendê-la."
}'
    ),
    (
        'faqs',
        'faq_aceita_cartao',
        '{
  "question": "Aceita cartão?",
  "answer": "Sim! Aceitamos cartão de crédito, débito e PIX. Parcelamos no crédito em até 3x sem juros."
}'
    ),
    (
        'faqs',
        'faq_tem_estacionamento',
        '{
  "question": "Tem estacionamento?",
  "answer": "Temos estacionamento em frente ao salão e também 4 vagas na esquina!"
}'
    ),
    (
        'faqs',
        'faq_quanto_dura_progressiva',
        '{
  "question": "Quanto tempo dura a progressiva?",
  "answer": "A progressiva completa leva em média 2h30 a 3h. Cabelos muito longos ou danificados podem levar até 3h30. Venha sem pressa!"
}'
    ),
    (
        'faqs',
        'faq_lavar_progressiva',
        '{
  "question": "Posso lavar o cabelo depois da progressiva?",
  "answer": "A progressiva precisa de 72 horas (3 dias) para fixar completamente. Não lave, não use touca nem prenda o cabelo nesse período."
}'
    ),
    (
        'faqs',
        'faq_produto_progressiva',
        '{
  "question": "Qual produto vocês usam na progressiva?",
  "answer": "Trabalhamos com Cadiveu e Troia Hair — marcas profissionais reconhecidas. Ambas são seguras com durabilidade de 3 a 6 meses. Informe se tiver alergia conhecida."
}'
    ),
    (
        'faqs',
        'faq_atende_criancas',
        '{
  "question": "Atendem crianças?",
  "answer": "Sim! Atendemos crianças acima de 8 anos para corte e manicure. Para tratamentos químicos (progressiva, tintura), o protocolo exige pelo menos 16 anos."
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════════
-- 6. INFORMAÇÕES DO NEGÓCIO
-- ═══════════════════════════════
INSERT INTO knowledge_base (category, key, data)
VALUES (
        'business',
        'business_info',
        '{
  "name": "Haven Escovaria & Esmalteria",
  "address": {
    "street": "Rua Mato Grosso",
    "number": "837E",
    "neighborhood": "Jardim Itália",
    "city": "Chapecó",
    "state": "SC"
  },
  "hours": {
    "weekdays": "08:00-20:00",
    "saturday": "08:00-20:00",
    "sunday": "closed",
    "note": "Sem pausa para almoço"
  },
  "parking": "Estacionamento em frente + 4 vagas na esquina",
  "whatsapp": "principal canal de contato e agendamento",
  "payment_methods": ["pix","cartao_credito","cartao_debito","dinheiro"],
  "installments": "até 3x sem juros no crédito"
}'
    ) ON CONFLICT (key) DO
UPDATE
SET data = EXCLUDED.data,
    is_active = true;
-- ═══════════════════════════════════════════════════════════════
-- PARTE 3: CAMPANHAS PADRÃO (idempotente via WHERE NOT EXISTS)
-- ═══════════════════════════════════════════════════════════════
INSERT INTO campaigns (
        name,
        type,
        status,
        target_segment,
        objective,
        objective_description,
        insights,
        start_date,
        end_date,
        tenant_id
    )
SELECT *
FROM (
        VALUES (
                'Reativação — Clientes Inativos 30d',
                'reativacao',
                'active',
                'inativos_30',
                'reativacao',
                'Reativar clientes que não visitam há mais de 30 dias com oferta de escova com desconto',
                E'Clientes inativos respondem bem a mensagens de saudade + desconto.\nEvitar pressão direta — perguntar como ela está primeiro.',
                '2026-03-01'::date,
                '2026-03-31'::date,
                'haven_escovaria'
            ),
            (
                'Follow-up Pós Progressiva (48h)',
                'follow_up',
                'active',
                'todos',
                'followup',
                'Verificar se a cliente está satisfeita 48h após a progressiva e lembrar das regras de não lavar',
                E'Pergunta de satisfação → se positivo, pedir avaliação no Google.\nSe negativo, transferir para humano imediatamente.',
                '2026-03-01'::date,
                NULL,
                'haven_escovaria'
            ),
            (
                'Promoção Dia das Mães — Pacote Cabelo + Manicure',
                'promocao',
                'scheduled',
                'recorrentes',
                'venda',
                'Vender pacote especial Dia das Mães com cabelo + manicure + pedicure com 15% OFF',
                E'Mães preferem atendimento pela manhã (sem filhos).\nEnfatizar que conseguimos fazer manicure DURANTE a pausa da progressiva — economiza quase 1h.\nOfertar o pacote completo com desconto por tempo limitado.',
                '2026-05-01'::date,
                '2026-05-11'::date,
                'haven_escovaria'
            )
    ) AS v(
        name,
        type,
        status,
        target_segment,
        objective,
        objective_description,
        insights,
        start_date,
        end_date,
        tenant_id
    )
WHERE NOT EXISTS (
        SELECT 1
        FROM campaigns
        WHERE name = v.name
            AND tenant_id = v.tenant_id
    );
-- ─────────────────────────────────────────────────────────────────────────────
-- VERIFICAÇÃO FINAL
-- ─────────────────────────────────────────────────────────────────────────────
SELECT category,
    COUNT(*) AS total
FROM knowledge_base
WHERE is_active = true
GROUP BY category
ORDER BY category;
SELECT COUNT(*) AS total_campanhas
FROM campaigns
WHERE tenant_id = 'haven_escovaria';