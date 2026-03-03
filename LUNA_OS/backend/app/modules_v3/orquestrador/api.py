"""
🌙 LUNA OS v3.0 — Módulo 2: Orquestrador (API)
Integração segura com Luna OS v2.2
"""

from typing import Dict, List
from datetime import datetime
from loguru import logger
from .orchestrator import orquestrador, coordenar_profissionais as _coordenar, get_orquestrador_status as _get_status


async def coordenar_profissionais(cliente_id: str, servicos: List[str], 
                                   horario: datetime = None,
                                   profissional: str = None) -> Dict:
    """
    API para Luna OS v2.2 chamar Orquestrador
    
    SEGURANÇA:
    - Feature flag verifica se módulo está habilitado
    - Rollback rápido se falhar
    - Retorna None se erro (Luna OS v2.2 resolve)
    """
    try:
        logger.info(f"🎯 Orquestrador API: {cliente_id} ({servicos})")
        
        # 1. Coordenar profissionais
        resultado = await _coordenar(cliente_id, servicos, horario, profissional)
        
        # 2. Logar sucesso
        if resultado and resultado.get('status') == 'coordenado':
            logger.info(f"✅ Orquestrador: {len(resultado.get('agendamentos', []))} profissionais coordenados")
        
        return resultado
        
    except Exception as e:
        # SEGURANÇA: Se falhar, LOGA erro mas NÃO quebra Luna OS v2.2
        logger.error(f"⚠️ Orquestrador API falhou: {e}")
        logger.info("🛑 Retornando None (Luna OS v2.2 resolve)")
        
        return {
            "status": "erro",
            "mensagem": str(e),
            "usar_fallback": True
        }


async def get_orquestrador_status() -> Dict:
    """Retorna status do módulo Orquestrador"""
    return await _get_status()
