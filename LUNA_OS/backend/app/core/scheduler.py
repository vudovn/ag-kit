"""
LUNA Scheduler - Orquestrador de Agendamentos (Belasis ERP)
Responsável por validar dados extraídos e gerenciar disponibilidade.

DEBT #M3: Type hints e docstrings completas
DEBT #M4: Docstrings em todas as funções públicas
"""

from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from loguru import logger
from app.integrations.belasis import belasis


class Scheduler:
    """
    Orquestra a lógica de agendamento entre o Brain e o ERP Belasis.

    Attributes:
        _services_cache: Cache de serviços do Belasis
        _professionals_cache: Cache de profissionais do Belasis
    """

    def __init__(self) -> None:
        """Inicializa Scheduler com caches vazios."""
        self._services_cache: Optional[List[Dict[str, Any]]] = None
        self._professionals_cache: Optional[List[Dict[str, Any]]] = None

    async def _ensure_cache(self) -> None:
        """
        Garante que temos serviços e profissionais em cache (memória).

        Faz fetch dos dados do Belasis apenas se cache estiver vazio.
        """
        if not self._services_cache:
            self._services_cache = await belasis.get_services()
        if not self._professionals_cache:
            self._professionals_cache = await belasis.get_professionals()

    def _find_service_id(self, service_name: str) -> Optional[str]:
        """
        Tenta encontrar o ID do serviço pelo nome/alias.

        Args:
            service_name: Nome ou apelido do serviço

        Returns:
            ID do serviço se encontrado, None caso contrário
        """
        if not service_name or not self._services_cache:
            return None

        name_lower = service_name.lower()
        for s in self._services_cache:
            # Match exato ou parcial
            if name_lower in s["name"].lower() or s["name"].lower() in name_lower:
                return s["id"]
        return None

    def _find_professional_id(self, professional_name: str) -> Optional[str]:
        """
        Tenta encontrar o ID do profissional pelo nome/apelido.

        Args:
            professional_name: Nome ou apelido do profissional

        Returns:
            ID do profissional se encontrado, None caso contrário
        """
        if not professional_name or not self._professionals_cache:
            return None

        name_lower = professional_name.lower()
        for p in self._professionals_cache:
            if name_lower in p["name"].lower() or p["name"].lower() in name_lower:
                return p["id"]
        return None

    async def process_booking(
        self, extracted_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Processa uma tentativa de agendamento.

        Args:
            extracted_data: Dados extraídos da conversa (service, professional, date, time)

        Returns:
            Tuple de (sucesso_parcial, mensagem_feedback, dados_ajustados)
        """
        await self._ensure_cache()

        service_raw = extracted_data.get("service")
        prof_raw = extracted_data.get("professional")
        date_raw = extracted_data.get("date")
        time_raw = extracted_data.get("time")

        service_id = self._find_service_id(service_raw)
        professional_id = self._find_professional_id(prof_raw)

        # 1. Validar Serviço
        if not service_id:
            return (
                False,
                "Qual serviço você gostaria de agendar? (ex: Escova, Manicure, Progressiva)",
                extracted_data,
            )

        # 2. Validar Data
        if not date_raw:
            return (
                False,
                f"Para qual dia você deseja marcar seu {service_raw}?",
                extracted_data,
            )

        # 3. Validar Horário e Disponibilidade
        if not time_raw:
            # Buscar horários disponíveis para o dia
            slots = await belasis.check_availability(
                service_id, professional_id, date_raw
            )
            if not slots:
                return (
                    False,
                    f"Infelizmente não temos horários disponíveis para {date_raw}. Quer tentar outro dia?",
                    extracted_data,
                )

            slots_str = ", ".join(slots[:5])
            return (
                False,
                f"Temos estes horários disponíveis para {date_raw}: {slots_str}. Qual prefere?",
                extracted_data,
            )

        # 4. Tentar Efetivar (se tivermos tudo)
        # Aqui poderíamos fazer uma última checagem se o slot específico está vago
        # No MOCK, vamos considerar que sim.

        booking_payload = {
            "service_id": service_id,
            "professional_id": professional_id,
            "date": date_raw,
            "time": time_raw,
            "client_name": extracted_data.get("name"),
            "client_phone": extracted_data.get("phone"),
        }

        return True, "Perfeito! Seu agendamento foi pré-confirmado.", booking_payload


# Singleton
scheduler = Scheduler()
