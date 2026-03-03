"""
👥 Behavior Agent - Agente de Análise Comportamental

Analisa padrões comportamentais do cliente:
- Padrões de comunicação (frequência, horário, tom)
- Histórico de interações
- Preferências implícitas
- Comportamentos de risco (churn)
- Comportamentos de oportunidade (upsell)

Baseado em:
- Behavioral Economics (Kahneman)
- Nudge Theory
- Pattern Recognition
- Customer Journey Analysis

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from .base_agent import BaseAgent, AgentContext, AgentResult


class BehaviorAgent(BaseAgent):
    """Agente de análise comportamental"""
    
    # Padrões de comportamento
    BEHAVIOR_PATTERNS = {
        "impulsivo": ["agora", "já", "ja", "hoje", "urgente", "preciso", "rápido"],
        "reflexivo": ["penso", "acho", "talvez", "verificar", "ver", "analisar", "pesquisar"],
        "economico": ["preço", "valor", "desconto", "promoção", "barato", "caro", "pagamento"],
        "qualidade": ["qualidade", "bom", "melhor", "excelente", "profissional", "resultado"],
        "conveniencia": ["perto", "local", "horário", "rápido", "prático", "facilidade"],
        "social": ["recomendam", "indicam", "amigas", "conhecem", "famoso", "popular"],
    }
    
    # Sinais de churn
    CHURN_SIGNALS = [
        "não volto", "nao volto", "não gostei", "nao gostei", "decepcionada",
        "demora", "demorado", "ruim", "péssimo", "horrível", "nunca mais",
        "outra", "outra", "concorrente", "trocar", "mudar",
    ]
    
    # Sinais de fidelidade
    LOYALTY_SIGNALS = [
        "sempre", "todo", "toda", "frequente", "costumo", "habitual",
        "amo", "adoro", "gosto", "recomendo", "indico", "volto",
        "amiga", "conhecida", "trago", "indicar",
    ]
    
    def get_name(self) -> str:
        return "BehaviorAgent"
    
    def get_expertise(self) -> str:
        return "Análise comportamental: padrões, churn, fidelidade, jornada"
    
    def analyze(self, context: AgentContext) -> AgentResult:
        start_time = time.time()
        errors = []
        
        try:
            client_messages = [m.get("content", "") for m in context.messages if m.get("direction") == "inbound"]
            full_text = " ".join(client_messages).lower()
            
            behavior_data = {
                "behavior_patterns": self._identify_behavior_patterns(full_text),
                "churn_risk": self._analyze_churn_risk(full_text, client_messages),
                "loyalty_indicators": self._analyze_loyalty(full_text, client_messages),
                "communication_patterns": self._analyze_communication_patterns(client_messages),
                "decision_making_style": self._analyze_decision_style(full_text),
                "customer_journey_stage": self._identify_journey_stage(context, client_messages),
            }
            
            confidence = self._calculate_confidence(behavior_data, len(client_messages))
            processing_time = int((time.time() - start_time) * 1000)
            
            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=behavior_data,
                confidence=confidence,
                processing_time_ms=processing_time,
                errors=errors,
            )
            
        except Exception as e:
            errors.append(str(e))
            return AgentResult(
                agent_name=self.get_name(),
                success=False,
                data={},
                confidence=0.0,
                processing_time_ms=int((time.time() - start_time) * 1000),
                errors=errors,
            )
    
    def _identify_behavior_patterns(self, text: str) -> Dict:
        patterns_found = {}
        
        for pattern, keywords in self.BEHAVIOR_PATTERNS.items():
            score = sum(text.count(kw) for kw in keywords)
            if score > 0:
                patterns_found[pattern] = {
                    "score": score,
                    "strength": "forte" if score > 3 else "média" if score > 1 else "fraca",
                }
        
        dominant_pattern = max(patterns_found, key=lambda x: patterns_found[x]["score"]) if patterns_found else "indeterminado"
        
        return {
            "patterns": patterns_found,
            "dominant_pattern": dominant_pattern,
            "total_patterns": len(patterns_found),
        }
    
    def _analyze_churn_risk(self, text: str, messages: List[str]) -> Dict:
        churn_signals_found = [signal for signal in self.CHURN_SIGNALS if signal in text]
        
        # Calcular risco
        risk_score = len(churn_signals_found) * 20  # Cada sinal = 20% de risco
        risk_score = min(100, risk_score)
        
        # Fatores adicionais
        negative_sentiment = text.count("não") + text.count("nao")
        if negative_sentiment > 5:
            risk_score = min(100, risk_score + 20)
        
        return {
            "signals": churn_signals_found,
            "risk_score": risk_score,
            "risk_level": "alto" if risk_score > 60 else "médio" if risk_score > 30 else "baixo",
            "recommendations": self._get_churn_prevention(recommendations=[] if risk_score < 30 else ["high_risk"]),
        }
    
    def _get_churn_prevention(self, recommendations: List[str]) -> List[str]:
        base_recommendations = [
            "Oferecer atendimento personalizado",
            "Apresentar soluções para dores mencionadas",
            "Oferecer benefício exclusivo",
            "Agendar follow-up em 24-48h",
        ]
        return base_recommendations
    
    def _analyze_loyalty(self, text: str, messages: List[str]) -> Dict:
        loyalty_signals_found = [signal for signal in self.LOYALTY_SIGNALS if signal in text]
        
        loyalty_score = len(loyalty_signals_found) * 15
        loyalty_score = min(100, loyalty_score)
        
        # Cliente recorrente?
        recurrent_words = ["sempre", "todo", "toda", "frequente", "costumo"]
        is_recurrent = any(word in text for word in recurrent_words)
        
        return {
            "signals": loyalty_signals_found,
            "loyalty_score": loyalty_score,
            "loyalty_level": "alto" if loyalty_score > 60 else "médio" if loyalty_score > 30 else "baixo",
            "is_recurrent": is_recurrent,
            "advocacy_potential": "alto" if len(loyalty_signals_found) > 3 else "médio" if len(loyalty_signals_found) > 1 else "baixo",
        }
    
    def _analyze_communication_patterns(self, messages: List[str]) -> Dict:
        if not messages:
            return {}
        
        # Frequência de mensagens
        message_count = len(messages)
        
        # Tamanho médio
        avg_length = sum(len(msg) for msg in messages) / message_count if message_count > 0 else 0
        
        # Uso de emojis
        emoji_count = sum(msg.count(e) for msg in messages for e in "😊😍🥰😂😅😢😡🤔👍❤️🔥")
        
        # Uso de pontos de interrogação
        question_count = sum(msg.count("?") for msg in messages)
        
        # Horário (se tiver timestamp)
        # Simplificado para este exemplo
        
        return {
            "message_count": message_count,
            "avg_message_length": avg_length,
            "emoji_usage": emoji_count,
            "question_count": question_count,
            "communication_style": "detalhado" if avg_length > 50 else "objetivo" if avg_length < 20 else "equilibrado",
            "engagement_level": "alto" if message_count > 10 else "médio" if message_count > 5 else "baixo",
        }
    
    def _analyze_decision_style(self, text: str) -> Dict:
        # Rápido vs Lento (Kahneman)
        fast_thinking = ["agora", "já", "ja", "quero", "faço", "agora", "hoje"]
        slow_thinking = ["penso", "acho", "talvez", "verificar", "analisar", "pesquisar"]
        
        fast_score = sum(text.count(kw) for kw in fast_thinking)
        slow_score = sum(text.count(kw) for kw in slow_thinking)
        
        decision_style = "rápido" if fast_score > slow_score else "refletido" if slow_score > fast_score else "equilibrado"
        
        return {
            "fast_thinking_score": fast_score,
            "slow_thinking_score": slow_score,
            "decision_style": decision_style,
            "recommendation": "Apresente opções claras e diretas" if decision_style == "rápido" else "Forneça informações detalhadas para decisão",
        }
    
    def _identify_journey_stage(self, context: AgentContext, messages: List[str]) -> Dict:
        # Estágios da jornada do cliente
        stages = {
            "primeiro_contato": len(messages) < 5,
            "exploracao": any(kw in " ".join(messages) for kw in ["o que", "como", "quais", "informações"]),
            "consideracao": any(kw in " ".join(messages) for kw in ["preço", "valor", "agendar", "horário"]),
            "decisao": any(kw in " ".join(messages) for kw in ["fechar", "confirmar", "faço", "quero"]),
            "fidelizacao": any(kw in " ".join(messages) for kw in ["sempre", "volto", "recomendo", "adoro"]),
        }
        
        current_stage = max(stages, key=lambda x: stages[x]) if any(stages.values()) else "desconhecido"
        
        return {
            "stage": current_stage,
            "stage_characteristics": stages,
            "next_stage": self._recommend_next_journey_stage(current_stage),
        }
    
    def _recommend_next_journey_stage(self, current_stage: str) -> str:
        next_stages = {
            "primeiro_contato": "exploracao",
            "exploracao": "consideracao",
            "consideracao": "decisao",
            "decisao": "fidelizacao",
            "fidelizacao": "advocacy",
            "desconhecido": "exploracao",
        }
        return next_stages.get(current_stage, "exploracao")
    
    def _calculate_confidence(self, behavior_data: Dict, message_count: int) -> float:
        factors = []
        
        # Mais mensagens = mais confiança
        factors.append(min(1.0, message_count / 10))
        
        # Padrões detectados
        patterns = behavior_data.get("behavior_patterns", {})
        factors.append(min(1.0, patterns.get("total_patterns", 0) / 3))
        
        # Sinais de churn/loyalty detectados
        churn = behavior_data.get("churn_risk", {})
        loyalty = behavior_data.get("loyalty_indicators", {})
        factors.append(1.0 if churn.get("signals") or loyalty.get("signals") else 0.5)
        
        return self._calculate_confidence(factors)
