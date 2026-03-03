"""
🎯 Marketing Campaigns API

Endpoints para gestão de campanhas de marketing e upsell.

Endpoints:
- GET /api/campaigns/active → Campanhas ativas no período
- GET /api/campaigns/{id} → Buscar campanha específica
- GET /api/upsell/{service_id} → Upsell para serviço específico
- POST /api/campaigns → Criar campanha (admin)

Autor: Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal

from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/campaigns", tags=["Marketing Campaigns"])


# ═══════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════

class CampaignResponse(BaseModel):
    id: str
    name: str
    description: str
    discount_percent: Optional[Decimal]
    start_date: date
    end_date: date
    campaign_script: Optional[str]
    target_services: Optional[List[str]]
    add_on_services: Optional[List[str]]


class UpsellResponse(BaseModel):
    service_name: str
    recommended_services: List[str]
    recommendation_text: str
    priority: int


class CampaignCreateRequest(BaseModel):
    name: str
    description: str
    discount_percent: Optional[Decimal] = 0
    start_date: date
    end_date: date
    target_services: Optional[List[str]] = []
    add_on_services: Optional[List[str]] = []
    campaign_script: Optional[str] = ""


# ═══════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════

@router.get("/active", response_model=List[CampaignResponse])
async def get_active_campaigns():
    """
    Busca campanhas ativas no período atual.
    
    Retorna campanhas onde:
    - is_active = true
    - start_date <= hoje
    - end_date >= hoje
    """
    try:
        supabase = get_supabase()
        
        result = supabase.rpc("get_active_campaigns").execute()
        
        campaigns = []
        for row in result.data:
            campaigns.append(CampaignResponse(
                id=str(row['id']),
                name=row['name'],
                description=row['description'],
                discount_percent=row['discount_percent'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                campaign_script=row['campaign_script'],
                target_services=row.get('target_services', []),
                add_on_services=row.get('add_on_services', [])
            ))
        
        return campaigns
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str):
    """
    Busca campanha específica por ID.
    """
    try:
        supabase = get_supabase()
        
        result = supabase.table("marketing_campaigns").select("*").eq("id", campaign_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        campaign = result.data[0]
        
        return CampaignResponse(
            id=str(campaign['id']),
            name=campaign['name'],
            description=campaign['description'],
            discount_percent=campaign['discount_percent'],
            start_date=campaign['start_date'],
            end_date=campaign['end_date'],
            campaign_script=campaign.get('campaign_script'),
            target_services=campaign.get('target_services', []),
            add_on_services=campaign.get('add_on_services', [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CampaignResponse)
async def create_campaign(request: CampaignCreateRequest):
    """
    Cria nova campanha de marketing.
    """
    try:
        supabase = get_supabase()
        
        campaign_data = {
            "name": request.name,
            "description": request.description,
            "discount_percent": float(request.discount_percent) if request.discount_percent else 0,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "target_services": request.target_services,
            "add_on_services": request.add_on_services,
            "campaign_script": request.campaign_script,
            "is_active": True
        }
        
        result = supabase.table("marketing_campaigns").insert(campaign_data).execute()
        
        campaign = result.data[0]
        
        return CampaignResponse(
            id=str(campaign['id']),
            name=campaign['name'],
            description=campaign['description'],
            discount_percent=campaign['discount_percent'],
            start_date=campaign['start_date'],
            end_date=campaign['end_date'],
            campaign_script=campaign.get('campaign_script'),
            target_services=campaign.get('target_services', []),
            add_on_services=campaign.get('add_on_services', [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════
# UPSELL ENDPOINTS
# ═══════════════════════════════════════════════

@router.get("/upsell/{service_id}", response_model=List[UpsellResponse])
async def get_upsell_for_service(service_id: str):
    """
    Busca oportunidades de upsell para um serviço específico.
    
    Exemplo:
    - Cliente pede "escova_lisa"
    - Retorna: manicure, pedicure, design_sobrancelha
    - Com script de vendas pronto
    """
    try:
        supabase = get_supabase()
        
        result = supabase.rpc("get_upsell_for_service", {"p_service_id": service_id}).execute()
        
        upsells = []
        for row in result.data:
            upsells.append(UpsellResponse(
                service_name=row['service_name'],
                recommended_services=row['recommended_services'],
                recommendation_text=row['recommendation_text'],
                priority=row['priority']
            ))
        
        return upsells
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════
# BRAIN INTEGRATION ENDPOINT
# ═══════════════════════════════════════════════

@router.get("/suggest/{service_id}")
async def suggest_add_ons(service_id: str):
    """
    Endpoint para o Brain usar durante conversas.
    
    Quando cliente solicita um serviço, o Brain chama este endpoint
    para pegar sugestões de upsell e campanhas ativas.
    
    Retorna:
    - Campanhas ativas relacionadas
    - Serviços complementares para upsell
    - Scripts prontos para usar na conversa
    """
    try:
        supabase = get_supabase()
        
        # Buscar campanhas ativas
        campaigns_result = supabase.rpc("get_active_campaigns").execute()
        
        # Buscar upsell para o serviço
        upsell_result = supabase.rpc("get_upsell_for_service", {"p_service_id": service_id}).execute()
        
        # Filtrar campanhas que incluem este serviço
        relevant_campaigns = []
        for campaign in campaigns_result.data:
            if service_id in campaign.get('target_services', []):
                relevant_campaigns.append({
                    "id": str(campaign['id']),
                    "name": campaign['name'],
                    "script": campaign.get('campaign_script', ''),
                    "discount": campaign.get('discount_percent', 0)
                })
        
        # Preparar resposta
        response = {
            "service_id": service_id,
            "active_campaigns": relevant_campaigns,
            "upsell_opportunities": [
                {
                    "service": upsell['service_name'],
                    "recommended": upsell['recommended_services'],
                    "script": upsell['recommendation_text']
                }
                for upsell in upsell_result.data
            ],
            "suggested_script": ""
        }
        
        # Gerar script sugerido
        if relevant_campaigns:
            campaign = relevant_campaigns[0]
            response["suggested_script"] = campaign['script']
        elif upsell_result.data:
            response["suggested_script"] = upsell_result.data[0]['recommendation_text']
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
