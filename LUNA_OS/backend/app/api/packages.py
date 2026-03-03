"""
📦 Packages API

Endpoints para gestão de pacotes.

Endpoints:
- GET /api/packages → Listar todos
- GET /api/packages/{id} → Buscar um

Autor: Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/packages", tags=["Packages"])


@router.get("")
async def list_packages(active_only: bool = True):
    """
    Lista todos os pacotes.

    - **active_only**: Se True, retorna apenas ativos (padrão: True)
    """
    try:
        supabase = get_supabase()

        query = supabase.table("knowledge_base").select("*").eq("category", "packages")

        if active_only:
            query = query.eq("is_active", True)

        result = query.execute()

        packages = []
        for item in result.data:
            package_data = item["data"]
            package_data["id"] = item["id"]
            package_data["key"] = item["key"]
            packages.append(package_data)

        return {"packages": packages, "total": len(packages), "success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{package_id}")
async def get_package(package_id: str):
    """
    Busca pacote por ID.

    - **package_id**: ID do pacote (ex: gel_3_maos, escova_4, etc)
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("key", f"package_{package_id}")
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Package not found")

        package_data = result.data[0]["data"]
        package_data["id"] = result.data[0]["id"]
        package_data["key"] = result.data[0]["key"]

        return {"package": package_data, "success": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
