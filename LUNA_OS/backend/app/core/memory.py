"""
LUNA Memory System - Curto, Médio e Longo Prazo
Padrão MCT: Tipagem forte e separação de responsabilidades

Arquitetura:
- Memory: Camada de acesso ao banco (Supabase)
- MemoryManager: Orquestração de operações complexas
- Modelos de dados tipados para cada entidade
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Literal
from loguru import logger

from app.integrations.supabase_client import get_supabase
from supabase import Client


# ═══════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════


@dataclass
class ClientProfile:
    """Perfil de cliente (Longo Prazo)"""

    id: str
    phone: str
    name: Optional[str] = None
    first_contact: Optional[str] = None
    last_contact: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    total_visits: int = 0
    total_spent: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "name": self.name,
            "first_contact": self.first_contact,
            "last_contact": self.last_contact,
            "tags": self.tags,
            "preferences": self.preferences,
            "total_visits": self.total_visits,
            "total_spent": self.total_spent,
        }


@dataclass
class Conversation:
    """Conversação (Curto Prazo)"""

    id: str
    phone: str
    client_id: Optional[str] = None
    status: Literal["active", "ended", "handed_off"] = "active"
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    messages_count: int = 0
    intent: Optional[str] = None
    sentiment: Optional[str] = None
    conversion_result: Optional[str] = None
    extracted_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "client_id": self.client_id,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "messages_count": self.messages_count,
            "intent": self.intent,
            "sentiment": self.sentiment,
            "conversion_result": self.conversion_result,
            "extracted_data": self.extracted_data,
        }


@dataclass
class MessageRecord:
    """Mensagem individual"""

    conversation_id: str
    direction: Literal["inbound", "outbound"]
    content: str
    intent_detected: Optional[str] = None
    sentiment: Optional[str] = None
    model_used: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "conversation_id": self.conversation_id,
            "direction": self.direction,
            "content": self.content,
            "intent_detected": self.intent_detected,
            "sentiment": self.sentiment,
            "model_used": self.model_used,
            "created_at": self.created_at,
        }


@dataclass
class BusinessIntelligence:
    """Inteligência de Negócio (BI)"""

    phone: str
    conversation_id: Optional[str]
    insight_text: Optional[str] = None
    objections: List[str] = field(default_factory=list)
    customer_mood: str = "unknown"
    urgency_level: int = 3
    potential_value: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "phone": self.phone,
            "conversation_id": self.conversation_id,
            "insight_text": self.insight_text,
            "objections": self.objections,
            "customer_mood": self.customer_mood,
            "urgency_level": self.urgency_level,
            "potential_value": self.potential_value,
            "metadata": self.metadata,
        }


# ═══════════════════════════════════════════════
# MEMORY LAYER (Acesso ao Banco)
# ═══════════════════════════════════════════════


class Memory:
    """
    Camada de acesso direto ao banco de dados.
    Operações CRUD básicas.
    """

    def __init__(self):
        self._supabase: Optional[Client] = None

    def _get_db(self) -> Client:
        """Lazy loading do cliente Supabase"""
        if self._supabase is None:
            self._supabase = get_supabase()
        return self._supabase


# ═══════════════════════════════════════════════
# MEMORY MANAGER (Orquestração)
# ═══════════════════════════════════════════════


class MemoryManager(Memory):
    """
    Orquestrador de Memória Soberana (MCT Legacy Extension)
    Operações de alto nível que combinam múltiplas operações do banco.
    """

    # ==================== CLIENT MEMORY (LONGO PRAZO) ====================

    async def get_or_create_client(self, phone: str, name: str = None) -> Dict:
        """
        Get or create client profile.
        Atualiza last_contact automaticamente.
        """
        db = self._get_db()
        now = datetime.utcnow().isoformat()

        # Try to find existing client
        result = db.table("clients").select("*").eq("phone", phone).execute()

        if result.data:
            client = result.data[0]
            # Update last contact and name if provided
            update_data = {"last_contact": now}
            if name and not client.get("name"):
                update_data["name"] = name

            db.table("clients").update(update_data).eq("phone", phone).execute()
            logger.debug(f"Client {phone} retrieved, last_contact updated")
            return client

        # Create new client
        new_client = {
            "phone": phone,
            "name": name,
            "first_contact": now,
            "last_contact": now,
            "tags": [],
            "preferences": {},
            "total_visits": 0,
            "total_spent": 0,
        }

        try:
            result = db.table("clients").insert(new_client).execute()
            created = result.data[0] if result.data else new_client
            logger.info(f"✨ New client created: {phone} ({name or 'Sem nome'})")
            return created
        except Exception as e:
            logger.error(f"❌ Failed to create client: {e}")
            # Return in-memory client (fallback)
            new_client["id"] = f"temp_{phone}"
            return new_client

    async def update_client_profile(self, phone: str, updates: Dict) -> Optional[Dict]:
        """Update client profile with provided fields"""
        db = self._get_db()

        # Remove protected fields
        safe_updates = {
            k: v
            for k, v in updates.items()
            if k not in ["id", "phone", "first_contact"]
        }

        try:
            result = (
                db.table("clients").update(safe_updates).eq("phone", phone).execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"❌ Failed to update client profile: {e}")
            return None

    async def add_client_tag(self, phone: str, tag: str):
        """Add tag to client (deduplicated)"""
        db = self._get_db()
        client = await self.get_or_create_client(phone)

        tags = client.get("tags", []) or []
        if tag not in tags:
            tags.append(tag)
            db.table("clients").update({"tags": tags}).eq("phone", phone).execute()
            logger.debug(f"Tag '{tag}' added to client {phone}")

    async def increment_client_visits(self, phone: str, amount: int = 1):
        """Increment total visits counter"""
        db = self._get_db()
        client = await self.get_or_create_client(phone)

        current = client.get("total_visits", 0) or 0
        db.table("clients").update({"total_visits": current + amount}).eq(
            "phone", phone
        ).execute()

    async def increment_client_spent(self, phone: str, amount: float):
        """Increment total spent amount"""
        db = self._get_db()
        client = await self.get_or_create_client(phone)

        current = client.get("total_spent", 0) or 0
        db.table("clients").update({"total_spent": current + amount}).eq(
            "phone", phone
        ).execute()

    # ==================== CONVERSATION MEMORY (CURTO PRAZO) ====================

    async def get_active_conversation(self, phone: str) -> Optional[Dict]:
        """Get active conversation for phone"""
        db = self._get_db()

        result = (
            db.table("conversations")
            .select("*")
            .eq("phone", phone)
            .eq("status", "active")
            .order("started_at", desc=True)
            .limit(1)
            .execute()
        )

        return result.data[0] if result.data else None

    async def start_conversation(self, phone: str, client_id: str = None) -> Dict:
        """Start new conversation"""
        db = self._get_db()
        now = datetime.utcnow().isoformat()

        conversation = {
            "phone": phone,
            "client_id": client_id,
            "status": "active",
            "started_at": now,
            "messages_count": 0,
            "extracted_data": {},
        }

        try:
            result = db.table("conversations").insert(conversation).execute()
            created = result.data[0] if result.data else conversation
            logger.debug(f"💬 New conversation started for {phone}")
            return created
        except Exception as e:
            logger.error(f"❌ Failed to start conversation: {e}")
            conversation["id"] = f"temp_{phone}_{now}"
            return conversation

    async def update_conversation(self, conversation_id: str, updates: Dict):
        """Update conversation fields"""
        db = self._get_db()

        # Remove protected fields
        safe_updates = {
            k: v for k, v in updates.items() if k not in ["id", "phone", "started_at"]
        }

        try:
            db.table("conversations").update(safe_updates).eq(
                "id", conversation_id
            ).execute()
        except Exception as e:
            logger.error(f"❌ Failed to update conversation: {e}")

    async def end_conversation(self, conversation_id: str, result: str = None):
        """End conversation with result"""
        db = self._get_db()
        now = datetime.utcnow().isoformat()

        update_data = {
            "status": "ended",
            "ended_at": now,
        }
        if result:
            update_data["conversion_result"] = result

        try:
            db.table("conversations").update(update_data).eq(
                "id", conversation_id
            ).execute()
            logger.debug(f"✅ Conversation {conversation_id} ended")
        except Exception as e:
            logger.error(f"❌ Failed to end conversation: {e}")

    async def mark_handoff(self, phone: str):
        """Mark active conversation as handed off to human"""
        db = self._get_db()
        conversation = await self.get_active_conversation(phone)

        if conversation:
            db.table("conversations").update(
                {
                    "status": "handed_off",
                    "updated_at": datetime.utcnow().isoformat(),
                }
            ).eq("id", conversation["id"]).execute()
            logger.warning(f"🤝 Handoff marked for {phone}")

    # ==================== MESSAGES ====================

    async def save_message(
        self,
        phone: str,
        direction: str,
        content: str,
        intent: str = None,
        sentiment: str = None,
        model_used: str = None,
        confidence_score: float = None,
        guardrail_passed: bool = None,
    ):
        """Save message to database with optional confidence metadata"""
        db = self._get_db()
        now = datetime.utcnow().isoformat()

        # Get or create conversation
        conversation = await self.get_active_conversation(phone)
        if not conversation:
            client = await self.get_or_create_client(phone)
            conversation = await self.start_conversation(phone, client.get("id"))

        # Save message
        message = {
            "conversation_id": conversation["id"],
            "direction": direction,
            "content": content,
            "intent_detected": intent,
            "sentiment": sentiment,
            "model_used": model_used,
            "created_at": now,
        }

        # [AUTOMELHORIA] Adicionar metadados de confiança se disponíveis
        if confidence_score is not None:
            message["confidence_score"] = round(confidence_score, 3)
        if guardrail_passed is not None:
            message["guardrail_passed"] = guardrail_passed

        try:
            db.table("messages").insert(message).execute()

            # Update conversation count
            new_count = (conversation.get("messages_count") or 0) + 1
            db.table("conversations").update(
                {
                    "messages_count": new_count,
                    "intent": intent or conversation.get("intent"),
                    "sentiment": sentiment or conversation.get("sentiment"),
                }
            ).eq("id", conversation["id"]).execute()

        except Exception as e:
            logger.error(f"❌ Failed to save message: {e}")

    async def get_conversation_context(
        self, phone: str, limit: int = 15
    ) -> List[Dict[str, str]]:
        """
        Get recent messages for context.
        Returns list in Claude format: [{role, content}, ...]
        """
        db = self._get_db()

        conversation = await self.get_active_conversation(phone)
        if not conversation:
            return []

        result = (
            db.table("messages")
            .select("direction, content")
            .eq("conversation_id", conversation["id"])
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        # Convert to Claude format (chronological order)
        messages = []
        for msg in reversed(result.data or []):
            role = "user" if msg["direction"] == "inbound" else "assistant"
            messages.append({"role": role, "content": msg["content"]})

        return messages

    # ==================== MÉDIO PRAZO (30 dias) ====================

    async def get_recent_history(self, phone: str, days: int = 30) -> Dict:
        """Get client's recent history for context building"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        # Recent conversations
        conversations = (
            db.table("conversations")
            .select("*")
            .eq("phone", phone)
            .gte("started_at", since)
            .execute()
        )

        # Recent appointments (via client_id)
        appointments_data = []
        try:
            client_result = (
                db.table("clients").select("id").eq("phone", phone).limit(1).execute()
            )
            if client_result.data:
                client_id = client_result.data[0]["id"]
                apt_result = (
                    db.table("appointments")
                    .select("*")
                    .eq("client_id", client_id)
                    .gte("date", since[:10])
                    .execute()
                )
                appointments_data = apt_result.data or []
        except Exception as e:
            logger.debug(f"No appointments found for {phone}: {e}")

        # Analyze patterns
        services_done = []
        professionals_used = []
        preferred_times = []

        for apt in appointments_data:
            if apt.get("service_name"):
                services_done.append(apt["service_name"])
            if apt.get("professional_name"):
                professionals_used.append(apt["professional_name"])
            if apt.get("time"):
                preferred_times.append(str(apt["time"])[:2])  # Hour only

        return {
            "total_conversations": len(conversations.data or []),
            "total_appointments": len(appointments_data),
            "services_done": list(set(services_done)),
            "professionals_used": list(set(professionals_used)),
            "preferred_hours": list(set(preferred_times)),
            "last_visit": appointments_data[0]["date"] if appointments_data else None,
        }

    # ==================== EXTRACTED DATA ====================

    async def save_extracted_data(self, phone: str, field: str, value: Any):
        """Save extracted field from conversation"""
        conversation = await self.get_active_conversation(phone)
        if conversation:
            extracted = conversation.get("extracted_data", {}) or {}
            extracted[field] = value
            await self.update_conversation(
                conversation["id"],
                {"extracted_data": extracted},
            )

    async def get_extracted_data(self, phone: str) -> Dict:
        """Get all extracted data from current conversation"""
        conversation = await self.get_active_conversation(phone)
        return conversation.get("extracted_data", {}) if conversation else {}

    # ==================== BUSINESS INTELLIGENCE (CEO INSIGHTS) ====================

    async def save_business_intelligence(
        self,
        phone: str,
        conversation_id: Optional[str],
        bi_data: Dict,
    ):
        """
        Salva insights estratégicos detectados na conversa.
        Padrão MCT: Sempre salva, mesmo com dados mínimos.
        """
        db = self._get_db()

        try:
            entry = {
                "phone": phone,
                "conversation_id": conversation_id,
                "insight_text": bi_data.get("insight"),
                "objections": bi_data.get("objections", []) or [],
                "customer_mood": bi_data.get("customer_mood", "unknown"),
                "urgency_level": bi_data.get("urgency_level", 3),
                "potential_value": bi_data.get("potential_value", "medium"),
                "metadata": bi_data.get("metadata", {}),
                "created_at": datetime.utcnow().isoformat(),
            }

            db.table("business_intelligence").insert(entry).execute()
            logger.debug(f"💎 BI saved for {phone}")

        except Exception as e:
            logger.error(f"❌ Error saving BI intelligence: {e}")

    # ==================== UTILITY METHODS ====================

    async def get_client_stats(self, phone: str) -> Dict:
        """Get comprehensive client statistics"""
        client = await self.get_or_create_client(phone)
        history = await self.get_recent_history(phone, days=90)

        return {
            "profile": client,
            "history": history,
            "engagement_score": self._calculate_engagement_score(history),
        }

    def _calculate_engagement_score(self, history: Dict) -> float:
        """Calculate client engagement score (0-100)"""
        score = 0.0

        # Conversations weight (30%)
        conv_count = history.get("total_conversations", 0) or 0
        score += min(30, conv_count * 3)

        # Appointments weight (50%)
        apt_count = history.get("total_appointments", 0) or 0
        score += min(50, apt_count * 5)

        # Recency weight (20%)
        last_visit = history.get("last_visit")
        if last_visit:
            try:
                days_since = (
                    datetime.utcnow() - datetime.fromisoformat(last_visit)
                ).days
                if days_since < 7:
                    score += 20
                elif days_since < 30:
                    score += 10
            except:
                pass

        return min(100, score)
