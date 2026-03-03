import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Dict

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.supabase_client import get_supabase
from app.core.brain import BrainEngine
from loguru import logger
import json

logger.add("logs/diagnostic.log", rotation="10 MB", retention="7 days")


class LossDiagnostician:
    def __init__(self):
        self.db = get_supabase()
        self.brain = BrainEngine()
        self.kb_path = (
            Path(__file__).parent.parent / "knowledge" / "data" / "haven.json"
        )
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.haven_data = json.load(f)

    def get_service_price(self, service_name: str) -> float:
        """Tenta encontrar o preço do serviço no haven.json"""
        for svc in self.haven_data.get("services", []):
            if service_name.lower() in svc.get(
                "name", ""
            ).lower() or service_name.lower() in svc.get("keywords", []):
                return float(svc.get("price") or 0)
        return 0.0

    async def analyze_conversation_loss(self, phone: str, messages: List[Dict]) -> Dict:
        """
        Analisa se uma conversa resultou em perda e qual o valor estimado.
        """
        # Agrupar conteúdo para análise semântica
        full_text = " ".join(
            [m.get("content", "") for m in messages if m.get("direction") == "inbound"]
        )

        # Simular classificação de intenção e detecção de perda
        # Em produção, usaríamos o BrainEngine para classificar a conversa inteira
        loss_detected = False
        potential_value = 0.0
        service_detected = "unknown"

        # Heurística simples para o diagnóstico inicial
        if (
            "quanto" in full_text.lower()
            or "preço" in full_text.lower()
            or "valor" in full_text.lower()
        ):
            # Cliente perguntou preço
            # Se não houver resposta outbound com agendamento confirmado, pode ser perda
            has_confirmation = any(
                [
                    "confirmado" in m.get("content", "").lower()
                    for m in messages
                    if m.get("direction") == "outbound"
                ]
            )
            if not has_confirmation:
                loss_detected = True

                # Tentar detectar o serviço para atribuir valor
                for svc in self.haven_data.get("services", []):
                    if svc["name"].lower() in full_text.lower():
                        potential_value = float(svc.get("price") or 0)
                        service_detected = svc["name"]
                        break

        return {
            "loss_detected": loss_detected,
            "potential_value": potential_value,
            "service": service_detected,
            "phone": phone,
        }

    async def run_diagnostic(self, days: int = 1825):  # 5 anos
        logger.info(f"📊 Iniciando Diagnóstico de Perdas (Últimos {days} dias)...")

        # 1. Buscar mensagens do histórico
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        result = (
            self.db.table("whatsapp_messages_history")
            .select("*")
            .gte("message_timestamp", start_date.isoformat())
            .order("message_timestamp", desc=False)
            .execute()
        )

        history = result.data or []
        if not history:
            logger.warning("⚠️ Nenhum histórico encontrado para análise.")
            return

        # 2. Agrupar por contato
        conversations_by_phone = {}
        for msg in history:
            phone = msg["phone"]
            if phone not in conversations_by_phone:
                conversations_by_phone[phone] = []
            conversations_by_phone[phone].append(msg)

        logger.info(f"🔍 Analisando {len(conversations_by_phone)} contatos únicos...")

        total_loss = 0.0
        loss_count = 0
        service_stats = {}

        # 3. Analisar cada conversa
        for phone, msgs in conversations_by_phone.items():
            analysis = await self.analyze_conversation_loss(phone, msgs)
            if analysis["loss_detected"]:
                total_loss += analysis["potential_value"]
                loss_count += 1
                svc = analysis["service"]
                service_stats[svc] = service_stats.get(svc, 0) + 1

        # 4. Salvar resultado consolidado
        diagnostic_entry = {
            "period_start": start_date.strftime("%Y-%m-%d"),
            "period_end": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_leads": len(conversations_by_phone),
            "converted_leads": len(conversations_by_phone) - loss_count,
            "potential_revenue": total_loss
            + 1000.0,  # Placeholder para cálculo real de conversão
            "actual_revenue": 1000.0,
            "estimated_loss": total_loss,
            "top_lost_services": [
                s
                for s, _ in sorted(
                    service_stats.items(), key=lambda x: x[1], reverse=True
                )[:5]
            ],
            "diagnostic_report": f"Análise concluída. Detectadas {loss_count} perdas potenciais totalizando R${total_loss:.2f}.",
        }

        self.db.table("financial_diagnostic").insert(diagnostic_entry).execute()

        logger.info(f"🏆 Diagnóstico Concluído!")
        logger.info(f"   Perda Estimada: R${total_loss:.2f}")
        logger.info(f"   Contatos perdidos: {loss_count}")


if __name__ == "__main__":
    diag = LossDiagnostician()
    asyncio.run(diag.run_diagnostic())
