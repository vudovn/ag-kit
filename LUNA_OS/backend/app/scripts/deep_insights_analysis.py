#!/usr/bin/env python3
"""
🌙💼 LUNA OS — DEEP INSIGHTS ANALYSIS
Análise Profunda dos Dados Extraídos (38K conversas)
Gera insights avançados de vendas e comportamento
"""

import json
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
import re

LOGS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")

def load_filtered_data():
    """Carrega dados filtrados mais recentes"""
    print("📂 Carregando dados filtrados...")
    
    files = sorted(LOGS_DIR.glob("filtered_conversations_*.json"))
    if not files:
        print("❌ Nenhum arquivo filtrado encontrado!")
        return None
    
    latest = files[-1]
    print(f"   📄 {latest.name}")
    
    with open(latest, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   ✅ {len(data):,} conversas carregadas")
    return data

def analyze_by_service(conversations):
    """Analisa por tipo de serviço mencionado"""
    print("\n🔍 Analisando por serviço...")
    
    service_keywords = {
        'escova': ['escova', 'escovaria', 'cabelo'],
        'unha': ['unha', 'gel', 'alongamento', 'manicure'],
        'make': ['make', 'maquiagem', 'maquiador'],
        'sobrancelha': ['sobrancelha', 'brow', 'design'],
        'massagem': ['massagem', 'relaxar'],
        'progressiva': ['progressiva', 'alisamento'],
        'coloracao': ['coloracao', 'tintura', 'mechas'],
        'pacote': ['pacote', 'combo', 'promocao'],
        'noiva': ['noiva', 'casamento', 'noivas'],
    }
    
    services_count = defaultdict(int)
    
    for conv in conversations:
        # Buscar em mensagens ou notas
        content = str(conv.get('notes', '') + ' ' + str(conv.get('intent', ''))).lower()
        
        for service, keywords in service_keywords.items():
            if any(kw in content for kw in keywords):
                services_count[service] += 1
    
    # Ordenar
    sorted_services = dict(sorted(services_count.items(), key=lambda x: x[1], reverse=True))
    
    print(f"   ✅ {len(sorted_services)} serviços identificados")
    return sorted_services

def analyze_by_hour(conversations):
    """Analisa distribuição por horário"""
    print("\n🔍 Analisando por horário...")
    
    by_hour = defaultdict(int)
    by_day_of_week = defaultdict(int)
    
    for conv in conversations:
        started = conv.get('started_at', '')
        if len(started) >= 13:
            # Extrair hora
            try:
                hour = int(started[11:13])
                by_hour[hour] += 1
                
                # Dia da semana (0=Monday, 6=Sunday)
                from datetime import datetime as dt
                date_obj = dt.fromisoformat(started.replace('Z', '+00:00'))
                day = date_obj.weekday()
                by_day_of_week[day] += 1
            except:
                pass
    
    by_hour_sorted = dict(sorted(by_hour.items()))
    by_day_sorted = dict(sorted(by_day_of_week.items()))
    
    print(f"   ✅ Horário e dia analisados")
    return by_hour_sorted, by_day_sorted

def analyze_client_lifetime(conversations):
    """Analisa lifetime value por cliente"""
    print("\n🔍 Analisando lifetime por cliente...")
    
    client_stats = defaultdict(lambda: {
        'conversations': 0,
        'first_contact': None,
        'last_contact': None,
        'intents': [],
        'sentiments': []
    })
    
    for conv in conversations:
        phone = conv.get('clean_phone') or conv.get('phone')
        if not phone:
            continue
        
        stats = client_stats[phone]
        stats['conversations'] += 1
        
        started = conv.get('started_at')
        if started:
            if not stats['first_contact'] or started < stats['first_contact']:
                stats['first_contact'] = started
            if not stats['last_contact'] or started > stats['last_contact']:
                stats['last_contact'] = started
        
        intent = conv.get('intent')
        if intent:
            stats['intents'].append(intent)
        
        sentiment = conv.get('sentiment')
        if sentiment:
            stats['sentiments'].append(sentiment)
    
    # Calcular métricas
    for phone, stats in client_stats.items():
        # Dias entre primeiro e último contato
        if stats['first_contact'] and stats['last_contact']:
            try:
                first = datetime.fromisoformat(stats['first_contact'].replace('Z', '+00:00'))
                last = datetime.fromisoformat(stats['last_contact'].replace('Z', '+00:00'))
                stats['lifetime_days'] = (last - first).days
            except:
                stats['lifetime_days'] = 0
        else:
            stats['lifetime_days'] = 0
        
        # Intenção mais comum
        if stats['intents']:
            stats['top_intent'] = Counter(stats['intents']).most_common(1)[0][0]
        else:
            stats['top_intent'] = None
        
        # Sentimento predominante
        if stats['sentiments']:
            stats['top_sentiment'] = Counter(stats['sentiments']).most_common(1)[0][0]
        else:
            stats['top_sentiment'] = None
    
    print(f"   ✅ {len(client_stats)} clientes analisados")
    return dict(client_stats)

def identify_churn_risk(client_stats, days_threshold=90):
    """Identifica clientes em risco de churn"""
    print("\n🔍 Identificando risco de churn...")
    
    at_risk = []
    now = datetime.utcnow()
    
    for phone, stats in client_stats.items():
        if stats['last_contact']:
            try:
                last = datetime.fromisoformat(stats['last_contact'].replace('Z', '+00:00'))
                days_since = (now - last).days
                
                if days_since > days_threshold:
                    at_risk.append({
                        'phone': phone,
                        'days_since': days_since,
                        'total_conversations': stats['conversations'],
                        'top_intent': stats['top_intent'],
                        'top_sentiment': stats['top_sentiment']
                    })
            except:
                pass
    
    # Ordenar por dias
    at_risk.sort(key=lambda x: x['days_since'], reverse=True)
    
    print(f"   ✅ {len(at_risk)} clientes em risco ({days_threshold}+ dias)")
    return at_risk

def generate_actionable_insights(services, by_hour, by_day, client_stats, churn_risk):
    """Gera insights acionáveis"""
    insights = []
    
    # Serviços mais populares
    if services:
        top_service = list(services.items())[0]
        insights.append({
            'type': 'opportunity',
            'category': 'services',
            'title': f'🎯 Serviço Mais Popular: {top_service[0]}',
            'desc': f'{top_service[1]} menções',
            'action': f'Criar campanhas focadas em {top_service[0]}'
        })
    
    # Horário de pico
    if by_hour:
        peak_hour = max(by_hour, key=by_hour.get)
        insights.append({
            'type': 'info',
            'category': 'timing',
            'title': f'🕐 Horário de Pico: {peak_hour}h',
            'desc': f'{by_hour[peak_hour]} conversas',
            'action': f'Reforçar equipe das {peak_hour-1}h às {peak_hour+1}h'
        })
    
    # Dia da semana
    if by_day:
        days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        peak_day_idx = max(by_day, key=by_day.get)
        peak_day = days[peak_day_idx] if peak_day_idx < len(days) else 'Unknown'
        insights.append({
            'type': 'info',
            'category': 'timing',
            'title': f'📅 Dia Mais Movimentado: {peak_day}',
            'desc': f'{by_day[peak_day_idx]} conversas',
            'action': f'Planejar promoções para dias mais lentos'
        })
    
    # Churn risk
    if churn_risk:
        high_value_risk = [c for c in churn_risk if c['total_conversations'] > 5][:5]
        if high_value_risk:
            insights.append({
                'type': 'critical',
                'category': 'retention',
                'title': f'🔴 {len(churn_risk)} Clientes em Risco de Churn',
                'desc': f'{len(high_value_risk)} são de alto valor (5+ conversas)',
                'action': 'Campanha urgente de reativação com oferta personalizada'
            })
    
    # Clientes VIP
    vip_clients = [p for p, s in client_stats.items() if s['conversations'] >= 10]
    if vip_clients:
        insights.append({
            'type': 'opportunity',
            'category': 'vip',
            'title': f'💎 {len(vip_clients)} Clientes VIP',
            'desc': '10+ conversas cada',
            'action': 'Programa de fidelidade exclusivo para VIPs'
        })
    
    return insights

def print_deep_insights_report(services, by_hour, by_day, client_stats, churn_risk, insights):
    """Imprime relatório de insights profundos"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — DEEP INSIGHTS ANALYSIS                        ║")
    print("║     Análise Profunda de Comportamento e Vendas              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Serviços
    print("─" * 70)
    print("🎯 SERVIÇOS MENCIONADOS")
    print("─" * 70)
    if services:
        for service, count in list(services.items())[:10]:
            print(f"  • {service.title()}: {count:,} menções")
    else:
        print("  Sem dados de serviços detectados")
    print()
    
    # Horário
    print("─" * 70)
    print("🕐 DISTRIBUIÇÃO POR HORÁRIO")
    print("─" * 70)
    if by_hour:
        max_val = max(by_hour.values())
        for hour in range(24):
            count = by_hour.get(hour, 0)
            if count > 0:
                bar = "█" * int(count / max_val * 30)
                print(f"  {hour:02d}h: {bar} {count:,}")
    print()
    
    # Dia da semana
    print("─" * 70)
    print("📅 DISTRIBUIÇÃO POR DIA DA SEMANA")
    print("─" * 70)
    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    if by_day:
        max_val = max(by_day.values())
        for day_idx, count in by_day.items():
            day_name = days[day_idx] if day_idx < len(days) else f'Dia {day_idx}'
            bar = "█" * int(count / max_val * 30)
            print(f"  {day_name:10s}: {bar} {count:,}")
    print()
    
    # Clientes
    print("─" * 70)
    print("👥 ANÁLISE DE CLIENTES")
    print("─" * 70)
    print(f"  Total Clientes: {len(client_stats):,}")
    
    # Distribuição por conversas
    conv_dist = Counter(s['conversations'] for s in client_stats.values())
    print(f"\n  Por Volume de Conversas:")
    for convs, count in sorted(conv_dist.items(), reverse=True)[:10]:
        print(f"    • {convs} conversas: {count:,} clientes")
    
    # VIPs
    vips = [p for p, s in client_stats.items() if s['conversations'] >= 10]
    print(f"\n  💎 Clientes VIP (10+ conversas): {len(vips)}")
    if vips:
        print(f"    Top 5: {', '.join(vips[:5])}")
    print()
    
    # Churn
    print("─" * 70)
    print("⚠️  RISCO DE CHURN")
    print("─" * 70)
    print(f"  Clientes em Risco: {len(churn_risk):,} (90+ dias sem contato)")
    if churn_risk:
        high_value = [c for c in churn_risk if c['total_conversations'] > 3][:10]
        if high_value:
            print(f"\n  🔴 Alto Valor em Risco (3+ conversas):")
            for client in high_value:
                print(f"    • {client['phone']}: {client['days_since']} dias | {client['total_conversations']} convs")
    print()
    
    # Insights
    print("─" * 70)
    print("💡 INSIGHTS ACIONÁVEIS")
    print("─" * 70)
    for i, insight in enumerate(insights, 1):
        icon = insight['type'].replace('critical', '🔴').replace('warning', '🟡').replace('opportunity', '💰').replace('info', 'ℹ️')
        print(f"\n{icon} {i}. {insight['title']}")
        print(f"   📊 {insight['desc']}")
        print(f"   💡 {insight['action']}")
    print()

def save_deep_analysis(services, by_hour, by_day, client_stats, churn_risk, insights):
    """Salva análise profunda"""
    OUTPUT_DIR = LOGS_DIR
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Salvar análise completa
    analysis = {
        'generated_at': datetime.now().isoformat(),
        'services': services,
        'by_hour': by_hour,
        'by_day': by_day,
        'client_stats_count': len(client_stats),
        'churn_risk_count': len(churn_risk),
        'churn_risk_sample': churn_risk[:100],  # Primeiros 100
        'insights': insights
    }
    
    output_file = OUTPUT_DIR / f"deep_insights_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Análise salva em: {output_file}")
    print()

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Deep Insights Analysis              ║")
    print("║     Análise Profunda de 38K Conversas            ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Load data
    conversations = load_filtered_data()
    
    if not conversations:
        return
    
    # Analyze
    services = analyze_by_service(conversations)
    by_hour, by_day = analyze_by_hour(conversations)
    client_stats = analyze_client_lifetime(conversations)
    churn_risk = identify_churn_risk(client_stats)
    insights = generate_actionable_insights(services, by_hour, by_day, client_stats, churn_risk)
    
    # Print report
    print_deep_insights_report(services, by_hour, by_day, client_stats, churn_risk, insights)
    
    # Save
    save_deep_analysis(services, by_hour, by_day, client_stats, churn_risk, insights)
    
    print("✅ Análise profunda concluída!")
    print()

if __name__ == "__main__":
    main()
