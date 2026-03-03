import asyncio
import os
import sys

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.campaign_manager import campaign_manager


async def test_campaigns():
    print("🔄 Sincronizando campanhas...")
    await campaign_manager.sync_campaigns()

    # Simula campanhas em memória se o DB estiver vazio para este teste
    if not campaign_manager.active_campaigns:
        print("⚠️ DB Vazio. Injetando campanha mock para teste de lógica...")
        campaign_manager.active_campaigns = [
            {
                "id": "mock_id",
                "name": "Promoção Verão",
                "trigger_keywords": ["VERAO20", "calor", "praia"],
                "discount_percent": 20,
                "message_template": "Aproveite 20% de desconto hoje!",
            }
        ]
    else:
        print(
            f"✅ {len(campaign_manager.active_campaigns)} campanhas carregadas do DB."
        )

    # Teste de detecção
    msg = "Quero marcar uma unha com o cupom VERAO20"
    camp = campaign_manager.detect_campaign(msg)

    if camp:
        print(f"🎯 Campanha detectada: {camp['name']}")
        context = campaign_manager.get_campaign_context(camp)
        print(f"📝 Contexto gerado:\n{context}")
    else:
        print("❌ Nenhuma campanha detectada.")


if __name__ == "__main__":
    asyncio.run(test_campaigns())
