"""
Tools Module - LUNA OS Backend
Ferramentas estilo MCP para Gemini 3.1
"""

from app.tools.gemini_tools import (
    # Core
    BaseTool,
    ToolRegistry,
    ToolResult,
    ToolStatus,
    ToolCategory,
    registry,
    
    # Gemini Integration
    GeminiToolExecutor,
    gemini_executor,
    
    # Tools registradas
    search_knowledge,
    check_availability,
    schedule_appointment,
    send_whatsapp,
    send_reminder,
    get_client_history,
    get_analytics,
    get_system_status,
)

__all__ = [
    # Core
    "BaseTool",
    "ToolRegistry",
    "ToolResult",
    "ToolStatus",
    "ToolCategory",
    "registry",
    
    # Gemini Integration
    "GeminiToolExecutor",
    "gemini_executor",
    
    # Tools
    "search_knowledge",
    "check_availability",
    "schedule_appointment",
    "send_whatsapp",
    "send_reminder",
    "get_client_history",
    "get_analytics",
    "get_system_status",
]
