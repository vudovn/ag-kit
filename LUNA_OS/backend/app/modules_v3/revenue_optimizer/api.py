"""
🌙 LUNA OS v3.0 — Módulo 5: Revenue Optimizer (API)
"""

from typing import Dict, List
from datetime import datetime
from loguru import logger
from .optimizer import revenue_optimizer, calcular_preco_dinamico as _calcular, sugerir_pacote as _sugerir, get_revenue_status as _get_status


async def calcular_preco_dinamico(servico: str, horario: datetime, cliente_id: str = None) -> Dict:
    """API para calcular preço dinâmico"""
    try:
        return await _calcular(servico, horario, cliente_id)
    except Exception as e:
        logger.error(f"⚠️ Revenue Optimizer API falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def sugerir_pacote(servicos: List[str]) -> Dict:
    """API para sugerir pacote"""
    try:
        return await _sugerir(servicos)
    except Exception as e:
        logger.error(f"⚠️ Sugestão de pacote falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def get_revenue_status() -> Dict:
    """Retorna status do módulo"""
    return await _get_status()
