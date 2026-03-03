#!/usr/bin/env python3
"""
🌙💼 LUNA OS — WhatsApp Sales Intelligence Report (API Version)
Relatório Rápido via API - Sem dependência de DB direto
"""

import httpx
import json
from datetime import datetime
from collections import Counter
from pathlib import Path

# Configuração
API_BASE = "http://localhost:8000"

def fetch_api(endpoint):
    """Busca dados da API"""
    try:
        response = httpx.get(f"{API_BASE}{endpoint}", timeout=30.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"❌ Erro ao buscar {endpoint}: {e}")
        return None

def analyze_conversations(conversations):
    """Analisa conversas"""
    if not conversations:
        return {}
    
    # Por status
    by_status = Counter(c.get('status', 'unknown') for c in conversations)
    
    # Por intent
    by_intent = Counter(c.get('intent', 'unknown') for c in conversations if c.get('intent'))
    
    # Por sentiment
    by_sentiment = Counter(c.get('sentiment', 'unknown') for c in conversations if c.get('sentiment'))
    
    # Por cliente
    by_client = Counter(c.get('client_name') or c.get('phone', 'unknown') for c in conversations)
    
    return {
        'total': len(conversations),
        'by_status': dict(by_status),
        'by_intent': dict(by_intent.most_common(15)),
        'by_sentiment': dict(by_sentiment),
        'top_clients': by_client.most_common(10)
    }

def analyze_clients(clients):
    """Analisa clientes"""
    if not clients:
        return {}
    
    # Com tags
    tagged = [c for c in clients if c.get('tags')]
    
    # Tags mais comuns
    all_tags = []
    for c in clients:
        all_tags.extend(c.get('tags', []))
    top_tags = Counter(all_tags).most_common(10)
    
    return {
        'total': len(clients),
        'tagged': len(tagged),
        'top_tags': top_tags
    }

def generate_insights(conv_analysis, client_analysis):
    """Gera insights"""
    insights = []
    
    # Volume
    total = conv_analysis.get('total', 0)
    if total < 50:
        insights.append({
            'type': 'warning',
            'title': '📉 Volume Baixo de Conversas',
            'desc': f'Apenas {total} conversas registradas',
            'action': 'Aumentar captação de leads via tráfego pago e orgânico'
        })
    
    # Conversão
    status = conv_analysis.get('by_status', {})
    ended = status.get('ended', 0)
    active = status.get('active', 0)
    if active > 0 and ended > 0:
        conv_rate = (ended / (active + ended)) * 100
        if conv_rate < 30:
            insights.append({
                'type': 'critical',
                'title': '🔴 Taxa de Conversão Baixa',
                'desc': f'Apenas {conv_rate:.1f}% das conversas são fechadas',
                'action': 'Criar follow-up automático e ofertas com urgência'
            })
    
    # Intenção
    intents = conv_analysis.get('by_intent', {})
    high_intent = sum(intents.get(i, 0) for i in ['agendar', 'agendamento', 'pacote', 'preco'])
    if total > 0:
        high_rate = (high_intent / total) * 100
        if high_rate < 20:
            insights.append({
                'type': 'warning',
                'title': '🟡 Baixa Intenção de Compra',
                'desc': f'Apenas {high_rate:.1f}% demonstram interesse real',
                'action': 'Melhorar qualificação de leads e copy de captação'
            })
    
    # Tags
    tags = client_analysis.get('top_tags', [])
    if tags:
        insights.append({
            'type': 'info',
            'title': '🏷️ Tags Mais Usadas',
            'desc': ', '.join([f'{t[0]} ({t[1]})' for t in tags[:5]]),
            'action': 'Usar tags para segmentação de campanhas'
        })
    
    return insights

def print_report():
    """Imprime relatório formatado"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — WHATSAPP SALES INTELLIGENCE REPORT            ║")
    print("║     Análise Completa de Conversas e Vendas                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📡 API: {API_BASE}")
    print()
    
    # Fetch dados
    print("📊 Coletando dados da API (grande volume)...")
    # Busca em páginas para grandes volumes
    all_conversations = []
    all_clients = []

    # Conversas - múltiplas páginas
    print("   📞 Buscando conversas...")
    for offset in range(0, 50000, 1000):
        convs = fetch_api(f"/api/conversations?limit=1000&offset={offset}")
        if convs and len(convs) > 0:
            all_conversations.extend(convs)
            print(f"      {len(all_conversations)} conversas encontradas...")
        else:
            break

    # Clientes - múltiplas páginas
    print("   👥 Buscando clientes...")
    for offset in range(0, 10000, 500):
        clients_batch = fetch_api(f"/api/clients?limit=500&offset={offset}")
        if clients_batch and len(clients_batch) > 0:
            all_clients.extend(clients_batch)
            print(f"      {len(all_clients)} clientes encontrados...")
        else:
            break

    conversations = all_conversations
    clients = all_clients

    analytics = fetch_api("/api/analytics/overview")
    health = fetch_api("/api/health/status")
    
    # Analisa
    print("🔍 Analisando dados...")
    conv_analysis = analyze_conversations(conversations)
    client_analysis = analyze_clients(clients)
    insights = generate_insights(conv_analysis, client_analysis)
    
    print()
    print("─" * 60)
    print("📈 VOLUME DE CONVERSAS")
    print("─" * 60)
    print(f"Total: {conv_analysis.get('total', 0)} conversas")
    
    print(f"\nPor Status:")
    for status, count in conv_analysis.get('by_status', {}).items():
        icon = "✅" if status == 'ended' else "🟡" if status == 'active' else "📁"
        print(f"  {icon} {status}: {count}")
    
    print(f"\nPor Intenção (Top 10):")
    intents = conv_analysis.get('by_intent', {})
    if isinstance(intents, dict):
        intents = list(intents.items())[:10]
    for intent, count in intents:
        icon = "💰" if intent in ['agendar', 'pacote', 'preco'] else "💬"
        print(f"  {icon} {intent}: {count}")
    
    print(f"\nPor Sentimento:")
    for sentiment, count in conv_analysis.get('by_sentiment', {}).items():
        icon = "😊" if sentiment == 'positive' else "😐" if sentiment == 'neutral' else "😟"
        print(f"  {icon} {sentiment}: {count}")
    
    print()
    print("─" * 60)
    print("👥 CLIENTES")
    print("─" * 60)
    print(f"Total: {client_analysis.get('total', 0)} clientes")
    print(f"Com Tags: {client_analysis.get('tagged', 0)}")
    
    tags = client_analysis.get('top_tags', [])
    if tags:
        print(f"\nTop Tags:")
        for tag, count in tags[:5]:
            print(f"  🏷️ #{tag}: {count}")
    
    print()
    print("─" * 60)
    print("🎯 FUNIL DE VENDAS")
    print("─" * 60)
    
    status = conv_analysis.get('by_status', {})
    total = conv_analysis.get('total', 0)
    ended = status.get('ended', 0)
    active = status.get('active', 0)
    historical = status.get('historical', 0)
    
    if total > 0:
        conv_rate = (ended / total) * 100 if total > 0 else 0
        print(f"Leads Totais: {total}")
        print(f"Conversas Ativas: {active} ({(active/total)*100:.1f}%)")
        print(f"Conversas Fechadas: {ended} ({conv_rate:.1f}%)")
        print(f"Históricas: {historical}")
    
    print()
    print("─" * 60)
    print("💡 INSIGHTS ACIONÁVEIS")
    print("─" * 60)
    
    if not insights:
        print("✅ Nenhum insight crítico no momento!")
    else:
        for i, insight in enumerate(insights, 1):
            icon = insight['type'].replace('critical', '🔴').replace('warning', '🟡').replace('info', 'ℹ️')
            print(f"\n{icon} {i}. {insight['title']}")
            print(f"   📊 {insight['desc']}")
            print(f"   💡 Ação: {insight['action']}")
    
    print()
    print("─" * 60)
    print("🏥 SAÚDE DO SISTEMA")
    print("─" * 60)
    
    if health:
        supabase = health.get('supabase', {})
        evolution = health.get('evolution', {})
        print(f"Supabase: {supabase.get('status', 'unknown')} ({supabase.get('latency', 0):.0f}ms)")
        print(f"Evolution: {evolution.get('status', 'unknown')} - {evolution.get('details', 'N/A')}")
        print(f"Status Geral: {health.get('overall', 'unknown').upper()}")
    
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🏆 FIM DO RELATÓRIO                                         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Salva relatório
    report = {
        'generated_at': datetime.now().isoformat(),
        'conversations': conv_analysis,
        'clients': client_analysis,
        'insights': insights,
        'health': health
    }
    
    output_path = Path(__file__).parent / "logs" / f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Relatório completo salvo em: {output_path}")
    print()

if __name__ == "__main__":
    print_report()
