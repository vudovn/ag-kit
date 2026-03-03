#!/usr/bin/env python3
"""
🌙🧪 LUNA OS — Export Real Conversations to Dojo Arena

Exporta conversas reais do WhatsApp e cria cenários automáticos no Dojo.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.integrations.supabase_client import get_supabase
from loguru import logger
import json

logger.add("logs/export_conversations.log", rotation="10 MB", retention="7 days")

def export_real_conversations(limit: int = 100):
    """
    Exporta conversas reais do Supabase e salva como cenários Dojo.
    """
    logger.info("🌙 Iniciando exportação de conversas reais...")
    
    db = get_supabase()
    
    # Exportar conversas com mensagens
    logger.info(f"📊 Buscando {limit} conversas no Supabase...")
    
    conversations = db.table("conversations").select("""
        id,
        phone,
        client_name,
        status,
        intent,
        started_at,
        messages(content, direction, intent_detected, created_at)
    """).order("started_at", desc=True).limit(limit).execute()
    
    if not conversations.data:
        logger.error("❌ Nenhuma conversa encontrada!")
        return []
    
    logger.info(f"✅ {len(conversations.data)} conversas encontradas")
    
    # Processar conversas
    scenarios = []
    
    for conv in conversations.data:
        # Extrair mensagens inbound (cliente)
        inbound_messages = [
            m for m in conv.get("messages", []) 
            if m.get("direction") == "inbound"
        ]
        
        if not inbound_messages:
            continue
        
        # Extrair primeira mensagem do cliente
        first_message = inbound_messages[0]
        
        # Determinar nível de dificuldade baseado na intent
        intent = conv.get("intent") or first_message.get("intent_detected") or "unknown"
        
        if intent in ["reclamacao", "reembolso", "ameaca_crise"]:
            level = "advanced"
        elif intent in ["objecao", "comparacao", "multi_servico"]:
            level = "intermediate"
        else:
            level = "beginner"
        
        # Criar cenário Dojo
        scenario = {
            "id": f"real_{conv['id']}",
            "name": f"Real: {conv.get('client_name') or conv['phone'][-5:]}",
            "level": level,
            "description": f"Conversa real via WhatsApp - Intent: {intent}",
            "sample_message": first_message["content"],
            "expected_intent": intent,
            "success_criteria": get_success_criteria(intent),
            "points": 20 if level == "beginner" else 30 if level == "intermediate" else 40,
            "source": "whatsapp_real",
            "metadata": {
                "phone": conv["phone"],
                "original_intent": intent,
                "started_at": conv.get("started_at"),
                "total_messages": len(inbound_messages)
            }
        }
        
        scenarios.append(scenario)
        logger.info(f"✅ Cenário criado: {scenario['name']} (intent: {intent})")
    
    # Salvar como JSON
    output_path = os.path.join(os.path.dirname(__file__), "real_conversations_scenarios.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(scenarios),
            "scenarios": scenarios
        }, f, ensure_ascii=False, indent=2)
    
    logger.info(f"💾 {len(scenarios)} cenários salvos em: {output_path}")
    
    # Resumo
    level_counts = {}
    for s in scenarios:
        level_counts[s["level"]] = level_counts.get(s["level"], 0) + 1
    
    logger.info("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  EXPORTAÇÃO CONCLUÍDA                                        ║
    ╠════════════════════════════════════════════════════════════╣
    """ + f"""
    ║  Total Cenários: {len(scenarios)}
    ║  Beginner: {level_counts.get('beginner', 0)}
    ║  Intermediate: {level_counts.get('intermediate', 0)}
    ║  Advanced: {level_counts.get('advanced', 0)}
    """ + """
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    return scenarios


def get_success_criteria(intent: str) -> list:
    """
    Retorna critérios de sucesso baseados na intent.
    """
    criteria_map = {
        "saudacao": ["warm_response", "offer_help"],
        "agendamento": ["collect_service", "collect_time", "collect_professional"],
        "preco": ["accurate_price", "value_proposition"],
        "horario_func": ["accurate_hours", "friendly_tone"],
        "localizacao": ["accurate_address", "offer_directions"],
        "reclamacao": ["empathy", "apology", "solution_offered"],
        "objecao": ["empathy", "value_proposition", "alternative_offered"],
        "multi_servico": ["upsell_package", "calculate_total_time"],
        "reembolso": ["policy_explained", "empathy", "handoff_if_needed"],
    }
    
    return criteria_map.get(intent, ["warm_response", "offer_help"])


if __name__ == "__main__":
    try:
        scenarios = export_real_conversations(limit=100)
        
        if scenarios:
            print(f"\n✅ {len(scenarios)} cenários exportados com sucesso!")
            print(f"📁 Arquivo: real_conversations_scenarios.json")
        else:
            print("\n⚠️ Nenhum cenário exportado. Verifique se há conversas no Supabase.")
            
    except Exception as e:
        logger.error(f"❌ Erro na exportação: {e}")
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
