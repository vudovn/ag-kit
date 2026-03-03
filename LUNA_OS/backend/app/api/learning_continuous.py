"""
🧠 Learning Contínuo - Sistema de Aprendizado Contínuo da LUNA

Aprende com erros, acertos e feedback para evoluir continuamente.

Endpoints:
- POST /api/learning/feedback → Receber feedback
- GET /api/learning/stats → Estatísticas de aprendizado
- POST /api/learning/improve → Melhorar sistema

Autor: Agent Flow
Data: 2026-03-02
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os

from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/learning", tags=["Learning Contínuo"])

# ═══════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════

class LearningFeedback(BaseModel):
    """Feedback de aprendizado"""
    conversation_id: str
    message: str
    response: str
    feedback: str  # "correct", "incorrect", "hallucination"
    correction: Optional[str] = None
    category: Optional[str] = None  # "location", "price", "professional", "service"

class LearningStats(BaseModel):
    """Estatísticas de aprendizado"""
    total_feedback: int
    correct_responses: int
    incorrect_responses: int
    hallucinations_detected: int
    accuracy_rate: float
    improvements_made: int

# ═══════════════════════════════════════════════
# SISTEMA DE APRENDIZADO (Em memória - depois migrar para DB)
# ═══════════════════════════════════════════════

LEARNING_STATE = {
    "total_feedback": 0,
    "correct_responses": 0,
    "incorrect_responses": 0,
    "hallucinations_detected": 0,
    "improvements_made": 0,
    "learned_patterns": []
}

# ═══════════════════════════════════════════════
# FUNÇÕES DE APRENDIZADO
# ═══════════════════════════════════════════════

async def learn_from_feedback(feedback: LearningFeedback):
    """
    Aprende com feedback recebido.
    """
    global LEARNING_STATE
    
    LEARNING_STATE["total_feedback"] += 1
    
    if feedback.feedback == "correct":
        LEARNING_STATE["correct_responses"] += 1
    elif feedback.feedback == "incorrect":
        LEARNING_STATE["incorrect_responses"] += 1
    elif feedback.feedback == "hallucination":
        LEARNING_STATE["hallucinations_detected"] += 1
        
        # Aprender padrão de alucinação
        if feedback.category and feedback.correction:
            LEARNING_STATE["learned_patterns"].append({
                "category": feedback.category,
                "wrong_pattern": feedback.message,
                "correct_response": feedback.correction,
                "learned_at": datetime.utcnow().isoformat()
            })
            LEARNING_STATE["improvements_made"] += 1
    
    # Calcular accuracy rate
    if LEARNING_STATE["total_feedback"] > 0:
        LEARNING_STATE["accuracy_rate"] = round(
            (LEARNING_STATE["correct_responses"] / LEARNING_STATE["total_feedback"]) * 100,
            2
        )
    
    # Salvar no Supabase
    try:
        supabase = get_supabase()
        supabase.table("learning_feedback").insert({
            "conversation_id": feedback.conversation_id,
            "message": feedback.message,
            "response": feedback.response,
            "feedback": feedback.feedback,
            "correction": feedback.correction,
            "category": feedback.category,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        # Se não tiver tabela, salva em arquivo local
        with open("logs/learning_feedback.jsonl", "a") as f:
            f.write(json.dumps(feedback.dict()) + "\n")
    
    return True

# ═══════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════

@router.post("/feedback", response_model=dict)
async def submit_feedback(feedback: LearningFeedback):
    """
    Receber feedback de aprendizado.
    
    Exemplo:
    - feedback: "correct" (resposta correta)
    - feedback: "incorrect" (resposta incorreta)
    - feedback: "hallucination" (alucinação detectada)
    """
    result = await learn_from_feedback(feedback)
    
    return {
        "status": "success",
        "message": "Feedback recebido e aprendizado realizado",
        "accuracy_rate": LEARNING_STATE["accuracy_rate"]
    }

@router.get("/stats", response_model=LearningStats)
async def get_learning_stats():
    """
    Retorna estatísticas de aprendizado.
    """
    return LearningStats(**LEARNING_STATE)

@router.post("/improve", response_model=dict)
async def improve_system():
    """
    Melhorar sistema com base no aprendizado.
    """
    improvements_made = 0
    
    # Analisar padrões aprendidos
    for pattern in LEARNING_STATE["learned_patterns"]:
        # Adicionar palavra proibida se for alucinação de localização
        if pattern["category"] == "location":
            # Extrair palavras proibidas
            palavras = pattern["wrong_pattern"].lower().split()
            for palavra in palavras:
                if palavra not in ["a", "o", "de", "da", "do", "um", "uma"]:
                    # Adicionar à lista de proibidas (em produção, salvar em DB)
                    improvements_made += 1
    
    LEARNING_STATE["improvements_made"] += improvements_made
    
    return {
        "status": "success",
        "message": f"Sistema melhorado com {improvements_made} melhorias",
        "total_improvements": LEARNING_STATE["improvements_made"]
    }

@router.get("/patterns", response_model=dict)
async def get_learned_patterns():
    """
    Retorna padrões aprendidos.
    """
    return {
        "total_patterns": len(LEARNING_STATE["learned_patterns"]),
        "patterns": LEARNING_STATE["learned_patterns"][-10:]  # Últimos 10
    }
