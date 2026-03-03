"""
LUNA CORE - Pydantic Schemas
Padrão Elite MCT: Tipagem forte para todas as entradas e saídas.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- BASE ---


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# --- CLIENTS ---


class ClientBase(BaseSchema):
    phone: str
    name: Optional[str] = None
    email: Optional[str] = None
    tags: List[str] = []
    preferences: Dict[str, Any] = {}
    notes: Optional[str] = None


class ClientRead(ClientBase):
    id: str
    first_contact: datetime
    last_contact: datetime
    total_visits: int = 0
    total_spent: float = 0.0
    conversation_count: Optional[int] = 0
    created_at: datetime


# --- CONVERSATIONS ---


class MessageRead(BaseSchema):
    id: str
    direction: str
    content: str
    created_at: datetime
    intent_detected: Optional[str] = Field(None, alias="intent_detected")
    sentiment: Optional[str] = None
    model_used: Optional[str] = None
    # [AUTOMELHORIA] Metadados de confiança e feedback
    confidence_score: Optional[float] = None
    guardrail_passed: Optional[bool] = None
    feedback: Optional[str] = None
    handled_by: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        protected_namespaces = ()


class ConversationBase(BaseSchema):
    id: str
    phone: str
    status: str
    intent: Optional[str] = None
    sentiment: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None


class ConversationRead(ConversationBase):
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    messages_count: int = 0
    needs_human_intervention: bool = False
    handled_by: Optional[str] = None
    handoff_reason: Optional[str] = None


class ConversationDetail(ConversationRead):
    messages: List[MessageRead] = []
    extracted_data: Dict[str, Any] = {}


# --- BRAIN ---


class BrainSimulateRequest(BaseModel):
    message: str
    phone: str
    name: Optional[str] = "Cliente"


class BrainResponse(BaseModel):
    ok: bool
    response: str
    intent: str
    intent_confidence: float
    model: str
    sentiment: str
    context_used: bool = False
    processing_ms: int
    mode: Optional[str] = None

    class Config:
        protected_namespaces = ()


# --- HEALTH ---


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


# --- ANALYTICS ---


class DashboardKPIs(BaseModel):
    total: int
    converted: int = 0
    abandoned: int = 0
    conversion_rate: float = 0.0


class DashboardMessages(BaseModel):
    total: int
    avg_response_time_ms: float = 0.0


class DashboardResponse(BaseModel):
    period_days: int
    conversations: DashboardKPIs
    messages: DashboardMessages
    appointments: Dict[str, int] = {"total": 0, "completed": 0}
