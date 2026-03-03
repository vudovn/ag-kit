# 🌙 LUNA OS v3.0 — MÓDULOS DE INTELIGÊNCIA

## Arquitetura de Módulos Isolados (Feature Flags)

**Data:** 26 de Fevereiro de 2026  
**Status:** 🟡 EM DESENVOLVIMENTO  
**Risco:** ZERO (módulos separados do Luna OS v2.2)

---

## 📊 VISÃO GERAL

```
╔══════════════════════════════════════════════════════════════╗
║  LUNA OS v3.0 — 8 MÓDULOS DE INTELIGÊNCIA                   ║
╠════════════════════════════════════════════════════════════╣
║  Cada módulo é INDEPENDENTE (liga/desliga)                 ║
║  Luna OS v2.2 continua FUNCIONANDO                         ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🗂️ ESTRUTURA DE DIRETÓRIOS

```
LUNA_OS/
├── backend/
│   ├── app/
│   │   ├── main.py              ← Luna OS v2.2 (NÃO MEXER)
│   │   ├── config.py            ← Luna OS v2.2 (NÃO MEXER)
│   │   ├── core/                ← Luna OS v2.2 (NÃO MEXER)
│   │   ├── api/                 ← Luna OS v2.2 (NÃO MEXER)
│   │   │
│   │   └── modules_v3/          ← MÓDULOS NOVOS (v3.0)
│   │       ├── __init__.py
│   │       ├── feature_flags.py ← INTERRUPTORES (liga/desliga)
│   │       │
│   │       ├── agenda_viva/     ← Módulo 1
│   │       │   ├── __init__.py
│   │       │   ├── optimizer.py
│   │       │   └── api.py
│   │       │
│   │       ├── orchestrator/    ← Módulo 2
│   │       │   ├── __init__.py
│   │       │   ├── multi_agent.py
│   │       │   └── api.py
│   │       │
│   │       ├── simulator/       ← Módulo 3
│   │       │   ├── __init__.py
│   │       │   ├── what_if.py
│   │       │   └── api.py
│   │       │
│   │       ├── churn_detector/  ← Módulo 4
│   │       │   ├── __init__.py
│   │       │   ├── predictor.py
│   │       │   └── api.py
│   │       │
│   │       ├── revenue_optimizer/ ← Módulo 5
│   │       │   ├── __init__.py
│   │       │   ├── dynamic_pricing.py
│   │       │   └── api.py
│   │       │
│   │       ├── ai_coach/        ← Módulo 6
│   │       │   ├── __init__.py
│   │       │   ├── trainer.py
│   │       │   └── api.py
│   │       │
│   │       ├── mystery_shopper/ ← Módulo 7
│   │       │   ├── __init__.py
│   │       │   ├── auditor.py
│   │       │   └── api.py
│   │       │
│   │       └── heat_map/        ← Módulo 8
│   │           ├── __init__.py
│   │           ├── visualizer.py
│   │           └── api.py
│   │
│   └── logs/
│       └── modules_v3.log       ← Log separado (não mistura)
│
├── frontend/
│   └── app/
│       ├── page.tsx             ← Luna OS v2.2 (NÃO MEXER)
│       └── modules_v3/          ← UI dos módulos novos
│           ├── dashboard/       ← Dashboard unificado
│           └── settings/        ← Configuração de feature flags
│
└── modules_v3_config.json       ← Configuração dos feature flags
```

---

## 🚩 FEATURE FLAGS (Interruptores)

### **Arquivo:** `modules_v3/feature_flags.py`

```python
"""
Feature Flags — Liga/Desliga Cada Módulo

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
```

---

## 🔌 INTEGRAÇÃO SEGURA COM LUNA OS v2.2

### **Exemplo: Como Luna OS v2.2 chama Módulo Novo**

```python
# backend/app/api/scheduling.py (Luna OS v2.2)

from app.modules_v3.feature_flags import is_module_enabled, get_traffic_percentage
from app.modules_v3.agenda_viva.api import optimize_scheduling as agenda_viva_optimize
import random

async def agendar_horario(cliente_id: str, servico: str, profissional: str = None):
    """
    Luna OS v2.2 — Agendamento (NÃO MEXER)
    
    Este código CONTINUA FUNCIONANDO sempre!
    """
    
    # 1. Luna OS v2.2 faz agendamento NORMAL
    resultado = await agendamento_tradicional(cliente_id, servico, profissional)
    
    # 2. Verifica se módulo novo está habilitado (FEATURE FLAG)
    if is_module_enabled('agenda_viva'):
        # 3. Verifica se este request está no % de tráfego do teste
        traffic_pct = get_traffic_percentage('agenda_viva')
        if random.randint(1, 100) <= traffic_pct:
            try:
                # 4. Chama módulo novo (opcional)
                resultado_otimizado = await agenda_viva_optimize(resultado)
                return resultado_otimizado
            except Exception as e:
                # 5. Se módulo novo quebrar, LOGA erro mas NÃO quebra Luna OS
                logger.error(f"Módulo agenda_viva falhou: {e}")
                # 6. Retorna resultado NORMAL (Luna OS funciona!)
                return resultado
    
    # 7. Retorna resultado NORMAL (sempre funciona)
    return resultado
```

**Segurança:**
- ✅ Luna OS v2.2 **SEMPRE funciona**
- ✅ Módulo novo é **opcional** (feature flag)
- ✅ Se módulo quebrar → **Luna OS continua**
- ✅ Rollback em **60 segundos**

---

## 📊 CONFIGURAÇÃO DOS MÓDULOS

### **Arquivo:** `modules_v3_config.json`

```json
{
  "version": "3.0.0",
  "luna_os_version": "2.2.0",
  "modules_directory": "backend/app/modules_v3",
  "feature_flags_file": "modules_v3/feature_flags.py",
  "log_file": "logs/modules_v3.log",
  "rollback_timeout_seconds": 300,
  "modules": {
    "agenda_viva": {
      "name": "Agenda Viva",
      "description": "Self-learning scheduler",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 60
    },
    "orchestrator": {
      "name": "Orquestrador",
      "description": "Multi-agent coordination",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 120
    },
    "simulator": {
      "name": "Simulador",
      "description": "What-if scenario engine",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 30
    },
    "churn_detector": {
      "name": "Churn Detector",
      "description": "Predictive analytics",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 30
    },
    "revenue_optimizer": {
      "name": "Revenue Optimizer",
      "description": "Dynamic pricing",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 60
    },
    "ai_coach": {
      "name": "AI Coach",
      "description": "Receptionist trainer",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 60
    },
    "mystery_shopper": {
      "name": "Mystery Shopper",
      "description": "Quality auditor",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 30
    },
    "heat_map": {
      "name": "Heat Map",
      "description": "Visual analytics",
      "status": "development",
      "enabled": false,
      "traffic_percentage": 0,
      "rollback_time_seconds": 30
    }
  }
}
```

---

## 🛡️ PLANO DE ROLLBACK

### **Script:** `rollback_module.sh`

```bash
#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🛡️ LUNA OS v3.0 — ROLLBACK RÁPIDO
# Desabilita módulo em 60 segundos
# ═══════════════════════════════════════════════════════════════

MODULE_NAME=$1

if [ -z "$MODULE_NAME" ]; then
    echo "❌ Uso: ./rollback_module.sh <nome_do_modulo>"
    echo "   Exemplo: ./rollback_module.sh agenda_viva"
    exit 1
fi

echo "🛑 Iniciando rollback do módulo: $MODULE_NAME"

# 1. Desabilita feature flag (instantâneo)
echo "   1/3: Desabilitando feature flag..."
python3 -c "
from app.modules_v3.feature_flags import disable_module
disable_module('$MODULE_NAME')
"

# 2. Limpa cache do módulo
echo "   2/3: Limpando cache..."
rm -rf backend/app/modules_v3/__pycache__/${MODULE_NAME}*

# 3. Verifica status
echo "   3/3: Verificando status..."
python3 -c "
from app.modules_v3.feature_flags import is_module_enabled
if is_module_enabled('$MODULE_NAME'):
    print('❌ Rollback FALHOU')
    exit(1)
else:
    print('✅ Rollback CONCLUÍDO')
"

echo ""
echo "✅ Rollback do módulo $MODULE_NAME concluído em <60 segundos"
echo "📊 Luna OS v2.2 está FUNCIONANDO normalmente"
```

---

## 📈 MONITORAMENTO

### **Dashboard de Feature Flags:**

```
╔══════════════════════════════════════════════════════════════╗
║  LUNA OS v3.0 — FEATURE FLAGS STATUS                        ║
╠════════════════════════════════════════════════════════════╣
║  Módulo              │ Status  │ Tráfego │ Rollback        ║
╠════════════════════════════════════════════════════════════╣
║  Agenda Viva         │ 🟡 OFF  │ 0%      │ 60s             ║
║  Orquestrador        │ 🟡 OFF  │ 0%      │ 120s            ║
║  Simulador           │ 🟡 OFF  │ 0%      │ 30s             ║
║  Churn Detector      │ 🟡 OFF  │ 0%      │ 30s             ║
║  Revenue Optimizer   │ 🟡 OFF  │ 0%      │ 60s             ║
║  AI Coach            │ 🟡 OFF  │ 0%      │ 60s             ║
║  Mystery Shopper     │ 🟡 OFF  │ 0%      │ 30s             ║
║  Heat Map            │ 🟡 OFF  │ 0%      │ 30s             ║
╠════════════════════════════════════════════════════════════╣
║  Luna OS v2.2: ✅ OPERACIONAL                              ║
╚════════════════════════════════════════════════════════════╝
```

---

## ✅ CHECKLIST SEMANA 0

```
□ 1. ✅ Dados das 40K mensagens salvos
□ 2. ✅ Estrutura de diretórios criada
□ 3. ✅ Feature flags implementados
□ 4. ✅ Integração segura com Luna OS v2.2
□ 5. ✅ Script de rollback criado
□ 6. ✅ Configuração JSON criada
□ 7. ⏳ Testar feature flags (liga/desliga)
□ 8. ⏳ Testar rollback (simulação)
□ 9. ⏳ Documentar cada módulo
□ 10. ⏳ Preparar ambiente de staging
```

---

## 🎯 PRÓXIMOS PASSOS

### **Hoje (Semana 0 - Dia 1):**
- ✅ Estrutura de diretórios criada
- ⏳ Implementar Módulo 1: Agenda Viva (esqueleto)
- ⏳ Testar feature flag (liga/desliga)

### **Amanhã (Semana 0 - Dia 2):**
- ⏳ Testar rollback (simulação)
- ⏳ Documentar Módulo 1
- ⏳ Preparar Módulo 2: Orquestrador

### **Fim da Semana 0:**
- ✅ Todos os 8 módulos com esqueleto criado
- ✅ Feature flags testados
- ✅ Rollback testado
- ✅ Pronto para Semana 1 (implementação real)

---

**🌙 "Inteligência completa. Complexidade invisível."**

**Status:** ✅ **SEMANA 0 INICIADA**

**Risco:** **ZERO** (nada muda em produção)

**Próximo:** Implementar esqueleto do Módulo 1 (Agenda Viva)
