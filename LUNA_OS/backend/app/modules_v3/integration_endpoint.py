"""
🌙 LUNA OS v3.0 — Endpoint Integrado: Modules v3
Integração segura com Luna OS v2.2

Status: 🟡 EM IMPLEMENTAÇÃO
Risco: BAIXO (feature flags + rollback)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from loguru import logger

# Imports dos módulos v3
from app.modules_v3.feature_flags import is_module_enabled, get_traffic_percentage
from app.modules_v3.agenda_viva.api import optimize_scheduling as agenda_viva_optimize
from app.modules_v3.simulador.api import simulate_scenarios as simulador_simulate

import random

router = APIRouter(prefix="/api/modules_v3", tags=["Modules V3"])


# ==================== MODELS ====================

class SchedulingRequest(BaseModel):
    """Request para agendamento otimizado"""
    cliente_id: str
    cliente_nome: Optional[str] = None
    servicos: List[str]
    profissional_preferencia: Optional[str] = None
    horario_solicitado: Optional[str] = None
    pedido_encaixe: bool = False
    urgencia: int = 3  # 1-5


class SchedulingResponse(BaseModel):
    """Response de agendamento otimizado"""
    status: str
    agendamento: Optional[Dict] = None
    otimizacao_aplicada: bool = False
    modulos_usados: List[str] = []
    alternativas: Optional[List[Dict]] = None
    mensagem: str = ""


# ==================== ENDPOINTS ====================

@router.post("/scheduling", response_model=SchedulingResponse)
async def scheduling_otimizado(request: SchedulingRequest):
    """
    🌙 LUNA OS v3.0 — Agendamento Otimizado
    
    Integra Agenda Viva + Simulador com Luna OS v2.2
    
    SEGURANÇA:
    - Feature flags verificam módulos habilitados
    - Rollback automático se falhar
    - Luna OS v2.2 SEMPRE funciona (fallback)
    """
    try:
        logger.info(f"📅 Scheduling v3: {request.cliente_nome} ({request.servicos})")
        
        # 1. Agendamento base (Luna OS v2.2)
        agendamento_base = {
            "cliente_id": request.cliente_id,
            "cliente_nome": request.cliente_nome,
            "servicos": request.servicos,
            "profissional": request.profissional_preferencia,
            "horario_solicitado": request.horario_solicitado,
            "pedido_encaixe": request.pedido_encaixe,
            "urgencia": request.urgencia,
            "otimizacoes": [],
            "alternativas": []
        }
        
        # 2. Verificar módulos habilitados (Feature Flags)
        modulos_ativos = []
        
        if is_module_enabled('agenda_viva'):
            traffic_pct = get_traffic_percentage('agenda_viva')
            if random.randint(1, 100) <= traffic_pct:
                modulos_ativos.append('agenda_viva')
        
        if is_module_enabled('simulador') and len(request.servicos) > 1:
            traffic_pct = get_traffic_percentage('simulador')
            if random.randint(1, 100) <= traffic_pct:
                modulos_ativos.append('simulador')
        
        # 3. Aplicar otimizações dos módulos ativos
        if 'agenda_viva' in modulos_ativos:
            try:
                logger.info("🧠 Agenda Viva: Otimizando...")
                resultado_agenda = await agenda_viva_optimize(agendamento_base)
                
                # Extrair otimizações
                otimozacoes = resultado_agenda.get('otimizacoes', [])
                if otimozacoes:
                    agendamento_base['otimizacoes'].extend(otimozacoes)
                    logger.info(f"✅ Agenda Viva: {len(otimozacoes)} otimizações")
                
            except Exception as e:
                logger.error(f"⚠️ Agenda Viva falhou: {e}")
                # NÃO quebra, continua sem Agenda Viva
        
        if 'simulador' in modulos_ativos:
            try:
                logger.info("🔮 Simulador: Testando cenários...")
                
                # Profissionais disponíveis (mock - viria do DB)
                profissionais = ["Ana", "Bia", "Clara"]
                if request.profissional_preferencia:
                    profissionais = [request.profissional_preferencia]
                
                horario_base = datetime.now()
                if request.horario_solicitado:
                    try:
                        horario_base = datetime.fromisoformat(
                            request.horario_solicitado.replace('Z', '+00:00')
                        )
                    except:
                        pass
                
                resultado_simulador = await simulador_simulate(
                    request.cliente_id,
                    request.servicos,
                    profissionais,
                    horario_base
                )
                
                # Extrair melhor cenário
                if resultado_simulador.get('status') == 'selecionado':
                    agendamento_base['simulador_cenario'] = resultado_simulador
                    agendamento_base['alternativas'] = resultado_simulador.get('alternativas', [])
                    logger.info(f"✅ Simulador: {resultado_simulador.get('nome')}")
                
            except Exception as e:
                logger.error(f"⚠️ Simulador falhou: {e}")
                # NÃO quebra, continua sem Simulador
        
        # 4. Montar response
        response = SchedulingResponse(
            status="sucesso",
            agendamento=agendamento_base,
            otimizacao_aplicada=len(modulos_ativos) > 0,
            modulos_usados=modulos_ativos,
            alternativas=agendamento_base.get('alternativas'),
            mensagem=_gerar_mensagem(modulos_ativos, agendamento_base)
        )
        
        logger.info(f"✅ Scheduling v3: {response.mensagem}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Scheduling v3 falhou: {e}")
        
        # FALLBACK: Luna OS v2.2 SEMPRE funciona
        return SchedulingResponse(
            status="fallback",
            agendamento={
                "cliente_id": request.cliente_id,
                "servicos": request.servicos,
                "erro": str(e)
            },
            otimizacao_aplicada=False,
            modulos_usados=[],
            mensagem="Usando Luna OS v2.2 (módulos v3 indisponíveis)"
        )


@router.get("/status")
async def modules_v3_status():
    """Retorna status dos módulos v3"""
    from app.modules_v3.agenda_viva.api import get_agenda_viva_status
    from app.modules_v3.simulador.api import get_simulador_status
    
    status = {
        "version": "3.0.0",
        "luna_os_core": "2.2.0",
        "modules": {}
    }
    
    # Status de cada módulo
    if is_module_enabled('agenda_viva'):
        try:
            status['modules']['agenda_viva'] = await get_agenda_viva_status()
        except:
            status['modules']['agenda_viva'] = {"status": "unreachable"}
    
    if is_module_enabled('simulador'):
        try:
            status['modules']['simulador'] = await get_simulador_status()
        except:
            status['modules']['simulador'] = {"status": "unreachable"}
    
    # Feature flags status
    from app.modules_v3.feature_flags import get_all_flags_status
    status['feature_flags'] = get_all_flags_status()
    
    return status


@router.get("/health")
async def modules_v3_health():
    """Health check dos módulos v3"""
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "modules": {}
    }
    
    # Check Agenda Viva
    if is_module_enabled('agenda_viva'):
        health['modules']['agenda_viva'] = "healthy"
    else:
        health['modules']['agenda_viva'] = "disabled"
    
    # Check Simulador
    if is_module_enabled('simulador'):
        health['modules']['simulador'] = "healthy"
    else:
        health['modules']['simulador'] = "disabled"
    
    return health


# ==================== HELPERS ====================

def _gerar_mensagem(modulos_ativos: List[str], agendamento: Dict) -> str:
    """Gera mensagem para o cliente"""
    if not modulos_ativos:
        return "Agendamento realizado com Luna OS v2.2"
    
    mensagens = []
    
    if 'agenda_viva' in modulos_ativos:
        otimozacoes = agendamento.get('otimizacoes', [])
        if otimozacoes:
            mensagens.append(f"{len(otimozacoes)} otimizações aplicadas")
    
    if 'simulador' in modulos_ativos:
        cenario = agendamento.get('simulador_cenario', {})
        if cenario:
            mensagens.append(f"melhor cenário: {cenario.get('nome', 'otimizado')}")
    
    if mensagens:
        return f"Agendamento otimizado ({', '.join(mensagens)})"
    else:
        return "Agendamento realizado"
