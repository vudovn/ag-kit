"""
Supabase Client
"""

# WORKAROUND: Fix httpx/gotrue proxy argument mismatch
import httpx

original_init = httpx.Client.__init__


def new_init(self, *args, **kwargs):
    if "proxy" in kwargs:
        kwargs["proxies"] = kwargs.pop("proxy")
    original_init(self, *args, **kwargs)


httpx.Client.__init__ = new_init

from supabase import create_client, Client
from app.config import settings

supabase: Client = None


async def init_supabase():
    global supabase
    # Padrão SWE-Bench: Garantir que segredos venham do ENV limpo (bypass .env corrompido)
    from os import getenv

    url = getenv("SUPABASE_URL", settings.supabase_url).strip('"').strip("'")
    key = getenv("SUPABASE_KEY", settings.supabase_key).strip('"').strip("'")
    supabase = create_client(url, key)
    return supabase


def get_supabase() -> Client:
    global supabase
    if supabase is None:
        from os import getenv

        url = getenv("SUPABASE_URL", settings.supabase_url).strip('"').strip("'")
        key = getenv("SUPABASE_KEY", settings.supabase_key).strip('"').strip("'")
        supabase = create_client(url, key)
    return supabase
