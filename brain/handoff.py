"""
🤝 LUNA Human Handoff System

Intelligent handoff from AI to human operators.
Ensures no customer is abandoned and complex cases get human attention.

Feature Flag: FEATURE_HANDOFF
"""

import os
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class HandoffMode(Enum):
    """Operational mode for conversation"""
    AI_ACTIVE = "ai_active"           # AI handles everything
    AI_ASSISTED = "ai_assisted"       # AI suggests, human approves
    HUMAN_ACTIVE = "human_active"     # Human handles everything
    PAUSED = "paused"                 # Conversation paused


class HandoffReason(Enum):
    """Reasons for triggering handoff"""
    CUSTOMER_REQUESTED = "customer_requested"
    LOW_CONFIDENCE = "low_confidence"
    HIGH_RISK = "high_risk"
    COMPLAINT_DETECTED = "complaint_detected"
    EXCEPTION_DETECTED = "exception_detected"
    MULTIPLE_FAILURES = "multiple_failures"
    VIP_CUSTOMER = "vip_customer"
    COMPLEX_QUERY = "complex_query"
    MANUAL = "manual"


@dataclass
class HandoffRequest:
    """Handoff request data structure"""
    conversation_id: str
    contact_id: str
    reason: HandoffReason
    priority: int  # 1-10, 10 = highest
    context_summary: str
    ai_attempts: int
    last_ai_response: Optional[str]
    customer_messages: List[str]
    requested_at: float = field(default_factory=time.time)
    accepted_by: Optional[str] = None  # Human operator ID
    accepted_at: Optional[float] = None
    resolved_at: Optional[float] = None
    resolution_notes: Optional[str] = None
    
    def is_accepted(self) -> bool:
        return self.accepted_at is not None
    
    def is_resolved(self) -> bool:
        return self.resolved_at is not None
    
    def time_since_request(self) -> float:
        return time.time() - self.requested_at
    
    def time_to_accept(self) -> Optional[float]:
        if self.accepted_at:
            return self.accepted_at - self.requested_at
        return None


class HandoffEngine:
    """
    Human Handoff Engine for LUNA.
    
    Features:
    - Automatic handoff detection
    - Priority-based routing
    - Context preservation
    - SLA monitoring
    - Feedback collection
    
    Usage:
        handoff = HandoffEngine()
        
        # Check if handoff needed
        if handoff.should_handoff(conversation):
            request = handoff.create_handoff(conversation)
            handoff.notify_humans(request)
    """
    
    def __init__(self):
        self._pending_requests: Dict[str, HandoffRequest] = {}
        self._resolved_requests: List[HandoffRequest] = []
        self._handoff_counts = {reason: 0 for reason in HandoffReason}
        
        # Thresholds (configurable)
        self.confidence_threshold = float(
            os.getenv("HANDOFF_CONFIDENCE_THRESHOLD", "0.5")
        )
        self.max_ai_failures = int(
            os.getenv("HANDOFF_MAX_AI_FAILURES", "2")
        )
        self.vip_ltv_threshold = float(
            os.getenv("HANDOFF_VIP_LTV_THRESHOLD", "10000")
        )
    
    def should_handoff(self, conversation: Dict[str, Any]) -> tuple[bool, Optional[HandoffReason]]:
        """
        Determine if conversation should be handed off to human.
        
        Args:
            conversation: Conversation data with context, messages, scores
            
        Returns:
            Tuple of (should_handoff, reason)
        """
        # Check conversation mode
        mode = conversation.get("mode", HandoffMode.AI_ACTIVE.value)
        if mode == HandoffMode.HUMAN_ACTIVE.value:
            return True, HandoffReason.MANUAL
        
        # Check for explicit customer request
        if self._customer_requested_handoff(conversation):
            return True, HandoffReason.CUSTOMER_REQUESTED
        
        # Check confidence score
        confidence = conversation.get("intent_confidence", 1.0)
        if confidence < self.confidence_threshold:
            return True, HandoffReason.LOW_CONFIDENCE
        
        # Check risk score
        risk = conversation.get("risk_score", 0.0)
        if risk > 0.7:
            return True, HandoffReason.HIGH_RISK
        
        # Check for complaints
        if self._complaint_detected(conversation):
            return True, HandoffReason.COMPLAINT_DETECTED
        
        # Check AI failure count
        failures = conversation.get("ai_failure_count", 0)
        if failures >= self.max_ai_failures:
            return True, HandoffReason.MULTIPLE_FAILURES
        
        # Check VIP status
        contact = conversation.get("contact", {})
        ltv = contact.get("ltv", 0)
        if ltv > self.vip_ltv_threshold:
            return True, HandoffReason.VIP_CUSTOMER
        
        # No handoff needed
        return False, None
    
    def create_handoff(
        self,
        conversation: Dict[str, Any],
        reason: HandoffReason,
        priority: Optional[int] = None
    ) -> HandoffRequest:
        """
        Create handoff request.
        
        Args:
            conversation: Conversation data
            reason: Handoff reason
            priority: Manual priority override (1-10)
            
        Returns:
            HandoffRequest object
        """
        # Calculate priority if not provided
        if priority is None:
            priority = self._calculate_priority(reason, conversation)
        
        # Extract context
        contact = conversation.get("contact", {})
        messages = conversation.get("messages", [])
        
        request = HandoffRequest(
            conversation_id=conversation.get("id", "unknown"),
            contact_id=contact.get("id", "unknown"),
            reason=reason,
            priority=priority,
            context_summary=self._summarize_context(conversation),
            ai_attempts=conversation.get("ai_attempts", 0),
            last_ai_response=conversation.get("last_ai_response"),
            customer_messages=[m.get("text", "") for m in messages[-5:]]
        )
        
        # Store request
        self._pending_requests[request.conversation_id] = request
        self._handoff_counts[reason] = self._handoff_counts.get(reason, 0) + 1
        
        return request
    
    def accept_handoff(self, conversation_id: str, operator_id: str) -> bool:
        """
        Accept handoff request.
        
        Args:
            conversation_id: Conversation to accept
            operator_id: Human operator accepting
            
        Returns:
            True if accepted successfully
        """
        request = self._pending_requests.get(conversation_id)
        if not request:
            return False
        
        request.accepted_by = operator_id
        request.accepted_at = time.time()
        
        return True
    
    def resolve_handoff(
        self,
        conversation_id: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Resolve handoff request.
        
        Args:
            conversation_id: Conversation to resolve
            notes: Resolution notes
            
        Returns:
            True if resolved successfully
        """
        request = self._pending_requests.pop(conversation_id, None)
        if not request:
            return False
        
        request.resolved_at = time.time()
        request.resolution_notes = notes
        self._resolved_requests.append(request)
        
        return True
    
    def get_pending_requests(self) -> List[HandoffRequest]:
        """Get all pending handoff requests sorted by priority"""
        return sorted(
            self._pending_requests.values(),
            key=lambda r: (-r.priority, r.requested_at)
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get handoff statistics"""
        total = len(self._pending_requests) + len(self._resolved_requests)
        
        return {
            "pending": len(self._pending_requests),
            "resolved": len(self._resolved_requests),
            "total": total,
            "by_reason": dict(self._handoff_counts),
            "avg_time_to_accept": self._avg_time_to_accept(),
            "thresholds": {
                "confidence": self.confidence_threshold,
                "max_failures": self.max_ai_failures,
                "vip_ltv": self.vip_ltv_threshold
            }
        }
    
    def _customer_requested_handoff(self, conversation: Dict) -> bool:
        """Check if customer explicitly requested human"""
        messages = conversation.get("messages", [])
        recent = messages[-3:]  # Last 3 messages
        
        request_phrases = [
            "quero falar com atendente",
            "falar com humano",
            "atendente humano",
            "quero pessoa",
            "falar com pessoa",
            "humano por favor",
            "atendente real"
        ]
        
        for msg in recent:
            text = msg.get("text", "").lower()
            if any(phrase in text for phrase in request_phrases):
                return True
        
        return False
    
    def _complaint_detected(self, conversation: Dict) -> bool:
        """Check for complaint indicators"""
        messages = conversation.get("messages", [])
        recent = messages[-3:]
        
        complaint_words = [
            "reclamação", "reclamar", "inaceitável", "absurdo",
            "péssimo", "horrível", "nunca mais", "cancelar",
            "processo", "procon", "direitos"
        ]
        
        for msg in recent:
            text = msg.get("text", "").lower()
            if any(word in text for word in complaint_words):
                return True
        
        return False
    
    def _calculate_priority(
        self,
        reason: HandoffReason,
        conversation: Dict
    ) -> int:
        """Calculate handoff priority (1-10)"""
        base_priority = {
            HandoffReason.COMPLAINT_DETECTED: 9,
            HandoffReason.HIGH_RISK: 8,
            HandoffReason.VIP_CUSTOMER: 8,
            HandoffReason.CUSTOMER_REQUESTED: 6,
            HandoffReason.MULTIPLE_FAILURES: 6,
            HandoffReason.LOW_CONFIDENCE: 4,
            HandoffReason.EXCEPTION_DETECTED: 7,
            HandoffReason.COMPLEX_QUERY: 5,
            HandoffReason.MANUAL: 5
        }
        
        priority = base_priority.get(reason, 5)
        
        # Adjust for VIP
        contact = conversation.get("contact", {})
        if contact.get("ltv", 0) > self.vip_ltv_threshold:
            priority = min(10, priority + 2)
        
        return priority
    
    def _summarize_context(self, conversation: Dict) -> str:
        """Create context summary for human"""
        contact = conversation.get("contact", {})
        messages = conversation.get("messages", [])
        
        summary_parts = [
            f"Contato: {contact.get('name', 'Unknown')}",
            f"Intent: {conversation.get('intent', 'unknown')}",
            f"Confiança: {conversation.get('intent_confidence', 0):.0%}",
            f"Mensagens: {len(messages)}"
        ]
        
        return " | ".join(summary_parts)
    
    def _avg_time_to_accept(self) -> Optional[float]:
        """Calculate average time to accept handoff"""
        accepted = [r for r in self._resolved_requests if r.accepted_at]
        if not accepted:
            return None
        
        times = [r.time_to_accept() for r in accepted]
        return sum(times) / len(times)


# Global singleton
handoff_engine = HandoffEngine()


def get_handoff_engine() -> HandoffEngine:
    """Get global handoff engine instance"""
    return handoff_engine


# Feature flag check
def is_handoff_enabled() -> bool:
    """Check if handoff feature is enabled"""
    return os.getenv("FEATURE_HANDOFF", "true").lower() == "true"


# Convenience functions
def check_handoff(conversation: Dict) -> tuple[bool, Optional[HandoffReason]]:
    """Check if handoff is needed"""
    if not is_handoff_enabled():
        return False, None
    return handoff_engine.should_handoff(conversation)


def create_handoff_request(
    conversation: Dict,
    reason: HandoffReason,
    priority: Optional[int] = None
) -> HandoffRequest:
    """Create handoff request"""
    return handoff_engine.create_handoff(conversation, reason, priority)
