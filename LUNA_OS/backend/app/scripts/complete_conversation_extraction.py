#!/usr/bin/env python3
"""
🌙💼 LUNA OS — COMPLETE CONVERSATION EXTRACTION
Extrai TODAS as conversas, exclui grupos, mantém apenas atendimentos
Pasta Oficial: /Users/franciscotaveira.ads/LUNA OS
"""

import httpx
import json
from datetime import datetime
from pathlib import Path
import re

API_BASE = "http://localhost:8000"
OUTPUT_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")

# Patterns para identificar grupos
GROUP_PATTERNS = [
    '@g.us',  # WhatsApp groups
    'broadcast',  # Broadcast lists
    'status@',  # Status updates
    '@newsletter',  # Newsletters
]

def is_group(jid_or_phone):
    """Verifica se é um grupo"""
    if not jid_or_phone:
        return True

    text = str(jid_or_phone).lower()
    return any(pattern in text for pattern in GROUP_PATTERNS)

def is_valid_attendimento(jid_or_phone):
    """Verifica se é um atendimento válido (número de telefone real)"""
    if not jid_or_phone:
        return False

    text = str(jid_or_phone)

    # Não deve ser grupo
    if is_group(text):
        return False

    # Deve ter números (pelo menos 8 dígitos)
    digits = re.sub(r'[^0-9]', '', text)
    return len(digits) >= 8

def clean_phone_number(phone_jid):
    """Limpa número de telefone do JID"""
    if not phone_jid:
        return None
    
    # Remove @s.whatsapp.net e outros sufixos
    phone = re.sub(r'@.*$', '', phone_jid)
    
    # Remove caracteres não numéricos
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Adiciona 55 se necessário (Brasil)
    if len(phone) == 10 or len(phone) == 11:
        phone = '55' + phone
    
    return phone if len(phone) >= 10 else None

def fetch_all_conversations(max_pages=200, page_size=1000):
    """Extrai TODAS as conversas"""
    all_conversations = []
    filtered_conversations = []
    groups_excluded = 0
    invalid_excluded = 0
    
    print("\n📞 EXTRAINDO TODAS AS CONVERSAS...")
    print(f"   API: {API_BASE}")
    print(f"   Max páginas: {max_pages}")
    print(f"   Page size: {page_size}")
    print()
    
    for page in range(max_pages):
        offset = page * page_size
        
        try:
            response = httpx.get(
                f"{API_BASE}/api/conversations",
                params={"limit": page_size, "offset": offset},
                timeout=120.0
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data or len(data) == 0:
                    print(f"   ✅ Fim dos dados na página {page+1}")
                    break
                
                all_conversations.extend(data)
                
                # Filtrar
                for conv in data:
                    phone = conv.get('phone') or conv.get('client_phone')
                    
                    # Verificar se é grupo
                    if is_group(phone):
                        groups_excluded += 1
                        continue
                    
                    # Verificar se é atendimento válido
                    if not is_valid_attendimento(phone):
                        invalid_excluded += 1
                        continue
                    
                    # Limpar número
                    clean_phone = clean_phone_number(phone)
                    if clean_phone:
                        conv['clean_phone'] = clean_phone
                        filtered_conversations.append(conv)
                
                if (page + 1) % 10 == 0:
                    print(f"   📊 Página {page+1}: {len(all_conversations):,} total | {len(filtered_conversations):,} válidas")
                
            else:
                print(f"   ⚠️ Status {response.status_code} na página {page+1}")
                break
                
        except Exception as e:
            print(f"   ❌ Erro na página {page+1}: {e}")
            break
    
    print()
    print(f"   ✅ Total extraídas: {len(all_conversations):,}")
    print(f"   🗑️ Grupos excluídos: {groups_excluded:,}")
    print(f"   🗑️ Inválidas excluídas: {invalid_excluded:,}")
    print(f"   ✅ Válidas para análise: {len(filtered_conversations):,}")
    print()
    
    return all_conversations, filtered_conversations, groups_excluded, invalid_excluded

def analyze_filtered_data(conversations):
    """Analisa dados filtrados"""
    print("\n🔍 ANALISANDO DADOS FILTRADOS...")
    
    by_status = {}
    by_intent = {}
    by_sentiment = {}
    by_month = {}
    by_clean_phone = {}
    
    for conv in conversations:
        # Status
        status = conv.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1
        
        # Intent
        intent = conv.get('intent')
        if intent:
            by_intent[intent] = by_intent.get(intent, 0) + 1
        
        # Sentiment
        sentiment = conv.get('sentiment')
        if sentiment:
            by_sentiment[sentiment] = by_sentiment.get(sentiment, 0) + 1
        
        # Month
        started = conv.get('started_at', '')
        if len(started) >= 7:
            month = started[:7]
            by_month[month] = by_month.get(month, 0) + 1
        
        # Clean phone
        clean_phone = conv.get('clean_phone')
        if clean_phone:
            by_clean_phone[clean_phone] = by_clean_phone.get(clean_phone, 0) + 1
    
    # Calculate conversion
    ended = by_status.get('ended', 0)
    active = by_status.get('active', 0)
    active_base = active + ended
    conversion_rate = (ended / active_base * 100) if active_base > 0 else 0
    
    unique_clients = len(by_clean_phone)
    
    analysis = {
        'total_filtered': len(conversations),
        'unique_clients': unique_clients,
        'by_status': by_status,
        'by_intent': dict(sorted(by_intent.items(), key=lambda x: x[1], reverse=True)[:30]),
        'by_sentiment': by_sentiment,
        'by_month': dict(sorted(by_month.items())),
        'top_clients': dict(sorted(by_clean_phone.items(), key=lambda x: x[1], reverse=True)[:20]),
        'conversion_rate': conversion_rate,
        'active_count': active,
        'ended_count': ended
    }
    
    print(f"   ✅ Análise concluída")
    print(f"   📊 Clientes únicos: {unique_clients:,}")
    print(f"   📊 Conversão: {conversion_rate:.2f}%")
    print()
    
    return analysis

def save_results(all_convs, filtered_convs, analysis, groups_excluded, invalid_excluded):
    """Salva todos os resultados"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save all conversations
    all_file = OUTPUT_DIR / f"all_conversations_raw_{timestamp}.json"
    with open(all_file, 'w', encoding='utf-8') as f:
        json.dump(all_convs, f, indent=2, ensure_ascii=False)
    print(f"💾 Todas (raw): {all_file}")
    
    # Save filtered conversations
    filtered_file = OUTPUT_DIR / f"filtered_conversations_{timestamp}.json"
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_convs, f, indent=2, ensure_ascii=False)
    print(f"💾 Filtradas: {filtered_file}")
    
    # Save analysis
    analysis_file = OUTPUT_DIR / f"filtered_analysis_{timestamp}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"💾 Análise: {analysis_file}")
    
    # Save summary
    summary = {
        'extracted_at': datetime.now().isoformat(),
        'total_extracted': len(all_convs),
        'groups_excluded': groups_excluded,
        'invalid_excluded': invalid_excluded,
        'filtered_count': len(filtered_convs),
        'unique_clients': analysis['unique_clients'],
        'conversion_rate': analysis['conversion_rate'],
        'files': {
            'all': str(all_file),
            'filtered': str(filtered_file),
            'analysis': str(analysis_file)
        }
    }
    
    summary_file = OUTPUT_DIR / f"extraction_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 Resumo: {summary_file}")
    print()
    
    return summary

def print_final_report(summary, analysis):
    """Imprime relatório final"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — COMPLETE CONVERSATION EXTRACTION              ║")
    print("║     Filtro: Grupos Excluídos | Apenas Atendimentos          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    print("─" * 70)
    print("📊 RESUMO DA EXTRAÇÃO")
    print("─" * 70)
    print(f"📥 Total Extraídas:     {summary['total_extracted']:,}")
    print(f"🗑️ Grupos Excluídos:    {summary['groups_excluded']:,}")
    print(f"🗑️ Inválidas Excluídas: {summary['invalid_excluded']:,}")
    print(f"✅ Válidas para Análise: {summary['filtered_count']:,}")
    print(f"👥 Clientes Únicos:     {summary['unique_clients']:,}")
    print()
    
    print("─" * 70)
    print("🎯 FUNIL DE VENDAS (FILTRADO)")
    print("─" * 70)
    print(f"🟡 Ativas:     {analysis['active_count']:,} ({analysis['active_count']/summary['filtered_count']*100:.2f}%)")
    print(f"✅ Fechadas:   {analysis['ended_count']:,} ({analysis['ended_count']/summary['filtered_count']*100:.2f}%)")
    print(f"🎯 Conversão:  {analysis['conversion_rate']:.2f}%")
    print()
    
    print("─" * 70)
    print("💬 INTENÇÕES (Top 15)")
    print("─" * 70)
    for intent, count in list(analysis['by_intent'].items())[:15]:
        icon = "💰" if intent in ['agendar', 'pacote', 'preco'] else "💬"
        pct = count / summary['filtered_count'] * 100
        print(f"  {icon} {intent}: {count:,} ({pct:.3f}%)")
    print()
    
    print("─" * 70)
    print("😊 SENTIMENTOS")
    print("─" * 70)
    for sentiment, count in analysis['by_sentiment'].items():
        icon = "😊" if sentiment == 'positive' else "😐" if sentiment == 'neutral' else "😟"
        pct = count / summary['filtered_count'] * 100 if summary['filtered_count'] > 0 else 0
        print(f"  {icon} {sentiment}: {count:,} ({pct:.3f}%)")
    print()
    
    print("─" * 70)
    print("📈 CRESCIMENTO POR MÊS (Top 12)")
    print("─" * 70)
    months = list(analysis['by_month'].items())[-12:]
    max_val = max([v for _, v in analysis['by_month'].items()]) if analysis['by_month'] else 1
    for month, count in months:
        bar = "█" * int(count / max_val * 40) if max_val > 0 else ""
        print(f"  {month}: {bar} {count:,}")
    print()
    
    print("─" * 70)
    print("🏆 TOP 10 CLIENTES (Mais Conversas)")
    print("─" * 70)
    for i, (phone, count) in enumerate(list(analysis['top_clients'].items())[:10], 1):
        print(f"  {i}. {phone}: {count} conversas")
    print()
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  ✅ EXTRAÇÃO E ANÁLISE CONCLUÍDAS!                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Complete Conversation Extraction    ║")
    print("║     Filtra grupos, mantém apenas atendimentos     ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Extract all conversations
    all_convs, filtered_convs, groups_excluded, invalid_excluded = fetch_all_conversations(
        max_pages=200,
        page_size=1000
    )
    
    if not filtered_convs:
        print("❌ Nenhuma conversa válida encontrada!")
        return
    
    # Analyze filtered data
    analysis = analyze_filtered_data(filtered_convs)
    
    # Save results
    summary = save_results(all_convs, filtered_convs, analysis, groups_excluded, invalid_excluded)
    
    # Print final report
    print_final_report(summary, analysis)
    
    print("📁 Arquivos salvos em: /Users/franciscotaveira.ads/LUNA OS/logs/")
    print()
    
    return summary

if __name__ == "__main__":
    main()
