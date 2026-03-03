"""
👩‍🦱 Professionals API

Endpoints para gestão de profissionais.

Endpoints:
- GET /api/professionals → Listar todos
- GET /api/professionals/{id} → Buscar um
- GET /api/professionals/{id}/schedule → Buscar agenda

Autor: Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/professionals", tags=["Professionals"])


@router.get("")
async def list_professionals(active_only: bool = True):
    """
    Lista todos os profissionais.

    - **active_only**: Se True, retorna apenas ativos (padrão: True)
    """
    try:
        supabase = get_supabase()

        query = (
            supabase.table("knowledge_base").select("*").eq("category", "professionals")
        )

        if active_only:
            query = query.eq("is_active", True)

        result = query.execute()

        professionals = []
        for item in result.data:
            prof_data = item["data"]
            prof_data["id"] = item["id"]
            prof_data["key"] = item["key"]
            professionals.append(prof_data)

        return {
            "professionals": professionals,
            "total": len(professionals),
            "success": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{professional_id}")
async def get_professional(professional_id: str):
    """
    Busca profissional por ID.

    - **professional_id**: ID do profissional (ex: yujaira, carla, etc)
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("key", f"professional_{professional_id}")
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Professional not found")

        prof_data = result.data[0]["data"]
        prof_data["id"] = result.data[0]["id"]
        prof_data["key"] = result.data[0]["key"]

        return {"professional": prof_data, "success": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{professional_id}/schedule")
async def get_professional_schedule(professional_id: str):
    """
    Busca agenda/semana do profissional.

    - **professional_id**: ID do profissional
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("key", f"professional_{professional_id}")
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Professional not found")

        prof_data = result.data[0]["data"]
        schedule = prof_data.get("schedule", {})

        return {
            "professional_id": professional_id,
            "schedule": schedule,
            "success": True,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/specialty/{specialty}")
async def get_professionals_by_specialty(specialty: str):
    """
    Busca profissionais por especialidade.

    - **specialty**: Especialidade (ex: cabelo, unhas, estetica)
    """
    try:
        supabase = get_supabase()

        result = (
            supabase.table("knowledge_base")
            .select("*")
            .eq("category", "professionals")
            .eq("is_active", True)
            .execute()
        )

        professionals = []
        for item in result.data:
            prof_data = item["data"]
            specialties = prof_data.get("specialties", [])

            # Verificar se especialidade bate
            if any(specialty.lower() in s.lower() for s in specialties):
                prof_data["id"] = item["id"]
                prof_data["key"] = item["key"]
                professionals.append(prof_data)

        return {
            "specialty": specialty,
            "professionals": professionals,
            "total": len(professionals),
            "success": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
