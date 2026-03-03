"""
✂️ Services API

Endpoints para gestão de serviços.

Endpoints:
- GET /api/services → Listar todos
- GET /api/services/{id} → Buscar um
- GET /api/services/category/{category} → Buscar por categoria

Autor: Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/services", tags=["Services"])


@router.get("")
async def list_services(active_only: bool = True):
    """
    Lista todos os serviços.

    - **active_only**: Se True, retorna apenas ativos (padrão: True)
    """
    try:
        supabase = get_supabase()

        query = supabase.table("knowledge_base").select("*").eq("category", "services")

        if active_only:
            query = query.eq("is_active", True)

        result = query.execute()

        services = []
        for item in result.data:
            service_data = item["data"]
            service_data["id"] = item["id"]
            service_data["key"] = item["key"]
            services.append(service_data)

        return {"services": services, "total": len(services), "success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{service_id}")
async def get_service(service_id: str):
    """
    Busca serviço por ID.

    - **service_id**: ID do serviço (ex: escova_lisa, progressiva_curtos, etc)
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("key", f"service_{service_id}")
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Service not found")

        service_data = result.data[0]["data"]
        service_data["id"] = result.data[0]["id"]
        service_data["key"] = result.data[0]["key"]

        return {"service": service_data, "success": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category}")
async def get_services_by_category(category: str):
    """
    Busca serviços por categoria.

    - **category**: Categoria (ex: cabelo, unhas, maquiagem, estetica, tratamentos)
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("category", "services")
            .eq("is_active", True)
            .execute()
        )

        services = []
        for item in result.data:
            service_data = item["data"]
            service_category = service_data.get("category", "")

            # Verificar se categoria bate
            if category.lower() in service_category.lower():
                service_data["id"] = item["id"]
                service_data["key"] = item["key"]
                services.append(service_data)

        return {
            "category": category,
            "services": services,
            "total": len(services),
            "success": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/promo/promocao-semana")
async def get_promo_services():
    """
    Busca serviços com promoção de segunda a quarta.
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("category", "services")
            .eq("is_active", True)
            .execute()
        )

        promo_services = []
        for item in result.data:
            service_data = item["data"]

            # Verificar se tem promoção seg-qua
            if "promo_price_seg_qua" in service_data:
                service_data["id"] = item["id"]
                service_data["key"] = item["key"]
                promo_services.append(service_data)

        return {
            "promotion": "Segunda a Quarta",
            "services": promo_services,
            "total": len(promo_services),
            "success": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
