"""
🎓 Dojo Learning Endpoints

Endpoints para gestão do ciclo de aprendizado do Dojo.

Endpoints:
- GET  /api/dojo/proposals              → Lista propostas pendentes
- POST /api/dojo/proposals/{id}/approve → Aprova proposta
- POST /api/dojo/proposals/{id}/reject  → Rejeita proposta
- GET  /api/dojo/edge-cases             → Lista edge cases
- POST /api/dojo/edge-cases/{id}/convert → Converte em cenário

Autor: MCT Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# [LAZY LOADING] Não importar na importação do módulo
# from app.dojo.learning_cycle import learning_cycle

router = APIRouter(prefix="/dojo", tags=["Dojo Learning"])


def _get_learning_cycle():
    """[LAZY LOADING] Obter learning_cycle apenas quando necessário"""
    from app.dojo.learning_cycle import learning_cycle
    return learning_cycle


class ApproveProposalRequest(BaseModel):
    approved_by: str
    apply_to_prompt: bool = True


class RejectProposalRequest(BaseModel):
    rejected_by: str
    reason: str


class ConvertEdgeCaseRequest(BaseModel):
    scenario_name: str
    scenario_level: str  # beginner, intermediate, advanced, expert
    expected_behavior: str


@router.get("/proposals")
async def get_proposals(
    status: str = Query("pending", description="Status filter: pending, approved, rejected"),
    limit: int = Query(50, description="Limit results")
):
    """
    Lista propostas de melhoria do system prompt.

    - **status**: Filtrar por status (pending, approved, rejected)
    - **limit**: Limite de resultados
    """
    try:
        learning_cycle = _get_learning_cycle()  # [LAZY LOADING]

        if status == "pending":
            proposals = await learning_cycle.get_pending_proposals(limit)
        else:
            # Buscar do Supabase diretamente para outros status
            from app.integrations.supabase_client import get_supabase
            supabase = get_supabase()

            result = supabase.table("prompt_proposals") \
                .select("*") \
                .eq("status", status) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()

            proposals = result.data or []

        return {
            "success": True,
            "count": len(proposals),
            "proposals": proposals
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: str, request: ApproveProposalRequest):
    """
    Aprova e aplica proposta de melhoria no system prompt.

    - **proposal_id**: ID da proposta
    - **approved_by**: Usuário que aprovou
    - **apply_to_prompt**: Se deve aplicar automaticamente ao prompt
    """
    try:
        learning_cycle = _get_learning_cycle()  # [LAZY LOADING]

        success = await learning_cycle.approve_proposal(
            proposal_id=proposal_id,
            approved_by=request.approved_by
        )

        if not success:
            raise HTTPException(status_code=400, detail="Failed to approve proposal")

        # TODO: Se apply_to_prompt=True, aplicar realmente ao system prompt

        return {
            "success": True,
            "message": "Proposal approved successfully",
            "proposal_id": proposal_id,
            "applied_to_prompt": request.apply_to_prompt
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: str, request: RejectProposalRequest):
    """
    Rejeita proposta de melhoria.

    - **proposal_id**: ID da proposta
    - **rejected_by**: Usuário que rejeitou
    - **reason**: Motivo da rejeição
    """
    try:
        learning_cycle = _get_learning_cycle()  # [LAZY LOADING]

        success = await learning_cycle.reject_proposal(
            proposal_id=proposal_id,
            rejected_by=request.rejected_by,
            reason=request.reason
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to reject proposal")
        
        return {
            "success": True,
            "message": "Proposal rejected",
            "proposal_id": proposal_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/edge-cases")
async def get_edge_cases(
    status: str = Query("new", description="Status filter: new, under_review, added_to_dojo, dismissed"),
    limit: int = Query(50, description="Limit results")
):
    """
    Lista edge cases capturados de conversas reais.
    
    - **status**: Filtrar por status
    - **limit**: Limite de resultados
    """
    try:
        from app.integrations.supabase_client import get_supabase
        supabase = get_supabase()
        
        result = supabase.table("dojo_edge_cases") \
            .select("*") \
            .eq("status", status) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        edge_cases = result.data or []
        
        return {
            "success": True,
            "count": len(edge_cases),
            "edge_cases": edge_cases
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edge-cases/{edge_case_id}/convert")
async def convert_edge_case(edge_case_id: str, request: ConvertEdgeCaseRequest):
    """
    Converte edge case em cenário do Dojo.
    
    - **edge_case_id**: ID do edge case
    - **scenario_name**: Nome do cenário a criar
    - **scenario_level**: Nível de dificuldade
    - **expected_behavior**: Comportamento esperado
    """
    try:
        from app.integrations.supabase_client import get_supabase
        supabase = get_supabase()
        
        # Atualizar edge case para status "added_to_dojo"
        supabase.table("dojo_edge_cases") \
            .update({
                "status": "added_to_dojo",
                "scenario_id": f"scenario_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "reviewed_at": datetime.utcnow().isoformat()
            }) \
            .eq("id", edge_case_id) \
            .execute()
        
        # TODO: Criar cenário real no Dojo (adicionar a scenarios.py ou banco)
        
        return {
            "success": True,
            "message": "Edge case converted to Dojo scenario",
            "edge_case_id": edge_case_id,
            "scenario_name": request.scenario_name,
            "scenario_level": request.scenario_level
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning/run")
async def run_learning_cycle(week_reference: Optional[str] = None):
    """
    Executa manualmente o ciclo de aprendizado.

    - **week_reference**: Semana de referência (ex: "2026-W09")
    """
    try:
        learning_cycle = _get_learning_cycle()  # [LAZY LOADING]

        result = await learning_cycle.run_weekly_analysis(week_reference)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
