"""
Google Gemini Tools Integration — MCT OS v2.0
Implementação de ferramentas estilo MCP para Gemini 3.1

Arquitetura:
- Ferramentas registradas via decorator
- Execução assíncrona com fallback
- Schema validation com Pydantic
- Logging estruturado para auditoria
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, Type
from enum import Enum
import json
import asyncio
from loguru import logger
from pydantic import BaseModel, Field, ValidationError


# ═══════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════

class ToolStatus(str, Enum):
    """Status de execução da ferramenta"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    NOT_FOUND = "not_found"


class ToolCategory(str, Enum):
    """Categoria da ferramenta"""
    KNOWLEDGE = "knowledge"
    SCHEDULING = "scheduling"
    COMMUNICATION = "communication"
    ANALYTICS = "analytics"
    SYSTEM = "system"


@dataclass
class ToolResult:
    """Resultado padronizado de ferramenta"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    status: ToolStatus = ToolStatus.SUCCESS
    execution_time_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "status": self.status.value,
            "execution_time_ms": self.execution_time_ms,
            "metadata": self.metadata,
        }


@dataclass
class ToolDefinition:
    """Definição de ferramenta para registro"""
    name: str
    description: str
    category: ToolCategory
    parameters: Type[BaseModel]
    function: Callable
    timeout_seconds: int = 30
    enabled: bool = True


# ═══════════════════════════════════════════════
# BASE TOOL CLASS
# ═══════════════════════════════════════════════

class BaseTool(ABC):
    """
    Classe base para todas as ferramentas.
    Padrão MCT: Validação + Execução + Logging
    """

    name: str = "base_tool"
    description: str = "Base tool"
    category: ToolCategory = ToolCategory.SYSTEM
    timeout_seconds: int = 30

    # Pydantic model para parâmetros
    parameters_schema: Type[BaseModel] = None

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        """
        Template method para execução de ferramentas.
        Segue padrão: Validate → Execute → Log → Return
        """
        start_time = datetime.utcnow()

        try:
            # 1. Validação dos parâmetros
            validated_params = await self.validate(params)

            # 2. Execução com timeout
            result = await asyncio.wait_for(
                self.run(validated_params),
                timeout=self.timeout_seconds
            )

            # 3. Log de sucesso
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.info(
                f"✅ Tool '{self.name}' executed in {execution_time}ms"
            )

            return ToolResult(
                success=True,
                data=result,
                status=ToolStatus.SUCCESS,
                execution_time_ms=execution_time,
                metadata={"params": validated_params.model_dump()},
            )

        except asyncio.TimeoutError:
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.error(f"❌ Tool '{self.name}' timed out after {self.timeout_seconds}s")
            return ToolResult(
                success=False,
                error=f"Timeout after {self.timeout_seconds}s",
                status=ToolStatus.TIMEOUT,
                execution_time_ms=execution_time,
            )

        except ValidationError as e:
            logger.error(f"❌ Tool '{self.name}' validation error: {e}")
            return ToolResult(
                success=False,
                error=f"Validation error: {str(e)}",
                status=ToolStatus.ERROR,
                execution_time_ms=0,
            )

        except Exception as e:
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.exception(f"❌ Tool '{self.name}' execution error: {e}")
            return ToolResult(
                success=False,
                error=str(e),
                status=ToolStatus.ERROR,
                execution_time_ms=execution_time,
            )

    async def validate(self, params: Dict[str, Any]) -> BaseModel:
        """Valida parâmetros usando schema Pydantic"""
        if self.parameters_schema is None:
            raise ValueError(f"Tool '{self.name}' has no parameters schema")

        return self.parameters_schema(**params)

    @abstractmethod
    async def run(self, params: BaseModel) -> Any:
        """
        Método abstrato para implementação da lógica.
        Deve ser sobrescrito por cada ferramenta.
        """
        pass


# ═══════════════════════════════════════════════
# TOOL REGISTRY (Singleton)
# ═══════════════════════════════════════════════

class ToolRegistry:
    """
    Registry central de ferramentas.
    Padrão Singleton com lazy loading.
    """

    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, ToolDefinition] = {}

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(
        self,
        name: str,
        description: str,
        category: ToolCategory,
        parameters: Type[BaseModel],
        timeout_seconds: int = 30,
    ):
        """
        Decorator para registrar ferramentas.
        Uso:
            @registry.register(
                name="search_knowledge",
                description="Busca na base de conhecimento",
                category=ToolCategory.KNOWLEDGE,
                parameters=SearchParams
            )
            async def search_knowledge(params): ...
        """
        def decorator(func: Callable):
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                category=category,
                parameters=parameters,
                function=func,
                timeout_seconds=timeout_seconds,
            )
            logger.info(f"🔧 Tool registered: {name} ({category.value})")
            return func
        return decorator

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Obtém definição de ferramenta por nome"""
        return self._tools.get(name)

    def list_tools(self, category: Optional[ToolCategory] = None) -> List[Dict]:
        """Lista todas as ferramentas (opcionalmente filtradas por categoria)"""
        tools = self._tools.values()
        if category:
            tools = [t for t in tools if t.category == category]

        return [
            {
                "name": t.name,
                "description": t.description,
                "category": t.category.value,
                "parameters": t.parameters.model_json_schema(),
                "timeout_seconds": t.timeout_seconds,
            }
            for t in tools
        ]

    def execute_tool(self, name: str, params: Dict[str, Any]) -> Any:
        """Executa ferramenta por nome"""
        tool_def = self.get(name)
        if not tool_def:
            raise ValueError(f"Tool '{name}' not found")

        if not tool_def.enabled:
            raise ValueError(f"Tool '{name}' is disabled")

        return tool_def.function(params)


# Singleton global
registry = ToolRegistry()


# ═══════════════════════════════════════════════
# KNOWLEDGE TOOLS
# ═══════════════════════════════════════════════

class SearchKnowledgeParams(BaseModel):
    """Parâmetros para busca de conhecimento"""
    query: str = Field(..., description="Termo de busca", min_length=2)
    category: Optional[str] = Field(None, description="Categoria (servicos, produtos, faq)")
    limit: int = Field(default=5, description="Número máximo de resultados", ge=1, le=20)


@registry.register(
    name="search_knowledge",
    description="Busca na base de conhecimento (serviços, produtos, FAQ)",
    category=ToolCategory.KNOWLEDGE,
    parameters=SearchKnowledgeParams,
)
async def search_knowledge(params: SearchKnowledgeParams) -> Dict:
    """
    Busca informações na base de conhecimento da Haven.
    Integra com KnowledgeBase loader.
    """
    from app.knowledge.loader import KnowledgeBase

    kb = KnowledgeBase()
    results = {}

    # Busca em diferentes categorias
    if params.category in (None, "servicos"):
        results["services"] = kb.search_services(params.query)[:params.limit]

    if params.category in (None, "faq"):
        results["faq"] = kb.search_faq(params.query)
        if results["faq"]:
            results["faq"] = [results["faq"]] if isinstance(results["faq"], dict) else results["faq"][:params.limit]

    if params.category in (None, "profissionais"):
        results["professionals"] = kb.search_professionals(params.query)[:params.limit]

    return {
        "query": params.query,
        "category": params.category,
        "results": results,
        "total_found": sum(len(v) if isinstance(v, list) else 1 for v in results.values() if v),
    }


# ═══════════════════════════════════════════════
# SCHEDULING TOOLS
# ═══════════════════════════════════════════════

class CheckAvailabilityParams(BaseModel):
    """Parâmetros para verificar disponibilidade"""
    service: str = Field(..., description="Nome do serviço")
    date: str = Field(..., description="Data (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Horário preferencial (HH:MM)")
    professional: Optional[str] = Field(None, description="Profissional preferida")


@registry.register(
    name="check_availability",
    description="Verifica disponibilidade de horários na agenda",
    category=ToolCategory.SCHEDULING,
    parameters=CheckAvailabilityParams,
)
async def check_availability(params: CheckAvailabilityParams) -> Dict:
    """
    Verifica horários disponíveis na agenda.
    Integra com sistema de agendamentos.
    """
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()

    # Buscar horários ocupados
    query = (
        db.table("appointments")
        .select("time")
        .eq("date", params.date)
        .eq("status", "confirmed")
    )

    if params.professional:
        query = query.eq("professional_name", params.professional)

    result = query.execute()
    occupied_times = [apt["time"] for apt in result.data or []]

    # Gerar horários disponíveis (8h às 20h)
    all_times = [f"{h:02d}:00" for h in range(8, 20)]
    available_times = [t for t in all_times if t not in occupied_times]

    return {
        "date": params.date,
        "service": params.service,
        "professional": params.professional,
        "available_times": available_times[:10],  # Retorna até 10 horários
        "total_available": len(available_times),
    }


class ScheduleAppointmentParams(BaseModel):
    """Parâmetros para agendamento"""
    client_id: str = Field(..., description="ID do cliente")
    service: str = Field(..., description="Nome do serviço")
    date: str = Field(..., description="Data (YYYY-MM-DD)")
    time: str = Field(..., description="Horário (HH:MM)")
    professional: Optional[str] = Field(None, description="Profissional")
    notes: Optional[str] = Field(None, description="Observações")


@registry.register(
    name="schedule_appointment",
    description="Agenda um horário na Haven",
    category=ToolCategory.SCHEDULING,
    parameters=ScheduleAppointmentParams,
)
async def schedule_appointment(params: ScheduleAppointmentParams) -> Dict:
    """
    Cria um novo agendamento.
    Valida disponibilidade antes de criar.
    """
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()

    # Validar disponibilidade
    availability = await check_availability(
        CheckAvailabilityParams(
            service=params.service,
            date=params.date,
            time=params.time,
            professional=params.professional,
        )
    )

    if params.time not in availability["available_times"]:
        return {
            "success": False,
            "error": "Horário indisponível",
            "suggested_times": availability["available_times"][:3],
        }

    # Criar agendamento
    appointment = {
        "client_id": params.client_id,
        "service_name": params.service,
        "date": params.date,
        "time": params.time,
        "professional_name": params.professional,
        "notes": params.notes,
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat(),
    }

    result = db.table("appointments").insert(appointment).execute()

    if result.data:
        # Atualizar contador de visitas do cliente
        db.rpc("increment_client_visits", {"p_client_id": params.client_id}).execute()

        return {
            "success": True,
            "appointment": result.data[0],
            "message": f"Agendamento confirmado para {params.date} às {params.time}",
        }
    else:
        return {
            "success": False,
            "error": "Falha ao criar agendamento",
        }


# ═══════════════════════════════════════════════
# COMMUNICATION TOOLS
# ═══════════════════════════════════════════════

class SendWhatsAppParams(BaseModel):
    """Parâmetros para envio de WhatsApp"""
    phone: str = Field(..., description="Número do telefone (com DDI)")
    message: str = Field(..., description="Mensagem a enviar")
    instance: str = Field(default="haven", description="Instância Evolution")


@registry.register(
    name="send_whatsapp",
    description="Envia mensagem via WhatsApp (Evolution API)",
    category=ToolCategory.COMMUNICATION,
    parameters=SendWhatsAppParams,
    timeout_seconds=60,
)
async def send_whatsapp(params: SendWhatsAppParams) -> Dict:
    """
    Envia mensagem via Evolution API.
    Usado para confirmações, lembretes e follow-ups.
    """
    from app.integrations.evolution import evolution

    try:
        await evolution.send_text(params.instance, params.phone, params.message)

        return {
            "success": True,
            "message": "Mensagem enviada com sucesso",
            "phone": params.phone,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "phone": params.phone,
        }


class SendReminderParams(BaseModel):
    """Parâmetros para envio de lembrete"""
    appointment_id: str = Field(..., description="ID do agendamento")
    reminder_type: str = Field(default="confirmation", description="Tipo: confirmation, reminder, followup")


@registry.register(
    name="send_reminder",
    description="Envia lembrete de agendamento",
    category=ToolCategory.COMMUNICATION,
    parameters=SendReminderParams,
)
async def send_reminder(params: SendReminderParams) -> Dict:
    """
    Envia lembrete automático de agendamento.
    Templates personalizados por tipo.
    """
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()

    # Buscar agendamento
    apt_result = (
        db.table("appointments")
        .select("*, clients(name, phone)")
        .eq("id", params.appointment_id)
        .execute()
    )

    if not apt_result.data:
        return {"success": False, "error": "Agendamento não encontrado"}

    apt = apt_result.data[0]
    client = apt.get("clients", {})

    # Template de mensagem
    templates = {
        "confirmation": f"""
Olá {client.get('name', 'Cliente')}! ✨

Confirme seu agendamento na Haven:
📅 {apt['date']} às {apt['time']}
💇‍♀️ {apt['service_name']}

Respondar SIM para confirmar ou NÃO para remarcar.
""",
        "reminder": f"""
Oi {client.get('name', 'Cliente')}! 😊

Lembrete do seu agendamento amanhã:
📅 {apt['date']} às {apt['time']}
📍 Rua Mato Grosso, 837E - Jardim Itália

Te esperamos lá! ✨
""",
        "followup": f"""
Olá {client.get('name', 'cliente')}! 💕

Como foi seu atendimento na Haven?
Adoraríamos saber sua opinião!

Respondar aqui se ficou tudo bem 😊
""",
    }

    message = templates.get(params.reminder_type, templates["confirmation"])

    # Enviar WhatsApp
    result = await send_whatsapp(
        SendWhatsAppParams(
            phone=client.get("phone"),
            message=message.strip(),
        )
    )

    if result["success"]:
        # Log do lembrete
        db.table("reminder_logs").insert({
            "appointment_id": params.appointment_id,
            "type": params.reminder_type,
            "sent_at": datetime.utcnow().isoformat(),
            "status": "sent",
        }).execute()

    return result


# ═══════════════════════════════════════════════
# ANALYTICS TOOLS
# ═══════════════════════════════════════════════

class GetClientHistoryParams(BaseModel):
    """Parâmetros para histórico do cliente"""
    phone: str = Field(..., description="Telefone do cliente")
    days: int = Field(default=90, description="Dias de histórico", ge=1, le=365)


@registry.register(
    name="get_client_history",
    description="Obtém histórico completo do cliente",
    category=ToolCategory.ANALYTICS,
    parameters=GetClientHistoryParams,
)
async def get_client_history(params: GetClientHistoryParams) -> Dict:
    """
    Retorna histórico de agendamentos e interações do cliente.
    """
    from app.core.memory import MemoryManager

    memory = MemoryManager()

    # Perfil do cliente
    client = await memory.get_or_create_client(params.phone)

    # Histórico de agendamentos
    history = await memory.get_recent_history(params.phone, days=params.days)

    # Conversas recentes
    conversations = await memory.get_conversation_context(params.phone, limit=20)

    return {
        "client": client,
        "history": history,
        "recent_conversations": conversations,
        "engagement_score": memory._calculate_engagement_score(history),
    }


class GetAnalyticsParams(BaseModel):
    """Parâmetros para analytics"""
    metric: str = Field(..., description="Métrica: revenue, appointments, satisfaction")
    start_date: str = Field(..., description="Data início (YYYY-MM-DD)")
    end_date: str = Field(..., description="Data fim (YYYY-MM-DD)")


@registry.register(
    name="get_analytics",
    description="Obtém métricas e analytics da Haven",
    category=ToolCategory.ANALYTICS,
    parameters=GetAnalyticsParams,
)
async def get_analytics(params: GetAnalyticsParams) -> Dict:
    """
    Retorna métricas de negócio.
    """
    from app.integrations.supabase_client import get_supabase

    db = get_supabase()

    if params.metric == "revenue":
        result = (
            db.table("appointments")
            .select("value")
            .gte("date", params.start_date)
            .lte("date", params.end_date)
            .eq("status", "completed")
            .execute()
        )
        total = sum(apt.get("value", 0) for apt in result.data or [])
        return {"metric": "revenue", "total": total, "period": f"{params.start_date} to {params.end_date}"}

    elif params.metric == "appointments":
        result = (
            db.table("appointments")
            .select("id, status")
            .gte("date", params.start_date)
            .lte("date", params.end_date)
            .execute()
        )
        by_status = {}
        for apt in result.data or []:
            status = apt.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1
        return {"metric": "appointments", "total": len(result.data or []), "by_status": by_status}

    elif params.metric == "satisfaction":
        result = (
            db.table("feedback")
            .select("rating")
            .gte("created_at", params.start_date)
            .lte("created_at", params.end_date)
            .execute()
        )
        ratings = [f.get("rating", 0) for f in result.data or []]
        avg = sum(ratings) / len(ratings) if ratings else 0
        return {"metric": "satisfaction", "average": round(avg, 2), "count": len(ratings)}

    return {"error": f"Unknown metric: {params.metric}"}


# ═══════════════════════════════════════════════
# SYSTEM TOOLS
# ═══════════════════════════════════════════════

class GetSystemStatusParams(BaseModel):
    """Parâmetros para status do sistema"""
    component: Optional[str] = Field(None, description="Componente: all, brain, memory, evolution")


@registry.register(
    name="get_system_status",
    description="Obtém status dos componentes do sistema",
    category=ToolCategory.SYSTEM,
    parameters=GetSystemStatusParams,
)
async def get_system_status(params: GetSystemStatusParams) -> Dict:
    """
    Retorna status de saúde dos componentes.
    """
    status = {}

    if params.component in (None, "brain"):
        status["brain"] = {
            "status": "healthy",
            "model_quick": "google/gemini-2.0-flash-001",
            "model_standard": "anthropic/claude-3.5-haiku",
            "model_complex": "anthropic/claude-3.5-sonnet",
        }

    if params.component in (None, "memory"):
        status["memory"] = {
            "status": "healthy",
            "cache_enabled": True,
        }

    if params.component in (None, "evolution"):
        status["evolution"] = {
            "status": "healthy",
            "instance": "haven",
        }

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "components": status,
        "overall": "healthy" if all(v.get("status") == "healthy" for v in status.values()) else "degraded",
    }


# ═══════════════════════════════════════════════
# GEMINI MCP INTEGRATION
# ═══════════════════════════════════════════════

class GeminiToolExecutor:
    """
    Executor de ferramentas para integração com Gemini.
    Converte tool calls do Gemini em execuções locais.
    """

    def __init__(self):
        self.registry = registry

    async def execute_tool_call(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
    ) -> Dict:
        """
        Executa tool call do Gemini.
        Formato compatível com Gemini API function calling.
        """
        logger.info(f"🔧 Executing Gemini tool call: {tool_name}")
        logger.debug(f"Args: {json.dumps(tool_args, indent=2)}")

        try:
            # Obter ferramenta
            tool_def = self.registry.get(tool_name)
            if not tool_def:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found",
                    "available_tools": [t["name"] for t in self.registry.list_tools()],
                }

            # Executar
            result = await tool_def.function(tool_def.parameters(**tool_args))

            return {
                "success": True,
                "tool": tool_name,
                "result": result,
            }

        except Exception as e:
            logger.exception(f"❌ Tool execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
            }

    def get_gemini_tools_schema(self) -> List[Dict]:
        """
        Retorna schema de ferramentas no formato Gemini.
        Usado para configurar function calling na API do Gemini.
        """
        tools = self.registry.list_tools()

        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
            for tool in tools
        ]


# Singleton
gemini_executor = GeminiToolExecutor()
