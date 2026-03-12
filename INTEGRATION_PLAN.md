# 🚀 PLANO DE INTEGRAÇÃO — Multi-Brain V2 + LUNA OS

**Data:** 2026-03-12  
**Objetivo:** Fazer Multi-Brain V2 funcionar no LUNA OS  
**Tempo Total:** 5-7 dias

---

## 📋 **O QUE PRECISA SER CRIADO**

### **1. BACKEND (2-3 dias)**

#### **Tarefa 1.1: Integrar Smart Caching**
**Arquivo:** `projects/LUNA_OS/backend/app/core/brain.py`

**O Que Fazer:**
```python
# Adicionar imports
import sys
sys.path.insert(0, '/Users/franciscotaveira.ads/Documents/antigravity-kit')

from brain.cache import contact_cache

# Usar no process_message
async def process_message(phone, name, message, history):
    # Smart Caching
    cached = contact_cache.get(phone)
    if cached:
        return cached
    
    # Processar...
    result = await process(...)
    
    # Salvar no cache
    contact_cache.set(phone, result)
    return result
```

**Tempo:** 2-3 horas

---

#### **Tarefa 1.2: Integrar Human Handoff**
**Arquivo:** `projects/LUNA_OS/backend/app/core/orchestrator.py`

**O Que Fazer:**
```python
from brain.handoff import check_handoff, create_handoff_request

# No orchestrator
async def human_gate(state):
    should, reason = check_handoff(conversation)
    if should:
        request = create_handoff_request(...)
        return escalate_to_human(reason)
```

**Tempo:** 3-4 horas

---

#### **Tarefa 1.3: Integrar Behavioral DNA**
**Arquivo:** `projects/LUNA_OS/backend/app/core/brain.py`

**O Que Fazer:**
```python
from brain.behavioral_dna import get_customer_dna, adapt_response_to_customer

# No process_message
dna = get_customer_dna(phone)
response = adapt_response_to_customer(base_response, phone)
```

**Tempo:** 2-3 horas

---

#### **Tarefa 1.4: Integrar Memory Chain**
**Arquivo:** `projects/LUNA_OS/backend/app/core/brain.py`

**O Que Fazer:**
```python
from brain.memory_chain import MemoryChain, log_interaction

chain = MemoryChain()

# Após cada interação
log_interaction({
    "contact_id": phone,
    "intent": intent,
    "outcome": "success"
})
```

**Tempo:** 2-3 horas

---

#### **Tarefa 1.5: Aplicar Migrations no Supabase**
**Arquivo:** `database/migrations/003_luna_os_integration.sql`

**O Que Fazer:**
1. Abrir Supabase Dashboard
2. Ir em SQL Editor
3. Copiar conteúdo do arquivo
4. Executar
5. Verificar: `SELECT * FROM feature_flags;`

**Tempo:** 30 minutos

---

### **2. FRONTEND (3-4 dias)**

#### **Tarefa 2.1: Dashboard Lux (Principal)**
**Arquivo:** `projects/LUNA_OS/frontend/app/lux-dashboard/page.tsx`

**O Que Criar:**
```tsx
// Dashboard principal com:
- Status do sistema
- Métricas em tempo real
- Quick actions
```

**Tempo:** 4-5 horas

---

#### **Tarefa 2.2: Memory Chain Viewer**
**Arquivo:** `projects/LUNA_OS/frontend/app/lux-dashboard/memory-chain/page.tsx`

**O Que Criar:**
```tsx
// Visualizar audit trail:
- Lista de hashes SHA-256
- Verificação de integridade
- Timeline de interações
```

**Tempo:** 6-8 horas

---

#### **Tarefa 2.3: Handoff Queue**
**Arquivo:** `projects/LUNA_OS/frontend/app/lux-dashboard/handoffs/page.tsx`

**O Que Criar:**
```tsx
// Fila de handoffs humanos:
- Lista de handoffs pendentes
- Aceitar handoff
- Resolver handoff
- Métricas de tempo
```

**Tempo:** 6-8 horas

---

#### **Tarefa 2.4: DNA Editor**
**Arquivo:** `projects/LUNA_OS/frontend/app/lux-dashboard/dna-editor/page.tsx`

**O Que Criar:**
```tsx
// Editor de Behavioral DNA:
- Lista de clientes
- Editar DNA por cliente
- Tom, vocabulário, emoji
- Preview em tempo real
```

**Tempo:** 6-8 horas

---

#### **Tarefa 2.5: API Integration**
**Arquivo:** `projects/LUNA_OS/frontend/app/api/lux/`

**O Que Criar:**
```
/api/lux/
├── metrics/route.ts       # Métricas do dashboard
├── memory-chain/route.ts  # Memory chain data
├── handoffs/route.ts      # Handoff queue
└── dna/route.ts           # DNA operations
```

**Tempo:** 4-5 horas

---

## 📊 **RESUMO DO TRABALHO**

| Área | Tarefas | Tempo |
|------|---------|-------|
| **Backend** | 5 tarefas | 2-3 dias |
| **Frontend** | 5 tarefas | 3-4 dias |
| **Database** | 1 tarefa | 30 min |
| **TOTAL** | **11 tarefas** | **5-7 dias** |

---

## ✅ **CHECKLIST COMPLETO**

### **Backend**
- [ ] 1.1 Integrar Smart Caching
- [ ] 1.2 Integrar Human Handoff
- [ ] 1.3 Integrar Behavioral DNA
- [ ] 1.4 Integrar Memory Chain
- [ ] 1.5 Aplicar Migrations no Supabase

### **Frontend**
- [ ] 2.1 Dashboard Lux
- [ ] 2.2 Memory Chain Viewer
- [ ] 2.3 Handoff Queue
- [ ] 2.4 DNA Editor
- [ ] 2.5 API Integration

### **Testes**
- [ ] Testar em staging
- [ ] Testar em produção
- [ ] Validar performance

---

## 🚀 **COMO COMEÇAR AGORA**

### **Opção 1: Eu Crio Tudo (Recomendado)**

**Diga:** "Cria tudo"

**Eu faço:**
1. Backend completo (2-3 dias)
2. Frontend completo (3-4 dias)
3. Testes e validação

**Resultado:** Multi-Brain V2 100% integrado

---

### **Opção 2: Eu Crio Backend, Você Faz Frontend**

**Diga:** "Cria só backend"

**Eu faço:**
1. Backend completo
2. Migrations aplicadas
3. API endpoints

**Você faz:**
1. Frontend Dashboard Lux

---

### **Opção 3: Priorizar (Produção Primeiro)**

**Diga:** "Prioriza produção"

**Eu faço:**
1. Smart Caching (1 hora)
2. Handoff (2 horas)
3. Migrations (30 min)

**Resultado:** Produção rápida, resto depois

---

## 📝 **MINHA RECOMENDAÇÃO**

### **Se Quer Produção Rápida:**

**Opção 3** — Priorizar produção:
- ✅ 3-4 horas
- ✅ Smart Caching + Handoff
- ✅ Produção imediata
- ⚠️ Resto depois

---

### **Se Quer Multi-Brain V2 Completo:**

**Opção 1** — Eu crio tudo:
- ✅ 5-7 dias
- ✅ Tudo integrado
- ✅ Dashboard Lux completo
- ✅ Produção completa

---

## 🎯 **DECISÃO**

**Qual você quer?**

1. **"Cria tudo"** — 5-7 dias, completo
2. **"Cria só backend"** — 2-3 dias, você faz front
3. **"Prioriza produção"** — 3-4 horas, rápido

---

**MCT LTDA 2026** | Integration Plan  
**Status:** ⏳ **Aguardando Decisão**  
**Próximo:** **VOCÊ DECIDE**
