"""
🥋 DOJO SCENARIOS - Protocolo Haven

Cenários de treino baseados no protocolo oficial da Haven Escovaria & Esmalteria.

Autor: Agent Flow
Data: 2026-03-01
"""

from app.dojo.scenarios import Scenario

# ═══════════════════════════════════════════════
# CENÁRIOS DE ATENDIMENTO (10 cenários)
# ═══════════════════════════════════════════════

SCENARIOS_HAVEN = [
    Scenario(
        id="haven_001",
        name="Agendamento Progressiva + Manicure",
        level="intermediate",
        description="Cliente quer fazer progressiva e manicure no mesmo dia",
        sample_message="Quero fazer progressiva e manicure, tem horário para sábado?",
        expected_intent="agendamento",
        success_criteria=[
            "oferecer_otimizacao_tempo",
            "explicar_pausa_quimica",
            "perguntar_profissional_preferencia"
        ],
        points=25
    ),
    
    Scenario(
        id="haven_002",
        name="Pergunta de Preços - Múltiplos Serviços",
        level="beginner",
        description="Cliente pergunta preços de vários serviços",
        sample_message="Quanto custa escova, manicure e make?",
        expected_intent="preco",
        success_criteria=[
            "informar_todos_precos",
            "mencionar_promocao_seg_qua",
            "oferecer_agendamento"
        ],
        points=15
    ),
    
    Scenario(
        id="haven_003",
        name="Cliente com Pressa - Otimização",
        level="intermediate",
        description="Cliente tem evento e pouco tempo",
        sample_message="Tenho um evento às 19h, consigo fazer cabelo e make até lá?",
        expected_intent="agendamento",
        success_criteria=[
            "calcular_tempo_total",
            "sugerir_comecar_cedo",
            "alertar_make_por_ultimo"
        ],
        points=30
    ),
    
    Scenario(
        id="haven_004",
        name="Pergunta Obrigatória - Remoção de Gel",
        level="beginner",
        description="Cliente quer manicure mas tem gel",
        sample_message="Quero fazer manicure amanhã",
        expected_intent="agendamento",
        success_criteria=[
            "perguntar_tem_gel_ou_alongamento",
            "informar_tempo_remocao",
            "informar_valor_remocao"
        ],
        points=20
    ),
    
    Scenario(
        id="haven_005",
        name="Cupom de Blogueira",
        level="beginner",
        description="Cliente tem cupom de desconto",
        sample_message="Tenho o cupom PRISCILA10, posso usar?",
        expected_intent="cupom",
        success_criteria=[
            "confirmar_cupom_valido",
            "calcular_desconto_10_porcento",
            "aplicar_no_valor_total"
        ],
        points=15
    ),
    
    Scenario(
        id="haven_006",
        name="Make + Cabelo - Ordem Correta",
        level="intermediate",
        description="Cliente quer fazer make e escova",
        sample_message="Quero fazer make e escova para um casamento",
        expected_intent="agendamento",
        success_criteria=[
            "explicar_make_sempre_por_ultimo",
            "sugerir_escova_primeiro",
            "calcular_tempo_total"
        ],
        points=25
    ),
    
    Scenario(
        id="haven_007",
        name="Fitagem - Confirmar com Cíntia",
        level="advanced",
        description="Cliente quer fitagem (cachos)",
        sample_message="Quero fazer fitagem no sábado às 10h",
        expected_intent="agendamento",
        success_criteria=[
            "alertar_precisa_confirmar_cintia",
            "mencionar_horario_limite_16h",
            "nao_confirmar_sem_verificar"
        ],
        points=30
    ),
    
    Scenario(
        id="haven_008",
        name="Alongamento - Exclusivo Suzana",
        level="advanced",
        description="Cliente quer alongamento de unhas",
        sample_message="Quero fazer alongamento de unhas",
        expected_intent="agendamento",
        success_criteria=[
            "informar_exclusivo_suzana",
            "informar_valor_450",
            "confirmar_disponibilidade_suzana"
        ],
        points=30
    ),
    
    Scenario(
        id="haven_009",
        name="Reclamação - Handoff",
        level="expert",
        description="Cliente reclama de serviço anterior",
        sample_message="Fiz unhas aqui semana passada e descascou em 2 dias!",
        expected_intent="reclamacao",
        success_criteria=[
            "receber_com_educacao",
            "pedir_fotos",
            "acionar_handoff_suzana"
        ],
        points=40
    ),
    
    Scenario(
        id="haven_010",
        name="Pacote de Escovas - Explicação",
        level="intermediate",
        description="Cliente quer saber sobre pacote de escovas",
        sample_message="Tem pacote de escovas? Como funciona?",
        expected_intent="pacote",
        success_criteria=[
            "explicar_pacote_4_ou_8_escovas",
            "informar_valores",
            "mencionar_validade",
            "informar_pagamento_vista"
        ],
        points=25
    )
]

# ═══════════════════════════════════════════════
# CENÁRIOS DE ESTRESSE (5 cenários extremos)
# ═══════════════════════════════════════════════

SCENARIOS_ESTRESSE = [
    Scenario(
        id="haven_stress_001",
        name="Urgência Noiva",
        level="expert",
        description="Noiva desesperada com pouco tempo",
        sample_message="Meu casamento é em 3 horas e preciso de cabelo, make e unhas! SOCORRO!",
        expected_intent="urgencia",
        success_criteria=[
            "manter_calma",
            "explicar_tempo_minimo_necessario",
            "oferecer_handoff_imediato"
        ],
        points=50
    ),
    
    Scenario(
        id="haven_stress_002",
        name="Cliente Agressiva - Procon",
        level="expert",
        description="Cliente ameaça chamar Procon",
        sample_message="Vou chamar o Procon! Vocês são uns incompetentes!",
        expected_intent="reclamacao_grave",
        success_criteria=[
            "manter_postura_profissional",
            "nao_discutir",
            "acionar_handoff_suzana_imediato"
        ],
        points=50
    ),
    
    Scenario(
        id="haven_stress_003",
        name="Múltiplos Serviços - Tempo Curto",
        level="expert",
        description="Cliente quer 5 serviços em 2 horas",
        sample_message="Quero progressiva, manicure, pedicure, make e sobrancelha em 2 horas",
        expected_intent="agendamento",
        success_criteria=[
            "explicar_tempo_total_real",
            "sugerir_dividir_em_dois_dias",
            "manter_educada"
        ],
        points=50
    ),
    
    Scenario(
        id="haven_stress_004",
        name="Confusão de Preços",
        level="advanced",
        description="Cliente viu preço errado na internet",
        sample_message="Vi no Google que progressiva custa R$ 150 aqui!",
        expected_intent="preco",
        success_criteria=[
            "informar_preco_correto_250_380",
            "explicar_variacao_tamanho",
            "manter_educada"
        ],
        points=30
    ),
    
    Scenario(
        id="haven_stress_005",
        name="Pedido de Desconto Exagerado",
        level="advanced",
        description="Cliente pede desconto não autorizado",
        sample_message="Faço todo mês, me dá 50% de desconto?",
        expected_intent="desconto",
        success_criteria=[
            "informar_descontos_soente_cupons_blogueiras",
            "mencionar_promocao_seg_qua",
            "manter_educada"
        ],
        points=30
    )
]

# ═══════════════════════════════════════════════
# EXPORTAR TODOS OS CENÁRIOS
# ═══════════════════════════════════════════════

ALL_SCENARIOS = SCENARIOS_HAVEN + SCENARIOS_ESTRESSE

print(f"✅ {len(ALL_SCENARIOS)} cenários Haven carregados")
print(f"   - {len(SCENARIOS_HAVEN)} cenários de atendimento")
print(f"   - {len(SCENARIOS_ESTRESSE)} cenários de estresse")
