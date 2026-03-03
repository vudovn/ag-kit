#!/usr/bin/env python3
"""
🌙💼 LUNA OS — ENTERPRISE SALES INTELLIGENCE REPORT
Relatório em Larga Escala (2000+ contatos, 35000+ conversas)
"""

import httpx
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path
import sys

API_BASE = "http://localhost:8000"

def fetch_paginated(endpoint, max_pages=100, page_size=1000):
    """Busca dados paginados em larga escala"""
    all_data = []
    
    for page in range(max_pages):
        offset = page * page_size
        try:
            response = httpx.get(
                f"{API_BASE}{endpoint}",
                params={"limit": page_size, "offset": offset},
                timeout=60.0
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    all_data.extend(data)
                    print(f"   📊 Página {page+1}: {len(all_data)} registros...")
                else:
                    break
            else:
                break
        except Exception as e:
            print(f"   ⚠️ Erro na página {page}: {e}")
            break
    
    return all_data

def analyze_enterprise_data(conversations, clients, messages_count=35000):
    """Analise em escala enterprise"""
    
    print("\n🔍 Analisando dados em larga escala...")
    
    # Conversas por período
    by_month = defaultdict(int)
    by_status = Counter()
    by_intent = Counter()
    by_sentiment = Counter()
    
    for conv in conversations:
        # Mês
        started = conv.get('started_at', '')
        if len(started) >= 7:
            month = started[:7]  # YYYY-MM
            by_month[month] += 1
        
        # Status
        by_status[conv.get('status', 'unknown')] += 1
        
        # Intent
        intent = conv.get('intent')
        if intent:
            by_intent[intent] += 1
        
        # Sentiment
        sentiment = conv.get('sentiment')
        if sentiment:
            by_sentiment[sentiment] += 1
    
    # Clientes por período
    clients_by_month = defaultdict(int)
    tagged_clients = 0
    all_tags = Counter()
    
    for client in clients:
        created = client.get('created_at', '')
        if len(created) >= 7:
            month = created[:7]
            clients_by_month[month] += 1
        
        tags = client.get('tags', [])
        if tags:
            tagged_clients += 1
            for tag in tags:
                all_tags[tag] += 1
    
    # Crescimento
    total_convs = len(conversations)
    total_clients = len(clients)
    months_active = len(by_month)
    
    avg_convs_per_month = total_convs / max(months_active, 1)
    avg_clients_per_month = total_clients / max(months_active, 1)
    
    # Conversão
    ended = by_status.get('ended', 0)
    active = by_status.get('active', 0)
    historical = by_status.get('historical', 0)
    
    conversion_rate = (ended / total_convs * 100) if total_convs > 0 else 0
    
    # Mensagens por conversa
    avg_messages_per_conv = messages_count / max(total_convs, 1)
    
    return {
        'total_conversations': total_convs,
        'total_clients': total_clients,
        'messages_count': messages_count,
        'months_active': months_active,
        'avg_convs_per_month': avg_convs_per_month,
        'avg_clients_per_month': avg_clients_per_month,
        'avg_messages_per_conv': avg_messages_per_conv,
        'by_month': dict(sorted(by_month.items())),
        'clients_by_month': dict(sorted(clients_by_month.items())),
        'by_status': dict(by_status),
        'by_intent': dict(by_intent.most_common(20)),
        'by_sentiment': dict(by_sentiment),
        'tagged_clients': tagged_clients,
        'tagged_rate': (tagged_clients / total_clients * 100) if total_clients > 0 else 0,
        'top_tags': all_tags.most_common(20),
        'conversion_rate': conversion_rate,
        'active_count': active,
        'ended_count': ended,
        'historical_count': historical
    }

def generate_enterprise_insights(analysis):
    """Gera insights para enterprise"""
    insights = []
    
    # Volume
    if analysis['total_conversations'] > 10000:
        insights.append({
            'type': 'success',
            'title': '🎯 Alto Volume de Conversas',
            'desc': f'{analysis["total_conversations"]:,} conversas registradas',
            'action': 'Implementar automação avançada e IA para escala'
        })
    
    # Base de clientes
    if analysis['total_clients'] > 1000:
        insights.append({
            'type': 'success',
            'title': '👥 Base Sólida de Clientes',
            'desc': f'{analysis["total_clients"]:,} clientes cadastrados',
            'action': 'Segmentar por comportamento e valor'
        })
    
    # Engajamento
    if analysis['avg_messages_per_conv'] > 10:
        insights.append({
            'type': 'success',
            'title': '💬 Alto Engajamento',
            'desc': f'Média de {analysis["avg_messages_per_conv"]:.1f} mensagens/conversa',
            'action': 'Otimizar respostas para reduzir tempo de atendimento'
        })
    
    # Conversão
    if analysis['conversion_rate'] < 10:
        insights.append({
            'type': 'critical',
            'title': '🔴 Conversão Baixa',
            'desc': f'Apenas {analysis["conversion_rate"]:.2f}% de conversão',
            'action': 'Revisar funil, criar urgência, melhorar qualificação'
        })
    elif analysis['conversion_rate'] > 30:
        insights.append({
            'type': 'success',
            'title': '✅ Conversão Excelente',
            'desc': f'{analysis["conversion_rate"]:.2f}% de conversão',
            'action': 'Escalar tráfego e manter qualidade'
        })
    
    # Tags
    if analysis['tagged_rate'] > 80:
        insights.append({
            'type': 'success',
            'title': '🏷️ Segmentação Avançada',
            'desc': f'{analysis["tagged_rate"]:.1f}% dos clientes taggeados',
            'action': 'Usar para campanhas personalizadas e LTV'
        })
    
    # Histórico
    if analysis['historical_count'] > analysis['total_conversations'] * 0.5:
        insights.append({
            'type': 'warning',
            'title': '📁 Grande Base Histórica',
            'desc': f'{analysis["historical_count"]:,} conversas históricas ({analysis["historical_count"]/analysis["total_conversations"]*100:.1f}%)',
            'action': 'Analisar com IA para extrair padrões e reativar'
        })
    
    # Crescimento
    if analysis['months_active'] >= 12:
        insights.append({
            'type': 'info',
            'title': '📈 Trajetória de Crescimento',
            'desc': f'{analysis["months_active"]} meses de operação',
            'action': 'Analisar sazonalidade e planejar picos'
        })
    
    return insights

def print_enterprise_report(analysis, insights):
    """Imprime relatório enterprise"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — ENTERPRISE SALES INTELLIGENCE REPORT          ║")
    print("║     Grande Volume (2000+ contatos, 35000+ conversas)        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    print("─" * 70)
    print("📊 MÉTRICAS GERAIS (ENTERPRISE)")
    print("─" * 70)
    print(f"📞 Total Conversas:     {analysis['total_conversations']:,}")
    print(f"👥 Total Clientes:      {analysis['total_clients']:,}")
    print(f"💬 Mensagens (Sync):    {analysis['messages_count']:,}")
    print(f"📅 Meses Ativos:        {analysis['months_active']}")
    print()
    print(f"📈 Média Conversas/Mês: {analysis['avg_convs_per_month']:,.1f}")
    print(f"📈 Média Clientes/Mês:  {analysis['avg_clients_per_month']:,.1f}")
    print(f"💬 Média Mensagens/Conv: {analysis['avg_messages_per_conv']:.1f}")
    print()
    
    print("─" * 70)
    print("🎯 FUNIL DE VENDAS")
    print("─" * 70)
    print(f"🟡 Ativas:      {analysis['active_count']:,} ({analysis['active_count']/analysis['total_conversations']*100:.2f}%)")
    print(f"✅ Fechadas:    {analysis['ended_count']:,} ({analysis['conversion_rate']:.2f}%)")
    print(f"📁 Históricas:  {analysis['historical_count']:,} ({analysis['historical_count']/analysis['total_conversations']*100:.2f}%)")
    print()
    
    print("─" * 70)
    print("📈 CRESCIMENTO POR PERÍODO")
    print("─" * 70)
    print("\nConversas por Mês (Top 12):")
    months = list(analysis['by_month'].items())[-12:]
    for month, count in months:
        bar = "█" * int(count / max(analysis['by_month'].values()) * 40)
        print(f"  {month}: {bar} {count:,}")
    print()
    
    print("─" * 70)
    print("🏷️ SEGMENTAÇÃO (TAGS)")
    print("─" * 70)
    print(f"Clientes Taggeados: {analysis['tagged_clients']:,} ({analysis['tagged_rate']:.1f}%)")
    print("\nTop 10 Tags:")
    for tag, count in analysis['top_tags'][:10]:
        print(f"  🏷️ #{tag}: {count:,}")
    print()
    
    print("─" * 70)
    print("💬 INTENÇÕES (TOP 15)")
    print("─" * 70)
    for intent, count in list(analysis['by_intent'].items())[:15]:
        icon = "💰" if intent in ['agendar', 'pacote', 'preco'] else "💬"
        pct = count / analysis['total_conversations'] * 100
        print(f"  {icon} {intent}: {count:,} ({pct:.2f}%)")
    print()
    
    print("─" * 70)
    print("😊 SENTIMENTOS")
    print("─" * 70)
    for sentiment, count in analysis['by_sentiment'].items():
        icon = "😊" if sentiment == 'positive' else "😐" if sentiment == 'neutral' else "😟"
        pct = count / analysis['total_conversations'] * 100 if analysis['total_conversations'] > 0 else 0
        print(f"  {icon} {sentiment}: {count:,} ({pct:.2f}%)")
    print()
    
    print("─" * 70)
    print("💡 INSIGHTS ESTRATÉGICOS")
    print("─" * 70)
    for i, insight in enumerate(insights, 1):
        icon = insight['type'].replace('critical', '🔴').replace('warning', '🟡').replace('success', '✅').replace('info', 'ℹ️')
        print(f"\n{icon} {i}. {insight['title']}")
        print(f"   📊 {insight['desc']}")
        print(f"   💡 {insight['action']}")
    print()
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🏆 FIM DO RELATÓRIO ENTERPRISE                             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Enterprise Report Generator         ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Fetch dados
    print("📊 Coletando dados em larga escala...")
    print()
    
    print("   📞 Buscando conversas (pode demorar)...")
    conversations = fetch_paginated("/api/conversations", max_pages=50, page_size=1000)
    print(f"   ✅ {len(conversations):,} conversas encontradas")
    print()
    
    print("   👥 Buscando clientes (pode demorar)...")
    clients = fetch_paginated("/api/clients", max_pages=20, page_size=500)
    print(f"   ✅ {len(clients):,} clientes encontrados")
    print()
    
    # Analisa
    analysis = analyze_enterprise_data(conversations, clients)
    
    # Gera insights
    insights = generate_enterprise_insights(analysis)
    
    # Imprime
    print_enterprise_report(analysis, insights)
    
    # Salva
    report = {
        'generated_at': datetime.now().isoformat(),
        'analysis': analysis,
        'insights': insights
    }
    
    # Salva na pasta oficial LUNA OS
    output_dir = Path("/Users/franciscotaveira.ads/LUNA OS/logs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"enterprise_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"💾 Relatório completo salvo em: {output_path}")
    print()

if __name__ == "__main__":
    main()
