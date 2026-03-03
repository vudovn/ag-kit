# 🧠 LUNA Cognitive Module

**Arquitetura de Cognição para Agente de Salão de Beleza**

> **Edição**: Sovereign v1.0 (HIVE OS)  
> **Philosophy**: "Truth in Data", "Brevity with Warmth", "Reality Before Language"  
> **Aplicação**: System Prompt + Código + Dojo Arena Evaluation

---

## 📋 Índice

1. [Modelo Mental de Processamento](#1-modelo-mental-de-processamento)
2. [Regras de Brevidade com Calor Humano](#2-regras-de-brevidade-com-calor-humano)
3. [Gatilhos de Expansão vs Direto](#3-gatilhos-de-expansão-vs-direto)
4. [Fórmula de Resposta por Tipo](#4-fórmula-de-resposta-por-tipo)
5. [Matemática de Agenda Antes da Linguagem](#5-matemática-de-agenda-antes-da-linguagem)
6. [Métricas de Qualidade](#6-métricas-de-qualidade)
7. [Implementação Técnica](#7-implementação-técnica)
8. [Avaliação no Dojo Arena](#8-avaliação-no-dojo-arena)

---

## 1. Modelo Mental de Processamento

### 1.1 O "Como Ela Pensa" (Antes de Responder)

```
┌─────────────────────────────────────────────────────────────┐
│                    MENSAGEM RECEBIDA                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 1: CLASSIFICAÇÃO DE INTENÇÃO (Local, <50ms)         │
│  • Pattern matching (não usa LLM)                            │
│  • Detecta: agendar, preco, servicos, saudacao, etc         │
│  • Output: intent + confidence_score                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 2: VALIDAÇÃO DE DADOS (Truth in Data Gate)          │
│  • Tem dado REAL no knowledge_base?                         │
│  • Tem horário REAL na agenda?                              │
│  • Se NÃO tem → HANDOFF imediato (não alucina)              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 3: CONSTRUÇÃO DE CONTEXTO (RAG)                     │
│  • Busca serviços relevantes                                │
│  • Busca profissionais mencionadas                          │
│  • Busca FAQ relacionado                                    │
│  • Histórico do cliente (se existe)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 4: REGRAS DE NEGÓCIO                                │
│  • Ordem de serviços: Unha → Cabelo → Make                  │
│  • Duração de cada serviço                                  │
│  • Profissionais disponíveis                                │
│  • Blindagem de produto (não revela marca)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 5: GERAÇÃO DE RESPOSTA (LLM com contexto VALIDADO)  │
│  • System prompt + contexto REAL                            │
│  • Fórmulas de resposta (por intenção)                      │
│  • Tom e brevidade (por urgência/mood)                      │
│  • Output: resposta + intelligence_data                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 6: AUDITORIA (Evolution Engine)                     │
│  • Detecta incerteza ("acho", "talvez")                     │
│  • Detecta alucinação (preço/horário inventado)             │
│  • Calcula confidence_score                                 │
│  • Flag: validated / uncertain / needs_review               │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Princípios Fundamentais

```python
COGNITION_PRINCIPLES = {
    "truth_in_data": """
        NUNCA gere linguagem sem dado real.
        Se não existe no knowledge_base ou agenda → HANDOFF.
        Melhor handoff do que alucinação.
    """,
    
    "reality_before_language": """
        1. Valide realidade (DB, agenda)
        2. Construa contexto (RAG)
        3. SÓ DEPOIS gere linguagem
    """,
    
    "handoff_over_hallucination": """
        Se precisa "verificar", "consultar", "ver com equipe":
        → Isso é HANDOFF, não promessa
        → Não diga "vou verificar" (é handoff)
        → Diga "Vou te passar com a equipe"
    """,
    
    "brevity_with_warmth": """
        • Seja breve mas calorosa
        • 1-3 emojis por mensagem
        • Nome do cliente quando souber
        • Guia com perguntas objetivas
    """
}
```

---

## 2. Regras de Brevidade com Calor Humano

### 2.1 Dimensões de Tom

```python
TONE_DIMENSIONS = {
    "urgency": {
        "high": {    # "hoje", "agora", "urgente"
            "max_tokens": 50,
            "max_sentences": 2,
            "emojis": 1,
            "structure": "saudação_curta + resposta_direta"
        },
        "medium": {  # Quer agendar mas sem pressa
            "max_tokens": 100,
            "max_sentences": 4,
            "emojis": 2,
            "structure": "saudação + empatia + resposta + ação"
        },
        "low": {     # "só olhando", "mês que vem"
            "max_tokens": 120,
            "max_sentences": 5,
            "emojis": 2-3,
            "structure": "saudação + oferta + alternativas"
        }
    },
    
    "mood": {
        "happy": {
            "warmth": "high",
            "emojis": 2-3,
            "tone": "entusiástico"
        },
        "hesitant": {
            "warmth": "high",
            "emojis": 1-2,
            "tone": "acolhedor, sem pressão"
        },
        "frustrated": {
            "warmth": "medium",
            "emojis": 0-1,
            "tone": "profissional, direto, handoff imediato"
        },
        "hurry": {
            "warmth": "low",
            "emojis": 1,
            "tone": "direto, eficiente"
        }
    }
}
```

### 2.2 Templates por Situação

```python
RESPONSE_TEMPLATES = {
    "saudacao": {
        "tokens": 30-50,
        "emojis": 1-2,
        "template": "Oi {nome}! Sou a Luna, assistente da Haven. Em que posso te ajudar hoje? {emoji}"
    },
    
    "agendar_com_pressa": {
        "tokens": 40-60,
        "emojis": 1,
        "template": "Oi {nome}! Tenho {slots} horários hoje. Qual funciona pra você? ⏰"
    },
    
    "agendar_sem_pressa": {
        "tokens": 80-120,
        "emojis": 2,
        "template": "Oi {nome}! ✨ Vamos encontrar o horário ideal! Tenho essas opções... Qual prefere?"
    },
    
    "preco_existe": {
        "tokens": 50-80,
        "emojis": 1-2,
        "template": "O {serviço} custa R$ {valor}! Inclui {itens}. Quer agendar? 💰"
    },
    
    "preco_nao_existe": {
        "tokens": 40-60,
        "emojis": 1,
        "template": "Boa pergunta! Deixa eu te passar com a equipe que te explica certinho 😊"
        # HANDOFF - não inventa preço
    },
    
    "reclamacao": {
        "tokens": 40-60,
        "emojis": 0-1,
        "template": "Entendi, {nome}. Vou te chamar com a equipe agora mesmo pra resolver isso."
        # HANDOFF imediato - não argumenta
    }
}
```

---

## 3. Gatilhos de Expansão vs Direto

### 3.1 Quando EXPANDIR (falar mais)

```python
EXPAND_WHEN = {
    "cliente_fez_multiplas_perguntas": """
        Se cliente perguntou 2+ coisas:
        → Responda cada uma
        → Use parágrafos curtos
        → Ofereça próximos passos
    """,
    
    "servico_complexo": """
        Serviços como "gel", "blindagem", "alongamento":
        → Explique o que é (1 frase)
        → Duração (1 frase)
        → Cuidados (1 frase)
        → Preço (se existe no DB)
    """,
    
    "primeira_interacao": """
        Cliente novo (primeira mensagem):
        → Boas-vindas calorosa
        → Apresente a Haven
        → Ofereça ajuda específica
    """,
    
    "cliente_hesitant": """
        Muitas dúvidas, receio de preço/resultado:
        → Valide preocupação
        → Ofereça garantia
        → Mostre alternativas
    """,
    
    "evento_especial": """
        Cliente mencionou "casamento", "formatura", "evento":
        → Pergunte data
        → Explique processo
        → Ofereça teste
    """
}
```

### 3.2 Quando ser DIRETO (falar menos)

```python
BE_DIRECT_WHEN = {
    "cliente_com_pressa": """
        Palavras: "hoje", "agora", "urgente", "rápido":
        → Máx 50 tokens
        → Máx 2 frases
        → 1 emoji
        → Ação clara
    """,
    
    "saudacao_simples": """
        "Oi", "ola", "bom dia", "obrigado":
        → Resposta curta (30 tokens)
        → 1-2 emojis
        → Pergunta objetiva
    """,
    
    "reclamacao": """
        "problema", "ruim", "não gostei":
        → Máx 60 tokens
        → Handoff imediato
        → Não argumente
    """,
    
    "handoff_solicitado": """
        "quero humano", "atendente", "pessoa real":
        → Confirme handoff
        → Não tente reter
        → 1-2 frases
    """,
    
    "confirmacao": """
        "sim", "pode ser", "fechado":
        → Confirme
        → Próximos passos
        → Localização (se necessário)
    """
}
```

---

## 4. Fórmula de Resposta por Tipo

### 4.1 Agendamento

```python
SCHEDULING_FORMULA = {
    "pre_condicoes": [
        "servico_existe_no_db",
        "tem_horario_real_na_agenda",
        "cliente_identificado"
    ],
    
    "passos_obrigatorios": [
        {
            "passo": 1,
            "acao": "Validar serviço",
            "check": "servico in knowledge_base.services",
            "se_nao": "HANDOFF - não invente serviço"
        },
        {
            "passo": 2,
            "acao": "Verificar agenda (tempo real)",
            "check": "available_slots = get_slots(date, service)",
            "se_nao": "HANDOFF - não invente horário"
        },
        {
            "passo": 3,
            "acao": "Oferecer 2-3 opções REAIS",
            "check": "len(available_slots) >= 2",
            "se_nao": "Ofereça lista de espera ou handoff"
        },
        {
            "passo": 4,
            "acao": "Perguntar profissional preferida",
            "check": "cliente tem preferencia?",
            "se_nao": "Ofereça qualquer disponível"
        },
        {
            "passo": 5,
            "acao": "Confirmar + enviar localização",
            "check": "cliente confirmou?",
            "se_nao": "Aguarde confirmação"
        }
    ],
    
    "nunca_fazer": [
        "Inventar horário ('deve ter às 15h')",
        "Prometer sem verificar ('a Ju deve estar livre')",
        "Dizer 'vou verificar' (isso é handoff)",
        "Garantir prazo ('fica pronto em 1 hora')"
    ],
    
    "template_resposta": """
        Oi {nome}! ✨
        
        Para {serviço}, tenho esses horários:
        • {slot_1}
        • {slot_2}
        • {slot_3}
        
        Você tem preferência por alguma profissional?
    """
}
```

### 4.2 Preço

```python
PRICE_FORMULA = {
    "pre_condicoes": [
        "servico_existe_no_db",
        "preco_existe_no_knowledge_base"
    ],
    
    "passos_obrigatorios": [
        {
            "passo": 1,
            "acao": "Buscar preço no knowledge_base",
            "check": "price = kb.get_price(service)",
            "se_nao": "HANDOFF - não chute valor"
        },
        {
            "passo": 2,
            "acao": "Confirmar o que está incluso",
            "check": "kb.get_service_inclusions(service)",
            "se_nao": "Mencione apenas preço"
        },
        {
            "passo": 3,
            "acao": "Oferecer agendamento",
            "check": "cliente quer agendar?",
            "se_nao": "Apenas informe preço"
        }
    ],
    
    "nunca_fazer": [
        "Inventar preço ('acho que é R$50')",
        "Criar promoção ('temos desconto hoje')",
        "Comparar com concorrência",
        "Justificar valor alto/baixo"
    ],
    
    "template_resposta": """
        O {serviço} custa R$ {valor}!
        
        Inclui: {itens_inclusos}
        
        Quer agendar? 😊
    """
}
```

### 4.3 Reclamação

```python
COMPLAINT_FORMULA = {
    "pre_condicoes": [
        "sentiment == negative",
        "urgency >= 4"
    ],
    
    "passos_obrigatorios": [
        {
            "passo": 1,
            "acao": "Validar sentimento negativo",
            "check": "detect_sentiment(message) == negative",
            "se_nao": "Continue fluxo normal"
        },
        {
            "passo": 2,
            "acao": "HANDOFF IMEDIATO",
            "check": "NUNCA tente resolver sozinho",
            "se_nao": "ERRO CRÍTICO - pode piorar situação"
        },
        {
            "passo": 3,
            "acao": "Não argumente, não justifique",
            "check": "0 tentativas de defesa",
            "se_nao": "ERRO - cliente fica mais bravo"
        }
    ],
    
    "nunca_fazer": [
        "Argumentar ('não foi bem assim')",
        "Justificar ('foi por causa de...')",
        "Prometer retorno ('vou ver e te chamo')",
        "Minimizar ('não é tão grave')",
        "Culpar cliente ('você não explicou direito')"
    ],
    
    "template_resposta": """
        Entendi, {nome}. Sinto muito que isso tenha acontecido.
        
        Vou te chamar com a equipe agora mesmo pra resolver isso.
        
        Um minutinho, por favor. 🤝
    """
}
```

---

## 5. Matemática de Agenda Antes da Linguagem

### 5.1 Validação de Agenda (Código Real)

```python
class AgendaValidator:
    """
    Valida agenda ANTES de gerar qualquer linguagem.
    Truth in Data: sem dado real = handoff.
    """
    
    async def validate_and_respond(
        self,
        service: str,
        date: str,
        time_preference: str = None
    ) -> Response:
        # 1. Buscar horários REAIS do Supabase
        available_slots = await self.get_real_slots(
            date=date,
            service_duration=self.get_service_duration(service)
        )
        
        # 2. Filtrar por preferência (se existe)
        if time_preference:
            valid_slots = self.filter_by_preference(
                available_slots,
                time_preference
            )
        else:
            valid_slots = available_slots
        
        # 3. SÓ DEPOIS gerar linguagem
        if not valid_slots:
            # SEM DADOS REAIS → HANDOFF
            return self.handoff_template(
                reason="no_available_slots",
                message="Vou te passar com a equipe pra encontrar um horário!"
            )
        
        # COM DADOS REAIS → GERA RESPOSTA
        return self.response_template(
            slots=valid_slots,  # Dados REAIS do DB
            service=service
        )
    
    async def get_real_slots(self, date: str, duration: int) -> List[str]:
        """
        Busca horários REAIS no Supabase.
        NUNCA invente horários.
        """
        db = get_supabase()
        
        # Buscar agendamentos existentes
        appointments = db.table("appointments") \
            .select("time") \
            .eq("date", date) \
            .eq("status", "confirmed") \
            .execute()
        
        occupied = [apt["time"] for apt in appointments.data or []]
        
        # Gerar horários disponíveis (8h às 20h)
        all_times = [f"{h:02d}:00" for h in range(8, 20)]
        available = [t for t in all_times if t not in occupied]
        
        return available[:10]  # Retorna até 10 horários
    
    def get_service_duration(self, service: str) -> int:
        """
        Duração REAL do serviço (do knowledge_base).
        """
        durations = {
            "escova": 30,
            "unha_simples": 45,
            "unha_gel": 90,
            "blindagem": 120,
            # ... buscar do DB
        }
        return durations.get(service, 60)
```

### 5.2 Ordem de Serviços (Regra de Negócio)

```python
SERVICE_ORDER_RULES = {
    "ordem_obrigatoria": ["unha", "cabelo", "maquiagem"],
    
    "razao": "Maquiagem SEMPRE por último (pode borrar com calor/química)",
    
    "validacao": """
        Se cliente quer múltiplos serviços:
        1. Validar ordem (unha → cabelo → make)
        2. Calcular tempo total (soma das durações)
        3. Verificar se cabe na agenda
        4. Oferecer horários que comportam TUDO
    """,
    
    "exemplo_resposta": """
        Perfeito! Vamos fazer:
        1. Unha de gel (90 min)
        2. Escova (30 min)
        3. Make (45 min)
        
        Tempo total: 2h45
        
        Tenho horário às 14h (termina 16h45)
        ou às 16h (termina 18h45).
        
        Qual prefere? ✨
    """
}
```

---

## 6. Métricas de Qualidade

### 6.1 Avaliação de Resposta (Evolution Engine)

```python
RESPONSE_QUALITY_METRICS = {
    "truth_in_data": {
        "weight": 0.40,  # 40% da nota
        "checks": [
            "preco_existe_no_db",
            "horario_existe_na_agenda",
            "servico_existe_no_knowledge_base",
            "nao_inventou_informacao"
        ],
        "pass_threshold": 1.0,  # 100% obrigatório
        "se_fail": "HANDOFF imediato + flag needs_review"
    },
    
    "brevity_with_warmth": {
        "weight": 0.25,  # 25% da nota
        "checks": [
            "tokens_dentro_do_limite",
            "emojis_na_quantidade_correta",
            "tom_caloroso_mas_profissional",
            "nao_foi_grosseira"
        ],
        "pass_threshold": 0.7  # 70% aceitável
    },
    
    "actionability": {
        "weight": 0.20,  # 20% da nota
        "checks": [
            "resposta_tem_acao_clara",
            "pergunta_objetiva_no_final",
            "nao_deixou_cliente_sem_resposta"
        ],
        "pass_threshold": 0.8  # 80% aceitável
    },
    
    "business_rules": {
        "weight": 0.15,  # 15% da nota
        "checks": [
            "ordem_servicos_respeitada",
            "duracao_calculada_corretamente",
            "blindagem_produto_respeitada"
        ],
        "pass_threshold": 1.0  # 100% obrigatório
    }
}

def calculate_quality_score(response: Response) -> float:
    """
    Calcula score de qualidade (0-100).
    """
    scores = {
        "truth_in_data": check_truth(response),
        "brevity_with_warmth": check_brevity(response),
        "actionability": check_actionability(response),
        "business_rules": check_business_rules(response)
    }
    
    weighted_score = sum(
        scores[metric] * weight
        for metric, weight in RESPONSE_QUALITY_METRICS.items()
    )
    
    # Se truth_in_data falhou ( < 100%), nota final = 0
    if scores["truth_in_data"] < 1.0:
        return 0.0
    
    return weighted_score * 100
```

### 6.2 Critérios de Aprovação no Dojo

```python
DOJO_PASS_CRITERIA = {
    "facil": {
        "min_score": 80,
        "scenarios": ["saudacao", "agradecimento", "localizacao"],
        "max_turns": 5
    },
    
    "medio": {
        "min_score": 75,
        "scenarios": ["agendar_simples", "preco_existe", "servicos"],
        "max_turns": 10
    },
    
    "dificil": {
        "min_score": 70,
        "scenarios": ["agendar_multiplos", "preco_nao_existe", "multiplas_perguntas"],
        "max_turns": 15
    },
    
    "com_pressa": {
        "min_score": 75,
        "scenarios": ["cliente_com_pressa", "agendar_mesmo_dia"],
        "max_turns": 5,
        "max_tokens_per_response": 60
    },
    
    "reclamacao": {
        "min_score": 90,  # Alto porque é crítico
        "scenarios": ["cliente_bravo", "problema_relato"],
        "max_turns": 3,
        "mandatory_handoff": True  # Obrigatório handoff
    }
}
```

---

## 7. Implementação Técnica

### 7.1 Estrutura de Arquivos (Reorganizada - Sem Redundância)

```
LUNA_OS/backend/app/
├── core/
│   ├── brain.py                  # Pipeline de Cognição (5 camadas)
│   │   ├── Classificação de intenção
│   │   ├── Validação de dados (Supabase)
│   │   ├── Construção de contexto (RAG)
│   │   ├── Regras de negócio
│   │   └── Geração de resposta (LLM)
│   │
│   ├── memory.py                 # Estado e contexto
│   │   ├── Client profiles (longo prazo)
│   │   ├── Conversation context (curto prazo)
│   │   └── Business Intelligence
│   │
│   └── evolution.py              # Auditoria e aprendizado
│       ├── Quality audit
│       ├── Maturity scoring
│       └── Learning log
│
├── integrations/
│   ├── evolution_api.py          # API WhatsApp (ferramenta completa)
│   │   ├── send_text()
│   │   ├── send_location()
│   │   ├── send_media()
│   │   ├── get_qr_code()
│   │   ├── fetch_contacts()
│   │   └── connection_status()
│   │
│   ├── supabase_client.py        # Banco de dados
│   └── openrouter.py             # LLM Gateway
│
├── knowledge/
│   ├── loader.py                 # RAG (serviços, FAQ, profissionais)
│   └── luna_config_cache.json    # ⚠️ REMOVIDO: Personalidade vai para brain.py
│
└── config.py                     # ⚠️ REMOVIDO: Personalidade vai para brain.py
    └── Apenas: URLs, chaves, modelos
```

**Princípios de Organização:**

| Componente | Responsabilidade | O Que Guarda |
|------------|------------------|--------------|
| `brain.py` | **Cognição + Personalidade** | System prompt, identidade Luna, regras de tom |
| `knowledge/loader.py` | **Dados do Negócio** | Serviços, preços, FAQ, profissionais (Supabase) |
| `integrations/evolution_api.py` | **Ferramenta WhatsApp** | API completa, sem redundância com conexões |
| `config.py` | **Configuração Técnica** | URLs, chaves, modelos (NADA de personalidade) |

### 7.2 System Prompt (Embutido no brain.py)

**Localização Correta**: `brain.py` (NÃO em config.py ou knowledge)

```python
# LUNA_OS/backend/app/core/brain.py

SYSTEM_PROMPT = """
<layer1_identity>
Você é Luna, a alma da recepção da Haven Escovaria & Esmalteria.
Sua voz é calorosa, profissional e tipicamente de Chapecó-SC.
</layer1_identity>

<layer2_context>
Atendimento via WhatsApp.
Cliente Atual: {client_name}
Histórico: {history_summary}
Local: Chapecó-SC (Jardim Itália)
</layer2_context>

<layer3_rules>
⚠️ BLINDAGEM ANTI-ALUCINAÇÃO ⚠️

REGRAS DE OURO:
1. NUNCA invente preços, horários, ou informações que não estão no knowledge_base
2. NUNCA diga "vou verificar" — se não tem a informação, ofereça handoff
3. NUNCA prometa que vai retornar — isso é handoff
4. Se precisa consultar alguém → HANDOFF, não promessa

ORDEM DE SERVIÇOS:
• Unha → Cabelo → Maquiagem (sempre)
• Maquiagem POR ÚLTIMO (pode borrar)

TOM E BREVIDADE:
• 1-3 emojis por mensagem
• Nome do cliente quando souber
• Direta com pressa, calorosa sem pressa
</layer3_rules>

<layer4_knowledge>
{context}  # Contexto RAG (serviços, FAQ, profissionais)
</layer4_knowledge>

<layer5_output>
Fale de forma natural e breve.
Se o cliente quiser marcar, colete: Serviço, Data/Hora e Profissional.

IMPORTANTE: Toda resposta deve ter análise de inteligência oculta:
---RESPONSE---
Sua resposta empática para a cliente.
---INTELLIGENCE---
{{
  "insight": "...",
  "objections": [...],
  "customer_mood": "happy|frustrated|hesitant|hurry",
  "urgency_level": 1-5,
  "potential_value": "high|medium|low"
}}
</layer5_output>
"""
```

**Por Que no brain.py?**

| Local | Problema | Solução |
|-------|----------|---------|
| `config.py` | Mistura personalidade com URLs/chaves | ❌ Separar: config = técnico |
| `knowledge/` | Mistura identidade com dados do negócio | ❌ Separar: knowledge = fatos |
| `brain.py` | **Cognição + Identidade** | ✅ **Local correto** |

**Identidade da Luna = Parte do Processo Cognitivo**

```python
# brain.py

class BrainEngine:
    """
    Pipeline de Cognição da LUNA

    A personalidade NÃO é configuração — é parte do processo de pensamento.
    """

    def build_system_prompt(self, client, context):
        """
        Constrói system prompt COM identidade embutida.
        Identidade + Contexto + Regras = Personalidade
        """
        return SYSTEM_PROMPT.format(
            client_name=client.get("name"),
            history_summary=self.get_history_summary(client),
            context=context  # RAG do knowledge_loader
        )
```

### 7.4 Evolution API (Ferramenta WhatsApp Completa)

**Localização**: `integrations/evolution_api.py` (NÃO redundante com conexões)

**Princípio**: Uma única ferramenta completa, não duplicar com `/connections`

```python
# LUNA_OS/backend/app/integrations/evolution_api.py

from httpx import AsyncClient

class EvolutionAPI:
    """
    Ferramenta completa para WhatsApp via Evolution API.

    NÃO criar redundância com /connections — esta é a ÚNica ferramenta.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"apikey": api_key}

    # ==================== MENSAGENS ====================

    async def send_text(self, instance: str, phone: str, message: str):
        """
        Envia mensagem de texto.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendText/{instance}",
                headers=self.headers,
                json={
                    "number": phone,
                    "text": message,
                    "delay": 1200
                }
            )
            return response.json()

    async def send_location(self, instance: str, phone: str, lat: float, lng: float, name: str, address: str):
        """
        Envia localização.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendLocation/{instance}",
                headers=self.headers,
                json={
                    "number": phone,
                    "latitude": lat,
                    "longitude": lng,
                    "name": name,
                    "address": address
                }
            )
            return response.json()

    async def send_media(self, instance: str, phone: str, media_url: str, caption: str = ""):
        """
        Envia imagem/vídeo.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendMedia/{instance}",
                headers=self.headers,
                json={
                    "number": phone,
                    "mediatype": "image",
                    "media": media_url,
                    "caption": caption
                }
            )
            return response.json()

    # ==================== CONEXÃO ====================

    async def get_qr_code(self, instance: str):
        """
        Obtém QR Code para conexão.
        """
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/instance/connect/{instance}",
                headers=self.headers
            )
            return response.json()

    async def connection_status(self, instance: str):
        """
        Verifica status da conexão.
        """
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/instance/connectionState/{instance}",
                headers=self.headers
            )
            return response.json()

    async def fetch_contacts(self, instance: str):
        """
        Busca contatos do WhatsApp.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/findAll/{instance}",
                headers=self.headers
            )
            return response.json()

    # ==================== UTILITÁRIOS ====================

    async def delete_instance(self, instance: str):
        """
        Remove instância.
        """
        async with AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/instance/delete/{instance}",
                headers=self.headers
            )
            return response.json()

    async def logout(self, instance: str):
        """
        Logout da instância.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/instance/logout/{instance}",
                headers=self.headers
            )
            return response.json()


# Singleton
evolution = EvolutionAPI(
    base_url=settings.evolution_url,
    api_key=settings.evolution_key
)
```

**Por Que Não Redundar com /connections?**

| Abordagem | Problema | Solução |
|-----------|----------|---------|
| `/connections` + `evolution_tools.py` | Duplica funcionalidade | ❌ **Não fazer** |
| `integrations/evolution_api.py` | **Única ferramenta completa** | ✅ **Fazer isso** |

**Fluxo Correto:**

```
┌─────────────────────────────────────────────────────────────┐
│  API: /connections (Frontend)                               │
│  • Status da conexão                                        │
│  • QR Code                                                  │
│  • Informações da instância                                 │
│  ↓                                                          │
│  Usa: integrations/evolution_api.py                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  API: /webhooks (Evolution → Backend)                       │
│  • Recebe mensagens                                         │
│  • Envia mensagens (via evolution_api.py)                   │
│  ↓                                                          │
│  Usa: integrations/evolution_api.py                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BRAIN: brain.py (Respostas)                                │
│  • Gera resposta                                            │
│  • Envia (via evolution_api.py)                            │
│  ↓                                                          │
│  Usa: integrations/evolution_api.py                         │
└─────────────────────────────────────────────────────────────┘

✅ TODOS usam a MESMA ferramenta: evolution_api.py
❌ NÃO criar evolution_tools.py separado
```

```python
class LunaCognitivePipeline:
    """
    Pipeline de Cognição da LUNA
    Implementação das 5 camadas + auditoria
    """
    
    async def process_message(
        self,
        phone: str,
        name: str,
        message: str,
        history: List[Dict] = None
    ) -> Dict:
        start_time = time.time()
        
        # CAMADA 1: Intenção
        intent, confidence = self.classify_intent(message)
        
        # CAMADA 2: Validação de Dados
        validated_data = await self.validate_data(intent)
        if not validated_data:
            return self.handoff_response("Sem dados reais")
        
        # CAMADA 3: Contexto RAG
        context = await self.build_context(intent, validated_data)
        
        # CAMADA 4: Regras de Negócio
        rules = self.apply_business_rules(intent, context)
        
        # CAMADA 5: Geração de Resposta
        response = await self.generate_response(
            intent=intent,
            context=context,
            rules=rules,
            validated_data=validated_data
        )
        
        # CAMADA 6: Auditoria
        audit_result = await self.audit_response(response)
        
        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "audit": audit_result,
            "processing_ms": int((time.time() - start_time) * 1000)
        }
```

---

## 8. Avaliação no Dojo Arena

### 8.1 Cenários de Teste

```python
DOJO_SCENARIOS = {
    "facil": [
        {
            "name": "Saudação Simples",
            "message": "Oi, bom dia!",
            "expected_intent": "saudacao",
            "expected_behavior": "resposta_curta_calorosa",
            "max_turns": 3
        },
        {
            "name": "Pedido de Localização",
            "message": "Onde fica?",
            "expected_intent": "localizacao",
            "expected_behavior": "envia_endereco",
            "max_turns": 2
        }
    ],
    
    "medio": [
        {
            "name": "Agendamento Simples",
            "message": "Quero agendar uma escova pra amanhã",
            "expected_intent": "agendar",
            "expected_behavior": "oferece_horarios_reais",
            "max_turns": 8
        },
        {
            "name": "Pedido de Preço",
            "message": "Quanto custa unha de gel?",
            "expected_intent": "preco",
            "expected_behavior": "informa_preco_se_existe_ou_handoff",
            "max_turns": 5
        }
    ],
    
    "dificil": [
        {
            "name": "Múltiplos Serviços",
            "message": "Quero fazer unha, cabelo e make pro casamento",
            "expected_intent": "agendar_multi_servico",
            "expected_behavior": "respeita_ordem_unha_cabelo_make",
            "max_turns": 15
        },
        {
            "name": "Preço Não Existe",
            "message": "Quanto custa blindagem com cronograma?",
            "expected_intent": "preco",
            "expected_behavior": "handoff_imediato",
            "max_turns": 3
        }
    ],
    
    "com_pressa": [
        {
            "name": "Cliente com Pressa",
            "message": "Preciso de um horário HOJE, é urgente!",
            "expected_intent": "agendar",
            "expected_behavior": "resposta_direta_max_60_tokens",
            "max_turns": 5,
            "max_tokens_per_response": 60
        }
    ],
    
    "reclamacao": [
        {
            "name": "Cliente Bravo",
            "message": "Isso é um absurdo! Fiz as unhas e já descascou!",
            "expected_intent": "reclamacao",
            "expected_behavior": "handoff_imediato_sem_argumentar",
            "max_turns": 2,
            "mandatory_handoff": True
        }
    ]
}
```

### 8.2 Critérios de Aprovação

```python
DOJO_EVALUATION = {
    "scoring": {
        "truth_in_data": {
            "weight": 0.40,
            "auto_fail_if": "hallucinated_price_or_schedule"
        },
        "brevity_with_warmth": {
            "weight": 0.25,
            "checks": ["token_count", "emoji_count", "tone"]
        },
        "actionability": {
            "weight": 0.20,
            "checks": ["clear_next_step", "objective_question"]
        },
        "business_rules": {
            "weight": 0.15,
            "auto_fail_if": "wrong_service_order"
        }
    },
    
    "pass_criteria": {
        "facil": {"min_score": 80, "max_turns": 5},
        "medio": {"min_score": 75, "max_turns": 10},
        "dificil": {"min_score": 70, "max_turns": 15},
        "com_pressa": {"min_score": 75, "max_tokens": 60},
        "reclamacao": {"min_score": 90, "mandatory_handoff": True}
    },
    
    "maturity_threshold": {
        "ready_for_production": 75,  # Score mínimo para ativar
        "observe_mode": 50,  # Score para modo observe
        "not_ready": 0  # Abaixo disso, não ativa
    }
}
```

---

## 📚 Referências

- **AGENT_FLOW.md** — Fluxo de agentes MCT
- **brain.py** — Implementação atual do pipeline
- **evolution.py** — Auditoria e métricas
- **system.md** — Identidade e regras da Luna

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Documento criado: 2026-02-27*
