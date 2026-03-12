# 🚀 LUNA OS EVOLUTION - GUIA DE IMPLANTAÇÃO

**Data:** 2026-03-01  
**Status:** ✅ **CÓDIGO IMPLEMENTADO**  
**Próximo Passo:** Executar migration e testar

---

## 📋 CHECKLIST DE IMPLANTAÇÃO

### ✅ COMPLETADO (Código)

- [x] 11 arquivos Python criados
- [x] 1 página Frontend criada
- [x] Migration SQL criado
- [x] Endpoints registrados no main.py
- [x] Task Runner integrado ao lifespan
- [x] Documentação completa

### ⏳ PENDENTE (Execução)

- [ ] Executar migration no Supabase
- [ ] Reiniciar backend Docker
- [ ] Testar endpoints
- [ ] Validar frontend

---

## 1️⃣ EXECUTAR MIGRATION NO SUPABASE

### Opção A: Via Dashboard (Recomendado)

1. Acesse https://supabase.com
2. Selecione seu projeto `sktrmwogifeuzrcnpvsw`
3. Vá para **SQL Editor**
4. Clique em **New Query**
5. Copie e cole o conteúdo de:
   ```
   backend/supabase_evolution_migration.sql
   ```
6. Clique em **Run**
7. Verifique se apareceu: `✅ Migration completed successfully! 4 tables created.`

### Opção B: Via CLI (Alternativo)

```bash
# Instalar Supabase CLI se não tiver
npm install -g supabase

# Login
supabase login

# Link do projeto
supabase link --project-ref sktrmwogifeuzrcnpvsw

# Executar migration
supabase db push --db-remote
```

### Verificar Tabelas Criadas

Após executar, verifique no **Table Editor** se as tabelas foram criadas:
- `prompt_proposals`
- `conversation_intelligence`
- `dojo_edge_cases`
- `health_checks`

---

## 2️⃣ REINICIAR BACKEND

### Se estiver usando Docker Compose:

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS

# Parar backend
docker compose stop luna-backend

# Remover container antigo
docker compose rm -f luna-backend

# Iniciar novo container (com novo código)
docker compose up -d luna-backend

# Ver logs
docker compose logs -f luna-backend
```

### Se estiver rodando localmente:

```bash
# Parar processo atual (Ctrl+C)

# Reiniciar
cd backend
source venv/bin/activate  # Se tiver virtualenv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar se Iniciou Corretamente:

Nos logs, procure por:
```
✅ Task Runner scheduler started
✅ Luna Core ready on port 8000
```

---

## 3️⃣ TESTAR ENDPOINTS

### Teste 1: Health Check

```bash
curl http://localhost:8000/health
```

**Esperado:**
```json
{
  "status": "healthy",
  "integrations": {
    "supabase": "connected",
    "evolution_api": "connected"
  }
}
```

### Teste 2: Dojo Proposals

```bash
curl http://localhost:8000/api/dojo/proposals
```

**Esperado:**
```json
{
  "success": true,
  "count": 0,
  "proposals": []
}
```

### Teste 3: Edge Cases

```bash
curl http://localhost:8000/api/dojo/edge-cases
```

**Esperado:**
```json
{
  "success": true,
  "count": 0,
  "edge_cases": []
}
```

### Teste 4: Intelligence Insights

```bash
curl "http://localhost:8000/api/intelligence/insights?days=7"
```

**Esperado:**
```json
{
  "success": true,
  "period_days": 7,
  "total_analyses": 0,
  "insights": []
}
```

### Teste 5: Root (Verificar Módulos)

```bash
curl http://localhost:8000/
```

**Esperado:**
```json
{
  "modules": [
    "brain",
    "memory",
    "analytics",
    "campaigns",
    "knowledge",
    "evolution",
    "evolution_proxy",
    "dojo",
    "dojo_simulator",
    "dojo_learning",      ← NOVO
    "conversation_intelligence",  ← NOVO
    "task_runner"  ← NOVO
  ]
}
```

---

## 4️⃣ TESTAR FRONTEND

### Acessar Página

```
http://localhost:3000/intelligence
```

### Verificar 3 Abas

**Aba 1: Dojo Proposals**
- Deve mostrar "No pending proposals!" se vazio
- Ou lista de propostas se existirem

**Aba 2: Client Intelligence**
- Campo de busca por telefone
- Ao buscar, mostra perfil completo

**Aba 3: Edge Cases**
- Deve mostrar "No edge cases!" se vazio
- Ou lista de edge cases se existirem

---

## 5️⃣ TESTAR PIPELINE MANUALMENTE

### Criar Conversa Teste

1. Envie mensagem no WhatsApp da Haven
2. Aguarde resposta da LUNA
3. Encerre conversa (handoff ou timeout)

### Verificar Processamento

Após 1 hora (ou quando Task Runner rodar):

```bash
# Buscar conversa processada
curl "http://localhost:8000/api/intelligence/{conversation_id}"
```

**Esperado:**
```json
{
  "success": true,
  "conversation": {...},
  "intelligence": {
    "emotional_state": "happy",
    "trust_level": "new",
    "services_mentioned": ["escova"],
    ...
  }
}
```

---

## 6️⃣ TESTAR LEARNING CYCLE MANUALMENTE

### Criar Feedback Teste

1. Acesse http://localhost:3000/dojo
2. Execute um cenário
3. Dê rating ≤ 3 (ex: 2 estrelas)
4. Adicione comentário

### Executar Learning Cycle

```bash
curl -X POST "http://localhost:8000/api/dojo/learning/run?week_reference=2026-W09"
```

**Esperado:**
```json
{
  "success": true,
  "week_reference": "2026-W09",
  "feedbacks_analyzed": 1,
  "proposals_generated": 0  # Ou 1 se tiver >2 falhas
}
```

### Verificar Propostas

```bash
curl http://localhost:8000/api/dojo/proposals
```

---

## 🐛 TROUBLESHOOTING

### Backend não inicia

**Sintoma:** Erro no log sobre imports

**Solução:**
```bash
# Verificar se arquivos existem
ls -la backend/app/dojo/learning_cycle.py
ls -la backend/app/modules_v3/conversation_intelligence/pipeline.py
ls -la backend/app/core/task_runner.py

# Se faltando, reinstalar
docker compose build --no-cache luna-backend
docker compose up -d luna-backend
```

### Tabelas não aparecem

**Sintoma:** Erro "relation does not exist"

**Solução:**
1. Verificar se migration rodou
2. Rodar migration manualmente no SQL Editor
3. Verificar schema público

### Frontend não carrega

**Sintoma:** Página em branco ou erro 404

**Solução:**
```bash
# Rebuild frontend
cd frontend
docker compose build luna-frontend
docker compose up -d luna-frontend

# Ou localmente
npm run dev
```

### Task Runner não roda

**Sintoma:** Logs não mostram "Task Runner scheduler started"

**Solução:**
1. Verificar se import está no main.py
2. Reiniciar backend
3. Checar logs: `docker compose logs luna-backend | grep task`

---

## 📊 MONITORAMENTO

### Logs em Tempo Real

```bash
# Backend
docker compose logs -f luna-backend

# Filtrar Task Runner
docker compose logs -f luna-backend | grep "Task"

# Filtrar Intelligence
docker compose logs -f luna-backend | grep "Intelligence"
```

### Health Checks

A cada 30 minutos, Task Runner registra em `health_checks`:

```bash
curl http://localhost:8000/api/health/status
```

### Propostas Pendentes

```bash
curl http://localhost:8000/api/dojo/proposals?status=pending
```

---

## ✅ CRITÉRIOS DE SUCESSO

Sistema está funcionando corretamente quando:

- [ ] Migration rodou sem erros
- [ ] Backend iniciou com Task Runner
- [ ] Endpoints retornam 200
- [ ] Frontend carrega 3 abas
- [ ] Conversa encerrada gera intelligence em ≤1h
- [ ] Perfil do cliente atualizado no Supabase
- [ ] Arquivo Obsidian atualizado
- [ ] Learning cycle gera propostas às segundas 07:00

---

## 📞 SUPORTE

Se encontrar erros:

1. Verifique logs: `docker compose logs luna-backend`
2. Teste endpoints manualmente com curl
3. Verifique tabelas no Supabase
4. Consulte documentação: `EVOLUTION_IMPLEMENTATION_COMPLETE.md`

---

**Próxima Revisão:** 2026-03-08 (7 dias)  
**Responsável:** Dev Team
