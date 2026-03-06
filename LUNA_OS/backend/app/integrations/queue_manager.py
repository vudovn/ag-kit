"""
Queue Manager - Gerencia filas de processamento (Thread-Safe)
Suporta: Jobs, Agendamentos, Processamento em Background
"""
import asyncio
import logging
import threading
from typing import Any, Callable, Dict, Optional
from datetime import datetime, timedelta
from functools import wraps

import redis
from rq import Queue, Worker, Retry, get_current_job
from rq_scheduler import Scheduler

logger = logging.getLogger(__name__)


class QueueManager:
    """Gerenciador centralizado de filas"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self._redis_conn: Optional[redis.Redis] = None
        self._lock = asyncio.Lock()
        self.queues: Dict[str, Queue] = {}
        self._scheduler: Optional[Scheduler] = None
        self._initialized = False

    @property
    def redis_conn(self) -> redis.Redis:
        """Lazy connection to Redis"""
        if self._redis_conn is None:
            self._redis_conn = redis.from_url(self.redis_url)
        return self._redis_conn

    @property
    def scheduler(self) -> Scheduler:
        """Lazy scheduler initialization"""
        if self._scheduler is None:
            self._scheduler = Scheduler(connection=self.redis_conn)
        return self._scheduler

    async def initialize(self) -> bool:
        """Initialize QueueManager with thread-safety"""
        async with self._lock:
            if self._initialized:
                return True
            
            try:
                # Test connection
                self.redis_conn.ping()
                self._initialized = True
                logger.info("✅ QueueManager initialized")
                return True
            except Exception as e:
                logger.error(f"❌ QueueManager initialization failed: {e}")
                return False

    def get_queue(self, name: str = "default", is_async: bool = True) -> Queue:
        """Obter ou criar fila"""
        if name not in self.queues:
            self.queues[name] = Queue(
                name, connection=self.redis_conn, is_async=is_async
            )
        return self.queues[name]

    def enqueue_job(
        self,
        queue_name: str,
        func: Callable,
        *args,
        job_id: Optional[str] = None,
        timeout: str = "5m",
        retry: int = 3,
        **kwargs,
    ):
        """Enfileirar job com retry automático"""
        queue = self.get_queue(queue_name)

        job = queue.enqueue(
            func,
            args=args,
            kwargs=kwargs,
            job_id=job_id,
            timeout=timeout,
            retry=Retry(max=retry, interval=[10, 30, 60]),
        )

        logger.info(f"Job {job.id} enfileirado em {queue_name}")
        return job

    def schedule_job(
        self,
        func: Callable,
        scheduled_time: datetime,
        job_id: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """Agendar job para tempo específico"""
        job = self.scheduler.schedule(
            scheduled_time=scheduled_time,
            func=func,
            args=args,
            kwargs=kwargs,
            job_id=job_id,
        )

        logger.info(f"Job {job.id} agendado para {scheduled_time}")
        return job

    def get_job_status(self, job_id: str, queue_name: str = "default"):
        """Obter status do job"""
        queue = self.get_queue(queue_name)
        job = queue.fetch_job(job_id)

        if not job:
            return None

        return {
            "id": job.id,
            "status": job.get_status(),
            "result": job.result,
            "exc_info": job.exc_info,
            "started_at": job.started_at,
            "ended_at": job.ended_at,
        }


# Thread-safe singleton instance
_queue_manager_lock = threading.Lock()
_queue_manager: Optional[QueueManager] = None


def get_queue_manager(redis_url: Optional[str] = None) -> QueueManager:
    """Get singleton instance (thread-safe)"""
    global _queue_manager
    
    with _queue_manager_lock:
        if _queue_manager is None:
            url = redis_url or "redis://luna-redis:6379/0"
            _queue_manager = QueueManager(redis_url=url)
        
        return _queue_manager


# Backward compatibility alias
queue_manager = get_queue_manager()


# Decorators para uso fácil
def background_job(queue_name: str = "default", timeout: str = "5m"):
    """Decorator para transformar função em background job"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return queue_manager.enqueue_job(
                queue_name, func, *args, timeout=timeout, **kwargs
            )

        return wrapper

    return decorator


def scheduled_job(queue_name: str = "default"):
    """Decorator para jobs agendados"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(scheduled_time: datetime, *args, **kwargs):
            return queue_manager.schedule_job(func, scheduled_time, *args, **kwargs)

        return wrapper

    return decorator


# ===== BACKGROUND JOBS ESPECÍFICAS DO LUNA =====


@background_job(queue_name="messages")
def process_whatsapp_message(phone: str, message: str, conversation_id: str):
    """Processar mensagem WhatsApp"""
    logger.info(f"Processando mensagem de {phone}: {message}")
    return {"status": "processed", "conversation_id": conversation_id}


@background_job(queue_name="analytics")
def update_customer_analytics(customer_id: str):
    """Atualizar analytics do cliente"""
    logger.info(f"Atualizando analytics para {customer_id}")
    return {"status": "updated", "customer_id": customer_id}


@background_job(queue_name="churn")
def predict_churn_risk(customer_id: str):
    """Prever risco de churn"""
    logger.info(f"Prevendo churn para {customer_id}")
    return {"customer_id": customer_id, "risk_score": 0.75}


@background_job(queue_name="campaigns")
def send_campaign_batch(campaign_id: str, batch_ids: list):
    """Enviar lote de campanhas"""
    logger.info(f"Enviando campanha {campaign_id} para {len(batch_ids)} clientes")
    return {"campaign_id": campaign_id, "sent": len(batch_ids)}


@scheduled_job(queue_name="scheduled")
def daily_report_generation(scheduled_time: datetime):
    """Gerar relatório diário"""
    logger.info(f"Gerando relatório diário em {scheduled_time}")
    return {"status": "report_generated", "timestamp": scheduled_time}
