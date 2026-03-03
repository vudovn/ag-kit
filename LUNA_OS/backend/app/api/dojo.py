"""
Dojo API — Training Arena Endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import time

from app.dojo.scenarios import get_scenarios, get_scenario_by_id, SCENARIOS
from app.dojo.personas import get_personas, get_persona_by_id, PERSONAS
from app.dojo.metrics import (
    calculate_empathy_score,
    calculate_clarity_score,
    calculate_actionability_score,
    calculate_success_metrics
)
from app.core.brain import process_message
from app.core.evolution import EvolutionEngine

router = APIRouter(prefix="/api/dojo", tags=["Dojo Arena"])
evolution_engine = EvolutionEngine()

# ==================== MODELS ====================

class DojoTestRequest(BaseModel):
    scenario_id: Optional[str] = None
    persona_id: Optional[str] = None
    message: str
    phone: str = "5549999999999"
    name: str = "Teste Dojo"

class DojoTestResponse(BaseModel):
    scenario_name: str
    persona_name: str
    user_message: str
    luna_response: str
    intent_detected: str
    confidence_score: float
    processing_time_ms: float
    metrics: dict
    success: bool
    points_earned: int

class DojoFeedbackRequest(BaseModel):
    scenario_id: str
    persona_id: str
    message: str
    response: str
    success: bool
    rating: int  # 1-5
    comment: Optional[str] = ""
    metrics: Optional[dict] = None

# ==================== ENDPOINTS ====================

@router.get("/scenarios")
async def list_scenarios(level: str = "all"):
    """
    Lista todos os cenários disponíveis para treino.
    """
    scenarios = get_scenarios(level)
    return {
        "total": len(scenarios),
        "scenarios": scenarios
    }

@router.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """
    Retorna detalhes de um cenário específico.
    """
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.get("/personas")
async def list_personas():
    """
    Lista todas as personas disponíveis.
    """
    return {
        "total": len(PERSONAS),
        "personas": PERSONAS
    }

@router.get("/personas/{persona_id}")
async def get_persona(persona_id: str):
    """
    Retorna detalhes de uma persona específica.
    """
    persona = get_persona_by_id(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

@router.post("/test", response_model=DojoTestResponse)
async def run_dojo_test(request: DojoTestRequest):
    """
    Executa um teste no Dojo Arena.
    Processa a mensagem e retorna resposta + métricas completas.
    """
    start_time = time.time()
    
    # Get scenario info
    scenario = get_scenario_by_id(request.scenario_id) if request.scenario_id else None
    scenario_name = scenario["name"] if scenario else "Custom Test"
    
    # Get persona info
    persona = get_persona_by_id(request.persona_id) if request.persona_id else None
    persona_name = persona["name"] if persona else "Custom Persona"
    
    # Process message with Brain
    result = await process_message(
        phone=request.phone,
        name=request.name,
        message=request.message,
        history=[]
    )
    
    processing_time = (time.time() - start_time) * 1000
    
    # Calculate metrics
    response_text = result.get("response", "")
    detected_intent = result.get("intent", "unknown")
    confidence = result.get("intent_confidence", 0)
    
    # Get scenario criteria for evaluation
    scenario_criteria = scenario.get("success_criteria", []) if scenario else []
    expected_intent = scenario.get("expected_intent", "") if scenario else ""
    
    # Calculate detailed metrics
    metrics = calculate_success_metrics(
        response=response_text,
        expected_intent=expected_intent,
        detected_intent=detected_intent,
        scenario_criteria=scenario_criteria
    )
    
    # Add additional metrics
    metrics["empathy_score"] = calculate_empathy_score(response_text)
    metrics["clarity_score"] = calculate_clarity_score(response_text)
    metrics["actionability_score"] = calculate_actionability_score(response_text)
    metrics["customer_mood"] = persona.get("mood", "unknown") if persona else "unknown"
    metrics["urgency_level"] = 3  # Could extract from intelligence
    metrics["objections_detected"] = []  # Could extract from intelligence
    
    return DojoTestResponse(
        scenario_name=scenario_name,
        persona_name=persona_name,
        user_message=request.message,
        luna_response=response_text,
        intent_detected=detected_intent,
        confidence_score=confidence,
        processing_time_ms=round(processing_time, 2),
        metrics=metrics,
        success=metrics["overall_success"],
        points_earned=metrics["points_earned"]
    )

@router.post("/feedback")
async def submit_feedback(request: DojoFeedbackRequest):
    """
    Salva feedback humano para evolução da LUNA.
    """
    from app.integrations.supabase_client import get_supabase
    
    db = get_supabase()
    
    try:
        record = {
            "scenario_id": request.scenario_id,
            "persona_id": request.persona_id,
            "message": request.message,
            "response": request.response,
            "success": request.success,
            "rating": request.rating,
            "comment": request.comment,
            "metrics": request.metrics or {}
        }
        
        result = db.table("dojo_feedback").insert(record).execute()
        
        return {
            "status": "saved",
            "id": result.data[0]["id"] if result.data else None
        }
    except Exception as e:
        # Table might not exist yet
        return {
            "status": "saved_locally",
            "warning": f"Table may not exist: {str(e)}"
        }

@router.get("/metrics/summary")
async def get_dojo_summary():
    """
    Retorna resumo das métricas do Dojo.
    """
    from app.integrations.supabase_client import get_supabase
    from app.dojo.metrics import calculate_dojo_summary
    
    db = get_supabase()
    
    try:
        # Get last 100 feedback entries
        result = db.table("dojo_feedback").select("*").order("created_at", desc=True).limit(100).execute()
        feedback_list = result.data or []
        
        summary = calculate_dojo_summary(feedback_list)
        
        # Add maturity score
        maturity = await evolution_engine.calculate_maturity_score()
        summary["maturity_score"] = maturity
        
        return summary
    except Exception as e:
        return {
            "total_tests": 0,
            "success_rate": 0,
            "avg_rating": 0,
            "maturity_score": await evolution_engine.calculate_maturity_score()
        }

@router.get("/leaderboard")
async def get_leaderboard():
    """
    Retorna leaderboard de cenários completados.
    """
    from app.integrations.supabase_client import get_supabase
    
    db = get_supabase()
    
    try:
        result = db.table("dojo_feedback").select("scenario_id, success, rating").execute()
        feedback_list = result.data or []
        
        # Group by scenario
        scenario_stats = {}
        for feedback in feedback_list:
            sid = feedback.get("scenario_id")
            if sid not in scenario_stats:
                scenario_stats[sid] = {"attempts": 0, "successes": 0, "ratings": []}
            
            scenario_stats[sid]["attempts"] += 1
            if feedback.get("success"):
                scenario_stats[sid]["successes"] += 1
            if feedback.get("rating"):
                scenario_stats[sid]["ratings"].append(feedback["rating"])
        
        # Build leaderboard
        leaderboard = []
        for scenario in SCENARIOS:
            stats = scenario_stats.get(scenario["id"], {"attempts": 0, "successes": 0, "ratings": []})
            success_rate = (stats["successes"] / stats["attempts"] * 100) if stats["attempts"] > 0 else 0
            avg_rating = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0
            
            leaderboard.append({
                "scenario_id": scenario["id"],
                "scenario_name": scenario["name"],
                "level": scenario["level"],
                "points": scenario["points"],
                "attempts": stats["attempts"],
                "success_rate": round(success_rate, 1),
                "avg_rating": round(avg_rating, 2),
                "completed": stats["successes"] > 0
            })
        
        # Sort by completion and success rate
        leaderboard.sort(key=lambda x: (x["completed"], x["success_rate"]), reverse=True)
        
        return {
            "leaderboard": leaderboard
        }
    except Exception as e:
        return {
            "leaderboard": []
        }
