import os
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.config import settings, refresh_dynamic_settings
from app.integrations.supabase_client import get_supabase
from loguru import logger

router = APIRouter(prefix="/api/settings", tags=["Settings"])

# ═══════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════


class SovereignSwitchState(BaseModel):
    """Estado atual dos switches soberanos"""

    campaigns_enabled: bool = Field(
        default=True, description="Campanhas de marketing ativas"
    )
    upsell_enabled: bool = Field(default=True, description="Upsell automático ativo")
    luna_mode: str = Field(default="observe", description="Modo LUNA (active/observe)")
    belasis_mock: bool = Field(default=True, description="Belasis em modo mock")


class SovereignSwitchUpdate(BaseModel):
    """Atualização de switches soberanos"""

    campaigns_enabled: Optional[bool] = None
    upsell_enabled: Optional[bool] = None
    luna_mode: Optional[str] = Field(default=None, pattern="^(active|observe)$")
    belasis_mock: Optional[bool] = None


# ═══════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════


@router.get("/sovereign", response_model=SovereignSwitchState)
async def get_sovereign_state():
    """
    Retorna estado atual dos switches soberanos.
    Lê valores reais do config/settings.
    """
    return SovereignSwitchState(
        campaigns_enabled=getattr(settings, "campaigns_enabled", True),
        upsell_enabled=getattr(settings, "upsell_enabled", True),
        luna_mode=settings.luna_mode,
        belasis_mock=settings.belasis_mock,
    )


@router.post("/sovereign", response_model=SovereignSwitchState)
async def update_sovereign_state(update: SovereignSwitchUpdate):
    """
    Atualiza estado dos switches soberanos com persistência no .env e Supabase.
    """
    env_paths = [
        "/app/.env",  # Docker container
        os.path.join(os.path.dirname(__file__), "../../../.env"),  # Local dev
    ]

    updates_env = {}
    updates_db = []

    if update.luna_mode is not None:
        updates_env["LUNA_MODE"] = update.luna_mode.lower()
        updates_db.append(
            {
                "key": "luna_mode",
                "value": update.luna_mode.lower(),
                "updated_at": "now()",
            }
        )
        settings.luna_mode = update.luna_mode.lower()
        os.environ["LUNA_MODE"] = update.luna_mode.lower()

    if update.belasis_mock is not None:
        updates_env["BELASIS_MOCK"] = "true" if update.belasis_mock else "false"
        updates_db.append(
            {"key": "belasis_mock", "value": update.belasis_mock, "updated_at": "now()"}
        )
        settings.belasis_mock = update.belasis_mock
        os.environ["BELASIS_MOCK"] = "true" if update.belasis_mock else "false"

    # Persist to .env
    saved_count = 0
    for env_path in env_paths:
        env_path = os.path.abspath(env_path)
        try:
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    content = f.read()
            else:
                content = ""

            for key, val in updates_env.items():
                pattern = rf"^{key}=.*$"
                new_line = f"{key}={val}"
                if re.search(pattern, content, re.MULTILINE):
                    content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
                else:
                    content = content.rstrip("\n") + f"\n{new_line}\n"

            with open(env_path, "w") as f:
                f.write(content)
            saved_count += 1
        except Exception as e:
            logger.error(f"❌ Erro ao salvar .env em {env_path}: {e}")

    # Persist to Supabase
    try:
        if updates_db:
            db = get_supabase()
            db.table("system_settings").upsert(updates_db).execute()
            refresh_dynamic_settings()
            logger.info(
                f"✅ Sovereign Switch: {len(updates_db)} campos persistidos no Supabase"
            )
    except Exception as e:
        logger.warning(f"⚠️ Erro ao persistir no Supabase: {e}")

    return await get_sovereign_state()


@router.get("/sovereign/health")
async def get_sovereign_health():
    """Retorna saúde do sistema soberano."""
    return {
        "campaigns_api": "operational",
        "upsell_api": "operational",
        "luna_mode": settings.luna_mode,
        "belasis_mock": settings.belasis_mock,
        "overall": "healthy",
    }
