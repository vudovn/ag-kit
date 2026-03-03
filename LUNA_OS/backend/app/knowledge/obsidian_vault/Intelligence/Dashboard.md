# 🧠 Intelligence Dashboard

**Última Atualização:** <% tp.date.now("YYYY-MM-DD HH:mm") %>  
**Status:** 🟢 Operacional com Ollama Local

---

## 🚀 Status em Tempo Real

### Ollama Local
```dataview
TABLE ollama_model as "Modelo", processing_time_ms as "Tempo (ms)", confidence_score as "Confiança"
FROM "Intelligence/Ollama Insights"
WHERE created_at >= date(now) - dur(24 hours)
SORT created_at DESC
LIMIT 5
```

### Agentes Ativos
- ✅ ExtractorAgent
- ✅ PsychologyAgent
- ✅ SalesAgent
- ✅ BehaviorAgent
- ✅ InsightsAgent
- ✅ StorageAgent
- ✅ LearningAgent

---

## 📊 Insights Recentes (Últimas 24h)

```dataview
TABLE without id file.link as "Cliente", phone as "Telefone", confidence_score as "Confiança", created_at as "Data"
FROM "Intelligence/Ollama Insights"
WHERE created_at >= date(now) - dur(1 day)
SORT created_at DESC
LIMIT 10
```

---

## 🎯 Top Insights da Semana

```dataview
TABLE without id file.link as "Cliente", phone as "Telefone", priority_score as "Prioridade"
FROM "Intelligence/Ollama Insights"
WHERE created_at >= date(now) - dur(7 days)
SORT priority_score DESC
LIMIT 10
```

---

## 🧠 Perfis Psicológicos

### Tipos DISC Predominantes

```dataview
TABLE without id file.link as "Cliente", disc_type as "Tipo DISC", communication_style as "Estilo"
FROM "Intelligence/Psychology Profiles"
WHERE disc_type != null
SORT created_at DESC
LIMIT 10
```

---

## 💰 Padrões de Vendas

### Estágios do Funil (Últimos 7 dias)

```dataview
TABLE without id file.link as "Cliente", funnel_stage as "Estágio", conversion_probability as "Conversão %"
FROM "Intelligence/Sales Patterns"
WHERE created_at >= date(now) - dur(7 days)
SORT conversion_probability DESC
LIMIT 10
```

---

## 🚨 Alertas Ativos

### Alto Risco de Churn
```dataview
TABLE without id file.link as "Cliente", phone as "Telefone", churn_risk as "Risco"
FROM "Intelligence/Agent Analysis"
WHERE churn_risk = "alto"
SORT created_at DESC
```

### Objeções Não Resolvidas
```dataview
TABLE without id file.link as "Cliente", objections_count as "Objeções"
FROM "Intelligence/Agent Analysis"
WHERE objections_count > 2
SORT created_at DESC
```

---

## 📈 Métricas da Semana

| Métrica | Valor | Variação |
|---------|-------|----------|
| Conversas Analisadas | `= length(filter(file.path, contains("Intelligence/")))` | - |
| Insights Gerados | `= length(filter(file.path, contains("Ollama Insights/")))` | - |
| Perfis Criados | `= length(filter(file.path, contains("Psychology Profiles/")))` | - |
| Alertas Ativos | `= length(filter(file.path, contains("Agent Analysis/")) where churn_risk = "alto")` | - |

---

## 🎯 Ações Recomendadas

```dataview
TASK FROM "Intelligence"
WHERE !completed
GROUP BY file.link
```

---

## 🔗 Links Rápidos

- [[000_MCT_MASTER_INDEX]]
- [[Dashboard]]
- [[Ollama Integration]]
- [[Conversation Intelligence]]

---

*Dashboard atualizado automaticamente via Dataview*
