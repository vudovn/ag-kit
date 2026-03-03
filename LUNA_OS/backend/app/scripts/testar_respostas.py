#!/usr/bin/env python3
"""
🌙🔧 LUNA OS v3.0 — TESTE RÁPIDO DE RESPOSTAS
Testa as respostas da Luna para perguntas problemáticas
"""

import sys
import asyncio
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.core.brain import process_message


async def testar_respostas():
    """Testa respostas para perguntas problemáticas"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🔧 TESTE RÁPIDO DE RESPOSTAS                     ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Perguntas problemáticas identificadas
    perguntas = [
        ("5549999999999", "Maria", "Quanto custa a escova lisa?"),
        ("5549999999999", "Maria", "Onde ficam vocês?"),
        ("5549999999999", "Maria", "Qual a diferença entre gel e acrílico?"),
        ("5549999999999", "Maria", "Tem desconto para primeira vez?"),
        ("5549999999999", "Maria", "Tem horário essa semana com a Ju?"),
    ]
    
    resultados = []
    
    for phone, name, pergunta in perguntas:
        print(f"🧑 Cliente: {pergunta}")
        print("─" * 50)
        
        try:
            resposta = await process_message(phone, name, pergunta, [])
            
            print(f"🤖 Luna: {resposta.get('response', 'N/A')[:200]}")
            print(f"🎯 Intent: {resposta.get('intent', 'unknown')} ({resposta.get('intent_confidence', 0)*100:.0f}%)")
            print(f"⏱ Tempo: {resposta.get('processing_ms', 0)}ms")
            
            sucesso = resposta.get('ok', False) and resposta.get('intent') != 'fallback_safety'
            
            if sucesso:
                print("✅ RESPOSTA BOA")
            else:
                print("❌ FALLBACK - PRECISA MELHORAR")
            
            resultados.append({
                "pergunta": pergunta,
                "sucesso": sucesso,
                "intent": resposta.get('intent', 'unknown'),
                "tempo_ms": resposta.get('processing_ms', 0)
            })
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            resultados.append({
                "pergunta": pergunta,
                "sucesso": False,
                "intent": "erro",
                "tempo_ms": 0
            })
        
        print()
    
    # Resumo
    print("=" * 50)
    print("RESUMO")
    print("=" * 50)
    
    sucessos = sum(1 for r in resultados if r.get('sucesso', False))
    total = len(resultados)
    taxa_sucesso = (sucessos / total * 100) if total > 0 else 0
    
    print(f"✅ Sucessos: {sucessos}/{total}")
    print(f"📈 Taxa de Sucesso: {taxa_sucesso:.1f}%")
    
    if taxa_sucesso < 80:
        print()
        print("⚠️ ATENÇÃO: Taxa de sucesso abaixo de 80%")
        print("→ Precisa melhorar Knowledge Base")
        print("→ Adicionar mais FAQs")
        print("→ Refinar classificação de intents")
    
    print()
    
    return resultados


if __name__ == "__main__":
    asyncio.run(testar_respostas())
