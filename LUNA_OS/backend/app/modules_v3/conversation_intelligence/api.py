"""
🧠 Conversation Intelligence API

API para análise psicológica e comportamental de conversas do WhatsApp.

Endpoints:
- POST /api/conversation-intelligence/analyze → Analisa conversa completa
- GET /api/conversation-intelligence/status → Status dos agentes
- GET /api/conversation-intelligence/insights/:phone → Insights por cliente

Autor: MCT Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from .agents.coordinator_agent import CoordinatorAgent, AgentContext

router = APIRouter(prefix="/api/conversation-intelligence", tags=["Conversation Intelligence"])

# Singleton
coordinator: Optional[CoordinatorAgent] = None


def get_coordinator() -> CoordinatorAgent:
    """Lazy loading do coordinator"""
    global coordinator
    if coordinator is None:
        coordinator = CoordinatorAgent({
            "debug": True,
            "obsidian_path": "/tmp/obsidian",  # Em produção: caminho real
        })
    return coordinator


class MessageInput(BaseModel):
    """Mensagem individual"""
    direction: str  # "inbound" ou "outbound"
    content: str
    timestamp: Optional[str] = None


class AnalyzeRequest(BaseModel):
    """Request para análise de conversa"""
    conversation_id: str
    phone: str
    client_name: Optional[str] = None
    messages: List[MessageInput]
    metadata: Optional[Dict[str, Any]] = {}


class AnalyzeResponse(BaseModel):
    """Resposta da análise"""
    success: bool
    conversation_id: str
    phone: str
    analysis: Dict[str, Any]
    processing_time_ms: int
    timestamp: str


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_conversation(request: AnalyzeRequest):
    """
    Analisa conversa completa usando equipe de agentes.
    
    **Pipeline:**
    1. ExtractorAgent → Extrai dados
    2. PsychologyAgent → Analisa psicologia
    3. SalesAgent → Analisa vendas
    4. BehaviorAgent → Analisa comportamento
    5. InsightsAgent → Gera insights
    6. StorageAgent → Armazena
    7. LearningAgent → Aprende
    
    **Retorna:**
    - Emoções predominantes
    - Tipo de personalidade (DISC)
    - Estágio no funil
    - Probabilidade de conversão
    - Risco de churn
    - Insights acionáveis
    """
    try:
        coordinator = get_coordinator()
        
        # Criar contexto
        context = AgentContext(
            conversation_id=request.conversation_id,
            phone=request.phone,
            client_name=request.client_name,
            messages=[m.dict() for m in request.messages],
            metadata=request.metadata or {},
        )
        
        # Executar análise
        result = coordinator.analyze_conversation(context, enable_learning=True)
        
        logger.info(f"✅ Análise concluída: {request.conversation_id}")
        
        return AnalyzeResponse(
            success=result.get("success", False),
            conversation_id=request.conversation_id,
            phone=request.phone,
            analysis=result,
            processing_time_ms=result.get("metadata", {}).get("processing_time_ms", 0),
            timestamp=datetime.utcnow().isoformat(),
        )
        
    except Exception as e:
        logger.error(f"❌ Erro na análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_agent_status():
    """
    Retorna status de todos os agentes.
    """
    coordinator = get_coordinator()
    return {
        "status": "operational",
        "agents": coordinator.get_agent_status(),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/insights/{phone}")
async def get_insights_by_phone(phone: str):
    """
    Retorna insights históricos de um cliente.
    
    **Retorna:**
    - Padrões comportamentais
    - Histórico de emoções
    - Evolução no funil
    - Recomendações personalizadas
    """
    # Em produção: buscar do Supabase/Obsidian
    return {
        "phone": phone,
        "insights": [],
        "message": "Em implementação - buscará histórico do Supabase/Obsidian",
    }


@router.get("/health")
async def health_check():
    """Health check do módulo"""
    try:
        coordinator = get_coordinator()
        status = coordinator.get_agent_status()
        
        return {
            "status": "healthy",
            "agents_loaded": len(status),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }
