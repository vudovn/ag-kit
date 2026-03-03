# 🥋 DOJO ARENA - GUIA COMPLETO

**Data:** 2026-03-01  
**Status:** ✅ **OPERACIONAL NO PAINEL**

---

## 📊 RESUMO EXECUTIVO

O **Dojo Arena** é o ambiente de **treinamento e teste da LUNA** onde você pode simular conversas com diferentes tipos de clientes e cenários para avaliar e melhorar o desempenho da IA.

**Disponível no painel:** `http://localhost:3000/dojo` ✅

---

## 🎯 O QUE PODE SER FEITO NO DOJO

### 1. 🧪 TESTAR CENÁRIOS

**15 Cenários Disponíveis:**

| ID | Nome | Nível | Descrição | Pontos |
|----|------|-------|-----------|--------|
| `scenario_001` | Saudação Simples | 🟢 Beginner | "Oi! Bom dia!" | 10 |
| `scenario_002` | Pergunta de Horário | 🟢 Beginner | "Qual o horário de vocês?" | 10 |
| `scenario_003` | Pergunta de Localização | 🟢 Beginner | "Onde fica o salão?" | 10 |
| `scenario_004` | Pergunta de Preço | 🟢 Beginner | "Quanto custa uma escova?" | 15 |
| `scenario_005` | Agendamento Simples | 🟢 Beginner | "Quero agendar uma escova" | 20 |
| `scenario_006` | Múltiplos Serviços | 🟡 Intermediate | "Unha e escova" | 25 |
| `scenario_007` | Objeção de Preço | 🟡 Intermediate | "Achei caro..." | 25 |
| `scenario_008` | Dúvida de Serviço | 🟡 Intermediate | "Qual você recomenda?" | 20 |
| `scenario_009` | Cliente Apres sada | 🟡 Intermediate | "Preciso pra hoje!" | 25 |
| `scenario_010` | Elogio | 🟡 Intermediate | "Amei o resultado!" | 15 |
| `scenario_011` | Reclamação | 🔴 Advanced | "Não gostei do serviço" | 30 |
| `scenario_012` | Handoff | 🔴 Advanced | "Quero falar com humano" | 30 |
| `scenario_013` | Cancelamento | 🔴 Advanced | "Preciso cancelar" | 30 |
| `scenario_014` | Retorno | 🔴 Advanced | "Quero voltar mas..." | 35 |
| `scenario_015` | Indicação | 🟣 Expert | "Vou indicar amigas" | 40 |

**Como testar:**
1. Acessar `http://localhost:3000/dojo`
2. Selecionar cenário
3. Clicar em "Testar"
4. Ver resposta da LUNA e métricas

---

### 2. 👥 SELECIONAR PERSONAS

**8 Personas Disponíveis:**

| ID | Nome | Humor | Emoji | Dificuldade |
|----|------|-------|-------|-------------|
| `persona_001` | Cliente Apressada | 🔥 Hurry | 🔥 | Fácil |
| `persona_002` | Cliente Sensível a Preço | 💰 Hesitant | 💰 | Média |
| `persona_003` | Cliente Insatisfeita | 😤 Frustrated | 😤 | Difícil |
| `persona_004` | Cliente Feliz | 😊 Happy | 😊 | Fácil |
| `persona_005` | Cliente Indecisa | 🤔 Hesitant | 🤔 | Média |
| `persona_006` | Cliente Exigente | 💅 Frustrated | 💅 | Difícil |
| `persona_007` | Cliente Primeira Vez | 🌟 Happy | 🌟 | Média |
| `persona_008` | Cliente Fidelizada | 💜 Happy | 💜 | Fácil |

**Cada persona tem:**
- Frases típicas
- Gatilhos específicos
- Dicas de sucesso

---

### 3. 📊 VER MÉTRICAS DE DESEMPENHO

**Métricas Avaliadas:**

| Métrica | Descrição | Peso |
|---------|-----------|------|
| **Empatia** | LUNA demonstrou compreensão? | 30% |
| **Clareza** | Resposta foi clara e objetiva? | 25% |
| **Acionabilidade** | Ofereceu ação/próximo passo? | 25% |
| **Tom Adequado** | Usou tom adequado ao humor? | 20% |

**Resultado:**
- ✅ Success (≥80%)
- ⚠️ Partial (50-79%)
- ❌ Failed (<50%)

---

### 4. 💰 GANHAR PONTOS

**Sistema de Pontuação:**

| Resultado | Pontos |
|-----------|--------|
| ✅ Success (Beginner) | 10-20 |
| ✅ Success (Intermediate) | 25-35 |
| ✅ Success (Advanced) | 40-50 |
| ✅ Success (Expert) | 55-70 |
| ⚠️ Partial | 50% dos pontos |
| ❌ Failed | 0 pontos |

**Ranking:**
- 🥉 Bronze: 0-100 pontos
- 🥈 Prata: 101-500 pontos
- 🥇 Ouro: 501-1000 pontos
- 💎 Diamante: 1000+ pontos

---

### 5. 📝 DAR FEEDBACK

**Após cada teste, você pode:**
- ⭐ Dar rating (1-5 estrelas)
- 💬 Adicionar comentário
- 📊 Ver métricas detalhadas

**Feedback é usado para:**
- Melhorar prompts da LUNA
- Ajustar pesos das métricas
- Identificar padrões de erro

---

### 6. 📈 ACOMPANHAR HISTÓRICO

**Histórico de Testes:**
- Últimos 10 testes
- Taxa de sucesso
- Pontos ganhos
- Evolução por nível

**Estatísticas:**
- Total de testes
- Melhor cenário
- Pior cenário
- Persona mais difícil

---

## 🖥️ PAINEL DOJO (FRONTEND)

### Status: ✅ **OPERACIONAL**

**URL:** `http://localhost:3000/dojo`

### Funcionalidades do Painel

#### 1. Header Hero
- Título "Dojo Arena 🥋"
- Badge "NOVO"
- Ícone de espadas cruzadas

#### 2. Seleção de Cenários
- Lista todos os 15 cenários
- Filtro por nível (beginner, intermediate, advanced, expert)
- Mostra descrição, pontos e critérios de sucesso

#### 3. Seleção de Personas
- 8 personas com emoji e descrição
- Mostra humor e dificuldade
- Dicas de sucesso para cada uma

#### 4. Área de Teste
- Campo de mensagem customizada
- Botão "Testar"
- Loading state durante teste

#### 5. Resultados
- Resposta da LUNA
- Intent detectada
- Score de confiança
- Tempo de processamento
- Métricas (empatia, clareza, acionabilidade)
- Success/Fail
- Pontos ganhos

#### 6. Feedback
- Rating de 1-5 estrelas
- Botões de feedback rápido
- Campo de comentário

#### 7. Histórico
- Últimos 10 testes
- Evolução em tempo real
- Gráficos de desempenho

---

## 🔌 API ENDPOINTS

### Base URL: `http://localhost:8000/api/dojo`

#### GET `/scenarios`
Lista todos os cenários disponíveis.

```bash
curl http://localhost:8000/api/dojo/scenarios
```

**Response:**
```json
{
  "total": 15,
  "scenarios": [...]
}
```

#### GET `/scenarios/{scenario_id}`
Detalhes de um cenário específico.

```bash
curl http://localhost:8000/api/dojo/scenarios/scenario_001
```

#### GET `/personas`
Lista todas as personas disponíveis.

```bash
curl http://localhost:8000/api/dojo/personas
```

**Response:**
```json
{
  "total": 8,
  "personas": [...]
}
```

#### POST `/test`
Executa um teste no Dojo.

```bash
curl -X POST http://localhost:8000/api/dojo/test \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "scenario_001",
    "persona_id": "persona_001",
    "message": "Oi! Bom dia!"
  }'
```

**Response:**
```json
{
  "scenario_name": "Saudação Simples",
  "persona_name": "Cliente Apressada",
  "user_message": "Oi! Bom dia!",
  "luna_response": "Bom dia! Como posso ajudar?",
  "intent_detected": "saudacao",
  "confidence_score": 0.95,
  "processing_time_ms": 234,
  "metrics": {
    "empathy_score": 0.9,
    "clarity_score": 0.95,
    "actionability_score": 0.85,
    "overall_success": true
  },
  "success": true,
  "points_earned": 10
}
```

#### POST `/feedback`
Envia feedback de um teste.

```bash
curl -X POST http://localhost:8000/api/dojo/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "scenario_001",
    "persona_id": "persona_001",
    "rating": 5,
    "comment": "Perfeito!"
  }'
```

#### GET `/metrics/summary`
Retorna resumo das métricas de desempenho.

```bash
curl http://localhost:8000/api/dojo/metrics/summary
```

---

## 🎮 COMO USAR (PASSO A PASSO)

### Teste Rápido

1. **Acessar:** `http://localhost:3000/dojo`
2. **Selecionar Cenário:** "Saudação Simples"
3. **Selecionar Persona:** "Cliente Apressada"
4. **Clicar em "Testar"**
5. **Ver Resultado:**
   - Resposta da LUNA
   - Métricas
   - Pontos ganhos

### Teste Customizado

1. **Acessar:** `http://localhost:3000/dojo`
2. **Selecionar Cenário:** Qualquer um
3. **Selecionar Persona:** Qualquer um
4. **Digitar Mensagem Customizada:** "Sua mensagem aqui"
5. **Clicar em "Testar"**
6. **Analisar Resultado**

### Dar Feedback

1. **Após teste,** ver resultado
2. **Clicar em estrelas** (1-5)
3. **Opcional:** Adicionar comentário
4. **Enviar**

---

## 📊 MÉTRICAS DETALHADAS

### Empathy Score (0-100%)

**Calculado baseado em:**
- Palavras de compreensão ("entendo", "compreendo")
- Validação de sentimentos ("sei como é")
- Tom acolhedor (emoji, expressões)

**Fórmula:**
```python
empathy_keywords = ["entendo", "compreendo", "sei", "sinto", "imagino"]
score = (matches / total_keywords) * 100
```

### Clarity Score (0-100%)

**Calculado baseado em:**
- Frases curtas (<20 palavras)
- Informação direta
- Sem ambiguidade

**Fórmula:**
```python
avg_sentence_length = total_words / total_sentences
score = max(0, 100 - (avg_sentence_length - 15) * 5)
```

### Actionability Score (0-100%)

**Calculado baseado em:**
- Call-to-action presente
- Próximo passo claro
- Oferta de ajuda

**Fórmula:**
```python
action_keywords = ["posso", "quer", "agendar", "marcar", "ajudar"]
score = (matches / total_keywords) * 100
```

### Overall Success

**Critérios:**
- ✅ Success: ≥80% em todas métricas
- ⚠️ Partial: 50-79% em alguma métrica
- ❌ Failed: <50% em alguma métrica

---

## 🏆 ESTRATÉGIAS DE TREINAMENTO

### Nível 1: Beginner (0-100 pontos)

**Foco:**
- Dominar saudações
- Responder perguntas básicas
- Usar tom adequado

**Cenários recomendados:**
- `scenario_001` - Saudação Simples
- `scenario_002` - Pergunta de Horário
- `scenario_003` - Pergunta de Localização

### Nível 2: Intermediate (101-500 pontos)

**Foco:**
- Lidar com objeções
- Vender pacotes
- Gerenciar tempo

**Cenários recomendados:**
- `scenario_006` - Múltiplos Serviços
- `scenario_007` - Objeção de Preço
- `scenario_009` - Cliente Apressada

### Nível 3: Advanced (501-1000 pontos)

**Foco:**
- Resolver reclamações
- Handoff adequado
- Reverter cancelamentos

**Cenários recomendados:**
- `scenario_011` - Reclamação
- `scenario_012` - Handoff
- `scenario_013` - Cancelamento

### Nível 4: Expert (1000+ pontos)

**Foco:**
- Encantar clientes
- Gerar indicações
- Fidelização

**Cenários recomendados:**
- `scenario_014` - Retorno
- `scenario_015` - Indicação

---

## 📈 EVOLUÇÃO DO DOJO

### ✅ Implementado (Hoje)

- [x] 15 cenários de treino
- [x] 8 personas
- [x] Sistema de métricas
- [x] Pontuação e ranking
- [x] Feedback
- [x] Histórico
- [x] Painel frontend
- [x] API completa

### 🚀 Próxima: Dojo Simulator (Ollama)

- [ ] Cliente virtual gerado por IA
- [ ] Conversas automáticas
- [ ] Batch de 100+ simulações
- [ ] Dados reais do WhatsApp

---

## 🔗 LINKS

### Painel
- **URL:** `http://localhost:3000/dojo`
- **Status:** ✅ Operacional

### API
- **Base:** `http://localhost:8000/api/dojo`
- **Docs:** `http://localhost:8000/docs`

### Arquivos
- **API:** `backend/app/api/dojo.py`
- **Frontend:** `frontend/app/dojo/page.tsx`
- **Personas:** `backend/app/dojo/personas.py`
- **Scenarios:** `backend/app/dojo/scenarios.py`
- **Metrics:** `backend/app/dojo/metrics.py`

---

## 🎯 RESUMO FINAL

| Recurso | Status | Localização |
|---------|--------|-------------|
| Testar Cenários | ✅ | Painel + API |
| Selecionar Personas | ✅ | Painel + API |
| Ver Métricas | ✅ | Painel + API |
| Ganhar Pontos | ✅ | Painel |
| Dar Feedback | ✅ | Painel + API |
| Histórico | ✅ | Painel |
| Dojo Simulator (Ollama) | 🚀 Em implementação | `backend/app/dojo/simulator.py` |

---

**Dojo Arena:** ✅ **100% Operacional no Painel**  
**URL:** `http://localhost:3000/dojo`
