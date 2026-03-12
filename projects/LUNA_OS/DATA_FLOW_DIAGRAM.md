# 🔄 LUNA OS - Data Flow Between Functions

Este documento mostra visualmente como os dados fluem entre as funções da LUNA.

---

## 📊 Visão Geral do Fluxo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUXO PRINCIPAL DE DADOS                              │
│                                                                              │
│  WHATSAPP (Evolution API)                                                    │
│     │                                                                        │
│     │ 1. Mensagem recebida                                                   │
│     ▼                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ BRAIN (app.core.brain)                                                  ││
│  │                                                                         ││
│  │  ┌──────────────────────────────────────────────────────────────────┐  ││
│  │  │ 1. process_message(phone, message)                                │  ││
│  │  │    ├─ Classifica intenção                                         │  ││
│  │  │    └─ Seleciona modelo                                            │  ││
│  │  └──────────────────────────────────────────────────────────────────┘  ││
│  │                                                                         ││
│  │  ┌──────────────────────────────────────────────────────────────────┐  ││
│  │  │ 2. build_context(phone)                                           │  ││
│  │  │    ├─ memory.get_client_profile(phone)                           │  ││
│  │  │    ├─ memory.get_recent_history(phone)                           │  ││
│  │  │    └─ semantic_memory.search_similar(message)                    │  ││
│  │  └──────────────────────────────────────────────────────────────────┘  ││
│  │                                                                         ││
│  │  ┌──────────────────────────────────────────────────────────────────┐  ││
│  │  │ 3. Logic Engine Pass                                              │  ││
│  │  │    └─ openrouter.complete(system=logic_prompt)                   │  ││
│  │  │        ├─ Extrai BOOKING_JSON                                    │  ││
│  │  │        ├─ Extrai UPDATE_STATE_JSON                               │  ││
│  │  │        └─ Extrai INTELLIGENCE_JSON                               │  ││
│  │  └──────────────────────────────────────────────────────────────────┘  ││
│  │                                                                         ││
│  │  ┌──────────────────────────────────────────────────────────────────┐  ││
│  │  │ 4. Voice Engine Pass                                              │  ││
│  │  │    └─ openrouter.complete(system=voice_prompt)                   │  ││
│  │  │        └─ Gera resposta em linguagem natural                     │  ││
│  │  └──────────────────────────────────────────────────────────────────┘  ││
│  │                                                                         ││
│  │  ┌──────────────────────────────────────────────────────────────────┐  ││
│  │  │ 5. Post-Processing                                                │  ││
│  │  │    ├─ scheduler.process_booking() [se agendamento]               │  ││
│  │  │    ├─ memory.save_conversation()                                 │  ││
│  │  │    ├─ memory.save_intelligence()                                 │  ││
│  │  │    └─ semantic_memory.add_embedding()                            │  ││
│  │  └──────────────────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│     │                                                                        │
│     │ 2. Resposta                                                            │
│     ▼                                                                        │
│  WHATSAPP (Evolution API)                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Detalhamento por Integração

### 1. BRAIN ↔ MEMORY

```
┌─────────────────────────┐         ┌─────────────────────────┐
│      BRAIN              │         │       MEMORY            │
│  (app.core.brain)       │         │  (app.core.memory)      │
│                         │         │                         │
│  process_message()      │─────┐   │                         │
│                         │     │   │                         │
│                         │     │1  │ get_client_profile()    │
│                         │     └──►│  - Lê perfil do cliente │
│                         │         │  - Retorna: nome, tags, │
│                         │         │    preferências, LTV    │
│                         │◄──────┘  │                         │
│                         │  Perfil │                         │
│                         │         │                         │
│                         │─────┐   │                         │
│                         │     │2  │ get_recent_history()    │
│                         │     └──►│  - Últimas 10 mensagens │
│                         │         │  - Histórico completo   │
│                         │◄──────┘  │                         │
│                         │  Mens.  │                         │
│                         │         │                         │
│                         │─────┐   │                         │
│                         │     │3  │ save_conversation()     │
│                         │     └──►│  - Salva conversa       │
│                         │         │  - Atualiza status      │
│                         │         │                         │
│                         │◄──────┘  │                         │
│                         │  OK     │                         │
│                         │         │                         │
│                         │─────┐   │                         │
│                         │     │4  │ save_intelligence()     │
│                         │     └──►│  - Insight              │
│                         │         │  - Pain point           │
│                         │         │  - Opportunity          │
│                         │         │  - Churn risk           │
│                         │◄──────┘  │                         │
│                         │  OK     │                         │
└─────────────────────────┘         └─────────────────────────┘

Dados trafegados:
┌────────────────────────────────────────────────────────────┐
│ get_client_profile(phone)                                  │
│  → phone: str                                              │
│  ← ClientProfile(id, name, tags, preferences, ...)         │
├────────────────────────────────────────────────────────────┤
│ get_recent_history(phone)                                  │
│  → phone: str                                              │
│  ← List[{"role": str, "content": str, "timestamp": str}]   │
├────────────────────────────────────────────────────────────┤
│ save_conversation(conv)                                    │
│  → Conversation(id, phone, status, intent, messages, ...)  │
│  ← bool                                                    │
├────────────────────────────────────────────────────────────┤
│ save_intelligence(phone, conv_id, intelligence)            │
│  → phone: str, conv_id: str,                               │
│    IntelligenceData(insight, pain_point, opportunity, ...) │
│  ← bool                                                    │
└────────────────────────────────────────────────────────────┘
```

### 2. BRAIN ↔ SEMANTIC MEMORY (MILVUS)

```
┌─────────────────────────┐         ┌─────────────────────────┐
│      BRAIN              │         │   SEMANTIC MEMORY       │
│  (app.core.brain)       │         │   (app.integrations.    │
│                         │         │    semantic_memory)     │
│                         │         │                         │
│  build_context()        │─────┐   │                         │
│                         │     │   │                         │
│                         │     │1  │ search_similar()        │
│                         │     └──►│  - Gera embedding       │
│                         │         │  - Busca no Milvus      │
│                         │         │  - COSINE similarity    │
│                         │◄──────┘  │                         │
│                         │  RAG    │                         │
│                         │  Context│                         │
│                         │         │                         │
│  Post-processing        │─────┐   │                         │
│                         │     │2  │ add_embedding()         │
│                         │     └──►│  - Gera embedding       │
│                         │         │  - Salva no Milvus      │
│                         │         │  - Coleção:             │
│                         │         │    luna_conversations   │
│                         │◄──────┘  │                         │
│                         │  OK     │                         │
└─────────────────────────┘         └─────────────────────────┘

Dados trafegados:
┌────────────────────────────────────────────────────────────┐
│ search_similar(text, limit, collection)                    │
│  → text: str, limit: int (default=5),                      │
│    collection: str (default="luna_conversations")          │
│  ← List[{                                                  │
│       conversation_id: str,                                │
│       content: str,                                        │
│       metadata: {phone, intent, sentiment, timestamp},     │
│       score: float                                         │
│     }]                                                     │
├────────────────────────────────────────────────────────────┤
│ add_embedding(text, metadata, collection)                  │
│  → text: str,                                              │
│    metadata: {phone, intent, sentiment, conversation_id},  │
│    collection: str                                         │
│  ← str (ID do embedding)                                   │
└────────────────────────────────────────────────────────────┘
```

### 3. BRAIN ↔ SCHEDULER

```
┌─────────────────────────┐         ┌─────────────────────────┐
│      BRAIN              │         │      SCHEDULER          │
│  (app.core.brain)       │         │  (app.core.scheduler)   │
│                         │         │                         │
│  process_message()      │─────┐   │                         │
│  [detecta agendamento]  │     │   │                         │
│                         │     │1  │ process_booking()       │
│                         │     └──►│  - Valida dados         │
│                         │         │  - Consulta Belasis     │
│                         │         │  - Encontra horário     │
│                         │         │  - Confirma agendamento │
│                         │◄──────┘  │                         │
│                         │  Result │                         │
│                         │         │                         │
└─────────────────────────┘         └─────────────────────────┘

Dados trafegados:
┌────────────────────────────────────────────────────────────┐
│ process_booking(phone, extracted_data, conversation_id)    │
│  → phone: str,                                             │
│    extracted_data: {                                       │
│      services: List[str],                                  │
│      date: str,                                            │
│      time: str,                                            │
│      professional: str (optional),                         │
│      client_has_gel: bool                                  │
│    },                                                      │
│    conversation_id: str                                    │
│  ← Tuple[                                                  │
│      success: bool,                                        │
│      feedback: str,                                        │
│      booking_data: Dict                                    │
│    ]                                                       │
└────────────────────────────────────────────────────────────┘
```

### 4. BRAIN ↔ OPENROUTER (LLM)

```
┌─────────────────────────┐         ┌─────────────────────────┐
│      BRAIN              │         │      OPENROUTER         │
│  (app.core.brain)       │         │ (app.integrations.      │
│                         │         │  openrouter)            │
│                         │         │                         │
│  Logic Engine Pass      │─────┐   │                         │
│  [model: DeepSeek/Mini] │     │   │                         │
│                         │     │1  │ complete()              │
│                         │     └──►│  - Envia messages       │
│                         │         │  - System: logic_prompt │
│                         │         │  - Temperature: 0.1     │
│                         │◄──────┘  │                         │
│                         │  Logic  │                         │
│                         │  Text   │                         │
│                         │         │                         │
│  Voice Engine Pass      │─────┐   │                         │
│  [model: Sonnet 4.6]    │     │2  │ complete()              │
│                         │     └──►│  - Envia messages       │
│                         │         │  - System: voice_prompt │
│                         │         │  - Temperature: 0.7     │
│                         │◄──────┘  │                         │
│                         │  Voice  │                         │
│                         │  Text   │                         │
└─────────────────────────┘         └─────────────────────────┘

Dados trafegados:
┌────────────────────────────────────────────────────────────┐
│ complete(messages, system, model, temperature, ...)        │
│  → messages: List[{role: str, content: str}],              │
│    system: str,                                            │
│    model: str,                                             │
│    temperature: float (0.0-1.0)                            │
│  ← str (resposta completa do LLM)                          │
└────────────────────────────────────────────────────────────┘
```

### 5. MEMORY ↔ SUPABASE

```
┌─────────────────────────┐         ┌─────────────────────────┐
│       MEMORY            │         │       SUPABASE          │
│  (app.core.memory)      │         │  (PostgreSQL Cloud)     │
│                         │         │                         │
│  get_client_profile()   │─────┐   │                         │
│                         │     │1  │ SELECT FROM clients     │
│                         │     └──►│  WHERE phone = ?        │
│                         │         │                         │
│                         │◄──────┘  │                         │
│                         │  Profile│                         │
│                         │  Data   │                         │
│                         │         │                         │
│  save_conversation()    │─────┐   │                         │
│                         │     │2  │ INSERT INTO conv.       │
│                         │     └──►│ INSERT INTO messages    │
│                         │         │                         │
│                         │◄──────┘  │                         │
│                         │  OK     │                         │
│                         │         │                         │
│  save_intelligence()    │─────┐   │                         │
│                         │     │3  │ INSERT INTO conv_       │
│                         │     └──►│    intelligence         │
│                         │         │                         │
│                         │◄──────┘  │                         │
│                         │  OK     │                         │
└─────────────────────────┘         └─────────────────────────┘

Tabelas usadas:
┌────────────────────────────────────────────────────────────┐
│ clients                                                    │
│  - id (UUID)                                               │
│  - phone (TEXT)                                            │
│  - name (TEXT)                                             │
│  - tags (TEXT[])                                           │
│  - preferences (JSONB)                                     │
│  - total_visits (INT)                                      │
│  - total_spent (DECIMAL)                                   │
│  - created_at (TIMESTAMP)                                  │
├────────────────────────────────────────────────────────────┤
│ conversations                                              │
│  - id (UUID)                                               │
│  - phone (TEXT)                                            │
│  - client_id (UUID)                                        │
│  - status (TEXT)                                           │
│  - intent (TEXT)                                           │
│  - sentiment (TEXT)                                        │
│  - started_at (TIMESTAMP)                                  │
│  - ended_at (TIMESTAMP)                                    │
├────────────────────────────────────────────────────────────┤
│ messages                                                   │
│  - id (UUID)                                               │
│  - conv_id (UUID)                                          │
│  - body (TEXT)                                             │
│  - from (TEXT)                                             │
│  - created_at (TIMESTAMP)                                  │
├────────────────────────────────────────────────────────────┤
│ conversation_intelligence                                  │
│  - id (UUID)                                               │
│  - conv_id (UUID)                                          │
│  - insight (TEXT)                                          │
│  - pain_point (TEXT)                                       │
│  - opportunity (TEXT)                                      │
│  - churn_risk (TEXT)                                       │
│  - mood (TEXT)                                             │
│  - created_at (TIMESTAMP)                                  │
└────────────────────────────────────────────────────────────┘
```

---

## 📈 Sequência Completa: Agendamento

```
Cliente                 WhatsApp                Brain                   Memory                Scheduler             OpenRouter            Milvus               Supabase
  │                        │                       │                        │                       │                       │                      │                    │
  │──1. Mensagem─────────►│                       │                        │                       │                       │                      │                    │
  │                        │──2. Webhook─────────►│                        │                       │                       │                      │                    │
  │                        │                       │                        │                       │                       │                      │                    │
  │                        │                       │──3. get_profile──────►│                       │                       │                      │                    │
  │                        │                       │◄─4. Profile───────────│                       │                       │                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──5. get_history──────►│                       │                       │                      │                    │
  │                        │                       │◄─6. History───────────│                       │                       │                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──7. search_similar─────────────────────────►│                      │                    │
  │                        │                       │◄─8. RAG Context────────────────────────────│                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──9. Logic Prompt─────────────────────────────────►│                      │                    │
  │                        │                       │◄─10. Logic Text──────────────────────────────────│                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──11. Voice Prompt────────────────────────────────►│                      │                    │
  │                        │                       │◄─12. Voice Response──────────────────────────────│                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──13. process_booking─────────────────────────►│                      │                    │
  │                        │                       │◄─14. Booking OK──────────────────────────────│                      │                    │
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │                       │──15. save_conversation──────────────────────────────────────────────────────────────────────►│
  │                        │                       │──16. save_intelligence──────────────────────────────────────────────────────────────────────►│
  │                        │                       │──17. add_embedding─────────────────────────────────────────────────────────────────────────►│
  │                        │                       │                        │                       │                      │                      │                    │
  │                        │◄─18. Response─────────│                        │                       │                       │                      │                    │
  │◄─19. Mensagem──────────│                        │                        │                       │                       │                      │                    │
  │                        │                       │                        │                       │                       │                      │                    │
```

---

## 🎯 Pontos de Verificação (Checkpoints)

### checkpoint_1: Recebimento
- [ ] Webhook recebido
- [ ] Phone extraído
- [ ] Message parseada

### checkpoint_2: Contexto
- [ ] Perfil do cliente lido
- [ ] Histórico recuperado
- [ ] RAG search executada

### checkpoint_3: Processamento
- [ ] Intent classificada
- [ ] Logic prompt executado
- [ ] Voice prompt executado
- [ ] Resposta gerada

### checkpoint_4: Ações
- [ ] Scheduler chamado (se agendamento)
- [ ] Conversa salva
- [ ] Inteligência extraída
- [ ] Embedding armazenado

### checkpoint_5: Resposta
- [ ] Resposta formatada
- [ ] Enviado para WhatsApp
- [ ] Cliente recebeu

---

## 📊 Matriz de Dependências

| De \ Para | Brain | Memory | Scheduler | Semantic | Supabase | Milvus | OpenRouter |
|-----------|-------|--------|-----------|----------|----------|--------|------------|
| **Brain** | - | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |
| **Memory** | ✅ | - | - | - | ✅ | - | - |
| **Scheduler** | ✅ | ✅ | - | - | ⚠️ | - | - |
| **Semantic** | ✅ | - | - | - | - | ✅ | - |

Legenda:
- ✅ = Dependência direta
- ⚠️ = Dependência via outro módulo
- - = Sem dependência

---

*Última atualização: 2026-03-11*
*LUNA OS v3.0*
