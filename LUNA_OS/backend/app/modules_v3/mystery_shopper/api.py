"""
🌙 LUNA OS v3.0 — Módulo 7: Mystery Shopper (API)
"""

from typing import Dict
from loguru import logger
from .auditor import mystery_shopper, testar_atendimento as _testar, gerar_relatorio_qualidade as _relatorio, get_mystery_status as _status


async def testar_atendimento(perfil: str = "primeira_vez") -> Dict:
    """API para testar atendimento"""
    try:
        return await _testar(perfil)
    except Exception as e:
        logger.error(f"⚠️ Mystery Shopper API falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def gerar_relatorio_qualidade() -> Dict:
    """API para gerar relatório de qualidade"""
    try:
        return await _relatorio()
    except Exception as e:
        logger.error(f"⚠️ Relatório qualidade falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def get_mystery_status() -> Dict:
    """Retorna status do módulo"""
    return await _status()
