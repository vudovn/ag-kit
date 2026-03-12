# 🔄 GUIA DE SINCRONIZAÇÃO - PASSO A PASSO

**Data:** 2026-03-01  
**Tempo Estimado:** 20 minutos  
**Status:** ⏳ **PRONTO PARA EXECUTAR**

---

## 📋 VISÃO GERAL

### O Que Será Sincronizado:

```
OBSIDIAN (980 arquivos)
    ↓
    ↓ (Seed SQL)
    ↓
SUPABASE (64 registros)
    ↓
    ↓ (APIs REST)
    ↓
PAINEL (7 páginas)
```

### Resultado Final:
- ✅ 9 Profissionais sincronizados
- ✅ 41 Serviços sincronizados
- ✅ 4 Pacotes sincronizados
- ✅ 4 FAQs sincronizados
- ✅ 1 Business Info sincronizado

---

## 🎯 PRÉ-REQUISITOS

### Antes de Começar:
- [x] Obsidian com 980 arquivos ✅
- [x] Seed SQL criado ✅
- [x] APIs criadas ✅
- [x] Painel criado ✅
- [ ] Supabase com dados ⏳
- [ ] Backend rodando ⏳
- [ ] Frontend rodando ⏳

---

## 📝 PASSO 1: EXECUTAR SEED SQL (10 min)

### 1.1 Acessar Supabase Dashboard

**URL:** https://supabase.com/dashboard

**Passos:**
1. Fazer login no Supabase
2. Selecionar projeto `sktrmwogifeuzrcnpvsw`

### 1.2 Abrir SQL Editor

**Passos:**
1. Clicar em "SQL Editor" no menu lateral
2. Clicar em "New Query"

### 1.3 Copiar Seed SQL

**Arquivo:** `backend/supabase_seed_haven.sql`

**Comando:**
```bash
# Copiar conteúdo do arquivo
cat backend/supabase_seed_haven.sql | pbcopy  # macOS
# OU
cat backend/supabase_seed_haven.sql | xclip -selection clipboard  # Linux
```

### 1.4 Executar SQL

**Passos:**
1. Colar SQL no SQL Editor
2. Clicar em "Run" ou pressionar `Ctrl+Enter` / `Cmd+Enter`
3. Aguardar execução (5-10 segundos)

### 1.5 Validar Execução

**SQL de Validação:**
```sql
-- Contar registros por categoria
SELECT 
  category,
  COUNT(*) as total
FROM knowledge_base
WHERE category IN ('services', 'professionals', 'coupons', 'packages', 'faqs', 'business')
GROUP BY category
ORDER BY category;
```

**Resultado Esperado:**
```
category       | total
---------------|-------
business       | 1
coupons        | 5
faqs           | 4
packages       | 4
professionals  | 9
services       | 41
---------------|-------
TOTAL          | 64
```

---

## 📝 PASSO 2: INICIAR BACKEND (2 min)

### 2.1 Iniciar Backend

**Comando:**
```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.2 Validar Backend

**URL:** http://localhost:8000

**Teste:**
```bash
curl http://localhost:8000/ | python3 -m json.tool
```

**Resultado Esperado:**
```json
{
  "name": "Luna Core",
  "version": "2.1.0",
  "status": "operational",
  "modules": [...]
}
```

### 2.3 Testar APIs

**Professionals:**
```bash
curl http://localhost:8000/api/professionals | python3 -m json.tool
```

**Esperado:** 9 profissionais

**Services:**
```bash
curl http://localhost:8000/api/services | python3 -m json.tool
```

**Esperado:** 41 serviços

**Packages:**
```bash
curl http://localhost:8000/api/packages | python3 -m json.tool
```

**Esperado:** 4 pacotes

---

## 📝 PASSO 3: INICIAR FRONTEND (2 min)

### 3.1 Iniciar Frontend

**Comando:**
```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/frontend
npm run dev
```

### 3.2 Validar Frontend

**URL:** http://localhost:3000

**Teste:**
```bash
curl http://localhost:3000 | head -20
```

**Resultado Esperado:** HTML da página

### 3.3 Testar Páginas

**Professionals:**
- URL: http://localhost:3000/professionals
- Esperado: 9 profissionais listados

**Services:**
- URL: http://localhost:3000/services
- Esperado: 41 serviços listados

**Packages:**
- URL: http://localhost:3000/packages
- Esperado: 4 pacotes listados

---

## 📝 PASSO 4: VALIDAR SINCRONIZAÇÃO (5 min)

### 4.1 Executar Script de Validação

**Comando:**
```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend
python3 scripts/validar_sincronizacao.py
```

### 4.2 Validar Resultado

**Esperado:**
```
📊 STATUS GERAL DE SINCRONIZAÇÃO
============================================================

📂 OBSIDIAN:
   Profissionais: 9/9
   Serviços: 41/41
   Pacotes: 4/4
   FAQs: 4/4
   Status: ✅ 100%

📄 SEED SQL:
   Arquivo: ✅ Existe
   INSERTs: 64
   Status: ✅ Pronto

🔌 APIS:
   Professionals: 9 registros
   Services: 41 registros
   Packages: 4 registros
   Status: ✅ Online

🖥️ PAINEL:
   Status: ✅ Online

📊 SINCRONIZAÇÃO: 100% (4/4)

🎉 PARABÉNS! SINCRONIZAÇÃO 100% COMPLETA!
```

---

## 📊 CHECKLIST DE SINCRONIZAÇÃO

### Pré-Sincronização:
- [x] Obsidian 100% completo
- [x] Seed SQL criado
- [x] APIs criadas
- [x] Painel criado

### Durante Sincronização:
- [ ] Seed SQL executado no Supabase
- [ ] 64 registros inseridos
- [ ] Backend iniciado
- [ ] APIs testadas
- [ ] Frontend iniciado
- [ ] Páginas testadas

### Pós-Sincronização:
- [ ] Script de validação executado
- [ ] 100% sincronização confirmada
- [ ] Validação com equipe realizada

---

## 🚨 TROUBLESHOOTING

### Problema: Seed SQL falha

**Solução:**
```sql
-- Verificar se tabela existe
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name = 'knowledge_base';
```

Se não existir, criar tabela primeiro.

### Problema: APIs não respondem

**Solução:**
```bash
# Verificar se backend está rodando
ps aux | grep uvicorn

# Verificar logs
# (No terminal onde rodou uvicorn)

# Reiniciar backend
cd backend
uvicorn app.main:app --reload
```

### Problema: Painel não carrega

**Solução:**
```bash
# Verificar se frontend está rodando
ps aux | grep next

# Verificar console do navegador (F12)

# Reiniciar frontend
cd frontend
npm run dev
```

---

## 📝 RESUMO DOS COMANDOS

### Copiar tudo de uma vez:

```bash
# 1. Copiar Seed SQL
cat backend/supabase_seed_haven.sql | pbcopy

# 2. Iniciar Backend
cd backend && uvicorn app.main:app --reload &

# 3. Iniciar Frontend
cd frontend && npm run dev &

# 4. Validar
python3 scripts/validar_sincronizacao.py
```

---

## ✅ STATUS FINAL

### Após Sincronização Completa:

| Sistema | Dados | Status |
|---------|-------|--------|
| **Obsidian** | 980 arquivos | ✅ 100% |
| **Supabase** | 64 registros | ✅ 100% |
| **APIs** | 64 registros | ✅ 100% |
| **Painel** | 64 registros | ✅ 100% |

**Sincronização:** ✅ **100% COMPLETA**

---

## 📄 ARQUIVOS ENVOLVIDOS

### Para Executar:
1. `backend/supabase_seed_haven.sql` (Seed SQL)

### Para Validar:
1. `backend/scripts/validar_sincronizacao.py` (Script de validação)
2. `backend/app/api/professionals.py` (API)
3. `backend/app/api/services.py` (API)
4. `backend/app/api/packages.py` (API)
5. `frontend/app/professionals/page.tsx` (Página)
6. `frontend/app/services/page.tsx` (Página)
7. `frontend/app/packages/page.tsx` (Página)

---

## 🎯 PRÓXIMOS PASSOS

### Após Sincronização 100%:
1. ⏳ Validar com equipe Suzana
2. ⏳ Executar testes automatizados
3. ⏳ Executar Dojo Scenarios
4. ⏳ Ativar LUNA_MODE (SOMENTE APÓS 95% APROVAÇÃO)

---

**Documento:** `LUNA_OS/GUIA_SINCRONIZACAO_PASSO_A_PASSO.md`  
**Status:** ⏳ **PRONTO PARA EXECUTAR**  
**Tempo Estimado:** 20 minutos
