"""
Test Belasis Mock Integration
Execute com: python -m app.scripts.test_belasis_mock (de dentro de /backend)
"""

import sys
import asyncio
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.belasis import belasis
from app.config import settings


async def test_belasis():
    print("🧪 Testando Integração Belasis (Mode: Mock? %s)" % settings.belasis_mock)

    # 1. Testar busca de serviços
    print("\n1. Buscando serviços...")
    services = await belasis.get_services()
    for s in services:
        print(f"   - {s['name']}: R$ {s['price']}")

    # 2. Testar busca de profissionais
    print("\n2. Buscando profissionais...")
    profs = await belasis.get_professionals()
    for p in profs:
        print(f"   - {p['name']} (Especialidades: {', '.join(p['specialties'])})")

    # 3. Testar disponibilidade
    print("\n3. Verificando disponibilidade para 'Escova Lisa' amanhã...")
    slots = await belasis.check_availability("svc_1", "prof_1", "2026-03-01")
    print(f"   - Horários: {', '.join(slots)}")

    # 4. Simular agendamento
    print("\n4. Simulando criação de agendamento...")
    apt_data = {
        "client_phone": "5549991111222",
        "service_id": "svc_1",
        "professional_id": "prof_1",
        "date": "2026-03-01",
        "time": "14:00",
    }
    result = await belasis.create_appointment(apt_data)
    print(f"   - Resumo: {result['message']}")
    print(f"   - ID: {result['id']}")


if __name__ == "__main__":
    asyncio.run(test_belasis())
