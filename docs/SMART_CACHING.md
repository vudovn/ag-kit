# 🚀 Smart Caching Guide

## Visão Geral

Smart Caching reduz chamadas de API em **100x** usando cache em memória com TTL configurável.

---

## 📊 Impacto

### Antes (Sem Cache)
```
100 mensagens → 100 requests no CRM
→ Lento (2-3s por request)
→ Caro (100 requests pagos)
→ CRM sobrecarregado
```

### Depois (Com Cache)
```
100 mensagens → 1 request no CRM (cache 5min)
→ Rápido (<10ms cache hit)
→ Barato (99% menos requests)
→ CRM saudável
```

---

## ⚡ Performance Esperada

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Cache Hit Rate** | 0% | 95%+ | +95% |
| **Latência** | 2-3s | <10ms | -99% |
| **API Requests** | 100/min | 1/min | -99% |
| **Custo API** | 100% | 1% | -99% |

---

## 🔧 Instalação

### 1. Habilitar Feature Flag

```bash
# .env
FEATURE_SMART_CACHE=true
```

### 2. Importar Cache

```python
# brain/runtime.py
from brain.cache import contact_cache, is_smart_cache_enabled

def get_contact_memory(contact_id: str) -> dict:
    """Get contact with smart caching"""
    
    # Check feature flag
    if not is_smart_cache_enabled():
        return crm.get_contact(contact_id)
    
    # Try cache first
    cached = contact_cache.get(contact_id)
    if cached is not None:
        return cached
    
    # Cache miss: fetch from CRM
    contact = crm.get_contact(contact_id)
    
    # Save to cache
    contact_cache.set(contact_id, contact)
    
    return contact
```

---

## 📖 Uso

### Básico

```python
from brain.cache import contact_cache

# Set
contact_cache.set("contact_123", {"name": "João", "ltv": 1000})

# Get
contact = contact_cache.get("contact_123")
if contact:
    print(f"Cache hit: {contact}")
else:
    print("Cache miss")
```

### Com Fallback

```python
def get_contact_with_fallback(contact_id: str):
    """Get contact with cache fallback"""
    
    # Try cache
    cached = contact_cache.get(contact_id)
    if cached:
        return cached
    
    # Fallback to CRM
    contact = crm.get_contact(contact_id)
    
    # Update cache
    contact_cache.set(contact_id, contact)
    
    return contact
```

### Invalidar Cache

```python
# Invalidar contato específico
contact_cache.invalidate("contact_123")

# Limpar todo cache
contact_cache.clear()
```

---

## ⚙️ Configuração

### Padrão (Recomendado)

```python
from brain.cache import ContactMemoryCache

contact_cache = ContactMemoryCache(
    ttl_seconds=300,    # 5 minutos
    max_size=1000       # 1000 contatos
)
```

### Alta Performance

```python
contact_cache = ContactMemoryCache(
    ttl_seconds=60,     # 1 minuto (dados mais frescos)
    max_size=5000       # 5000 contatos
)
```

### Baixa Memória

```python
contact_cache = ContactMemoryCache(
    ttl_seconds=600,    # 10 minutos (menos refresh)
    max_size=200        # 200 contatos
)
```

---

## 📊 Monitoramento

### Stats em Tempo Real

```python
stats = contact_cache.get_stats()

print(f"Hit rate: {stats['hit_rate']}")
print(f"Entries: {stats['entries']}")
print(f"Evictions: {stats['evictions']}")
print(f"Memory: {stats['memory_usage_mb']:.2f} MB")
```

### Output Exemplo

```json
{
  "hits": 950,
  "misses": 50,
  "hit_rate": "95.00%",
  "entries": 234,
  "max_size": 1000,
  "ttl_seconds": 300,
  "evictions": 12,
  "memory_usage_mb": 2.34
}
```

---

## 🐛 Troubleshooting

### Problema: Cache Hit Rate Baixo (<50%)

**Causas:**
- TTL muito curto
- Muitos contatos únicos
- Cache size muito pequeno

**Soluções:**
```python
# Aumentar TTL
contact_cache = ContactMemoryCache(ttl_seconds=600)  # 10min

# Aumentar max_size
contact_cache = ContactMemoryCache(max_size=5000)
```

---

### Problema: Memória Alta (>50MB)

**Causas:**
- max_size muito alto
- Dados grandes por contato

**Soluções:**
```python
# Reduzir max_size
contact_cache = ContactMemoryCache(max_size=500)

# Reduzir TTL
contact_cache = ContactMemoryCache(ttl_seconds=120)
```

---

### Problema: Dados Desatualizados

**Causas:**
- TTL muito longo
- Dados mudam frequentemente

**Soluções:**
```python
# Reduzir TTL
contact_cache = ContactMemoryCache(ttl_seconds=60)  # 1min

# Invalidar manualmente após update
crm.update_contact(contact_id, data)
contact_cache.invalidate(contact_id)
```

---

## 🔒 Feature Flag

### Habilitar

```bash
export FEATURE_SMART_CACHE=true
```

### Desabilitar (Rollback)

```bash
export FEATURE_SMART_CACHE=false
# Volta para código sem cache imediatamente
```

### Verificar Status

```python
from brain.cache import is_smart_cache_enabled

if is_smart_cache_enabled():
    print("Smart Cache: ATIVO")
else:
    print("Smart Cache: INATIVO")
```

---

## 📈 Métricas de Sucesso

### Semana 1

- [ ] Cache hit rate > 90%
- [ ] Latência média < 100ms
- [ ] Requests CRM -90%
- [ ] Memória < 10MB

### Semana 2

- [ ] Cache hit rate > 95%
- [ ] Latência média < 50ms
- [ ] Requests CRM -95%
- [ ] Zero erros de cache

### Mês 1

- [ ] Economia de API: R$ 500+/mês
- [ ] Tempo de resposta: -95%
- [ ] Zero downtime de cache
- [ ] Rollback nunca necessário

---

## 🎯 Best Practices

### ✅ Faça

```python
# Sempre verificar cache primeiro
cached = contact_cache.get(contact_id)
if cached:
    return cached

# Sempre salvar no cache após fetch
contact = crm.get_contact(contact_id)
contact_cache.set(contact_id, contact)

# Invalidar após update
contact_cache.invalidate(contact_id)
```

### ❌ Não Faça

```python
# Não ignorar cache
contact = crm.get_contact(contact_id)  # Lento!

# Não salvar dados inválidos
contact_cache.set(contact_id, None)  # inútil

# Não esquecer de invalidar
crm.update_contact(contact_id, data)
# contact_cache.invalidate(contact_id) ← esqueceu!
```

---

## 📚 API Reference

### ContactMemoryCache

```python
class ContactMemoryCache:
    def __init__(self, ttl_seconds=300, max_size=1000)
    def get(self, contact_id: str) -> Optional[Dict]
    def set(self, contact_id: str, data: Dict) -> bool
    def invalidate(self, contact_id: str) -> None
    def clear(self) -> None
    def get_stats(self) -> Dict[str, Any]
```

### MultiBrainCache

```python
class MultiBrainCache:
    def __init__(self, ttl_seconds=60, max_size=500)
    def get_brain(self, contact_id: str) -> Optional[str]
    def set_brain(self, contact_id: str, brain: str, reason: str) -> bool
    def invalidate_brain(self, contact_id: str) -> None
```

---

## 🔗 Links Relacionados

- `brain/cache.py` - Implementação completa
- `brain/tests/test_cache.py` - Testes unitários
- `docs/PARALLEL_EXECUTION.md` - Framework de execução
- `docs/IMPLEMENTATION_PACT.md` - Pacto de implementação

---

**Versão:** 1.0.0  
**Status:** ✅ Production Ready  
**Feature Flag:** `FEATURE_SMART_CACHE`  
**Rollback:** Set flag to `false`
