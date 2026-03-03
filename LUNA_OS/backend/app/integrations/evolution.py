"""
Evolution API Integration (WhatsApp)
"""

import httpx
from app.config import settings
from app.core.resilience import retry


class EvolutionAPI:
    def __init__(self):
        self.base_url = settings.evolution_url
        self.api_key = settings.evolution_key
        self.instance = settings.evolution_instance
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}

    @retry(retries=3, backoff_in_seconds=1)
    async def send_text(self, to: str, text: str) -> dict:
        """Send text message"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/message/sendText/{self.instance}",
                headers=self.headers,
                json={"number": to.replace("@s.whatsapp.net", ""), "text": text},
            )
            response.raise_for_status()
            return response.json()

    @retry(retries=3, backoff_in_seconds=1)
    async def send_buttons(self, to: str, text: str, buttons: list) -> dict:
        """Send buttons message"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/message/sendButtons/{self.instance}",
                headers=self.headers,
                json={
                    "number": to.replace("@s.whatsapp.net", ""),
                    "title": "Opções",
                    "description": text,
                    "buttons": [
                        {"buttonId": f"btn_{i}", "buttonText": {"displayText": b}}
                        for i, b in enumerate(buttons)
                    ],
                },
            )
            response.raise_for_status()
            return response.json()

    @retry(retries=3, backoff_in_seconds=1)
    async def send_location(
        self, to: str, lat: float, lng: float, name: str, address: str
    ) -> dict:
        """Send location"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/message/sendLocation/{self.instance}",
                headers=self.headers,
                json={
                    "number": to.replace("@s.whatsapp.net", ""),
                    "latitude": lat,
                    "longitude": lng,
                    "name": name,
                    "address": address,
                },
            )
            response.raise_for_status()
            return response.json()

    async def get_instance_status(self) -> dict:
        """Get instance connection status"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/instance/connectionState/{self.instance}",
                headers=self.headers,
            )
            return response.json()

    async def get_chats(self) -> list:
        """Get all chats from instance"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(
                f"{self.base_url}/chat/getChats/{self.instance}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def fetch_messages(self, number: str, limit: int = 100) -> list:
        """Fetch message history for a specific number"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Note: fetchMessages usually expects a POST with query or body depending on version
            # Assuming Latest Evolution v2 pattern
            payload = {
                "where": {
                    "key": {
                        "remoteJid": f"{number.replace('@s.whatsapp.net', '')}@s.whatsapp.net"
                    }
                },
                "limit": limit,
            }
            response = await client.post(
                f"{self.base_url}/chat/fetchMessages/{self.instance}",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            # Returns a list of messages
            return response.json()


evolution = EvolutionAPI()
