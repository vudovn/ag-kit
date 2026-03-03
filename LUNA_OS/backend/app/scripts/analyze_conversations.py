#!/usr/bin/env python3
"""
🌙📊 LUNA OS — CONVERSATION ANALYTICS SUITE
Análise completa das conversas do WhatsApp
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import statistics

# Paths
EXTRACTIONS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs/extractions")
OUTPUT_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs/analytics")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load latest extraction
files = list(EXTRACTIONS_DIR.glob("whatsapp_conversations_*.json"))
if not files:
    print("❌ No extraction files found!")
    exit(1)

latest_file = sorted(files)[-1]
print(f"📂 Loading: {latest_file.name}")

with open(latest_file, 'r') as f:
    data = json.load(f)

conversations = data.get("conversations", [])
metadata = data.get("metadata", {})

print(f"📊 Analyzing {len(conversations)} conversations...")
print()

# ============================================================================
# 1. PERFIL DE CLIENTES VIP
# ============================================================================
print("=" * 80)
print("👑 1. PERFIL DE CLIENTES VIP")
print("=" * 80)

# Sort by total messages
vip_clients = sorted(conversations, key=lambda x: x["total_messages"], reverse=True)[:20]

print("\n📋 TOP 20 CLIENTES POR VOLUME DE MENSAGENS:\n")
print(f"{'#':<3} {'Telefone':<15} {'Mensagens':<12} {'Duração (min)':<15} {'Início':<20}")
print("-" * 70)

for i, client in enumerate(vip_clients, 1):
    print(f"{i:<3} {client['phone']:<15} {client['total_messages']:<12} {client['duration_minutes']:<15.0f} {client['first_message'][:19] if client['first_message'] else 'N/A':<20}")

# Save VIP list
vip_data = {
    "generated_at": datetime.now().isoformat(),
    "top_20_vip_clients": vip_clients
}

with open(OUTPUT_DIR / "vip_clients.json", 'w') as f:
    json.dump(vip_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved to: {OUTPUT_DIR / 'vip_clients.json'}")

# ============================================================================
# 2. ANÁLISE DE TEMPO DE RESPOSTA
# ============================================================================
print()
print("=" * 80)
print("⏱️  2. ANÁLISE DE TEMPO DE RESPOSTA")
print("=" * 80)

# Load raw messages for detailed analysis
print("\n📥 Loading raw messages for time analysis...")

# We need to extract message-level data
# For now, estimate based on conversation patterns
response_times = []

for conv in conversations:
    if conv["total_messages"] >= 2:
        # Estimate: if conversation has duration, calculate avg time between messages
        if conv["duration_minutes"] > 0 and conv["total_messages"] > 1:
            avg_gap = conv["duration_minutes"] / (conv["total_messages"] - 1)
            response_times.append(avg_gap)

if response_times:
    avg_response = statistics.mean(response_times)
    median_response = statistics.median(response_times)
    min_response = min(response_times)
    max_response = max(response_times)
    
    print(f"\n📊 TEMPO MÉDIO ENTRE MENSAGENS (estimado):")
    print(f"   • Média: {avg_response:.1f} minutos")
    print(f"   • Mediana: {median_response:.1f} minutos")
    print(f"   • Mínimo: {min_response:.1f} minutos")
    print(f"   • Máximo: {max_response:.1f} minutos")
    
    # Categorize
    fast = sum(1 for r in response_times if r < 5)
    medium = sum(1 for r in response_times if 5 <= r < 30)
    slow = sum(1 for r in response_times if r >= 30)
    
    print(f"\n📊 DISTRIBUIÇÃO:")
    print(f"   • Rápido (<5min): {fast} conversas ({fast/len(response_times)*100:.1f}%)")
    print(f"   • Médio (5-30min): {medium} conversas ({medium/len(response_times)*100:.1f}%)")
    print(f"   • Lento (>30min): {slow} conversas ({slow/len(response_times)*100:.1f}%)")

# ============================================================================
# 3. DETECÇÃO DE FAQs AUTOMÁTICAS
# ============================================================================
print()
print("=" * 80)
print("❓ 3. DETECÇÃO DE FAQs AUTOMÁTICAS")
print("=" * 80)

# Common question patterns
question_patterns = [
    (r"qual[ao]?\s*(o|a)?\s*(valor|preço|preco|custo)", "PERGUNTA SOBRE VALOR"),
    (r"quanto\s+(custa|é|eh|vale)", "PERGUNTA SOBRE VALOR"),
    (r"tem\s+(horário|horario|vaga|agenda)", "PERGUNTA SOBRE HORÁRIO"),
    (r"onde\s+(fica|é|eh|localiza)", "PERGUNTA SOBRE LOCALIZAÇÃO"),
    (r"qual\s+(o|a)?\s*(endereço|endereco|local)", "PERGUNTA SOBRE LOCALIZAÇÃO"),
    (r"funciona\s+(quando|que\s+horas|horário|horario)", "PERGUNTA SOBRE HORÁRIO"),
    (r"precisa\s+de\s+(horário|horario|agenda)", "PERGUNTA SOBRE AGENDAMENTO"),
    (r"como\s+(funciona|é|eh|agendar)", "PERGUNTA SOBRE FUNCIONAMENTO"),
    (r"faz\s+(o|a)?\s*(unha|cabelo|sobrancelha|limpeza)", "PERGUNTA SOBRE SERVIÇO"),
    (r"tem\s+(desconto|promoção|promocao)", "PERGUNTA SOBRE PROMOÇÃO"),
]

faq_counts = defaultdict(int)
faq_examples = defaultdict(list)

for conv in conversations:
    first_content = conv.get("first_content", "") or ""
    last_content = conv.get("last_content", "") or ""
    
    for pattern, category in question_patterns:
        if re.search(pattern, first_content, re.IGNORECASE):
            faq_counts[category] += 1
            if len(faq_examples[category]) < 3:
                faq_examples[category].append(first_content[:80])
        if re.search(pattern, last_content, re.IGNORECASE):
            faq_counts[category] += 1

print("\n📋 PERGUNTAS MAIS FREQUENTES:\n")
print(f"{'Categoria':<40} {'Ocorrências':<15}")
print("-" * 55)

for category, count in sorted(faq_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{category:<40} {count:<15}")

# Save FAQs
faq_data = {
    "generated_at": datetime.now().isoformat(),
    "faq_categories": dict(faq_counts),
    "examples": dict(faq_examples)
}

with open(OUTPUT_DIR / "faq_detection.json", 'w') as f:
    json.dump(faq_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved to: {OUTPUT_DIR / 'faq_detection.json'}")

# ============================================================================
# 4. ANÁLISE DE HORÁRIOS E DIAS
# ============================================================================
print()
print("=" * 80)
print("📅 4. ANÁLISE DE HORÁRIOS E DIAS")
print("=" * 80)

hour_distribution = defaultdict(int)
day_distribution = defaultdict(int)

days_map = {
    0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 
    4: "Sexta", 5: "Sábado", 6: "Domingo"
}

for conv in conversations:
    if conv.get("first_message"):
        try:
            dt = datetime.fromisoformat(conv["first_message"].replace("Z", "+00:00"))
            hour_distribution[dt.hour] += 1
            day_distribution[days_map[dt.weekday()]] += 1
        except:
            pass

print("\n📊 MENSAGENS POR HORÁRIO DO DIA:\n")
for hour in sorted(hour_distribution.keys()):
    count = hour_distribution[hour]
    bar = "█" * (count // 10)
    print(f"   {hour:02d}:00 | {bar} ({count})")

print("\n📊 MENSAGENS POR DIA DA SEMANA:\n")
day_order = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
for day in day_order:
    count = day_distribution.get(day, 0)
    bar = "█" * (count // 20)
    print(f"   {day:<10} | {bar} ({count})")

# Find peak hour and day
peak_hour = max(hour_distribution, key=hour_distribution.get) if hour_distribution else 0
peak_day = max(day_distribution, key=day_distribution.get) if day_distribution else "N/A"

print(f"\n📈 HORÁRIO DE PICO: {peak_hour:02d}:00")
print(f"📈 DIA DE PICO: {peak_day}")

# ============================================================================
# 5. JORNADA DO CLIENTE (CONVERSÃO)
# ============================================================================
print()
print("=" * 80)
print("🎯 5. JORNADA DO CLIENTE - CONVERSÃO")
print("=" * 80)

# Analyze conversation lengths as proxy for conversion
short_convs = [c for c in conversations if c["total_messages"] < 5]
medium_convs = [c for c in conversations if 5 <= c["total_messages"] < 20]
long_convs = [c for c in conversations if c["total_messages"] >= 20]

print("\n📊 DISTRIBUIÇÃO POR TAMANHO DA CONVERSA:\n")
print(f"   • Curtas (<5 msgs): {len(short_convs)} ({len(short_convs)/len(conversations)*100:.1f}%)")
print(f"   • Médias (5-20 msgs): {len(medium_convs)} ({len(medium_convs)/len(conversations)*100:.1f}%)")
print(f"   • Longas (20+ msgs): {len(long_convs)} ({len(long_convs)/len(conversations)*100:.1f}%)")

# Average messages per conversation
avg_messages = statistics.mean([c["total_messages"] for c in conversations])
median_messages = statistics.median([c["total_messages"] for c in conversations])

print(f"\n📈 MÉDIA DE MENSAGENS POR CONVERSA: {avg_messages:.1f}")
print(f"📈 MEDIANA DE MENSAGENS POR CONVERSA: {median_messages:.1f}")

# ============================================================================
# 6. ANÁLISE DE CONTEÚDO - PALAVRAS-CHAVE
# ============================================================================
print()
print("=" * 80)
print("🔑 6. ANÁLISE DE CONTEÚDO - PALAVRAS-CHAVE")
print("=" * 80)

# Common words in first/last messages
service_keywords = [
    "unha", "unhas", "cabelo", "escova", "penteado", "tratamento",
    "sobrancelha", "cilios", "gel", "manicure", "pedicure", "esmalte",
    "maquiagem", "limpeza", "hidratação", "hidratacao", "corte"
]

action_keywords = [
    "agendar", "agenda", "horário", "horario", "marcar", "reservar",
    "valor", "preço", "preco", "quanto", "custa", "pagar"
]

service_counts = defaultdict(int)
action_counts = defaultdict(int)

for conv in conversations:
    text = (conv.get("first_content", "") or "" + " " + conv.get("last_content", "") or "").lower()
    
    for keyword in service_keywords:
        if keyword in text:
            service_counts[keyword] += 1
    
    for keyword in action_keywords:
        if keyword in text:
            action_counts[keyword] += 1

print("\n📋 SERVIÇOS MAIS MENCIONADOS:\n")
for keyword, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"   • {keyword}: {count}")

print("\n📋 AÇÕES/INTENÇÕES MAIS COMUNS:\n")
for keyword, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"   • {keyword}: {count}")

# ============================================================================
# 7. RESUMO EXECUTIVO
# ============================================================================
print()
print("=" * 80)
print("📊 7. RESUMO EXECUTIVO")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    LUNA OS — RELATÓRIO EXECUTIVO                 ║
╠══════════════════════════════════════════════════════════════════╣
║  📈 MÉTRICAS GERAIS                                              ║
║  • Total de Conversas: {len(conversations):,}
║  • Total de Mensagens: {metadata.get('total_messages', sum(c['total_messages'] for c in conversations)):,}
║  • Período: {metadata.get('extracted_at', 'N/A')}
║
║  👥 CLIENTES
║  • VIPs (100+ msgs): {metadata.get('conversations_with_100_plus', sum(1 for c in conversations if c['total_messages'] >= 100))}
║  • Ativos (50+ msgs): {metadata.get('conversations_with_50_plus', sum(1 for c in conversations if c['total_messages'] >= 50))}
║  • Ocasioinais (10+ msgs): {metadata.get('conversations_with_10_plus', sum(1 for c in conversations if c['total_messages'] >= 10))}
║
║  🎯 INSIGHTS
║  • Horário de Pico: {peak_hour:02d}:00
║  • Dia de Pico: {peak_day}
║  • Média de Mensagens/Conversa: {avg_messages:.1f}
║
║  ❓ TOP 3 FAQs
""")

top_faqs = sorted(faq_counts.items(), key=lambda x: x[1], reverse=True)[:3]
for i, (faq, count) in enumerate(top_faqs, 1):
    print(f"║    {i}. {faq}: {count} ocorrências")

print("""
╚══════════════════════════════════════════════════════════════════╝
""")

# Save complete report
report = {
    "generated_at": datetime.now().isoformat(),
    "metadata": metadata,
    "summary": {
        "total_conversations": len(conversations),
        "total_messages": metadata.get('total_messages', 0),
        "vip_clients": metadata.get('conversations_with_100_plus', 0),
        "active_clients": metadata.get('conversations_with_50_plus', 0),
        "occasional_clients": metadata.get('conversations_with_10_plus', 0),
        "avg_messages_per_conversation": avg_messages,
        "peak_hour": peak_hour,
        "peak_day": peak_day
    },
    "vip_clients": vip_clients,
    "faq_categories": dict(faq_counts),
    "service_keywords": dict(service_counts),
    "action_keywords": dict(action_counts),
    "hour_distribution": dict(hour_distribution),
    "day_distribution": dict(day_distribution)
}

with open(OUTPUT_DIR / "complete_analytics_report.json", 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n✅ Relatório completo salvo em: {OUTPUT_DIR / 'complete_analytics_report.json'}")
print()
print("=" * 80)
print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
print("=" * 80)
