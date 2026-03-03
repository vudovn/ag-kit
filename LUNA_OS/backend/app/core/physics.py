"""
LUNA Physics - Física dos Procedimentos
Padrão Elite MCT: Lógica de tempo, compatibilidade e otimização.
"""

from typing import List, Dict, Any
from app.core.config_haven import TEMPOS_REAIS


def analisar_compatibilidade_servicos(
    servicos_solicitados: List[str],
) -> Dict[str, Any]:
    """
    Analisa se serviços podem ser feitos juntos baseado na física dos procedimentos.
    """
    if not servicos_solicitados:
        return {
            "compativel": False,
            "ordem_recommended": [],
            "tempo_total_min": 0,
            "justificativa": "Nenhum serviço solicitado",
            "servicos_simultaneos": [],
        }

    # Verificar se tem maquiagem + algo com calor
    tem_make = any("make" in s for s in servicos_solicitados)
    tem_calor = any(
        "progressiva" in s or "cauterizacao" in s or "tintura" in s
        for s in servicos_solicitados
    )

    if tem_make and tem_calor:
        # Make sempre por último
        servicos_sem_make = [s for s in servicos_solicitados if "make" not in s]
        return {
            "compativel": True,
            "ordem_recommended": servicos_sem_make
            + [s for s in servicos_solicitados if "make" in s],
            "tempo_total_min": calcular_tempo_total(
                servicos_solicitados, simultaneo=False
            ),
            "justificativa": "Make é sempre por último porque calor de secador/chapinha derrete a maquiagem",
            "servicos_simultaneos": [],
        }

    # Verificar janelas de oportunidade (progressiva + unhas)
    tem_progressiva = any("progressiva" in s for s in servicos_solicitados)
    tem_unhas = any(
        "manicure" in s or "pedicure" in s or "gel" in s for s in servicos_solicitados
    )

    if tem_progressiva and tem_unhas:
        # Economia de tempo durante pausa química
        tempo_sequencial = calcular_tempo_total(servicos_solicitados, simultaneo=False)
        economia = 50  # média de economia (40-60 min)

        return {
            "compativel": True,
            "ordem_recommended": servicos_solicitados,
            "tempo_total_min": tempo_sequencial - economia,
            "justificativa": f"Durante a pausa química da progressiva ({economia} min), conseguimos fazer suas unhas! Economia de tempo!",
            "servicos_simultaneos": [
                s
                for s in servicos_solicitados
                if "manicure" in s or "pedicure" in s or "gel" in s
            ],
        }

    # Verificar tintura + manicure (mãos)
    tem_tintura = any("tintura" in s or "retoque" in s for s in servicos_solicitados)
    tem_manicure = any("manicure" in s for s in servicos_solicitados)

    if tem_tintura and tem_manicure:
        tempo_sequencial = calcular_tempo_total(servicos_solicitados, simultaneo=False)
        economia = 35  # média (30-40 min)

        return {
            "compativel": True,
            "ordem_recommended": servicos_solicitados,
            "tempo_total_min": tempo_sequencial - economia,
            "justificativa": f"Durante a pausa da tintura ({economia} min), fazemos suas unhas das mãos!",
            "servicos_simultaneos": [
                s for s in servicos_solicitados if "manicure" in s
            ],
        }

    # Default: sequencial compatível
    return {
        "compativel": True,
        "ordem_recommended": servicos_solicitados,
        "tempo_total_min": calcular_tempo_total(servicos_solicitados, simultaneo=False),
        "justificativa": "Serviços compatíveis em sequência",
        "servicos_simultaneos": [],
    }


def calcular_tempo_total(servicos: List[str], simultaneo: bool = False) -> int:
    """
    Calcula tempo total considerando janelas de simultaneidade.
    """
    if not servicos:
        return 0

    # Somar tempos médios
    tempo_sequencial = 0
    for s in servicos:
        tempo_servico = TEMPOS_REAIS.get(s, {})
        if isinstance(tempo_servico, dict):
            tempo_sequencial += tempo_servico.get("medio", 60)
        else:
            tempo_sequencial += 60  # Default se não for dict

    if not simultaneo:
        return tempo_sequencial

    # Verificar se tem progressiva com janela
    tem_progressiva = any("progressiva" in s for s in servicos)
    tem_unhas = any("manicure" in s or "pedicure" in s for s in servicos)

    if tem_progressiva and tem_unhas:
        # Economiza tempo da janela (40-60 min)
        economia = 50
        return max(0, tempo_sequencial - economia)

    # Verificar tintura + manicure
    tem_tintura = any("tintura" in s or "retoque" in s for s in servicos)
    tem_manicure = any("manicure" in s for s in servicos)

    if tem_tintura and tem_manicure:
        economia = 35
        return max(0, tempo_sequencial - economia)

    return tempo_sequencial


def gerar_script_multi_servicos(servicos: List[str], analise: Dict[str, Any]) -> str:
    """
    Gera script de resposta para múltiplos serviços.
    """
    if not servicos:
        return "Nenhum serviço selecionado."

    resposta = []
    resposta.append(f"Perfeito! Para {' + '.join(servicos)}, podemos fazer assim:")
    resposta.append("")

    if analise.get("servicos_simultaneos"):
        # Tem otimização possível
        resposta.append(
            f"⏱️ **Tempo total: {analise['tempo_total_min']} min** (otimizado!)"
        )
        resposta.append("")
        resposta.append(analise["justificativa"])
    else:
        # Sequencial
        resposta.append(f"⏱️ **Tempo total: {analise['tempo_total_min']} min**")
        resposta.append("")
        resposta.append(analise["justificativa"])

    resposta.append("")
    resposta.append("Você tem preferência por alguma profissional?")
    resposta.append(
        "Se não tiver, consigo organizar com duas profissionais e você sai bem mais rápido!"
    )

    return "\n".join(resposta)
