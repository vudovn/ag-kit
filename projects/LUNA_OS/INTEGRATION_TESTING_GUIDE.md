# 🧪 LUNA OS - Guia de Testes de Integração

Este guia explica como testar e verificar a comunicação entre as funções da LUNA.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura de Testes](#arquitetura-de-testes)
3. [Como Rodar os Testes](#como-rodar-os-testes)
4. [Entendendo os Resultados](#entendendo-os-resultados)
5. [Cenários de Teste](#cenários-de-teste)
6. [Debug de Problemas](#debug-de-problemas)

---

## 🎯 Visão Geral

### O que são testes de integração?

Testes de integração verificam se **diferentes componentes do sistema estão se comunicando corretamente**, trocando dados como esperado.

### Por que são importantes?

- ✅ Detectam problemas de comunicação entre módulos
- ✅ Validam fluxo de dados end-to-end
- ✅ Identificam dependências quebradas
- ✅ Previnem regressões em integrações

### Componentes testados:

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO PRINCIPAL                           │
│                                                              │
│  WhatsApp → Brain → Memory → RAG → LLM → Response → Save    │
│                ↓         ↓         ↓                        │
│            Scheduler  Supabase  Milvus                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitetura de Testes

### Estrutura de arquivos:

```
backend/tests/
├── test_integration_flow.py       # Testes unitários de integração
├── test_integration_simulator.py  # Simulador visual de fluxos
├── data_flow_tracker.py           # Rastreador de fluxo de dados
└── test_*.py                      # Outros testes
```

### Camadas de teste:

| Camada | Descrição | Exemplo |
|--------|-----------|---------|
| **Unitário** | Testa uma função isolada | `test_classify_intent()` |
| **Integração** | Testa comunicação entre 2+ componentes | `test_brain_reads_client_profile()` |
| **E2E** | Testa fluxo completo | `test_full_message_flow()` |
| **Simulação** | Simula cenários reais | `run_scenario_1_agendamento_simples()` |

---

## 🚀 Como Rodar os Testes

### Pré-requisitos:

```bash
# 1. Ambiente virtual ativado
source venv/bin/activate  # ou venv\Scripts\Activate.ps1 no Windows

# 2. Dependências instaladas
pip install pytest pytest-asyncio loguru

# 3. Serviços rodando (opcional, para testes reais)
docker-compose up -d  # Supabase, Milvus, Redis, etc.
```

### Opção 1: Testes Unitários de Integração (Pytest)

```bash
# Roda todos os testes de integração
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend
pytest tests/test_integration_flow.py -v

# Roda com output detalhado
pytest tests/test_integration_flow.py -v -s

# Roda testes específicos
pytest tests/test_integration_flow.py::TestBrainMemoryIntegration -v

# Roda com coverage
pytest tests/test_integration_flow.py --cov=app --cov-report=html
```

### Opção 2: Simulador Visual (Recomendado para Debug)

```bash
# Roda todos os cenários
python tests/test_integration_simulator.py

# Roda cenário específico
python tests/test_integration_simulator.py --scenario 1  # Agendamento simples
python tests/test_integration_simulator.py --scenario 2  # Conversa completa
python tests/test_integration_simulator.py --scenario 3  # Dúvidas
python tests/test_integration_simulator.py --scenario 4  # Reclamação
```

### Opção 3: Data Flow Tracker (Avançado)

```bash
# Rastreia fluxo de dados em tempo real
python tests/data_flow_tracker.py

# Gera relatório JSON
# (Adicione no seu código:)
tracker.export_json("data_flow_report.json")
```

---

## 📊 Entendendo os Resultados

### Output do Pytest:

```
tests/test_integration_flow.py::TestEndToEndFlow::test_full_message_flow PASSED
tests/test_integration_flow.py::TestBrainMemoryIntegration::test_brain_reads_client_profile PASSED
tests/test_integration_flow.py::TestBrainSchedulerIntegration::test_scheduling_intent_detection PASSED

============= 15 passed, 0 failed in 3.42s =============
```

✅ **PASSED**: Teste passou, integração funcionando
❌ **FAILED**: Teste falhou, problema na integração
⚠️ **SKIPPED**: Teste pulado (dependência não disponível)

### Output do Simulador:

```
══════════════════════════════════════════════════════════
🚀 INICIANDO FLUXO: agendamento_simples
   Phone: +5511999888777
   Message: "Quero agendar um horário para amanhã às 14h"
══════════════════════════════════════════════════════════

📱 WhatsApp: Message received
🧠 Brain: Starting processing
💾 Memory: Client profile accessed
📅 Scheduler: Booking flow triggered
💬 Response: Generated
   text: "Claro! Qual horário você prefere..."

✅ [E2E] Response generated: Claro! Qual horário você prefere...
✅ [E2E] Intent: AGENDAR, Confidence: 0.92
✅ [E2E] Processing time: 245ms
```

### Output do Data Flow Tracker:

```
══════════════════════════════════════════════════════════
📊 DATA FLOW TRACKER - REPORT
══════════════════════════════════════════════════════════

⏱️  Duration: 2.34s
📈 Total Flows: 42
🔗 Components: 7
⚡ Flows/sec: 17.95
✅ Success Rate: 97.6%
❌ Errors: 1

──────────────────────────────────────────────────────────
🧩 COMPONENTS
──────────────────────────────────────────────────────────

BRAIN:
  Calls Made: 12
  Calls Received: 8
  Data Sent: 4521 bytes
  Data Received: 8932 bytes
  Avg Latency: 245.3ms
  Errors: 0

MEMORY:
  Calls Made: 5
  Calls Received: 10
  Data Sent: 2341 bytes
  Data Received: 5621 bytes
  Avg Latency: 12.4ms
  Errors: 0

──────────────────────────────────────────────────────────
🔗 COMMUNICATION MATRIX
──────────────────────────────────────────────────────────

  whatsapp        → brain          : 8 calls
  brain           → memory         : 10 calls
  brain           → semantic       : 5 calls
  semantic        → milvus         : 5 calls
  brain           → openrouter     : 8 calls
  brain           → scheduler      : 3 calls
```

---

## 🎭 Cenários de Teste

### Cenário 1: Agendamento Simples

**Objetivo:** Verificar fluxo básico de agendamento

**Mensagem:**
```
"Quero agendar um horário para amanhã às 14h"
```

**Fluxo esperado:**
```
WhatsApp → Brain → Memory (perfil) → Brain → Scheduler → Response
```

**O que verificar:**
- [ ] Brain detecta intent `AGENDAR`
- [ ] Memory retorna perfil do cliente
- [ ] Scheduler recebe dados estruturados
- [ ] Resposta menciona agendamento

### Cenário 2: Conversa Completa

**Objetivo:** Verificar preservação de contexto

**Mensagens:**
```
1. "Oi, bom dia!"
2. "Quero fazer unha e pé"
3. "Tem horário sábado de manhã?"
4. "Pode ser às 10h?"
5. "Com a Ana, por favor"
```

**O que verificar:**
- [ ] Histórico é mantido entre mensagens
- [ ] Contexto é usado nas respostas
- [ ] Estado da conversa é preservado
- [ ] Dados extraídos são acumulados

### Cenário 3: Dúvidas e Informações

**Objetivo:** Verificar uso de Knowledge Base

**Mensagens:**
```
1. "Qual o preço da manicure?"
2. "E pedicure?"
3. "Tem pacote combinado?"
4. "Como funciona o serviço de gel?"
```

**O que verificar:**
- [ ] Brain consulta base de conhecimento
- [ ] RAG retorna contexto relevante
- [ ] Respostas são precisas
- [ ] Intent `INFO` ou `PRECO` detectada

### Cenário 4: Reclamação

**Objetivo:** Verificar fluxo de crise

**Mensagens:**
```
1. "Preciso falar com um responsável"
2. "Meu agendamento foi cancelado sem aviso"
3. "Isso é um absurdo!"
```

**O que verificar:**
- [ ] Intent `RECLAMACAO` detectada
- [ ] Sentimento negativo identificado
- [ ] Urgência crítica marcada
- [ ] Handoff para humano acionado

---

## 🐛 Debug de Problemas

### Problema: Teste falha com "Connection Error"

**Causa:** Serviços externos offline (Supabase, Milvus, etc.)

**Solução:**
```bash
# Verifica status dos containers
docker-compose ps

# Reinicia serviços
docker-compose restart supabase-db luna-milvus redis

# Ou usa mocks
pytest tests/test_integration_flow.py -k "mock"
```

### Problema: "Import Error" ou "Module Not Found"

**Causa:** Dependências não instaladas ou caminho errado

**Solução:**
```bash
# Reinstala dependências
pip install -r requirements.txt

# Verifica PYTHONPATH
export PYTHONPATH=/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend:$PYTHONPATH
```

### Problema: Dados não persistem entre testes

**Causa:** Testes usando banco de dados diferente ou limpando estado

**Solução:**
```python
# Usa fixtures compartilhadas
@pytest.fixture(scope="session")
def shared_db():
    # Setup uma vez para todos os testes
    ...

# Ou desabilita cleanup
os.environ['TEST_CLEANUP'] = 'false'
```

### Problema: Latência muito alta nos testes

**Causa:** Chamadas reais para LLMs externas

**Solução:**
```python
# Usa mocks para LLMs
with patch('app.integrations.openrouter.complete', return_value="Mock response"):
    result = await brain.process_message(phone, message)
```

---

## 📈 Métricas de Qualidade

### O que monitorar:

| Métrica | Ideal | Aceitável | Crítico |
|---------|-------|-----------|---------|
| Success Rate | >99% | >95% | <90% |
| Avg Latency | <500ms | <1000ms | >2000ms |
| Data Integrity | 100% | >99% | <95% |
| Coverage | >80% | >70% | <60% |

### Como melhorar:

1. **Reduzir latência:**
   - Usar cache (Redis)
   - Otimizar queries
   - Parallelizar chamadas

2. **Aumentar confiabilidade:**
   - Adicionar retries
   - Implementar circuit breakers
   - Usar fallbacks

3. **Melhorar cobertura:**
   - Adicionar testes para edge cases
   - Testar cenários de erro
   - Cobrir integrações críticas

---

## 📚 Recursos Adicionais

### Arquivos relacionados:

- [`test_integration_flow.py`](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/tests/test_integration_flow.py) - Testes unitários
- [`test_integration_simulator.py`](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/tests/test_integration_simulator.py) - Simulador visual
- [`data_flow_tracker.py`](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/tests/data_flow_tracker.py) - Rastreador de dados
- [`test_brain.py`](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/tests/test_brain.py) - Testes do Brain
- [`test_memory.py`](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/tests/test_memory.py) - Testes do Memory

### Documentação:

- [LUNA_OS_ARCHITECTURE_DIAGRAMS.md](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/LUNA_OS_ARCHITECTURE_DIAGRAMS.md) - Arquitetura completa
- [NEURAL_GATEWAY_DIAGNOSTIC_20260311.md](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/NEURAL_GATEWAY_DIAGNOSTIC_20260311.md) - Diagnóstico do sistema

---

## 🎯 Próximos Passos

1. **Rodar testes agora:**
   ```bash
   cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend
   python tests/test_integration_simulator.py --scenario 1
   ```

2. **Verificar saúde das integrações:**
   ```bash
   pytest tests/test_integration_flow.py::test_integration_health -v
   ```

3. **Gerar relatório completo:**
   ```bash
   pytest tests/test_integration_flow.py --tb=short -v > integration_report.txt
   ```

4. **Identificar gaps:**
   - Quais integrações não estão testadas?
   - Quais cenários faltam?
   - Quais métricas estão abaixo do ideal?

---

*Última atualização: 2026-03-11*
*LUNA OS v3.0*
