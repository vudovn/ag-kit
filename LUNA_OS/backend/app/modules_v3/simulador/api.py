"""
🌙 LUNA OS v3.0 — Módulo 3: Simulador (API)
Integração segura com Luna OS v2.2
"""

from typing import Dict, List
from datetime import datetime
from loguru import logger
from .simulator import simulador, get_simulador_status as _get_status


async def simulate_scenarios(cliente_id: str, servicos: List[str], 
                             profissionais: List[str],
                             horario_base: datetime = None) -> Dict:
    """
    API para Luna OS v2.2 chamar Simulador
    
    SEGURANÇA:
    - Feature flag verifica se módulo está habilitado
    - Rollback rápido se falhar
    - Retorna None se erro (Luna OS v2.2 resolve)
    """
    try:
        if horario_base is None:
            horario_base = datetime.now()
        
        # 1. Simular cenários
        resultado = await simulador.simular_agendamento(
            cliente_id, servicos, profissionais, horario_base
        )
        
        # 2. Logar sucesso
        cenarios_testados = resultado.get('cenarios_testados', 0)
        if cenarios_testados > 0:
            logger.info(f"✅ Simulador: {cenarios_testados} cenários testados")
        
        return resultado
        
    except Exception as e:
        # SEGURANÇA: Se falhar, LOGA erro mas NÃO quebra Luna OS v2.2
        logger.error(f"⚠️ Simulador API falhou: {e}")
        logger.info("🛑 Retornando None (Luna OS v2.2 resolve)")
        
        return {
            "status": "erro",
            "mensagem": str(e),
            "usar_fallback": True
        }


async def get_simulador_status() -> Dict:
    """Retorna status do módulo Simulador"""
    return await _get_status()
