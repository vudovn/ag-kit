"""
LUNA Marketing - Sugestões e Upsell
Padrão Elite MCT: Campanhas e retenção estratégica.
"""

from typing import Optional, Dict, Any
import httpx
from loguru import logger


def get_marketing_suggestion(service_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca sugestões de marketing e upsell para um serviço.
    """
    try:
        # Chamar API de campanhas
        # Nota: luna-backend é o nome do container no docker compose
        response = httpx.get(
            f"http://luna-backend:8000/api/campaigns/suggest/{service_id}", timeout=2.0
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception as e:
        logger.debug(f"Erro ao buscar campanhas: {e}")
        return None


def generate_upsell_script(service_id: str, client_name: str = "") -> str:
    """
    Gera script de upsell para usar durante espera.
    """
    suggestion = get_marketing_suggestion(service_id)

    if not suggestion:
        return ""

    # Se tem campanha ativa
    if suggestion.get("active_campaigns"):
        campaign = suggestion["active_campaigns"][0]
        script = campaign.get("script", "")

        if client_name:
            script = f"{client_name}, {script}"

        return script

    # Se tem upsell
    if suggestion.get("upsell_opportunities"):
        upsell = suggestion["upsell_opportunities"][0]
        script = upsell.get("script", "")

        if client_name:
            script = f"{client_name}, {script}"

        return script

    return ""
