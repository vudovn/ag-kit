"""
Evolution Engine - Camada 6: Evolução Contínua (Sōra)
Padrão MCT: Auditoria em tempo real + Aprendizado contínuo

Arquitetura:
- Audit: Qualidade técnica das respostas (incerteza, alucinação)
- Intelligence: Alinhamento de negócio (mood, urgência, valor)
- Maturity: Score combinado para decisão de ativação
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any
from enum import Enum
from loguru import logger

from app.integrations.supabase_client import get_supabase
from supabase import Client


# ═══════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════


class AuditFlag(str, Enum):
    """Flags de auditoria"""

    VALIDATED = "validated"
    UNCERTAIN = "uncertain"
    NEEDS_REVIEW = "needs_human_review"


class MaturityStatus(str, Enum):
    """Status de maturidade"""

    NO_DATA = "no_data"
    DEVELOPING = "developing"
    MEDIUM = "medium"
    READY = "ready"


@dataclass
class AuditResult:
    """Resultado da auditoria de resposta"""

    confidence_score: float = 1.0
    audit_flag: AuditFlag = AuditFlag.VALIDATED
    has_price: bool = False
    has_time: bool = False
    uncertainty_detected: bool = False
    uncertainty_matches: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "confidence_score": self.confidence_score,
            "audit_flag": self.audit_flag.value,
            "has_price": self.has_price,
            "has_time": self.has_time,
            "uncertainty_detected": self.uncertainty_detected,
            "matches": self.uncertainty_matches,
            "metadata": self.metadata,
        }


@dataclass
class MaturityScore:
    """Score de maturidade do sistema"""

    score: int = 0
    evolution_component: int = 0
    intelligence_component: int = 0
    total_interactions: int = 0
    recommendation: str = "Aguardando volume de dados..."
    status: MaturityStatus = MaturityStatus.NO_DATA

    def to_dict(self) -> Dict:
        return {
            "score": self.score,
            "evolution_component": self.evolution_component,
            "intelligence_component": self.intelligence_component,
            "total_interactions": self.total_interactions,
            "recommendation": self.recommendation,
            "status": self.status.value,
        }


# ═══════════════════════════════════════════════
# EVOLUTION ENGINE
# ═══════════════════════════════════════════════


class EvolutionEngine:
    """
    Camada 6: Evolução Contínua
    Responsável por auditar respostas, aprender com interações e medir maturidade.
    """

    # Keywords que indicam incerteza (anti-patterns)
    UNCERTAINTY_KEYWORDS = [
        "acho",
        "talvez",
        "não tenho certeza",
        "provavelmente",
        "deve ser",
        "acredito que",
        "vou verificar",
        "deixa eu ver",
        "já te falo",
        "vou ver com",
    ]

    # Keywords que indicam preço/horário (requerem validação)
    SENSITIVE_PATTERNS = {
        "price": re.compile(r"R\$\s*\d+(?:,\d{2})?"),
        "time": re.compile(r"\d{1,2}h(?:\d{2})?|\d{1,2}:\d{2}"),
    }

    def __init__(self):
        self._supabase: Optional[Client] = None

    def _get_db(self) -> Client:
        """Lazy loading do cliente Supabase"""
        if self._supabase is None:
            self._supabase = get_supabase()
        return self._supabase

    async def audit_response(
        self,
        intent: str,
        response: str,
        phone: Optional[str] = None,
    ) -> AuditResult:
        """
        Auditoria em tempo real da resposta gerada pela LUNA.

        Critérios:
        1. Detecção de incerteza (palavras-chave)
        2. Detecção de dados sensíveis (preços/horários)
        3. Contexto da intenção (preço/horário são OK se relevantes)
        4. Cálculo de confiança (heurística ponderada)
        """
        response_lower = response.lower()

        # 1. Detecção de incerteza
        uncertainty_matches = [
            word for word in self.UNCERTAINTY_KEYWORDS if word in response_lower
        ]
        has_uncertainty = len(uncertainty_matches) > 0

        # 2. Detecção de dados sensíveis
        has_price = bool(self.SENSITIVE_PATTERNS["price"].search(response))
        has_time = bool(self.SENSITIVE_PATTERNS["time"].search(response))

        # 3. Cálculo de confiança (heurística)
        confidence_score = self._calculate_confidence(
            has_uncertainty=has_uncertainty,
            has_price=has_price,
            has_time=has_time,
            intent=intent,
        )

        # 4. Determinação da flag de auditoria
        audit_flag = self._determine_audit_flag(
            confidence_score=confidence_score,
            has_uncertainty=has_uncertainty,
        )

        result = AuditResult(
            confidence_score=confidence_score,
            audit_flag=audit_flag,
            has_price=has_price,
            has_time=has_time,
            uncertainty_detected=has_uncertainty,
            uncertainty_matches=uncertainty_matches,
            metadata={
                "intent": intent,
                "phone": phone,
                "response_length": len(response),
            },
        )

        logger.info(
            f"🔍 Evolution Audit: {audit_flag.value} "
            f"(Score: {confidence_score:.2f}) for {phone}"
        )

        return result

    def _calculate_confidence(
        self,
        has_uncertainty: bool,
        has_price: bool,
        has_time: bool,
        intent: str,
    ) -> float:
        """
        Calcula score de confiança (0.0 - 1.0)

        Regras:
        - Incerteza reduz confiança em 0.4
        - Preço/horário fora de contexto reduz em 0.3
        - Base starts at 1.0
        """
        confidence = 1.0

        # Penalidade por incerteza
        if has_uncertainty:
            confidence -= 0.4

        # Penalidade por dados sensíveis fora de contexto
        sensitive_intents = {"preco", "agendar", "horario_func"}
        if (has_price or has_time) and intent not in sensitive_intents:
            confidence -= 0.3

        # Clamp entre 0.0 e 1.0
        return max(0.0, min(1.0, confidence))

    def _determine_audit_flag(
        self,
        confidence_score: float,
        has_uncertainty: bool,
    ) -> AuditFlag:
        """Determina flag de auditoria baseada na confiança"""

        if confidence_score >= 0.8:
            return AuditFlag.VALIDATED
        elif has_uncertainty:
            return AuditFlag.UNCERTAIN
        else:
            return AuditFlag.NEEDS_REVIEW

    async def log_evolution(
        self,
        phone: str,
        intent: str,
        response: str,
        audit_data: AuditResult,
        conversation_id: Optional[str] = None,
    ):
        """
        Registra interação no learning_log para aprendizado futuro.
        """
        db = self._get_db()

        try:
            log_entry = {
                "phone": phone,
                "conversation_id": conversation_id,
                "intent": intent,
                "response_content": response[:500],  # Limit size
                "confidence_score": audit_data.confidence_score,
                "audit_flag": audit_data.audit_flag.value,
                "metadata": {
                    "has_price": audit_data.has_price,
                    "has_time": audit_data.has_time,
                    "uncertainty": audit_data.uncertainty_detected,
                    "uncertainty_matches": audit_data.uncertainty_matches,
                },
                "created_at": datetime.utcnow().isoformat(),
            }

            db.table("learning_log").insert(log_entry).execute()
            logger.debug(f"📚 Evolution log saved for {phone}")

        except Exception as e:
            logger.error(f"❌ Error logging evolution: {e}")

    async def calculate_maturity_score(self) -> MaturityScore:
        """
        Calcula Score de Maturidade Soberana (0-100).

        Fórmula:
        - 70% Evolution (Qualidade Técnica)
        - 30% Intelligence (Alinhamento de Negócio)

        Thresholds:
        - > 75: Pronto para ativar
        - > 50: Maturidade média (observar)
        - < 50: Não ativar
        """
        db = self._get_db()

        try:
            # 1. Componente Evolution (Qualidade Técnica)
            evolution_score = await self._calculate_evolution_component(db)

            # 2. Componente Intelligence (Alinhamento Negócio)
            intelligence_score = await self._calculate_intelligence_component(db)

            # 3. Score combinado (70% Evolution + 30% Intelligence)
            combined_score = round(
                (evolution_score.get("score", 0) * 0.7)
                + (intelligence_score.get("score", 0) * 0.3)
            )

            # 4. Determinar status e recomendação
            status, recommendation = self._evaluate_maturity(
                combined_score=combined_score,
                total_interactions=evolution_score["total"],
            )

            return MaturityScore(
                score=combined_score,
                evolution_component=evolution_score["score"],
                intelligence_component=intelligence_score["score"],
                total_interactions=evolution_score["total"],
                recommendation=recommendation,
                status=status,
            )

        except Exception as e:
            logger.error(f"❌ Error calculating maturity score: {e}")
            return MaturityScore(
                score=0,
                recommendation=f"Erro no cálculo: {str(e)}",
                status=MaturityStatus.NO_DATA,
            )

    async def _calculate_evolution_component(
        self,
        db: Client,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Calcula componente de evolução baseado em logs recentes.
        Retorna dict com score (0-100) e total de interações.
        """
        try:
            result = (
                db.table("learning_log")
                .select("audit_flag")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            logs = result.data or []
            total = len(logs)

            if total == 0:
                return {"score": 0, "total": 0}

            # Contagens por flag
            validated = sum(1 for l in logs if l.get("audit_flag") == "validated")
            uncertain = sum(1 for l in logs if l.get("audit_flag") == "uncertain")
            needs_review = sum(
                1 for l in logs if l.get("audit_flag") == "needs_human_review"
            )

            # Score ponderado
            score = round(
                ((validated * 1.0) + (uncertain * 0.5) + (needs_review * 0.2))
                / total
                * 100
            )

            return {"score": min(100, score), "total": total}

        except Exception as e:
            logger.error(f"❌ Error calculating evolution component: {e}")
            return {"score": 0, "total": 0}

    async def _calculate_intelligence_component(
        self,
        db: Client,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Calcula componente de inteligência baseado em BI recente.
        Retorna dict com score (0-100) e total de registros.
        """
        try:
            result = (
                db.table("business_intelligence")
                .select("urgency_level, potential_value, customer_mood")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            bi_logs = result.data or []
            total = len(bi_logs)

            if total == 0:
                return {"score": 0, "total": 0}

            # Score baseado em humor positivo e valor
            happy_moods = {"happy", "hurry"}
            high_values = {"high"}

            happy_count = sum(
                1 for l in bi_logs if l.get("customer_mood") in happy_moods
            )
            high_value_count = sum(
                1 for l in bi_logs if l.get("potential_value") in high_values
            )

            # 70% humor positivo + 30% valor alto
            score = round(
                ((happy_count * 0.7) + (high_value_count * 0.3)) / total * 100
            )

            return {"score": min(100, score), "total": total}

        except Exception as e:
            logger.error(f"❌ Error calculating intelligence component: {e}")
            return {"score": 0, "total": 0}

    def _evaluate_maturity(
        self,
        combined_score: int,
        total_interactions: int,
    ) -> tuple[MaturityStatus, str]:
        """Avalia maturidade e retorna status + recomendação"""

        if total_interactions == 0:
            return (
                MaturityStatus.NO_DATA,
                "Aguardando volume de dados soberanos...",
            )
        elif combined_score > 75:
            return (
                MaturityStatus.READY,
                "✅ PRONTO PARA ATIVAR. Maturidade soberana atingida.",
            )
        elif combined_score > 50:
            return (
                MaturityStatus.MEDIUM,
                "Maturidade média. Continue em modo 'observe' para refinar.",
            )
        else:
            return (
                MaturityStatus.DEVELOPING,
                "Não ativar ainda. Alma em desenvolvimento.",
            )

    async def get_quality_metrics(self, days: int = 7) -> Dict[str, Any]:
        """
        Retorna métricas de qualidade para período específico.
        """
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        try:
            # Learning logs
            logs_result = (
                db.table("learning_log")
                .select("audit_flag, confidence_score, created_at")
                .gte("created_at", since)
                .execute()
            )

            logs = logs_result.data or []

            # Business intelligence
            bi_result = (
                db.table("business_intelligence")
                .select("customer_mood, urgency_level, potential_value, created_at")
                .gte("created_at", since)
                .execute()
            )

            bi_logs = bi_result.data or []

            # Métricas
            total_interactions = len(logs)
            validated_rate = (
                sum(1 for l in logs if l.get("audit_flag") == "validated")
                / total_interactions
                if total_interactions > 0
                else 0
            )

            avg_confidence = (
                sum(l.get("confidence_score", 0) for l in logs) / total_interactions
                if total_interactions > 0
                else 0
            )

            mood_distribution = self._count_distribution(
                [l.get("customer_mood", "unknown") for l in bi_logs]
            )

            urgency_avg = (
                sum(l.get("urgency_level", 3) for l in bi_logs) / len(bi_logs)
                if bi_logs
                else 3
            )

            return {
                "period_days": days,
                "total_interactions": total_interactions,
                "validated_rate": round(validated_rate, 2),
                "avg_confidence": round(avg_confidence, 2),
                "mood_distribution": mood_distribution,
                "avg_urgency": round(urgency_avg, 1),
                "total_bi_insights": len(bi_logs),
            }

        except Exception as e:
            logger.error(f"❌ Error getting quality metrics: {e}")
            return {
                "period_days": days,
                "error": str(e),
            }

    def _count_distribution(self, values: List[str]) -> Dict[str, int]:
        """Conta distribuição de valores"""
        distribution = {}
        for value in values:
            distribution[value] = distribution.get(value, 0) + 1
        return distribution


# Import timedelta for metrics
from datetime import timedelta
