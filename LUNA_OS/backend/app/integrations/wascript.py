"""
WAScript Integration
Envia a inteligência extraída pela LUNA diretamente para as Notas do CRM.
"""

import os
import httpx
from loguru import logger
from typing import Dict, Any


class WAScriptClient:
    def __init__(self):
        self.base_url = "https://api-whatsapp.wascript.com.br"
        self.token = os.getenv("WASCRIPT_TOKEN", "")

    async def add_client_note(self, phone: str, insight_data: Dict[str, Any]) -> bool:
        """
        Envia uma nota para o perfil do cliente no WAScript CRM.
        """
        if not self.token:
            logger.warning("WASCRIPT_TOKEN not configured. Skipping note creation.")
            return False

        # Formata o output visual para a secretária
        insight_text = insight_data.get("insight", "")
        mood = insight_data.get("customer_mood", "neutro")
        urgency = insight_data.get("urgency_level", 1)

        # Emoji baseado na urgência
        urgency_emoji = "🔥" if urgency >= 3 else "⚡"

        note = f"🤖 LUNA INSIGHT {urgency_emoji}\n\n📝 Resumo: {insight_text}\n🎭 Humor: {mood}\n\n*Nota gerada automaticamente pelo Dual Brain*"

        endpoint = f"{self.base_url}/api/criar-nota/{self.token}"
        payload = {"userID": phone, "text": note}

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(endpoint, json=payload)

            if response.status_code in (200, 201):
                logger.info(f"✅ WAScript: Nota CRM criada com sucesso para {phone}")
                return True
            else:
                logger.error(
                    f"❌ WAScript: Falha ao criar nota ({response.status_code}) - {response.text}"
                )
                return False

        except Exception as e:
            logger.exception(f"🚨 WAScript API Error: {e}")
            return False


wascript = WAScriptClient()
