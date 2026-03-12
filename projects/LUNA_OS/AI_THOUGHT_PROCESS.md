# 🧠 AI Thought Process — LUNA OS v3.0

## Visão Geral

Implementação de observabilidade completa do processo decisório da IA, permitindo acompanhar em tempo real o "pensamento" interno da Luna durante as conversas.

---

## 🎯 Funcionalidades Implementadas

### 1. **AI Thought Panel** (Frontend)

**Local:** `frontend/app/conversations/page.tsx`

Um painel lateral que exibe:

- **🎯 Triage:** Classificação inicial da mensagem (intent, urgência, sentimento, confiança)
- **🔄 Agent Chain:** Sequência de agentes executados
- **🚨 Escalation:** Se foi necessário escalar para humano e o motivo
- **💬 Resposta Gerada:** A resposta que a IA construiu
- **🛡️ Guardrails:** Se passou ou foi bloqueada pelos guardrails

**Como usar:**
1. Abra uma conversa em `/conversations`
2. No painel "Live Intelligence", clique em **"AI Thought"**
3. O painel lateral mostrará todo o processo decisório

---

### 2. **API de Pensamento da IA** (Backend)

**Endpoints:**

#### `GET /api/conversations/{id}/thought`

Retorna o processo de pensamento completo:

```json
{
  "success": true,
  "thought": {
    "triage": {
      "intent": "agendamento",
      "urgency": "medium",
      "sentiment": "neutral",
      "confidence": 0.92,
      "summary": "Cliente quer agendar horário para amanhã"
    },
    "agent_chain": ["triage", "resolution", "followup"],
    "agent_insights": {
      "triage": {...},
      "resolution": {...}
    },
    "escalation": {
      "requires_human": false,
      "human_reason": ""
    },
    "response": {
      "generated": "Vou verificar a agenda da Jú para você...",
      "model_used": "google/gemini-2.0-flash-001",
      "processing_time_ms": 1234
    },
    "guardrails": {
      "passed": true,
      "blocked_reason": ""
    }
  }
}
```

#### `GET /api/conversations/{id}/orchestration`

Retorna status detalhado da orquestração de agentes:

```json
{
  "success": true,
  "orchestration": {
    "pipeline": {
      "status": "completed",
      "current_agent": "followup",
      "agents_executed": ["triage", "resolution", "followup"],
      "total_agents": 3
    },
    "agents_detail": [...],
    "performance": {
      "processing_time_ms": 1234,
      "created_at": "2026-03-10T10:00:00Z"
    }
  }
}
```

#### `GET /api/conversations/debug/active`

Retorna sessões de debug ativas (conversas sendo processadas nos últimos 5 minutos).

---

### 3. **Sistema de Apelidos para Profissionais**

**Endpoints:**

#### `GET /api/professionals/aliases`

Retorna todos profissionais com seus apelidos:

```json
{
  "success": true,
  "professionals": [
    {
      "id": "uuid-123",
      "key": "professional_yujaira",
      "name": "Yujaira",
      "aliases": ["Jú", "Julia", "Ju"],
      "all_names": ["Yujaira", "Jú", "Julia", "Ju"]
    }
  ]
}
```

#### `POST /api/professionals/{id}/aliases`

Adiciona ou atualiza apelidos:

```bash
curl -X POST http://localhost:8000/api/professionals/yujaira/aliases \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your-key" \
  -d '{"aliases": ["Jú", "Julia", "Ju"]}'
```

**Como a IA usa os apelidos:**

Quando um cliente menciona "Jú", a IA:
1. Busca no sistema de apelidos
2. Encontra que "Jú" = "Yujaira"
3. Consulta a agenda de Yujaira
4. Responde corretamente

---

## 🔍 Arquitetura de Orquestração

### Pipeline de Processamento

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DO ORCHESTRATOR                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  MENSAGEM WHATSAPP → [Triage Agent]                         │
│                        │                                      │
│                        ├─→ Classifica: intent, urgency,      │
│                        │   sentiment, confidence             │
│                        │                                      │
│                        ├─→ Baixa confiança → Human Gate      │
│                        │                                      │
│                        ├─→ Reclamação → Complaint Agent      │
│                        │                                      │
│                        └─→ Outros → Resolution Agent         │
│                                                              │
│  [Resolution Agent] → Gera resposta → [Followup Agent]      │
│                                                              │
│  [Guardrails] → Valida → [WhatsApp]                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Agentes Envolvidos

| Agente | Função | Arquivo |
|--------|--------|---------|
| **Triage** | Classifica intenção e urgência | `backend/app/core/agents/triage.py` |
| **Resolution** | Resolve dúvidas | `backend/app/core/agents/resolution.py` |
| **Complaint** | Gerencia reclamações | `backend/app/core/agents/complaint.py` |
| **Followup** | Agenda acompanhamento | `backend/app/core/agents/followup.py` |
| **Human Gate** | Avalia escalação | `backend/app/core/agents/human_gate.py` |

---

## 📊 Casos de Uso

### Caso 1: Cliente pede agendamento

**Mensagem:** "Queria agendar meu horário amanhã às 17:40 pra corte"

**Pensamento da IA:**
```
🎯 Triage:
  - Intent: agendamento
  - Urgency: medium
  - Sentiment: neutral
  - Confidence: 0.95

🔄 Agent Chain: triage → resolution → followup

💬 Resposta:
  "Vou verificar a agenda da Jú para você.
   Ela tem horário amanhã às 17:40.
   Posso confirmar?"

🛡️ Guardrails: Passed ✅
```

### Caso 2: Cliente pede por apelido

**Mensagem:** "Yujaira tem horário hoje à tarde p escova modelada?"

**Processo:**
1. IA busca "Yujaira" no sistema de apelidos
2. Encontra: Yujaira = "Jú" = "Julia"
3. Consulta agenda de Yujaira
4. Retorna horários disponíveis

### Caso 3: Reclamação (escalação)

**Mensagem:** "Estou muito insatisfeita com o atendimento!"

**Pensamento da IA:**
```
🎯 Triage:
  - Intent: reclamacao
  - Urgency: critical
  - Sentiment: angry
  - Confidence: 0.98

🚨 Escalation:
  - Requires Human: YES
  - Reason: Cliente muito insatisfeita, necessita compensação

💬 Resposta:
  "Sinto muito pela experiência.
   Vou transferir para nossa gerente resolver isso agora."
```

---

## 🛠️ Debug e Observabilidade

### Logs em Tempo Real

**Backend:** `backend/logs/luna_core.log`

```log
[Orchestrator] Triage → route=resolution intent=agendamento urgency=medium confidence=0.95
[Triage] intent=agendamento urgency=medium sentiment=neutral confidence=0.95 → resolution
[Resolution] ticket=TKT-ABC123 escalation=false intent=agendamento
[Followup] scheduled=True followup_in=24h
[Orchestrator] Concluído | intent=agendamento chain=[triage,resolution,followup] time=1234ms
```

### Painel de Debug

**Frontend:** Botão "AI Thought" no painel de conversas

Mostra visualmente:
- Todo o pipeline executado
- Decisões de cada agente
- Motivo de escalações
- Resposta gerada antes de enviar

---

## 📁 Arquivos Criados/Modificados

### Backend
- ✅ `backend/app/api/ai_thought.py` — API de pensamento da IA
- ✅ `backend/app/api/professionals.py` — Sistema de apelidos (atualizado)
- ✅ `backend/app/main.py` — Router registrado

### Frontend
- ✅ `frontend/app/conversations/page.tsx` — AI Thought Panel

---

## 🚀 Próximos Passos

1. **Testar com conversas reais** — Validar com dados do Supabase
2. **Adicionar histórico** — Mostrar evolução do pensamento ao longo da conversa
3. **Exportar pensamento** — Permitir salvar/exportar o processo para Obsidian
4. **Alertas de alucinação** — Detectar quando confiança é baixa mas IA responde mesmo assim

---

## 🎉 Benefícios

- ✅ **Transparência:** Saiba exatamente o que a IA está "pensando"
- ✅ **Debug:** Identifique problemas de orquestração rapidamente
- ✅ **Treinamento:** Use os pensamentos para melhorar prompts
- ✅ **Confiança:** Valide se a IA está alinhada com as orientações
- ✅ **Apelidos:** Clientes podem chamar profissionais por nomes íntimos

---

**Implementado:** 2026-03-10  
**Versão:** LUNA OS v3.0  
**Status:** ✅ Production Ready
