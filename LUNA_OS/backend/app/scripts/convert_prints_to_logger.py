#!/usr/bin/env python3
"""
Script utilitário para converter print() em logger.info() em todos os scripts.
DEBT #B6: Scripts - remover prints, usar logger
"""

import os
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

# Scripts para converter
scripts = [
    "analyze_conversations.py",
    "deep_insights_analysis.py",
    "extracao_direta_conversas.py",
    "extrair_conversas_completas.py",
    "full_extraction.py",
    "robust_extraction_agent.py",
    "robust_extraction_agent_standalone.py",
    "whatsapp_sales_intelligence.py",
    "analise_profunda_threads.py",
]

for script_name in scripts:
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"❌ {script_name} não encontrado")
        continue
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar import logger se não existir
    if 'from loguru import logger' not in content:
        # Encontrar última importação
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
        
        lines.insert(insert_idx, 'from loguru import logger')
        content = '\n'.join(lines)
        print(f"✅ {script_name}: import logger adicionado")
    
    # Substituir print() por logger.info()
    # Padrão: print("texto") → logger.info("texto")
    content = re.sub(r'\bprint\(', 'logger.info(', content)
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {script_name}: print() → logger.info() convertido")

print("\n✅ Conversão concluída!")
print("📝 Revise os arquivos para garantir que a conversão foi correta")
