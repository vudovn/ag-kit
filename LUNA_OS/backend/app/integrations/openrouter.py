"""
OpenRouter Client — MCT Token Economy + Circuit Breaker
Roteamento estratégico de modelos por função para máxima eficiência de tokens.
"""

import httpx
from app.config import settings
from app.core.resilience import retry
from loguru import logger
from datetime import datetime, timedelta

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# [KIMI-P3] Timeout por fase: connect rápido (5s), read generoso mas limitado (12s)
OPENROUTER_TIMEOUT = httpx.Timeout(
    connect=5.0,
    read=12.0,
    write=5.0,
    pool=2.0,
)

# [CIRCUIT BREAKER] Estado do circuito
class CircuitBreaker:
    """Circuit Breaker para OpenRouter"""

    def __init__(self, failure_threshold=3, recovery_timeout=60):
        self.failure_threshold = failure_threshold  # 3 falhas consecutivas
        self.recovery_timeout = recovery_timeout  # 60 segundos para recuperar
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_failure(self):
        """Registrar falha"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"🚨 CIRCUIT BREAKER OPEN — {self.failure_count} falhas consecutivas")

    def record_success(self):
        """Registrar sucesso"""
        self.failure_count = 0
        self.state = "CLOSED"

    def can_execute(self) -> bool:
        """Verificar se pode executar"""
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            # Verificar se já passou o timeout de recuperação
            if self.last_failure_time:
                elapsed = datetime.utcnow() - self.last_failure_time
                if elapsed > timedelta(seconds=self.recovery_timeout):
                    self.state = "HALF_OPEN"
                    logger.warning("⚠️ CIRCUIT BREAKER HALF_OPEN — Tentando recuperar")
                    return True
            return False

        if self.state == "HALF_OPEN":
            return True

        return False

    def get_state(self) -> str:
        """Obter estado atual"""
        return self.state

# [CIRCUIT BREAKER] Instância global
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)


class OpenRouterClient:
    def __init__(self):
        # We read from settings in each request to allow runtime updates
        pass

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {settings.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://luna-os.mctltda.com",
            "X-Title": "LUNA Core v2.0 - Haven",
        }

    @retry(retries=3, backoff_in_seconds=1)
    async def complete(
        self,
        messages: list,
        system: str = None,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        context: dict = None,  # [LOG ESTRUTURADO] Contexto para logs
    ) -> str:
        """
        Send a chat completion request to OpenRouter.
        """
        if not model:
            model = settings.model_standard

        # [LOG ESTRUTURADO] Logger com contexto completo
        log_context = {"model": model, "max_tokens": max_tokens}
        if context:
            log_context.update(context)
        log = logger.bind(**log_context)

        payload_messages = []
        if system:
            payload_messages.append({"role": "system", "content": system})
        payload_messages.extend(messages)

        payload = {
            "model": model,
            "messages": payload_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            # [CIRCUIT BREAKER] Verificar se pode executar
            if not circuit_breaker.can_execute():
                log.warning(f"🚨 CIRCUIT BREAKER OPEN — Usando fallback local")
                raise Exception("Circuit Breaker OPEN — OpenRouter indisponível")

            async with httpx.AsyncClient(timeout=OPENROUTER_TIMEOUT) as client:
                url = f"{OPENROUTER_BASE}/chat/completions"
                log.debug(f"OpenRouter → {url} | msgs={len(payload_messages)}")

                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                )

                if response.status_code != 200:
                    log.error(
                        f"OpenRouter HTTP {response.status_code} | body={response.text[:200]}"
                    )
                response.raise_for_status()
                data = response.json()

                # [CIRCUIT BREAKER] Registrar sucesso
                circuit_breaker.record_success()

                # Log usage for token economy monitoring
                usage = data.get("usage", {})
                log.info(
                    f"OpenRouter OK | "
                    f"in={usage.get('prompt_tokens', '?')} "
                    f"out={usage.get('completion_tokens', '?')} tokens"
                )

                return data["choices"][0]["message"]["content"]

        except httpx.TimeoutException as e:
            # [CIRCUIT BREAKER] Registrar falha
            circuit_breaker.record_failure()
            log.warning(f"⚠️ OpenRouter TIMEOUT após {OPENROUTER_TIMEOUT.read}s | {e}")
            raise
        except httpx.HTTPStatusError as e:
            # [CIRCUIT BREAKER] Registrar falha
            circuit_breaker.record_failure()
            log.error(f"⚠️ OpenRouter HTTP Error | status={e.response.status_code}")
            raise
        except Exception as e:
            # [CIRCUIT BREAKER] Registrar falha
            circuit_breaker.record_failure()
            log.error(f"⚠️ OpenRouter Error | {type(e).__name__}: {e}")
            raise


# Singleton
openrouter = OpenRouterClient()
