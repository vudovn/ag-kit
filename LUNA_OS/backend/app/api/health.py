from fastapi import APIRouter
from app.integrations.supabase_client import get_supabase
from app.config import settings
import httpx
import time
from loguru import logger

router = APIRouter()


@router.get("/status")
async def get_health_status():
    """Perform active health checks for all core integrations"""

    status = {
        "supabase": {"status": "disconnected", "latency": 0, "details": None},
        "openrouter": {"status": "disconnected", "details": None},
        "evolution": {"status": "disconnected", "details": None},
        "system": {"status": "unknown", "details": None},
        "overall": "healthy",
    }

    # 1. Supabase Check
    try:
        start_time = time.time()
        db = get_supabase()

        # Pass 8 Shadow: Read + Write Integrity Check (Adversarial)
        # 1.1 Read Check
        resp = db.table("knowledge_base").select("id", count="exact").limit(1).execute()
        count = resp.count if hasattr(resp, "count") else 0

        # 1.2 Write Check (Pulse Test)
        # Tentamos escrever um pequeno log de batimento cardíaco para garantir permissões de escrita
        try:
            db.table("health_logs").insert(
                {
                    "service": "luna-core",
                    "status": "online",
                    "details": "100x shadow check",
                }
            ).execute()
            write_status = "OK"
        except Exception as e:
            # [DEBT #A1] Log erro específico ao invés de except genérico
            logger.warning(f"Health check: Tabela health_logs não existe ou sem permissão de escrita: {e}")
            write_status = "Table Missing/Read Only"

        status["supabase"]["status"] = "connected" if count > 0 else "warning"
        status["supabase"]["latency"] = round((time.time() - start_time) * 1000, 2)

        if count == 0:
            status["supabase"]["details"] = "Conectado. Cérebro VAZIO"
            status["overall"] = "attention"
        else:
            status["supabase"]["details"] = f"Integridade: R/W ({write_status})"

    except Exception as e:
        # [DEBT #A1] Log erro específico
        logger.error(f"Health check Supabase falhou: {e}")
        status["supabase"]["details"] = f"Erro Infra: {str(e)}"
        status["overall"] = "unhealthy"

    # 2. OpenRouter Check
    if not settings.openrouter_key:
        status["openrouter"]["status"] = "not_configured"
        status["overall"] = "attention"
    else:
        try:
            # Pass 6 Shadow: Add Sovereign Headers (X-Title & Referer)
            headers = {
                "Authorization": f"Bearer {settings.openrouter_key}",
                "X-Title": "LUNA OS - Sovereign Edition",
                "HTTP-Referer": "https://mct.tech",
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://openrouter.ai/api/v1/models", headers=headers
                )
                if resp.status_code == 200:
                    models_data = resp.json().get("data", [])
                    available_models = [m.get("id") for m in models_data]

                    if settings.model_quick in available_models:
                        status["openrouter"]["status"] = "connected"
                        status["openrouter"][
                            "details"
                        ] = f"MCT Core: {settings.model_quick}"
                    else:
                        status["openrouter"]["status"] = "warning"
                        status["openrouter"][
                            "details"
                        ] = f"Modelo {settings.model_quick} não listado (Shadow Gap)"
                else:
                    status["openrouter"]["status"] = "error"
                    status["openrouter"][
                        "details"
                    ] = f"OpenRouter API {resp.status_code}"
                    status["overall"] = "unhealthy"
        except Exception as e:
            # [DEBT #A1] Log erro específico
            logger.error(f"Health check OpenRouter falhou: {e}")
            status["openrouter"]["details"] = f"Network/Auth Error: {str(e)}"
            status["overall"] = "unhealthy"

    # 3. Evolution API Check
    if not settings.evolution_url or not settings.evolution_instance:
        status["evolution"]["status"] = "not_configured"
        status["overall"] = "attention"
    else:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                headers = {"apikey": settings.evolution_key}

                # Check instance status
                resp = await client.get(
                    f"{settings.evolution_url}/instance/connectionState/{settings.evolution_instance}",
                    headers=headers,
                )
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        instance_status = data.get("instance", {}).get("state")
                        status["evolution"]["status"] = (
                            "connected" if instance_status == "open" else "warning"
                        )
                        status["evolution"]["details"] = f"Estado: {instance_status}"
                    except Exception as e:
                        # [DEBT #A1] Log erro específico
                        logger.error(f"Health check Evolution: erro ao parsear resposta: {e}")
                        status["evolution"]["status"] = "error"
                        status["evolution"][
                            "details"
                        ] = "Erro de Parsing (Resposta Inválida)"

                    # Pass 7 Shadow: Get Engine Version for Sovereignty Verification
                    try:
                        v_resp = await client.get(
                            f"{settings.evolution_url}/instance/fetchInstances",
                            headers=headers,
                        )
                        if v_resp.status_code == 200:
                            # Finding our instance in the list to get version if possible, or just checking general health
                            status["evolution"]["details"] += " | API Online"
                    except Exception as e:
                        logger.debug(f"Health check Evolution: versão não disponível: {e}")

                    # Pass 4 Amplifier: Validate Webhook
                    hw_resp = await client.get(
                        f"{settings.evolution_url}/webhook/find/{settings.evolution_instance}",
                        headers=headers,
                    )
                    if hw_resp.status_code == 200:
                        wh_data = hw_resp.json()
                        if not wh_data:
                            status["evolution"]["status"] = "warning"
                            status["evolution"]["details"] += " | ⚠️ SEM WEBHOOK"
                else:
                    status["evolution"]["status"] = "error"
                    status["evolution"][
                        "details"
                    ] = f"Evolution Offline ({resp.status_code})"
                    status["overall"] = "unhealthy"
        except Exception as e:
            # [DEBT #A1] Log erro específico
            logger.error(f"Health check Evolution API falhou: {e}")
            status["evolution"]["details"] = f"Connection Fail: {str(e)}"
            status["overall"] = "unhealthy"

    # 4. System/Storage Check (Pass 4 Expert Amplifier)
    try:
        import shutil

        total, used, free = shutil.disk_usage("/")
        disk_percent = (used / total) * 100
        status["system"] = {
            "status": "connected" if disk_percent < 90 else "warning",
            "details": f"Disco: {disk_percent:.1f}% em uso",
        }
        if disk_percent > 95:
            status["overall"] = "attention"
    except Exception as e:
        # [DEBT #A1] Log erro específico
        logger.warning(f"Health check: falha ao ler métricas de disco: {e}")
        status["system"] = {
            "status": "warning",
            "details": "Falha ao ler métricas de disco",
        }

    status["last_check"] = time.strftime("%H:%M:%S")
    return status
