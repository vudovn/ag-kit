#!/usr/bin/env python3
"""
🌙💼 LUNA OS — SCHEDULING COMPLEXITY MINING
Extrai situações REAIS de encaixes, negociações e malabarismos de agendamento
Das 38.000 conversas, busca padrões complexos de atendimento
"""

import json
from datetime import datetime
from pathlib import Path
import re

LOGS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")

# Keywords para identificar situações complexas
COMPLEX_PATTERNS = {
    'encaixe': [
        'encaixar', 'encaixo', 'consegue encaixar', 'tem um horarinho',
        'vê se consegue', 'ajeitar', 'encaixe', 'brecha'
    ],
    'multiplos_servicos': [
        'e também', 'além de', 'mais', 'também quero', 'aproveitar e fazer',
        'fazer dois', 'fazer três', 'pacote', 'combo', 'completo'
    ],
    'tempo_negociacao': [
        'demora quanto', 'quanto tempo', 'horário', 'tempo de', 'previsto',
        'duração', 'leva quanto', 'rápido', 'pressa', 'urgente', 'correndo'
    ],
    'profissional_multipla': [
        'com outra', 'atendendo', 'ocupada', 'finalizando', 'terminando',
        'livre', 'disponível', 'agenda', 'horário dela'
    ],
    'sequenciamento': [
        'primeiro', 'depois', 'enquanto', 'antes', 'quando terminar',
        'inicia', 'continua', 'passa para', 'emenda', 'sequência'
    ],
    'negociacao': [
        'pode ser', 'se importa', 'tudo bem', 'aceita', 'concorda',
        'prefere', 'melhor', 'compensa', 'vale a pena', 'outro dia'
    ],
    'lavagem_cabelo': [
        'lavar', 'lavatório', 'shampoo', 'molhar', 'enxaguar',
        'couro cabeludo', 'hidratação'
    ],
    'conflito_agenda': [
        'não tem', 'sem horário', 'lotado', 'cheio', 'sem vaga',
        'impossível', 'não dá', 'não consigo', 'complicado'
    ],
    'solucao_criativa': [
        'que tal', 'sugestão', 'podemos', 'assim funciona', 'resolve',
        'dá certo', 'funciona', 'perfeito', 'ótimo'
    ],
    'cliente_espera': [
        'aguardar', 'esperar', 'chegar antes', 'chegar depois',
        'já chegar', 'vir mais cedo', 'ficar na espera'
    ]
}

def load_filtered_conversations():
    """Carrega conversas filtradas"""
    print("📂 Carregando conversas filtradas...")
    
    files = sorted(LOGS_DIR.glob("filtered_conversations_*.json"))
    if not files:
        print("❌ Nenhum arquivo encontrado!")
        return None
    
    latest = files[-1]
    print(f"   📄 {latest.name}")
    
    with open(latest, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   ✅ {len(data):,} conversas carregadas")
    return data

def find_complex_situations(conversations, min_patterns=3):
    """Busca situações complexas de agendamento"""
    print(f"\n🔍 Buscando situações complexas (min {min_patterns} padrões)...")
    
    complex_cases = []
    
    for i, conv in enumerate(conversations):
        # Coletar todo o texto da conversa
        content_parts = []
        
        # Intent
        if conv.get('intent'):
            content_parts.append(conv['intent'].lower())
        
        # Notes ou outras informações
        if conv.get('notes'):
            content_parts.append(str(conv['notes']).lower())
        
        # Client name pode ter contexto
        if conv.get('client_name'):
            content_parts.append(str(conv['client_name']).lower())
        
        content = ' '.join(content_parts)
        
        # Contar padrões encontrados
        patterns_found = {}
        for category, keywords in COMPLEX_PATTERNS.items():
            for keyword in keywords:
                if keyword in content:
                    if category not in patterns_found:
                        patterns_found[category] = []
                    patterns_found[category].append(keyword)
        
        # Se encontrou múltiplos padrões
        if len(patterns_found) >= min_patterns:
            complex_cases.append({
                'conversation_id': conv.get('id', i),
                'phone': conv.get('clean_phone') or conv.get('phone'),
                'client_name': conv.get('client_name'),
                'intent': conv.get('intent'),
                'status': conv.get('status'),
                'started_at': conv.get('started_at'),
                'patterns_found': patterns_found,
                'pattern_count': len(patterns_found),
                'content_sample': content[:200] if content else None
            })
        
        if (i + 1) % 5000 == 0:
            print(f"   📊 Processadas {i+1:,} | Encontradas {len(complex_cases):,} situações complexas")
    
    print(f"   ✅ {len(complex_cases):,} situações complexas encontradas")
    
    # Ordenar por complexidade
    complex_cases.sort(key=lambda x: x['pattern_count'], reverse=True)
    
    return complex_cases

def analyze_scheduling_patterns(complex_cases):
    """Analisa padrões de agendamento complexo"""
    print("\n🔍 Analisando padrões de agendamento...")
    
    pattern_stats = {}
    by_intent = {}
    by_status = {}
    
    for case in complex_cases:
        # Padrões mais comuns
        for pattern in case['patterns_found'].keys():
            pattern_stats[pattern] = pattern_stats.get(pattern, 0) + 1
        
        # Por intent
        intent = case.get('intent', 'unknown')
        by_intent[intent] = by_intent.get(intent, 0) + 1
        
        # Por status
        status = case.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1
    
    # Ordenar
    pattern_stats = dict(sorted(pattern_stats.items(), key=lambda x: x[1], reverse=True))
    by_intent = dict(sorted(by_intent.items(), key=lambda x: x[1], reverse=True))
    by_status = dict(sorted(by_status.items(), key=lambda x: x[1], reverse=True))
    
    print(f"   ✅ Padrões analisados")
    
    return pattern_stats, by_intent, by_status

def print_scheduling_mining_report(complex_cases, pattern_stats, by_intent, by_status):
    """Imprime relatório de mineração de agendamentos"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — SCHEDULING COMPLEXITY MINING                  ║")
    print("║     Situações Reais de Encaixes e Negociações              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    print("─" * 70)
    print("📊 RESUMO DA MINERAÇÃO")
    print("─" * 70)
    print(f"🔍 Situações Complexas: {len(complex_cases):,}")
    print(f"📊 Total Conversas: 38.000")
    print(f"📈 Percentual Complexo: {len(complex_cases)/38000*100:.2f}%")
    print()
    
    print("─" * 70)
    print("🎯 PADRÕES IDENTIFICADOS (Top 15)")
    print("─" * 70)
    for pattern, count in list(pattern_stats.items())[:15]:
        icon = get_pattern_icon(pattern)
        print(f"  {icon} {pattern.replace('_', ' ').title()}: {count:,} casos")
    print()
    
    print("─" * 70)
    print("📋 POR INTENÇÃO (Top 10)")
    print("─" * 70)
    for intent, count in list(by_intent.items())[:10]:
        print(f"  • {intent}: {count:,} situações complexas")
    print()
    
    print("─" * 70)
    print("📊 POR STATUS")
    print("─" * 70)
    for status, count in by_status.items():
        icon = "✅" if status == 'ended' else "🟡" if status == 'active' else "📁"
        print(f"  {icon} {status}: {count:,}")
    print()
    
    print("─" * 70)
    print("💡 EXEMPLOS DE SITUAÇÕES COMPLEXAS")
    print("─" * 70)
    
    # Mostrar top 10 casos mais complexos
    for i, case in enumerate(complex_cases[:10], 1):
        print(f"\n{i}. Cliente: {case.get('client_name', 'N/A')} | {case.get('phone', 'N/A')}")
        print(f"   Intent: {case.get('intent', 'N/A')} | Status: {case.get('status', 'N/A')}")
        print(f"   Complexidade: {case['pattern_count']} padrões")
        print(f"   Padrões: {', '.join(case['patterns_found'].keys())}")
        if case.get('content_sample'):
            print(f"   Contexto: {case['content_sample'][:150]}...")
    
    print()
    print("─" * 70)
    print("🎯 INSIGHTS PARA IA DE AGENDAMENTO")
    print("─" * 70)
    print("""
    1. ENCAIXES: A IA precisa entender janelas de tempo entre atendimentos
    2. MULTI-SERVIÇOS: Sequenciamento lógico (lavar → escova → unha)
    3. PROFISSIONAIS MÚLTIPLAS: Coordenação entre equipes
    4. NEGOCIAÇÃO: Flexibilidade com preferências da cliente
    5. TEMPO REAL: Status de "finalizando" vs "ocupada"
    6. PLANO B: Sempre ter alternativa quando não der encaixe
    """)
    print()

def get_pattern_icon(pattern):
    """Retorna ícone para padrão"""
    icons = {
        'encaixe': '🔧',
        'multiplos_servicos': '📦',
        'tempo_negociacao': '⏱️',
        'profissional_multipla': '👥',
        'sequenciamento': '🔗',
        'negociacao': '🤝',
        'lavagem_cabelo': '🚿',
        'conflito_agenda': '⚠️',
        'solucao_criativa': '💡',
        'cliente_espera': '⏳'
    }
    return icons.get(pattern, '📊')

def save_mining_results(complex_cases, pattern_stats, by_intent, by_status):
    """Salva resultados da mineração"""
    OUTPUT_DIR = LOGS_DIR
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Salvar casos complexos (top 1000 para não pesar)
    cases_file = OUTPUT_DIR / f"scheduling_complex_cases_{timestamp}.json"
    with open(cases_file, 'w', encoding='utf-8') as f:
        json.dump(complex_cases[:1000], f, indent=2, ensure_ascii=False)
    
    # Salvar análise
    analysis = {
        'generated_at': datetime.now().isoformat(),
        'total_complex_cases': len(complex_cases),
        'pattern_stats': pattern_stats,
        'by_intent': by_intent,
        'by_status': by_status,
        'files': {
            'cases': str(cases_file)
        }
    }
    
    analysis_file = OUTPUT_DIR / f"scheduling_analysis_{timestamp}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Casos complexos: {cases_file}")
    print(f"💾 Análise: {analysis_file}")
    print()

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Scheduling Complexity Mining        ║")
    print("║     Mineração de Encaixes e Negociações Reais    ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Load conversations
    conversations = load_filtered_conversations()
    
    if not conversations:
        return
    
    # Find complex situations
    complex_cases = find_complex_situations(conversations, min_patterns=2)
    
    # Analyze patterns
    pattern_stats, by_intent, by_status = analyze_scheduling_patterns(complex_cases)
    
    # Print report
    print_scheduling_mining_report(complex_cases, pattern_stats, by_intent, by_status)
    
    # Save results
    save_mining_results(complex_cases, pattern_stats, by_intent, by_status)
    
    print("✅ Mineração de agendamentos concluída!")
    print()

if __name__ == "__main__":
    main()
