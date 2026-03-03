"""
LUNA Learning Engine — Aprendizado Contínuo
Padrão Kimi-SWE: Feedback Loop com Golden Examples e Auto-Regras.

Mecanismos:
  A. Captura de correções (diff handoff vs LUNA)
  B. Golden examples (conversas que converteram)
  C. Auto-geração de regras (3+ correções = nova regra)
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from loguru import logger


# ═══════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════


@dataclass
class LearningPattern:
    """Padrão aprendido de uma interação."""

    pattern_type: str  # "correction", "golden", "violation"
    trigger_text: str
    wrong_response: Optional[str] = None
    correct_response: Optional[str] = None
    intent: Optional[str] = None
    phone: Optional[str] = None
    conversation_id: Optional[str] = None
    times_applied: int = 0

    def to_dict(self) -> Dict:
        return {
            "pattern_type": self.pattern_type,
            "trigger_text": self.trigger_text,
            "wrong_response": self.wrong_response,
            "correct_response": self.correct_response,
            "intent": self.intent,
            "phone": self.phone,
            "conversation_id": self.conversation_id,
            "times_applied": self.times_applied,
        }


class LearningEngine:
    """
    Motor de Aprendizado Contínuo.
    Aprende com cada handoff, cada conversão e cada violação.
    """

    def __init__(self):
        self._db = None

    def _get_db(self):
        if self._db is None:
            try:
                from app.integrations.supabase_client import get_supabase

                self._db = get_supabase()
            except Exception as e:
                logger.warning(f"LearningEngine: Supabase indisponível: {e}")
        return self._db

    # ═══════════════════════════════════════════════
    # A. CAPTURA DE CORREÇÕES
    # ═══════════════════════════════════════════════

    async def capture_correction(
        self,
        phone: str,
        conversation_id: str,
        luna_response: str,
        human_response: str,
        trigger_message: str,
        intent: str = None,
    ):
        """
        Captura a diferença entre o que LUNA disse e o que o humano corrigiu.
        Chamado automaticamente quando um handoff acontece e o operador responde.
        """
        log = logger.bind(phone=phone, module="learning")

        # Só salvar se as respostas forem significativamente diferentes
        if self._responses_are_similar(luna_response, human_response):
            log.debug("Respostas similares — correção ignorada")
            return

        pattern = LearningPattern(
            pattern_type="correction",
            trigger_text=trigger_message,
            wrong_response=luna_response,
            correct_response=human_response,
            intent=intent,
            phone=phone,
            conversation_id=conversation_id,
        )

        await self._save_pattern(pattern)
        log.info(
            f"📝 Correção capturada | trigger='{trigger_message[:50]}...' | "
            f"LUNA→'{luna_response[:40]}...' vs Humano→'{human_response[:40]}...'"
        )

        # Verificar se atingiu threshold para auto-regra
        await self._check_auto_rule_threshold(pattern)

    # ═══════════════════════════════════════════════
    # B. GOLDEN EXAMPLES
    # ═══════════════════════════════════════════════

    async def mark_golden_example(
        self,
        phone: str,
        conversation_id: str,
        messages: List[Dict],
        intent: str = None,
    ):
        """
        Marca uma conversa que teve conversão positiva como golden example.
        Chamado quando `conversion_result == 'booked'` ou equivalente.
        """
        log = logger.bind(phone=phone, module="learning")

        # Extrair trigger (primeira pergunta do cliente)
        client_messages = [m for m in messages if m.get("role") == "user"]
        if not client_messages:
            return

        trigger = client_messages[0].get("content", "")

        # Extrair a melhor resposta da LUNA (a que levou à conversão)
        luna_messages = [m for m in messages if m.get("role") == "assistant"]
        best_response = luna_messages[-1].get("content", "") if luna_messages else ""

        pattern = LearningPattern(
            pattern_type="golden",
            trigger_text=trigger,
            correct_response=best_response,
            intent=intent,
            phone=phone,
            conversation_id=conversation_id,
        )

        await self._save_pattern(pattern)
        log.info(f"⭐ Golden example salvo | intent={intent}")

    # ═══════════════════════════════════════════════
    # C. AUTO-GERAÇÃO DE REGRAS
    # ═══════════════════════════════════════════════

    async def _check_auto_rule_threshold(self, new_pattern: LearningPattern):
        """
        Verifica se há 3+ correções do mesmo tipo.
        Se sim, gera uma regra automática.
        """
        db = self._get_db()
        if not db:
            return

        log = logger.bind(module="learning_auto_rules")

        try:
            # Buscar correções similares (mesmo intent)
            similar = (
                db.table("learning_patterns")
                .select("*")
                .eq("pattern_type", "correction")
                .eq("intent", new_pattern.intent or "unknown")
                .eq("active", True)
                .execute()
            )

            count = len(similar.data or [])

            if count >= 3:
                log.warning(
                    f"🔄 AUTO-REGRA ativada | {count} correções do tipo "
                    f"'{new_pattern.intent}' detectadas"
                )

                # Gerar regra (salvar como pattern tipo "auto_rule")
                auto_rule = LearningPattern(
                    pattern_type="auto_rule",
                    trigger_text=f"Auto-regra para intent '{new_pattern.intent}'",
                    wrong_response=new_pattern.wrong_response,
                    correct_response=f"Padrão corrigido {count}x por operadores humanos",
                    intent=new_pattern.intent,
                )

                await self._save_pattern(auto_rule)

        except Exception as e:
            log.error(f"Erro ao verificar threshold: {e}")

    # ═══════════════════════════════════════════════
    # D. ENRIQUECIMENTO DO CONTEXTO
    # ═══════════════════════════════════════════════

    async def get_relevant_patterns(
        self,
        message: str,
        intent: str = None,
        limit: int = 3,
    ) -> List[Dict]:
        """
        Busca padrões relevantes (golden examples + correções) para enriquecer
        o contexto do LLM como few-shot examples.
        """
        db = self._get_db()
        if not db:
            return []

        try:
            # Buscar golden examples e auto_rules do mesmo intent
            query = (
                db.table("learning_patterns")
                .select("trigger_text, correct_response, pattern_type, times_applied")
                .in_("pattern_type", ["golden", "auto_rule"])
                .eq("active", True)
                .order("times_applied", desc=True)
                .limit(limit)
            )

            if intent:
                query = query.eq("intent", intent)

            result = query.execute()
            patterns = result.data or []

            # Incrementar times_applied para tracking
            for p in patterns:
                try:
                    db.table("learning_patterns").update(
                        {"times_applied": (p.get("times_applied", 0) or 0) + 1}
                    ).eq("trigger_text", p["trigger_text"]).execute()
                except Exception:
                    pass

            return patterns

        except Exception as e:
            logger.bind(module="learning").error(f"Erro ao buscar padrões: {e}")
            return []

    # ═══════════════════════════════════════════════
    # UTILS
    # ═══════════════════════════════════════════════

    def _responses_are_similar(self, a: str, b: str, threshold: float = 0.7) -> bool:
        """
        Verificação simples de similaridade por token overlap.
        Se > threshold, considera as respostas similares (não precisa salvar).
        """
        if not a or not b:
            return False

        tokens_a = set(a.lower().split())
        tokens_b = set(b.lower().split())

        if not tokens_a or not tokens_b:
            return False

        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b

        jaccard = len(intersection) / len(union)
        return jaccard >= threshold

    async def _save_pattern(self, pattern: LearningPattern):
        """Persiste padrão no Supabase."""
        db = self._get_db()
        if not db:
            logger.warning(
                "LearningEngine: Não foi possível salvar padrão (DB offline)"
            )
            return

        try:
            entry = {
                **pattern.to_dict(),
                "active": True,
                "created_at": datetime.utcnow().isoformat(),
            }
            db.table("learning_patterns").insert(entry).execute()
        except Exception as e:
            logger.error(f"Erro ao salvar learning pattern: {e}")


# ═══════════════════════════════════════════════
# CONFIDENCE SCORE
# ═══════════════════════════════════════════════


def calculate_confidence(
    intent_confidence: float,
    guardrail_penalty: float,
    data_completeness: float = 0.5,
    has_learning_match: bool = False,
) -> float:
    """
    Calcula score composto de confiança para a resposta.

    Pesos:
      - intent_confidence (40%): confiança da classificação de intenção
      - guardrail_penalty (30%): penalidade dos guardrails (0.0 = ok, 1.0 = fail total)
      - data_completeness (20%): campos extraídos / campos necessários
      - learning_match (10%): resposta similar já foi aprovada em golden example

    Returns:
        float entre 0.0 e 1.0
    """
    guardrail_score = max(0.0, 1.0 - guardrail_penalty)
    learning_bonus = 1.0 if has_learning_match else 0.5

    score = (
        (intent_confidence * 0.40)
        + (guardrail_score * 0.30)
        + (data_completeness * 0.20)
        + (learning_bonus * 0.10)
    )

    return round(min(1.0, max(0.0, score)), 3)


def decide_action(confidence_score: float) -> str:
    """
    Decide ação baseada no score de confiança.

    Returns:
        "send" | "send_flagged" | "escalate"
    """
    if confidence_score >= 0.85:
        return "send"  # Envia automaticamente
    elif confidence_score >= 0.60:
        return "send_flagged"  # Envia + flag no dashboard
    else:
        return "escalate"  # Não envia, handoff automático


# Singleton
learning = LearningEngine()
