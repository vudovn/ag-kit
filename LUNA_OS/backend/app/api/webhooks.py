"""
Webhooks API - Evolution WhatsApp
Padrão MCT: Configuração Dinâmica e Zero Estado Global

Arquitetura:
- Settings dinâmicos (lidos do DB/ENV em tempo real)
- Processamento assíncrono em background
- Camadas: Sanitização → Brain → Memory → Evolution → Response
"""

from datetime import datetime
from typing import Optional, Dict, Any
import json

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

from app.config import settings, get_dynamic_settings
from app.core.brain import process_message
from app.core.memory import MemoryManager
from app.core.resilience import sanitize_input
from app.core.evolution import EvolutionEngine
from app.integrations.evolution import evolution as evol_client
from app.core.rate_limit import limiter

# Routers
router = APIRouter()

# Singletons
memory = MemoryManager()
evolution = EvolutionEngine()


# ═══════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════


class WebhookPayload(BaseModel):
    """Payload do webhook da Evolution API"""

    event: str
    instance: str
    data: dict


class ModeResponse(BaseModel):
    """Resposta da API de modo"""

    mode: str
    responding: bool
    source: str = "settings"


class ModeChangeRequest(BaseModel):
    """Request para mudança de modo"""

    mode: str = Field(..., pattern="^(active|observe)$")


# ═══════════════════════════════════════════════
# MODE MANAGEMENT
# ═══════════════════════════════════════════════


@router.get("/mode", response_model=ModeResponse)
@limiter.limit("100/minute")
async def get_mode(request: Request):
    """
    Retorna o modo atual da Luna.
    Fonte: Settings dinâmicos (DB/ENV em tempo real)
    """
    dynamic_settings = get_dynamic_settings()
    luna_mode = dynamic_settings.luna_mode

    return ModeResponse(
        mode=luna_mode,
        responding=luna_mode == "active",
        source="dynamic_settings",
    )


@router.post("/mode", response_model=ModeResponse)
@limiter.limit("50/minute")
async def set_mode(request: Request, body: ModeChangeRequest):
    """
    Altera o modo em runtime (sem reiniciar).
    Persiste no banco para sincronização entre containers.
    """
    new_mode = body.mode.lower()

    try:
        # Persistir no banco (Supabase)
        from app.integrations.supabase_client import get_supabase

        supabase = get_supabase()

        # Atualizar system_settings
        result = (
            supabase.table("system_settings")
            .upsert(
                {
                    "key": "luna_mode",
                    "value": new_mode,
                    "updated_at": datetime.utcnow().isoformat(),
                }
            )
            .execute()
        )

        logger.info(
            f"🔄 Luna Mode alterado para: {new_mode.upper()} (DB: {result.data})"
        )

        return ModeResponse(
            mode=new_mode,
            responding=new_mode == "active",
            source="database",
        )

    except Exception as e:
        logger.error(f"❌ Erro ao persistir modo no banco: {e}")
        # Fallback: apenas retorna o modo (não quebra a API)
        return ModeResponse(
            mode=new_mode,
            responding=new_mode == "active",
            source="ephemeral",
        )


# ═══════════════════════════════════════════════
# WEBHOOK HANDLERS
# ═══════════════════════════════════════════════


@router.post("/evolution")
@limiter.limit("200/minute")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook receiver for Evolution API
    Processa mensagens recebidas e dispatch para processamento em background.
    """
    # [HARDENING] Validação HMAC de Payload (Proteção contra Man-In-The-Middle)
    import hmac
    import hashlib

    # Captura body real e cabeçalhos
    body_bytes = await request.body()
    # Evolution API default HMAC header
    signature = request.headers.get(
        "evolution-webhook-signature"
    ) or request.headers.get("evolution-signature")
    expected_secret = os.getenv("WEBHOOK_API_KEY", "")

    if not signature or not expected_secret:
        # Fallback para o modelo antigo de apikey se assinatura falhar
        # (Somente se explicitamente configurado ou HMAC não habilitado no Evolution ainda)
        api_key = request.headers.get("apikey")
        if api_key != expected_secret:
            logger.warning(
                f"🚨 UNAUTHORIZED Webhook attempt (No Signature/Invalid Key)! IP: {request.client.host}"
            )
            raise HTTPException(
                status_code=401, detail="Unauthorized: Invalid signature or apikey"
            )
    else:
        # Computa o SHA256 do payload usando a API Key como secret
        expected_signature = hmac.new(
            expected_secret.encode("utf-8"), body_bytes, hashlib.sha256
        ).hexdigest()

        # Faz uma comparação segura contra Time-Based Attacks
        if not hmac.compare_digest(expected_signature, signature):
            logger.warning(
                f"🚨 UNAUTHORIZED Webhook attack blocked (HMAC Mismatch)! IP: {request.client.host}"
            )
            raise HTTPException(
                status_code=401, detail="Unauthorized: HMAC Signature Mismatch"
            )

    try:
        body = await request.json()
        event = body.get("event", "")
        instance = body.get("instance", "")
        data = body.get("data", {})

        logger.debug(f"📩 Webhook received: {event} from {instance}")

        # Process only incoming messages
        if event == "messages.upsert":
            message_data = data.get("message", {})
            key = data.get("key", {})

            # Skip outgoing messages
            if key.get("fromMe", False):
                logger.debug(
                    f"⏭️ Ignoring outgoing message to {key.get('remoteJid', '')}"
                )
                return {"status": "ignored", "reason": "outgoing message"}

            # Extract info
            remote_jid = key.get("remoteJid", "")
            push_name = data.get("pushName", "")

            # Get message content
            text = _extract_message_text(message_data)

            if text and remote_jid:
                # Sanitização — Blindagem Sōra
                text = sanitize_input(text)
                if not text:
                    logger.warning(f"⚠️ Message ignored: empty after sanitization")
                    return {"status": "ignored", "reason": "empty after sanitization"}

                # Dispatch para processamento em background
                background_tasks.add_task(
                    handle_message,
                    instance,
                    remote_jid,
                    push_name,
                    text,
                )

                # Retorna modo atual para debug
                dynamic_settings = get_dynamic_settings()
                return {
                    "status": "processing",
                    "mode": dynamic_settings.luna_mode,
                }

        return {"status": "ok"}

    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.exception(f"❌ Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _extract_message_text(message_data: Dict) -> Optional[str]:
    """Extrai texto de diferentes formatos de mensagem"""
    if "conversation" in message_data:
        return message_data["conversation"]
    elif "extendedTextMessage" in message_data:
        return message_data["extendedTextMessage"].get("text", "")
    elif "dialogue" in message_data:
        return message_data["dialogue"]
    return None


# ═══════════════════════════════════════════════
# MESSAGE PROCESSING PIPELINE
# ═══════════════════════════════════════════════


async def handle_message(
    instance_name: str,
    phone: str,
    name: str,
    message: str,
):
    """
    Pipeline de processamento de mensagens.
    Respeita o modo LUNA (active/observe) em tempo real.
    """
    start_time = datetime.utcnow()
    logger.info(f"💬 Processing: {name} ({phone}): {message[:50]}...")

    try:
        # 1. Ler modo dinâmico (sempre fresco do DB/ENV)
        dynamic_settings = get_dynamic_settings()
        luna_mode = dynamic_settings.luna_mode

        mode_label = "🔇 OBSERVE" if luna_mode == "observe" else "🟢 ACTIVE"
        logger.info(f"💬 [{mode_label}] {name} ({phone}): {message[:50]}...")

        # 2. Obter contexto da conversa
        conversation = await memory.get_conversation_context(phone)

        # 3. Processar com brain (sempre roda para log/BI)
        result = await brain.process_message(
            phone=phone,
            name=name,
            message=message,
            history=conversation.get("history", []),
        )

        intent = result.get("intent")
        response_text = result.get("response")

        # 4. 🌙 CAMADA 6: EVOLUÇÃO (Auditoria de Alma)
        audit_data = await evolution.audit_response(intent, response_text, phone)

        # 5. 💎 CAMADA CEO: INTELIGÊNCIA ESTRATÉGICA
        intelligence_data = result.get("intelligence", {})
        await memory.save_business_intelligence(
            phone=phone,
            conversation_id=conversation.get("id") if conversation else None,
            bi_data=intelligence_data,
        )
        logger.info(
            f"💎 BI stored: mood={intelligence_data.get('customer_mood')} | "
            f"urgency={intelligence_data.get('urgency_level')}"
        )

        # 6. Registrar aprendizado
        await evolution.log_evolution(
            phone=phone,
            intent=intent,
            response=response_text,
            audit_data=audit_data,
            conversation_id=conversation.get("id") if conversation else None,
        )

        # 7. Enviar resposta (condicional ao modo)
        if luna_mode == "active":
            await _send_response_and_actions(instance_name, phone, result)
        else:
            # OBSERVE mode: log but don't send
            logger.warning(
                f"🌙 MODE: observe. Response audited but NOT sent to {phone}"
            )
            logger.debug(f"Audit Result: {audit_data}")
            response_preview = (response_text or "")[:80]
            logger.info(f'👁️ [OBSERVE] Luna would respond: "{response_preview}..."')
            logger.info(f"    Intent: {intent} | Model: {result.get('model')}")

        # 8. Update memory (sempre salva, independente do modo)
        await memory.save_message(
            phone=phone,
            direction="inbound",
            content=message,
            intent=intent,
            sentiment=result.get("sentiment"),
        )

        if luna_mode == "active" and response_text:
            await memory.save_message(
                phone=phone,
                direction="outbound",
                content=response_text,
                model_used=result.get("model"),
                confidence_score=(
                    result.get("intelligence", {})
                    .get("metadata", {})
                    .get("confidence_score")
                    if isinstance(result.get("intelligence"), dict)
                    else None
                ),
                guardrail_passed=(
                    result.get("intelligence", {})
                    .get("metadata", {})
                    .get("guardrail_passed")
                    if isinstance(result.get("intelligence"), dict)
                    else None
                ),
            )

        # 9. Log de performance
        elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
        logger.info(f"✅ Message processed in {elapsed:.0f}ms for {name}")

    except Exception as e:
        logger.exception(f"❌ Message handling error: {e}")
        await _handle_processing_error(instance_name, phone, luna_mode)


async def _send_response_and_actions(instance_name: str, phone: str, result: Dict):
    """Envia resposta e executa ações especiais"""
    response_text = result.get("response")

    # Enviar resposta textual
    if response_text:
        await evol_client.send_text(instance_name, phone, response_text)
        logger.info(f"🚀 Response sent to {phone}")

    # Ações especiais
    action = result.get("action")
    if action == "send_location":
        logger.info(f"📍 Sending location to {phone}")
        await evol_client.send_location(
            instance_name,
            phone,
            lat=-27.0922,
            lng=-52.6158,
            name="Haven Escovaria & Esmalteria",
            address="Rua Mato Grosso, 837E - Jardim Itália, Chapecó - SC",
        )
    elif action == "handoff":
        logger.warning(f"🤝 HANDOFF requested by {phone}")
        await memory.mark_handoff(phone)


async def _handle_processing_error(
    instance_name: str,
    phone: str,
    luna_mode: str,
):
    """Tratamento de erro no processamento"""
    if luna_mode == "active":
        try:
            await evol_client.send_text(
                instance_name,
                phone,
                "Oi! Tive um probleminha técnico. Pode repetir sua mensagem? 😊",
            )
        except Exception as send_err:
            logger.error(f"❌ Failed to send error message: {send_err}")


# Import brain no final para evitar circular dependency
from app.core.brain import BrainEngine

brain = BrainEngine()
