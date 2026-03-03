-- 🌙 LUNA OS - Seed Haven SQL
-- Popular Supabase com dados oficiais da Haven
-- Data: 2026-03-01

-- ═══════════════════════════════════════════════
-- 1. SERVIÇOS (41 registros)
-- ═══════════════════════════════════════════════

-- CABELO - ESCOVAS
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_escova_lisa', '{
  "id": "escova_lisa",
  "name": "Escova Lisa",
  "price": 59.00,
  "promo_price_seg_qua": 49.00,
  "duration_min": 45,
  "category": "cabelo",
  "includes_blowdry": true
}', true),
('services', 'service_escova_modelada', '{
  "id": "escova_modelada",
  "name": "Escova Modelada",
  "price": 69.00,
  "promo_price_seg_qua": 49.00,
  "duration_min": 60,
  "category": "cabelo",
  "includes_blowdry": true
}', true),
('services', 'service_adicional_mega', '{
  "id": "adicional_mega",
  "name": "Adicional Mega Hair",
  "price": 20.00,
  "duration_min": 20,
  "category": "cabelo",
  "type": "adicional"
}', true);

-- CABELO - PENTEADOS
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_penteado_basico', '{
  "id": "penteado_basico",
  "name": "Penteado Básico",
  "price": 115.00,
  "promo_price_seg_qua": 99.00,
  "duration_min": 30,
  "category": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_penteado_plus', '{
  "id": "penteado_plus",
  "name": "Penteado Plus",
  "price": 139.00,
  "promo_price_seg_qua": 99.00,
  "duration_min": 35,
  "category": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_penteado_premium', '{
  "id": "penteado_premium",
  "name": "Penteado Premium",
  "price": 169.00,
  "duration_min": 45,
  "category": "cabelo",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true);

-- CABELO - CORTE
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_corte_com_escova', '{
  "id": "corte_com_escova",
  "name": "Corte + Escova Lisa",
  "price": 170.00,
  "promo_price_seg_qua": 80.00,
  "duration_min": 80,
  "category": "cabelo",
  "includes_blowdry": true
}', true),
('services', 'service_corte_sem_escova', '{
  "id": "corte_sem_escova",
  "name": "Corte Sem Escova",
  "price": 120.00,
  "promo_price_seg_qua": 80.00,
  "duration_min": 45,
  "category": "cabelo",
  "includes_blowdry": false
}', true);

-- CABELO - QUÍMICAS
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_progressiva_curtos', '{
  "id": "progressiva_curtos",
  "name": "Progressiva Cabelos Curtos",
  "price": 250.00,
  "duration_min": 180,
  "category": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 40,
  "chemical_pause_max": 70
}', true),
('services', 'service_progressiva_medios', '{
  "id": "progressiva_medios",
  "name": "Progressiva Cabelos Médios",
  "price": 295.00,
  "duration_min": 210,
  "category": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 50,
  "chemical_pause_max": 70
}', true),
('services', 'service_progressiva_longos', '{
  "id": "progressiva_longos",
  "name": "Progressiva Cabelos Longos",
  "price": 380.00,
  "duration_min": 240,
  "category": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 60,
  "chemical_pause_max": 90
}', true),
('services', 'service_cauterizacao', '{
  "id": "cauterizacao",
  "name": "Cauterização",
  "price_min": 180.00,
  "price_med": 210.00,
  "price_long": 230.00,
  "duration_min": 75,
  "category": "cabelo",
  "includes_blowdry": false
}', true),
('services', 'service_tintura_retoque', '{
  "id": "tintura_retoque",
  "name": "Tintura / Retoque de Raiz",
  "price": 179.00,
  "duration_min": 120,
  "category": "cabelo",
  "includes_blowdry": true,
  "chemical_pause_min": 30,
  "chemical_pause_max": 40
}', true);

-- CABELO - TRATAMENTOS (8 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_hidratacao', '{
  "id": "hidratacao",
  "name": "Hidratação",
  "price": 85.00,
  "promo_price_seg_qua": 50.00,
  "duration_min": 50,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_nutricao', '{
  "id": "nutricao",
  "name": "Nutrição",
  "price": 95.00,
  "duration_min": 60,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_reconstrucao_truss', '{
  "id": "reconstrucao_truss",
  "name": "Reconstrução TRUSS",
  "price": 110.00,
  "duration_min": 75,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_tratamento_labrizza', '{
  "id": "tratamento_labrizza",
  "name": "Tratamentos LABRIZZA",
  "price": 125.00,
  "duration_min": 75,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_tratamento_coreano', '{
  "id": "tratamento_coreano",
  "name": "Tratamentos Coreanos",
  "price": 135.00,
  "duration_min": 90,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_umectacao', '{
  "id": "umectacao",
  "name": "Umectação",
  "price": 65.00,
  "promo_price_seg_qua": 30.00,
  "duration_min": 70,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_hidratacao_ozonio', '{
  "id": "hidratacao_ozonio",
  "name": "Hidratação + Ozônio",
  "price": 50.00,
  "duration_min": 70,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true),
('services', 'service_tratamento_detox', '{
  "id": "tratamento_detox",
  "name": "Tratamento DETOX",
  "price": 99.00,
  "duration_min": 80,
  "category": "tratamentos",
  "includes_blowdry": false,
  "alert": "NÃO inclui escova"
}', true);

-- CABELO - FINALIZAÇÃO (2 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_matizacao_loiros', '{
  "id": "matizacao_loiros",
  "name": "Matização de Loiros",
  "price": 115.00,
  "duration_min": 80,
  "category": "cabelo",
  "includes_blowdry": true,
  "alert": "EXCEÇÃO: esta matização INCLUI escova"
}', true),
('services', 'service_fitagem', '{
  "id": "fitagem",
  "name": "Fitagem (Definição de Cachos)",
  "price": 85.00,
  "promo_price_seg_qua": 59.00,
  "duration_min": 80,
  "category": "cabelo",
  "includes_blowdry": false,
  "professional": "cintia",
  "alert": "Confirmar com Cíntia ANTES"
}', true);

-- UNHAS - TRADICIONAL (4 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_manicure', '{
  "id": "manicure",
  "name": "Manicure",
  "price_min": 42.00,
  "price_max": 50.00,
  "duration_min": 40,
  "category": "unhas",
  "professionals": ["davila", "luisa", "edna"]
}', true),
('services', 'service_pedicure', '{
  "id": "pedicure",
  "name": "Pedicure",
  "price_min": 45.00,
  "price_max": 60.00,
  "duration_min": 45,
  "category": "unhas",
  "professionals": ["davila", "luisa", "edna"]
}', true),
('services', 'service_plastica_pes', '{
  "id": "plastica_pes",
  "name": "Plástica dos Pés",
  "price": 140.00,
  "duration_min": 90,
  "category": "unhas",
  "includes": ["pedicure_tradicional"],
  "alert": "INCLUI pedicure"
}', true),
('services', 'service_manicure_russa', '{
  "id": "manicure_russa",
  "name": "Manicure Russa",
  "price": 80.00,
  "duration_min": 50,
  "category": "unhas",
  "professionals": ["davila", "luisa"]
}', true);

-- UNHAS - GEL (4 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_gel_maos', '{
  "id": "gel_maos",
  "name": "Esmaltação em Gel",
  "price_min": 120.00,
  "price_max": 140.00,
  "duration_min": 100,
  "category": "unhas",
  "professionals": ["davila", "luisa"],
  "maintenance_rule": "Mesmo valor da aplicação"
}', true),
('services', 'service_manutencao_gel', '{
  "id": "manutencao_gel",
  "name": "Manutenção em Gel",
  "price": "mesmo_da_aplicacao",
  "duration_min": 70,
  "category": "unhas",
  "professionals": ["davila", "luisa"]
}', true),
('services', 'service_remocao_gel', '{
  "id": "remocao_gel",
  "name": "Remoção de Gel",
  "price": 30.00,
  "duration_min": 30,
  "category": "unhas",
  "alert": "PERGUNTA OBRIGATÓRIA"
}', true),
('services', 'service_remocao_alongamento', '{
  "id": "remocao_alongamento",
  "name": "Remoção de Alongamento",
  "price": 30.00,
  "duration_min": 30,
  "category": "unhas",
  "alert": "PERGUNTA OBRIGATÓRIA"
}', true);

-- UNHAS - ESPECIALIDADES (2 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_alongamento_suzana', '{
  "id": "alongamento_suzana",
  "name": "Alongamento de Unhas (Suzana)",
  "price": 450.00,
  "duration_min": 160,
  "category": "unhas",
  "professional": "suzana",
  "includes": ["gel", "cutelagem_russa"],
  "alert": "EXCLUSIVO Suzana"
}', true),
('services', 'service_reconstrucao_individual', '{
  "id": "reconstrucao_individual",
  "name": "Reconstrução Individual",
  "price": "adicional",
  "duration_min": 25,
  "category": "unhas",
  "professional": "davila",
  "notes": "Valor adicional - confirmar no sistema"
}', true);

-- MAQUIAGEM (3 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_make_casual', '{
  "id": "make_casual",
  "name": "Make Casual",
  "price": 120.00,
  "duration_min": 40,
  "category": "maquiagem",
  "professionals": ["tay", "mariana"],
  "always_last": true
}', true),
('services', 'service_make_basica', '{
  "id": "make_basica",
  "name": "Make Básica",
  "price": 149.00,
  "promo_price_seg_qua": 110.00,
  "duration_min": 55,
  "category": "maquiagem",
  "professionals": ["tay", "mariana"],
  "always_last": true
}', true),
('services', 'service_make_premium', '{
  "id": "make_premium",
  "name": "Make Premium",
  "price": 195.00,
  "duration_min": 75,
  "category": "maquiagem",
  "professionals": ["tay", "mariana"],
  "always_last": true
}', true);

-- ESTÉTICA (5 serviços)
INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('services', 'service_design_sobrancelha', '{
  "id": "design_sobrancelha",
  "name": "Design de Sobrancelha",
  "price": 60.00,
  "promo_price_seg_qua": 45.00,
  "duration_min": 30,
  "category": "estetica",
  "professionals": ["tay", "yujaira"]
}', true),
('services', 'service_design_com_tintura', '{
  "id": "design_com_tintura",
  "name": "Design com Tintura",
  "price": 80.00,
  "promo_price_seg_qua": 65.00,
  "duration_min": 40,
  "category": "estetica",
  "professional": "tay"
}', true),
('services', 'service_brow_lamination', '{
  "id": "brow_lamination",
  "name": "Brow Lamination",
  "price": 150.00,
  "duration_min": 60,
  "category": "estetica",
  "professional": "tay",
  "adicional_tintura": 30.00
}', true),
('services', 'service_lash_lifting', '{
  "id": "lash_lifting",
  "name": "Lash Lifting",
  "price": 165.00,
  "duration_min": 40,
  "category": "estetica",
  "professional": "tay"
}', true),
('services', 'service_epilacao_facial', '{
  "id": "epilacao_facial",
  "name": "Epilação Facial",
  "price": 35.00,
  "duration_min": 20,
  "category": "estetica",
  "professional": "tay"
}', true);

-- ═══════════════════════════════════════════════
-- 2. PROFISSIONAIS (9 registros)
-- ═══════════════════════════════════════════════

INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('professionals', 'professional_yujaira', '{
  "id": "yujaira",
  "name": "Yujaira",
  "nickname": "Ju",
  "category": "cabelo",
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
}', true),
('professionals', 'professional_carla', '{
  "id": "carla",
  "name": "Carla",
  "nickname": "Carla",
  "category": "cabelo_spa",
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
}', true),
('professionals', 'professional_mariana', '{
  "id": "mariana",
  "name": "Mariana",
  "nickname": "Mariana",
  "category": "cabelo",
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
}', true),
('professionals', 'professional_davila', '{
  "id": "davila",
  "name": "Dávila",
  "nickname": "Dávila",
  "category": "unhas",
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
}', true),
('professionals', 'professional_luisa', '{
  "id": "luisa",
  "name": "Luisa",
  "nickname": "Lu",
  "category": "unhas",
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
}', true),
('professionals', 'professional_edna', '{
  "id": "edna",
  "name": "Edna",
  "nickname": "Edna",
  "category": "unhas",
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
}', true),
('professionals', 'professional_tay', '{
  "id": "tay",
  "name": "Tay",
  "nickname": "Tay",
  "category": "estetica_facial",
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
}', true),
('professionals', 'professional_cintia', '{
  "id": "cintia",
  "name": "Cíntia",
  "nickname": "Cíntia",
  "category": "freelancer",
  "level": "especialista_cachos",
  "specialty": "Fitagem (Definição de Cachos)",
  "schedule": {
    "segunda": "08:00-16:00",
    "terca": "08:00-16:00",
    "quarta": "08:00-16:00",
    "quinta": "08:00-16:00",
    "sexta": "08:00-16:00",
    "sabado": "08:00-16:00/17:00"
  },
  "alert": "NUNCA confirmar sem checar antes"
}', true),
('professionals', 'professional_suzana', '{
  "id": "suzana",
  "name": "Suzana",
  "nickname": "Suzana",
  "category": "proprietaria",
  "level": "especialista_alongamento",
  "specialty": "Alongamento (EXCLUSIVO)",
  "schedule": "Por confirmar",
  "alert": "EXCLUSIVO alongamento"
}', true);

-- ═══════════════════════════════════════════════
-- 3. CUPONS (5 registros)
-- ═══════════════════════════════════════════════

INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('coupons', 'coupon_PRISCILA10', '{
  "code": "PRISCILA10",
  "blogger": "Priscila Kuhn",
  "discount": 0.10,
  "type": "percentage"
}', true),
('coupons', 'coupon_EWYLIN10', '{
  "code": "EWYLIN10",
  "blogger": "Ewylin Salvatori",
  "discount": 0.10,
  "type": "percentage"
}', true),
('coupons', 'coupon_SOLANGE10', '{
  "code": "SOLANGE10",
  "blogger": "Solange",
  "discount": 0.10,
  "type": "percentage"
}', true),
('coupons', 'coupon_CAROLINE10', '{
  "code": "CAROLINE10",
  "blogger": "Caroline",
  "discount": 0.10,
  "type": "percentage"
}', true),
('coupons', 'coupon_KETLYN10', '{
  "code": "KETLYN10",
  "blogger": "Ketlyn",
  "discount": 0.10,
  "type": "percentage"
}', true);

-- ═══════════════════════════════════════════════
-- 4. PACOTES (4 registros)
-- ═══════════════════════════════════════════════

INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('packages', 'package_gel_3_maos', '{
  "id": "gel_3_maos",
  "name": "Pacote Gel 3 Aplicações (Mãos)",
  "quantity": 3,
  "type": "gel_maos",
  "price_lu": 99.00,
  "price_davila": 120.00,
  "validity_days": 60,
  "payment": "vista_pix_ou_dinheiro"
}', true),
('packages', 'package_gel_6_maos', '{
  "id": "gel_6_maos",
  "name": "Pacote Gel 6 Aplicações (Mãos)",
  "quantity": 6,
  "type": "gel_maos",
  "price_lu": 99.00,
  "price_davila": 120.00,
  "validity_days": 120,
  "payment": "vista_pix_ou_dinheiro"
}', true),
('packages', 'package_escova_4', '{
  "id": "escova_4",
  "name": "Pacote 4 Escovas",
  "quantity": 4,
  "type": "escovas",
  "lisa": 55.00,
  "modelada": 65.00,
  "validity_days": 30,
  "payment": "vista_pix_ou_dinheiro"
}', true),
('packages', 'package_escova_8', '{
  "id": "escova_8",
  "name": "Pacote 8 Escovas",
  "quantity": 8,
  "type": "escovas",
  "lisa": 52.00,
  "modelada": 59.00,
  "validity_days": 60,
  "payment": "vista_pix_ou_dinheiro"
}', true);

-- ═══════════════════════════════════════════════
-- 5. FAQs (4 registros)
-- ═══════════════════════════════════════════════

INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('faqs', 'faq_horario_funcionamento', '{
  "id": "horario_funcionamento",
  "question": "Qual o horário de funcionamento?",
  "answer": "Atendemos de segunda a sábado, das 8h às 20h, sem pausa para almoço!",
  "category": "geral"
}', true),
('faqs', 'faq_precisa_agendar', '{
  "id": "precisa_agendar",
  "question": "Precisa agendar?",
  "answer": "Sim! Trabalhamos somente com horário agendado para melhor atendê-la.",
  "category": "geral"
}', true),
('faqs', 'faq_aceita_cartao', '{
  "id": "aceita_cartao",
  "question": "Aceita cartão?",
  "answer": "Sim! Aceitamos cartão de crédito, débito e PIX. Parcelamos no crédito em até 3x sem juros.",
  "category": "pagamento"
}', true),
('faqs', 'faq_tem_estacionamento', '{
  "id": "tem_estacionamento",
  "question": "Tem estacionamento?",
  "answer": "Temos estacionamento em frente ao salão e também 4 vagas na esquina!",
  "category": "localizacao"
}', true);

-- ═══════════════════════════════════════════════
-- 6. BUSINESS INFO (1 registro)
-- ═══════════════════════════════════════════════

INSERT INTO knowledge_base (category, key, data, is_active) VALUES
('business', 'business_info', '{
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
  "coordinates": {
    "lat": -27.0922,
    "lng": -52.6158
  }
}', true);

-- ═══════════════════════════════════════════════
-- RESUMO DA INSERÇÃO
-- ═══════════════════════════════════════════════

-- Contar registros inseridos
SELECT 
  category,
  COUNT(*) as total_registros
FROM knowledge_base
WHERE category IN ('services', 'professionals', 'coupons', 'packages', 'faqs', 'business')
GROUP BY category
ORDER BY category;

-- Total geral
SELECT 
  COUNT(*) as total_geral_registros
FROM knowledge_base
WHERE category IN ('services', 'professionals', 'coupons', 'packages', 'faqs', 'business');

-- ✅ Seed Haven completado!
-- Total esperado: 64 registros
-- - 41 services
-- - 9 professionals
-- - 5 coupons
-- - 4 packages
-- - 4 faqs
-- - 1 business
