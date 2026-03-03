import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.evolution import evolution
from app.integrations.supabase_client import get_supabase
from loguru import logger

logger.add("logs/sync_history.log", rotation="10 MB", retention="7 days")


async def sync_history():
    logger.info("🌙 Iniciando Sincronização de Histórico WhatsApp...")
    db = get_supabase()

    try:
        # 1. Obter todos os chats
        logger.info("📊 Buscando chats na Evolution API...")
        chats = await evolution.get_chats()

        # O retorno do get_chats costuma ser uma lista de objetos de chat
        # Se for v2, pode estar dentro de uma chave
        if isinstance(chats, dict) and "instance" in chats:
            chats = chats.get("data", [])

        logger.info(f"✅ {len(chats)} chats encontrados")

        total_synced = 0

        for chat in chats:
            jid = chat.get("id") or chat.get("jid")
            if not jid or "@g.us" in jid:  # Ignorar grupos
                continue

            phone = jid.split("@")[0]
            logger.info(f"📲 Sincronizando: {phone}...")

            try:
                # 2. Buscar mensagens do chat
                messages = await evolution.fetch_messages(
                    phone, limit=500
                )  # Pegar um bom bloco

                if not messages:
                    continue

                # O retorno do fetchMessages pode variar por versão
                if isinstance(messages, dict):
                    messages = messages.get("messages", []) or messages.get("data", [])

                msgs_to_insert = []
                for msg in messages:
                    # Transformar para o schema do Supabase
                    # Heurística de direção: se key.fromMe for True, é outbound
                    key = msg.get("key", {})
                    direction = "outbound" if key.get("fromMe") else "inbound"

                    # Conteúdo (pode ser texto, imagem, etc - focar em texto por enquanto)
                    content = ""
                    message_payload = msg.get("message", {})
                    if "conversation" in message_payload:
                        content = message_payload["conversation"]
                    elif "extendedTextMessage" in message_payload:
                        content = message_payload["extendedTextMessage"].get("text", "")

                    # Timestamp (Evolution costuma mandar em segundos)
                    ts = msg.get("messageTimestamp")
                    if ts:
                        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    else:
                        dt = datetime.now(timezone.utc)

                    msgs_to_insert.append(
                        {
                            "message_id": key.get("id"),
                            "phone": phone,
                            "content": content,
                            "direction": direction,
                            "message_timestamp": dt.isoformat(),
                            "is_group": False,
                            "metadata": msg,
                        }
                    )

                # 3. Upsert no Supabase
                if msgs_to_insert:
                    # Batch upsert (on_conflict message_id)
                    db.table("whatsapp_messages_history").upsert(
                        msgs_to_insert, on_conflict="message_id"
                    ).execute()
                    total_synced += len(msgs_to_insert)
                    logger.info(
                        f"  ✅ {len(msgs_to_insert)} mensagens sincronizadas para {phone}"
                    )

                # Pequeno delay para não sobrecarregar API
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"❌ Erro ao sincronizar {phone}: {e}")

        logger.info(f"🏆 Sincronização Concluída! Total: {total_synced} mensagens.")

    except Exception as e:
        logger.error(f"❌ Erro fatal na sincronização: {e}")


if __name__ == "__main__":
    asyncio.run(sync_history())
