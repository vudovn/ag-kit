"""
🏠 Haven Escovaria & Esmalteria - Configuração Oficial
Baseado no Protocolo WhatsApp Haven (Aprovado pela Proprietária)
Data: 2026-03-01
"""

# ═══════════════════════════════════════════════
# 1. PROFISSIONAIS (Documento 1)
# ═══════════════════════════════════════════════

PROFISSIONAIS = {
    # ─── CABELO ───
    "yujaira": {
        "nome": "Yujaira",
        "apelido": "Ju",
        "categoria": "cabelo",
        "nivel": "completa",
        "especialidade": "Penteados e Tranças",
        "faz": [
            "penteados", "tranças", "progressiva", "tintura_simples",
            "tintura_complexa", "tratamentos_capilares", "escova_lisa",
            "escova_modelada", "corte_simples", "design_sobrancelha"
        ],
        "nao_faz": ["unhas", "maquiagem"],
        "restricoes": [
            "design_sobrancelha somente quando Tay indisponível",
            "penteados elaborados: não agendar em janelas pequenas"
        ],
        "horarios": {
            "segunda": "08:00-20:00",
            "terca": "FOLGA",
            "quarta": "08:00-20:00",
            "quinta": "08:00-20:00",
            "sexta": "08:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    "carla": {
        "nome": "Carla",
        "apelido": "Carla",
        "categoria": "cabelo_spa",
        "nivel": "senior",
        "especialidade": "Progressiva",
        "faz_haven": [
            "progressiva", "escova_babyliss", "tratamentos_capilares",
            "coloracao_simples", "retoque_raiz_simples", "corte_basico"
        ],
        "faz_sora": [
            "ritual_ashi", "pausa_nagi", "cuidado_hikari",
            "conexao_mizu", "ceu_sora", "massagem_lombar"
        ],
        "nao_faz": [
            "penteados", "tranças", "coloracao_complexa",
            "unhas", "escova_modelada_na_escova"
        ],
        "restricao_critica": "SEMPRE verificar agenda do Spa antes de confirmar Haven",
        "horarios": {
            "segunda": "08:00-20:00 (eventual)",
            "terca": "08:00-20:00",
            "quarta": "08:00-20:00",
            "quinta": "08:00-20:00",
            "sexta": "08:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    "mariana": {
        "nome": "Mariana",
        "apelido": "Mariana",
        "categoria": "cabelo",
        "nivel": "completa_avancada",
        "especialidade": "Cores Complexas e Cortes Técnicos",
        "faz": [
            "penteados", "tranças", "progressiva", "tratamentos_capilares",
            "corte_complexo", "tintura_completa", "retoque_todos_tipos",
            "maquiagem_simples", "manicure_tradicional_mao"
        ],
        "nao_faz": ["pedicure", "gel_unhas"],
        "restricao": "Manicure somente contingência — não atividade principal",
        "horarios": {
            "segunda": "NÃO ATENDE",
            "terca": "12:00-17:30",
            "quarta": "12:00-17:30",
            "quinta": "12:00-17:30",
            "sexta": "12:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    # ─── UNHAS ───
    "davila": {
        "nome": "Dávila",
        "apelido": "Dávila",
        "categoria": "unhas",
        "nivel": "master_unhas",
        "especialidade": "Manicure Avançada e Gel",
        "faz": [
            "manicure_tradicional", "pedicure_tradicional",
            "gel_maos", "gel_pes", "blindagem", "reconstrucao_individual",
            "manicure_russa", "pedicure_russa", "plastica_pes",
            "esmalte_em_gel"
        ],
        "nao_faz": ["cabelo", "maquiagem"],
        "valores": {"manicure": 50.00, "pedicure": 60.00, "gel": 140.00},
        "horarios": {
            "segunda": "08:00-17:00",
            "terca": "08:00-17:00",
            "quarta": "08:00-17:00",
            "quinta": "08:00-17:00",
            "sexta": "08:00-17:00",
            "sabado": "08:00-17:00"
        }
    },
    
    "luisa": {
        "nome": "Luisa",
        "apelido": "Lu",
        "categoria": "unhas",
        "nivel": "senior_unhas",
        "especialidade": "Manicure e Gel",
        "faz": [
            "manicure_tradicional", "pedicure_tradicional",
            "gel_maos", "gel_pes"
        ],
        "nao_faz": ["reconstrucao_individual", "cabelo", "maquiagem"],
        "restricao": "Reconstrução individual: redirecionar para Dávila",
        "valores": {"manicure": 42.00, "pedicure": 45.00, "gel": 120.00},
        "horarios": {
            "segunda": "NÃO ATENDE",
            "terca": "08:00-20:00",
            "quarta": "08:00-20:00",
            "quinta": "08:00-20:00",
            "sexta": "08:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    "edna": {
        "nome": "Edna",
        "apelido": "Edna",
        "categoria": "unhas",
        "nivel": "junior",
        "especialidade": "Manicure Tradicional",
        "faz": [
            "manicure_tradicional", "pedicure_tradicional",
            "maquiagem_leve"
        ],
        "em_treinamento": ["apoio_spa"],
        "nao_faz": ["gel", "reconstrucao", "cabelo"],
        "valores": {"manicure": 42.00, "pedicure": 45.00},
        "horarios": {
            "segunda": "08:00-20:00",
            "terca": "08:00-20:00",
            "quarta": "FOLGA",
            "quinta": "08:00-20:00",
            "sexta": "08:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    # ─── MAQUIAGEM / ESTÉTICA ───
    "tay": {
        "nome": "Tay",
        "apelido": "Tay",
        "categoria": "estetica_facial",
        "nivel": "especialista",
        "especialidade": "Maquiagem e Sobrancelhas",
        "faz": [
            "maquiagem_casual", "maquiagem_social", "maquiagem_festa",
            "maquiagem_noiva", "design_sobrancelha", "design_sobrancelha_com_tintura",
            "brow_lamination", "lash_lifting", "epilacao_facial_linha",
            "manicure_tradicional"
        ],
        "nao_faz": ["cabelo", "gel_unhas", "pedicure"],
        "restricao": "Unhas somente contingência — iniciante",
        "horarios": {
            "segunda": "NÃO ATENDE",
            "terca": "08:00-20:00",
            "quarta": "08:00-20:00",
            "quinta": "08:00-20:00",
            "sexta": "08:00-20:00",
            "sabado": "08:00-20:00"
        }
    },
    
    # ─── FREELANCER ───
    "cintia": {
        "nome": "Cíntia",
        "apelido": "Cíntia",
        "categoria": "freelancer",
        "nivel": "especialista_cachos",
        "especialidade": "Fitagem (Definição de Cachos)",
        "faz": ["fitagem_cachos"],
        "nao_faz": ["progressiva", "tintura", "unhas", "maquiagem"],
        "disponibilidade": {
            "semana": "até 16h",
            "sabado": "até 16h/17h máximo"
        },
        "protocolo": "NUNCA confirmar sem checar com Cíntia antes",
        "contato_necessario": True
    },
    
    # ─── EXCLUSIVO ───
    "suzana": {
        "nome": "Suzana",
        "apelido": "Suzana",
        "categoria": "proprietaria",
        "nivel": "especialista_alongamento",
        "especialidade": "Alongamento de Unhas (EXCLUSIVO)",
        "faz": ["alongamento_unhas"],
        "valores": {"alongamento": 450.00},
        "inclui": ["gel", "cutelagem_russa"],
        "observacao": "Alongamento SOMENTE pela Suzana. Confirmar disponibilidade antes de vender."
    }
}

# ═══════════════════════════════════════════════
# 2. SERVIÇOS E PREÇOS (Documento 2)
# ═══════════════════════════════════════════════

SERVICOS = {
    # ─── CABELO ───
    "escova_lisa": {
        "nome": "Escova Lisa",
        "valor": 59.00,
        "valor_promo_seg_qua": 49.00,
        "inclui_escova": True,
        "duracao_min": 45,
        "duracao_max": 60,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "cabelo"
    },
    
    "escova_modelada": {
        "nome": "Escova Modelada",
        "valor": 69.00,
        "valor_promo_seg_qua": 49.00,
        "inclui_escova": True,
        "duracao_min": 45,
        "duracao_max": 60,
        "quem_faz": ["yujaira", "mariana"],
        "nota": "Carla: somente babyliss",
        "categoria": "cabelo"
    },
    
    "adicional_mega": {
        "nome": "Adicional Mega Hair",
        "valor": 20.00,
        "tipo": "adicional",
        "categoria": "cabelo"
    },
    
    "penteado_basico": {
        "nome": "Penteado Básico",
        "valor": 115.00,
        "valor_promo_seg_qua": 99.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "duracao_max": 40,
        "quem_faz": ["yujaira", "mariana"],
        "alerta": "NÃO inclui escova — comunicar sempre",
        "categoria": "cabelo"
    },
    
    "penteado_plus": {
        "nome": "Penteado Plus",
        "valor": 139.00,
        "valor_promo_seg_qua": 99.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "duracao_max": 40,
        "quem_faz": ["yujaira", "mariana"],
        "alerta": "NÃO inclui escova — comunicar sempre",
        "categoria": "cabelo"
    },
    
    "penteado_premium": {
        "nome": "Penteado Premium",
        "valor": 169.00,
        "inclui_escova": False,
        "duracao_min": 40,
        "duracao_max": 60,
        "quem_faz": ["yujaira", "mariana"],
        "alerta": "NÃO inclui escova — comunicar sempre",
        "categoria": "cabelo"
    },
    
    "corte_com_escova": {
        "nome": "Corte + Escova Lisa",
        "valor": 170.00,
        "valor_promo_seg_qua": 80.00,
        "inclui_escova": True,
        "duracao_min": 80,
        "quem_faz": ["yujaira", "mariana"],
        "categoria": "cabelo"
    },
    
    "corte_sem_escova": {
        "nome": "Somente Corte (sem escova)",
        "valor": 120.00,
        "valor_promo_seg_qua": 80.00,
        "inclui_escova": False,
        "duracao_min": 45,
        "quem_faz": ["yujaira", "mariana"],
        "nota": "Perguntar: com escova (R$170) ou sem (R$120)?",
        "categoria": "cabelo"
    },
    
    "retoque_raiz": {
        "nome": "Retoque de Raiz",
        "valor": 179.00,
        "inclui_escova": True,
        "duracao_min": 60,
        "pausa_quimica_min": 30,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "nota": "Carla: somente retoque simples",
        "categoria": "cabelo"
    },
    
    "fitagem": {
        "nome": "Fitagem (com difusor)",
        "valor": 85.00,
        "valor_promo_seg_qua": 59.00,
        "duracao_min": 70,
        "quem_faz": ["cintia"],
        "alerta": "Confirmar com Cíntia ANTES de qualquer agendamento",
        "categoria": "cabelo"
    },
    
    "matizacao_loiros": {
        "nome": "Matização de Loiros",
        "valor": 115.00,
        "inclui_escova": True,
        "duracao_min": 60,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "EXCEÇÃO: esta matização INCLUI escova",
        "categoria": "cabelo"
    },
    
    "progressiva_curtos": {
        "nome": "Progressiva Cabelos Curtos",
        "valor": 250.00,
        "inclui_escova": True,
        "duracao_total_min": 180,
        "pausa_quimica": {"min": 40, "max": 70},
        "quem_faz": ["yujaira", "carla", "mariana"],
        "produto": "Borabella Perfecta",
        "categoria": "cabelo"
    },
    
    "progressiva_medios": {
        "nome": "Progressiva Cabelos Médios",
        "valor": 295.00,
        "inclui_escova": True,
        "duracao_total_min": 180,
        "pausa_quimica": {"min": 50, "max": 70},
        "quem_faz": ["yujaira", "carla", "mariana"],
        "produto": "Borabella Perfecta",
        "categoria": "cabelo"
    },
    
    "progressiva_longos": {
        "nome": "Progressiva Cabelos Longos",
        "valor": 380.00,
        "inclui_escova": True,
        "duracao_total_min": 210,
        "duracao_max_min": 240,
        "pausa_quimica": {"min": 60, "max": 90},
        "quem_faz": ["yujaira", "carla", "mariana"],
        "produto": "Borabella Perfecta",
        "categoria": "cabelo"
    },
    
    "cauterizacao_curtos": {
        "nome": "Cauterização Cabelos Curtos",
        "valor": 180.00,
        "inclui_escova": False,
        "duracao_min": 60,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "cabelo"
    },
    
    "cauterizacao_medios": {
        "nome": "Cauterização Cabelos Médios",
        "valor": 210.00,
        "inclui_escova": False,
        "duracao_min": 75,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "cabelo"
    },
    
    "cauterizacao_longos": {
        "nome": "Cauterização Cabelos Longos",
        "valor": 230.00,
        "inclui_escova": False,
        "duracao_min": 90,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "cabelo"
    },
    
    # ─── TRATAMENTOS ───
    "hidratacao": {
        "nome": "Hidratação",
        "valor": 85.00,
        "valor_promo_seg_qua": 50.00,
        "inclui_escova": False,
        "duracao_min": 15,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "nutricao": {
        "nome": "Nutrição",
        "valor": 95.00,
        "inclui_escova": False,
        "duracao_min": 15,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "reconstrucao_truss": {
        "nome": "Reconstrução TRUSS",
        "valor": 110.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "tratamento_labrizza": {
        "nome": "Tratamentos LABRIZZA",
        "valor": 125.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "tratamento_coreano": {
        "nome": "Tratamentos Coreanos",
        "valor": 135.00,
        "inclui_escova": False,
        "duracao_min": 40,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "umectacao": {
        "nome": "Umectação",
        "valor": 65.00,
        "valor_promo_seg_qua": 30.00,
        "inclui_escova": False,
        "duracao_min": 15,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "indicado_para": "cabelo muito ressecado, opaco, pontas secas",
        "alerta": "NÃO inclui escova",
        "categoria": "tratamentos"
    },
    
    "hidratacao_ozonio": {
        "nome": "Hidratação + Ozônio",
        "valor": 50.00,
        "valor_promo_seg_qua": 50.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "tratamentos"
    },
    
    "tratamento_detox": {
        "nome": "Tratamento DETOX",
        "valor": 99.00,
        "inclui_escova": False,
        "duracao_min": 30,
        "quem_faz": ["yujaira", "carla", "mariana"],
        "categoria": "tratamentos"
    },
    
    # ─── UNHAS ───
    "manicure": {
        "nome": "Manicure",
        "valor": 50.00,
        "valor_davila": 50.00,
        "valor_lu_edna": 42.00,
        "duracao_min": 40,
        "quem_faz": ["davila", "luisa", "edna"],
        "categoria": "unhas"
    },
    
    "pedicure": {
        "nome": "Pedicure",
        "valor": 60.00,
        "valor_davila": 60.00,
        "valor_lu_edna": 45.00,
        "duracao_min": 45,
        "quem_faz": ["davila", "luisa", "edna"],
        "categoria": "unhas"
    },
    
    "plastica_pes": {
        "nome": "Plástica dos Pés",
        "valor": 140.00,
        "inclui": ["pedicure_tradicional"],
        "duracao_min": 90,
        "quem_faz": ["davila", "luisa"],
        "alerta": "INCLUI pedicure — NÃO cobrar pedicure separado",
        "categoria": "unhas"
    },
    
    "manicure_russa": {
        "nome": "Manicure Russa",
        "valor": 80.00,
        "duracao_min": 50,
        "quem_faz": ["davila", "luisa"],
        "categoria": "unhas"
    },
    
    "gel_davila": {
        "nome": "Esmaltação em Gel (Dávila)",
        "valor": 140.00,
        "duracao_min": 120,
        "quem_faz": ["davila"],
        "regra_manutencao": "Manutenção = mesmo valor da aplicação",
        "categoria": "unhas"
    },
    
    "gel_lu": {
        "nome": "Esmaltação em Gel (Lu)",
        "valor": 120.00,
        "duracao_min": 120,
        "quem_faz": ["luisa"],
        "regra_manutencao": "Manutenção = mesmo valor da aplicação",
        "categoria": "unhas"
    },
    
    "manutencao_gel": {
        "nome": "Manutenção em Gel",
        "valor": "mesmo_da_aplicacao_original",
        "duracao_min": 90,
        "quem_faz": ["davila", "luisa"],
        "categoria": "unhas"
    },
    
    "remocao_gel": {
        "nome": "Remoção de Gel",
        "valor": 30.00,
        "duracao_min": 30,
        "quem_faz": ["davila", "luisa"],
        "alerta": "PERGUNTA OBRIGATÓRIA: cliente já tem gel?",
        "categoria": "unhas"
    },
    
    "remocao_alongamento": {
        "nome": "Remoção de Alongamento",
        "valor": 30.00,
        "duracao_min": 30,
        "quem_faz": ["davila", "luisa", "suzana"],
        "alerta": "PERGUNTA OBRIGATÓRIA: cliente já tem alongamento?",
        "categoria": "unhas"
    },
    
    "alongamento_suzana": {
        "nome": "Alongamento de Unhas (Suzana)",
        "valor": 450.00,
        "duracao_min": 180,
        "quem_faz": ["suzana"],
        "inclui": ["gel", "cutelagem_russa"],
        "alerta": "EXCLUSIVO Suzana — confirmar disponibilidade",
        "categoria": "unhas"
    },
    
    # ─── MAQUIAGEM ───
    "make_casual": {
        "nome": "Make Casual",
        "valor": 120.00,
        "duracao_min": 40,
        "quem_faz": ["tay", "mariana"],
        "categoria": "maquiagem"
    },
    
    "make_basica": {
        "nome": "Make Básica",
        "valor": 149.00,
        "valor_promo_seg_qua": 110.00,
        "duracao_min": 50,
        "quem_faz": ["tay", "mariana"],
        "categoria": "maquiagem"
    },
    
    "make_premium": {
        "nome": "Make Premium",
        "valor": 195.00,
        "duracao_min": 60,
        "quem_faz": ["tay", "mariana"],
        "categoria": "maquiagem"
    },
    
    # ─── SOBRANCELHAS / ESTÉTICA ───
    "design_sobrancelha": {
        "nome": "Design de Sobrancelha",
        "valor": 60.00,
        "valor_promo_seg_qua": 45.00,
        "duracao_min": 30,
        "quem_faz": ["tay", "yujaira"],
        "categoria": "estetica"
    },
    
    "design_com_tintura": {
        "nome": "Design com Tintura",
        "valor": 80.00,
        "valor_promo_seg_qua": 65.00,
        "duracao_min": 40,
        "quem_faz": ["tay"],
        "categoria": "estetica"
    },
    
    "brow_lamination": {
        "nome": "Brow Lamination",
        "valor": 150.00,
        "duracao_min": 60,
        "quem_faz": ["tay"],
        "adicional_tintura": 30.00,
        "categoria": "estetica"
    },
    
    "lash_lifting": {
        "nome": "Lash Lifting",
        "valor": 165.00,
        "duracao_min": 60,
        "quem_faz": ["tay"],
        "categoria": "estetica"
    },
    
    "epilacao_facial": {
        "nome": "Epilação Facial (linha)",
        "valor": 35.00,
        "duracao_min": 20,
        "quem_faz": ["tay"],
        "categoria": "estetica"
    }
}

# ═══════════════════════════════════════════════
# 3. FÍSICA DOS PROCEDIMENTOS (Documento 5)
# ═══════════════════════════════════════════════
# ATENÇÃO: A ordem NÃO é protocolo - é FÍSICA + LOGÍSTICA
# Baseado em: tempo de preparação, janelas de execução simultânea,
# disponibilidade de profissionais, estabilidade necessária

FISICA_PROCEDIMENTOS = {
    # ─── CABELO ───
    "progressiva": {
        "tempo_total_min": 180,  # 3 horas média
        "fases": [
            {"nome": "lavatorio_antirresiduo", "duracao_min": 20, "cliente_deitada": True},
            {"nome": "pausa_quimica", "duracao_min": 60, "janela_para_outros": True, "janela_min": 40, "janela_max": 90},
            {"nome": "enxague_secagem", "duracao_min": 30, "cliente_deitada": False},
            {"nome": "chapinha_finalizacao", "duracao_min": 90, "cliente_imovel": True, "calor": True}
        ],
        "compativel_durante_janela": ["manicure", "pedicure", "design_sobrancelha"],
        "incompativel_durante": ["maquiagem", "lavatorio"],
        "pos_fases": ["maquiagem", "penteado_simples"]
    },

    "tintura_retoque": {
        "tempo_total_min": 120,  # 2 horas média
        "fases": [
            {"nome": "aplicacao", "duracao_min": 35, "cliente_sentada": True},
            {"nome": "pausa_quimica", "duracao_min": 35, "janela_para_outros": True, "janela_min": 30, "janela_max": 40},
            {"nome": "enxague_matizacao", "duracao_min": 20, "cliente_deitada": True},
            {"nome": "secagem_finalizacao", "duracao_min": 35, "cliente_imovel": False}
        ],
        "compativel_durante_janela": ["manicure_maos"],
        "incompativel_durante": ["pedicure", "maquiagem", "lavatorio"],
        "pos_fases": ["maquiagem", "penteado"]
    },

    "escova_lisa_modelada": {
        "tempo_total_min": 50,
        "fases": [
            {"nome": "lavatorio", "duracao_min": 15, "cliente_deitada": True, "maos_molham": True},
            {"nome": "secagem_escova", "duracao_min": 35, "cliente_sentada": True, "janela_para_outros": True, "janela_min": 20}
        ],
        "compativel_durante_janela": ["manicure_maos"],
        "incompativel_durante": ["maquiagem", "pedicure"],
        "pos_fases": ["maquiagem", "penteado_simples"]
    },

    "penteado": {
        "tempo_total_min": 45,
        "pre_requisito": "cabelo_seco",
        "fases": [
            {"nome": "montagem_penteado", "duracao_min": 45, "cliente_imovel": True, "calor": False}
        ],
        "compativel_durante": [],
        "incompativel_durante": ["maquiagem", "lavatorio"],
        "pos_fases": ["maquiagem"]
    },

    "corte_com_escova": {
        "tempo_total_min": 80,
        "fases": [
            {"nome": "lavatorio", "duracao_min": 15, "cliente_deitada": True},
            {"nome": "corte", "duracao_min": 30, "cliente_sentada": True},
            {"nome": "secagem_escova", "duracao_min": 35, "janela_para_outros": True}
        ],
        "compativel_durante_janela": ["manicure_maos"],
        "pos_fases": ["maquiagem"]
    },

    # ─── UNHAS ───
    "manicure_tradicional": {
        "tempo_total_min": 40,
        "fases": [
            {"nome": "cuticulagem_esmalte", "duracao_min": 40, "cliente_maos_imoveis": True}
        ],
        "compativel_durante": ["escova_secagem", "pausa_progressiva", "pausa_tintura", "penteado"],
        "incompativel_durante": ["lavatorio", "chapinha", "make"],
        "pos_fases": []
    },

    "pedicure_tradicional": {
        "tempo_total_min": 45,
        "fases": [
            {"nome": "cuticulagem_esmalte_pes", "duracao_min": 45, "cliente_pes_imoveis": True, "acesso_pes_necessario": True}
        ],
        "compativel_durante": ["pausa_progressiva_longa", "escova_se_cadeira_permitir"],
        "incompativel_durante": ["lavatorio", "tintura", "chapinha", "make"],
        "pos_fases": []
    },

    "gel_maos": {
        "tempo_total_min": 100,
        "fases": [
            {"nome": "preparacao_base", "duracao_min": 30, "cliente_maos_imoveis": True},
            {"nome": "cura_uv_1", "duracao_min": 3, "maos_na_cabine": True},
            {"nome": "aplicacao_cor", "duracao_min": 30, "cliente_maos_imoveis": True},
            {"nome": "cura_uv_2", "duracao_min": 3, "maos_na_cabine": True},
            {"nome": "finalizacao", "duracao_min": 10, "cliente_maos_imoveis": False}
        ],
        "compativel_durante": ["pausa_progressiva", "escova", "penteado"],
        "incompativel_durante": ["lavatorio", "qualquer_coisa_que_mova_maos"],
        "pos_fases": []
    },

    "remocao_gel_alongamento": {
        "tempo_total_min": 30,
        "obrigatorio_perguntar": True,
        "fases": [
            {"nome": "lixa_remocao", "duracao_min": 30, "cliente_maos_imoveis": True}
        ],
        "compativel_durante": [],
        "incompativel_durante": ["lavatorio"],
        "pos_fases": ["manicure", "gel"]
    },

    # ─── MAQUIAGEM ───
    "maquiagem": {
        "tempo_total_min": 50,
        "sempre_por_ultimo": True,
        "razao": "cliente_precisa_estar_imovel_sem_calor_sem_agua",
        "pre_requisitos_obrigatorios": ["cabelo_finalizado", "unhas_feitas_ou_secas"],
        "fases": [
            {"nome": "preparacao_pele", "duracao_min": 10, "cliente_imovel": True},
            {"nome": "aplicacao_make", "duracao_min": 30, "cliente_imovel": True, "cabeca_estavel": True},
            {"nome": "finalizacao", "duracao_min": 10, "cliente_imovel": True}
        ],
        "compativel_durante": [],
        "incompativel_durante": ["qualquer_coisa"],
        "pos_fases": []
    },

    # ─── SOBRANCELHAS ───
    "design_sobrancelha": {
        "tempo_total_min": 30,
        "fases": [
            {"nome": "design_limpeza", "duracao_min": 30, "cliente_cabeca_imovel": True}
        ],
        "compativel_durante": ["pausa_tintura", "pausa_progressiva", "espera_produto"],
        "incompativel_durante": ["lavatorio", "maquiagem"],
        "pos_fases": ["maquiagem"]
    }
}

# ─── REGRAS DE COMPATIBILIDADE BASEADAS EM FÍSICA ───

REGRAS_FISICAS_ATENDIMENTO = {
    "regra_1_sempre_perguntar_simultaneidade": {
        "descricao": "Sempre perguntar se cliente quer otimizar tempo com 2 profissionais",
        "script": "Você tem preferência por alguma profissional? Se não tiver, consigo organizar com duas e você sai bem mais rápido!"
    },

    "regra_2_identificar_janelas": {
        "descricao": "Identificar janelas de tempo durante pausas químicas",
        "janelas": {
            "progressiva_pausa": {"min": 40, "max": 90, "servicos_possiveis": ["manicure", "pedicure"]},
            "tintura_pausa": {"min": 30, "max": 40, "servicos_possiveis": ["manicure_maos"]}
        }
    },

    "regra_3_nunca_make_antes_cabelo": {
        "descricao": "Make sempre por último - calor/água estragam",
        "razoes": [
            "Cabeleleira mexe com cabelo → estraga make",
            "Calor de secador/chapinha → derrete make",
            "Spray de cabelo → cai no rosto",
            "Cliente precisa estar imóvel → depois de unhas prontas"
        ]
    },

    "regra_4_verificar_disponibilidade_profissionais": {
        "descricao": "Verificar se há 2+ profissionais disponíveis para simultaneidade",
        "logica": "se escovista_disponivel E manicure_disponivel → agendar_em_paralelo"
    },

    "regra_5_considerar_tempos_secagem cura": {
        "descricao": "Adicionar tempo de secagem/cura UV ao total",
        "exemplos": {
            "gel": "+2-3 min por camada de cura UV",
            "progressiva": "+40-90 min de pausa química"
        }
    },

    "regra_6_nunca_lavatorio_com_unhas": {
        "descricao": "Lavatório molha mãos → não pode com unhas feitas",
        "logica": "se lavatorio → nao_pode_unhas_antes"
    },

    "regra_7_calor_estrava_make": {
        "descricao": "Chapinha/secador derretem make",
        "logica": "se chapinha_ou_secador → nao_pode_make_durante"
    },

    "regra_8_cliente_imovel_make": {
        "descricao": "Make requer cliente imóvel e estável",
        "logica": "make_sempre_por_ultimo"
    }
}

# ─── MATRIZ DE COMPATIBILIDADE (SIMPLIFICADA) ───

COMPATIBILIDADE_SERVICOS = {
    # (servico1, servico2): (compativel, condicao)
    ("progressiva_pausa", "manicure"): (True, "pausa >= 40 min"),
    ("progressiva_pausa", "pedicure"): (True, "pausa >= 60 min"),
    ("tintura_pausa", "manicure_maos"): (True, "pausa >= 30 min"),
    ("tintura_pausa", "pedicure"): (False, "cliente não pode mover pés"),
    ("escova_secagem", "manicure"): (True, "durante secagem"),
    ("escova_secagem", "pedicure"): (False, "acesso aos pés difícil"),
    ("penteado", "manicure"): (False, "cliente move mãos"),
    ("penteado", "pedicure"): (True, "se cadeira permitir acesso"),
    ("make", "qualquer_coisa"): (False, "sempre por último"),
    ("lavatorio", "unhas"): (False, "mãos molham"),
    ("chapinha", "make"): (False, "calor derrete make"),
}

# ─── TEMPOS REAIS DE CADA SERVIÇO ───

TEMPOS_REAIS = {
    "escova_lisa": {"min": 45, "medio": 50, "max": 60},
    "escova_modelada": {"min": 45, "medio": 55, "max": 75},
    "penteado_basico": {"min": 30, "medio": 35, "max": 45},
    "penteado_complexo": {"min": 45, "medio": 60, "max": 90},
    "progressiva_curtos": {"min": 150, "medio": 180, "max": 210},
    "progressiva_medios": {"min": 180, "medio": 210, "max": 240},
    "progressiva_longos": {"min": 210, "medio": 240, "max": 270},
    "tintura_retoque": {"min": 90, "medio": 120, "max": 150},
    "manicure": {"min": 35, "medio": 40, "max": 50},
    "pedicure": {"min": 40, "medio": 45, "max": 60},
    "gel_maos": {"min": 90, "medio": 100, "max": 120},
    "make_casual": {"min": 35, "medio": 40, "max": 50},
    "make_completa": {"min": 50, "medio": 60, "max": 90},
    "design_sobrancelha": {"min": 25, "medio": 30, "max": 40}
}

# ═══════════════════════════════════════════════
# 4. CUPONS (Documento 8)
# ═══════════════════════════════════════════════

CUPONS = {
    "PRISCILA10": {
        "blogueira": "Priscila Kuhn",
        "desconto": 0.10,
        "tipo": "porcentagem"
    },
    "EWYLIN10": {
        "blogueira": "Ewylin Salvatori",
        "desconto": 0.10,
        "tipo": "porcentagem"
    },
    "SOLANGE10": {
        "blogueira": "Solange",
        "desconto": 0.10,
        "tipo": "porcentagem"
    },
    "CAROLINE10": {
        "blogueira": "Caroline",
        "desconto": 0.10,
        "tipo": "porcentagem"
    },
    "KETLYN10": {
        "blogueira": "Ketlyn",
        "desconto": 0.10,
        "tipo": "porcentagem"
    }
}

# ═══════════════════════════════════════════════
# 5. PACOTES (Documento 4)
# ═══════════════════════════════════════════════

PACOTES = {
    "gel_3_maos": {
        "nome": "Pacote Gel 3 Aplicações (Mãos)",
        "quantidade": 3,
        "tipo": "gel_maos",
        "valor_lu": 99.00,  # Avulso R$120
        "valor_davila": 120.00,  # Avulso R$140
        "validade_dias": 60,
        "pagamento": "vista_pix_ou_dinheiro"
    },
    
    "gel_6_maos": {
        "nome": "Pacote Gel 6 Aplicações (Mãos)",
        "quantidade": 6,
        "tipo": "gel_maos",
        "valor_lu": 99.00,
        "valor_davila": 120.00,
        "validade_dias": 120,
        "pagamento": "vista_pix_ou_dinheiro"
    },
    
    "gel_pacote_com_pedicure": {
        "nome": "Pacote Gel + Pedicure",
        "tipo": "gel_maos_pedicure",
        "pedicure_lu_edna": 40.00,
        "pedicure_davila": 55.00,
        "gel_pe_lu": 99.00,
        "gel_pe_davila": 120.00
    },
    
    "unhas_tradicionais_4_maos": {
        "nome": "Pacote 4 Mãos",
        "quantidade": 4,
        "tipo": "unhas_tradicionais",
        "valor_davila": 45.00,
        "valor_outras": 38.00,
        "validade_dias": 30
    },
    
    "unhas_tradicionais_4_maos_1_pe": {
        "nome": "Pacote 4 Mãos + 1 Pé",
        "tipo": "unhas_tradicionais_misto",
        "valor_davila_mao": 45.00,
        "valor_davila_pe": 55.00,
        "valor_outras_mao": 38.00,
        "valor_outras_pe": 40.00,
        "validade_dias": 30
    },
    
    "unhas_tradicionais_4_maos_2_pes": {
        "nome": "Pacote 4 Mãos + 2 Pés",
        "tipo": "unhas_tradicionais_misto",
        "valor_davila_mao": 45.00,
        "valor_davila_pe": 55.00,
        "valor_outras_mao": 38.00,
        "valor_outras_pe": 40.00,
        "validade_dias": 40
    },
    
    "escova_4": {
        "nome": "Pacote 4 Escovas",
        "quantidade": 4,
        "tipo": "escovas",
        "lisa": 55.00,  # Avulso R$59
        "modelada": 65.00,  # Avulso R$69
        "validade_dias": 30,
        "pagamento": "vista_pix_ou_dinheiro"
    },
    
    "escova_8": {
        "nome": "Pacote 8 Escovas",
        "quantidade": 8,
        "tipo": "escovas",
        "lisa": 52.00,
        "modelada": 59.00,
        "validade_dias": 60,
        "pagamento": "vista_pix_ou_dinheiro"
    },
    
    "escova_adicional_premium": {
        "coreanos": 30.00,
        "labriza": 25.00,
        "kerastase": 30.00
    }
}

# ═══════════════════════════════════════════════
# 6. UPSELL LAVATÓRIO (Documento 3)
# ═══════════════════════════════════════════════

UPSELL_LAVATORIO = {
    "produtos_coreanos": {
        "adicional": 30.00,
        "descricao": "Produtos coreanos premium"
    },
    "produtos_labrizza": {
        "adicional": 25.00,
        "descricao": "Tratamentos LABRIZZA"
    },
    "produtos_kerastase": {
        "adicional": 30.00,
        "descricao": "Linha Kérastase"
    },
    "script_whatsapp": "Na conversa eu já te passo o valor base com os produtos da casa 😊 No lavatório, se você quiser, a equipe oferece opções premium com acréscimo (coreanos, Labriza ou Kérastase), sempre informando o valor antes. Você só escolhe se quiser, tá!"
}

# ═══════════════════════════════════════════════
# 7. HORÁRIO DE FUNCIONAMENTO
# ═══════════════════════════════════════════════

HORARIOS_FUNCIONAMENTO = {
    "segunda": "08:00-20:00",
    "terca": "08:00-20:00",
    "quarta": "08:00-20:00",
    "quinta": "08:00-20:00",
    "sexta": "08:00-20:00",
    "sabado": "08:00-20:00",
    "domingo": "FECHADO",
    "nota": "Sem pausa para almoço"
}

# ═══════════════════════════════════════════════
# 8. ENDEREÇO E ESTACIONAMENTO
# ═══════════════════════════════════════════════

ENDERECO = {
    "rua": "Rua Mato Grosso",
    "numero": "837E",
    "bairro": "Jardim Itália",
    "cidade": "Chapecó",
    "estado": "SC",
    "estacionamento": "Estacionamento em frente + 4 vagas na esquina"
}

# ═══════════════════════════════════════════════
# 9. GATILHOS DE HANDOFF (Documento 9)
# ═══════════════════════════════════════════════

HANDOFF_TRIGGERS = [
    "procon", "advogado", "processar", "reclamação formal",
    "danos morais", "jurídico", "defesa do consumidor",
    "quero falar com a proprietária", "quero falar com a Suzana",
    "isso é um absurdo", "vou denunciar"
]

HANDOFF_SCRIPT = "Entendi perfeitamente. Vou encaminhar seu caso para avaliação da nossa equipe. Alguém entrará em contato em breve para te dar a melhor solução. 😊"

# ═══════════════════════════════════════════════
# 10. SCRIPTS DE ATENDIMENTO (Documento 11)
# ═══════════════════════════════════════════════

SCRIPTS_ATENDIMENTO = {
    "abertura": "Oi! Seja bem-vinda à Haven 😊 Me diz por favor: qual procedimento você quer fazer e para qual dia/horário você está pensando?",
    
    "diagnostico_rapido": "É para algum evento com horário certo? E nas unhas: você está com gel ou alongamento hoje?",
    
    "pergunta_remocao": "Você está com gel ou alongamento nas mãos ou nos pés?",
    
    "otimizacao_tempo": "Você tem preferência por alguma profissional? Se não tiver, eu consigo otimizar seu tempo e organizar para fazer com duas profissionais e você sair mais rápido!",
    
    "confirmacao_final": "Fechado, {nome} 😊 Agendado {procedimento} no {dia} às {hora}. Você já sabe nossa localização ou quer que eu te envie o endereço certinho? Temos estacionamento em frente ao prédio e também 4 vagas na esquina, caso você prefira não deixar na rua.",
    
    "retencao_sem_horario": "Entendi, para {procedimento} no {dia} nesse horário específico, hoje a agenda fechou. Mas eu consigo te ajudar agora com duas opções bem próximas: {opcao1} ou {opcao2}. Se você tiver flexibilidade, eu também posso tentar encaixe. E se preferir, te coloco na lista de prioridade para te chamar se surgir vaga.",
    
    "upsell_escova": "Na conversa eu já te passo o valor base com os produtos da casa 😊 No lavatório, se você quiser, a equipe oferece opções premium com acréscimo (coreanos, Labriza ou Kérastase), sempre informando o valor antes. Você só escolhe se quiser, tá!",
    
    "cupom": "Perfeito! Com o cupom {NOME10} você tem 10% de desconto. O valor fica R$ {valor} no total. Quer confirmar para {dia/horário}?",
    
    "reclamacao": "Entendi, obrigada por avisar. Me manda por favor as fotos e confirma pra mim a data e o procedimento? Vou encaminhar para avaliação e a gente já te dá a melhor solução pra você sair satisfeita."
}
