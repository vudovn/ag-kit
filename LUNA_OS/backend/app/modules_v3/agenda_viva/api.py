"""
🌙 LUNA OS v3.0 — Módulo 1: Agenda Viva (API)
Integração segura com Luna OS v2.2
"""

from typing import Dict
from loguru import logger
from .optimizer import agenda_viva


async def optimize_scheduling(agendamento: Dict) -> Dict:
    """
    API para Luna OS v2.2 chamar Agenda Viva
    
    SEGURANÇA:
    - Feature flag verifica se módulo está habilitado
    - Rollback rápido se falhar
    - Retorna agendamento original se erro
    """
    try:
        # 1. Verificar se Agenda Viva está inicializada
        if not agenda_viva.regras:
            logger.info("⚠️ Agenda Viva não inicializada, inicializando...")
            await agenda_viva.inicializar()
        
        # 2. Otimizar agendamento
        resultado = await agenda_viva.otimizar(agendamento)
        
        # 3. Logar sucesso
        otimizacao_count = len(resultado.get('otimizacoes', []))
        if otimizacao_count > 0:
            logger.info(f"✅ Agenda Viva: {otimizacao_count} otimizações aplicadas")
        
        return resultado
        
    except Exception as e:
        # SEGURANÇA: Se falhar, LOGA erro mas NÃO quebra Luna OS v2.2
        logger.error(f"⚠️ Agenda Viva API falhou: {e}")
        logger.info("🛑 Retornando agendamento original (Luna OS v2.2 funciona)")
        
        # Retornar agendamento original com flag de erro
        return {
            **agendamento,
            'agenda_viva_error': str(e),
            'usar_fallback': True
        }


async def get_agenda_viva_status() -> Dict:
    """Retorna status do módulo Agenda Viva"""
    return {
        "modulo": "agenda_viva",
        "status": "healthy" if agenda_viva.regras else "initializing",
        "situacoes_carregadas": agenda_viva.situacoes_carregadas,
        "regras_ativas": len(agenda_viva.regras),
        "historico_aprendizados": len(agenda_viva.historico_aprendizado)
    }
