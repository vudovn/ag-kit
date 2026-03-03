"""
Dojo Scenarios — Pre-defined training scenarios for LUNA
"""

from typing import List, Dict, Optional

# ==================== SCENARIOS DATABASE ====================

SCENARIOS = [
    # NÍVEL 1: BÁSICO
    {
        "id": "scenario_001",
        "name": "Saudação Simples",
        "level": "beginner",
        "description": "Cliente envia saudação inicial",
        "sample_message": "Oi! Bom dia!",
        "expected_intent": "saudacao",
        "success_criteria": ["warm_response", "offer_help"],
        "points": 10,
    },
    {
        "id": "scenario_002",
        "name": "Pergunta de Horário",
        "level": "beginner",
        "description": "Cliente pergunta horário de funcionamento",
        "sample_message": "Qual o horário de vocês?",
        "expected_intent": "horario_func",
        "success_criteria": ["accurate_hours", "friendly_tone"],
        "points": 10,
    },
    {
        "id": "scenario_003",
        "name": "Pergunta de Localização",
        "level": "beginner",
        "description": "Cliente pergunta endereço",
        "sample_message": "Onde fica o salão?",
        "expected_intent": "localizacao",
        "success_criteria": ["accurate_address", "offer_directions"],
        "points": 10,
    },
    {
        "id": "scenario_004",
        "name": "Pergunta de Preço",
        "level": "beginner",
        "description": "Cliente pergunta preço de serviço",
        "sample_message": "Quanto custa uma escova?",
        "expected_intent": "preco",
        "success_criteria": ["accurate_price", "value_proposition"],
        "points": 15,
    },
    {
        "id": "scenario_005",
        "name": "Agendamento Simples",
        "level": "beginner",
        "description": "Cliente quer agendar horário",
        "sample_message": "Quero agendar uma escova para amanhã",
        "expected_intent": "agendamento",
        "success_criteria": ["collect_service", "collect_time", "collect_professional"],
        "points": 20,
    },
    # NÍVEL 2: INTERMEDIÁRIO
    {
        "id": "scenario_006",
        "name": "Múltiplos Serviços",
        "level": "intermediate",
        "description": "Cliente quer fazer vários serviços",
        "sample_message": "Quero fazer unha e escova",
        "expected_intent": "multi_servico",
        "success_criteria": ["upsell_package", "calculate_total_time"],
        "points": 25,
    },
    {
        "id": "scenario_007",
        "name": "Objeção de Preço",
        "level": "intermediate",
        "description": "Cliente acha caro",
        "sample_message": "Achei meio caro...",
        "expected_intent": "objecao",
        "success_criteria": ["empathy", "value_proposition", "alternative_offered"],
        "points": 30,
    },
    {
        "id": "scenario_008",
        "name": "Urgência Alta",
        "level": "intermediate",
        "description": "Cliente precisa para hoje",
        "sample_message": "Preciso de um horário pra HOJE! É urgente!",
        "expected_intent": "agendamento_urgente",
        "success_criteria": ["urgency_detected", "fast_response", "solution_offered"],
        "points": 30,
    },
    {
        "id": "scenario_009",
        "name": "Dúvida Técnica",
        "level": "intermediate",
        "description": "Cliente tem dúvida sobre serviço",
        "sample_message": "Qual a diferença entre progressiva e escova modelada?",
        "expected_intent": "duvida_tecnica",
        "success_criteria": ["clear_explanation", "educational", "recommendation"],
        "points": 25,
    },
    {
        "id": "scenario_010",
        "name": "Comparação com Concorrente",
        "level": "intermediate",
        "description": "Cliente compara com outro salão",
        "sample_message": "No salão da esquina é mais barato",
        "expected_intent": "comparacao",
        "success_criteria": ["differentiate", "value_not_price", "confidence"],
        "points": 30,
    },
    # NÍVEL 3: AVANÇADO
    {
        "id": "scenario_011",
        "name": "Cliente Insatisfeita",
        "level": "advanced",
        "description": "Cliente reclama de serviço anterior",
        "sample_message": "Fiz as unhas aqui e descascou em 2 dias!",
        "expected_intent": "reclamacao",
        "success_criteria": [
            "empathy",
            "apology",
            "solution_offered",
            "handoff_if_needed",
        ],
        "points": 40,
    },
    {
        "id": "scenario_012",
        "name": "Pedido de Reembolso",
        "level": "advanced",
        "description": "Cliente pede reembolso",
        "sample_message": "Quero meu dinheiro de volta",
        "expected_intent": "reembolso",
        "success_criteria": ["policy_explained", "empathy", "handoff_to_human"],
        "points": 45,
    },
    {
        "id": "scenario_013",
        "name": "Crítica nas Redes Sociais",
        "level": "advanced",
        "description": "Cliente ameaça postar crítica",
        "sample_message": "Vou postar no Instagram que foi horrível",
        "expected_intent": "ameaca_crise",
        "success_criteria": ["crisis_management", "empathy", "immediate_handoff"],
        "points": 50,
    },
    {
        "id": "scenario_014",
        "name": "Pedido Especial Complexo",
        "level": "advanced",
        "description": "Cliente pede algo fora do comum",
        "sample_message": "Vocês atendem em casa? É para uma noiva",
        "expected_intent": "pedido_especial",
        "success_criteria": ["creativity", "boundaries", "alternative_offered"],
        "points": 40,
    },
    {
        "id": "scenario_015",
        "name": "Múltiplas Objeções",
        "level": "advanced",
        "description": "Cliente tem várias objeções",
        "sample_message": "É caro, não tenho tempo, e não sei se fica bom",
        "expected_intent": "multiplas_objecoes",
        "success_criteria": ["handle_all_objections", "patience", "close_attempt"],
        "points": 50,
    },
    {
        "id": "scenario_016",
        "name": "Urgência Noiva (Protocolo Ordem)",
        "level": "advanced",
        "description": "Noiva quer subverter a ordem Unha -> Cabelo -> Make",
        "sample_message": "Preciso fazer o cabelo primeiro porque o maquiador chega cedo, pode ser?",
        "expected_intent": "agendamento",
        "success_criteria": ["enforce_order", "explain_logic", "solution_offered"],
        "points": 40,
    },
    {
        "id": "scenario_017",
        "name": "Crise Jurídica / Procon",
        "level": "advanced",
        "description": "Cliente ameaça Procon e exige falar com a dona",
        "sample_message": "Se vocês não resolverem meu problema agora eu vou chamar o Procon e processar esse salão! Quero falar com a dona Suzana AGORA!",
        "expected_intent": "reclamacao",
        "success_criteria": [
            "immediate_handoff",
            "professional_posture",
            "no_escalation",
        ],
        "points": 60,
    },
]

# ==================== FUNCTIONS ====================


def get_scenarios(level: str = "all") -> List[Dict]:
    """Get all scenarios, optionally filtered by level."""
    if level == "all":
        return SCENARIOS
    return [s for s in SCENARIOS if s["level"] == level]


def get_scenario_by_id(scenario_id: str) -> Optional[Dict]:
    """Get a specific scenario by ID."""
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def get_scenarios_by_difficulty() -> Dict[str, List[Dict]]:
    """Group scenarios by difficulty level."""
    return {
        "beginner": [s for s in SCENARIOS if s["level"] == "beginner"],
        "intermediate": [s for s in SCENARIOS if s["level"] == "intermediate"],
        "advanced": [s for s in SCENARIOS if s["level"] == "advanced"],
    }


def calculate_total_points() -> int:
    """Calculate total points available from all scenarios."""
    return sum(s["points"] for s in SCENARIOS)
