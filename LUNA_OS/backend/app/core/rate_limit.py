"""
Rate Limiter Configuration - DEBT #19, #M3
Configuração de rate limiting por tipo de endpoint

DEBT #M3: Type hints completos adicionados
"""
from typing import Callable
from slowapi import Limiter
from slowapi.util import get_remote_address

# Global IP-based rate limiter
limiter: Limiter = Limiter(key_func=get_remote_address)


# Rate limit presets for different endpoint types
RATE_LIMITS = {
    # Public endpoints (low limit)
    "public": "30/minute",

    # Authenticated user endpoints (medium limit)
    "user": "100/minute",

    # Webhook endpoints (high limit - external systems)
    "webhook": "1000/minute",

    # Health check endpoints (very high limit)
    "health": "60/minute",

    # Admin endpoints (medium limit)
    "admin": "50/minute",

    # Search/query endpoints (lower limit - expensive operations)
    "search": "20/minute",

    # Write operations (lower limit)
    "write": "30/minute",
}


def get_limit_for_type(limit_type: str) -> str:
    """
    Get rate limit string for endpoint type.

    Args:
        limit_type: One of 'public', 'user', 'webhook', 'health', 'admin', 'search', 'write'

    Returns:
        Rate limit string (e.g., "30/minute")
    """
    return RATE_LIMITS.get(limit_type, RATE_LIMITS["public"])


# DEBT #19: Specific limit decorators for common use cases
limiter_public = limiter.limit(RATE_LIMITS["public"])
limiter_user = limiter.limit(RATE_LIMITS["user"])
limiter_webhook = limiter.limit(RATE_LIMITS["webhook"])
limiter_health = limiter.limit(RATE_LIMITS["health"])
limiter_admin = limiter.limit(RATE_LIMITS["admin"])
limiter_search = limiter.limit(RATE_LIMITS["search"])
limiter_write = limiter.limit(RATE_LIMITS["write"])
