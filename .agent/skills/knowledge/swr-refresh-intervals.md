# 🔄 SWR Refresh Intervals — Best Practices

**Created:** 2026-02-27  
**Status:** ✅ Actionable  
**Priority:** 🔴 High (Performance)

---

## Problema Identificado

Múltiplos componentes SWR com `refreshInterval` curtos geram excesso de requisições:

```tsx
// Dashboard (page.tsx)
refreshInterval: 30000  // 30s → 2 req/min
refreshInterval: 10000  // 10s → 6 req/min ⚠️
refreshInterval: 60000  // 60s → 1 req/min

// Conversas (conversations/page.tsx)
refreshInterval: 10000  // 10s → 6 req/min ⚠️
refreshInterval: 5000   // 5s → 12 req/min 🔴

// Clientes (clients/page.tsx)
refreshInterval: 30000  // 30s → 2 req/min

// Total: ~29 req/min por usuário ativo
```

---

## Impacto

### Backend (Supabase)
```
1 usuário ativo:
- 29 requisições/minuto
- 1,740 requisições/hora
- 41,760 requisições/dia (se rodar 24h)

10 usuários ativos:
- 290 req/min
- 17,400 req/hora
- 417,600 req/dia
```

**Custo Estimado (Supabase Pro):**
- 500M reads/mês incluídos
- 417K reads/dia → 12.5M reads/mês (dentro do limite)
- **Mas:** 10 usuários → 125M reads/mês (25% do limite)

---

## Guia de Refresh Intervals

### Dados Críticos (Tempo Real)
```tsx
// Chat ativo (usuário digitando)
refreshInterval: 3000  // 3s
revalidateOnFocus: true

// Justificativa: Usuário precisa ver resposta imediatamente
```

### Dados Importantes (Quase Real)
```tsx
// Lista de conversas (usuário na página)
refreshInterval: 15000  // 15s
revalidateOnFocus: true
revalidateOnReconnect: true

// Justificativa: Novas conversas podem chegar, mas 15s é aceitável
```

### Dados de Contexto (Dashboard)
```tsx
// KPIs de dashboard
refreshInterval: 30000  // 30s
revalidateOnFocus: true
revalidateOnReconnect: true

// Justificativa: Números não mudam tão rápido
```

### Dados Analíticos (Relatórios)
```tsx
// Analytics, relatórios, históricos
refreshInterval: 60000  // 60s
revalidateOnFocus: false  // Só recarrega se usuário sair/voltar
revalidateOnReconnect: true

// Justificativa: Dados históricos não mudam em tempo real
```

### Dados Estáticos (Configurações)
```tsx
// Configurações, perfis, preferências
refreshInterval: false  // Não recarrega automaticamente
revalidateOnFocus: false
revalidateOnReconnect: true

// Mutação manual quando necessário
mutate()
```

---

## Implementação Recomendada

### 1. Dashboard (page.tsx)
```tsx
// Antes
const { data } = useSWR('/api/analytics/dashboard?days=7', fetcher, {
  refreshInterval: 30000,
  revalidateOnFocus: true
})

const { data: maturityData } = useSWR('/api/evolution/maturity', fetcher, {
  refreshInterval: 10000  // ⚠️ Muito rápido
})

// Depois
const { data } = useSWR('/api/analytics/dashboard?days=7', fetcher, {
  refreshInterval: 30000,  // ✅ OK
  revalidateOnFocus: true,
  revalidateOnReconnect: true
})

const { data: maturityData } = useSWR('/api/evolution/maturity', fetcher, {
  refreshInterval: 30000,  // ✅ 30s (maturidade não muda tão rápido)
  revalidateOnFocus: false,  // ✅ Só recarrega se sair/voltar
  revalidateOnReconnect: true
})
```

---

### 2. Conversas (conversations/page.tsx)
```tsx
// Antes
const { data: conversations, mutate: mutateList } = useSWR<Conversation[]>('/api/conversations', fetcher, {
  refreshInterval: 10000  // ⚠️ Rápido
})

const { data: detail, isValidating: loadingMsgs } = useSWR<ConversationDetail>(
  selectedId ? `/api/conversations/${selectedId}` : null,
  fetcher,
  { refreshInterval: 5000 }  // 🔴 Muito rápido
)

// Depois
const { data: conversations, mutate: mutateList } = useSWR<Conversation[]>('/api/conversations', fetcher, {
  refreshInterval: 30000,  // ✅ 30s
  revalidateOnFocus: true,
  revalidateOnReconnect: true
})

const { data: detail, isValidating: loadingMsgs } = useSWR<ConversationDetail>(
  selectedId ? `/api/conversations/${selectedId}` : null,
  fetcher,
  {
    refreshInterval: selectedId ? 15000 : false,  // ✅ 15s apenas se conversa ativa
    revalidateOnFocus: true,
    revalidateOnReconnect: true,
    dedupingInterval: 3000  // ✅ Não duplica req em 3s
  }
)
```

---

### 3. Clientes (clients/page.tsx)
```tsx
// Antes
const { data: clientsData, error: clientsError } = useSWR<Client[]>('/api/clients', fetcher, {
  refreshInterval: 30000
})

// Depois
const { data: clientsData, error: clientsError } = useSWR<Client[]>('/api/clients', fetcher, {
  refreshInterval: 60000,  // ✅ 60s (clientes não mudam tão rápido)
  revalidateOnFocus: false,  // ✅ Só recarrega se sair/voltar
  revalidateOnReconnect: true,
  dedupingInterval: 5000  // ✅ Não duplica req em 5s
})
```

---

## Otimizações Adicionais

### 1. Pause When Invisible
```tsx
useSWR(key, fetcher, {
  refreshInterval: 30000,
  refreshWhenHidden: false,  // ✅ Não recarrega se aba invisível
  refreshWhenOffline: false  // ✅ Não recarrega se offline
})
```

### 2. Conditional Fetching
```tsx
const { data } = useSWR(
  selectedId ? `/api/conversations/${selectedId}` : null,  // ✅ Só fetch se tiver ID
  fetcher,
  { refreshInterval: 15000 }
)
```

### 3. Manual Mutation (Controle Total)
```tsx
const { data, mutate } = useSWR('/api/clients', fetcher, {
  refreshInterval: false  // ❌ Sem auto-refresh
})

// Atualizar manualmente quando necessário
const handleClientUpdate = async (newData) => {
  await mutate(newData, { revalidate: false })  // Otimistic update
}
```

---

## Monitoramento

### Métricas para Acompanhar

```typescript
// Adicionar logging no backend (FastAPI)
from loguru import logger
from datetime import datetime

@router.get("/conversations")
async def list_conversations():
    start = datetime.now()
    # ... query ...
    duration = (datetime.now() - start).total_seconds() * 1000
    logger.info(f"GET /conversations: {duration}ms")
```

### Dashboard de Requisições (Supabase)

```sql
-- Ver top endpoints mais chamados
SELECT
  path,
  count(*) as requests,
  avg(duration_ms) as avg_ms
FROM request_logs
GROUP BY path
ORDER BY requests DESC
LIMIT 10;
```

---

## Checklist de Implementação

- [ ] Atualizar Dashboard refreshInterval para 30s
- [ ] Atualizar Conversas lista para 30s
- [ ] Atualizar Conversas mensagens para 15s (apenas se ativa)
- [ ] Atualizar Clientes para 60s
- [ ] Adicionar `refreshWhenHidden: false`
- [ ] Adicionar `dedupingInterval: 3000-5000`
- [ ] Testar com múltiplas abas abertas
- [ ] Monitorar reqs/min no Supabase

---

## Meta de Performance

| Métrica | Atual | Após Otimização |
|---------|-------|-----------------|
| Requisições/min | ~29 | ~8 |
| Requisições/hora | ~1,740 | ~480 |
| Redução | - | **72% menos** |

---

## Referências

- [SWR Documentation](https://swr.vercel.app/docs/revalidation)
- [SWR Refresh Interval](https://swr.vercel.app/docs/revalidation#refresh-interval)
- [React Query Refresh Logic](https://tanstack.com/query/latest/docs/react/guides/window-focus-refetching)
