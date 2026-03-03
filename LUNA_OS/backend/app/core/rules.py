"""
LUNA Rules - Regras de Negativação e Blindagem
Padrão Elite MCT: Zero alucinação em dados críticos.
"""

NEGATION_RULES = {
    "localizacao": {
        "proibido": [
            "próximo a",
            "perto de",
            "ao lado de",
            "em frente a",
            "pracinha",
            "praça",
        ],
        "obrigatorio": "Rua Mato Grosso, 837E - Jardim Itália, Chapecó-SC",
        "resposta_segura": "Nosso endereço é Rua Mato Grosso, 837E - Jardim Itália, Chapecó-SC. Temos estacionamento em frente + 4 vagas na esquina!",
    },
    "preco": {
        "proibido": [
            "mais ou menos",
            "em torno de",
            "acho que",
            "talvez",
            "provavelmente",
        ],
        "obrigatorio": "consultar_preco_real",
        "resposta_segura": "Deixe-me verificar o preço exato desse serviço",
    },
    "profissionais": {
        "proibido": ["todos", "todas", "qualquer"],
        "obrigatorio": "usar_lista_real",
        "lista_real": ["Yujaira", "Carla", "Dávila", "Luisa", "Edna", "Tay"],
        "resposta_segura": "Essa profissional não faz parte da nossa equipe. Temos Yujaira, Carla, Dávila, Luisa, Edna e Tay.",
    },
    "servicos": {
        "proibido": ["todos os serviços", "todos os tipos"],
        "obrigatorio": "usar_cardapio_real",
        "resposta_segura": "Esse serviço não está no nosso cardápio. Posso te ajudar com nossos serviços reais!",
    },
}


def verificar_regras_negativação(response: str) -> str:
    """
    Verifica se a resposta viola regras de negativação.
    Se violar, retorna resposta segura.
    """
    response_lower = response.lower()

    # Verificar localização
    if "localizacao" in NEGATION_RULES:
        for palavra_proibida in NEGATION_RULES["localizacao"]["proibido"]:
            if palavra_proibida in response_lower:
                return NEGATION_RULES["localizacao"]["resposta_segura"]

    # Verificar preço
    if "preco" in NEGATION_RULES:
        for palavra_proibida in NEGATION_RULES["preco"]["proibido"]:
            if palavra_proibida in response_lower:
                return NEGATION_RULES["preco"]["resposta_segura"]

    # Verificar profissionais
    if "profissionais" in NEGATION_RULES:
        for palavra_proibida in NEGATION_RULES["profissionais"]["proibido"]:
            if palavra_proibida in response_lower:
                return NEGATION_RULES["profissionais"]["resposta_segura"]

    # Verificar serviços
    if "servicos" in NEGATION_RULES:
        for palavra_proibida in NEGATION_RULES["servicos"]["proibido"]:
            if palavra_proibida in response_lower:
                return NEGATION_RULES["servicos"]["resposta_segura"]

    # Se passou por todas as regras, retorna resposta original
    return response
