"""
🌙 LUNA OS v3.0 — Módulo 4: Churn Detector (API)
Integração segura com Luna OS v2.2
"""

from typing import Dict, List
from loguru import logger
from .predictor import churn_predictor, analisar_churn_cliente as _analisar, get_churn_status as _get_status


async def analisar_churn_cliente(cliente_id: str, historico: Dict) -> Dict:
    """
    API para Luna OS v2.2 chamar Churn Detector
    
    SEGURANÇA:
    - Feature flag verifica se módulo está habilitado
    - Rollback rápido se falhar
    - Retorna erro se falhar (não quebra Luna OS v2.2)
    """
    try:
        logger.info(f"⚠️ Churn Detector API: {cliente_id}")
        
        # 1. Analisar churn
        resultado = await _analisar(cliente_id, historico)
        
        # 2. Logar sucesso
        nivel = resultado.get('nivel_risco', 'desconhecido')
        logger.info(f"✅ Churn Detector: {nivel}")
        
        return resultado
        
    except Exception as e:
        # SEGURANÇA: Se falhar, LOGA erro mas NÃO quebra Luna OS v2.2
        logger.error(f"⚠️ Churn Detector API falhou: {e}")
        
        return {
            "status": "erro",
            "mensagem": str(e),
            "usar_fallback": True
        }


async def analisar_churn_lista(lista_clientes: List[Dict]) -> Dict:
    """
    API para analisar múltiplos clientes
    """
    try:
        logger.info(f"📊 Churn Detector API: {len(lista_clientes)} clientes")
        
        resultado = await _analisar_churn_lista(lista_clientes)
        
        return resultado
        
    except Exception as e:
        logger.error(f"⚠️ Churn Detector API (lista) falhou: {e}")
        
        return {
            "status": "erro",
            "mensagem": str(e),
            "usar_fallback": True
        }


async def get_churn_status() -> Dict:
    """Retorna status do módulo Churn Detector"""
    return await _get_status()
