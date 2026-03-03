"""
🌙 LUNA OS v3.0 — Módulo 8: Heat Map (API)
"""

from typing import Dict
from loguru import logger
from .visualizer import heat_map, gerar_heatmap_agenda as _heatmap_agenda, gerar_heatmap_receita as _heatmap_receita, gerar_dashboard_unificado as _dashboard, get_heat_map_status as _status


async def gerar_heatmap_agenda() -> Dict:
    """API para heatmap de agenda"""
    try:
        return await _heatmap_agenda()
    except Exception as e:
        logger.error(f"⚠️ Heatmap agenda falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def gerar_heatmap_receita() -> Dict:
    """API para heatmap de receita"""
    try:
        return await _heatmap_receita()
    except Exception as e:
        logger.error(f"⚠️ Heatmap receita falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def gerar_dashboard_unificado() -> Dict:
    """API para dashboard unificado"""
    try:
        return await _dashboard()
    except Exception as e:
        logger.error(f"⚠️ Dashboard falhou: {e}")
        return {"status": "erro", "mensagem": str(e)}


async def get_heat_map_status() -> Dict:
    """Retorna status do módulo"""
    return await _status()
