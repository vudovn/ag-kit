"""
🧠 LUNA Multi-Brain Router v2

Intelligent routing between multiple AI brains based on contact DNA, intent, risk, and context.

Feature Flag: FEATURE_MULTI_BRAIN_V2

Usage:
    from brain.multi_brain_router import MultiBrainRouter
    
    router = MultiBrainRouter()
    
    # Route request to best brain
    brain = router.route_request(conversation)
    
    # Get response from selected brain
    response = router.get_response(brain, conversation)
"""

import os
import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib


class BrainType(Enum):
    """Available AI brain types"""
    QUICK = "quick"           # Haiku - Triagem, extração ($0.25/M, ~50ms)
    STANDARD = "standard"     # Sonnet 4.6 - Vendas, chat ($5-8/M, ~300ms)
    COMPLEX = "complex"       # Opus 4.6 - Crises, reclamações ($15/M, ~500ms)


# Model Routing Strategy (from docs/luna_os/MODEL_ROUTING_STRATEGY.md)
MODEL_ROUTING = {
    # Quick Brain (Haiku) - Triagem, extração
    "triage": BrainType.QUICK,
    "intent_detection": BrainType.QUICK,
    "sentiment_analysis": BrainType.QUICK,
    "intelligence_extraction": BrainType.QUICK,
    "field_extraction": BrainType.QUICK,
    "guardrails": BrainType.QUICK,
    "saudacao": BrainType.QUICK,

    # Standard Brain (Sonnet 4.6) - Vendas, chat, relacionamento
    "resolution": BrainType.STANDARD,
    "voice_response": BrainType.STANDARD,
    "chat_normal": BrainType.STANDARD,
    "upsell": BrainType.STANDARD,
    "agendamento": BrainType.STANDARD,
    "objecao_simples": BrainType.STANDARD,
    "followup": BrainType.STANDARD,
    "relacionamento": BrainType.STANDARD,

    # Complex Brain (Opus 4.6) - Crises, reclamações
    "reclamacao": BrainType.COMPLEX,
    "crise": BrainType.COMPLEX,
    "procon": BrainType.COMPLEX,
    "handoff": BrainType.COMPLEX,
    "reembolso": BrainType.COMPLEX,
    "dojo_analysis": BrainType.COMPLEX,
    "edge_case_generation": BrainType.COMPLEX,
}

# Custo por 1K tokens (OpenRouter)
MODEL_COSTS = {
    BrainType.QUICK: 0.00025,      # $0.25/M tokens
    BrainType.STANDARD: 0.000008,  # $5-8/M tokens (avg)
    BrainType.COMPLEX: 0.000015,   # $15/M tokens
}

# Latência estimada (ms)
MODEL_LATENCY = {
    BrainType.QUICK: 50,
    BrainType.STANDARD: 300,
    BrainType.COMPLEX: 500,
}


@dataclass
class BrainDecision:
    """Decision about which brain to use"""
    brain: BrainType
    confidence: float
    reason: str
    alternative_brains: List[BrainType]
    estimated_cost: float
    estimated_latency: float
    contact_dna_factor: bool
    risk_factor: bool
    intent_factor: bool


class MultiBrainRouter:
    """
    Intelligent Multi-Brain Router.
    
    Features:
    - Route based on contact DNA
    - Route based on intent complexity
    - Route based on risk score
    - Route based on LTV
    - Cost optimization
    - Latency optimization
    - Cache brain decisions
    
    Usage:
        router = MultiBrainRouter()
        decision = router.route_request(conversation)
        response = router.get_response(decision.brain, conversation)
    """
    
    def __init__(self):
        """Initialize Multi-Brain Router"""
        # Brain configurations
        self.brain_configs = {
            BrainType.QUICK: {
                "model": os.getenv("MULTI_BRAIN_QUICK", "haiku"),
                "cost_per_1k": 0.00025,
                "avg_latency_ms": 200,
                "max_tokens": 4096
            },
            BrainType.STANDARD: {
                "model": os.getenv("MULTI_BRAIN_STANDARD", "sonnet"),
                "cost_per_1k": 0.003,
                "avg_latency_ms": 500,
                "max_tokens": 4096
            },
            BrainType.COMPLEX: {
                "model": os.getenv("MULTI_BRAIN_COMPLEX", "opus"),
                "cost_per_1k": 0.015,
                "avg_latency_ms": 1000,
                "max_tokens": 4096
            }
        }
        
        # Thresholds
        self.vip_ltv_threshold = float(os.getenv("MULTI_BRAIN_VIP_LTV", "10000"))
        self.high_risk_threshold = float(os.getenv("MULTI_BRAIN_HIGH_RISK", "0.7"))
        self.low_confidence_threshold = float(os.getenv("MULTI_BRAIN_LOW_CONFIDENCE", "0.5"))
        
        # Cache for brain decisions
        self._decision_cache: Dict[str, Tuple[BrainDecision, float]] = {}
        self._cache_ttl = 60  # 1 minute
    
    def route_request(self, conversation: Dict[str, Any]) -> BrainDecision:
        """
        Route request to best brain based on intent, risk, LTV, and context.

        Args:
            conversation: Conversation data with contact, intent, risk, etc.

        Returns:
            BrainDecision with selected brain and reasoning
        """
        # Check cache first
        cache_key = self._create_cache_key(conversation)
        cached = self._get_cached_decision(cache_key)
        if cached:
            return cached

        # Extract factors
        contact = conversation.get("contact", {})
        intent = conversation.get("intent", "unknown")
        intent_confidence = conversation.get("intent_confidence", 1.0)
        risk_score = conversation.get("risk_score", 0.0)
        ltv = contact.get("ltv", 0)
        complexity = conversation.get("complexity", "medium")

        # Get contact DNA if available
        dna_factor = False
        if "behavioral_dna" in contact:
            dna_factor = True

        # STRATEGY 1: Intent-based routing (from MODEL_ROUTING)
        if intent.lower() in MODEL_ROUTING:
            selected_brain = MODEL_ROUTING[intent.lower()]
            confidence = 0.9  # High confidence for explicit routing
            reason = f"Intent '{intent}' mapped to {selected_brain.value} brain"
        else:
            # STRATEGY 2: Score-based routing (fallback)
            scores = self._calculate_brain_scores(conversation)
            selected_brain = max(scores, key=scores.get)
            confidence = scores[selected_brain] / sum(scores.values()) if sum(scores.values()) > 0 else 0.5
            reason = self._explain_decision(selected_brain, scores, conversation)

        # Create decision
        decision = BrainDecision(
            brain=selected_brain,
            confidence=confidence,
            reason=reason,
            alternative_brains=self._get_alternatives(selected_brain, {}),
            estimated_cost=MODEL_COSTS[selected_brain],
            estimated_latency=MODEL_LATENCY[selected_brain],
            contact_dna_factor=dna_factor,
            risk_factor=risk_score > 0.5,
            intent_factor=True
        )

        # Cache decision
        self._cache_decision(cache_key, decision)

        return decision
    
    def get_response(
        self,
        brain: BrainType,
        conversation: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get response from selected brain.
        
        Args:
            brain: Selected brain type
            conversation: Conversation data
            **kwargs: Additional parameters for brain API
            
        Returns:
            Response from brain
        """
        # In production, this would call the actual brain API
        # For now, return mock response
        
        config = self.brain_configs[brain]
        
        return {
            "brain": brain.value,
            "model": config["model"],
            "response": f"[{brain.value.upper()}] Response to: {conversation.get('messages', [{'text': ''}])[-1].get('text', '')}",
            "tokens_used": 150,
            "cost": config["cost_per_1k"] * 0.15,
            "latency_ms": config["avg_latency_ms"],
            "timestamp": time.time()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics"""
        return {
            "cached_decisions": len(self._decision_cache),
            "brain_configs": {
                brain.value: config["model"]
                for brain, config in self.brain_configs.items()
            },
            "thresholds": {
                "vip_ltv": self.vip_ltv_threshold,
                "high_risk": self.high_risk_threshold,
                "low_confidence": self.low_confidence_threshold
            }
        }
    
    def _create_cache_key(self, conversation: Dict[str, Any]) -> str:
        """Create cache key from conversation"""
        key_data = f"{conversation.get('contact', {}).get('id')}:{conversation.get('intent')}:{conversation.get('risk_score')}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached_decision(self, cache_key: str) -> Optional[BrainDecision]:
        """Get cached decision if not expired"""
        if cache_key in self._decision_cache:
            decision, timestamp = self._decision_cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                return decision
            else:
                del self._decision_cache[cache_key]
        return None
    
    def _cache_decision(self, cache_key: str, decision: BrainDecision):
        """Cache brain decision"""
        self._decision_cache[cache_key] = (decision, time.time())
    
    def _explain_decision(
        self,
        selected_brain: BrainType,
        scores: Dict[BrainType, float],
        conversation: Dict[str, Any]
    ) -> str:
        """Explain why this brain was selected"""
        reasons = []
        
        contact = conversation.get("contact", {})
        ltv = contact.get("ltv", 0)
        risk = conversation.get("risk_score", 0)
        complexity = conversation.get("complexity", "medium")
        
        if selected_brain == BrainType.QUICK:
            reasons.append("Rotina simples")
            if complexity == "simple":
                reasons.append("baixa complexidade")
        elif selected_brain == BrainType.COMPLEX:
            reasons.append("Caso sensível")
            if ltv > self.vip_ltv_threshold:
                reasons.append("cliente VIP")
            if risk > self.high_risk_threshold:
                reasons.append("alto risco")
        else:
            reasons.append("Chat normal")
        
        return f"{selected_brain.value}: {', '.join(reasons)}"
    
    def _get_alternatives(
        self,
        selected: BrainType,
        scores: Dict[BrainType, float]
    ) -> List[BrainType]:
        """Get alternative brains sorted by score"""
        sorted_brains = sorted(scores.keys(), key=lambda b: scores[b], reverse=True)
        return [b for b in sorted_brains if b != selected]


# Global singleton
multi_brain_router = MultiBrainRouter()


def get_multi_brain_router() -> MultiBrainRouter:
    """Get global router instance"""
    return multi_brain_router


# Feature flag check
def is_multi_brain_enabled() -> bool:
    """Check if multi-brain feature is enabled"""
    return os.getenv("FEATURE_MULTI_BRAIN_V2", "false").lower() == "true"


# Convenience functions
def route_to_brain(conversation: Dict[str, Any]) -> BrainDecision:
    """Route conversation to best brain"""
    if not is_multi_brain_enabled():
        # Default to standard if feature disabled
        return BrainDecision(
            brain=BrainType.STANDARD,
            confidence=1.0,
            reason="Multi-brain disabled",
            alternative_brains=[],
            estimated_cost=0,
            estimated_latency=0,
            contact_dna_factor=False,
            risk_factor=False,
            intent_factor=False
        )
    return multi_brain_router.route_request(conversation)
