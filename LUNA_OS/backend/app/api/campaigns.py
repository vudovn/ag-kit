"""
Campaigns API Endpoints

DEBT #A5: Validação de inputs adicionada
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
import uuid
import datetime
from loguru import logger
from app.core.rate_limit import limiter

router = APIRouter()


# [DEBT #A5] Validação de schema com Pydantic
VALID_CAMPAIGN_TYPES = {"acquisition", "retention", "reactivation", "seasonal", "upsell"}
VALID_STATUSES = {"draft", "active", "paused", "completed", "cancelled"}


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

    # [DEBT #A5] Validadores
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Nome da campanha é obrigatório")
        if len(v) > 200:
            raise ValueError("Nome deve ter no máximo 200 caracteres")
        return v.strip()

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if v not in VALID_CAMPAIGN_TYPES:
            raise ValueError(f"Tipo inválido: {v}. Válidos: {VALID_CAMPAIGN_TYPES}")
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v and v not in VALID_STATUSES:
            raise ValueError(f"Status inválido: {v}. Válidos: {VALID_STATUSES}")
        return v or "draft"

    @field_validator('discount_percent')
    @classmethod
    def validate_discount_percent(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Desconto percentual deve estar entre 0 e 100")
        return v

    @field_validator('discount_fixed')
    @classmethod
    def validate_discount_fixed(cls, v):
        if v is not None and v < 0:
            raise ValueError("Desconto fixo não pode ser negativo")
        return v

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, info):
        if v and info.data.get('start_date'):
            start = info.data['start_date']
            if v < start:
                raise ValueError("end_date deve ser após start_date")
        return v


@router.post("")
@router.post("/")
@limiter.limit("30/minute")  # [DEBT #A6] Rate limiting adicionado
async def create_campaign(request: Request, campaign: CampaignCreate):
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
@limiter.limit("100/minute")
async def list_campaigns(request: Request):
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
