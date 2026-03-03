"""
Exemplo de Uso - Gemini Tools Integration
Demonstração de como usar as ferramentas com Gemini 3.1
"""

import asyncio
from app.tools.gemini_tools import (
    gemini_executor,
    registry,
    search_knowledge,
    check_availability,
    schedule_appointment,
    send_whatsapp,
    get_client_history,
    get_analytics,
    get_system_status,
)


async def example_search_knowledge():
    """Exemplo: Busca de conhecimento"""
    print("\n🔍 === Exemplo: Search Knowledge ===")

    result = await search_knowledge({
        "query": "escova progressiva",
        "category": "servicos",
        "limit": 5,
    })

    print(f"Success: {result.success}")
    print(f"Results: {result.data}")


async def example_check_availability():
    """Exemplo: Verificar disponibilidade"""
    print("\n📅 === Exemplo: Check Availability ===")

    result = await check_availability({
        "service": "Escova",
        "date": "2024-01-20",
        "time": "14:00",
        "professional": "Ana",
    })

    print(f"Success: {result.success}")
    print(f"Available times: {result.data.get('available_times', [])}")


async def example_schedule_appointment():
    """Exemplo: Agendar horário"""
    print("\n✅ === Exemplo: Schedule Appointment ===")

    result = await schedule_appointment({
        "client_id": "client_123",
        "service": "Unha de gel",
        "date": "2024-01-20",
        "time": "15:00",
        "professional": "Carla",
        "notes": "Primeira vez",
    })

    print(f"Success: {result.success}")
    print(f"Message: {result.data.get('message', '') if result.data else 'N/A'}")


async def example_send_whatsapp():
    """Exemplo: Enviar WhatsApp"""
    print("\n📱 === Exemplo: Send WhatsApp ===")

    result = await send_whatsapp({
        "phone": "5511999999999",
        "message": "Olá! Este é um teste de envio de mensagem.",
        "instance": "haven",
    })

    print(f"Success: {result.success}")
    print(f"Result: {result.data}")


async def example_get_client_history():
    """Exemplo: Histórico do cliente"""
    print("\n📊 === Exemplo: Get Client History ===")

    result = await get_client_history({
        "phone": "5511999999999",
        "days": 90,
    })

    print(f"Success: {result.success}")
    if result.data:
        print(f"Client: {result.data.get('client', {}).get('name', 'N/A')}")
        print(f"Engagement Score: {result.data.get('engagement_score', 0)}")


async def example_get_analytics():
    """Exemplo: Analytics"""
    print("\n📈 === Exemplo: Get Analytics ===")

    result = await get_analytics({
        "metric": "appointments",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
    })

    print(f"Success: {result.success}")
    print(f"Analytics: {result.data}")


async def example_get_system_status():
    """Exemplo: Status do sistema"""
    print("\n🔧 === Exemplo: Get System Status ===")

    result = await get_system_status({
        "component": None,  # Todos componentes
    })

    print(f"Success: {result.success}")
    print(f"Overall status: {result.data.get('overall', 'unknown')}")
    print(f"Components: {list(result.data.get('components', {}).keys())}")


async def example_gemini_tool_call():
    """Exemplo: Tool call via Gemini executor"""
    print("\n🤖 === Exemplo: Gemini Tool Call ===")

    # Simula tool call do Gemini
    result = await gemini_executor.execute_tool_call(
        tool_name="search_knowledge",
        tool_args={"query": "manicure", "limit": 3},
    )

    print(f"Tool: {result.get('tool', 'N/A')}")
    print(f"Success: {result.get('success', False)}")
    print(f"Result: {result.get('result', {})}")


async def example_list_all_tools():
    """Exemplo: Listar todas as ferramentas"""
    print("\n🛠️ === Exemplo: List All Tools ===")

    tools = registry.list_tools()

    print(f"Total tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")


async def main():
    """Executa todos os exemplos"""
    print("=" * 60)
    print("GEMINI TOOLS INTEGRATION - EXAMPLES")
    print("=" * 60)

    # Listar ferramentas
    await example_list_all_tools()

    # Exemplos individuais
    await example_search_knowledge()
    await example_check_availability()
    # await example_schedule_appointment()  # Descomentar para testar agendamento real
    # await example_send_whatsapp()  # Descomentar para testar envio real
    await example_get_client_history()
    await example_get_analytics()
    await example_get_system_status()
    await example_gemini_tool_call()

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
