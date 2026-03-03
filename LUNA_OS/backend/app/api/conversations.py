"""Conversations API - Padrão Elite MCT"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
from app.integrations.supabase_client import get_supabase
from app.schemas import ConversationRead, ConversationDetail

router = APIRouter()


# [AUTOMELHORIA] Schema para feedback
class FeedbackRequest(BaseModel):
    message_id: str
    feedback: str  # 'positive' ou 'negative'
    correction: Optional[str] = None  # Texto corrigido (se negativo)


def normalize_conv(c: dict) -> dict:
    """Flatten nested client{name,phone} into top-level client_name / client_phone"""
    client = c.pop("client", None) or {}
    c["client_name"] = client.get("name") or c.get("phone", "")
    c["client_phone"] = client.get("phone") or c.get("phone", "")
    return c


@router.get("", response_model=List[ConversationRead])
@router.get("/", response_model=List[ConversationRead])
async def list_conversations(status: str = None, limit: int = 50):
    logger.info(f"Listando conversas (status={status}, limit={limit})")
    db = get_supabase()
    query = (
        db.table("conversations")
        .select("*, client:clients(name, phone)")
        .order("started_at", desc=True)
        .limit(limit)
    )
    if status:
        query = query.eq("status", status)

    try:
        data = query.execute().data or []
        return [normalize_conv(c) for c in data]
    except Exception as e:
        logger.error(f"Erro ao listar conversas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar conversas")


@router.get("/active", response_model=List[ConversationRead])
async def get_active_conversations():
    logger.info("Buscando conversas ativas")
    db = get_supabase()
    try:
        data = (
            db.table("conversations")
            .select("*, client:clients(name, phone)")
            .eq("status", "active")
            .execute()
            .data
            or []
        )
        return [normalize_conv(c) for c in data]
    except Exception as e:
        logger.error(f"Erro ao buscar conversas ativas: {e}")
        raise HTTPException(
            status_code=500, detail="Falha ao recuperar conversas monitoradas"
        )


@router.get("/handoffs")
async def get_handoffs():
    logger.info("Verificando handoffs pendentes")
    db = get_supabase()
    try:
        return (
            db.table("handoffs")
            .select("*, conversation:conversations(*), client:clients(*)")
            .eq("status", "pending")
            .execute()
            .data
            or []
        )
    except Exception as e:
        logger.error(f"Erro ao buscar handoffs: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar handoffs")


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: str):
    logger.info(f"Buscando detalhes da conversa {conversation_id}")
    db = get_supabase()

    try:
        conv_resp = (
            db.table("conversations")
            .select("*, client:clients(name, phone)")
            .eq("id", conversation_id)
            .execute()
        )

        if not conv_resp.data:
            logger.warning(f"Conversa {conversation_id} não encontrada")
            raise HTTPException(status_code=404, detail="Conversa não encontrada")

        messages_resp = (
            db.table("messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at")
            .execute()
        )

        conv_data = normalize_conv(conv_resp.data[0])
        conv_data["messages"] = messages_resp.data or []

        return conv_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar conversa {conversation_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Erro ao processar histórico da conversa"
        )


@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    """Receber feedback do operador sobre resposta da LUNA (👍/👎)"""
    logger.info(f"📝 Feedback recebido: {req.feedback} para msg {req.message_id}")
    db = get_supabase()

    try:
        # 1. Atualizar coluna feedback na mensagem
        result = (
            db.table("messages")
            .update({"feedback": req.feedback})
            .eq("id", req.message_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Mensagem não encontrada")

        msg_data = result.data[0]

        # 2. Se feedback negativo com correção, alimentar Learning Engine
        if req.feedback == "negative" and req.correction:
            try:
                from app.core.learning import learning

                await learning.capture_correction(
                    phone=msg_data.get("conversation_id", "unknown"),
                    intent=msg_data.get("intent_detected", "general"),
                    luna_response=msg_data.get("content", ""),
                    human_response=req.correction,
                )
                logger.info("🧠 Learning Engine alimentado com correção")
            except Exception as learn_err:
                logger.warning(f"⚠️ Learning Engine falhou: {learn_err}")

        # 3. Se feedback positivo, considerar como golden example
        if req.feedback == "positive":
            try:
                from app.core.learning import learning

                await learning.mark_golden_example(
                    conversation_id=msg_data.get("conversation_id"),
                    intent=msg_data.get("intent_detected", "general"),
                    message="",
                    response=msg_data.get("content", ""),
                )
                logger.info("⭐ Golden example registrado")
            except Exception as learn_err:
                logger.warning(f"⚠️ Golden example falhou: {learn_err}")

        return {"ok": True, "message": f"Feedback '{req.feedback}' registrado"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar feedback: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar feedback")
