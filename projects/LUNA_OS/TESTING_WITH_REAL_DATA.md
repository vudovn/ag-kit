# 🧪 Testes com Dados Reais - Guia Completo

**Data:** 2026-03-11  
**Status:** ✅ **PRONTO PARA USAR**

---

## 🎯 Por Que Usar Dados Reais?

```
✅ Cenários realistas (não inventados)
✅ Volume real de conversas
✅ Intenções e sentimentos verdadeiros
✅ Validação de automações em produção
```

---

## 📊 O Que Podemos Testar

### 1. **Classificação de Intenções**
```python
# Extrair conversas reais do Supabase
# Rodar classificação do Brain
# Comparar com resultado esperado

Exemplo:
Conversa: "Quero agendar um horário"
Esperado: intent=agendamento, confidence>0.8
Resultado: ✅ PASS ou ❌ FAIL
```

### 2. **Detecção de Sentimento**
```python
# Analisar mensagens de clientes
# Detectar: happy, neutral, angry, sad
# Validar se detecção está correta

Exemplo:
Conversa: "Isso é um absurdo! Estou esperando há 30min"
Esperado: sentiment=angry, confidence>0.9
Resultado: ✅ PASS
```

### 3. **Automações Triggeradas**
```python
# Simular conversas
# Verificar quais automações são acionadas
# Validar se são as corretas

Exemplo:
Conversa de reclamação → Handoff humano ✅
Conversa de orçamento → Upsell detection ✅
```

---

## 🚀 Como Rodar Testes com Dados Reais

### Opção 1: **Simulação (Sem Conexão)**

```bash
# Roda cenários pré-definidos (baseados em conversas reais)
cd backend
python tests/simulate_tests.py --scenario=all
```

**Cenários Incluídos:**
- ✅ Agendamento simples
- ✅ Reclamação de atraso
- ✅ Orçamento de serviço
- ✅ Pós-venda
- ✅ Cliente inativo

**Saída:**
```
╔══════════════════════════════════════════════════════════╗
║     LUNA OS - Simulation Test Suite                      ║
╚══════════════════════════════════════════════════════════╝

============================================================
Cenário: Agendamento Simples
Descrição: Cliente quer agendar horário
============================================================

[1/4] Classificando intenção...
  Intent: agendamento (confiança: 0.90)
  Sentiment: neutral

[2/4] Validando classificação...
  Expected: agendamento / neutral
  Result: ✓ PASS

[3/4] Testando automações...
  ✓ Handoff Humano: Not triggered
  ⚠ Detecção de Upsell: Not triggered
  ⚠ Campanha de Reativação: Not triggered
  ✓ Follow-up Automático: Triggered

[4/4] Gerando relatório...

✓ Resultados salvos em: simulation_results_20260311_153045.json
```

---

### Opção 2: **Dados Reais do Supabase**

```bash
# Extrai conversas reais e testa
python tests/test_with_real_data.py --limit=100
```

**O Que Faz:**
1. Conecta no Supabase
2. Extrai N conversas
3. Roda classificação
4. Compara com intenções reais (se tiver)
5. Gera relatório

---

### Opção 3: **Dados Reais + Windmill**

```bash
# Processa conversas reais no Windmill
# Roda automações reais
# Verifica resultados
python tests/test_windmill_automation.py
```

**O Que Faz:**
1. Pega conversas do Supabase
2. Cria jobs no Windmill
3. Aguarda processamento
4. Verifica resultados

---

## 📁 Estrutura de Testes com Dados Reais

```
backend/tests/
├── simulate_tests.py              # Simulação (sem DB)
├── test_with_real_data.py         # Dados reais do Supabase
├── test_windmill_automation.py    # Automações Windmill
├── fixtures/
│   ├── real_conversations.json    # Exemplos reais (anonimizados)
│   └── expected_results.json      # Resultados esperados
└── results/
    ├── simulation_*.json          # Resultados de simulação
    └── real_data_*.json           # Resultados de dados reais
```

---

## 🧪 Cenários de Teste Incluídos

### 1. Agendamento Simples
```
Cliente: "Oi, quero agendar um horário"
Assistant: "Para qual serviço?"
Cliente: "Corte e escova"
Assistant: "Qual dia e horário?"
Cliente: "Amanhã às 14h"

Esperado:
✓ intent: agendamento (confidence > 0.8)
✓ sentiment: neutral
✓ automation: follow-up agendado
```

### 2. Reclamação - Atraso
```
Cliente: "Isso é um absurdo!"
Cliente: "Estou esperando há 30 minutos"
Cliente: "Ninguém me dá satisfação"

Esperado:
✓ intent: reclamacao (confidence > 0.9)
✓ sentiment: angry
✓ automation: handoff humano triggerado
✓ alert: Ntfy enviado
```

### 3. Orçamento com Upsell
```
Cliente: "Quanto cobra para coloração?"
Assistant: "O valor varia..."
Cliente: "Tem promoção?"

Esperado:
✓ intent: orcamento (confidence > 0.8)
✓ sentiment: neutral
✓ automation: upsell detection triggerado
✓ suggestion: pacote promocional
```

### 4. Pós-Venda
```
Assistant: "Como foi seu atendimento?"
Cliente: "Oi! Foi ótimo, adorei!"
Cliente: "Amei o resultado"

Esperado:
✓ intent: feedback_positivo (confidence > 0.9)
✓ sentiment: happy
✓ automation: review request enviado
```

### 5. Cliente Inativo (60+ dias)
```
Assistant: "Sentimos sua falta! 15% OFF"
Cliente: "Oi! Faz tempo mesmo..."
Cliente: "Quanto tá o corte + escova?"

Esperado:
✓ intent: reativacao (confidence > 0.8)
✓ sentiment: neutral
✓ automation: campanha de reativação
```

---

## 📊 Métricas de Validação

### Accuracy de Classificação
```
Total Conversas: 100
Classificações Corretas: 87
Accuracy: 87%

Por Intenção:
• agendamento: 92% accuracy
• reclamacao: 95% accuracy
• orcamento: 85% accuracy
• feedback: 90% accuracy
• reativacao: 78% accuracy
```

### Eficácia de Automações
```
Automações Triggeradas: 45
Automações Corretas: 42
Precision: 93%

Por Tipo:
• Follow-up: 100% correct
• Handoff: 95% correct
• Upsell: 88% correct
• Campaign: 90% correct
```

---

## 🔧 Como Adicionar Novos Cenários

### 1. Editar `simulate_tests.py`

```python
SCENARIOS = {
    "novo_cenario": {
        "name": "Nome do Cenário",
        "description": "Descrição",
        "messages": [
            {"from": "client", "body": "Mensagem 1"},
            {"from": "assistant", "body": "Resposta 1"},
            # ... mais mensagens
        ],
        "expected_intent": "intenção_esperada",
        "expected_sentiment": "sentimento_esperado",
        "should_trigger_handoff": False,
        "should_trigger_upsell": False,
        "should_trigger_campaign": False
    }
}
```

### 2. Rodar Teste

```bash
python tests/simulate_tests.py --scenario=novo_cenario
```

---

## 📈 Resultados Esperados

### Após Rodar 100 Conversas Reais

```
╔══════════════════════════════════════════════════════════╗
║         TEST RESULTS - REAL DATA                         ║
╠══════════════════════════════════════════════════════════╣
║  Total Conversas: 100                                    ║
║  Classificações Corretas: 87                             ║
║  Accuracy: 87%                                           ║
╠══════════════════════════════════════════════════════════╣
║  Automações Triggeradas: 45                              ║
║  Automações Corretas: 42                                 ║
║  Precision: 93%                                          ║
╠══════════════════════════════════════════════════════════╣
║  ✅ READY FOR PRODUCTION                                 ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🎯 Próximos Passos

### 1. Extrair Dados Reais do Supabase

```python
# tests/extract_real_conversations.py
from app.integrations.supabase_client import get_supabase

supabase = get_supabase()

# Extrair 100 conversas
result = supabase.table('conversations')\
    .select('id, phone, status, created_at')\
    .limit(100)\
    .execute()

# Extrair mensagens
for conv in result.data:
    messages = supabase.table('messages')\
        .select('*')\
        .eq('conversation_id', conv['id'])\
        .execute()
    
    # Salvar em fixtures/real_conversations.json
```

### 2. Validar Classificações

```python
# Para cada conversa real:
# 1. Rodar classificação do Brain
# 2. Comparar com intenção real (se tiver)
# 3. Calcular accuracy
```

### 3. Testar Automações

```python
# Para cada conversa:
# 1. Simular processamento
# 2. Verificar automações triggeradas
# 3. Validar se foram corretas
```

---

## ✅ Checklist de Validação

```
[1] Extrair 100 conversas reais
    → python tests/extract_real_conversations.py

[2] Rodar simulações
    → python tests/simulate_tests.py --scenario=all

[3] Validar accuracy > 80%
    → Ver relatório

[4] Testar automações
    → python tests/test_windmill_automation.py

[5] Documentar resultados
    → Salvar em tests/results/
```

---

**Implementado:** 2026-03-11  
**Próxima Revisão:** 2026-03-18  
**Status:** ✅ **PRONTO PARA TESTAR**
