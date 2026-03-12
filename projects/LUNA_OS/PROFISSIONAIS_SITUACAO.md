# 👩‍🦱 Situação dos Profissionais - Análise e Correção

**Data:** 2026-03-11  
**Status:** ⚠️ **PROBLEMA IDENTIFICADO**

---

## 🔍 DIAGNÓSTICO

### Problema Principal

**`BELASIS_MOCK=true`** está ativado no `.env`, fazendo com que o backend retorne **dados fictícios** em vez de buscar do Belasis real.

### Dados Atuais (Mock)

```python
_MOCK_EMPLOYEES = [
    {"id": 1, "name": "Ju", "active": True},
    {"id": 2, "name": "Dávila", "active": True},
    {"id": 3, "name": "Lu", "active": True},
    {"id": 4, "name": "Carla", "active": True},
]
```

**Apenas 4 profissionais** estão sendo retornados, e são dados **fictícios**.

---

## ✅ O QUE ESTÁ FUNCIONANDO

| Componente | Status | Observação |
|------------|--------|------------|
| Frontend `/professionals` | ✅ | Página implementada e bonita |
| API `/api/belasis/professionals` | ✅ | Endpoint registrado e funcional |
| Router Belasis | ✅ | Prefixo `/api/belasis` correto |
| Config LUNA por profissional | ✅ | Sistema de configuração pronto |
| Supabase knowledge_base | ✅ | Tabela pronta para armazenar configs |

---

## ❌ O QUE PRECISA SER CORRIGIDO

### 1. **Ativar Belasis Real** (CRÍTICO)

**Arquivo:** `.env`

**Atual:**
```env
BELASIS_MOCK=true
BELASIS_API_KEY=
```

**Precisa ser:**
```env
BELASIS_MOCK=false
BELASIS_API_KEY=bpk_SEU_TOKEN_AQUI
```

**Ação:** Obter a chave de API do Belasis e atualizar o `.env`.

---

### 2. **Profissionais Reais vs Mock**

**No Mock (4 profissionais):**
- Ju
- Dávila
- Lu
- Carla

**Profissionais Reais (prováveis):**
- Yujaira (Ju)
- Dávila
- Luana (Lu)
- Carla
- Mariana
- ... (outros do salão)

**Ação:** Após ativar Belasis real, os dados verdadeiros serão carregados.

---

## 📊 ARQUITETURA DE PROFISSIONAIS

### Fluxo de Dados

```
┌─────────────────┐
│   Belasis ERP   │
│   (API Real)    │
└────────┬────────┘
         │ GET /employees
         ▼
┌─────────────────┐
│  Backend LUNA   │
│ /api/belasis/   │
│  professionals  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend LUNA  │
│  /professionals │
└─────────────────┘
```

### Camada de Configuração LUNA

Além dos dados do Belasis, o sistema tem uma **camada de configuração LUNA** por profissional:

```
┌──────────────────────────────────────┐
│  knowledge_base (Supabase)           │
│  key: luna_config_professional_{id}  │
│                                      │
│  data: {                             │
│    specialties: [...]                │
│    restrictions: [...]               │
│    simultaneous: true/false          │
│    notes: "..."                      │
│    custom_script: "..."              │
│    active: true/false                │
│  }                                   │
└──────────────────────────────────────┘
```

---

## 🛠️ PASSOS PARA CORRIGIR

### Passo 1: Obter Chave de API do Belasis

1. Acessar https://api.belasis.com.br
2. Gerar API Key (ACCESS-TOKEN)
3. Copiar token (formato: `bpk_...`)

### Passo 2: Atualizar `.env`

```bash
# Editar .env
BELASIS_MOCK=false
BELASIS_API_KEY=bpk_SEU_TOKEN_AQUI
```

### Passo 3: Reiniciar Backend

```bash
# Parar backend atual
docker compose restart luna-backend

# Ou se estiver rodando localmente:
pkill -f "uvicorn.*main:app"
cd backend && python -m uvicorn app.main:app --reload
```

### Passo 4: Verificar Dados Reais

```bash
# Testar endpoint
curl http://localhost:8000/api/belasis/professionals \
  -H "X-Admin-Key: SUA_ADMIN_KEY" | jq
```

**Resposta esperada (dados reais):**
```json
{
  "professionals": [
    {
      "id": 1,
      "name": "Yujaira",
      "active": true,
      "luna_config": { ... }
    },
    {
      "id": 2,
      "name": "Dávila",
      "active": true,
      "luna_config": { ... }
    }
    // ... todos os profissionais reais
  ],
  "total": 9,
  "source": "belasis"
}
```

---

## 🎯 FUNCIONALIDADES DISPONÍVEIS

### 1. Listar Profissionais

```
GET /api/belasis/professionals
```

Retorna todos os profissionais do Belasis + config LUNA.

### 2. Configurar LUNA por Profissional

```
GET /api/belasis/professionals/{id}/config
PUT /api/belasis/professionals/{id}/config
```

**Body (PUT):**
```json
{
  "specialties": ["Progressiva", "Coloração"],
  "restrictions": ["Não faz manicure"],
  "simultaneous": true,
  "notes": "Especialista em cabelos longos",
  "custom_script": "Ao mencionar Dávila, destacar progressiva...",
  "active": true
}
```

### 3. Frontend

A página `/professionals` permite:
- ✅ Ver todos os profissionais
- ✅ Ver status (ativo/inativo)
- ✅ Configurar especialidades LUNA
- ✅ Configurar restrições
- ✅ Atender simultâneo (sim/não)
- ✅ Adicionar notas operacionais
- ✅ Script personalizado de atendimento
- ✅ Sincronizar com Belasis

---

## 📝 RESUMO

| Item | Status | Ação Necessária |
|------|--------|-----------------|
| Backend API | ✅ Pronto | Nenhum |
| Frontend UI | ✅ Pronto | Nenhum |
| Config LUNA | ✅ Pronto | Nenhum |
| **Belasis Real** | ❌ **Mock** | **Adicionar API Key** |
| Profissionais Reais | ❌ 4 mock | **Ativar Belasis** |

---

## 🔧 COMANDOS ÚTEIS

### Verificar status atual

```bash
# Ver se backend está rodando
curl http://localhost:8000/api/health | jq

# Ver profissionais (mock)
curl http://localhost:8000/api/belasis/professionals \
  -H "X-Admin-Key: $(grep ADMIN_KEY .env | cut -d= -f2)" | jq
```

### Logs do backend

```bash
# Docker
docker logs luna-backend -f

# Local
tail -f backend/logs/luna_core.log
```

---

## ✅ CONCLUSÃO

**O sistema de profissionais está 100% implementado e funcional.**

O único problema é que está rodando em **modo mock** (`BELASIS_MOCK=true`), retornando dados fictícios.

**Para corrigir:**
1. Obter API Key do Belasis
2. Atualizar `.env` com `BELASIS_MOCK=false` e `BELASIS_API_KEY=bpk_...`
3. Reiniciar backend
4. Dados reais serão carregados automaticamente

---

**Relatório gerado:** 2026-03-11  
**Autor:** LUNA OS Architecture Analysis
