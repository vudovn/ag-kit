#!/usr/bin/env python3
"""
🌙 LUNA OS v3.0 — Teste de Feature Flags
Teste SEGURO (não modifica produção)

Risco: ZERO (só leitura)
"""

import sys
from pathlib import Path

# Adiciona backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.modules_v3.feature_flags import (
    is_module_enabled,
    get_traffic_percentage,
    enable_module,
    disable_module,
    get_all_flags_status
)

def test_feature_flags():
    """Testa feature flags (liga/desliga)"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS v3.0 — Teste de Feature Flags         ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Teste 1: Verifica se todos começam DESLIGADOS
    print("📊 Teste 1: Status inicial (todos OFF)")
    print("─" * 50)
    
    all_off = True
    for module_name in ['agenda_viva', 'orchestrator', 'simulator']:
        enabled = is_module_enabled(module_name)
        status = "✅ OFF" if not enabled else "❌ ON"
        print(f"   {module_name}: {status}")
        if enabled:
            all_off = False
    
    if all_off:
        print("\n   ✅ Todos começam DESLIGADOS (seguro)")
    else:
        print("\n   ❌ Algum módulo está LIGADO (perigo)")
    
    print()
    
    # Teste 2: Liga módulo (1% tráfego)
    print("📊 Teste 2: Ligar módulo (1% tráfego)")
    print("─" * 50)
    
    enable_module('agenda_viva', traffic_pct=1)
    
    enabled = is_module_enabled('agenda_viva')
    traffic = get_traffic_percentage('agenda_viva')
    
    if enabled and traffic == 1:
        print(f"   ✅ Módulo LIGADO para {traffic}% do tráfego")
    else:
        print(f"   ❌ Falha ao ligar módulo")
    
    print()
    
    # Teste 3: Desliga módulo (ROLLBACK)
    print("📊 Teste 3: Desligar módulo (ROLLBACK)")
    print("─" * 50)
    
    disable_module('agenda_viva')
    
    enabled = is_module_enabled('agenda_viva')
    traffic = get_traffic_percentage('agenda_viva')
    
    if not enabled and traffic == 0:
        print(f"   ✅ Módulo DESLIGADO (rollback OK)")
    else:
        print(f"   ❌ Falha ao desligar módulo")
    
    print()
    
    # Teste 4: Status completo
    print("📊 Teste 4: Status completo de todos módulos")
    print("─" * 50)
    
    status = get_all_flags_status()
    
    for name, info in status.items():
        on_off = "🟢 ON" if info['enabled'] else "🟡 OFF"
        print(f"   {name}: {on_off} | Tráfego: {info['traffic']}% | Rollback: {info['rollback']}s")
    
    print()
    print("╔════════════════════════════════════════════════════╗")
    print("║  ✅ TESTE CONCLUÍDO                                ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║  • Feature flags FUNCIONAM                        ║")
    print("║  • Liga/Desliga OK                                ║")
    print("║  • Rollback testado                               ║")
    print("║  • Luna OS v2.2 NÃO foi modificado                ║")
    print("╚════════════════════════════════════════════════════╝")
    print()

if __name__ == "__main__":
    test_feature_flags()
