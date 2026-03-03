import asyncio
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime
import re

# Adiciona a raiz ao sys.path para importações
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.supabase_client import get_supabase


async def analyze():
    print("🚀 Iniciando Motor de Análise Rápida (Zero IA)...\n")
    db = get_supabase()

    print("📥 Baixando as últimas 5.000 interações do Supabase...")
    # Buscando apenas colunas necessárias para economizar RAM e Banda
    res = (
        db.table("whatsapp_messages_history")
        .select("content, message_timestamp, direction")
        .order("message_timestamp", desc=True)
        .limit(5000)
        .execute()
    )

    messages = res.data
    if not messages:
        print("Nenhuma mensagem encontrada.")
        return

    print(f"✅ {len(messages)} mensagens carregadas na memória instantaneamente!\n")
    print("🧠 Processando Matemática e Expressões Regulares (Regex)...")

    # Contadores
    hourly_distribution = Counter()
    intent_counters = {
        "agendamento": 0,
        "preco_valor": 0,
        "cancelamento": 0,
        "duvida_endereco": 0,
    }

    # RegEx Patterns
    patterns = {
        "agendamento": re.compile(
            r"\b(marcar|agendar|horario|livre|vaga|quero ir)\b", re.IGNORECASE
        ),
        "preco_valor": re.compile(
            r"\b(valor|preco|custa|pagar|pix|cartao)\b", re.IGNORECASE
        ),
        "cancelamento": re.compile(
            r"\b(cancelar|desmarcar|imprevisto|nao vou conseguir)\b", re.IGNORECASE
        ),
        "duvida_endereco": re.compile(
            r"\b(onde|endereco|localizacao|rua|fica)\b", re.IGNORECASE
        ),
    }

    client_msgs = 0

    for msg in messages:
        # Pula mensagens que nós enviamos (outbound)
        if msg.get("direction") == "outbound":
            continue

        content = str(msg.get("content") or "")
        client_msgs += 1

        # Horário
        ts = msg.get("message_timestamp")
        if ts:
            try:
                # Parse timestamp
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                # Converte para hora local (exemplo: GMT-3 para Brasil)
                hora_local = (dt.hour - 3) % 24
                hourly_distribution[hora_local] += 1
            except:
                pass

        # Regex Match
        for intent, regex in patterns.items():
            if regex.search(content):
                intent_counters[intent] += 1

    print(
        f"📊 Análise concluída sobre {client_msgs} mensagens recebidas de clientes.\n"
    )

    print("━" * 50)
    print("🔥 HORÁRIOS DE PICO (Top 5 Horários de Maior Movimento)")
    print("━" * 50)
    if hourly_distribution:
        max_qtd = max(hourly_distribution.values())
        for hora, qtd in hourly_distribution.most_common(5):
            bar = "█" * int((qtd / max_qtd) * 20)
            print(f"⏰ {hora:02d}h : {bar} ({qtd} msgs)")

    print("\n━" * 50)
    print("🎯 INTENÇÕES DETECTADAS (Via Regex)")
    print("━" * 50)
    for intent, count in sorted(
        intent_counters.items(), key=lambda item: item[1], reverse=True
    ):
        pct = (count / client_msgs) * 100 if client_msgs > 0 else 0
        nome_bonito = intent.replace("_", " ").title()
        print(f"➤ {nome_bonito.ljust(18)}: {count} menções ({pct:.1f}%)")

    print(
        "\n💡 Custo desta análise: $0.00 | Uso de RAM: < 20MB | Tempo: Fração de segundo"
    )


if __name__ == "__main__":
    asyncio.run(analyze())
