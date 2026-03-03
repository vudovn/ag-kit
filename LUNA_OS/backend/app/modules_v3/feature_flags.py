"""
🌙 LUNA OS v3.0 — Feature Flags
Interruptores para Módulos de Inteligência

SEGURANÇA: Todos começam DESLIGADOS (False)
"""

FEATURE_FLAGS = {
    # Módulo 1: Agenda Viva
    'agenda_viva': {
        'enabled': False,        # Começa DESLIGADO
        'traffic_percentage': 0, # 0% do tráfego
        'rollback_time': 60,     # 60 segundos para rollback
    },
    
    # Módulo 2: Orquestrador
    'orchestrator': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 120,
    },
    
    # Módulo 3: Simulador
    'simulator': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 30,
    },
    
    # Módulo 4: Churn Detector
    'churn_detector': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 30,
    },
    
    # Módulo 5: Revenue Optimizer
    'revenue_optimizer': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 60,
    },
    
    # Módulo 6: AI Coach
    'ai_coach': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 60,
    },
    
    # Módulo 7: Mystery Shopper
    'mystery_shopper': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 30,
    },
    
    # Módulo 8: Heat Map
    'heat_map': {
        'enabled': False,
        'traffic_percentage': 0,
        'rollback_time': 30,
    },

    # Módulo 9: Conversation Intelligence (NOVO)
    'conversation_intelligence': {
        'enabled': True,  # ✅ ATIVADO
        'traffic_percentage': 100,
        'rollback_time': 60,
    },
}


def is_module_enabled(module_name: str) -> bool:
    """Verifica se módulo está habilitado"""
    if module_name not in FEATURE_FLAGS:
        return False
    return FEATURE_FLAGS[module_name]['enabled']


def get_traffic_percentage(module_name: str) -> int:
    """Retorna porcentagem de tráfego para o módulo"""
    if module_name not in FEATURE_FLAGS:
        return 0
    return FEATURE_FLAGS[module_name]['traffic_percentage']


def enable_module(module_name: str, traffic_pct: int = 1):
    """
    Habilita módulo com porcentagem de tráfego
    
    SEGURANÇA: Começa com 1% para teste
    """
    if module_name in FEATURE_FLAGS:
        FEATURE_FLAGS[module_name]['enabled'] = True
        FEATURE_FLAGS[module_name]['traffic_percentage'] = min(traffic_pct, 100)
        print(f"✅ Módulo {module_name} habilitado para {traffic_pct}% do tráfego")


def disable_module(module_name: str):
    """
    Desabilita módulo (ROLLBACK)
    
    SEGURANÇA: Rollback instantâneo
    """
    if module_name in FEATURE_FLAGS:
        FEATURE_FLAGS[module_name]['enabled'] = False
        FEATURE_FLAGS[module_name]['traffic_percentage'] = 0
        print(f"🛑 Módulo {module_name} DESABILITADO (rollback)")


def get_all_flags_status() -> dict:
    """Retorna status de todos os módulos"""
    return {
        name: {
            'enabled': flag['enabled'],
            'traffic': flag['traffic_percentage'],
            'rollback': flag['rollback_time']
        }
        for name, flag in FEATURE_FLAGS.items()
    }
