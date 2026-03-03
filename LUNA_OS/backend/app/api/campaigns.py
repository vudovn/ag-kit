"""
Campaigns API Endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid, datetime

router = APIRouter()


class CampaignCreate(BaseModel):
    name: str
    type: str
    status: Optional[str] = "draft"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    discount_percent: Optional[int] = None
    discount_fixed: Optional[float] = None
    services: Optional[List[str]] = []
    trigger_keywords: Optional[List[str]] = []
    message_template: Optional[str] = None
    target_segment: Optional[str] = "todos"
    # Novos campos para objetivos e insights
    objective: Optional[str] = "venda"  # venda, reativacao, branding, followup
    objective_description: Optional[str] = None  # Descrição do objetivo em texto livre
    insights: Optional[str] = None  # Contexto para IA: "Mães preferem manhã", etc
    success_metric: Optional[str] = "agendamentos"  # agendamentos, respostas, cliques
    budget_limit: Optional[float] = None  # Limite de desconto por cliente
    max_uses: Optional[int] = None  # Limite de usos do cupom


@router.post("")
@router.post("/")
async def create_campaign(campaign: CampaignCreate):
    """Create new campaign — direct Supabase insert"""
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()
    record = {
        "id": str(uuid.uuid4()),
        "name": campaign.name,
        "type": campaign.type,
        "status": campaign.status or "draft",
        "start_date": campaign.start_date,
        "end_date": campaign.end_date,
        "discount_percent": campaign.discount_percent,
        "discount_fixed": campaign.discount_fixed,
        "services": campaign.services,
        "trigger_keywords": campaign.trigger_keywords,
        "message_template": campaign.message_template,
        "objective": campaign.objective,
        "objective_description": campaign.objective_description,
        "insights": campaign.insights,
        "success_metric": campaign.success_metric,
        "budget_limit": campaign.budget_limit,
        "max_uses": campaign.max_uses,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }
    try:
        result = db.table("campaigns").insert(record).execute()
        return result.data[0] if result.data else record
    except Exception as e:
        logger.error(f"Erro ao salvar campanha: {e}")
        return record


@router.get("")
@router.get("/")
async def list_campaigns():
    """List all campaigns"""
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()
    result = db.table("campaigns").select("*").order("created_at", desc=True).execute()
    return result.data or []


@router.get("/active")
async def list_active_campaigns():
    """List active campaigns"""
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()
    try:
        result = (
            db.table("campaigns")
            .select("*")
            .eq("status", "active")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data or []
    except Exception:
        return []


@router.patch("/{campaign_id}/status")
async def update_campaign_status(campaign_id: str, status: str):
    """Update campaign status"""
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()
    result = (
        db.table("campaigns").update({"status": status}).eq("id", campaign_id).execute()
    )
    return result.data[0] if result.data else {"error": "Campaign not found"}
