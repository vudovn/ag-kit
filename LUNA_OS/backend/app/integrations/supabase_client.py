"""
Supabase Client - Thread-Safe Singleton

DEBT #6: Workaround para incompatibilidade httpx/gotrue vs supabase-py.
O supabase-py usa 'proxy' mas httpx>=0.24 espera 'proxies'.
Este monkey patch é seguro e idempotente.
"""
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# WORKAROUND: Fix httpx/gotrue proxy argument mismatch
# Only apply patch if needed (check httpx version)
import httpx

# Check if patch is needed (httpx version >= 0.24 uses 'proxies' not 'proxy')
_httpx_version = tuple(int(x) for x in httpx.__version__.split('.')[:2])

if _httpx_version >= (0, 24):
    original_init = httpx.Client.__init__

    def new_init(self, *args, **kwargs):
        # Convert 'proxy' to 'proxies' for httpx>=0.24 compatibility
        if "proxy" in kwargs and "proxies" not in kwargs:
            kwargs["proxies"] = kwargs.pop("proxy")
            logger.debug("Applied httpx proxy compatibility patch")
        original_init(self, *args, **kwargs)

    httpx.Client.__init__ = new_init
    logger.info(f"Applied httpx.Client patch for version {httpx.__version__}")
else:
    logger.debug(f"httpx version {httpx.__version__} does not need proxy patch")

from supabase import create_client, Client
from app.config import settings

# Thread-safe singleton pattern
_supabase_lock = asyncio.Lock()
_supabase_client: Optional[Client] = None


async def init_supabase() -> Client:
    """
    Initialize Supabase client with thread-safety.
    Must be called during application startup.

    DEBT #16: Added timeout configuration for network resilience.
    """
    global _supabase_client

    async with _supabase_lock:
        if _supabase_client is not None:
            return _supabase_client

        from os import getenv

        url = getenv("SUPABASE_URL", settings.supabase_url).strip('"').strip("'")
        key = getenv("SUPABASE_KEY", settings.supabase_key).strip('"').strip("'")

        # [DEBT #16] Timeout configurável via ENV (default: 30s)
        timeout = int(getenv("SUPABASE_TIMEOUT", "30"))

        # FIX v2.0.3: Use options dict instead of ClientOptions class
        options = dict(
            postgrest_client_timeout=timeout,
            storage_client_timeout=timeout,
            realtime_client_timeout=timeout,
        )

        _supabase_client = create_client(url, key, options=options)
        return _supabase_client


def get_supabase() -> Optional[Client]:
    """
    Get Supabase client (synchronous, for use after initialization).
    Returns None if not initialized yet.
    """
    return _supabase_client


async def get_supabase_async() -> Client:
    """
    Get Supabase client with lazy initialization (thread-safe).
    Use this when init_supabase() wasn't called during startup.

    DEBT #16: Added timeout configuration.
    """
    global _supabase_client

    async with _supabase_lock:
        if _supabase_client is None:
            from os import getenv

            url = getenv("SUPABASE_URL", settings.supabase_url).strip('"').strip("'")
            key = getenv("SUPABASE_KEY", settings.supabase_key).strip('"').strip("'")

            # [DEBT #16] Timeout configurável via ENV (default: 30s)
            timeout = int(getenv("SUPABASE_TIMEOUT", "30"))

            # FIX v2.0.3: Use options dict instead of ClientOptions class
            options = dict(
                postgrest_client_timeout=timeout,
                storage_client_timeout=timeout,
            )

            _supabase_client = create_client(url, key, options=options)

        return _supabase_client
