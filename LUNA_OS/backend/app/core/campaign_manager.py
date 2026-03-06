"""
LUNA CORE - Campaign Manager
Gerencia a ativação e detecção de campanhas dinâmicas.
"""

from typing import List, Dict, Optional
from loguru import logger
from datetime import datetime

# [LAZY LOADING] Não importar na importação do módulo
# Importar apenas quando necessário (lazy loading)


class CampaignManager:
    def __init__(self):
        self.db = None  # [LAZY LOADING] Inicializar como None
        self.active_campaigns = []
        self.last_sync = None
        self._alerted_on_failure = False  # Prevent alert spam

    def _get_db(self):
        """[LAZY LOADING] Obter Supabase client apenas quando necessário"""
        if self.db is None:
            try:
                from app.integrations.supabase_client import get_supabase
                self.db = get_supabase()
            except Exception as e:
                logger.warning(f"⚠️ CampaignManager: Supabase não disponível - {e}")
                self.db = None
        return self.db

    async def sync_campaigns(self):
        """Busca campanhas ativas do Supabase."""
        try:
            db = self._get_db()  # [LAZY LOADING] Obter DB apenas quando necessário

            if db is None:
                logger.warning("⚠️ CampaignManager: Supabase não inicializado - usando fallback")
                self.active_campaigns = []
                self.last_sync = datetime.utcnow()

                # [DEBT #3] Alert on failure (prevent spam with flag)
                if not self._alerted_on_failure:
                    try:
                        from app.integrations.alert_system import alert_system, AlertSeverity
                        alert_system.send_alert(
                            title="⚠️ CampaignManager: Supabase Offline",
                            message="Campanhas não estão sendo aplicadas. Verificar conexão Supabase.",
                            severity=AlertSeverity.HIGH,
                            tags=["degraded", "campaigns", "supabase"]
                        )
                        self._alerted_on_failure = True
                    except Exception as alert_err:
                        logger.debug(f"Could not send alert: {alert_err}")
                return

            now = datetime.utcnow().isoformat()
            # Busca campanhas ativas onde a data atual está no intervalo
            result = (
                db.table("campaigns").select("*").eq("status", "active").execute()
            )

            raw_campaigns = result.data or []
            self.active_campaigns = []

            for camp in raw_campaigns:
                start = camp.get("start_date")
                end = camp.get("end_date")

                # Filtro de data (opcional)
                is_valid = True
                if start and now < start:
                    is_valid = False
                if end and now > end:
                    is_valid = False

                if is_valid:
                    self.active_campaigns.append(camp)

            self.last_sync = datetime.utcnow()
            self._alerted_on_failure = False  # Reset alert flag on success
            logger.info(
                f"🚀 CampaignManager: {len(self.active_campaigns)} campanhas ativas carregadas."
            )

        except Exception as e:
            logger.error(f"❌ Erro ao sincronizar campanhas: {e}")
            self.active_campaigns = []
            self.last_sync = datetime.utcnow()

    def detect_campaign(self, message: str) -> Optional[Dict]:
        """Detecta se uma mensagem aciona alguma campanha ativa via trigger_keywords."""
        msg_lower = message.lower()

        for camp in self.active_campaigns:
            keywords = camp.get("trigger_keywords") or []
            if any(kw.lower() in msg_lower for kw in keywords):
                return camp
        return None

    def get_campaign_context(self, campaign: Dict) -> str:
        """Gera um bloco de texto para o System Prompt com os dados da campanha."""
        name = campaign.get("name", "Campanha")
        msg = campaign.get("message_template", "")
        disc_p = campaign.get("discount_percent")
        disc_f = campaign.get("discount_fixed")

        context = f"### CAMPANHA ATIVA DETECTADA: {name}\n"
        if disc_p:
            context += f"- Desconto: {disc_p}%\n"
        if disc_f:
            context += f"- Desconto: R$ {disc_f}\n"
        if msg:
            context += f"- Diretriz de Mensagem: {msg}\n"

        return context


# [LAZY LOADING] Instanciar sob demanda
# A instância é criada quando o módulo é importado no main.py
campaign_manager = CampaignManager()
