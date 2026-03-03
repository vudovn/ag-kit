"""
Modelos de Dados do Cérebro LUNA
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


class IntentType:
    """Tipos de intenção suportados"""

    AGENDAR = "agendar"
    PRECO = "preco"
    SERVICOS_TECNICOS = "servicos_tecnicos"
    SAUDACAO = "saudacao"
    AGRADECIMENTO = "agradecimento"
    DISPONIBILIDADE = "disponibilidade"
    SERVICOS = "servicos"
    PACOTE = "pacote"
    CUPOM = "cupom"
    LOCALIZACAO = "localizacao"
    HORARIO_FUNC = "horario_func"
    RECLAMACAO = "reclamacao"
    HANDOFF = "handoff"
    CONVERSA = "conversa"
    MULTI_SERVICO = "multi_servico"
    UNKNOWN = "unknown"


class SentimentType:
    """Tipos de sentimento"""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class CustomerMood:
    """Humor do cliente"""

    HAPPY = "happy"
    FRUSTRATED = "frustrated"
    HESITANT = "hesitant"
    HURRY = "hurry"
    UNKNOWN = "unknown"


class PotentialValue:
    """Valor potencial do cliente"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class IntelligenceData:
    """Dados de inteligência extraídos da conversa"""

    insight: str = "Insight não detectado"
    objections: List[str] = field(default_factory=list)
    customer_mood: CustomerMood = CustomerMood.UNKNOWN
    urgency_level: int = 3
    potential_value: PotentialValue = PotentialValue.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "insight": self.insight,
            "objections": self.objections,
            "customer_mood": self.customer_mood,
            "urgency_level": self.urgency_level,
            "potential_value": self.potential_value,
            "metadata": self.metadata,
        }


@dataclass
class BrainResult:
    """Resultado do processamento do brain"""

    ok: bool = True
    response: str = ""
    intent: str = IntentType.UNKNOWN
    model: str = "local"
    sentiment: str = SentimentType.NEUTRAL
    intent_confidence: float = 0.0
    processing_ms: int = 0
    action: Optional[str] = None
    intelligence: IntelligenceData = field(default_factory=IntelligenceData)

    def to_dict(self):
        return {
            "ok": self.ok,
            "response": self.response,
            "intent": self.intent,
            "model": self.model,
            "sentiment": self.sentiment,
            "intent_confidence": self.intent_confidence,
            "processing_ms": self.processing_ms,
            "action": self.action,
            "intelligence": self.intelligence.to_dict(),
        }
