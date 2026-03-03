"""
Script para gerar haven.json com dados completos
Fonte: brain.py (PROFISSIONAIS, SERVICOS, REGRAS_NEGOCIO)
"""

import json
import sys
import os

# Adicionar backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.brain import PROFISSIONAIS, SERVICOS, REGRAS_NEGOCIO

def generate_haven_json():
    """Gera haven.json completo"""
    
    # Mapear profissionais para formato JSON
    professionals_json = []
    for id, prof in PROFISSIONAIS.items():
        professionals_json.append({
            "id": id,
            "name": prof.get("apelido", id),
            "nickname": prof.get("apelido", id),
            "empresa": prof.get("empresa", "Haven"),
            "nivel": prof.get("nivel", "junior"),
            "specialties": get_specialties(prof),
            "services": prof.get("faz", []) + prof.get("faz_haven", []),
            "nao_faz": prof.get("nao_faz", []),
            "restricoes": prof.get("restricoes", []),
            "restricao_critica": prof.get("restricao_critica", None),
            "valores": prof.get("valores", {}),
            "disponibilidade": prof.get("disponibilidade", {}),
            "protocolo": prof.get("protocolo", None),
            "observacao": prof.get("observacao", None),
        })
    
    # Mapear serviços para formato JSON
    services_json = []
    for id, serv in SERVICOS.items():
        services_json.append({
            "id": id,
            "name": serv.get("nome", id),
            "valor": serv.get("valor", 0),
            "inclui_escova": serv.get("inclui_escova", False),
            "duracao_min": serv.get("duracao_min", 30),
            "duracao_max": serv.get("duracao_max", serv.get("duracao_min", 30)),
            "quem_faz": serv.get("quem_faz", []),
            "categoria": get_categoria(id),
            "notas": serv.get("nota", serv.get("ALERTA", None)),
            "regra_manutencao": serv.get("regra_manutencao", None),
            "inclui": serv.get("inclui", []),
            "pausa_quimica": serv.get("pausa_quimica", None),
            "produto": serv.get("produto", None),
            "indicado_para": serv.get("indicado_para", None),
        })
    
    # Estrutura completa
    haven_data = {
        "business": {
            "name": "Haven Escovaria & Esmalteria",
            "address": {
                "street": "Rua Mato Grosso, 837E",
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
        },
        "professionals": professionals_json,
        "services": services_json,
        "rules": {
            "ordem_obrigatoria": REGRAS_NEGOCIO.get("ordem_obrigatoria_servicos", []),
            "escova_nao_inclusa_em": REGRAS_NEGOCIO.get("escova_nao_inclusa_em", []),
            "escova_inclusa_em": REGRAS_NEGOCIO.get("escova_inclusa_em", []),
            "pergunta_remocao_gel_obrigatoria": REGRAS_NEGOCIO.get("pergunta_remocao_gel_obrigatoria", []),
            "profissionais_restricoes": REGRAS_NEGOCIO.get("profissionais_restricoes", {}),
            "paralelo_inteligente": REGRAS_NEGOCIO.get("paralelo_inteligente", {}),
            "evento_horario_fixo": REGRAS_NEGOCIO.get("evento_horario_fixo", {}),
        },
        "faq": [
            {
                "id": "faq_1",
                "question": "Tem estacionamento?",
                "answer": "Sim! Temos estacionamento em frente e mais 4 vagas na esquina.",
                "patterns": ["estacionamento", "estacionar", "carro", "vaga"]
            },
            {
                "id": "faq_2",
                "question": "Qual o horário de funcionamento?",
                "answer": "Funcionamos de segunda a sábado, das 8h às 20h, sem pausa para almoço!",
                "patterns": ["horário", "horario", "funcionamento", "abre", "fecha"]
            },
            {
                "id": "faq_3",
                "question": "Aceita cartão?",
                "answer": "Sim! Aceitamos cartão de crédito, débito e PIX.",
                "patterns": ["cartão", "cartao", "crédito", "credito", "débito", "debito", "pix"]
            },
            {
                "id": "faq_4",
                "question": "Precisa agendar?",
                "answer": "Sim! Trabalhamos apenas com horário marcado para te atender melhor.",
                "patterns": ["precisa agendar", "marcação", "marcar", "agendamento"]
            }
        ],
        "packages": {
            "dia_noiva": {
                "nome": "Dia da Noiva",
                "servicos": ["make_premium", "penteado_premium", "manicure_russa", "plastica_pes"],
                "valor": 650.00,
                "duracao": 300,
                "descricao": "Pacote completo para noivas"
            },
            "dia_de_realeza": {
                "nome": "Dia de Realeza",
                "servicos": ["make_basica", "penteado_basico", "manicure_padrao", "pedicure_padrao"],
                "valor": 380.00,
                "duracao": 180,
                "descricao": "Um dia especial completo"
            }
        },
        "coupons": [
            {
                "code": "PRISCILA10",
                "discount": 0.10,
                "description": "10% de desconto",
                "valid_until": "2026-12-31"
            },
            {
                "code": "EWYLIN10",
                "discount": 0.10,
                "description": "10% de desconto",
                "valid_until": "2026-12-31"
            }
        ]
    }
    
    return haven_data


def get_specialties(prof):
    """Extrai especialidades do profissional"""
    specialties = []
    faz = prof.get("faz", []) + prof.get("faz_haven", [])
    
    if any("cabelo" in s or "progressiva" in s or "penteado" in s for s in faz):
        specialties.append("cabelo")
    if any("unha" in s or "manicure" in s or "pedicure" in s for s in faz):
        specialties.append("unhas")
    if any("make" in s or "maquiagem" in s for s in faz):
        specialties.append("maquiagem")
    if any("sobrancelha" in s or "lash" in s for s in faz):
        specialties.append("estetica_facial")
    if any("spa" in s.lower() for s in prof.get("faz_sora", [])):
        specialties.append("spa")
    
    return specialties


def get_categoria(service_id):
    """Determina categoria do serviço"""
    if any(x in service_id for x in ["cabelo", "escova", "penteado", "progressiva", "corte", "retoque", "matizacao", "fitagem", "hidratacao", "nutricao", "reconstrucao", "umectacao"]):
        return "cabelo"
    elif any(x in service_id for x in ["unha", "manicure", "pedicure", "gel", "alongamento", "plastica"]):
        return "unhas"
    elif any(x in service_id for x in ["make", "maquiagem"]):
        return "maquiagem"
    elif any(x in service_id for x in ["sobrancelha", "lash", "brow", "epilacao"]):
        return "estetica"
    else:
        return "outros"


if __name__ == "__main__":
    # Gerar dados
    haven_data = generate_haven_json()
    
    # Salvar
    output_path = os.path.join(os.path.dirname(__file__), "data", "haven.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(haven_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ haven.json gerado com sucesso!")
    print(f"📊 Profissionais: {len(haven_data['professionals'])}")
    print(f"📊 Serviços: {len(haven_data['services'])}")
    print(f"📊 FAQ: {len(haven_data['faq'])}")
    print(f"📊 Pacotes: {len(haven_data['packages'])}")
    print(f"📊 Cupons: {len(haven_data['coupons'])}")
    print(f"\n📁 Arquivo: {output_path}")
