"""Settings API — returns real config, not hardcoded values"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings
import os
import re
import httpx

router = APIRouter()


class OrKeyBody(BaseModel):
    key: str


class ModelsBody(BaseModel):
    model_quick: str
    model_standard: str
    model_complex: str


class OperationModeBody(BaseModel):
    luna_mode: str
    belasis_mock: bool


@router.get("/openrouter-models")
async def get_openrouter_models():
    """Fetch available models from OpenRouter to populate the frontend select."""
    if not settings.openrouter_key:
        return {"data": []}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {settings.openrouter_key}"},
            )
            resp.raise_for_status()
            data = resp.json()
            return {"data": data.get("data", [])}
    except Exception as e:
        # [DEBT #M2] Substituir print() por logger
        from loguru import logger
        logger.error(f"Error fetching OpenRouter models: {e}")
        return {"data": []}


@router.post("/models")
async def save_models(body: ModelsBody):
    """Persist AI Models to the container .env file"""
    env_paths = [
        "/app/.env",  # Docker container
        os.path.join(os.path.dirname(__file__), "../../../.env"),  # Local dev
    ]

    saved_count = 0
    last_error = None

    updates = {
        "MODEL_QUICK": body.model_quick.strip(),
        "MODEL_STANDARD": body.model_standard.strip(),
        "MODEL_COMPLEX": body.model_complex.strip(),
        "LOGIC_MODEL_ID": body.model_quick.strip(),  # Set logic to quick for now as default sync
        "VOICE_MODEL_ID": body.model_standard.strip(),  # Set voice to standard for now as default sync
    }

    for env_path in env_paths:
        env_path = os.path.abspath(env_path)
        try:
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    content = f.read()
            else:
                content = ""

            for key, val in updates.items():
                if not val:
                    continue
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
            last_error = str(e)
            continue

    # Update in-memory config immediately
    for k, v in updates.items():
        if v:
            os.environ[k] = v
    if body.model_quick:
        settings.model_quick = body.model_quick
    if body.model_standard:
        settings.model_standard = body.model_standard
    if body.model_complex:
        settings.model_complex = body.model_complex
    if body.model_quick:
        settings.logic_model_id = body.model_quick
    if body.model_standard:
        settings.voice_model_id = body.model_standard

    if saved_count == 0:
        raise HTTPException(500, f"Falha ao salvar .env: {last_error}")

    return {
        "status": "saved",
        "message": f"Modelos salvos em {saved_count} local(is). Reinicie o container para persistência total.",
    }


@router.post("/openrouter-key")
async def save_openrouter_key(body: OrKeyBody):
    """Persist OPENROUTER_API_KEY to the container .env file"""
    key = body.key.strip()
    if not key or not key.startswith("sk-or"):
        raise HTTPException(400, "Chave inválida. Deve começar com 'sk-or'")

    # Docker-safe path: save to /app/.env (mounted volume)
    # Also save to backend root for local development
    env_paths = [
        "/app/.env",  # Docker container
        os.path.join(os.path.dirname(__file__), "../../../.env"),  # Local dev
    ]

    saved_count = 0
    last_error = None

    for env_path in env_paths:
        env_path = os.path.abspath(env_path)
        try:
            # Read current .env
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    content = f.read()
            else:
                content = ""

            # Replace or append OPENROUTER_API_KEY
            pattern = r"^OPENROUTER_API_KEY=.*$"
            new_line = f"OPENROUTER_API_KEY={key}"
            if re.search(pattern, content, re.MULTILINE):
                content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
            else:
                content = content.rstrip("\n") + f"\n{new_line}\n"

            with open(env_path, "w") as f:
                f.write(content)
            saved_count += 1
        except Exception as e:
            last_error = str(e)
            continue

    # Update in-memory config immediately
    os.environ["OPENROUTER_API_KEY"] = key
    settings.openrouter_key = key

    if saved_count == 0:
        raise HTTPException(500, f"Falha ao salvar .env: {last_error}")

    return {
        "status": "saved",
        "message": f"Chave salva em {saved_count} local(is). Reinicie o container para persistência total.",
        "paths_written": saved_count,
    }


@router.post("/operation-mode")
async def save_operation_mode(body: OperationModeBody):
    """Persist LUNA_MODE and BELASIS_MOCK to the container .env file"""
    env_paths = [
        "/app/.env",  # Docker container
        os.path.join(os.path.dirname(__file__), "../../../.env"),  # Local dev
    ]

    saved_count = 0
    last_error = None

    updates = {
        "LUNA_MODE": body.luna_mode.lower(),
        "BELASIS_MOCK": "true" if body.belasis_mock else "false",
    }

    for env_path in env_paths:
        env_path = os.path.abspath(env_path)
        try:
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    content = f.read()
            else:
                content = ""

            for key, val in updates.items():
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
            last_error = str(e)
            continue

    # Update in-memory config
    if body.luna_mode:
        settings.luna_mode = body.luna_mode.lower()
        os.environ["LUNA_MODE"] = body.luna_mode.lower()

    settings.belasis_mock = body.belasis_mock
    os.environ["BELASIS_MOCK"] = "true" if body.belasis_mock else "false"

    # Also try to persist to Supabase for dynamic settings (immediate effect)
    try:
        from app.integrations.supabase_client import get_supabase
        from app.config import refresh_dynamic_settings

        db = get_supabase()
        db.table("system_settings").upsert(
            [
                {
                    "key": "luna_mode",
                    "value": body.luna_mode.lower(),
                    "updated_at": "now()",
                },
                {
                    "key": "belasis_mock",
                    "value": body.belasis_mock,
                    "updated_at": "now()",
                },
            ]
        ).execute()
        refresh_dynamic_settings()
    except Exception as e:
        print(f"⚠️ Could not persist to Supabase, but .env was saved: {e}")

    if saved_count == 0:
        raise HTTPException(500, f"Falha ao salvar .env: {last_error}")

    return {
        "status": "saved",
        "message": f"Modo de operação salvo. Requer reinicialização do container para efeito total.",
    }


@router.get("")
@router.get("/")
async def get_settings():
    """Return current system configuration"""
    return {
        "bot": {
            "name": "Luna",
            "greeting": "Oi! Sou a Luna, sua assistente virtual da Haven 🌙",
            "fallback": "Desculpa, não entendi. Pode reformular?",
            "handoff_trigger": "falar com humano",
        },
        "ai": {
            "provider": "openrouter",
            "use_openrouter": settings.use_openrouter,
            "models": {
                "quick": {
                    "id": settings.model_quick,
                    "use": "Saudações, horário, localização (menor custo)",
                },
                "standard": {
                    "id": settings.model_standard,
                    "use": "Preços, serviços, agendamento (equilibrado)",
                },
                "complex": {
                    "id": settings.model_complex,
                    "use": "Reclamações, handoff, multi-serviço (máxima qualidade)",
                },
            },
        },
        "business": {
            "name": "Haven Escovaria & Esmalteria",
            "hours": "Segunda a Sábado, 8h às 20h",
            "address": "Rua Mato Grosso, 837E - Jardim Itália, Chapecó-SC",
        },
        "integrations": {
            "evolution_instance": settings.evolution_instance,
            "supabase_configured": bool(settings.supabase_url),
            "openrouter_configured": bool(settings.openrouter_key),
        },
        "mode": {
            "luna_mode": settings.luna_mode,
            "belasis_mock": settings.belasis_mock,
        },
    }


@router.put("")
@router.put("/")
async def update_settings(body: dict):
    """Update settings — persists to Supabase system_settings table"""
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()
    try:
        db.table("system_settings").upsert(
            {"key": "luna_config", "value": body, "updated_at": "now()"}
        ).execute()
        return {"status": "updated", "settings": body}
    except Exception as e:
        # Supabase table may not exist yet — return success anyway
        return {"status": "ok_no_persist", "detail": str(e), "settings": body}
