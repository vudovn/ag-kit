#!/usr/bin/env python3
"""
🌙💼 LUNA OS — ANALYZE EXTRACTED DATA
Analisa TODOS os dados extraídos (19k conversas, 20.5k clientes)
"""

import json
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

LOGS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")

def load_latest_data():
    """Carrega os dados mais recentes"""
    print("📂 Carregando dados extraídos...")
    
    # Find latest files
    conv_files = sorted(LOGS_DIR.glob("all_conversations_*.json"))
    clients_files = sorted(LOGS_DIR.glob("all_clients_*.json"))
    
    if not conv_files or not clients_files:
        print("❌ Nenhum arquivo de extração encontrado!")
        print("   Rode: python3 app/scripts/full_data_extraction.py")
        return None, None
    
    latest_conv = conv_files[-1]
    latest_clients = clients_files[-1]
    
    print(f"   📞 {latest_conv.name}")
    print(f"   👥 {latest_clients.name}")
    
    with open(latest_conv, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    with open(latest_clients, 'r', encoding='utf-8') as f:
        clients = json.load(f)
    
    print(f"   ✅ {len(conversations):,} conversas")
    print(f"   ✅ {len(clients):,} clientes")
    
    return conversations, clients

def analyze_conversations(conversations):
    """Analisa TODAS as conversas"""
    print("\n🔍 Analisando conversas...")
    
    by_status = Counter()
    by_intent = Counter()
    by_sentiment = Counter()
    by_month = defaultdict(int)
    by_client = Counter()
    
    for conv in conversations:
        by_status[conv.get('status', 'unknown')] += 1
        
        intent = conv.get('intent')
        if intent:
            by_intent[intent] += 1
        
        sentiment = conv.get('sentiment')
        if sentiment:
            by_sentiment[sentiment] += 1
        
        started = conv.get('started_at', '')
        if len(started) >= 7:
            by_month[started[:7]] += 1
        
        phone = conv.get('phone')
        if phone:
            by_client[phone] += 1
    
    # Calculate conversion
    ended = by_status.get('ended', 0)
    active = by_status.get('active', 0)
    historical = by_status.get('historical', 0)
    total = len(conversations)
    
    active_base = active + ended
    conversion_rate = (ended / active_base * 100) if active_base > 0 else 0
    
    return {
        'total': total,
        'by_status': dict(by_status),
        'by_intent': dict(by_intent.most_common(30)),
        'by_sentiment': dict(by_sentiment),
        'by_month': dict(sorted(by_month.items())),
        'top_clients': by_client.most_common(20),
        'conversion_rate': conversion_rate,
        'active_count': active,
        'ended_count': ended,
        'historical_count': historical
    }

def analyze_clients(clients):
    """Analisa TODOS os clientes"""
    print("\n🔍 Analisando clientes...")
    
    tagged = 0
    all_tags = Counter()
    by_month = defaultdict(int)
    
    for client in clients:
        tags = client.get('tags', [])
        if tags:
            tagged += 1
            for tag in tags:
                all_tags[tag] += 1
        
        created = client.get('created_at', '')
        if len(created) >= 7:
            by_month[created[:7]] += 1
    
    return {
        'total': len(clients),
        'tagged': tagged,
        'tagged_rate': (tagged / len(clients) * 100) if clients else 0,
        'top_tags': all_tags.most_common(30),
        'by_month': dict(sorted(by_month.items()))
    }

def generate_insights(conv_analysis, client_analysis):
    """Gera insights baseados nos dados completos"""
    insights = []
    
    total_convs = conv_analysis['total']
    total_clients = client_analysis['total']
    conversion_rate = conv_analysis['conversion_rate']
    tagged_rate = client_analysis['tagged_rate']
    
    # Volume
    if total_convs > 10000:
        insights.append({
            'type': 'success',
            'title': '🎯 Volume Enterprise',
            'desc': f'{total_convs:,} conversas registradas',
            'action': 'Implementar automação avançada para escala'
        })
    
    if total_clients > 10000:
        insights.append({
            'type': 'success',
            'title': '👥 Base Sólida',
            'desc': f'{total_clients:,} clientes cadastrados',
            'action': 'Segmentar por valor e comportamento'
        })
    
    # Conversão
    if conversion_rate > 30:
        insights.append({
            'type': 'success',
            'title': '✅ Conversão Excelente',
            'desc': f'{conversion_rate:.1f}% de conversão na base ativa',
            'action': 'Escalar tráfego e manter qualidade'
        })
    elif conversion_rate < 10:
        insights.append({
            'type': 'warning',
            'title': '🟡 Conversão Baixa',
            'desc': f'{conversion_rate:.1f}% de conversão',
            'action': 'Revisar funil e qualificação'
        })
    
    # Tags
    if tagged_rate > 80:
        insights.append({
            'type': 'success',
            'title': '🏷️ Segmentação Avançada',
            'desc': f'{tagged_rate:.1f}% dos clientes taggeados',
            'action': 'Usar para campanhas de LTV'
        })
    
    # Histórico
    historical = conv_analysis['historical_count']
    if historical > total_convs * 0.5:
        insights.append({
            'type': 'warning',
            'title': '📁 Grande Base Histórica',
            'desc': f'{historical:,} conversas históricas ({historical/total_convs*100:.1f}%)',
            'action': 'Analisar com IA e criar campanhas de reativação'
        })
    
    # Reativação potencial
    legacy_tags = sum(1 for tag, _ in client_analysis['top_tags'] if 'legado' in tag.lower() or 'sync' in tag.lower())
    if legacy_tags > 0:
        insights.append({
            'type': 'opportunity',
            'title': '💰 Oportunidade de Reativação',
            'desc': 'Clientes #legado identificados',
            'action': 'Campanha "Volte para a Haven" com 25% OFF'
        })
    
    return insights

def print_full_report(conv_analysis, client_analysis, insights):
    """Imprime relatório completo"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — FULL DATA ANALYSIS REPORT                     ║")
    print("║     Análise Completa dos Dados Extraídos                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    print("─" * 70)
    print("📊 MÉTRICAS GERAIS")
    print("─" * 70)
    print(f"📞 Total Conversas:     {conv_analysis['total']:,}")
    print(f"👥 Total Clientes:      {client_analysis['total']:,}")
    print()
    print(f"🎯 Conversão Real:      {conv_analysis['conversion_rate']:.2f}%")
    print(f"🏷️ Clientes Taggeados:  {client_analysis['tagged']:,} ({client_analysis['tagged_rate']:.1f}%)")
    print()
    
    print("─" * 70)
    print("🎯 FUNIL DE VENDAS")
    print("─" * 70)
    print(f"🟡 Ativas:      {conv_analysis['active_count']:,} ({conv_analysis['active_count']/conv_analysis['total']*100:.2f}%)")
    print(f"✅ Fechadas:    {conv_analysis['ended_count']:,} ({conv_analysis['ended_count']/conv_analysis['total']*100:.2f}%)")
    print(f"📁 Históricas:  {conv_analysis['historical_count']:,} ({conv_analysis['historical_count']/conv_analysis['total']*100:.2f}%)")
    print()
    
    print("─" * 70)
    print("📈 CRESCIMENTO POR MÊS (Top 12)")
    print("─" * 70)
    months = list(conv_analysis['by_month'].items())[-12:]
    max_val = max([v for _, v in conv_analysis['by_month'].items()]) if conv_analysis['by_month'] else 1
    for month, count in months:
        bar = "█" * int(count / max_val * 40)
        print(f"  {month}: {bar} {count:,}")
    print()
    
    print("─" * 70)
    print("💬 INTENÇÕES (Top 20)")
    print("─" * 70)
    intents = conv_analysis['by_intent']
    if isinstance(intents, dict):
        intents = list(intents.items())[:20]
    for intent, count in intents:
        icon = "💰" if intent in ['agendar', 'pacote', 'preco'] else "💬"
        pct = count / conv_analysis['total'] * 100
        print(f"  {icon} {intent}: {count:,} ({pct:.3f}%)")
    print()
    
    print("─" * 70)
    print("😊 SENTIMENTOS")
    print("─" * 70)
    for sentiment, count in conv_analysis['by_sentiment'].items():
        icon = "😊" if sentiment == 'positive' else "😐" if sentiment == 'neutral' else "😟"
        pct = count / conv_analysis['total'] * 100 if conv_analysis['total'] > 0 else 0
        print(f"  {icon} {sentiment}: {count:,} ({pct:.3f}%)")
    print()
    
    print("─" * 70)
    print("🏷️ TOP TAGS")
    print("─" * 70)
    for tag, count in client_analysis['top_tags'][:15]:
        print(f"  🏷️ #{tag}: {count:,}")
    print()
    
    print("─" * 70)
    print("💡 INSIGHTS ESTRATÉGICOS")
    print("─" * 70)
    for i, insight in enumerate(insights, 1):
        icon = insight['type'].replace('critical', '🔴').replace('warning', '🟡').replace('success', '✅').replace('opportunity', '💰').replace('info', 'ℹ️')
        print(f"\n{icon} {i}. {insight['title']}")
        print(f"   📊 {insight['desc']}")
        print(f"   💡 {insight['action']}")
    print()
    
    # Calculate score
    score = 60
    if conv_analysis['total'] > 10000: score += 10
    if client_analysis['tagged_rate'] > 80: score += 10
    if conv_analysis['conversion_rate'] > 30: score += 10
    if conv_analysis['by_sentiment'].get('negative', 0) == 0: score += 10
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"║  🏆 SCORE FINAL: {score}/100{' ' * 42}║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

def save_report(conv_analysis, client_analysis, insights):
    """Salva relatório em JSON"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'conversations': conv_analysis,
        'clients': client_analysis,
        'insights': insights
    }
    
    output_file = LOGS_DIR / f"full_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Relatório salvo em: {output_file}")
    print()

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Full Data Analysis                  ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Load data
    conversations, clients = load_latest_data()
    
    if not conversations or not clients:
        return
    
    # Analyze
    conv_analysis = analyze_conversations(conversations)
    client_analysis = analyze_clients(clients)
    
    # Generate insights
    insights = generate_insights(conv_analysis, client_analysis)
    
    # Print report
    print_full_report(conv_analysis, client_analysis, insights)
    
    # Save
    save_report(conv_analysis, client_analysis, insights)
    
    print("✅ Análise completa!")
    print()

if __name__ == "__main__":
    main()
