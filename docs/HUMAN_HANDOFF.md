# 🤝 Human Handoff Guide

## Visão Geral

Sistema inteligente de handoff que garante que **nenhum cliente seja abandonado** e casos complexos recebam atenção humana.

---

## 📊 Impacto

### Antes (Sem Handoff)
```
Cliente pede atendente → IA ignora → Cliente frustrado → Churn
IA falha 3x → Cliente sem resposta → Abandono
VIP tratado igual → Experiência ruim → Perda de receita
```

### Depois (Com Handoff)
```
Cliente pede atendente → Handoff imediato → Humano resolve → Satisfação
IA falha 2x → Handoff automático → Humano assume → Resolução
VIP detectado → Handoff prioritário → Atendimento premium → Retenção
```

---

## ⚡ Gatilhos de Handoff

| Gatilho | Detecção | Prioridade |
|---------|----------|------------|
| **Cliente pediu** | "quero falar com atendente" | 6/10 |
| **Baixa confiança** | intent_confidence < 0.5 | 4/10 |
| **Alto risco** | risk_score > 0.7 | 8/10 |
| **Reclamação** | "inaceitável", "cancelar" | 9/10 |
| **Múltiplas falhas** | ai_failure_count >= 2 | 6/10 |
| **VIP** | ltv > R$ 10.000 | 8/10 |

---

## 🔧 Instalação

### 1. Habilitar Feature Flag

```bash
# .env
FEATURE_HANDOFF=true
HANDOFF_CONFIDENCE_THRESHOLD=0.5
HANDOFF_MAX_AI_FAILURES=2
HANDOFF_VIP_LTV_THRESHOLD=10000
```

### 2. Integrar no Runtime

```python
# brain/runtime.py
from brain.handoff import (
    handoff_engine,
    HandoffReason,
    check_handoff,
    create_handoff_request
)

def process_message(conversation: dict):
    """Process message with handoff support"""
    
    # 1. Check if handoff needed
    should_handoff, reason = check_handoff(conversation)
    
    if should_handoff:
        # 2. Create handoff request
        request = create_handoff_request(conversation, reason)
        
        # 3. Change mode to human
        conversation["mode"] = "human_active"
        
        # 4. Notify humans
        notify_operators(request)
        
        # 5. Inform customer
        return {
            "text": f"Vou transferir você para {operator_name}. Ele já está ciente do seu caso!"
        }
    
    # Continue with AI processing
    return ai_response(conversation)
```

---

## 📖 Uso

### Verificar Handoff

```python
from brain.handoff import check_handoff

conversation = {
    "id": "conv_001",
    "contact": {"ltv": 5000},
    "messages": [{"text": "Quero atendente"}],
    "intent_confidence": 0.85,
    "risk_score": 0.2
}

should, reason = check_handoff(conversation)
if should:
    print(f"Handoff necessário: {reason}")
```

### Criar Request

```python
from brain.handoff import create_handoff_request, HandoffReason

request = create_handoff_request(
    conversation=conversation,
    reason=HandoffReason.CUSTOMER_REQUESTED,
    priority=7  # Opcional, calculado automaticamente
)

print(f"Handoff criado: {request.conversation_id}")
print(f"Prioridade: {request.priority}")
```

### Aceitar Handoff

```python
from brain.handoff import handoff_engine

accepted = handoff_engine.accept_handoff(
    conversation_id="conv_001",
    operator_id="operator_123"
)
```

### Resolver Handoff

```python
resolved = handoff_engine.resolve_handoff(
    conversation_id="conv_001",
    notes="Issue resolved successfully"
)
```

---

## 🎯 Prioridades

### Prioridade Automática

| Razão | Base | VIP Bônus |
|-------|------|-----------|
| Reclamação | 9/10 | +2 = 10/10 |
| Alto Risco | 8/10 | +2 = 10/10 |
| VIP | 8/10 | - |
| Cliente Pediu | 6/10 | +2 = 8/10 |
| Múltiplas Falhas | 6/10 | +2 = 8/10 |
| Baixa Confiança | 4/10 | +2 = 6/10 |

---

## 📊 Monitoramento

### Stats em Tempo Real

```python
from brain.handoff import handoff_engine

stats = handoff_engine.get_stats()

print(f"Pendentes: {stats['pending']}")
print(f"Resolvidos: {stats['resolved']}")
print(f"Tempo médio aceite: {stats['avg_time_to_accept']:.1f}s")
print(f"Por razão: {stats['by_reason']}")
```

### Output Exemplo

```json
{
  "pending": 3,
  "resolved": 15,
  "total": 18,
  "by_reason": {
    "customer_requested": 8,
    "low_confidence": 3,
    "high_risk": 2,
    "vip_customer": 5
  },
  "avg_time_to_accept": 12.5,
  "thresholds": {
    "confidence": 0.5,
    "max_failures": 2,
    "vip_ltv": 10000
  }
}
```

---

## ⚙️ Configuração

### Padrão (Recomendado)

```bash
FEATURE_HANDOFF=true
HANDOFF_CONFIDENCE_THRESHOLD=0.5
HANDOFF_MAX_AI_FAILURES=2
HANDOFF_VIP_LTV_THRESHOLD=10000
```

### Mais Agressivo (Mais handoffs)

```bash
HANDOFF_CONFIDENCE_THRESHOLD=0.7      # Mais sensível
HANDOFF_MAX_AI_FAILURES=1             # Falhou 1x → handoff
HANDOFF_VIP_LTV_THRESHOLD=5000        # VIP mais fácil
```

### Mais Conservador (Menos handoffs)

```bash
HANDOFF_CONFIDENCE_THRESHOLD=0.3      # Menos sensível
HANDOFF_MAX_AI_FAILURES=3             # Tenta 3x
HANDOFF_VIP_LTV_THRESHOLD=20000       # Só VIPs muito altos
```

---

## 🐛 Troubleshooting

### Problema: Muitos Handoffs

**Sintomas:**
- Operadores sobrecarregados
- Handoffs > 50% das conversas

**Soluções:**
```bash
# Aumentar threshold de confiança
HANDOFF_CONFIDENCE_THRESHOLD=0.3

# Aumentar falhas permitidas
HANDOFF_MAX_AI_FAILURES=3
```

---

### Problema: Poucos Handoffs

**Sintomas:**
- Clientes frustrados
- Churn aumentando

**Soluções:**
```bash
# Diminuir threshold de confiança
HANDOFF_CONFIDENCE_THRESHOLD=0.7

# Diminuir falhas permitidas
HANDOFF_MAX_AI_FAILURES=1

# Diminuir threshold VIP
HANDOFF_VIP_LTV_THRESHOLD=5000
```

---

### Problema: Demora no Aceite

**Sintomas:**
- Tempo médio > 30s
- Clientes esperando

**Soluções:**
1. Aumentar equipe de operadores
2. Implementar notificação push
3. Criar SLA de aceite (< 15s)

---

## 🔒 Feature Flag

### Habilitar

```bash
export FEATURE_HANDOFF=true
```

### Desabilitar (Rollback)

```bash
export FEATURE_HANDOFF=false
# IA handles everything (sem handoff)
```

---

## 📈 Métricas de Sucesso

### Semana 1

- [ ] 100% handoffs detectados
- [ ] Tempo médio aceite < 30s
- [ ] Zero handoffs perdidos
- [ ] Operadores notificados

### Semana 2

- [ ] Tempo médio aceite < 15s
- [ ] Handoff rate: 10-20%
- [ ] Satisfação cliente: > 90%
- [ ] Zero abandonos

### Mês 1

- [ ] Churn reduzido 20%
- [ ] VIP retention: > 95%
- [ ] Resolução primeira tentativa: > 80%
- [ ] NPS handoff: > 70

---

## 🎯 Best Practices

### ✅ Faça

```python
# Sempre verificar handoff antes de responder
should, reason = check_handoff(conversation)
if should:
    return handle_handoff(reason)

# Sempre informar cliente do handoff
return f"Vou transferir para {operator}. Ele já sabe do seu caso!"

# Sempre registrar resolução
handoff_engine.resolve_handoff(conv_id, "Resolved")
```

### ❌ Não Faça

```python
# Não ignore pedido de humano
# ❌ return ai_response(conversation)
# ✅ return handle_handoff(CUSTOMER_REQUESTED)

# Não esqueça de invalidar modo
# ❌ conversation["mode"] = "ai_active"  # depois do handoff
# ✅ manter "human_active" até resolução

# Não deixe handoff pendente
# ❌ handoff_engine.accept_handoff(...)  # sem resolve
# ✅ sempre resolver após atendimento
```

---

## 🔗 Links Relacionados

- `brain/handoff.py` - Implementação completa
- `brain/tests/test_handoff.py` - Testes unitários
- `brain/cache.py` - Smart Caching
- `docs/SMART_CACHING.md` - Guia de caching
- `docs/MULTI_BRAIN_MOATS.md` - Multi-Brain strategy

---

**Versão:** 1.0.0  
**Status:** ✅ Production Ready  
**Feature Flag:** `FEATURE_HANDOFF`  
**Rollback:** Set flag to `false`
