"""
Dojo Personas — Customer personas for training scenarios
"""

from typing import List, Dict, Optional

# ==================== PERSONAS DATABASE ====================

PERSONAS = [
    {
        "id": "persona_001",
        "name": "Cliente Apressada",
        "mood": "hurry",
        "emoji": "🔥",
        "description": "Sempre com pressa, mensagens curtas e diretas",
        "typical_phrases": [
            "Preciso pra hoje!",
            "Tem horário agora?",
            "É urgente!",
            "Rápido por favor",
        ],
        "triggers": ["hoje", "agora", "urgente", "rápido", "pressa"],
        "success_tips": ["Resposta rápida", "Soluções imediatas", "Sem rodeios"],
    },
    {
        "id": "persona_002",
        "name": "Cliente Sensível a Preço",
        "mood": "hesitant",
        "emoji": "💰",
        "description": "Sempre pergunta preço, busca desconto",
        "typical_phrases": [
            "Quanto custa?",
            "Tem desconto?",
            "Achei caro...",
            "Tem promoção?",
        ],
        "triggers": ["preço", "custa", "desconto", "promoção", "caro", "barato"],
        "success_tips": ["Focar em valor", "Oferecer pacotes", "Mostrar benefícios"],
    },
    {
        "id": "persona_003",
        "name": "Cliente Insatisfeita",
        "mood": "frustrated",
        "emoji": "😤",
        "description": "Reclama de serviço anterior",
        "typical_phrases": [
            "Descascou em 2 dias!",
            "Não ficou como eu queria",
            "Já é a segunda vez que...",
            "Estou muito decepcionada",
        ],
        "triggers": ["reclamação", "problema", "erro", "decepção", "não gostei"],
        "success_tips": [
            "Empatia primeiro",
            "Pedir desculpas",
            "Oferecer solução",
            "Handoff se necessário",
        ],
    },
    {
        "id": "persona_004",
        "name": "Cliente Feliz",
        "mood": "happy",
        "emoji": "😊",
        "description": "Satisfeita, quer agendar sempre",
        "typical_phrases": [
            "Amei o resultado!",
            "Quero vir sempre",
            "Vou indicar pra amigas",
            "Ficou perfeito!",
        ],
        "triggers": ["amei", "perfeito", "maravilhoso", "indicação", "sempre"],
        "success_tips": [
            "Reforçar relacionamento",
            "Oferecer fidelidade",
            "Pedir indicação",
        ],
    },
    {
        "id": "persona_005",
        "name": "Cliente Indecisa",
        "mood": "hesitant",
        "emoji": "🤔",
        "description": "Não sabe qual serviço escolher",
        "typical_phrases": [
            "Não sei qual fazer...",
            "Qual você recomenda?",
            "Estou em dúvida",
            "Me ajuda a escolher?",
        ],
        "triggers": ["dúvida", "indecisa", "recomenda", "ajuda", "não sei"],
        "success_tips": ["Fazer perguntas", "Oferecer opções", "Guiar decisão"],
    },
    {
        "id": "persona_006",
        "name": "Cliente Exigente",
        "mood": "frustrated",
        "emoji": "💅",
        "description": "Quer tudo perfeito, muitos detalhes",
        "typical_phrases": [
            "Tem que ficar exatamente assim",
            "Já fiz em 5 lugares e nenhum ficou bom",
            "Quero o melhor profissional",
            "Não aceito menos que perfeição",
        ],
        "triggers": ["perfeição", "exatamente", "melhor", "detalhes"],
        "success_tips": [
            "Validar expectativas",
            "Mostrar portfólio",
            "Oferecer especialista",
        ],
    },
    {
        "id": "persona_007",
        "name": "Cliente Primeira Vez",
        "mood": "happy",
        "emoji": "🌟",
        "description": "Nunca fez o serviço antes",
        "typical_phrases": [
            "É minha primeira vez",
            "Nunca fiz isso antes",
            "Tenho medo",
            "Dói?",
        ],
        "triggers": ["primeira vez", "medo", "nunca fiz", "dúvida"],
        "success_tips": ["Educar", "Tranquilizar", "Explicar processo"],
    },
    {
        "id": "persona_008",
        "name": "Cliente Fidelizada",
        "mood": "happy",
        "emoji": "💜",
        "description": "Vem sempre, já conhece tudo",
        "typical_phrases": [
            "Quero com a Ju como sempre",
            "Vou fazer o de sempre",
            "Já sou cliente há 2 anos",
            "Meu horário habitual",
        ],
        "triggers": ["sempre", "habitual", "já conheço", "de sempre"],
        "success_tips": [
            "Reconhecer fidelidade",
            "Oferecer benefícios",
            "Manter preferências",
        ],
    },
    {
        "id": "persona_009",
        "name": "Noiva Desesperada",
        "mood": "hurry",
        "emoji": "👰",
        "description": "Ansiosa, quer mudar regras de horário",
        "typical_phrases": [
            "Meu dia de noiva tem que ser perfeito",
            "Não posso seguir essa ordem",
            "É o meu casamento!",
            "Preciso de uma exceção",
        ],
        "triggers": ["noiva", "casamento", "exceção", "perfeito", "ordem"],
        "success_tips": [
            "Empatia extrema",
            "Firmeza nas regras",
            "Explicar benefício técnico",
        ],
    },
    {
        "id": "persona_010",
        "name": "Consumidora Agressiva",
        "mood": "frustrated",
        "emoji": "⚖️",
        "description": "Conhece direitos, ameaça judicialmente",
        "typical_phrases": [
            "Vou chamar o Procon",
            "Vou processar vocês",
            "Quero falar com o responsável",
            "Isso é um absurdo",
        ],
        "triggers": ["procon", "processar", "justiça", "advogado", "responsável"],
        "success_tips": ["Handoff imediato", "Formalidade", "Evitar discussão"],
    },
]

# ==================== FUNCTIONS ====================


def get_personas() -> List[Dict]:
    """Get all available personas."""
    return PERSONAS


def get_persona_by_id(persona_id: str) -> Optional[Dict]:
    """Get a specific persona by ID."""
    for persona in PERSONAS:
        if persona["id"] == persona_id:
            return persona
    return None


def get_personas_by_mood() -> Dict[str, List[Dict]]:
    """Group personas by mood."""
    return {
        "happy": [p for p in PERSONAS if p["mood"] == "happy"],
        "frustrated": [p for p in PERSONAS if p["mood"] == "frustrated"],
        "hesitant": [p for p in PERSONAS if p["mood"] == "hesitant"],
        "hurry": [p for p in PERSONAS if p["mood"] == "hurry"],
    }


def get_persona_suggestions_for_scenario(scenario_id: str) -> List[Dict]:
    """Get persona suggestions based on scenario."""
    scenario_persona_map = {
        "scenario_001": ["persona_004", "persona_007"],  # Saudação: Happy, Primeira Vez
        "scenario_002": ["persona_001", "persona_004"],  # Horário: Hurry, Happy
        "scenario_003": [
            "persona_004",
            "persona_007",
        ],  # Localização: Happy, Primeira Vez
        "scenario_004": ["persona_002", "persona_005"],  # Preço: Sensível, Indecisa
        "scenario_005": [
            "persona_004",
            "persona_008",
        ],  # Agendamento: Happy, Fidelizada
        "scenario_006": ["persona_004", "persona_006"],  # Múltiplos: Happy, Exigente
        "scenario_007": ["persona_002", "persona_005"],  # Objeção: Sensível, Indecisa
        "scenario_008": ["persona_001", "persona_006"],  # Urgência: Apressada, Exigente
        "scenario_009": [
            "persona_005",
            "persona_007",
        ],  # Dúvida: Indecisa, Primeira Vez
        "scenario_010": [
            "persona_002",
            "persona_006",
        ],  # Comparação: Sensível, Exigente
        "scenario_011": [
            "persona_003",
            "persona_006",
        ],  # Insatisfeita: Insatisfeita, Exigente
        "scenario_012": [
            "persona_003",
            "persona_006",
        ],  # Reembolso: Insatisfeita, Exigente
        "scenario_013": ["persona_003"],  # Crítica: Insatisfeita
        "scenario_014": [
            "persona_006",
            "persona_007",
        ],  # Especial: Exigente, Primeira Vez
        "scenario_015": [
            "persona_002",
            "persona_003",
        ],  # Múltiplas objeções: Sensível, Insatisfeita
    }

    suggested_ids = scenario_persona_map.get(scenario_id, [])
    return [p for p in PERSONAS if p["id"] in suggested_ids]
