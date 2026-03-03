"""
BELASIS API Integration
Sovereign Implementation for LUNA OS
"""

import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.config import settings
from loguru import logger


class BelasisClient:
    """
    Cliente para integração com o ERP Belasis.
    Suporta modo MOCK para testes sem chave de API.
    """

    def __init__(self):
        self.base_url = settings.belasis_url
        self.api_key = settings.belasis_key
        self.mock_mode = settings.belasis_mock
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def get_services(self) -> List[Dict[str, Any]]:
        """Busca lista de serviços e preços"""
        if self.mock_mode:
            logger.debug("🛡️ Belasis: Usando MOCK para services")
            return [
                {"id": "svc_1", "name": "Escova Lisa", "price": 59.0, "duration": 45},
                {
                    "id": "svc_2",
                    "name": "Escova Modelada",
                    "price": 79.0,
                    "duration": 60,
                },
                {
                    "id": "svc_3",
                    "name": "Manicure Tradicional",
                    "price": 50.0,
                    "duration": 45,
                },
                {
                    "id": "svc_4",
                    "name": "Gel Mãos (Aplicação)",
                    "price": 150.0,
                    "duration": 120,
                },
                {
                    "id": "svc_5",
                    "name": "Progressiva Perfecta",
                    "price": 350.0,
                    "duration": 180,
                },
            ]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/services", headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("data", [])
        except Exception as e:
            logger.error(f"❌ Erro ao buscar serviços Belasis: {e}")
            return []

    async def get_professionals(self) -> List[Dict[str, Any]]:
        """Busca lista de profissionais"""
        if self.mock_mode:
            logger.debug("🛡️ Belasis: Usando MOCK para professionals")
            return [
                {"id": "prof_1", "name": "Ju", "specialties": ["Escova", "Corte"]},
                {"id": "prof_2", "name": "Dávila", "specialties": ["Gel", "Manicure"]},
                {"id": "prof_3", "name": "Lu", "specialties": ["Manicure"]},
                {
                    "id": "prof_4",
                    "name": "Carla",
                    "specialties": ["Progressiva", "Química"],
                },
            ]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/professionals", headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("data", [])
        except Exception as e:
            logger.error(f"❌ Erro ao buscar profissionais Belasis: {e}")
            return []

    async def check_availability(
        self, service_id: str, professional_id: Optional[str], date: str
    ) -> List[str]:
        """
        Busca horários disponíveis para um serviço e data.
        Formato date: 'YYYY-MM-DD'
        """
        if self.mock_mode:
            logger.debug(f"🛡️ Belasis: Usando MOCK para availability ({date})")
            # Gera alguns horários fixos para teste
            return ["09:00", "10:30", "14:00", "15:30", "17:00"]

        try:
            params = {"service_id": service_id, "date": date}
            if professional_id:
                params["professional_id"] = professional_id

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/availability", headers=self.headers, params=params
                )
                response.raise_for_status()
                return response.json().get("slots", [])
        except Exception as e:
            logger.error(f"❌ Erro ao verificar disponibilidade Belasis: {e}")
            return []

    async def create_appointment(
        self, appointment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cria um agendamento no ERP.
        """
        if self.mock_mode:
            logger.debug("🛡️ Belasis: Usando MOCK para create_appointment")
            return {
                "status": "success",
                "id": "bel_mock_999",
                "message": "Agendamento simulado com sucesso",
                "data": appointment_data,
            }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/appointments",
                    headers=self.headers,
                    json=appointment_data,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"❌ Erro ao criar agendamento Belasis: {e}")
            return {"status": "error", "message": str(e)}


# Singleton
belasis = BelasisClient()
