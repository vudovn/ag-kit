"""
Sistema de Alertas - Ntfy
Notificações para: Churn Alto, Oportunidades, Erros
"""

import logging
import json
from typing import Optional, Dict, Any
from enum import Enum
import httpx

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Níveis de severidade"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertSystem:
    """Sistema centralizado de alertas"""
    
    def __init__(self, ntfy_topic: str, base_url: str = "https://ntfy.sh"):
        self.ntfy_topic = ntfy_topic
        self.base_url = base_url
        self.client = httpx.Client()
    
    def send_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        tags: Optional[list] = None,
        click_action: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """Enviar alerta via Ntfy"""
        
        # Mapear severidade para emoji
        severity_emoji = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️",
            AlertSeverity.HIGH: "🔴",
            AlertSeverity.CRITICAL: "🚨"
        }
        
        headers = {
            "Title": f"{severity_emoji[severity]} {title}",
            "Priority": severity.value
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
                content=body
            )
            response.raise_for_status()
            logger.info(f"Alerta enviado: {title}")
        except Exception as e:
            logger.error(f"Erro ao enviar alerta: {e}")
    
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