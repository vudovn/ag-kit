"""
Sistema de Alertas - Ntfy (com Rate-Limit)
Notificações para: Churn Alto, Oportunidades, Erros

DEBT #10: Implementa rate-limit para prevenir spam de alertas em falhas em cascata.
"""

import logging
import json
import time
from typing import Optional, Dict, Any
from enum import Enum
from collections import defaultdict
from datetime import datetime, timedelta
import httpx

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Níveis de severidade"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Rate-limit configuration
ALERT_RATE_LIMITS = {
    AlertSeverity.CRITICAL: {"max": 10, "window_seconds": 60},  # 10/min
    AlertSeverity.HIGH: {"max": 5, "window_seconds": 60},       # 5/min
    AlertSeverity.MEDIUM: {"max": 3, "window_seconds": 60},     # 3/min
    AlertSeverity.LOW: {"max": 1, "window_seconds": 60},        # 1/min
}


class RateLimiter:
    """Token bucket rate limiter for alerts"""
    
    def __init__(self):
        # Track alerts by type: {alert_type: [timestamp, timestamp, ...]}
        self._alert_history: Dict[str, list] = defaultdict(list)
        self._suppressed_count: Dict[str, int] = defaultdict(int)
    
    def should_allow(self, alert_type: str, severity: AlertSeverity) -> bool:
        """
        Check if alert should be sent based on rate limit.
        Returns True if allowed, False if rate-limited.
        """
        config = ALERT_RATE_LIMITS.get(severity, ALERT_RATE_LIMITS[AlertSeverity.MEDIUM])
        max_alerts = config["max"]
        window = config["window_seconds"]
        now = time.time()
        
        # Clean old entries
        self._alert_history[alert_type] = [
            ts for ts in self._alert_history[alert_type]
            if now - ts < window
        ]
        
        # Check if under limit
        if len(self._alert_history[alert_type]) < max_alerts:
            self._alert_history[alert_type].append(now)
            return True
        
        # Rate-limited
        self._suppressed_count[alert_type] += 1
        return False
    
    def get_suppressed_count(self, alert_type: str) -> int:
        """Get count of suppressed alerts for this type"""
        return self._suppressed_count.get(alert_type, 0)
    
    def reset_suppressed_count(self, alert_type: str):
        """Reset suppressed count after sending a summary"""
        self._suppressed_count[alert_type] = 0


class AlertSystem:
    """Sistema centralizado de alertas com rate-limit"""

    def __init__(self, ntfy_topic: str, base_url: str = "https://ntfy.sh"):
        self.ntfy_topic = ntfy_topic
        self.base_url = base_url
        self.client = httpx.Client(timeout=10.0)  # Add timeout
        self._rate_limiter = RateLimiter()
        self._last_summary_sent: Dict[str, float] = {}

    def _get_alert_type_key(self, title: str, tags: Optional[list] = None) -> str:
        """Generate a unique key for alert type (for rate limiting)"""
        # Use tags or extract from title
        if tags:
            return "_".join(sorted(tags))
        # Extract first word from title as type
        return title.split()[0] if title else "unknown"

    def _should_send_alert(self, title: str, severity: AlertSeverity, tags: Optional[list] = None) -> bool:
        """Check if alert passes rate-limit"""
        alert_type = self._get_alert_type_key(title, tags)
        return self._rate_limiter.should_allow(alert_type, severity)

    def _send_suppressed_summary(self, alert_type: str, severity: AlertSeverity):
        """Send summary of suppressed alerts"""
        now = time.time()
        # Only send summary every 5 minutes
        if now - self._last_summary_sent.get(alert_type, 0) < 300:
            return
        
        count = self._rate_limiter.get_suppressed_count(alert_type)
        if count > 0:
            self._send_raw_alert(
                title=f"📊 Resumo de Alertas Suprimidos: {alert_type}",
                message=f"{count} alertas foram suprimidos devido ao rate-limit nos últimos minutos.",
                severity=AlertSeverity.MEDIUM,
                tags=["rate-limit", "summary", alert_type]
            )
            self._rate_limiter.reset_suppressed_count(alert_type)
            self._last_summary_sent[alert_type] = now

    def _send_raw_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        tags: Optional[list] = None,
        click_action: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """Internal method to send alert without rate-limit check"""
        severity_emoji = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️",
            AlertSeverity.HIGH: "🔴",
            AlertSeverity.CRITICAL: "🚨"
        }

        headers = {
            "Title": f"{severity_emoji.get(severity, '⚠️')} {title}",
            "Priority": str(severity.value if severity else "medium")
        }

        if tags:
            headers["Tags"] = ",".join(tags)

        if click_action:
            headers["Click"] = click_action

        body = message
        if data:
            body += f"\n\n```json\n{json.dumps(data, indent=2)}\n```"

        try:
            response = self.client.post(
                f"{self.base_url}/{self.ntfy_topic}",
                headers=headers,
                content=body,
                timeout=10.0
            )
            response.raise_for_status()
            logger.info(f"Alerta enviado: {title}")
        except Exception as e:
            logger.error(f"Erro ao enviar alerta: {e}")

    def send_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        tags: Optional[list] = None,
        click_action: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """Enviar alerta via Ntfy com rate-limit"""
        
        # Check rate-limit
        if not self._should_send_alert(title, severity, tags):
            logger.debug(f"Rate-limit: Alerta suprimido '{title}'")
            self._send_suppressed_summary(
                self._get_alert_type_key(title, tags),
                severity
            )
            return
        
        self._send_raw_alert(
            title=title,
            message=message,
            severity=severity,
            tags=tags,
            click_action=click_action,
            data=data
        )

    def alert_high_churn(self, customer: Dict[str, Any]):
        """Alerta: Cliente com risco alto de churn"""
        self.send_alert(
            title=f"CHURN ALTO: {customer['name']}",
            message=f"Risco de perda: {customer['churn_score']:.0%}\n"
                   f"Cliente: {customer['phone']}\n"
                   f"Última compra: {customer['last_purchase_days']} dias atrás",
            severity=AlertSeverity.HIGH,
            tags=["churn", "alert"],
            click_action=f"/customers/{customer['id']}",
            data={
                "customer_id": customer['id'],
                "risk_score": customer['churn_score'],
                "actions": ["send_offer", "call_customer", "discount"]
            }
        )

    def alert_high_conversion_opportunity(self, conversation: Dict[str, Any]):
        """Alerta: Oportunidade de venda"""
        self.send_alert(
            title=f"🎯 VENDA QUENTE: {conversation['customer_name']}",
            message=f"Probabilidade conversão: {conversation['conversion_prob']:.0%}\n"
                   f"Estágio: {conversation['funnel_stage']}\n"
                   f"Ação recomendada: {conversation['recommended_action']}",
            severity=AlertSeverity.MEDIUM,
            tags=["sales", "opportunity"],
            click_action=f"/conversations/{conversation['id']}",
            data=conversation
        )

    def alert_system_error(self, error: Exception, context: Dict[str, Any]):
        """Alerta: Erro no sistema"""
        self.send_alert(
            title=f"🐛 ERRO NO SISTEMA",
            message=f"Tipo: {type(error).__name__}\n"
                   f"Mensagem: {str(error)}",
            severity=AlertSeverity.CRITICAL,
            tags=["error", "system"],
            data={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            }
        )

    def alert_campaign_sent(self, campaign: Dict[str, Any]):
        """Notificação: Campanha enviada"""
        self.send_alert(
            title=f"✅ Campanha Enviada: {campaign['name']}",
            message=f"Total enviado: {campaign['total_sent']}\n"
                   f"Taxa abertura estimada: {campaign['estimated_open_rate']:.0%}",
            severity=AlertSeverity.LOW,
            tags=["campaign", "success"],
            data=campaign
        )

    def alert_peak_hours_reached(self, queue_info: Dict[str, Any]):
        """Alerta: Pico de mensagens"""
        self.send_alert(
            title="📊 PICO DE MENSAGENS",
            message=f"Mensagens na fila: {queue_info['pending']}\n"
                   f"Tempo médio espera: {queue_info['avg_wait']}s\n"
                   f"Taxa processamento: {queue_info['processing_rate']} msg/s",
            severity=AlertSeverity.MEDIUM,
            tags=["queue", "performance"],
            data=queue_info
        )


# Instância global
import os
alert_system = AlertSystem(
    ntfy_topic=os.getenv("NTFY_TOPIC", "luna-alerts"),
    base_url=os.getenv("NTFY_BASE_URL", "https://ntfy.sh")
)
