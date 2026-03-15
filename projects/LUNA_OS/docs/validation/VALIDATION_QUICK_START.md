# 🚀 Quick Start - Validation Framework

**TL;DR:** Sistema que rastreia 4 hipóteses em 4 semanas com observabilidade integrada. Você define o alvo, o Windmill coleta dados, o API diagnostica automaticamente.

---

## ⚡ 5 Minutos para Começar

### 1️⃣ Rodar Script de Inicialização
```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/projects/LUNA_OS

# Definir seu admin key (encontrar em .env)
export ADMIN_KEY="seu_admin_key_aqui"
export WINDMILL_TOKEN="seu_windmill_token_aqui"

# Executar init
bash scripts/init_validation_framework.sh
```

**Saída esperada:**
```
🔬 UNALUX Validation Framework - Initialization
✓ Fases criadas
✓ 4 Checkpoints criados
✓ Coleta de dados iniciada
✓ Schedules configurados no Windmill

Checkpoint IDs:
  Week 1 (Redis): abc-123-...
  Week 2 (CSP):   def-456-...
  Week 3 (FSM):   ghi-789-...
  Week 4 (Load):  jkl-012-...
```

### 2️⃣ Copiar Scripts para Windmill
```bash
# No UI do Windmill (http://localhost:8001):
# 1. Criar 4 scripts novos
# 2. Colar conteúdo de windmill/validation/week*.py
# 3. Deploy cada um

# OU via CLI:
windmill sync "windmill/validation/" --yes
```

### 3️⃣ Ver Dashboard de Progresso
```
Abrir: http://localhost:3000/validation
```

Dashboard mostra:
- ⏳ Progresso (5/50 eventos coletados)
- 📊 Métricas (média, min, max)
- 🔴 Anomalias detectadas
- ✅ Status (atende critérios?)

### 4️⃣ Monitorar via CLI
```bash
# Listar todos os diagnósticos
curl -X GET http://localhost:8000/api/validation/diagnostics \
  -H "Authorization: Bearer $ADMIN_KEY" | jq

# Ver diagnóstico detalhado de um checkpoint
curl -X POST http://localhost:8000/api/validation/diagnose/abc-123-... \
  -H "Authorization: Bearer $ADMIN_KEY" | jq

# Ver eventos coletados
curl -X GET http://localhost:8000/api/validation/events/abc-123-... \
  -H "Authorization: Bearer $ADMIN_KEY" | jq '.[] | {event_type, metric_value}'
```

---

## 📅 Timeline das 4 Semanas

```
┌──────────────────────────────────────────────────────────┐
│ SEMANA 1 (Redis Cache)                        50 eventos │
│ Alvo: latência <500ms                     Risco: 🟢 Baixo │
│ ├─ Seg: Setup Windmill schedule                          │
│ ├─ Ter-Sex: Coleta rodando a cada 6h                     │
│ └─ Sab: Análise, 50 eventos? Atende critérios?          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SEMANA 2 (CSP Solver)                        100 eventos │
│ Alvo: solver <2000ms, 90% sucesso         Risco: 🟡 Médio │
│ ├─ Seg: Ativar schedule week 2                           │
│ ├─ Ter-Sex: Coleta rodando a cada 4h                     │
│ └─ Sab: Análise, performance aceitável?                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SEMANA 3 (FSM Conflito)                      30 eventos  │
│ Alvo: 80% resolvido sem escalação         Risco: 🟡 Médio │
│ ├─ Seg: Ativar schedule week 3 em staging                │
│ ├─ Ter-Sex: Coleta de conflitos simulados                │
│ └─ Sab: Análise, FSM funcionando bem?                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SEMANA 4 (Load Test Windmill)               1000 eventos  │
│ Alvo: P99 <5000ms, erro <1%                Risco: 🔴 Alto │
│ ├─ Seg: Ativar schedule week 4 em staging                │
│ ├─ Ter-Sex: Coleta de jobs em alta carga                 │
│ └─ Sab: GO/NO-GO decision para produção                  │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Entender a Métrica

### Exemplo: Week 1 (Redis Cache)

**Meta:** 50 eventos com latência <500ms

**Um evento = uma atualização de perfil:**
```
Evento:
  timestamp: 2025-03-14T10:30:45.123Z
  operation: update_profile_redis_supabase
  customer_id: customer_042
  latency_ms: 245.5
  is_valid: true ✓
```

**Diagnóstico após 25 eventos:**
```json
{
  "completion_percentage": 50,
  "avg_metric_value": 342.5,
  "min_metric_value": 120.3,
  "max_metric_value": 498.2,
  "stddev_metric_value": 85.4,
  "meets_acceptance_criteria": true,
  "blockers": []
}
```

✅ **Interpretação:**
- 50% do caminho (25/50 eventos)
- Média 342.5ms < 500ms ✓
- Todos os eventos válidos ✓
- Sem anomalias críticas ✓
- **Status:** Atende critérios até agora!

---

## 🚨 Quando Algo Dá Errado

### Cenário 1: Latência Alta

```json
{
  "events_collected": 30,
  "avg_metric_value": 620.5,
  "max_metric_value": 1850.3,
  "meets_acceptance_criteria": false,
  "blockers": [
    "⚠️ Latência acima do limite (620.5ms > 500ms)",
    "⚠️ Variabilidade alta nas métricas"
  ]
}
```

**O que fazer:**
1. Verificar logs do Redis (conexão lenta?)
2. Verificar Supabase (replicação lenta?)
3. Otimizar query ou aumentar pool de conexões
4. Rodar script novamente com melhorias

### Cenário 2: Anomalia Crítica

```
⚠️ 3 anomalias críticas detectadas
  - Outlier: latência 2500ms (3σ acima da média)
  - Threshold Exceeded: 1 erro ao conectar Redis
  - Unexpected State: evento com is_valid=false
```

**O que fazer:**
1. Clicar em anomalia para ver detalhes
2. Investigar causa (network issue? memory spike?)
3. Mitigar ou corrigir
4. Continuar coleta (anomalias são esperadas)

### Cenário 3: Objetivo Não Atingido

```
Semana 1 concluiu:
  - ❌ Latência média 620ms > 500ms
  - ✅ Taxa de sucesso 98% >= 98%
  - ❌ Variabilidade alta (stddev 250ms)

Decisão: BLOQUEADOR
```

**Opções:**
1. **Replit:** Corrigir raiz do problema, validar novamente
2. **Mitigar:** Aceitar latência maior com compensação em outro lugar
3. **Escalar:** Conversar com time sobre trade-offs

---

## 📊 Glossário de Métricas

| Métrica | O Que Significa | Unidade | Alvo | Crítico Se |
|---------|-----------------|--------|------|-----------|
| latency_ms | Tempo para operação completar | ms | <500 | >1000ms |
| solver_time_ms | Tempo do CSP solver rodar | ms | <2000 | >5000ms |
| resolution_rate | % de conflitos resolvidos | % | ≥80 | <50 |
| escalation_rate | % de conflitos escalados | % | ≤10 | >30 |
| job_latency_ms | Tempo de job Windmill | ms | P99<5000 | P99>10000 |
| error_rate | % de jobs com erro | % | <1 | >5 |

---

## 🔧 Endpoints Chave

```bash
# Criar checkpoint manual
POST /api/validation/checkpoints/create

# Registrar evento manual
POST /api/validation/events/record

# Ver diagnóstico
POST /api/validation/diagnose/{checkpoint_id}

# Listar todos os diagnósticos
GET /api/validation/diagnostics

# Ver eventos coletados
GET /api/validation/events/{checkpoint_id}

# Ver anomalias
GET /api/validation/anomalies/{checkpoint_id}

# Listar fases
GET /api/validation/phases
```

---

## 📈 Dashboard Frontend

Components implementados em `frontend/app/validation/`:

```tsx
// Componentes disponíveis
<ValidationPhaseCard />      // Mostra uma fase
<MetricsChart />             // Gráfico de métricas
<CheckpointProgress />       // Progress bar
<AnomalyAlert />             // Alerta de anomalia
<DiagnosticSummary />        // Resumo consolidado
```

Você pode:
- 📊 Ver gráficos em tempo real
- 🔍 Drill down em anomalias
- 💾 Exportar dados como CSV
- 🔔 Receber notificações ao atingir alvo

---

## ❓ FAQ

**P: Quando começo a coleta?**
A: Imediatamente após rodar `init_validation_framework.sh`. Scripts rodam nos horários configurados (Week 1 a cada 6h, Week 2 a cada 4h, etc).

**P: Posso registrar eventos manualmente?**
A: Sim! Use `POST /api/validation/events/record`. Útil se quiser validar algo específico fora da schedule.

**P: O que significa "anomalia"?**
A: Valor fora do padrão (3 desvios padrão da média). Não é erro! É só aviso de que algo saiu do normal.

**P: Posso pausar/retomar validação?**
A: Sim! Pause a schedule no Windmill. Dados continuam sendo agregados quando você re-ativar.

**P: Como exporto os dados?**
A: `GET /api/validation/diagnostics` retorna JSON. Pipe para `jq > diagnostics.json` ou use dashboard export.

**P: Preciso completar os 4 checkpoints em ordem?**
A: Não! Mas é recomendado porque cada um valida um bloco construído no anterior (Redis → Solver → FSM → Windmill).

---

## 🎓 Próximo Nível

Quando terminar as 4 semanas:
1. Leia `VALIDATION_FRAMEWORK.md` (doc completa)
2. Entenda como anomalias são detectadas
3. Customize critérios de aceitação
4. Integre com seu CI/CD (falhar build se checkpoint não atender)
5. Configure alertas Slack/email para anomalias críticas

---

**Documentação:** `VALIDATION_FRAMEWORK.md`
**Scripts:** `windmill/validation/week*.py`
**API:** OpenAPI em `/api/docs`
**Suporte:** Veja troubleshooting section em `VALIDATION_FRAMEWORK.md`
