# 🎯 UNALUX - Sistema Completo de Validação Observável

**Estrutura de Validação Integrada:**

```
┌────────────────────────────────────────────────────────────────────────┐
│                    WINDMILL + VALIDAÇÃO FRAMEWORK                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  FASE DE VALIDAÇÃO (4 Semanas)                                        │
│  ├─ Semana 1: Redis Cache (50 eventos)                   Risco 🟢    │
│  ├─ Semana 2: CSP Solver (100 eventos)                  Risco 🟡    │
│  ├─ Semana 3: FSM Conflito (30 eventos)                 Risco 🟡    │
│  └─ Semana 4: Windmill Load (1000 eventos)              Risco 🔴    │
│                                                                        │
│  COMO FUNCIONA:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ 1. Defina Hipótese                                              │ │
│  │    "Perfil em Redis atualiza em <500ms"                        │ │
│  │                                                                 │ │
│  │ 2. Crie Checkpoint                                             │ │
│  │    POST /api/validation/checkpoints/create                    │ │
│  │    → Retorna checkpoint_id = abc-123                          │ │
│  │                                                                 │ │
│  │ 3. Configure Schedule no Windmill                             │ │
│  │    Script: week1_redis_cache.py                               │ │
│  │    Cron: 0 */6 * * * (a cada 6h)                             │ │
│  │    Args: VALIDATION_CHECKPOINT_WEEK1=abc-123                 │ │
│  │                                                                 │ │
│  │ 4. Script Windmill Coleta Dados                              │ │
│  │    Para cada iteração:                                        │ │
│  │    - Executa operação                                         │ │
│  │    - Mede latência                                            │ │
│  │    - Registra evento                                          │ │
│  │    → POST /api/validation/events/record                      │ │
│  │                                                                 │ │
│  │ 5. Sistema Detecta Anomalias                                 │ │
│  │    Se métrica > 3σ da média:                                 │ │
│  │    → INSERT validation_anomalies                             │ │
│  │                                                                 │ │
│  │ 6. Você Consulta Diagnóstico                                 │ │
│  │    POST /api/validation/diagnose/abc-123                    │ │
│  │    ← Retorna: progresso, métricas, anomalias, status        │ │
│  │                                                                 │ │
│  │ 7. Dashboard Mostra Tudo em Tempo Real                       │ │
│  │    http://localhost:3000/validation                          │ │
│  │    ├─ Progress bar (25/50 eventos)                           │ │
│  │    ├─ Métricas (média, min, max, desvio)                   │ │
│  │    ├─ Anomalias (se houver)                                 │ │
│  │    └─ Status (✓ Atende | ✗ Bloqueador)                     │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  DIAGRAMA DE FLUXO:                                                    │
│                                                                        │
│   User/Admin                Backend (FastAPI)      Windmill          │
│   │                         │                        │               │
│   ├─ POST /checkpoints/create              Checkpoint criado        │
│   │                    ├─ ID gerado: abc-123                        │
│   │                    │                                             │
│   ├─ SET env var ────────────────────────→ VALIDATION_CHECKPOINT_WEEK1=abc-123
│   │                                        │                         │
│   │                                        │ ╔═════════════════════╗ │
│   │                                        │ ║ SCHEDULE RODANDO    ║ │
│   │                                        │ ║ Cron: 0 */6 * * *   ║ │
│   │                                        │ ╚═════════════════════╝ │
│   │                    Executa a cada 6h:  │                         │
│   │                    ├─ 1. Atualiza Redis│ week1_redis_cache.py   │
│   │                    ├─ 2. Atualiza DB   │─────────────────────────│
│   │                    ├─ 3. Mede latência │                         │
│   │                    ├─ 4. Registra      │                         │
│   │                    │    evento         │                         │
│   │                    │                   │                         │
│   │                    ├─ POST /events/record (latency_ms: 245.5)   │
│   │                    │  • Insert em validation_events             │
│   │                    │  • Calcula média/stddev                   │
│   │                    │  • Detecta outliers (3σ)                  │
│   │                    │  • Insert em validation_anomalies         │
│   │                    │                                             │
│   │ POST /diagnose/abc-123                 Retorna JSON             │
│   ├──────────────────────────────────────────────────────────────→  │
│   │                         • events_collected: 12                  │
│   │                         • avg_metric_value: 342.5              │
│   │                         • completion_percentage: 24             │
│   │ Mostra no Dashboard         • anomalies_detected: 1              │
│   │ ✓ Progress: 12/50           • meets_criteria: true             │
│   │ ✓ Média: 342.5ms            • blockers: []                     │
│   │ ✓ Sem anomalias                                                │
│   │                                                                 │
│   └─────────────────────────────────────────────────────────────── │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Checklist de Implementação

### **Setup Inicial (30 min)**
- [ ] Migração `015_validation_framework` aplicada
- [ ] Tabelas criadas no Supabase
- [ ] API `/api/validation/` registrada em `main.py`
- [ ] Endpoints testados com Postman/curl

### **Windmill Setup (1h)**
- [ ] 4 scripts copiados para Windmill UI
- [ ] Cada script testado manualmente (rodar 1x)
- [ ] Schedules criados no Windmill
- [ ] Variáveis de ambiente configuradas

### **Frontend Dashboard (1h)**
- [ ] Componentes React criados em `frontend/app/validation/`
- [ ] Dashboard responsivo
- [ ] Gráficos em tempo real
- [ ] Alertas de anomalia

### **Iniciação de Validação (5 min)**
- [ ] Rodar `bash scripts/init_validation_framework.sh`
- [ ] 4 fases criadas
- [ ] 4 checkpoints criados
- [ ] Schedules ativados

### **Semana 1-4: Acompanhamento**
- [ ] Verificar dashboard diariamente
- [ ] Se anomalias: investigar causa
- [ ] Se completar: avançar para próxima semana
- [ ] Se falhar: debugar, corrigir, rodar novamente

---

## 🔄 Integração com Windmill + FastAPI

### **Flow Completo**

**1. Admin cria checkpoint:**
```bash
curl -X POST http://localhost:8000/api/validation/checkpoints/create \
  -H "Authorization: Bearer key" \
  -d '{"name": "Redis Cache", ...}'

# Retorno:
# {"checkpoint_id": "abc-123"}
```

**2. Admin configura schedule no Windmill:**
```bash
curl -X POST http://localhost:8001/api/w/luna/schedules/create \
  -H "Authorization: Bearer token" \
  -d '{
    "path": "u/validation/redis_cache_schedule",
    "schedule": "0 */6 * * *",
    "script_path": "u/validation/week1_redis_cache",
    "args": {"VALIDATION_CHECKPOINT_WEEK1": "abc-123"},
    "enabled": true
  }'
```

**3. Windmill executa script a cada 6h:**
```python
# windmill/validation/week1_redis_cache.py
def main():
    # Coleta dados
    # Para cada amostra:
    # - Executa operação
    # - Registra evento via POST /api/validation/events/record
    # - Retorna summary
```

**4. FastAPI recebe eventos:**
```python
# backend/app/api/validation_tracking.py
@router.post("/events/record")
async def record_event(event: ValidationEventCreate, ...):
    # Insere em validation_events
    # Verifica anomalias (background task)
    # Atualiza diagnostic (background task)
    # Retorna event_id
```

**5. Background tasks:**
```python
# Task 1: update_diagnostic_async()
# - A cada 10 eventos, recalcula métricas
# - Se chegou ao target, marca como "completed"

# Task 2: check_anomalies_async()
# - Detecta outliers (3σ)
# - Insere em validation_anomalies
# - Marca severidade
```

**6. Admin consulta diagnóstico:**
```bash
curl -X POST http://localhost:8000/api/validation/diagnose/abc-123 \
  -H "Authorization: Bearer key"

# Retorno:
# {
#   "checkpoint": {...},
#   "diagnostic": {
#     "events_collected": 25,
#     "events_target": 50,
#     "completion_percentage": 50,
#     "avg_metric_value": 342.5,
#     "meets_acceptance_criteria": true,
#     ...
#   },
#   "is_healthy": true
# }
```

**7. Dashboard atualiza em tempo real:**
```jsx
// frontend/app/validation/page.tsx
// GET /api/validation/diagnostics a cada 10s
// Renderiza:
// - Progress bar (25/50)
// - Métricas (342.5ms)
// - Anomalias (0)
// - Status (✓)
```

---

## 🎓 Exemplo Passo a Passo - Semana 1

### **Dia 1 - Segunda (Setup)**

```bash
# 1. Admin rodar init script
export ADMIN_KEY="sk_test_123"
export WINDMILL_TOKEN="token_456"
bash scripts/init_validation_framework.sh

# Saída:
# ✓ 4 Fases criadas
# ✓ 4 Checkpoints criados
# Week 1 Checkpoint ID: abc-123
# Week 2 Checkpoint ID: def-456
# ...

# 2. Copiar scripts para Windmill
# (Manualmente via UI ou via sync)

# 3. Verificar schedules criados
curl -X GET http://localhost:8001/api/w/luna/schedules/list \
  -H "Authorization: Bearer $WINDMILL_TOKEN" | jq
```

### **Dia 2-5 (Coleta)**

```
Windmill executa automaticamente:
  02/Mar 06:00 → week1_redis_cache.py roda
    ├─ 10 eventos registrados
    └─ Diagnóstico: 10/50 (20%)

  02/Mar 12:00 → week1_redis_cache.py roda
    ├─ 10 eventos registrados
    └─ Diagnóstico: 20/50 (40%)

  03/Mar 06:00 → week1_redis_cache.py roda
    ├─ 9 eventos registrados (1 outlier detectado)
    └─ Diagnóstico: 29/50 (58%)
         └─ ⚠️ Anomalia: latência 1200ms (3σ acima)

  ... continua coletando ...
```

### **Dia 6-7 (Análise)**

```bash
# Admin verifica progresso
curl -X POST http://localhost:8000/api/validation/diagnose/abc-123 \
  -H "Authorization: Bearer $ADMIN_KEY" | jq

# Resposta:
{
  "diagnostic": {
    "events_collected": 52,
    "events_target": 50,
    "completion_percentage": 104,  ← COMPLETADO!
    "avg_metric_value": 342.5,
    "min_metric_value": 120.3,
    "max_metric_value": 498.2,
    "stddev_metric_value": 85.4,
    "valid_events": 50,
    "anomalies_detected": 2,
    "critical_anomalies": 0,
    "meets_acceptance_criteria": true,
    "blockers": []
  },
  "is_healthy": true  ← ✓ PASSOU!
}

# ✓ Resultado: SEMANA 1 VALIDADA
# Próximo: Ativar Semana 2
```

---

## 📊 Interpretação de Resultados

### **Cenário 1: Sucesso ✓**
```json
{
  "completion_percentage": 102,
  "avg_metric_value": 342.5,
  "meets_acceptance_criteria": true,
  "blockers": []
}
```
→ **Decisão:** PASSAR para próxima semana

### **Cenário 2: Variabilidade Alta ⚠️**
```json
{
  "completion_percentage": 105,
  "stddev_metric_value": 450.0,  ← Muito alto!
  "anomalies_detected": 5,
  "meets_acceptance_criteria": false,
  "blockers": [
    "⚠️ Variabilidade alta nas métricas (stddev 450 > média 500 * 50%)"
  ]
}
```
→ **Decisão:** INVESTIGAR (Redis lag? DB lento?)

### **Cenário 3: Latência Acima do Limite ✗**
```json
{
  "completion_percentage": 105,
  "avg_metric_value": 620.5,  ← Acima de 500!
  "meets_acceptance_criteria": false,
  "blockers": [
    "⚠️ Latência acima do limite (620.5ms > 500ms)"
  ]
}
```
→ **Decisão:** BLOQUEADOR - Otimizar antes de continuar

---

## 🔐 Segurança & Observabilidade

### **Dados Sensíveis**
- Eventos não registram senhas/tokens
- Customer IDs desidentificados se necessário
- Anomalias logged, não expostas publicamente

### **Rastreabilidade**
- Cada evento tem `related_customer_id`, `related_conversation_id`, etc
- Anomalias linkam de volta ao evento
- Diagnósticos auditáveis (história completa em `validation_diagnostics`)

### **Alerts**
```python
# Configurar alerts (opcional):
if anomaly.severity == "critical":
    notify_slack(f"Critical anomaly: {anomaly.description}")
    escalate_to_engineering()
```

---

## 📈 Após as 4 Semanas

Se tudo passar:
1. **Semana 5:** Deploy para produção com feature flags
2. **Semana 6-8:** Monitoramento contínuo
3. **Semana 9+:** Otimizações baseadas em dados reais

Se algo falhar:
- Pause validação
- Investigate & fix
- Rerun fase com melhorias
- Document lessons learned

---

## 📞 Suporte & Troubleshooting

**Problema:** Script Windmill não executa
```bash
# Verificar logs
curl -X GET http://localhost:8001/api/w/luna/jobs/list \
  -H "Authorization: Bearer $WINDMILL_TOKEN" | jq '.[-1]'

# Ver detalhes de erro
curl -X GET http://localhost:8001/api/w/luna/jobs/{job_id}/logs \
  -H "Authorization: Bearer $WINDMILL_TOKEN"
```

**Problema:** Diagnóstico vazio
```bash
# Verificar se eventos estão sendo registrados
curl -X GET http://localhost:8000/api/validation/events/abc-123 \
  -H "Authorization: Bearer $ADMIN_KEY" | jq 'length'

# Se 0, o script não está chamando POST /events/record
```

**Problema:** Anomalia detectada
- Olhe a `description` da anomalia
- Compare `detected_value` com `expected_range`
- Rodar script novamente para confirmar se é padrão

---

## 🎯 Sumário Executivo

| Aspecto | Detalhe |
|---------|---------|
| **O Quê** | Sistema que valida 4 hipóteses de performance/estabilidade |
| **Quanto Tempo** | 4 semanas (1 semana por componente) |
| **Como** | Scripts Windmill coletam dados → API registra → Dashboard mostra |
| **Quem Gerencia** | Admin via API e Dashboard |
| **Resultado** | GO/NO-GO decision para produção no final da semana 4 |
| **Risco Mitigation** | Detecta anomalias automaticamente, valida antes de escalar |

---

**Próximos Passos:**
1. Ler `VALIDATION_QUICK_START.md` (5 min)
2. Rodar `init_validation_framework.sh` (5 min)
3. Acompanhar dashboard (contínuo)
4. Consultar `VALIDATION_FRAMEWORK.md` se tiver dúvidas

**Documentação:**
- `VALIDATION_FRAMEWORK.md` - Referência Completa
- `VALIDATION_QUICK_START.md` - Passo a Passo Rápido
- API Docs: `/api/docs` quando backend rodando

**Arquivos Criados:**
```
backend/app/api/validation_tracking.py       (API endpoints)
windmill/validation/week1_redis_cache.py     (Script semana 1)
windmill/validation/week2_csp_solver.py      (Script semana 2)
windmill/validation/week3_fsm_conflict.py    (Script semana 3)
windmill/validation/week4_windmill_load.py   (Script semana 4)
scripts/init_validation_framework.sh         (Init automation)
frontend/app/validation/page.tsx             (Dashboard React)
migrations/015_validation_framework.sql      (DB schema)
```

**Status:** ✅ Framework 100% implementado e pronto para uso
