# 🧠 Conversation Intelligence Module

**Módulo de Inteligência de Conversas com Psicologia e Vendas**

---

## 📋 VISÃO GERAL

Este módulo implementa uma **equipe multi-agente** especializada em análise profunda de conversas do WhatsApp, utilizando:

- ✅ **Psicologia** (emoções, personalidade, gatilhos mentais)
- ✅ **Vendas** (funil, objeções, técnicas)
- ✅ **Comportamento** (padrões, churn, lealdade)
- ✅ **Neurociência** (Sistema 1 e 2, vieses cognitivos)

---

## 🏗️ ARQUITETURA

### Equipe de 7 Agentes

```
┌─────────────────────────────────────────────────────────────┐
│                    COORDINATOR AGENT                         │
│                     (Orquestrador)                           │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  EXTRACTOR    │    │  PSYCHOLOGY   │    │    SALES      │
│   AGENT       │    │    AGENT      │    │    AGENT      │
│               │    │               │    │               │
│ • Dados       │    │ • Emoções     │    │ • Funil       │
│ • Entidades   │    │ • DISC        │    │ • Objeções    │
│ • Intenções   │    │ • Gatilhos    │    │ • Conversão   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   BEHAVIOR    │    │   INSIGHTS    │    │   STORAGE     │
│    AGENT      │    │    AGENT      │    │    AGENT      │
│               │    │               │    │               │
│ • Padrões     │    │ • Síntese     │    │ • Supabase    │
│ • Churn       │    │ • Insights    │    │ • Obsidian    │
│ • Lealdade    │    │ • Alertas     │    │ • Cache       │
└───────────────┘    └───────────────┘    └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │   LEARNING    │
                    │    AGENT      │
                    │               │
                    │ • Padrões     │
                    │ • Ajustes     │
                    │ • Feedback    │
                    └───────────────┘
```

---

## 🚀 INSTALAÇÃO

### 1. Adicionar ao main.py

```python
from app.modules_v3.conversation_intelligence.api import router as ci_router

app.include_router(ci_router)
```

### 2. Configurar Feature Flag

Em `modules_v3/feature_flags.py`:

```python
'conversation_intelligence': {
    'enabled': True,  # Ativar módulo
    'traffic_percentage': 100,
    'rollback_time': 60,
},
```

---

## 📖 USO

### Via API

```bash
# Analisar conversa
curl -X POST http://localhost:8000/api/conversation-intelligence/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_123",
    "phone": "5549991112233",
    "client_name": "Maria Silva",
    "messages": [
      {"direction": "inbound", "content": "Oi, quero agendar uma escova"},
      {"direction": "outbound", "content": "Oi Maria! Qual dia você prefere?"}
    ]
  }'
```

### Via Python

```python
from modules_v3.conversation_intelligence.agents.coordinator_agent import CoordinatorAgent, AgentContext

# Inicializar
coordinator = CoordinatorAgent({"debug": True})

# Criar contexto
context = AgentContext(
    conversation_id="conv_123",
    phone="5549991112233",
    client_name="Maria Silva",
    messages=[
        {"direction": "inbound", "content": "Oi, quero agendar"},
        {"direction": "outbound", "content": "Oi! Qual dia?"}
    ]
)

# Analisar
result = coordinator.analyze_conversation(context)

# Acessar insights
print(result["insights"]["key_insights"])
print(result["insights"]["recommendations"])
```

---

## 📊 RESULTADOS

### Exemplo de Resposta

```json
{
  "success": true,
  "conversation_id": "conv_123",
  "phone": "5549991112233",
  "analysis": {
    "extracted_data": {
      "services": [{"name": "escova", "category": "cabelo"}],
      "intents": [{"type": "agendamento", "confidence": 0.9}]
    },
    "psychology": {
      "dominant_emotion": "alegria",
      "personality_type": "I - Influente",
      "communication_style": "emocional"
    },
    "sales": {
      "funnel_stage": "consideration",
      "conversion_probability": 75,
      "objections_count": 0
    },
    "behavior": {
      "dominant_pattern": "impulsivo",
      "churn_risk": "baixo",
      "loyalty_level": "médio"
    },
    "insights": {
      "key_insights": [
        {
          "category": "psicologia",
          "insight": "Emoção predominante: alegria",
          "action": "Reforçar decisão positiva",
          "priority": "média"
        }
      ],
      "recommendations": [
        "Use linguagem emocional e crie conexão pessoal",
        "Fechar agendamento agora (alta probabilidade)"
      ],
      "priority_score": 82
    }
  }
}
```

---

## 🎯 CASOS DE USO

### 1. Análise em Tempo Real

```python
# A cada nova mensagem, analisar e sugerir próxima ação
result = coordinator.analyze_conversation(context)

if result["sales"]["funnel_stage"] == "decision":
    # Sugerir fechamento
    send_message("Posso confirmar seu agendamento?")
```

### 2. Segmentação de Clientes

```python
# Agrupar por personalidade
if result["psychology"]["personality_type"] == "D - Dominante":
    # Cliente direto → abordagem objetiva
elif result["psychology"]["personality_type"] == "I - Influente":
    # Cliente social → abordagem amigável
```

### 3. Prevenção de Churn

```python
if result["behavior"]["churn_risk"] == "alto":
    # Acionar retenção
    send_retention_offer()
    notify_human_agent()
```

### 4. Otimização de Conversão

```python
if result["sales"]["conversion_probability"] > 80:
    # Alta probabilidade → fechar agora
    close_sale()
elif result["sales"]["conversion_probability"] < 30:
    # Baixa → nutrir mais
    nurture_lead()
```

---

## 📚 FRAMEWORKS UTILIZADOS

| Framework | Agente | Aplicação |
|-----------|--------|-----------|
| **Paul Ekman** | Psychology | 6 emoções básicas |
| **Big Five** | Psychology | Traços de personalidade |
| **DISC** | Psychology | Tipos comportamentais |
| **Cialdini** | Psychology | Gatilhos mentais |
| **SPIN Selling** | Sales | Perguntas de venda |
| **Funil de Vendas** | Sales | Estágios |
| **Kahneman** | Behavior | Sistema 1 e 2 |
| **Nudge Theory** | Behavior | Empurrões sutis |

---

## 🔧 CONFIGURAÇÃO

### Configurar Agentes

```python
config = {
    "debug": True,
    "obsidian_path": "/path/to/obsidian_vault",
    "extractor": {"enabled": True},
    "psychology": {"enabled": True, "debug": False},
    "sales": {"enabled": True},
    "behavior": {"enabled": True},
    "insights": {"enabled": True},
    "storage": {"enabled": True, "supabase": True, "obsidian": True},
    "learning": {"enabled": True, "learning_rate": 0.1},
}

coordinator = CoordinatorAgent(config)
```

---

## 📈 MÉTRICAS

### Por Conversa

- **Tempo de processamento:** ~500-1000ms
- **Confiança média:** 0.7-0.9
- **Insights gerados:** 3-8 por conversa

### Por Cliente

- **Emoção predominante**
- **Tipo de personalidade**
- **Risco de churn**
- **Nível de lealdade**
- **Probabilidade de conversão**

---

## 🚨 ALERTAS

O módulo gera alertas automáticos para:

- 🔴 **Churn Alto** → Intervenção imediata
- 🟡 **Objeções Múltiplas** → Ajustar abordagem
- 🟢 **Alta Conversão** → Fechar agora
- 💡 **Oportunidade Upsell** → Oferecer mais

---

## 📖 KNOWLEDGE BASE

A base de conhecimento inclui:

- **Psicologia:** Emoções, personalidade, gatilhos
- **Vendas:** SPIN, funil, objeções
- **Comportamento:** Padrões, vieses, jornada

Ver `knowledge/psychology_sales_frameworks.md` para detalhes.

---

## 🔗 LINKS RELACIONADOS

- [[000_MCT_MASTER_INDEX]]
- [[LUNA_SYSTEM_PROMPT]]
- [[REGRAS_NEGOCIO]]
- [[PROFISSIONAIS_HAVEN]]

---

**Criado:** 2026-03-01  
**Via:** Agent Flow  
**Versão:** 1.0.0  
**Status:** ✅ Operacional
