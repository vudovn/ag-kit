import asyncio
import functools
import random
import re
from loguru import logger


def retry(retries=3, backoff_in_seconds=1):
    """
    Decorador de retry com exponential backoff para funções assíncronas.
    Ideal para APIs instáveis.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(
                            f"❌ Falha definitiva após {retries} tentativas em {func.__name__}: {e}"
                        )
                        raise

                    sleep_time = (backoff_in_seconds * 2**x) + (
                        random.randint(0, 1000) / 1000
                    )
                    logger.warning(
                        f"⚠️ Falha em {func.__name__} (tentativa {x+1}/{retries}). Retentando em {sleep_time:.2f}s... Erro: {e}"
                    )

                    await asyncio.sleep(sleep_time)
                    x += 1

        return wrapper

    return decorator


def sanitize_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitiza a entrada do usuário para prevenir ataques básicos e abusos.
    """
    if not text:
        return ""

    # 1. Limitar tamanho para prevenir DoS simples ou ataques de contexto longo
    text = text[:max_length]

    # 2. Remover caracteres de controle Unicode que podem ser usados para ocultar comandos
    text = "".join(ch for ch in text if ch.isprintable() or ch in ["\n", "\r", "\t"])

    # 3. Detectar padrões suspeitos de Prompt Injection (apenas logar para auditoria)
    jailbreak_patterns = [
        r"ignore previous",
        r"system prompt",
        r"você é agora",
        r"you are now",
        r"forget everything",
    ]

    for pattern in jailbreak_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"🚨 Possível tentativa de Jailbreak detectada: '{pattern}'")
            # Poderíamos bloquear aqui, mas por enquanto apenas logamos para monitoramento
            break

    return text.strip()


class ResilienceEngine:
    """
    Camada de Resiliência Sōra: Centraliza lógica de retry e sanitização.
    """

    def __init__(self):
        self.retry = retry
        self.sanitize = sanitize_input
