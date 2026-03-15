# ✅ COMECE AQUI — Validação UNALUX Hoje

**Tempo total: 15 minutos**

---

## 🎯 Objetivo Hoje

Validar que sua infraestrutura (Windmill + Supabase + Redis + API) funciona e que **não há double-booking** quando dois clientes tentam agendar o mesmo horário.

---

## 🚀 Passo 1: Preparar Ambiente (2 min)

```bash
# Navegar para o projeto
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/projects/LUNA_OS

# Instalar dependências
pip install -r tests/requirements.txt

# Criar arquivo .env local (se não existir)
cat > .env.test << EOF
# Windmill
WINDMILL_URL=http://localhost:8000
WINDMILL_TOKEN=seu_token_windmill

# Supabase
DATABASE_URL=postgresql://postgres:password@localhost:5432/postgres
SUPABASE_URL=https://sktrmwogifeuzrcnpvsw.supabase.co
SUPABASE_KEY=seu_key_supabase
REDIS_URL=redis://localhost:6379

# API
API_URL=http://localhost:8000
ADMIN_KEY=seu_admin_key
EOF

# Carregar variáveis
source .env.test
```

---

## ⚡ Passo 2: Health Check (5 min)

```bash
# Tornar script executável
chmod +x tests/phase1_infrastructure/health_check.sh

# Rodar health check
bash tests/phase1_infrastructure/health_check.sh
```

**Esperado:**
```
✅ Windmill: OK
✅ Supabase: OK
✅ Redis: OK
✅ Validation API: OK

✅ INFRAESTRUTURA VALIDADA
```

**Se algo falha:** Veja troubleshooting em `tests/README.md`

---

## 🔀 Passo 3: Teste de Concorrência (5 min)

```bash
# Rodar teste de concorrência
python tests/phase1_infrastructure/test_double_booking.py
```

**Esperado:**
```
🧪 UNALUX Concurrency Test

Executando 10 requisições simultâneas...
  [1/10] ✅ SUCCESS
  [2/10] ❌ FAILED
  [3/10] ❌ FAILED
  ...
  [10/10] ❌ FAILED

✅ Sucessos: 1/10
❌ Falhas: 9/10

✅ PASS: Concorrência Controlada
   Apenas 1 de 10 conseguiu agendar.
   Double-booking prevenido com sucesso!
```

**Se falha:** Significa que 2+ clientes conseguiram agendar o mesmo slot. Crítico! Não avance.

---

## ✅ Passo 4: Documentar Resultado (3 min)

```bash
# Salvar resultado
cat > validation_log.md << EOF
# Validação UNALUX — Fase 1

**Data:** $(date)
**Resultado:** ✅ PASSOU

## Health Check
- Windmill: ✅
- Supabase: ✅
- Redis: ✅
- API: ✅

## Concorrência
- Sucessos: 1/10 ✅
- Double-booking: Prevenido ✅
- Status: PASSOU

## Próximo Passo
Avançar para Fase 2 (Shadow Mode)
EOF

cat validation_log.md
```

---

## 📊 Status Depois de Rodar

| Componente | Status | Próximo Passo |
|-----------|--------|---------------|
| Infra | ✅ Validada | Usar em produção |
| Concorrência | ✅ Segura | Fase 2 |
| Windmill | ✅ Funciona | Escalar testes |
| DB | ✅ Integridade | A/B testing |

---

## 🎯 Se Tudo Passar

```bash
echo "🎉 FASE 1 COMPLETA!"
echo "Próximo: Fase 2 (Shadow Mode) — Comparar decisão do sistema vs humano"
echo "Quando: Próxima semana"
echo "O que fazer: Coletar 50 agendamentos reais de Supabase"
```

---

## 🚨 Se Algo Falhar

### Health Check Falha
```bash
# Verificar qual serviço caiu
docker ps | grep -E "windmill|postgres|redis"

# Reiniciar serviço
docker compose up -d [nome_do_serviço]

# Rodar health check novamente
bash tests/phase1_infrastructure/health_check.sh
```

### Double-Booking Detectado
```bash
# CRÍTICO! Não avance sem corrigir.
# Possíveis causas:
# 1. Falta UNIQUE constraint em (professional_id, start_time)
# 2. Falta lock no DB durante inserção
# 3. Falta CRDT para concorrência

# Verificar constraint
psql $DATABASE_URL -c "
  SELECT constraint_name
  FROM information_schema.table_constraints
  WHERE table_name='appointments' AND constraint_type='UNIQUE'
"

# Se vazio, adicionar constraint:
psql $DATABASE_URL -c "
  ALTER TABLE appointments
  ADD CONSTRAINT unique_professional_time
  UNIQUE(professional_id, start_time)
"

# Rodar teste novamente
python tests/phase1_infrastructure/test_double_booking.py
```

---

## 📞 Precisa de Ajuda?

1. **Leia:** `tests/README.md` (troubleshooting completo)
2. **Veja:** `VALIDATION_FRAMEWORK.md` (arquitetura inteira)
3. **Execute:** `tests/phase1_infrastructure/health_check.sh` (diagnóstico)

---

## ⏱️ Timeline Recomendado

- **Hoje (Dia 1):** ✅ Fase 1 — Health Check + Concorrência
- **Semana 1:** Fase 2 — Shadow Mode (comparar com humano)
- **Semana 2:** Fase 3 — A/B Test (memória aumenta conversão?)
- **Semana 3:** Fase 4 — Load Test (Windmill aguenta carga?)

---

**Pronto? Comece:**

```bash
bash tests/phase1_infrastructure/health_check.sh
```

Se passar, rode:

```bash
python tests/phase1_infrastructure/test_double_booking.py
```

Se ambos passarem, você tem luz verde para Fase 2! 🟢

---

**Última atualização:** 2025-03-14
**Status:** Pronto para usar
