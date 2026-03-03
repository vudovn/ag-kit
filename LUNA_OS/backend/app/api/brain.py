"""
Brain API — Simulador interno de conversação
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.brain import process_message, classify_intent, select_model, build_context
from app.core.memory import Memory

router = APIRouter()
memory = Memory()


class SimulateRequest(BaseModel):
    message: str
    phone: str = "5549900000000"  # Número simulado padrão
    name: str = "Teste Interno"
    history: Optional[List[dict]] = None


class SimulateResponse(BaseModel):
    response: str
    intent: str
    intent_confidence: float
    model: str
    sentiment: str
    tokens_estimate: Optional[int] = None
    context_used: bool
    processing_ms: Optional[int] = None


@router.post("/simulate", response_model=dict)
async def simulate_chat(req: SimulateRequest):
    """
    Simula uma conversa com a Luna sem enviar nada ao WhatsApp.
    Executa o pipeline completo: classify → context → openrouter → response.
    """
    start = datetime.utcnow()

    try:
        result = await process_message(
            phone=req.phone,
            name=req.name,
            message=req.message,
            history=req.history or [],
        )

        elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)

        # Classify novamente para retornar confidence
        intent, confidence = classify_intent(req.message)

        return {
            "ok": True,
            "response": result.get("response", ""),
            "intent": result.get("intent", intent),
            "intent_confidence": confidence,
            "model": result.get("model", "unknown"),
            "sentiment": result.get("sentiment", "neutral"),
            "context_used": bool(result.get("context")),
            "processing_ms": elapsed_ms,
            "mode": "simulate — sem envio ao WhatsApp",
        }

    except Exception as e:
        elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        return {"ok": False, "error": str(e), "processing_ms": elapsed_ms}


@router.get("/status")
async def brain_status():
    """Retorna status do brain e modelos configurados"""
    from app.config import settings

    return {
        "status": "online",
        "models": {
            "quick": settings.model_quick,
            "standard": settings.model_standard,
            "complex": settings.model_complex,
        },
        "knowledge_base": "haven.json",
        "intents": 13,
        "mode": "simulate_only",
    }
