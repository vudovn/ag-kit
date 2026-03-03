#!/usr/bin/env python3
"""
🌙💼 LUNA OS — DEEP MESSAGE EXTRACTION
Extrai TODAS as mensagens do WhatsApp com RIQUEZA DE DETALHES
Foco: Situações complexas de agendamento, encaixes, negociações
"""

import httpx
import json
from pathlib import Path
from datetime import datetime
import time

# Carregar creds do .env
env_file = Path('/Users/franciscotaveira.ads/LUNA OS/.env')
SUPABASE_URL = ''
SUPABASE_KEY = ''

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key == 'SUPABASE_URL':
                    SUPABASE_URL = value
                elif key == 'SUPABASE_KEY':
                    SUPABASE_KEY = value

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

OUTPUT_DIR = Path('/Users/franciscotaveira.ads/LUNA OS/logs')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_all_messages_batch(batch_size=1000, max_batches=40):
    """Extrai mensagens em lotes menores com controle"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 DEEP MESSAGE EXTRACTION                       ║")
    print("║     Extraindo TODAS as mensagens do WhatsApp      ║")
    print("╚════════════════════════════════════════════════════╝")
    print()

    all_messages = []
    offset = 0
    total_fetched = 0

    for batch_num in range(max_batches):
        print(f"📥 Lote {batch_num + 1}/{max_batches} ({batch_size} mensagens)...")

        try:
            response = httpx.get(
                f'{SUPABASE_URL}/rest/v1/whatsapp_messages_history',
                headers=HEADERS,
                params={
                    'limit': batch_size,
                    'offset': offset,
                    'order': 'message_timestamp.desc'
                },
                timeout=60.0
            )

            if response.status_code == 200:
                batch = response.json()

                if not batch or len(batch) == 0:
                    print(f"   ✅ Fim dos dados")
                    break

                all_messages.extend(batch)
                total_fetched += len(batch)

                print(f"   ✅ Total: {total_fetched:,} mensagens")

                # Pausa maior entre lotes
                time.sleep(1.0)

                offset += batch_size
            else:
                print(f"   ❌ Erro: {response.status_code}")
                break

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            break

    return all_messages

def analyze_message_content(messages):
    """Analisa conteúdo em busca de situações complexas"""
    print("\n")
    print("🔍 Analisando conteúdo das mensagens...")
    print()
    
    # Categorias de situações complexas
    complex_patterns = {
        'multi_servico': [
            'também quero', 'além de', 'e também', 'dois serviços', 'três',
            'pacote', 'combo', 'completo', 'faz tudo', 'tudo junto'
        ],
        'encaixe': [
            'encaixar', 'encaixe', 'consegue', 'ajeitar', 'brecha',
            'horarinho', 'vê se tem', 'qualquer horário'
        ],
        'tempo': [
            'demora', 'quanto tempo', 'horas', 'minutos', 'rápido',
            'pressa', 'urgente', 'correndo', 'tempo livre'
        ],
        'profissional': [
            'com outra', 'atendendo', 'ocupada', 'finalizando', 'terminando',
            'livre', 'disponível', 'agenda dela', 'a outra'
        ],
        'sequencia': [
            'primeiro', 'depois', 'enquanto', 'antes', 'quando terminar',
            'inicia', 'continua', 'passa para', 'emenda', 'sequência'
        ],
        'negociacao': [
            'pode ser', 'se importa', 'tudo bem', 'aceita', 'prefere',
            'outro dia', 'outra hora', 'melhor', 'compensa'
        ],
        'conflito': [
            'não tem', 'sem horário', 'lotado', 'cheio', 'não dá',
            'impossível', 'não consigo', 'complicado', 'difícil'
        ],
        'solucao': [
            'que tal', 'sugestão', 'podemos', 'assim funciona', 'resolve',
            'dá certo', 'funciona', 'perfeito', 'ótimo', 'combinado'
        ],
        'espera': [
            'aguardar', 'esperar', 'chegar antes', 'chegar depois',
            'já chegar', 'vir mais cedo', 'ficar na espera', 'sala de espera'
        ],
        'lavar_cabelo': [
            'lavar', 'lavatório', 'shampoo', 'molhar', 'enxaguar',
            'couro cabeludo', 'hidratação', 'banho'
        ]
    }
    
    complex_messages = []
    
    for msg in messages:
        content = (msg.get('content') or '').lower()
        direction = msg.get('direction', 'unknown')
        
        # Apenas mensagens com conteúdo significativo
        if len(content) < 20:
            continue
        
        # Encontrar padrões
        patterns_found = []
        for category, keywords in complex_patterns.items():
            for keyword in keywords:
                if keyword in content:
                    patterns_found.append(category)
                    break
        
        # Se encontrou pelo menos 1 padrão complexo
        if patterns_found:
            complex_messages.append({
                'phone': msg.get('phone'),
                'direction': direction,
                'content': msg.get('content'),
                'timestamp': msg.get('message_timestamp'),
                'patterns': list(set(patterns_found)),
                'complexity': len(set(patterns_found)),
                'sender_name': msg.get('sender_name'),
                'is_group': msg.get('is_group'),
                'metadata': msg.get('metadata', {})
            })
        
        if len(complex_messages) % 500 == 0:
            print(f"   📊 {len(complex_messages):,} situações complexas encontradas")
    
    print(f"   ✅ {len(complex_messages):,} situações complexas encontradas")
    
    # Ordenar por complexidade
    complex_messages.sort(key=lambda x: x['complexity'], reverse=True)
    
    return complex_messages

def print_deep_analysis(complex_messages, total_messages):
    """Imprime análise profunda"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 DEEP MESSAGE ANALYSIS — SITUAÇÕES COMPLEXAS            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    print("─" * 70)
    print("📊 RESUMO DA ANÁLISE")
    print("─" * 70)
    print(f"📥 Total Mensagens: {total_messages:,}")
    print(f"✅ Situações Complexas: {len(complex_messages):,}")
    print(f"📈 Percentual: {len(complex_messages)/max(total_messages,1)*100:.3f}%")
    print()
    
    if complex_messages:
        print("─" * 70)
        print("💬 TOP 30 SITUAÇÕES MAIS COMPLEXAS")
        print("─" * 70)
        print()
        
        for i, msg in enumerate(complex_messages[:30], 1):
            print(f"{i}. 📱 {msg['phone']} | {msg['direction']} | Complexidade: {msg['complexity']}")
            print(f"   Padrões: {', '.join(msg['patterns'])}")
            print(f"   🕐 {msg['timestamp']}")
            print(f"   💬 \"{msg['content'][:250]}...\"")
            print()
        
        print("─" * 70)
        print("🎯 PADRÕES MAIS COMUNS")
        print("─" * 70)
        
        from collections import Counter
        all_patterns = []
        for msg in complex_messages:
            all_patterns.extend(msg['patterns'])
        
        pattern_counts = Counter(all_patterns)
        for pattern, count in pattern_counts.most_common(15):
            icon = get_pattern_icon(pattern)
            print(f"  {icon} {pattern.replace('_', ' ').title()}: {count} ocorrências")
        
        print()
        print("─" * 70)
        print("💡 INSIGHTS PARA IA DE AGENDAMENTO")
        print("─" * 70)
        print("""
    Com base nestes exemplos REAIS, a IA precisa aprender:
    
    1. ENCAIXES: Identificar janelas entre atendimentos
    2. MULTI-SERVIÇOS: Sequenciar logicamente (lavar → escova → unha)
    3. PROFISSIONAIS: Coordenar múltiplas equipes
    4. NEGOCIAÇÃO: Oferecer alternativas quando não der encaixe
    5. TEMPO REAL: Entender "finalizando" vs "ocupada"
    6. PLANO B: Sempre ter alternativa quando não der encaixe
    7. SEQUENCIAMENTO: Ordem lógica dos serviços
    8. ESPERA: Gerenciar sala de espera virtual/física
        """)
    else:
        print("⚠️ Nenhuma situação complexa encontrada")

def get_pattern_icon(pattern):
    """Retorna ícone para padrão"""
    icons = {
        'multi_servico': '📦',
        'encaixe': '🔧',
        'tempo': '⏱️',
        'profissional': '👥',
        'sequencia': '🔗',
        'negociacao': '🤝',
        'conflito': '⚠️',
        'solucao': '💡',
        'espera': '⏳',
        'lavar_cabelo': '🚿'
    }
    return icons.get(pattern, '📊')

def save_deep_results(complex_messages, all_messages):
    """Salva resultados completos"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Salvar TODAS as mensagens
    all_file = OUTPUT_DIR / f"all_messages_full_{timestamp}.json"
    with open(all_file, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, indent=2, ensure_ascii=False)
    print(f"💾 TODAS mensagens: {all_file} ({len(all_messages):,} registros)")
    
    # Salvar situações complexas
    complex_file = OUTPUT_DIR / f"complex_situations_{timestamp}.json"
    with open(complex_file, 'w', encoding='utf-8') as f:
        json.dump(complex_messages, f, indent=2, ensure_ascii=False)
    print(f"💾 Situações complexas: {complex_file} ({len(complex_messages):,} registros)")
    
    # Salvar resumo
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_messages': len(all_messages),
        'complex_situations': len(complex_messages),
        'percentage': len(complex_messages)/max(len(all_messages),1)*100,
        'files': {
            'all': str(all_file),
            'complex': str(complex_file)
        }
    }
    
    summary_file = OUTPUT_DIR / f"extraction_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 Resumo: {summary_file}")
    print()

def main():
    """Main function"""
    # Extrair TODAS as mensagens
    all_messages = fetch_all_messages_batch(batch_size=5000)
    
    if not all_messages:
        print("\n❌ Nenhuma mensagem extraída!")
        return
    
    print(f"\n✅ {len(all_messages):,} mensagens extraídas com sucesso!")
    
    # Analisar conteúdo
    complex_messages = analyze_message_content(all_messages)
    
    # Imprimir análise
    print_deep_analysis(complex_messages, len(all_messages))
    
    # Salvar resultados
    save_deep_results(complex_messages, all_messages)
    
    print("✅ Extração e análise PROFUNDAS concluídas!")
    print()

if __name__ == "__main__":
    main()
