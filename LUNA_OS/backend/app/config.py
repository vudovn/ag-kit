"""
LUNA CORE - Configuration
Padrão MCT: Settings estáticos (ENV) + Dinâmicos (DB)
"""

import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings
from loguru import logger

load_dotenv()


class Settings(BaseSettings):
    """
    Settings estáticos (carregados de ENV/.env)
    Para settings que mudam em runtime, usar get_dynamic_settings()
    """

    # App
    app_name: str = "Luna Core"
    app_version: str = "3.0.0"
    debug: bool = os.getenv("APP_DEBUG", "false").lower() == "true"
    luna_mode: str = os.getenv("LUNA_MODE", "active").lower()

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # Evolution API
    evolution_url: str = os.getenv("EVOLUTION_API_URL", "http://localhost:8081")
    evolution_key: str = os.getenv("EVOLUTION_API_KEY", "")
    evolution_instance: str = os.getenv("EVOLUTION_INSTANCE", "haven")

    # Anthropic
    anthropic_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # OpenRouter
    openrouter_key: str = os.getenv("OPENROUTER_API_KEY", "")

    # Belasis
    belasis_url: str = os.getenv("BELASIS_API_URL", "https://api.belasis.com.br")
    belasis_key: str = os.getenv("BELASIS_API_KEY", "")
    belasis_mock: bool = os.getenv("BELASIS_MOCK", "true").lower() == "true"

    # Models
    model_quick: str = "google/gemini-2.0-flash-001"
    model_standard: str = "anthropic/claude-3.5-haiku"
    model_complex: str = "anthropic/claude-3.5-sonnet"

    # Webhook Security
    webhook_api_key: str = os.getenv("WEBHOOK_API_KEY", "")

    # v3.0 Stack
    redis_v3_url: str = os.getenv("REDIS_URL", "redis://luna-redis:6379/0")
    milvus_host: str = os.getenv("MILVUS_HOST", "luna-milvus")
    milvus_port: int = int(os.getenv("MILVUS_PORT", "19530"))
    jaeger_host: str = os.getenv("JAEGER_AGENT_HOST", "luna-jaeger")
    jaeger_port: int = int(os.getenv("JAEGER_AGENT_PORT", "6831"))
    ntfy_topic: str = os.getenv("NTFY_TOPIC", "luna-alerts")
    windmill_host: str = os.getenv("WINDMILL_HOST", "luna-windmill")
    windmill_token: str = os.getenv("WINDMILL_TOKEN", "")

    # Computed properties
    @property
    def use_openrouter(self) -> bool:
        """Check if OpenRouter is configured"""
        return bool(self.openrouter_key)

    # [KIMI-P4] Validação de fields críticos na startup
    # Padrão SWE-Bench: fail fast em produção, warning em desenvolvimento
    @model_validator(mode="after")
    def validate_critical_keys(self):
        warnings = []
        is_production = os.getenv("ENV", "development").lower() == "production"

        # OpenRouter
        if not self.openrouter_key:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: OPENROUTER_API_KEY não configurada. "
                    "Defina no .env antes de iniciar em PRODUÇÃO."
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] OPENROUTER_API_KEY não configurada — fallback local ativado"
                )

        # Supabase
        if not self.supabase_url or not self.supabase_key:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: SUPABASE_URL ou SUPABASE_KEY não configurados. "
                    "Defina no .env antes de iniciar em PRODUÇÃO."
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] Supabase não configurado — memória desabilitada"
                )

        # Webhook Security
        if not self.webhook_api_key:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: WEBHOOK_API_KEY não configurada. "
                    "Defina no .env antes de iniciar em PRODUÇÃO."
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] WEBHOOK_API_KEY não configurada — webhooks sem autenticação"
                )

        # Log warnings (dev) ou errors (production)
        for w in warnings:
            if is_production:
                logger.error(w)
            else:
                logger.warning(w)

        if is_production and warnings:
            logger.error("🚨 Produção iniciada com warnings. Revise configuração!")

        return self

    class Config:
        env_file = ".env"
        extra = "allow"
        protected_namespaces = ()  # Permite campos começando com model_


class DynamicSettings:
    """
    Settings dinâmicos (lidos do DB em tempo real)
    Usado para configurações que podem mudar em runtime sem restart.
    """

    def __init__(self):
        self._cache: Optional[dict] = None
        self._cache_time: Optional[datetime] = None
        self._cache_ttl_seconds = 5  # Cache por 5 segundos

    def _get_from_db(self) -> dict:
        """Lê settings do banco de dados"""
        try:
            from app.integrations.supabase_client import get_supabase

            supabase = get_supabase()

            result = supabase.table("system_settings").select("*").execute()
            settings_dict = {}

            for row in result.data or []:
                key = row.get("key")
                value = row.get("value")
                if key and value is not None:
                    settings_dict[key] = value

            return settings_dict
        except Exception as e:
            logger.debug(f"⚠️ Could not read dynamic settings from DB: {e}")
            return {}

    def _is_cache_valid(self) -> bool:
        """Verifica se cache ainda é válido"""
        if self._cache_time is None:
            return False
        elapsed = (datetime.utcnow() - self._cache_time).total_seconds()
        return elapsed < self._cache_ttl_seconds

    def refresh(self) -> "DynamicSettings":
        """Força refresh dos settings do DB"""
        self._cache = self._get_from_db()
        self._cache_time = datetime.utcnow()
        logger.debug(f"🔄 Dynamic settings refreshed: {self._cache}")
        return self

    @property
    def luna_mode(self) -> str:
        """
        Lê modo LUNA (DB > ENV > default)
        Prioridade: 1) DB, 2) ENV, 3) default 'active'
        """
        # Tenta cache primeiro
        if not self._is_cache_valid():
            self._cache = self._get_from_db()
            self._cache_time = datetime.utcnow()

        # DB tem prioridade
        if self._cache and "luna_mode" in self._cache:
            mode = self._cache["luna_mode"].lower()
            if mode in ("active", "observe"):
                return mode

        # Fallback para ENV
        env_mode = os.getenv("LUNA_MODE", "active").lower()
        if env_mode in ("active", "observe"):
            return env_mode

        return "active"

    @property
    def debug(self) -> bool:
        """Debug mode (DB > ENV > default)"""
        if not self._is_cache_valid():
            self._cache = self._get_from_db()
            self._cache_time = datetime.utcnow()

        if self._cache and "debug" in self._cache:
            val = str(self._cache["debug"]).lower()
            return val in ("true", "1", "yes")

        return os.getenv("APP_DEBUG", "false").lower() == "true"


# Singleton global
_dynamic_settings: Optional[DynamicSettings] = None


def get_dynamic_settings() -> DynamicSettings:
    """
    Factory para DynamicSettings (singleton)
    Uso: settings = get_dynamic_settings()
    """
    global _dynamic_settings
    if _dynamic_settings is None:
        _dynamic_settings = DynamicSettings()
    return _dynamic_settings


def refresh_dynamic_settings() -> DynamicSettings:
    """
    Força refresh imediato dos settings dinâmicos
    Uso: Quando o usuário altera configurações via UI
    """
    settings = get_dynamic_settings()
    return settings.refresh()


# Settings estáticos (backward compatibility)
settings = Settings()
