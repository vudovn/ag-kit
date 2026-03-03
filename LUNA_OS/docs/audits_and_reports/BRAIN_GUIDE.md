# 🧠 LUNA Brain — Guia de Estrutura de Conhecimento

**Como organizar o conhecimento da Luna sem redundância ou confusão**

---

## 📌 VISÃO GERAL

O **Brain** é a única fonte da verdade para o conhecimento da Luna. As configurações do negócio ficam aqui, não em Settings.

```
┌─────────────────────────────────────────────────────────┐
│                   LUNA BRAIN                            │
├─────────────────────────────────────────────────────────┤
│  📦 Conhecimento (o que a Luna SABE)                   │
│  ─────────────────────────────────────────────────────  │
│  • Negócio: Dados fixos da empresa                     │
│  • Serviços: Lista completa com preços                 │
│  • FAQ: Perguntas e respostas frequentes               │
│  • Prompts: Comportamentos e regras de atuação         │
│  • Insights: Dicas de venda, padrões de clientes       │
├─────────────────────────────────────────────────────────┤
│  ⚙️  Settings (o que a Luna É)                         │
│  ─────────────────────────────────────────────────────  │
│  • Nome: "Luna"                                        │
│  • Personalidade: Tom, estilo, fallback                │
│  • IA: Modelos, provedores, chaves de API              │
│  • Webhooks: Configurações de integração               │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 CATEGORIAS DO BRAIN

### 1. **Negócio** 🏢

**O que colocar:** Dados FIXOS e IMUTÁVEIS da empresa

| Campo | Exemplo | Muda? |
|-------|---------|-------|
| Nome | Haven Escovaria & Esmalteria | ❌ Nunca |
| Endereço | Rua Mato Grosso, 837E, Chapecó | ❌ Raro |
| Horário | Seg-Sáb, 8h-20h | ❌ Raro |
| Telefone | (49) 99999-9999 | ❌ Nunca |
| Instagram | @haven.escovaria | ❌ Nunca |

**Formato:**
```json
{
  "name": "Haven Escovaria & Esmalteria",
  "address": "Rua Mato Grosso, 837E - Jardim Itália, Chapecó - SC",
  "hours": "Segunda a Sábado, 8h às 20h",
  "phone": "(49) 99999-9999",
  "instagram": "@haven.escovaria"
}
```

**⚠️ NÃO coloque aqui:**
- Preços de serviços (vai em **Serviços**)
- Promoções temporárias (vai em **Insights**)
- Regras de atendimento (vai em **Prompts**)

---

### 2. **Serviços** 🎯

**O que colocar:** LISTA COMPLETA de serviços com preços e duração

| Campo | Exemplo |
|-------|---------|
| Nome | Escova Progressiva |
| Preço | R$ 120 |
| Duração | 90 minutos |
| Categoria | Cabelo |
| Descrição | Alisamento com formol |
| Keywords | ["liso", "progressiva", "alisar"] |

**Formato:**
```json
{
  "services": [
    {
      "name": "Escova Simples",
      "price": 35,
      "duration": 30,
      "category": "Cabelo",
      "keywords": ["liso", "secar", "modelar"]
    },
    {
      "name": "Manicure",
      "price": 30,
      "duration": 30,
      "category": "Unha",
      "keywords": ["unha", "cutícula", "esmalte"]
    }
  ]
}
```

**✅ Dica:** A Luna usa isso para responder perguntas de preço

**⚠️ NÃO coloque aqui:**
- Promoções temporárias (use **Insights**)
- Pacotes (use campo específico **Pacotes**)

---

### 3. **FAQ** 💬

**O que colocar:** PERGUNTAS FREQUENTES e respostas objetivas

| Pergunta | Resposta |
|----------|----------|
| Aceita cartão? | Sim, crédito, débito e PIX |
| Precisa agendar? | Recomendamos sim! |
| Tem estacionamento? | Sim, gratuito |
| Atende domingo? | Não, só Seg-Sáb |

**Formato:**
```json
{
  "questions": [
    {
      "q": "Aceita cartão?",
      "a": "Sim! Aceitamos cartão de crédito, débito e PIX."
    },
    {
      "q": "Precisa agendar horário?",
      "a": "Recomendamos agendamento para garantir seu horário. Mas podemos atender sem agendar se tiver vaga!"
    }
  ]
}
```

**✅ Dica:** Use padrões de pergunta:
```json
{
  "patterns": ["aceita cartão", "paga com cartão", "tem máquina"],
  "answer": "Sim, aceitamos..."
}
```

**⚠️ NÃO coloque aqui:**
- Preços (vai em **Serviços**)
- Comportamentos (vai em **Prompts**)

---

### 4. **Prompts** 📖

**O que colocar:** REGRAS DE COMPORTAMENTO da Luna

**Exemplos:**

| Situação | Como agir |
|----------|-----------|
| Cliente pede desconto | "Vou ver com a equipe" → handoff |
| Cliente elogia | Agradeça e ofereça indicação |
| Cliente reclama | Peça desculpas e chame humano |
| Pergunta complexa | Não invente → handoff |

**Formato:**
```json
{
  "rules": [
    {
      "trigger": "cliente pede desconto",
      "action": "Não prometa. Diga: 'Vou ver com a equipe' e faça handoff"
    },
    {
      "trigger": "cliente elogia",
      "action": "Agradeça: 'Que bom que gostou!' e peça indicação"
    }
  ]
}
```

**✅ Dica:** Isso molda a PERSONALIDADE da Luna

**⚠️ NÃO coloque aqui:**
- Dados da empresa (vai em **Negócio**)
- Lista de serviços (vai em **Serviços**)

---

### 5. **Insights** 💡

**O que colocar:** DICAS DE VENDA e padrões observados

**Exemplos:**

| Insight | Uso |
|---------|-----|
| "Mães preferem manhã" | Campanha Dia das Mães |
| "Noite tem menos procura" | Oferta relâmpago 17h |
| "Unha + Escova = ticket maior" | Upsell automático |

**Formato:**
```json
{
  "insights": [
    {
      "title": "Mães preferem manhã",
      "description": "80% das mães agendam horário da manhã",
      "action": "Ofereça horários 8h-12h para mães"
    },
    {
      "title": "Sexta tem cancelamento",
      "description": "Sextas têm 30% mais cancelamento",
      "action": "Confirme quinta-feira os agendamentos de sexta"
    }
  ]
}
```

**✅ Dica:** Isso é aprendido com o tempo — atualize frequentemente

**⚠️ NÃO coloque aqui:**
- Dados fixos (vai em **Negócio**)
- Regras obrigatórias (vai em **Prompts**)

---

## 🔀 FLUXO DE INFORMAÇÃO

```
Cliente pergunta → Luna busca no Brain:
                   1. FAQ (tem pergunta similar?)
                   2. Serviços (tem preço/lista?)
                   3. Negócio (tem dado fixo?)
                   4. Prompts (tem regra?)
                   5. Insights (tem dica?)
                   ↓
                   Se nada → Handoff (NÃO INVENTE!)
```

---

## ❓ PERGUNTAS FREQUENTES

### "Se eu remover tudo do Brain, a Luna fica burra?"

**Sim.** A Luna perde acesso a:
- Preços dos serviços
- Horário de funcionamento
- Endereço
- FAQ
- Regras de comportamento

**Ela ainda:**
- Responde saudações básicas (hardcoded)
- Faz análise de sentimento
- Classifica intents
- Salva no Supabase

---

### "Settings e Brain têm dados duplicados. Qual prevalece?"

**Brain prevalece** para conhecimento.

**Settings** é apenas para:
- Nome de exibição da Luna
- Frase de fallback
- Chaves de API
- Configurações técnicas

**Regra:** Se está no Brain, usa o Brain. Settings é backup.

---

### "Posso ter o mesmo dado em Negócio e Serviços?"

**Não.** Isso causa redundância e conflito.

**Exemplo errado:**
- Negócio: "Escova custa R$35"
- Serviços: "Escova: R$35"

**Exemplo certo:**
- Negócio: "Nome, endereço, horário"
- Serviços: "Escova: R$35, 30min"

---

### "Como atualizo uma promoção temporária?"

**Use Insights**, não altere Serviços.

**Exemplo:**
```json
// Insights
{
  "title": "Promoção Dia das Mães",
  "description": "15% OFF em serviços de cabelo",
  "valid_until": "2026-05-10",
  "action": "Ofereça para clientes que perguntarem preço"
}
```

---

## 📋 CHECKLIST: ONDE COLOCAR CADA COISA

| Informação | Categoria | Exemplo |
|------------|-----------|---------|
| Nome da empresa | 🏢 Negócio | "Haven Escovaria" |
| Endereço | 🏢 Negócio | "Rua Mato Grosso, 837E" |
| Horário | 🏢 Negócio | "Seg-Sáb, 8h-20h" |
| Preço de serviço | 🎯 Serviços | "Escova: R$35" |
| Duração | 🎯 Serviços | "Manicure: 30min" |
| "Aceita cartão?" | 💬 FAQ | "Sim, crédito/débito/PIX" |
| "Tem desconto?" | 💬 FAQ | "Temos pacote promocional" |
| Como lidar com reclamação | 📖 Prompts | "Peça desculpas → handoff" |
| Quando oferecer upsell | 📖 Prompts | "Após fechar serviço principal" |
| Padrão de mães | 💡 Insights | "Preferem manhã" |
| Melhor dia para oferta | 💡 Insights | "Terça tem menos movimento" |

---

## 🛠️ MANUTENÇÃO DO BRAIN

### Frequência Recomendada

| Categoria | Quando atualizar |
|-----------|------------------|
| 🏢 Negócio | Só se mudar algo fixo |
| 🎯 Serviços | Mensalmente (preços/serviços novos) |
| 💬 FAQ | Semanalmente (novas perguntas) |
| 📖 Prompts | Mensalmente (ajuste de comportamento) |
| 💡 Insights | Diariamente (aprendizado contínuo) |

### Como Adicionar

1. Acesse `/brain` no dashboard
2. Clique em "Novo item de conhecimento"
3. Selecione categoria
4. Preencha título e conteúdo
5. Clique em "Salvar"

### Como Remover

1. Acesse `/brain`
2. Passe mouse sobre o item
3. Clique em 🗑️
4. Confirme

---

## 🎯 EXEMPLO PRÁTICO COMPLETO

**Situação:** Cliente pergunta "Quanto custa escova progressiva?"

**Busca no Brain:**

1. **FAQ?** → Não tem pergunta exata
2. **Serviços?** → ✅ ENCONTROU!
   ```json
   {"name": "Escova Progressiva", "price": 120, "duration": 90}
   ```
3. **Negócio?** → Não precisa
4. **Prompts?** → Verifica regra de preço
   - "Sempre confirme preço do knowledge_base"
5. **Insights?** → Tem dica relevante
   - "Progressiva tem alta margem → ofereça hidratação junto"

**Resposta da Luna:**
> "A escova progressiva custa R$120 e leva cerca de 1h30. Enquanto você faz, que tal aproveitar para fazer uma hidratação? Temos uma condição especial! 😊"

---

**MCT OS — Poder invisível, simplicidade visível.** 🌙
