"""
🌙 LUNA OS v3.0 — Módulo 6: AI Coach (API)
"""

from typing import Dict, List
from loguru import logger
from .trainer import ai_coach, gerar_treino as _gerar, avaliar_resposta as _avaliar, gerar_relatorio as _relatorio, get_ai_coach_status as _status


async def gerar_treino(categoria: str = "aleatorio", dificuldade: str = "medio") -> Dict:
    """API para gerar treino"""
    try:
        return await _gerar(categoria, dificuldade)
    except Exception as e:
        logger.error(f"⚠️ AI Coach API falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def avaliar_resposta(resposta: str, resposta_ideal: str, pontos_chave: List[str]) -> Dict:
    """API para avaliar resposta"""
    try:
        return await _avaliar(resposta, resposta_ideal, pontos_chave)
    except Exception as e:
        logger.error(f"⚠️ Avaliação falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def gerar_relatorio(cliente_id: str = None) -> Dict:
    """API para gerar relatório"""
    try:
        return await _relatorio(cliente_id)
    except Exception as e:
        logger.error(f"⚠️ Relatório falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def get_ai_coach_status() -> Dict:
    """Retorna status do módulo"""
    return await _status()
