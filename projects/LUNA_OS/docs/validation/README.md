# ✅ Validation Framework — Testes Estruturados

Framework de validação em 4 semanas para garantir qualidade e confiabilidade do sistema.

## Documentos

- **`VALIDATION_START_HERE.md`** — ⭐ Guia rápido de iniciação
  - Como rodar os testes
  - O que cada teste valida

- **`CHECKPOINT_PHASE1.md`** — Status ATUAL (15 Março 2026)
  - ✅ 3/4 testes críticos passando
  - Backend: ✅ Saudável
  - Redis: ✅ OK (<10ms)
  - Windmill: ✅ Respondendo
  - Validation API: 🟡 Auth pendente (10 min fix)

- **`validation_phase1_report.md`** — Relatório detalhado de Phase 1
  - Métricas coletadas
  - Latências medidas
  - Bloqueadores identificados
  - Próximos passos

- **`VALIDATION_FRAMEWORK.md`** — Especificações completas das 4 fases
  - Phase 1 (Week 1): Infrastructure validation
  - Phase 2 (Week 2): Shadow mode comparison
  - Phase 3 (Week 3): A/B testing
  - Phase 4 (Week 4): Load testing

- **`VALIDATION_COMPLETE_GUIDE.md`** — Guia completo com exemplos e código

## Checklist de Execução

### Phase 1 (Infraestrutura) — CURRENT
- [x] Redis PING test ✅
- [x] Redis SET/GET test ✅
- [x] Windmill health check ✅
- [x] Backend health check ✅
- [ ] Validation API auth fix (10 min)

### Phase 2 (Shadow Mode) — Próxima
- [ ] Coletar 50 agendamentos históricos
- [ ] Comparar decisão sistema vs humano
- [ ] Target: 70%+ concordância

### Phase 3 (A/B Testing) — Semana 3
- [ ] Validar impacto de memória na conversão
- [ ] Medir engagement improvement
- [ ] Statistical significance

### Phase 4 (Load Testing) — Semana 4
- [ ] Windmill 1000 jobs/day
- [ ] Peak load handling
- [ ] Performance benchmarks

## Como Rodar os Testes

```bash
# Phase 1 - Infrastructure health check
bash tests/phase1_infrastructure/health_check_fixed.sh

# Phase 1 - Double booking test (concorrência)
python tests/phase1_infrastructure/test_double_booking.py
```

## Status

| Teste | Status | Latência | Evidência |
|-------|--------|----------|-----------|
| Backend /health | ✅ | ~1s | HTTP 200 |
| Redis PING | ✅ | <5ms | PONG |
| Redis SET/GET | ✅ | <10ms | OK |
| Windmill | ✅ | N/A | Responde |
| Validation API | 🟡 | ~50ms | 401 (auth) |

## Métricas de Sucesso

- Phase 1: 4/4 testes ✅
- Phase 2: 70%+ concordância
- Phase 3: Conversão +15% com memória
- Phase 4: 1000 jobs/day sem falhas

## Próximos Passos

1. Corrigir Validation API auth (10 min) → 4/4 tests
2. Iniciar Phase 2 com dados reais
3. Coletar comparativas sistema vs humano
