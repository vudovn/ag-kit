"""
LUNA CORE - Configuration
Padrão MCT: Settings estáticos (ENV) + Dinâmicos (DB)

DEBT #M3: Type hints completos
DEBT #M4: Docstrings em todas funções públicas
"""

import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings
from loguru import logger

load_dotenv()


class Settings(BaseSettings):
    """
    Settings estáticos (carregados de ENV/.env).

    Para settings que mudam em runtime, usar get_dynamic_settings().

    Attributes:
        app_name: Nome da aplicação
        app_version: Versão da aplicação
        debug: Modo debug ativo
        luna_mode: Modo LUNA (active/observe)
        supabase_url: URL do Supabase
        supabase_key: Chave de API do Supabase
        evolution_url: URL da Evolution API
        evolution_key: Chave de API da Evolution
        evolution_instance: Instância da Evolution
        anthropic_key: Chave de API da Anthropic
        openrouter_key: Chave de API do OpenRouter
        belasis_url: URL do Belasis ERP
        belasis_key: Chave de API do Belasis
        belasis_mock: Modo mock do Belasis
        model_quick: Modelo IA para respostas rápidas
        model_standard: Modelo IA para respostas padrão
        model_complex: Modelo IA para respostas complexas
        webhook_api_key: Chave de segurança para webhooks
        redis_v3_url: URL do Redis v3
        milvus_host: Host do Milvus
        milvus_port: Porta do Milvus
        jaeger_host: Host do Jaeger
        jaeger_port: Porta do Jaeger
        ntfy_topic: Tópico do Ntfy
        windmill_host: Host do Windmill
        windmill_token: Token do Windmill
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

    # [DEBT #12] Cache TTL configurável via ENV
    @property
    def settings_cache_ttl(self) -> int:
        """Dynamic settings cache TTL in seconds (default: 5)"""
        return int(os.getenv("SETTINGS_CACHE_TTL", "5"))

    # [KIMI-P4] Validação de fields críticos na startup
    # Padrão SWE-Bench: fail fast em produção, warning em desenvolvimento
    # [DEBT #C2] Adicionada validação para stack v3.0
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

        # [DEBT #C2] Validação de variáveis críticas da stack v3.0
        # Redis v3 (Queue Manager)
        if not self.redis_v3_url or "redis://" not in self.redis_v3_url:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: REDIS_URL não configurada ou inválida. "
                    "Exemplo: redis://luna-redis:6379/0"
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] REDIS_URL não configurada — filas desabilitadas"
                )

        # Milvus (Vector DB)
        if not self.milvus_host:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: MILVUS_HOST não configurado. "
                    "Exemplo: luna-milvus"
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] MILVUS_HOST não configurado — Vector DB desabilitada"
                )

        # Jaeger (Distributed Tracing)
        if not self.jaeger_host:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: JAEGER_AGENT_HOST não configurado. "
                    "Exemplo: luna-jaeger"
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] JAEGER_AGENT_HOST não configurado — Tracing desabilitado"
                )

        # Ntfy (Alertas Push)
        if not self.ntfy_topic:
            if is_production:
                raise RuntimeError(
                    "🚨 STARTUP BLOQUEADA: NTFY_TOPIC não configurado. "
                    "Exemplo: luna-alerts"
                )
            else:
                warnings.append(
                    "⚠️ [DEV MODE] NTFY_TOPIC não configurado — alertas desabilitados"
                )

        # Windmill (Workflows) - Apenas warning (opcional)
        if not self.windmill_token:
            warnings.append(
                "⚠️ WINDMILL_TOKEN não configurado — workflows desabilitados"
            )

        # Validação de timeout (range aceitável: 5-300s)
        supabase_timeout = int(os.getenv("SUPABASE_TIMEOUT", "30"))
        if supabase_timeout < 5 or supabase_timeout > 300:
            warnings.append(
                f"⚠️ SUPABASE_TIMEOUT={supabase_timeout}s fora do range recomendado (5-300s)"
            )

        # Validação de cache TTL (range aceitável: 1-300s)
        cache_ttl = int(os.getenv("SETTINGS_CACHE_TTL", "5"))
        if cache_ttl < 1 or cache_ttl > 300:
            warnings.append(
                f"⚠️ SETTINGS_CACHE_TTL={cache_ttl}s fora do range recomendado (1-300s)"
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
    Settings dinâmicos (lidos do DB em tempo real).

    Usado para configurações que podem mudar em runtime sem restart.

    Attributes:
        _cache: Cache dos settings
        _cache_time: Timestamp do cache
        _cache_ttl_seconds: TTL do cache em segundos
    """

    def __init__(self) -> None:
        """Inicializa DynamicSettings com cache vazio."""
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[datetime] = None
        # [DEBT #12] TTL configurável via ENV (default: 5 segundos)
        self._cache_ttl_seconds: int = settings.settings_cache_ttl

    def _get_from_db(self) -> Dict[str, Any]:
        """
        Lê settings do banco de dados.

        Returns:
            Dicionário com settings do banco
        """
        try:
            from app.integrations.supabase_client import get_supabase

            supabase = get_supabase()

            if supabase is None:
                logger.debug("Supabase não disponível para dynamic settings")
                return {}

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
        """
        Verifica se cache ainda é válido.

        Returns:
            True se cache é válido, False caso contrário
        """
        if self._cache_time is None:
            return False
        elapsed = (datetime.utcnow() - self._cache_time).total_seconds()
        return elapsed < self._cache_ttl_seconds

    def refresh(self) -> "DynamicSettings":
        """
        Força refresh dos settings do DB.

        Returns:
            Instância atualizada de DynamicSettings
        """
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
        """
        Debug mode (DB > ENV > default).

        Returns:
            True se debug está ativo, False caso contrário
        """
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
    Factory para DynamicSettings (singleton).

    Returns:
        Instância singleton de DynamicSettings
    """
    global _dynamic_settings
    if _dynamic_settings is None:
        _dynamic_settings = DynamicSettings()
    return _dynamic_settings


def refresh_dynamic_settings() -> DynamicSettings:
    """
    Força refresh imediato dos settings dinâmicos.

    Returns:
        DynamicSettings com cache atualizado

    Uso: Quando o usuário altera configurações via UI
    """
    settings = get_dynamic_settings()
    return settings.refresh()


# Settings estáticos (backward compatibility)
settings = Settings()
