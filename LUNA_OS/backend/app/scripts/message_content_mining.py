#!/usr/bin/env python3
"""
🌙💼 LUNA OS — MESSAGE CONTENT MINING
Acessa o Supabase diretamente para buscar CONTEÚDO COMPLETO das mensagens
Encontra situações reais de encaixes, negociações e agendamentos complexos
"""

import httpx
import json
import os
from datetime import datetime
from pathlib import Path

# Config do Supabase (do .env)
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://sktrmwogifeuzrcnpvsw.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Carregar do .env se existir
env_file = Path('/Users/franciscotaveira.ads/LUNA OS/.env')
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

def test_supabase_connection():
    """Testa conexão com Supabase"""
    print("🔍 Testando conexão com Supabase...")
    print(f"   URL: {SUPABASE_URL[:50]}...")
    
    try:
        response = httpx.get(
            f"{SUPABASE_URL}/rest/v1/whatsapp_messages_history",
            headers=HEADERS,
            params={'limit': 1},
            timeout=10.0
        )
        
        if response.status_code == 200:
            print(f"   ✅ Conexão OK!")
            return True
        else:
            print(f"   ⚠️ Status: {response.status_code}")
            print(f"   {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def fetch_messages_with_content(limit=10000, offset=0):
    """Busca mensagens COM CONTEÚDO"""
    print(f"\n📥 Buscando mensagens ({limit} a partir de {offset})...")
    
    try:
        response = httpx.get(
            f"{SUPABASE_URL}/rest/v1/whatsapp_messages_history",
            headers=HEADERS,
            params={
                'limit': limit,
                'offset': offset,
                'order': 'message_timestamp.desc'
            },
            timeout=120.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data)} mensagens recebidas")
            return data
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   {response.text[:300]}")
            return []
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return []

def find_scheduling_situations(messages):
    """Busca situações de agendamento complexo no conteúdo"""
    
    scheduling_keywords = {
        'encaixe': ['encaixar', 'encaixo', 'consegue encaixar', 'ajeitar', 'brecha', 'horarinho'],
        'multiplos': ['e também', 'além de', 'mais', 'também quero', 'fazer dois', 'pacote', 'combo'],
        'tempo': ['demora', 'quanto tempo', 'horas', 'minutos', 'rápido', 'pressa', 'urgente'],
        'profissionais': ['com outra', 'atendendo', 'ocupada', 'finalizando', 'livre', 'disponível'],
        'sequencia': ['primeiro', 'depois', 'enquanto', 'antes', 'quando terminar', 'inicia', 'continua'],
        'negociacao': ['pode ser', 'se importa', 'tudo bem', 'aceita', 'prefere', 'outro dia'],
        'conflito': ['não tem', 'sem horário', 'lotado', 'cheio', 'não dá', 'impossível', 'complicado'],
        'solucao': ['que tal', 'sugestão', 'podemos', 'assim funciona', 'resolve', 'dá certo']
    }
    
    situations = []
    
    for msg in messages:
        content = (msg.get('content') or '').lower()
        direction = msg.get('direction', 'unknown')
        phone = msg.get('phone', 'unknown')
        
        # Buscar categorias encontradas
        categories_found = []
        for category, keywords in scheduling_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    categories_found.append(category)
                    break
        
        # Se encontrou pelo menos 2 categorias = situação complexa
        if len(categories_found) >= 2:
            situations.append({
                'phone': phone,
                'direction': direction,
                'content': msg.get('content'),
                'timestamp': msg.get('message_timestamp'),
                'categories': list(set(categories_found)),
                'complexity': len(set(categories_found))
            })
    
    return situations

def print_mining_results(situations, total_messages):
    """Imprime resultados da mineração"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — MESSAGE CONTENT MINING                        ║")
    print("║     Situações Reais de Agendamento Complexo                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    print("─" * 70)
    print("📊 RESUMO")
    print("─" * 70)
    print(f"📥 Mensagens Analisadas: {total_messages:,}")
    print(f"✅ Situações Complexas: {len(situations):,}")
    print(f"📈 Percentual: {len(situations)/max(total_messages,1)*100:.3f}%")
    print()
    
    if situations:
        print("─" * 70)
        print("💬 EXEMPLOS REAIS (Top 20)")
        print("─" * 70)
        
        # Ordenar por complexidade
        situations.sort(key=lambda x: x['complexity'], reverse=True)
        
        for i, sit in enumerate(situations[:20], 1):
            print(f"\n{i}. 📱 {sit['phone']} ({sit['direction']})")
            print(f"   Complexidade: {sit['complexity']} categorias | {', '.join(sit['categories'])}")
            print(f"   🕐 {sit['timestamp']}")
            print(f"   💬 \"{sit['content'][:200]}...\"")
        
        print()
        print("─" * 70)
        print("🎯 CATEGORIAS MAIS COMUNS")
        print("─" * 70)
        
        from collections import Counter
        all_cats = []
        for sit in situations:
            all_cats.extend(sit['categories'])
        
        cat_counts = Counter(all_cats)
        for cat, count in cat_counts.most_common(10):
            print(f"  • {cat}: {count} ocorrências")
        
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
    6. PLANO B: Sempre ter opção secundária
        """)
    else:
        print("⚠️ Nenhuma situação complexa encontrada nas mensagens analisadas")
        print("   Possíveis causas:")
        print("   1. Supabase sem chave de acesso")
        print("   2. Tabela whatsapp_messages_history vazia")
        print("   3. Mensagens sem conteúdo de agendamento")
    
    print()

def save_mining_results(situations):
    """Salva resultados"""
    OUTPUT_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Salvar situações
    situations_file = OUTPUT_DIR / f"message_mining_situations_{timestamp}.json"
    with open(situations_file, 'w', encoding='utf-8') as f:
        json.dump(situations[:1000], f, indent=2, ensure_ascii=False)  # Top 1000
    
    print(f"💾 Situações salvas: {situations_file}")
    print(f"   ({min(len(situations), 1000)} registros)")
    print()

def main():
    """Main"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Message Content Mining              ║")
    print("║     Busca CONTEÚDO REAL das mensagens            ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Testar conexão
    if not test_supabase_connection():
        print("\n❌ Não foi possível conectar ao Supabase")
        print("\nPara acessar o conteúdo completo das mensagens:")
        print("1. Verifique se SUPABASE_KEY está no .env")
        print("2. Execute: cd '/Users/franciscotaveira.ads/LUNA OS'")
        print("3. Execute: python3 backend/app/scripts/message_content_mining.py")
        return
    
    # Buscar mensagens (primeiras 10.000)
    messages = fetch_messages_with_content(limit=10000, offset=0)
    
    if not messages:
        print("\n⚠️ Nenhuma mensagem retornada")
        return
    
    # Buscar situações complexas
    situations = find_scheduling_situations(messages)
    
    # Imprimir resultados
    print_mining_results(situations, len(messages))
    
    # Salvar
    save_mining_results(situations)
    
    print("✅ Mineração de conteúdo concluída!")
    print()

if __name__ == "__main__":
    main()
