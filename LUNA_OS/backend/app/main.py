import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

from app.config import settings
from app.api import (
    webhooks,
    conversations,
    clients,
    analytics_super,
    campaigns,
    knowledge,
    settings as settings_api,
    health,
    dojo,
    professionals,
    services,
    packages,
    campaigns_new,
    sovereign_switch,
    webhook_sync,
    learning_continuous,
)
from app.api.evolution_proxy import router as evolution_proxy
from app.api.brain import router as brain_router
from app.api.dojo_simulator import router as dojo_simulator_router
from app.api.dojo_learning import router as dojo_learning_router
from app.modules_v3.conversation_intelligence.api import router as ci_router
from app.api.intelligence import router as intelligence_router
from app.integrations.supabase_client import init_supabase

# v3.0 Stack Imports
from app.integrations.queue_manager import queue_manager
from app.integrations.vector_db_manager import vector_db_manager
from app.integrations.tracing_setup import setup_tracing
from app.integrations.alert_system import alert_system, AlertSeverity

# Configure Loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
logger.add("logs/luna_core.log", rotation="10 MB", retention="10 days", level="INFO")


# Rate Limiter - Usando instância centralizada


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🌙 Luna Core v2.1 starting...")
    await init_supabase()
    logger.info("✅ Supabase connected")
    logger.info("✅ Evolution Proxy enabled")

    # Start Task Runner scheduler (background tasks)
    from app.core.task_runner import start_scheduler

    start_scheduler()
    logger.info("✅ Task Runner scheduler started")

    # [v3.0] Initialize Distributed Tracing
    setup_tracing("luna-core")
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    FastAPIInstrumentor.instrument_app(app)
    logger.info("✅ Distributed Tracing (Jaeger) initialized")

    # [v3.0] Initialize Vector DB
    try:
        vector_db_manager.connect()
        logger.info("✅ Vector DB (Milvus) connected")
    except Exception as e:
        logger.warning(f"⚠️ Vector DB connection failed: {e}")

    # [v3.0] Alert System Startup
    alert_system.send_alert(
        title="LUNA OS v3.0 ONLINE",
        message="LUNA OS v3.0 has started with full Intelligence Stack.",
        severity=AlertSeverity.LOW,
        tags=["startup", "online"],
    )

    logger.info("✅ Luna Core v3.0 ready on port 8000")
    yield
    logger.info("🌙 Luna Core shutting down...")


app = FastAPI(
    title="Luna Core",
    description="Sistema de Atendimento IA para Haven Escovaria & Esmalteria",
    version="3.0.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

# [v3.0] Instrument Application (Global Scope)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

FastAPIInstrumentor.instrument_app(app)

# Rate Limiter app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Middleware de Latência e Log de Requisição
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Log da requisição soberana
    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s"
    )

    return response


# CORS - Configuração Soberana
# Em produção, restringir para domínios específicos via ALLOWED_ORIGINS env var
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
)

# Routes
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(
    conversations.router, prefix="/api/conversations", tags=["Conversations"]
)
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(
    analytics_super.router, prefix="/api/analytics", tags=["Super Analytics"]
)
# app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["Settings"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(brain_router, prefix="/api/brain", tags=["Brain"])
app.include_router(evolution_proxy)  # Evolution API Proxy
app.include_router(dojo.router)  # Dojo Arena
app.include_router(dojo_simulator_router)  # 🥋 Dojo Simulator (Ollama)
app.include_router(dojo_learning_router)  # 🎓 Dojo Learning Cycle
app.include_router(ci_router)  # 🧠 Conversation Intelligence
app.include_router(intelligence_router)  # 🧠 Intelligence Endpoints
app.include_router(professionals.router)  # 👩‍🦱 Professionals API
app.include_router(services.router)  # ✂️ Services API
app.include_router(packages.router)  # 📦 Packages API
app.include_router(campaigns_new.router)  # 🎯 Marketing Campaigns
app.include_router(sovereign_switch.router)  # ⚡ Sovereign Switch
app.include_router(webhook_sync.router)  # 🔄 Webhook Sync
app.include_router(learning_continuous.router)  # 🧠 Learning Contínuo


@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):
    return {
        "name": "Luna Core",
        "version": "3.0.0",  # v3.0 Stack: Queues, VectorDB, Tracing, ML Engine
        "status": "operational",
        "modules": [
            "brain",  # 🧠 Cérebro com anti-alucinação
            "memory",  # 💾 Memória
            "analytics",  # 📊 Analytics
            "campaigns",  # 🎯 Campanhas
            "knowledge",  # 📚 Conhecimento
            "evolution",  # 🔄 Evolution API
            "evolution_proxy",  # 🔌 Proxy
            "dojo",  # 🥋 Dojo Arena
            "dojo_simulator",  # 🎮 Simulator
            "dojo_learning",  # 📖 Learning
            "conversation_intelligence",  # 🧠 Intelligence
            "task_runner",  # ⏰ Task Runner
            "sovereign_switch",  # ⚡ Sovereign Switch
            "webhook_sync",  # 🔄 Webhook Sync
            "learning_continuous",  # 🧠 Learning Contínuo
        ],
        "features": {
            "anti_hallucination": True,  # ✅ Sistema anti-alucinação ativo
            "continuous_learning": True,  # ✅ Aprendizado contínuo ativo
            "validation_system": True,  # ✅ Validação pré-resposta ativa
        },
    }


@app.get("/health")
@limiter.limit("60/minute")
async def health_ping(request: Request):
    """Diagnóstico Soberano — Verifica a saúde de todas as integrações"""
    from app.integrations.supabase_client import get_supabase
    from app.integrations.evolution import evolution

    health_report = {
        "status": "healthy",
        "version": "2.0.0",
        "integrations": {"supabase": "unknown", "evolution_api": "unknown"},
    }

    # 1. Testar Supabase
    try:
        db = get_supabase()
        db.table("clients").select("count", count="exact").limit(1).execute()
        health_report["integrations"]["supabase"] = "connected"
    except Exception as e:
        health_report["integrations"]["supabase"] = f"error: {str(e)}"
        health_report["status"] = "degraded"

    # 2. Testar Evolution API
    try:
        status = await evolution.get_instance_status()
        health_report["integrations"]["evolution_api"] = "connected"
    except Exception as e:
        health_report["integrations"]["evolution_api"] = f"error: {str(e)}"
        health_report["status"] = "degraded"

    # 3. [v3.0] Testar Milvus
    try:
        from pymilvus import connections

        if connections.has_connection("default"):
            health_report["integrations"]["milvus"] = "connected"
        else:
            health_report["integrations"]["milvus"] = "disconnected"
    except Exception:
        health_report["integrations"]["milvus"] = "error"

    # 4. [v3.0] Testar Redis v3 (Queue)
    try:
        if queue_manager.redis_conn.ping():
            health_report["integrations"]["redis_v3"] = "connected"
    except Exception:
        health_report["integrations"]["redis_v3"] = "error"

    return health_report


# Global Error Handler for Sovereign Consistency
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from fastapi.responses import JSONResponse

    logger.error(f"🚨 Sovereign Error Captured in {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "LUNA Core interceptou um erro crítico.",
            "details": str(exc),
            "sovereignty_code": "MCT-500",
        },
    )
