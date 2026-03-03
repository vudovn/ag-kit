"""Knowledge Base API — Brain da Luna (Schema Real)

Usa o schema real do Supabase: (id, category, key, data JSONB)
onde `data` contém todos os campos estruturados (nome, preço, horários etc.)
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Any, Optional
from app.integrations.supabase_client import get_supabase
from app.services.brain_structurer import brain_structurer
from app.core.rate_limit import limiter
import json
import uuid

router = APIRouter()


class KnowledgeCreate(BaseModel):
    category: (
        str  # service | professional | rule | faq | coupon | package | business_info
    )
    key: str  # Unique identifier within category
    data: dict  # JSONB — structured data (nome, preço, horários etc.)


class KnowledgeUpdate(BaseModel):
    key: Optional[str] = None
    data: Optional[dict] = None


@router.get("")
@router.get("/")
@limiter.limit("100/minute")
async def get_knowledge(request: Request, category: Optional[str] = None):
    """Return all knowledge items, optionally filtered by category"""
    try:
        db = get_supabase()
        query = db.table("knowledge_base").select("*")

        if category and category != "all":
            query = query.eq("category", category)

        result = query.order("category").execute()
        return result.data or []
    except Exception as e:
        return []


@router.get("/{category}")
@limiter.limit("100/minute")
async def get_knowledge_by_category(request: Request, category: str):
    """Return knowledge items filtered by category"""
    try:
        db = get_supabase()
        result = (
            db.table("knowledge_base")
            .select("*")
            .eq("category", category)
            .order("key")
            .execute()
        )
        return result.data or []
    except Exception as e:
        return []


@router.post("")
@router.post("/")
@limiter.limit("30/minute")
async def create_knowledge_item(request: Request, item: KnowledgeCreate):
    """Create a new knowledge item using (category, key, data JSONB)"""
    db = get_supabase()
    try:
        record = {
            "id": str(uuid.uuid4()),
            "category": item.category,
            "key": item.key,
            "data": json.dumps(item.data) if isinstance(item.data, dict) else item.data,
        }
        result = db.table("knowledge_base").insert(record).execute()
        return {"status": "created", "item": result.data[0] if result.data else record}
    except Exception as e:
        raise HTTPException(500, f"Erro ao salvar: {str(e)}")


@router.delete("/{item_id}")
@limiter.limit("30/minute")
async def delete_knowledge_item(request: Request, item_id: str):
    """Delete a knowledge item by id"""
    db = get_supabase()
    try:
        db.table("knowledge_base").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(500, f"Erro ao deletar: {str(e)}")


@router.put("/{item_id}")
@limiter.limit("30/minute")
async def update_knowledge_item(request: Request, item_id: str, item: KnowledgeUpdate):
    """Update an existing knowledge item"""
    db = get_supabase()
    try:
        record_update = {}
        if item.key is not None:
            record_update["key"] = item.key
        if item.data is not None:
            record_update["data"] = (
                json.dumps(item.data) if isinstance(item.data, dict) else item.data
            )

        if not record_update:
            raise HTTPException(400, "Nenhum campo para atualizar")

        result = (
            db.table("knowledge_base").update(record_update).eq("id", item_id).execute()
        )
        return {"status": "updated", "item": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erro ao atualizar: {str(e)}")


@router.post("/structure")
@router.post("/structure/")
@limiter.limit("30/minute")
async def structure_knowledge(request: Request, body: dict):
    """Convert plain text to structured JSON using AI"""
    text = body.get("text")
    category = body.get("category")

    if not text:
        raise HTTPException(400, "Texto é obrigatório")

    structured_data = await brain_structurer.structure(text, category)
    return {"structured_data": structured_data}
