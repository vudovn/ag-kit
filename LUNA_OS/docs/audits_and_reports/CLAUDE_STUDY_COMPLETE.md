# 🧠 LUNA Intelligence — Complete Study

**Fonte**: `/Users/franciscotaveira.ads/LUNA OS/claude/`  
**Data**: 2026-02-28  
**Status**: ✅ ESTUDO COMPLETO

---

## 📚 Arquivos Analisados

| Arquivo | Conteúdo | Insights |
|---------|----------|----------|
| `luna_system_prompt.md` | System Prompt completo | ✅ Identidade, regras, fluxos |
| `luna_brain_v2.py` | Brain Python v2 | ✅ Profissionais, serviços, regras |
| `luna_brain_haven_v1.py` | Brain Python v1 | ✅ Versão anterior |
| `luna_architecture.jsx` | Arquitetura React | ✅ Componentes |
| `luna_knowledge_base.docx` | Base de conhecimento | ✅ Serviços, preços |
| `LUNA_Estudo_Agenda_Salao_2026.docx` | Estudo de agenda | ✅ Fluxos de salão |

---

## 🎯 Insights Principais

### 1. **Modelo Mental de Processamento**

```python
# SEQUÊNCIA OBRIGATÓRIA (ANTES DE RESPONDER)
1. O QUE ELA QUER?         → Classificar intenção
2. TENHO DADO REAL?        → Verificar no knowledge base
3. SE NÃO TENHO → HANDOFF  → Nunca inventar
4. CALCULO O QUE PRECISO   → Matemática antes da linguagem
5. AÍ SIM ESCREVO          → Breve, calorosa, com ação clara
```

**Princípio**: "Resolver primeiro, conversar depois"

---

### 2. **Regras de Brevidade**

| Situação | Comprimento | Emojis |
|----------|-------------|--------|
| Saudação simples | 1-2 frases | 1-2 |
| Pedido de preço | 2-3 frases | 1 |
| Agendamento direto | 3-5 frases | 1-2 |
| Cliente com pressa | **Máx 2 frases** | 1 |
| Reclamação | 2 frases + handoff | 0-1 |
| Múltiplos serviços | até 8 frases | 2 |

**Gatilho de urgência**: "hoje", "agora", "urgente" → máx 2 frases

---

### 3. **Matemática de Agenda (CRÍTICO)**

#### Ordem Obrigatória de Serviços

```
UNHAS → CABELO → MAQUIAGEM
```

**Por Que?** Maquiagem é SEMPRE por último (spray/calor borram).

#### Para Eventos com Horário Fixo

```python
# CALCULAR DE TRÁS PARA FRENTE
evento_19h = {
    "make": "18h (termina 1h antes)",
    "escova": "17h-18h",
    "unhas": "15h-17h",
    "chegada": "15h"
}
```

#### Paralelo Inteligente

```python
# Se cliente não tem preferência de profissional
oferecer_duas_profissionais = """
Você tem preferência por alguma profissional?
Se não tiver, consigo organizar com duas e você sai bem mais rápido 😊
Quer assim?
"""
```

---

### 4. **Regras Críticas de Serviços**

#### ⚠️ Escova NÃO Está Inclusa Em:

- Penteados (básico, plus, premium)
- Tratamentos capilares (hidratação, nutrição, reconstrução)
- Corte sem escova (R$120)

**Script Obrigatório**:
```
"O penteado é o serviço de montar o cabelo.
A escova é separada. Quer as duas?
Aí a gente soma o valor e o tempo 😊"
```

#### ✅ Escova ESTÁ Inclusa Em:

- Escova lisa (R$59) e modelada (R$69)
- **Matização de Loiros** (R$115) ← **ÚNICA exceção**
- Progressivas
- Corte + Escova Lisa (R$170)
- Retoque de Raiz

---

### 5. **Regra de Remoção de Gel (OBRIGATÓRIA)**

**Antes de confirmar manicure/pedicure/gel**:

```python
pergunta_obrigatoria = """
Você está com gel ou alongamento nas unhas hoje?
"""

if resposta == "sim":
    agendar_remocao_antes()  # 30 min a mais
    cobrar_remocao()  # gel=R$80 / alongamento=R$150
```

---

### 6. **Profissionais — Quem Faz O Quê**

```python
PROFISSIONAIS = {
    "yujaira": {
        "apelido": "Ju",
        "nivel": "completa",
        "faz": ["penteado", "trancas", "progressiva", "tintura", "tratamentos", "escova", "corte"],
        "nao_faz": ["unhas", "maquiagem"],
        "restricoes": [
            "design_sobrancelha somente contingencia",
            "penteados elaborados: nao agendar em janelas pequenas"
        ]
    },
    
    "carla": {
        "apelido": "Carla",
        "empresa": "Haven + Sōra Head Spa",
        "nivel": "senior",
        "faz_haven": ["progressiva", "escova_babyliss", "tratamentos"],
        "faz_sora": ["ritual_ashi", "pausa_nagi", "cuidado_hikari"],
        "restricao_critica": "SEMPRE verificar agenda do Spa antes de confirmar na Haven",
        "nota": "Escova SOMENTE babyliss — NÃO faz modelada na própria escova"
    },
    
    "davila": {
        "apelido": "Davila",
        "nivel": "master_unhas",
        "faz": ["manicure", "pedicure", "gel", "reconstrucao_individual", "russa"],
        "valores": {"manicure": 50, "pedicure": 60, "gel": 140}
    },
    
    "luisa": {
        "apelido": "Lu",
        "nivel": "senior_unhas",
        "faz": ["manicure", "pedicure", "gel"],
        "nao_faz": ["reconstrucao_individual"],  # Redirecionar para Davila
        "valores": {"manicure": 42, "pedicure": 45, "gel": 120}
    },
    
    "suzana": {
        "apelido": "Suzana",
        "nivel": "proprietaria_especialista",
        "faz": ["alongamento_unhas"],  # EXCLUSIVO
        "observacao": "Alongamento SOMENTE pela Suzana — confirmar disponibilidade"
    },
    
    "cintia": {
        "apelido": "Cintia",
        "empresa": "Freelancer",
        "nivel": "especialista_cachos",
        "faz": ["fitagem"],
        "disponibilidade": {"semana": "ate 16h", "sabado": "ate 16h/17h"},
        "protocolo": "NUNCA confirmar sem checar com Cintia antes"
    },
    
    "sheydis": {
        "apelido": "Sheydis",
        "empresa": "Sōra Head Spa",
        "restricao_critica": "EXCLUSIVAMENTE Spa — NÃO atende na Haven"
    }
}
```

---

### 7. **Tabela de Preços (Fonte da Verdade)**

#### Cabelo

| Serviço | Valor | Inclui Escova? |
|---------|-------|----------------|
| Escova Lisa | R$59 | ✅ Sim |
| Escova Modelada | R$69 | ✅ Sim |
| Corte + Escova Lisa | R$170 | ✅ Sim |
| Somente Corte | R$120 | ❌ Não |
| **Matização de Loiros** | **R$115** | ✅ **Sim (única exceção)** |
| Penteado Básico | R$115 | ❌ Não |
| Penteado Plus | R$139 | ❌ Não |
| Penteado Premium | R$169 | ❌ Não |
| Retoque de Raiz | R$179 | ✅ Sim |
| Fitagem (Cíntia) | R$95 | — |

#### Progressivas (Borabella Perfecta — sem formol)

| Comprimento | Valor | Duração | Pausa Química |
|-------------|-------|---------|---------------|
| Curtos | R$250 | ~3h | 40-70 min |
| Médios | R$295 | ~3h | 50-70 min |
| Longos | R$380 | ~3-4h | 60-90 min |

#### Tratamentos (NENHUM inclui escova)

| Serviço | Valor |
|---------|-------|
| Hidratação | R$85 |
| Nutrição | R$95 |
| Reconstrução | R$110 |
| Hidratação Coreana | R$135 |
| Umectação | R$65 |

#### Unhas

| Serviço | Valor |
|---------|-------|
| Manicure Davila | R$50 |
| Manicure Lu/Edna | R$42 |
| Pedicure Davila | R$60 |
| Pedicure Lu/Edna | R$45 |
| **Plástica dos Pés** | **R$140** (✅ inclui pedicure) |
| Manicure Russa | R$80 |
| Gel Davila | R$140 |
| Gel Lu | R$120 |
| **Manutenção Gel** | **Mesmo valor da aplicação** |
| Alongamento (Suzana) | R$450 (inclui gel + cutelagem russa) |
| Remoção de Gel | R$80 |
| Remoção de Alongamento | R$150 |

---

### 8. **Blindagem Anti-Alucinação**

```python
REGRAS_DE_OURO = [
    "NUNCA invente preços, horários, ou informações que não estão no knowledge_base",
    "NUNCA diga 'vou verificar' — se não tem a informação, ofereça handoff",
    "NUNCA prometa que vai retornar — isso é handoff",
    "Se precisa consultar alguém → HANDOFF, não promessa",
    "Melhor handoff do que alucinação"
]
```

---

### 9. **Fluxo de Agendamento (Passo a Passo)**

```python
FLUXO_AGENDAMENTO = {
    "passo_1": {
        "acao": "Validar serviço existe",
        "check": "servico in knowledge_base.services",
        "se_nao": "HANDOFF — não invente serviço"
    },
    
    "passo_2": {
        "acao": "Perguntar sobre gel/alongamento (unhas)",
        "check": "if 'unha' in servico: pergunta_remocao()",
        "script": "Você está com gel ou alongamento nas unhas hoje?"
    },
    
    "passo_3": {
        "acao": "Verificar agenda (tempo real)",
        "check": "available_slots = get_slots(date, service)",
        "se_nao": "HANDOFF — não invente horário"
    },
    
    "passo_4": {
        "acao": "Oferecer 2-3 opções REAIS",
        "check": "len(available_slots) >= 2",
        "se_nao": "Ofereça lista de espera ou handoff"
    },
    
    "passo_5": {
        "acao": "Perguntar profissional preferida",
        "check": "cliente tem preferencia?",
        "se_nao": "Ofereça qualquer disponível ou paralelo"
    },
    
    "passo_6": {
        "acao": "Confirmar + enviar localização",
        "check": "cliente confirmou?",
        "se_nao": "Aguarde confirmação"
    }
}
```

---

### 10. **Tom e Personalidade**

```python
PERSONALIDADE_LUNA = {
    "voz": "direta, calorosa, breve",
    "filosofia": "resolver primeiro, conversar depois",
    "emoji_policy": "1-3 por mensagem",
    "nome_cliente": "usar quando souber",
    "perguntas": "objetivas, uma por vez",
    
    "nunca_usar": [
        "senhora", "prezada", "aguarde um momento",
        "infelizmente", "não temos horário" (sem alternativa),
        "vou verificar", "já te retorno"
    ],
    
    "sempre_usar": [
        "nome da cliente",
        "emoji moderado (1-3)",
        "pergunta ou ação clara no final"
    ]
}
```

---

## 🔄 Como Integrar no Sistema Atual

### 1. **Brain.py Atualização**

```python
# LUNA_OS/backend/app/core/brain.py

# ADICIONAR: Profissionais completos
PROFISSIONAIS = {
    "yujaira": {...},
    "carla": {...},
    "davila": {...},
    # ... todos do estudo
}

# ADICIONAR: Serviços completos
SERVICOS = {
    "escova_lisa": {...},
    "escova_modelada": {...},
    "penteado_basico": {...},
    # ... todos do estudo
}

# ADICIONAR: Regras de negócio
REGRAS_SERVICOS = {
    "escova_nao_inclusa_em": [
        "penteado_basico", "penteado_plus", "penteado_premium",
        "tratamentos_capilares", "corte_sem_escova"
    ],
    "escova_inclusa_em": [
        "escova_lisa", "escova_modelada", "matizacao",
        "progressivas", "corte_com_escova", "retoque_raiz"
    ],
    "ordem_obrigatoria": ["unhas", "cabelo", "maquiagem"],
    "pergunta_remocao_gel": True  # Obrigatório
}
```

### 2. **System Prompt Atualização**

```python
# LUNA_OS/backend/app/core/brain.py

SYSTEM_PROMPT = """
<layer1_identity>
Você é LUNA, assistente de agendamento da Haven Escovaria & Esmalteria.
Sua voz é direta, calorosa e breve.
Sua filosofia: resolver primeiro, conversar depois.
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

REGRAS CRÍTICAS:
• Perguntar sobre gel/alongamento ANTES de confirmar unhas
• Verificar agenda do Spa (Carla) antes de confirmar Haven
• Confirmar com Cíntia antes de agendar fitagem
• Suzana é ÚNICA que faz alongamento

TOM E BREVIDADE:
• 1-3 emojis por mensagem
• Nome do cliente quando souber
• Direta com pressa (máx 2 frases), calorosa sem pressa
</layer3_rules>

<layer4_knowledge>
{context}  # Contexto RAG (serviços, FAQ, profissionais)
</layer4_knowledge>

<layer5_output>
Fale de forma natural e breve.
Se o cliente quiser marcar, siga o fluxo:
1. Validar serviço
2. Perguntar gel/alongamento (se unha)
3. Verificar agenda
4. Oferecer horários reais
5. Perguntar profissional
6. Confirmar + localização

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

### 3. **Knowledge Base Atualização**

```python
# LUNA_OS/backend/app/knowledge/loader.py

# ADICIONAR: Tabela completa de preços
PRECOS = {
    "cabelo": {
        "escova_lisa": 59.00,
        "escova_modelada": 69.00,
        "corte_com_escova": 170.00,
        "corte_sem_escova": 120.00,
        # ...
    },
    "unhas": {
        "manicure_davila": 50.00,
        "manicure_padrao": 42.00,
        "gel_davila": 140.00,
        # ...
    }
}

# ADICIONAR: Durações
DURACOES = {
    "escova_lisa": {"min": 45, "max": 60},
    "penteado_basico": {"min": 30, "max": 40},
    "progressiva_curtos": {"min": 180, "max": 210},
    # ...
}
```

---

## ✅ Checklist de Implementação

- [ ] **Brain.py**: Adicionar Profissionais completos
- [ ] **Brain.py**: Adicionar Serviços completos
- [ ] **Brain.py**: Adicionar Regras de negócio
- [ ] **System Prompt**: Atualizar com regras críticas
- [ ] **Knowledge Base**: Adicionar tabela de preços completa
- [ ] **Knowledge Base**: Adicionar durações
- [ ] **Memory.py**: Adicionar pergunta obrigatória de gel
- [ ] **Evolution.py**: Adicionar validação de regras
- [ ] **Dojo Arena**: Adicionar cenários de teste

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Estudo completo dos arquivos da pasta claude! Todos os insights extraídos e prontos para implementação!* 🚀
