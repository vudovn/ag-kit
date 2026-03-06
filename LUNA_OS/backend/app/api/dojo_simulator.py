"""
🥋 DOJO SIMULATOR API

Endpoints para simulação de conversas com IA local (Ollama).

Endpoints:
- POST /api/dojo/simulate → Simula conversa única
- POST /api/dojo/simulate/batch → Simula múltiplas conversas
- GET /api/dojo/simulate/results → Resultados das simulações
- GET /api/dojo/personas → Lista personas
- GET /api/dojo/scenarios → Lista cenários

Autor: Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from app.dojo.simulator import DojoSimulator, simulator
from app.dojo.personas import PERSONAS
from app.dojo.scenarios import SCENARIOS

router = APIRouter(prefix="/api/dojo", tags=["Dojo Simulator"])


class SimulateRequest(BaseModel):
    """Request para simulação única"""

    scenario_id: str
    persona_id: str
    max_turns: int = 10


class SimulateBatchRequest(BaseModel):
    """Request para simulação em batch"""

    scenario_ids: List[str]
    persona_ids: List[str]
    max_turns: int = 10


class SimulateResponse(BaseModel):
    """Resposta da simulação"""

    success: bool
    scenario: str
    persona: str
    score: float
    turns: int
    conversation: List[Dict[str, Any]]
    timestamp: str


@router.post("/simulate", response_model=SimulateResponse)
async def simulate_conversation(request: SimulateRequest):
    """
    Simula uma conversa entre cliente virtual e LUNA.

    **Usa Ollama local (Llama 3.2) para gerar respostas do cliente.**

    - **scenario_id:** Cenário a ser simulado
    - **persona_id:** Persona do cliente virtual
    - **max_turns:** Número máximo de trocas de mensagens
    - **save_to_obsidian:** Se salva resultado no Obsidian
    """
    try:
        result = await simulator.simulate_conversation(
            scenario_id=request.scenario_id,
            persona_id=request.persona_id,
            max_turns=request.max_turns,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return SimulateResponse(
            success=True,
            scenario=result["scenario"],
            persona=result["persona"],
            score=result["score"],
            turns=result["turns"],
            conversation=result["conversation"],
            timestamp=result["timestamp"],
        )

    except Exception as e:
        logger.error(f"Erro na simulação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulate/batch")
async def simulate_batch(
    request: SimulateBatchRequest, background_tasks: BackgroundTasks
):
    """
    Simula múltiplas conversas em background.

    **Ideal para treinamento em massa.**
    """
    results = []

    for scenario_id in request.scenario_ids:
        for persona_id in request.persona_ids:
            try:
                result = await simulator.simulate_conversation(
                    scenario_id=scenario_id,
                    persona_id=persona_id,
                    max_turns=request.max_turns,
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Erro na simulação {scenario_id} + {persona_id}: {e}")

    return {
        "success": True,
        "total_simulations": len(results),
        "average_score": (
            sum(r.get("score", 0) for r in results) / len(results) if results else 0
        ),
        "results": results,
    }


@router.get("/simulate/results")
async def get_simulation_results(limit: int = 10):
    """
    Retorna resultados das simulações recentes.
    """
    # Em produção: buscar do Obsidian ou Supabase
    return {
        "results": [],
        "message": "Em implementação - buscará resultados do Obsidian/Supabase",
    }


@router.get("/personas")
async def list_personas():
    """
    Lista todas as personas disponíveis.
    """
    return {"personas": PERSONAS, "total": len(PERSONAS)}


@router.get("/scenarios")
async def list_scenarios():
    """
    Lista todos os cenários disponíveis.
    """
    return {"scenarios": SCENARIOS, "total": len(SCENARIOS)}


@router.get("/status")
async def dojo_status():
    """
    Status do Dojo Simulator.
    """
    ollama_status = "unknown"

    try:
        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://127.0.0.1:11434/api/tags")
            if response.status_code == 200:
                ollama_status = "connected"
            else:
                ollama_status = "error"
    except Exception as e:
        # [DEBT #A9] Manter fallback mas logar erro específico
        logger.debug(f"Dojo Simulator: Ollama não disponível: {e}")
        ollama_status = "disconnected"

    return {
        "status": "operational",
        "ollama": ollama_status,
        "personas": len(PERSONAS),
        "scenarios": len(SCENARIOS),
        "simulator": "initialized",
    }
