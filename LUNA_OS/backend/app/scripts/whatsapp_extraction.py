#!/usr/bin/env python3
"""
📱 WHATSAPP EXTRACTION — Extração Completa de Conversas (2 anos)

Extrai 100% das conversas do WhatsApp dos últimos 2 anos para:
- Base de treinamento do Dojo
- Análise de padrões reais
- Melhoria da LUNA com dados reais
- 100% Local (Supabase → Obsidian/JSON)

Autor: Agent Flow
Data: 2026-03-01
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase


class WhatsAppExtractor:
    """
    Extrator completo de conversas do WhatsApp.
    """

    def __init__(self):
        self.db = get_supabase()
        self.output_path = (
            Path(os.path.dirname(os.path.dirname(__file__)))
            / "knowledge"
            / "obsidian_vault"
            / "_Archive"
            / "2026"
            / "WhatsApp-Extraction"
        )
        self.output_path.mkdir(parents=True, exist_ok=True)

        logger.info("📱 WhatsApp Extractor inicializado")

    def extract_all_conversations(
        self,
        days_back: int = 730,  # 2 anos
        limit: int = 100000,
        save_format: str = "json",
    ) -> Dict:
        """
        Extrai todas as conversas dos últimos N dias.

        Args:
            days_back: Dias para trás (730 = 2 anos)
            limit: Limite de mensagens
            save_format: Formato de salvamento (json, md, csv)

        Returns:
            Dict: Estatísticas da extração
        """

        logger.info(f"📥 Iniciando extração de {days_back} dias (limite: {limit})")

        # Calcular data inicial
        start_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat()

        # Extrair mensagens
        logger.info("📥 Buscando mensagens do Supabase...")
        result = (
            self.db.table("whatsapp_messages_history")
            .select(
                """
            id,
            phone,
            content,
            direction,
            message_timestamp,
            intent_detected,
            sentiment_detected
        """
            )
            .gte("message_timestamp", start_date)
            .order("message_timestamp", asc=True)
            .limit(limit)
            .execute()
        )

        messages = result.data or []
        logger.info(f"✅ {len(messages)} mensagens encontradas")

        if not messages:
            return {"error": "Nenhuma mensagem encontrada"}

        # Agrupar por conversa (phone)
        conversations = self._group_by_conversation(messages)
        logger.info(f"📱 {len(conversations)} conversas únicas")

        # Salvar em formatos
        stats = {
            "total_messages": len(messages),
            "total_conversations": len(conversations),
            "date_range": {"start": start_date, "end": datetime.utcnow().isoformat()},
            "extraction_timestamp": datetime.utcnow().isoformat(),
        }

        # Salvar JSON completo
        if save_format in ["json", "all"]:
            self._save_json(messages, conversations, stats)

        # Salvar Markdown por conversa
        if save_format in ["md", "all"]:
            self._save_markdown(conversations, stats)

        # Salvar CSV para análise
        if save_format in ["csv", "all"]:
            self._save_csv(messages, stats)

        # Salvar no Obsidian (Insights)
        self._save_to_obsidian(conversations, stats)

        logger.info(f"✅ Extração concluída! Dados salvos em: {self.output_path}")

        return stats

    def _group_by_conversation(self, messages: List[Dict]) -> Dict[str, List[Dict]]:
        """Agrupa mensagens por telefone"""
        conversations = {}

        for msg in messages:
            phone = msg.get("phone", "unknown")
            if phone not in conversations:
                conversations[phone] = []
            conversations[phone].append(msg)

        return conversations

    def _save_json(self, messages: List[Dict], conversations: Dict, stats: Dict):
        """Salva em JSON"""
        # JSON completo
        filepath = self.output_path / "whatsapp-extraction-complete.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "stats": stats,
                    "messages": messages,
                    "conversations": {k: v for k, v in conversations.items()},
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        logger.info(f"📄 JSON salvo: {filepath}")

        # JSON apenas conversas (para Dojo)
        filepath_dojo = self.output_path / "dojo-training-data.json"

        training_data = []
        for phone, msgs in conversations.items():
            if len(msgs) >= 4:  # Mínimo 2 trocas
                training_data.append(
                    {"phone": phone, "messages": msgs, "turns": len(msgs) // 2}
                )

        with open(filepath_dojo, "w", encoding="utf-8") as f:
            json.dump({"training_data": training_data}, f, ensure_ascii=False, indent=2)

        logger.info(f"📄 Dojo training data salvo: {filepath_dojo}")

    def _save_markdown(self, conversations: Dict, stats: Dict):
        """Salva cada conversa em Markdown"""
        folder = self.output_path / "conversations"
        folder.mkdir(parents=True, exist_ok=True)

        for phone, msgs in conversations.items():
            if len(msgs) < 2:
                continue

            filename = f"Conversation-{phone}-{msgs[0]['message_timestamp'][:10]}.md"
            filepath = folder / filename

            content = self._generate_conversation_md(phone, msgs, stats)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        logger.info(f"📝 {len(conversations)} conversas salvas em Markdown")

    def _generate_conversation_md(
        self, phone: str, messages: List[Dict], stats: Dict
    ) -> str:
        """Gera Markdown de uma conversa"""

        conversation_lines = []
        for msg in messages:
            role = "🤖 LUNA" if msg["direction"] == "outbound" else "👤 CLIENTE"
            timestamp = (
                msg["message_timestamp"][11:16]
                if msg.get("message_timestamp")
                else "??:??"
            )
            content = msg["content"]

            conversation_lines.append(f"**[{timestamp}] {role}:** {content}")

        conversation_md = "\n\n".join(conversation_lines)

        return f"""---
type: whatsapp_conversation
phone: {phone}
messages: {len(messages)}
date: {messages[0]['message_timestamp'][:10] if messages else 'unknown'}
tags:
  - whatsapp
  - conversation
  - extraction
---

# 💬 Conversa: {phone}

**Data:** {messages[0]['message_timestamp'][:10] if messages else 'Unknown'}  
**Mensagens:** {len(messages)}  
**Turnos:** {len(messages) // 2}

---

## Conversa

{conversation_md}

---

## 📊 Metadados

- **Telefone:** {phone}
- **Primeira mensagem:** {messages[0]['message_timestamp'] if messages else 'N/A'}
- **Última mensagem:** {messages[-1]['message_timestamp'] if messages else 'N/A'}
- **Intenções detectadas:** {len([m for m in messages if m.get('intent_detected')])}

---

*Extraído via WhatsApp Extraction - {stats['extraction_timestamp'][:10]}*
"""

    def _save_csv(self, messages: List[Dict], stats: Dict):
        """Salva em CSV para análise"""
        import csv

        filepath = self.output_path / "whatsapp-extraction.csv"

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "phone",
                    "content",
                    "direction",
                    "message_timestamp",
                    "intent_detected",
                    "sentiment_detected",
                ],
            )
            writer.writeheader()
            writer.writerows(messages)

        logger.info(f"📊 CSV salvo: {filepath}")

    def _save_to_obsidian(self, conversations: Dict, stats: Dict):
        """Salva resumo no Obsidian"""
        obsidian_path = Path(
            "/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/app/knowledge/obsidian_vault/_Active/03-INTELLIGENCE/Agent-Analysis"
        )
        obsidian_path.mkdir(parents=True, exist_ok=True)

        filename = (
            f"WhatsApp-Extraction-Summary-{datetime.utcnow().strftime('%Y%m%d')}.md"
        )
        filepath = obsidian_path / filename

        # Top 10 conversas por número de mensagens
        top_conversations = sorted(
            conversations.items(), key=lambda x: len(x[1]), reverse=True
        )[:10]

        content = f"""---
type: extraction_summary
created_at: {stats['extraction_timestamp']}
total_messages: {stats['total_messages']}
total_conversations: {stats['total_conversations']}
tags:
  - whatsapp
  - extraction
  - summary
---

# 📱 WhatsApp Extraction Summary

**Data:** {stats['extraction_timestamp'][:10]}  
**Período:** {stats['date_range']['start'][:10]} até {stats['date_range']['end'][:10]}  
**Total Mensagens:** {stats['total_messages']}  
**Total Conversas:** {stats['total_conversations']}

---

## 📊 Top 10 Conversas (por atividade)

| # | Telefone | Mensagens | Turnos |
|---|----------|-----------|--------|
"""

        for i, (phone, msgs) in enumerate(top_conversations, 1):
            content += f"| {i} | {phone} | {len(msgs)} | {len(msgs) // 2} |\n"

        content += f"""
## 📈 Estatísticas

- **Média de mensagens por conversa:** {stats['total_messages'] / stats['total_conversations']:.1f}
- **Período de extração:** {stats['date_range']['start'][:10]} a {stats['date_range']['end'][:10]}
- **Dados brutos:** `_Archive/2026/WhatsApp-Extraction/`

---

## 🔗 Links Relacionados

- [[000_MCT_MASTER_INDEX]]
- [[Intelligence Dashboard]]
- [[Dojo Simulator]]

---

*Gerado via WhatsApp Extraction*
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"📝 Resumo salvo no Obsidian: {filepath}")


if __name__ == "__main__":
    extractor = WhatsAppExtractor()

    print("📱 Iniciando extração do WhatsApp...")
    print("Isso pode levar alguns minutos.")

    stats = extractor.extract_all_conversations(
        days_back=730, limit=100000, save_format="all"  # 2 anos  # json + md + csv
    )

    print("\n✅ Extração concluída!")
    print(f"\n📊 Estatísticas:")
    print(f"  - Total mensagens: {stats.get('total_messages', 0)}")
    print(f"  - Total conversas: {stats.get('total_conversations', 0)}")
    print(
        f"  - Período: {stats.get('date_range', {}).get('start', 'N/A')[:10]} até {stats.get('date_range', {}).get('end', 'N/A')[:10]}"
    )
    print(
        f"\n📁 Dados salvos em: /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/app/knowledge/obsidian_vault/_Archive/2026/WhatsApp-Extraction/"
    )
