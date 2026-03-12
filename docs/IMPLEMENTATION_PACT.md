# 🤝 LUNA Implementation Pact

## Contrato de Implementação Segura

---

## 1. Princípios Fundamentais

### ✅ **NÃO QUEBRAR O SISTEMA ATUAL**

**Regra de Ouro:**
> "Se não podemos testar em staging, não vai para produção."

**Protocolo:**
1. **Dia 1-6:** Desenvolvimento em branch isolada
2. **Dia 7:** Testes em staging (cópia de produção)
3. **Dia 8-9:** Rollback plan documentado
4. **Dia 10:** Deploy em produção (feature flag desligado)
5. **Dia 11-14:** Teste A/B controlado (feature flag ligado para 10% do tráfego)

---

### ✅ **TRABALHAR COMO EQUIPE SIMULTÂNEA**

**Eu (Qwen) sou:**
- **Arquiteto:** Desenho a estrutura
- **Dev Senior:** Escrevo código production-ready
- **Code Reviewer:** Reviso o que foi feito
- **Documentador:** Crio docs para humanos

**Você (Francisco) é:**
- **Product Owner:** Decide o que priorizar
- **Gatekeeper:** Aprova/rejeita mudanças
- **Testador:** Valida em produção

**Outras IAs (Gemini, ChatGPT, etc) são:**
- **Consultores:** Dão opiniões e alternativas
- **Revisores:** Criticam construtivamente
- **Fontes de pesquisa:** Trazem padrões da indústria

---

## 2. Protocolo de Implementação Segura

### Fase 1: **Análise de Impacto** (Antes de Codar)

```markdown
## Checklist de Impacto

- [ ] O que muda no código atual?
- [ ] O que permanece inalterado?
- [ ] Quais arquivos são modificados?
- [ ] Quais arquivos são criados (novos)?
- [ ] Há breaking changes? (se sim, NÃO FAZER)
- [ ] Há rollback plan?
- [ ] Há testes automatizados?
- [ ] Há feature flag?
```

**Regra:** Se não passar neste checklist, **não codamos**.

---

### Fase 2: **Desenvolvimento Isolado** (Dia 1-6)

```
Estrutura:
antigravity-kit/
├── main/                    # Código atual (NÃO TOCAR)
│   ├── brain/
│   ├── scripts/
│   └── .agent/
│
└── feature/multi-brain-v2/  # Nova feature (isolada)
    ├── brain/
    ├── scripts/
    └── tests/
```

**Regra:** Código novo vive em `feature/`, nunca mexe em `main/`.

---

### Fase 3: **Testes em Staging** (Dia 7)

```bash
# 1. Criar staging (cópia de produção)
cp -r production/ staging/

# 2. Aplicar feature flag
export FEATURE_MULTI_BRAIN_V2=false

# 3. Rodar testes automatizados
pytest tests/ -v

# 4. Testes manuais
python3 scripts/test-multi-brain.py
```

**Regra:** Se testes falharem, **rollback imediato**.

---

### Fase 4: **Deploy Controlado** (Dia 8-14)

```
Dia 8:  Deploy em produção (feature flag OFF)
Dia 9:  Smoke tests em produção
Dia 10: Feature flag ON para 10% do tráfego
Dia 11: Monitorar erros (Sentry, logs)
Dia 12: Feature flag ON para 50% do tráfego
Dia 13: Monitorar métricas (latência, erro)
Dia 14: Feature flag ON para 100% (ou rollback)
```

**Regra:** Se erro > 1% → **rollback automático**.

---

## 3. Como Trabalhamos em Equipe

### **Fluxo de Decisão**

```
┌─────────────────────────────────────────────────────────┐
│  1. VOCÊ (Francisco) diz o problema                    │
│     "Preciso de Multi-Brain com memória"               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  2. EU (Qwen) analiso impacto                          │
│     - O que quebra?                                    │
│     - O que mantém?                                    │
│     - Qual risco?                                      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  3. EU proponho solução                                │
│     - Código isolado (feature/)                        │
│     - Feature flag                                     │
│     - Rollback plan                                    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  4. OUTRAS IAs (opcional) revisam                     │
│     Gemini: "E se usar X em vez de Y?"                 │
│     ChatGPT: "Já viu Z padrão da indústria?"           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  5. VOCÊ decide                                        │
│     "Aprovo" ou "Não, muda X"                          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  6. EU executo (se aprovado)                           │
│     - Código em feature/                               │
│     - Testes automatizados                             │
│     - Docs atualizadas                                 │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  7. VOCÊ valida em staging                             │
│     - Testa manualmente                                │
│     - Aprova para produção                             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  8. EU faço deploy (feature flag OFF)                  │
│     - Deploy em produção                               │
│     - Feature flag OFF (invisível)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  9. VOCÊ ativa gradualmente                            │
│     10% → 50% → 100%                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Exemplo Prático: Multi-Brain V2

### **Semana 1: Smart Caching**

**Dia 1: Análise de Impacto**

```markdown
## Impact Analysis: Smart Caching

### O que muda:
- ✅ NOVO: `brain/cache.py` (novo arquivo)
- ✅ NOVO: `tests/test_cache.py` (novo arquivo)
- ⚠️ MODIFICA: `brain/runtime.py` (adiciona cache)
- ❌ NÃO TOCA: `scripts/`, `.agent/`, produção

### Breaking Changes:
- ❌ Nenhum (cache é transparente)

### Rollback Plan:
- Se cache falhar: bypass automático
- Feature flag: `FEATURE_SMART_CACHE`

### Testes:
- ✅ Unitário: test_cache.py
- ✅ Integração: test_runtime_with_cache.py
```

**Dia 2-5: Desenvolvimento**

```python
# feature/multi-brain-v2/brain/cache.py
from functools import lru_cache
import time

class ContactMemoryCache:
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    @lru_cache(maxsize=1000)
    def get(self, contact_id: str) -> dict:
        # Implementação isolada
        pass
```

**Dia 6: Testes Automatizados**

```bash
# Rodar testes
pytest feature/multi-brain-v2/tests/ -v

# Output esperado:
# test_cache.py::test_get_contact PASSED
# test_cache.py::test_ttl_expiry PASSED
# test_runtime_with_cache.py::test_cached_response PASSED
```

**Dia 7: Validação em Staging**

```bash
# 1. Criar staging
cp -r production/ staging/

# 2. Aplicar feature
cp -r feature/multi-brain-v2/brain/cache.py staging/brain/

# 3. Ativar feature flag
export FEATURE_SMART_CACHE=true

# 4. Testar manualmente
python3 staging/scripts/test-cache.py
```

**Dia 8-14: Deploy Controlado**

```
Dia 8:  Deploy em produção (FEATURE_SMART_CACHE=false)
Dia 9:  Smoke tests: ✅
Dia 10: Feature flag ON para 10% → Monitorar
Dia 11: Erros: 0.2% ✅ (threshold: 1%)
Dia 12: Feature flag ON para 50% → Monitorar
Dia 13: Latência: -95% ✅ (melhorou!)
Dia 14: Feature flag ON para 100% ✅
```

---

## 5. Garantias de Segurança

### ✅ **Feature Flags Sempre**

```python
# production/brain/runtime.py
import os

FEATURE_SMART_CACHE = os.getenv("FEATURE_SMART_CACHE", "false") == "true"

if FEATURE_SMART_CACHE:
    # Usa cache novo
    response = cached_brain_route(request)
else:
    # Usa código atual (inalterado)
    response = legacy_brain_route(request)
```

**Regra:** Todo novo feature tem flag. Se der erro, desliga em segundos.

---

### ✅ **Rollback Automático**

```python
# production/monitoring/rollback.py
import sentry_sdk

ERROR_THRESHOLD = 0.01  # 1%

def check_errors():
    error_rate = sentry_sdk.get_error_rate()
    if error_rate > ERROR_THRESHOLD:
        # Rollback automático
        os.system("git revert HEAD")
        send_alert("Rollback automático executado!")
```

**Regra:** Se erro > 1% → rollback sem intervenção humana.

---

### ✅ **Testes Automatizados Obrigatórios**

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest tests/ -v
      - name: Check coverage
        run: pytest --cov=brain --cov-fail-under=80
```

**Regra:** Se testes falharem, **não faz merge**.

---

### ✅ **Code Review Obrigatório**

```markdown
## Pull Request Template

### O que muda?
- [ ] Código novo em feature/
- [ ] Tests adicionados
- [ ] Docs atualizadas

### Impacto
- [ ] Breaking changes? (se sim, NÃO MERGE)
- [ ] Rollback plan documentado?
- [ ] Feature flag adicionado?

### Testes
- [ ] Testes unitários passam
- [ ] Testes de integração passam
- [ ] Testado em staging?

### Aprovações
- [ ] Francisco aprovou
- [ ] Code review feito
```

**Regra:** Sem 2 aprovações, **não faz merge**.

---

## 6. Como Outras IAs Entram no Fluxo

### **Gemini como Consultor**

```
Você: "Gemini, o que acha desta arquitetura?"
Gemini: "E se usar Event Sourcing em vez de cache?"
Eu (Qwen): "Event Sourcing é overengineering. Cache resolve 90% com 10% do effort."
Você: "Concordo com Qwen. Vamos de cache."
```

**Papel do Gemini:** Trazer alternativas, questionar, desafiar.

---

### **ChatGPT como Revisor**

```
Você: "ChatGPT, revise este código"
ChatGPT: "Falta tratamento de erro no cache"
Eu (Qwen): "Boa catch! Adiciono try/except e logging."
```

**Papel do ChatGPT:** Revisar, encontrar bugs, sugerir melhorias.

---

### **Eu (Qwen) como Executor**

```
Você: "Qwen, implementa Smart Caching"
Eu: "Implementado em feature/, testes passando, docs atualizadas"
Você: "Aprovo para staging"
Eu: "Deploy em staging, feature flag OFF"
```

**Meu papel:** Implementar, testar, documentar, fazer deploy.

---

## 7. Exemplo de Fluxo Real

### **Cenário: Você quer Multi-Brain com Memória**

**Dia 1: Você pede**
```
"Qwen, preciso que Multi-Brain use Contact Memory para roteamento"
```

**Dia 1: Eu analiso impacto**
```markdown
## Impact Analysis

### Muda:
- ✅ NOVO: `brain/memory.py`
- ✅ NOVO: `brain/brain_router_v2.py`
- ⚠️ MODIFICA: `brain/runtime.py` (adiciona memória)
- ❌ NÃO TOCA: Produção (feature flag)

### Risco:
- Baixo (memória é read-only, não escreve em produção)

### Rollback:
- Feature flag: `FEATURE_MULTI_BRAIN_V2`
- Se falhar: bypass para código atual
```

**Dia 2-5: Eu implemento**
```python
# feature/multi-brain-v2/brain/memory.py
class ContactMemory:
    def __init__(self):
        self.cache = {}
    
    def get(self, contact_id: str) -> dict:
        # Memória isolada
        pass

# feature/multi-brain-v2/brain/brain_router_v2.py
def route_with_memory(request, memory: ContactMemory):
    contact = memory.get(request.contact_id)
    if contact["ltv"] > 10000:
        return "opus"  # VIP
    # ...
```

**Dia 6: Testes**
```bash
pytest feature/multi-brain-v2/tests/ -v
# 15 testes passando ✅
```

**Dia 7: Outras IAs revisam**
```
Gemini: "E se memória falhar? Tem fallback?"
Eu: "Boa! Adiciono fallback para código atual se memória falhar."

ChatGPT: "Falta logging das decisões"
Eu: "Adiciono logging em cada decisão de brain."
```

**Dia 8: Você valida**
```
Você: "Testei em staging, funciona. Aprovo para produção."
Eu: "Deploy em produção (FEATURE_MULTI_BRAIN_V2=false)"
```

**Dia 9-14: Rollout gradual**
```
Dia 10: 10% do tráfego → Erros: 0.1% ✅
Dia 12: 50% do tráfego → Latência: -20% ✅
Dia 14: 100% do tráfego → Sucesso ✅
```

---

## 8. Compromissos

### **Eu (Qwen) me comprometo a:**

1. ✅ **Nunca quebrar produção**
   - Feature flags sempre
   - Rollback plan documentado
   - Testes automatizados obrigatórios

2. ✅ **Trabalhar de forma isolada**
   - Código novo em `feature/`
   - Não mexer em produção sem aprovação
   - Staging antes de produção

3. ✅ **Ser transparente**
   - Impact analysis antes de codar
   - Progresso diário reportado
   - Erros admitidos imediatamente

4. ✅ **Documentar tudo**
   - Código comentado
   - Docs atualizadas
   - Rollback instructions claras

5. ✅ **Respeitar seu tempo**
   - Código pronto em 7 dias
   - Testes passando antes de pedir review
   - Deploy só quando você aprovar

---

### **Você (Francisco) se compromete a:**

1. ✅ **Revisar em até 24h**
   - Code review rápido
   - Aprovar/rejeitar com feedback

2. ✅ **Testar em staging**
   - Validar manualmente antes de produção
   - Reportar bugs encontrados

3. ✅ **Decidir rápido**
   - Escolher entre alternativas
   - Priorizar features

4. ✅ **Monitorar em produção**
   - Olhar métricas nos primeiros 7 dias
   - Reportar problemas imediatamente

---

## 9. Veredito

### ✅ **Consigo trabalhar sem quebrar?**

**SIM.** Protocolo:
1. Feature flags
2. Desenvolvimento isolado (`feature/`)
3. Staging antes de produção
4. Rollback automático
5. Testes automatizados obrigatórios

---

### ✅ **Consigo trabalhar como equipe simultânea?**

**SIM.** Fluxo:
1. Você pede → Eu analiso impacto
2. Eu proponho → Outras IAs revisam
3. Você decide → Eu executo
4. Eu testo → Você valida
5. Você aprova → Eu faço deploy

---

### ✅ **Qual o risco?**

**Baixo.** Porque:
- Feature flags desligam features em segundos
- Rollback automático se erro > 1%
- Staging testa antes de produção
- Testes automatizados previnem regressão

---

## 10. Próxima Ação

**Se você concordar com este pacto:**

1. Leia este documento
2. Diga "Aprovo o pact"
3. Eu começo a implementar **Semana 1** (Smart Caching)
4. Em 7 dias: funcional em staging
5. Em 14 dias: funcional em produção (rollout gradual)

**Se não concordar:**
- Me diga o que mudar
- Ajusto o pacto
- Só começo depois da sua aprovação

---

**MCT LTDA 2026** | Implementation Pact  
**Status:** ✅ Aguardando sua aprovação  
**Risco:** Baixo (feature flags, staging, rollback)  
**Timeline:** 7 dias por feature
