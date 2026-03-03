# 🌙 LUNA OS v2.1 — Avaliação Crítica Completa

**Data:** 26 de Fevereiro de 2026  
**Status:** 🔴 **PROBLEMAS CRÍTICOS IDENTIFICADOS**

---

## 📊 RESUMO EXECUTIVO

| Categoria | Status | Problemas |
|-----------|--------|-----------|
| **Alucinação do Agente** | 🔴 Crítico | Regras fracas, agente inventa informações |
| **Dados Reais WhatsApp** | 🔴 Crítico | Webhook não está salvando conversas |
| **Dashboard** | 🔴 Crítico | Mostra apenas dados fakes/seed |
| **Analytics** | 🟡 Atenção | Redundante com dashboard, falta diagnóstico |
| **Campanhas** | 🟡 Atenção | Sem objetivos/insights, sem mensagens oportunistas |
| **Brain/Knowledge** | 🟡 Atenção | Estrutura confusa, redundância com Settings |
| **Personas** | 🟢 OK | Funcional, mas pode sugerir automáticas |
| **UI/UX** | 🟡 Atenção | Fundo muito claro, contraste alto |
| **Configurações** | 🟡 Atenção | Redundante com Brain, API key sem proteção |

---

## 🔴 PROBLEMAS CRÍTICOS

### 1. ALUCINAÇÃO DO AGENTE — BRAIN

**Problema:** Agente está inventando informações e pedindo para cliente "aguardar" sem necessidade

**Causa Raiz:**
- `build_system_prompt()` no `brain.py` tem regras FRACAS
- Não há blindagem explícita do tipo "NÃO INVENTE", "NÃO PROMETA", "NÃO ADEIE"
- Foco excessivo em "ser prestativa" leva a alucinação

**Solução Necessária:**
```python
# ADICIONAR no system prompt (layer3_rules):
"""
REGRAS DE OURO — NUNCA QUEBRE:
1. NUNCA invente preços, horários ou informações não confirmadas no knowledge_base
2. NUNCA diga "vou verificar" ou "aguarde" — se não sabe, ofereça handoff
3. NUNCA prometa retorno ou ligação — isso é handoff
4. Se a pergunta exigir consulta externa, diga: "Deixa eu te passar com a equipe"
5. NÃO use frases como "só um minutinho", "já te falo", "vou ver"
"""
```

**Arquivo:** `backend/app/core/brain.py` — linha ~240

---

### 2. DADOS REAIS DO WHATSAPP NÃO CARREGAM

**Problema:** Dashboard e conversas mostram apenas dados seed/fakes

**Causa Raiz:**
- Webhook da Evolution API pode não estar configurado no Evolution Manager
- OU webhook está recebendo mas não está salvando no Supabase
- OU tables do Supabase não existem (migration não rodou)

**Diagnóstico Necessário:**
```bash
# 1. Verificar se webhook está ativo no Evolution
docker-compose logs command-tower-evo-api | grep webhook

# 2. Verificar se backend está recebendo
docker-compose logs luna-backend | grep "Webhook:"

# 3. Verificar se está salvando no Supabase
docker-compose logs luna-backend | grep "messages"

# 4. Verificar se tables existem
# Acessar Supabase Dashboard → Table Editor
```

**Solução:**
1. Configurar webhook no Evolution Manager: `http://luna-backend:8000/api/webhooks/evolution`
2. Executar migration no Supabase SQL Editor
3. Testar envio de mensagem real no WhatsApp

---

### 3. DASHBOARD COM DADOS FAKES

**Problema:** `/api/analytics/dashboard` retorna dados vazios ou seed

**Causa Raiz:**
- Mesma do problema #2 — webhook não está populando tables

**Solução:**
- Após corrigir webhook, rodar `docker-compose restart luna-backend`
- Aguardar primeiras mensagens reais
- Dashboard atualizará automaticamente (SWR refresh)

---

## 🟡 PROBLEMAS DE ATENÇÃO

### 4. ANALYTICS REDUNDANTE

**Problema:** `/analytics` repete dados do dashboard

**O que falta:**
- Diagnóstico de conversas existentes (ex: "5 clientes perguntaram preço e não agendaram")
- Funil de conversão por etapa (saudação → preço → agendamento → confirmado)
- Palavras-chave mais frequentes por intent
- Horário pico de abandono
- Comparativo semanal/mensal

**Solução:** Criar novos endpoints:
```python
GET /api/analytics/funnel       # Funil de conversão
GET /api/analytics/keywords     # Palavras-chave por intent
GET /api/analytics/abandonment  # Motivos de abandono
GET /api/analytics/comparison   # Semana atual vs anterior
```

---

### 5. CAMPANHAS SEM OBJETIVOS/INSIGHTS

**Problema:** Criou campanha "Dia das Mães" mas não pediu:
- Qual objetivo? (venda direta, reativação, brand awareness?)
- Qual público? (inativos, novas clientes, todas?)
- Qual orçamento? (desconto máximo, limite de uso)
- Qual métrica de sucesso? (agendamentos, cliques, respostas)

**Solução:** Adicionar campos no modal de campanha:
```typescript
interface CampaignCreate {
  objective: 'venda' | 'reativacao' | 'branding' | 'followup'
  target: 'todos' | 'inativos_30d' | 'inativos_60d' | 'novas' | 'recorrentes'
  budget_type: 'desconto_percent' | 'desconto_fixo' | 'brinde'
  budget_value: number
  success_metric: 'agendamentos' | 'respostas' | 'cliques'
  insights?: string  // Contexto para IA: "Mães costumam querer X"
}
```

---

### 6. MENSAGENS OPORTUNÍSTAS DURANTE CONVERSA

**Problema:** Cliente pergunta "tem horário?", agente responde e fica silêncio (vácuo)

**Solução:** Campanhas ativas durante conversa
```python
# Quando intent = "disponibilidade" e status = "verificando"
# Inserir mensagem de oportunidade após 30s

OPPORTUNITY_MESSAGES = {
    "agendamento": [
        "Enquanto verifico, sabia que temos uma condição especial essa semana para {servico}?",
        "Aproveita que tô olhando aqui: temos pacote {X} com desconto pra hoje!",
    ],
    "preco": [
        "Enquanto te passo o valor, queria te contar do nosso cupom {X}...",
    ],
}
```

**Implementação:**
- No `webhooks.py`, após salvar mensagem do cliente
- Iniciar timer de 30s
- Se agente ainda não respondeu, enviar mensagem de oportunidade
- Cancelar timer se agente responder antes

---

### 7. BRAIN/KNOWLEDGE CONFUSO

**Problema:**
- Não está claro o que vai em "Prompt" vs "FAQ" vs "Negócio"
- Se remover tudo do Brain, agente fica "burro"?
- Redundância: Settings tem dados do negócio, Brain também

**Solução:**

**Estrutura Clara:**

| Seção | O que colocar | Exemplo |
|-------|---------------|---------|
| **Negócio** | Dados fixos | Nome, endereço, horário |
| **Serviços** | Lista completa | Escova: R$35, 30min |
| **FAQ** | Perguntas frequentes | "Aceita cartão?" → "Sim" |
| **Prompts** | Comportamento | "Sempre ofereça brinde" |
| **Insights** | Dicas de venda | "Mães preferem manhã" |
| **Settings** | Configurações | Nome da Luna, fallback |

**Regra:** Settings é CONFIGURAÇÃO, Brain é CONHECIMENTO

---

### 8. PERSONAS — SUGESTÕES AUTOMÁTICAS

**Problema:** Criação manual é boa, mas poderia sugerir baseado em dados

**Solução:**
```python
# Analytics: identificar padrões
# Ex: "30% das clientes perguntam preço antes de agendar"
# → Sugerir persona "Sensível a Preço"

GET /api/analytics/personas/suggest

Response:
{
    "suggested_personas": [
        {
            "name": "Cliente Pressionada",
            "triggers": ["sempre pergunta 'tem pra hoje'", "fala muito rápido"],
            "confidence": 0.85,
            "sample_count": 45
        }
    ]
}
```

---

### 9. UI — FUNDO MUITO CLARO

**Problema:** `bg-[#F9FBFF]` causa contraste alto com cards brancos

**Solução:** Escurecer para `bg-[#F0F4EF]` (Bambu mais fechado)

**Arquivo:** `frontend/app/page.tsx` e `globals.css`
```css
:root {
  --color-bg: #F0F4EF;  /* Mais escuro, menos contraste */
}
```

---

### 10. CONFIGURAÇÕES — API KEY SEM PROTEÇÃO

**Problema:**
- API Key fica visível após salvar
- Risco de alteração acidental

**Solução:** Já implementada parcialmente — mascara após salvar
- Manter máscara `••••••••••`
- Adicionar botão "Deletar e criar nova"
- Confirmar com senha antes de deletar

---

### 11. REDUNDÂNCIA CONFIGURAÇÕES ↔ BRAIN

**Problema:**
- Settings tem "Dados do Negócio"
- Brain tem "Negócio" na knowledge base

**Solução:**
- **Remover** seção "Dados do Negócio" de Settings
- **Manter** apenas em Brain (única fonte da verdade)
- Settings fica só para: IA, Personalidade, Webhooks

---

### 12. EVOLUTION API — BAILEYS VERSION

**Problema:** Versão antiga do Evolution não mostra janela de conversa

**Solução:**
- Atualizar Evolution API para v2.2.3+ (já está no docker-compose)
- OU usar Evolution Manager externo (iframe em `/connections`)

---

## 🟢 O QUE ESTÁ OK

| Item | Status | Observação |
|------|--------|------------|
| Personas (criação manual) | ✅ | Funcional, UI boa |
| Brain Simulator | ✅ | Testes internos OK |
| Health Check | ✅ | Endpoints respondem |
| Docker Compose | ✅ | Serviços sobem |
| CORS/Rate Limiting | ✅ | Implementados |

---

## 📋 PLANO DE AÇÃO

### Prioridade 1 (Crítico — 24h)
1. [ ] **Blindagem anti-alucinação** no brain.py
2. [ ] **Diagnóstico do webhook** — verificar logs
3. [ ] **Executar migration** no Supabase (se necessário)
4. [ ] **Configurar webhook** no Evolution Manager

### Prioridade 2 (Atenção — 48h)
5. [ ] **Campanhas com objetivos** — adicionar campos
6. [ ] **Mensagens oportunistas** — timer durante conversa
7. [ ] **Limpar redundância** Settings ↔ Brain
8. [ ] **Ajustar cor de fundo** — menos contraste

### Prioridade 3 (Melhoria — 7 dias)
9. [ ] **Analytics de diagnóstico** — funil, keywords, abandono
10. [ ] **Personas sugeridas** — baseado em dados reais
11. [ ] **Proteção de API Key** — confirmação para deletar
12. [ ] **Documentação clara** — o que vai em cada seção do Brain

---

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

```bash
# 1. Verificar logs do webhook
docker-compose logs luna-backend | grep -i webhook | tail -50

# 2. Verificar se Evolution está enviando
docker-compose logs command-tower-evo-api | grep -i webhook | tail -50

# 3. Testar webhook manualmente
curl -X POST http://localhost:8000/api/webhooks/evolution \
  -H "Content-Type: application/json" \
  -d '{"event":"messages.upsert","instance":"haven","data":{"message":{"conversation":"teste"},"key":{"remoteJid":"5549999999999@s.whatsapp.net","fromMe":false}}}'

# 4. Verificar tables no Supabase
# Dashboard → Table Editor → conversations, messages, clients
```

---

**MCT OS — Poder invisível, simplicidade visível.** 🌙
