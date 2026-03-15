# 🔬 Sistema de Validação Observável - UNALUX

**Objetivo:** Rastrear, medir e validar cada hipótese da arquitetura durante 4 semanas, com observabilidade integrada na ferramenta.

---

## 📊 Arquitetura do Framework

```
┌─────────────────────────────────────────────────────────────┐
│           VALIDATION TRACKING SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  API Endpoints (/api/validation/)                          │
│  ├── POST /checkpoints/create      → Define hipótese       │
│  ├── POST /events/record           → Registra evento       │
│  ├── POST /diagnose/{id}           → Consolida diagnóstico │
│  └── GET  /phases                  → Roadmap 4 semanas     │
│                                                             │
│  Windmill Scripts (windmill/validation/)                   │
│  ├── week1_redis_cache.py          → Coleta 50 eventos    │
│  ├── week2_csp_solver.py           → Coleta 100 eventos   │
│  ├── week3_fsm_conflict.py         → Coleta 30 eventos    │
│  └── week4_windmill_load.py        → Coleta 1000 eventos  │
│                                                             │
│  Database Schema (validation_*)                            │
│  ├── validation_checkpoints        → Metas (o quê)        │
│  ├── validation_events             → Dados (como)         │
│  ├── validation_anomalies          → Desvios              │
│  ├── validation_diagnostics        → Resumo              │
│  └── validation_phases             → Fases (quando)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 As 4 Fases de Validação

### **Semana 1: Redis Cache + Supabase**
- **Hipótese:** Perfil em Redis sincronizado com Supabase atualiza em <500ms
- **Componente:** `cache`
- **Alvo:** 50 eventos
- **Métrica:** `latency_ms`
- **Critério:** média <500ms, taxa de sucesso ≥98%
- **Script:** `week1_redis_cache.py`
- **Risco:** 🟢 Baixo

### **Semana 2: CSP Solver**
- **Hipótese:** OR-Tools resolve agendamento complexo em <2s
- **Componente:** `csp_solver`
- **Alvo:** 100 eventos
- **Métrica:** `solver_time_ms`
- **Critério:** média <2000ms, taxa de sucesso ≥90%
- **Script:** `week2_csp_solver.py`
- **Risco:** 🟡 Médio

### **Semana 3: FSM Conflito**
- **Hipótese:** FSM resolve 80% dos conflitos sem escalação
- **Componente:** `fsm_conflict`
- **Alvo:** 30 eventos
- **Métrica:** `resolution_rate`, `escalation_rate`
- **Critério:** resolução ≥80%, escalação ≤10%
- **Script:** `week3_fsm_conflict.py`
- **Risco:** 🟡 Médio

### **Semana 4: Load Test Windmill**
- **Hipótese:** Windmill aguenta 1000 jobs/dia com <1% erro
- **Componente:** `windmill_load`
- **Alvo:** 1000 eventos
- **Métrica:** `job_latency_ms`, `error_rate`
- **Critério:** p99 <5000ms, erro <1%
- **Script:** `week4_windmill_load.py`
- **Risco:** 🔴 Alto

---

## 🚀 Como Usar

### **Passo 1: Inicializar o Framework**

```bash
# No FastAPI, chamar:
curl -X POST http://localhost:8000/api/validation/phases/init \
  -H "Authorization: Bearer YOUR_ADMIN_KEY"

# Resposta:
{
  "success": true,
  "phases_created": 4,
  "phases": [
    {
      "week": 1,
      "name": "Redis Cache + Supabase Sync",
      "status": "pending",
      ...
    },
    ...
  ]
}
```

### **Passo 2: Criar Checkpoints Individuais**

```bash
curl -X POST http://localhost:8000/api/validation/checkpoints/create \
  -H "Authorization: Bearer YOUR_ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Redis Cache Performance",
    "hypothesis": "Perfil em Redis atualiza em <500ms",
    "component": "cache",
    "target_events": 50,
    "target_metric_name": "latency_ms",
    "target_metric_value": 500,
    "acceptance_criteria": {
      "max_latency_ms": 500,
      "min_success_rate": 0.98
    },
    "target_completion_date": "2025-03-21"
  }'

# Resposta:
{
  "success": true,
  "checkpoint_id": "abc-123-def-456",
  "status": "created"
}
```

### **Passo 3: Agendar Scripts de Coleta no Windmill**

```javascript
// No Windmill UI:
// 1. Copiar week1_redis_cache.py para Windmill
// 2. Criar Schedule: "0 */6 * * *" (a cada 6h)
// 3. Passar env var: VALIDATION_CHECKPOINT_WEEK1=abc-123-def-456
```

Ou via API:

```bash
curl -X POST http://localhost:8000/api/windmill/schedules/create \
  -H "Authorization: Bearer YOUR_WINDMILL_TOKEN" \
  -d '{
    "path": "u/validation/week1_schedule",
    "schedule": "0 */6 * * *",
    "script_path": "u/validation/week1_redis_cache",
    "args": {
      "VALIDATION_CHECKPOINT_WEEK1": "abc-123-def-456"
    },
    "enabled": true
  }'
```

### **Passo 4: Registrar Eventos Manualmente (ou via Windmill)**

Quando os scripts Windmill rodam, eles já registram eventos automaticamente. Mas você pode registrar manualmente:

```bash
curl -X POST http://localhost:8000/api/validation/events/record \
  -H "Authorization: Bearer YOUR_ADMIN_KEY" \
  -d '{
    "checkpoint_id": "abc-123-def-456",
    "event_type": "performance_sample",
    "event_data": {
      "operation": "update_profile",
      "timestamp": "2025-03-14T10:30:00Z"
    },
    "metric_name": "latency_ms",
    "metric_value": 245.5,
    "metric_unit": "ms",
    "is_valid": true,
    "related_customer_id": "cust_001"
  }'
```

### **Passo 5: Consultar Diagnóstico em Tempo Real**

```bash
curl -X POST http://localhost:8000/api/validation/diagnose/abc-123-def-456 \
  -H "Authorization: Bearer YOUR_ADMIN_KEY"

# Resposta (diagnóstico consolidado):
{
  "checkpoint": {
    "id": "abc-123-def-456",
    "name": "Redis Cache Performance",
    "hypothesis": "Perfil em Redis atualiza em <500ms",
    "status": "in_progress",
    ...
  },
  "diagnostic": {
    "events_collected": 42,
    "events_target": 50,
    "completion_percentage": 84,
    "avg_metric_value": 342.5,
    "min_metric_value": 120.3,
    "max_metric_value": 498.2,
    "stddev_metric_value": 85.4,
    "valid_events": 41,
    "anomalies_detected": 2,
    "critical_anomalies": 0,
    "meets_acceptance_criteria": true,
    "blockers": []
  },
  "status": "collecting",
  "is_healthy": true
}
```

---

## 📈 Dashboard de Progresso (Frontend)

Componente React para visualizar progresso:

```jsx
// frontend/app/validation/page.tsx
import { useEffect, useState } from 'react';

export default function ValidationDashboard() {
  const [diagnostics, setDiagnostics] = useState([]);

  useEffect(() => {
    // Buscar todos os diagnósticos
    fetch('/api/validation/diagnostics', {
      headers: { 'Authorization': `Bearer ${process.env.NEXT_PUBLIC_API_KEY}` }
    })
    .then(r => r.json())
    .then(setDiagnostics);
  }, []);

  return (
    <div className="grid grid-cols-2 gap-4 p-6">
      {diagnostics.map(d => (
        <div key={d.checkpoint_id} className="border rounded p-4">
          {/* Progress Bar */}
          <div className="mb-2">
            <h3 className="font-bold">{d.checkpoint_id}</h3>
            <p className="text-sm text-gray-500">
              {d.events_collected} / {d.events_target} eventos
            </p>
            <div className="w-full bg-gray-200 rounded h-2">
              <div
                className={`h-full rounded ${
                  d.meets_acceptance_criteria ? 'bg-green-500' : 'bg-yellow-500'
                }`}
                style={{ width: `${d.completion_percentage}%` }}
              />
            </div>
          </div>

          {/* Metrics */}
          <div className="text-sm space-y-1">
            <p>📊 Média: {d.avg_metric_value?.toFixed(2)}</p>
            <p>🔴 Min: {d.min_metric_value?.toFixed(2)}</p>
            <p>🟢 Max: {d.max_metric_value?.toFixed(2)}</p>
            <p>📈 Desvio: {d.stddev_metric_value?.toFixed(2)}</p>
          </div>

          {/* Blockers */}
          {d.blockers.length > 0 && (
            <div className="mt-3 p-2 bg-red-100 rounded">
              {d.blockers.map((blocker, i) => (
                <p key={i} className="text-xs text-red-700">{blocker}</p>
              ))}
            </div>
          )}

          {/* Status */}
          <div className="mt-3 text-xs">
            {d.meets_acceptance_criteria ? (
              <span className="text-green-600 font-bold">✓ Atende Critérios</span>
            ) : (
              <span className="text-yellow-600">⏳ Aguardando Dados</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
```

---

## 🔍 Detecção Automática de Anomalias

O sistema detecta automaticamente:

1. **Outliers (3σ):** Valores > 3 desvios padrão da média
2. **Threshold Exceeded:** Métrica acima/abaixo do limite
3. **Unexpected State:** Evento que não deveria ter acontecido

Exemplo de anomalia registrada:

```json
{
  "anomaly_id": "xyz-789",
  "checkpoint_id": "abc-123",
  "anomaly_type": "outlier",
  "severity": "high",
  "description": "Latência 1245ms está 3σ acima da média (342ms)",
  "detected_value": 1245,
  "expected_range_min": 85.7,
  "expected_range_max": 598.3,
  "action_taken": "logged",
  "created_at": "2025-03-14T10:35:22Z"
}
```

---

## 📋 Checklist Semanal

### **Semana 1** (Redis Cache)
- [ ] API `/validation/checkpoints/create` funcionando
- [ ] Script `week1_redis_cache.py` no Windmill
- [ ] Schedule executando a cada 6 horas
- [ ] 50 eventos coletados
- [ ] Diagnóstico mostrando média <500ms
- [ ] Nenhuma anomalia crítica

### **Semana 2** (CSP Solver)
- [ ] Checkpoint semana 1 completado com sucesso
- [ ] Script `week2_csp_solver.py` no Windmill
- [ ] 100 eventos coletados
- [ ] Solver tempo <2000ms em 90% dos casos
- [ ] Nenhuma anomalia que impeça produção

### **Semana 3** (FSM Conflito)
- [ ] Checkpoint semana 2 completado
- [ ] Script `week3_fsm_conflict.py` em staging
- [ ] 30 eventos de conflito
- [ ] 80% resolvidos sem escalação
- [ ] Dashboard mostrando histórico de decisões

### **Semana 4** (Load Test)
- [ ] Checkpoints 1-3 completados
- [ ] Script `week4_windmill_load.py` em staging
- [ ] 1000 jobs simulados
- [ ] P99 latência <5000ms
- [ ] Erro rate <1%
- [ ] **Go/No-Go decision** para produção

---

## 🛠️ Troubleshooting

### Evento não registrando?
```bash
# Verificar se checkpoint existe
curl -X GET http://localhost:8000/api/validation/checkpoints \
  -H "Authorization: Bearer YOUR_KEY"

# Checar logs do Windmill
curl -X GET http://localhost:8001/api/jobs/[job_id]/logs \
  -H "Authorization: Bearer YOUR_WINDMILL_TOKEN"
```

### Diagnóstico vazio?
```bash
# Verificar se eventos estão sendo coletados
curl -X GET http://localhost:8000/api/validation/events/[checkpoint_id] \
  -H "Authorization: Bearer YOUR_KEY"

# Confirmar que eventos_target está correto
curl -X GET http://localhost:8000/api/validation/checkpoints/[checkpoint_id] \
  -H "Authorization: Bearer YOUR_KEY"
```

### Métrica não aparecendo?
- Certificar que `metric_name` e `metric_value` estão preenchidos
- Verificar se `metric_unit` é válido (ms, count, score, percentage)
- Confirmar que evento tem `is_valid=true`

---

## 📚 Documentação Adicional

- **Windmill Scripts:** Veja `windmill/validation/week*.py`
- **API Reference:** `/api/validation/` no Swagger
- **Banco de Dados:** Schema em `migrations/015_validation_framework.sql`
- **Frontend:** Componentes em `frontend/app/validation/`

---

## ✅ Roadmap Pós-Validação

Se tudo passar nas 4 semanas:

1. **Semana 5:** Deploy para produção com feature flags
2. **Semana 6-8:** Monitoramento contínuo em produção
3. **Semana 9+:** Otimizações baseadas em dados reais

Se algo falhar:
- 🔴 **Crítico:** Pause, investigate, iterate
- 🟡 **Médio:** Continue com mitigações
- 🟢 **Baixo:** Log, monitor, address em próximo sprint

---

**Last Updated:** 2025-03-14
**Framework Version:** 1.0
**Owner:** UNALUX Engineering
