"""
LUNA OS — Multi-Brain V2 Integration Layer

Esta camada integra as features do Multi-Brain V2 no LUNA OS de forma segura e testada.
"""

import sys
from pathlib import Path

# Adicionar antigravity-kit ao path
ANTIGRAVITY_DIR = Path("/Users/franciscotaveira.ads/Documents/antigravity-kit")
if str(ANTIGRAVITY_DIR) not in sys.path:
    sys.path.insert(0, str(ANTIGRAVITY_DIR))

from loguru import logger


# ═══════════════════════════════════════════════
# SMART CACHING INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.cache import contact_cache, ContactMemoryCache
    SMART_CACHE_AVAILABLE = True
    logger.info("✅ Smart Caching integrado")
except ImportError as e:
    logger.warning(f"⚠️ Smart Caching não disponível: {e}")
    SMART_CACHE_AVAILABLE = False
    contact_cache = None


# ═══════════════════════════════════════════════
# HUMAN HANDOFF INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.handoff import handoff_engine, HandoffEngine, check_handoff, create_handoff_request, HandoffReason
    HANDOFF_AVAILABLE = True
    logger.info("✅ Human Handoff integrado")
except ImportError as e:
    logger.warning(f"⚠️ Human Handoff não disponível: {e}")
    HANDOFF_AVAILABLE = False
    handoff_engine = None


# ═══════════════════════════════════════════════
# BEHAVIORAL DNA INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.behavioral_dna import dna_manager, BehavioralDNA, get_customer_dna, adapt_response_to_customer
    DNA_AVAILABLE = True
    logger.info("✅ Behavioral DNA integrado")
except ImportError as e:
    logger.warning(f"⚠️ Behavioral DNA não disponível: {e}")
    DNA_AVAILABLE = False
    dna_manager = None


# ═══════════════════════════════════════════════
# MEMORY CHAIN INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.memory_chain import memory_chain, MemoryChain, log_interaction, verify_audit_trail
    MEMORY_CHAIN_AVAILABLE = True
    logger.info("✅ Memory Chain integrado")
except ImportError as e:
    logger.warning(f"⚠️ Memory Chain não disponível: {e}")
    MEMORY_CHAIN_AVAILABLE = False
    memory_chain = None


# ═══════════════════════════════════════════════
# MULTI-BRAIN ROUTER INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.multi_brain_router import multi_brain_router, MultiBrainRouter, route_to_brain, BrainType
    ROUTER_AVAILABLE = True
    logger.info("✅ Multi-Brain Router integrado")
except ImportError as e:
    logger.warning(f"⚠️ Multi-Brain Router não disponível: {e}")
    ROUTER_AVAILABLE = False
    multi_brain_router = None


# ═══════════════════════════════════════════════
# ANALYTICS INTEGRATION
# ═══════════════════════════════════════════════

try:
    from brain.analytics import analytics_dashboard, AnalyticsDashboard, track_event, get_metrics
    ANALYTICS_AVAILABLE = True
    logger.info("✅ Analytics Dashboard integrado")
except ImportError as e:
    logger.warning(f"⚠️ Analytics Dashboard não disponível: {e}")
    ANALYTICS_AVAILABLE = False
    analytics_dashboard = None


# ═══════════════════════════════════════════════
# HELPER FUNCTIONS — LUNA OS API
# ═══════════════════════════════════════════════

def get_cached_contact(contact_id: str):
    """Get contact from smart cache"""
    if not SMART_CACHE_AVAILABLE or not contact_cache:
        return None
    return contact_cache.get(contact_id)


def set_cached_contact(contact_id: str, data: dict):
    """Set contact in smart cache"""
    if not SMART_CACHE_AVAILABLE or not contact_cache:
        return False
    return contact_cache.set(contact_id, data)


def check_if_needs_handoff(conversation: dict):
    """Check if conversation needs human handoff"""
    if not HANDOFF_AVAILABLE:
        return False, None
    return check_handoff(conversation)


def create_handoff(conversation: dict, reason: str):
    """Create handoff request"""
    if not HANDOFF_AVAILABLE:
        return None
    
    handoff_reason = HandoffReason(reason) if isinstance(reason, str) else reason
    return create_handoff_request(conversation, handoff_reason)


def get_customer_behavioral_dna(contact_id: str):
    """Get customer behavioral DNA"""
    if not DNA_AVAILABLE:
        return None
    return get_customer_dna(contact_id)


def adapt_response(dna, base_response: str) -> str:
    """Adapt response to customer DNA"""
    if not DNA_AVAILABLE or not dna:
        return base_response
    return dna_manager.adapt_response(base_response, dna)


def log_to_memory_chain(interaction: dict):
    """Log interaction to memory chain (audit trail)"""
    if not MEMORY_CHAIN_AVAILABLE:
        return None
    return log_interaction(interaction)


def route_to_best_brain(conversation: dict):
    """Route conversation to best brain (quick/standard/complex)"""
    if not ROUTER_AVAILABLE:
        return "standard", 1.0
    
    decision = route_to_brain(conversation)
    return decision.brain.value, decision.confidence


def track_analytics_event(event_type: str, metadata: dict = None):
    """Track analytics event"""
    if not ANALYTICS_AVAILABLE:
        return
    track_event(event_type, metadata)


def get_lux_metrics(period: str = "24h"):
    """Get LUX dashboard metrics"""
    if not ANALYTICS_AVAILABLE:
        return {}
    return get_metrics(period)


# ═══════════════════════════════════════════════
# STATUS REPORT
# ═══════════════════════════════════════════════

def get_integration_status() -> dict:
    """Get integration status report"""
    return {
        "smart_cache": SMART_CACHE_AVAILABLE,
        "human_handoff": HANDOFF_AVAILABLE,
        "behavioral_dna": DNA_AVAILABLE,
        "memory_chain": MEMORY_CHAIN_AVAILABLE,
        "multi_brain_router": ROUTER_AVAILABLE,
        "analytics": ANALYTICS_AVAILABLE,
        "total_features": 6,
        "integrated_features": sum([
            SMART_CACHE_AVAILABLE,
            HANDOFF_AVAILABLE,
            DNA_AVAILABLE,
            MEMORY_CHAIN_AVAILABLE,
            ROUTER_AVAILABLE,
            ANALYTICS_AVAILABLE
        ])
    }


# Log status on import
status = get_integration_status()
logger.info(f"🌙 LUNA OS Multi-Brain V2 Integration: {status['integrated_features']}/{status['total_features']} features")
