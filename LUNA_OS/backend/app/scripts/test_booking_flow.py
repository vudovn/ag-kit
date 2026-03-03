"""
Test LUNA Booking Flow (Sovereign Integration)
"""

import sys
import asyncio
from pathlib import Path

# Adiciona o diretório raiz ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.core.brain import BrainEngine


async def test_flow():
    brain = BrainEngine()
    phone = "5549991112233"
    name = "Maria Teste"

    print("\n--- INÍCIO DA SIMULAÇÃO DE AGENDAMENTO ---")

    # Rodada 1: Intenção genérica
    print("\n[USER]: Oi! Quero marcar um horário.")
    res1 = await brain.process_message(phone, name, "Oi! Quero marcar um horário.")
    print(f"[LUNA]: {res1['response']}")

    # Rodada 2: Escolhe serviço
    print("\n[USER]: Quero fazer uma escova.")
    res2 = await brain.process_message(phone, name, "Quero fazer uma escova.")
    print(f"[LUNA]: {res2['response']}")

    # Rodada 3: Escolhe data
    print("\n[USER]: Pode ser amanhã?")
    res3 = await brain.process_message(phone, name, "Pode ser amanhã?")
    print(f"[LUNA]: {res3['response']}")

    # Rodada 4: Escolhe horário
    print("\n[USER]: Às 14h, por favor.")
    res4 = await brain.process_message(phone, name, "Às 14h, por favor.")
    print(f"[LUNA]: {res4['response']}")

    if res4.get("action") == "confirm_appointment":
        print("\n✅ SUCESSO: Agendamento identificado e validado pelo Scheduler!")
    else:
        print("\n❌ FALHA: Agendamento não atingiu o estado de confirmação.")


if __name__ == "__main__":
    asyncio.run(test_flow())
