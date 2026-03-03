#!/usr/bin/env python3
"""
🌙💼 LUNA OS — FULL DATA EXTRACTION
Extrai TODAS as conversas e clientes para diagnóstico completo
Pasta Oficial: /Users/franciscotaveira.ads/LUNA OS
"""

import httpx
import json
from datetime import datetime
from pathlib import Path

API_BASE = "http://localhost:8000"
OUTPUT_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")

def fetch_all(endpoint, max_items=100000, page_size=1000):
    """Extrai TODOS os dados de um endpoint"""
    all_data = []
    
    print(f"   📥 Buscando {endpoint}...")
    
    for page in range(max_items // page_size):
        offset = page * page_size
        try:
            response = httpx.get(
                f"{API_BASE}{endpoint}",
                params={"limit": page_size, "offset": offset},
                timeout=120.0
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    all_data.extend(data)
                    if (page + 1) % 10 == 0:
                        print(f"      Página {page+1}: {len(all_data):,} registros...")
                else:
                    print(f"      ✅ Fim dos dados na página {page+1}")
                    break
            else:
                print(f"      ⚠️ Status {response.status_code} na página {page+1}")
                break
                
        except Exception as e:
            print(f"      ❌ Erro na página {page+1}: {e}")
            break
    
    return all_data

def main():
    """Extrai TODOS os dados"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS — Full Data Extraction                ║")
    print("║     Extrai TODAS as conversas e clientes          ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Extract conversations
    print("📞 EXTRAINDO CONVERSAS...")
    conversations = fetch_all("/api/conversations", max_items=100000, page_size=1000)
    print(f"   ✅ {len(conversations):,} conversas extraídas")
    print()
    
    # Extract clients
    print("👥 EXTRAINDO CLIENTES...")
    clients = fetch_all("/api/clients", max_items=50000, page_size=500)
    print(f"   ✅ {len(clients):,} clientes extraídos")
    print()
    
    # Save conversations
    conv_file = OUTPUT_DIR / f"all_conversations_{timestamp}.json"
    with open(conv_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)
    print(f"💾 Conversas salvas: {conv_file}")
    
    # Save clients
    clients_file = OUTPUT_DIR / f"all_clients_{timestamp}.json"
    with open(clients_file, 'w', encoding='utf-8') as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)
    print(f"💾 Clientes salvos: {clients_file}")
    
    # Save summary
    summary = {
        'extracted_at': datetime.now().isoformat(),
        'total_conversations': len(conversations),
        'total_clients': len(clients),
        'conversations_file': str(conv_file),
        'clients_file': str(clients_file)
    }
    
    summary_file = OUTPUT_DIR / f"extraction_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 Resumo salvo: {summary_file}")
    
    # Print summary
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  📊 EXTRACTION SUMMARY                            ║")
    print("╚════════════════════════════════════════════════════╝")
    print(f"   Conversas: {len(conversations):,}")
    print(f"   Clientes:  {len(clients):,}")
    print(f"   Arquivos:  3 (conversas, clientes, resumo)")
    print()
    print("✅ Extração completa!")
    print()
    
    return summary

if __name__ == "__main__":
    main()
