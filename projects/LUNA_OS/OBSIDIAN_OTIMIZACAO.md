# 🧠 LUNA OS Obsidian Vault - Análise Crítica & Otimização

**Data:** 2026-02-28  
**Auditor:** Agente MCT via Agent Flow  
**Foco:** Potencializar LUNA através do Obsidian

---

## 📊 RESUMO EXECUTIVO

| Métrica | Valor | Status |
|---------|-------|--------|
| **Total de Arquivos .md** | 351 | ✅ |
| **Clientes Cadastrados** | 92 | ✅ |
| **Logs de Conversas** | 197 | ⚠️ |
| **Serviços Arquivados** | 36 | ⚠️ |
| **FAQs Arquivados** | 4 | ⚠️ |
| **Prompts Copilot** | 19 | ✅ |
| **Diretórios Vazios** | 9 | ❌ |

**Veredito:** 🟡 **Sistema em Migração Incompleta**

---

## 1️⃣ O QUE FAZ SENTIDO ✅ (Manter & Expandir)

### A. Arquitetura de Diretórios

```
✅ CRM/Clients/          → Perfis de clientes (92 arquivos)
✅ CRM/Logs/Recent/      → Logs de conversas (197 arquivos)
✅ copilot/              → Prompts customizados (19 arquivos)
✅ Templates/            → Modelo "Novo Cliente"
✅ 000_MCT_MASTER_INDEX  → Hub de navegação
✅ Dashboard.md          → Dashboard executivo
```

**Por que funciona:**
- Separação clara entre dados ativos (CRM) e histórico (Archive)
- Sistema de templates padronizado
- Navegação hierárquica intuitiva

### B. Schema de Clientes

```yaml
---
id: <uuid>
phone: <phone_number>
persona: None
tags: ['legado', 'sync_4anos']
last_contact: <ISO timestamp>
---
# Nome do Cliente

**Notas:** None

**Preferências:**
```json
{}
```
```

**Pontos Fortes:**
- UUID único para sincronização com Supabase
- Phone number como identificador secundário
- Tags para segmentação
- Timestamp de último contato
- Campo estruturado para preferências (JSON)

**Exemplos de Sucesso:**
- `instituto-suzana-rios.md` - Tem profile_pic
- `priscila-parceria-kuhn.md` - Tem profile_pic
- `carla-haven.md` - Cliente ativo

### C. Copilot Custom Prompts (19 arquivos)

**Destaques:**

| Prompt | Função | Valor |
|--------|--------|-------|
| **LUNA - Auditor do Dojo** | Auditoria de conversas | 🔥 Essencial |
| **MCT - Extrair Knowledge Item** | Extração de conhecimento | 🔥 Essencial |
| **MCT - Code Review** | Revisão de código | ✅ Útil |
| **MCT - Gerar Implementation Plan** | Planejamento técnico | ✅ Útil |
| **Clip Web Page** | Web clipping | ✅ Inovador |
| **Clip YouTube Transcript** | Resumo de vídeos | ✅ Inovador |

**Por que funciona:**
- Prompts específicos para contexto MCT
- Metadados de configuração (order, enabled)
- Placeholder `{}` para texto selecionado

### D. Sistema de Tags

```yaml
#crm              → Logs de conversas
#archive          → Conteúdo legado
#legado           → Clientes migrados
#sync_4anos       → Sincronização antiga
#cliente/novo     → Template de novo cliente
#moc              → Map of Content
#dashboard        → Dashboards
#mct              → MCT-specific
```

**Funciona porque:**
- Tags hierárquicas (`cliente/novo`)
- Separação claro entre ativo e arquivo
- Compatível com Dataview queries

---

## 2️⃣ O QUE NÃO FAZ SENTIDO ❌ (Problemas Críticos)

### A. DIRETÓRIOS VAZIOS (9 diretórios)

```
❌ Brain/Business Info/     → VAZIO
❌ Brain/FAQs/              → VAZIO
❌ Brain/Insights/          → VAZIO
❌ Brain/Prompts/           → VAZIO
❌ Brain/Services/          → VAZIO
❌ FAQs/                    → VAZIO
❌ Insights/                → VAZIO
❌ Prompts/                 → VAZIO
❌ Services/                → VAZIO
```

**Problema:**
- Conteúdo ativo está em `Archive/Legacy Knowledge/`
- Estrutura planejada não foi implementada
- Dataview queries apontam para pastas inexistentes

**Impacto na LUNA:**
- LUNA não tem acesso a serviços ativos via RAG
- FAQs não estão disponíveis para consulta
- Brain personality não está documentada

### B. CONTEÚDO NO LUGAR ERRADO

**Serviços (36 arquivos):**
```
❌ Archive/Legacy Knowledge/SVC-*.md
✅ Deveria estar em: Brain/Services/ ou Services/
```

**FAQs (4 arquivos):**
```
❌ Archive/Legacy Knowledge/FAQ-*.md
✅ Deveria estar em: Brain/FAQs/ ou FAQs/
```

**Por que é um problema:**
- LUNA busca conhecimento ativo, não arquivo
- RAG não encontra informações relevantes
- Dataview queries falham

### C. DADOS DE CLIENTES VAZIOS

**92 clientes, mas:**
- **100%** têm `Notas: None`
- **98%** têm `Preferências: {}` (vazio)
- **100%** têm tag `legado` (sugere migração incompleta)
- **100%** têm tag `sync_4anos` (significado obscuro)

**Exemplo:**
```yaml
# Carla Haven (cliente ativa)
Notas: None          ❌ Vazio
Preferências: {}     ❌ Vazio
Tags: ['legado', 'sync_4anos']  ⚠️ Apenas tags genéricas
```

**Contraste (o que deveria ter):**
```yaml
# Deveria ter:
Notas: |
  - Prefere atendimento sábado manhã
  - Alérgica a produto X
  - Cliente desde 2022, faz progressiva a cada 3 meses
  
Preferências:
  {
    "servicos_favoritos": ["progressiva", "hidratacao"],
    "profissional_preferida": "yujaira",
    "horario_preferido": "sabado_manha",
    "observacoes": "alergia_a_formol",
    "perfil_pic": "https://..."
  }
  
Tags: ['cliente/vip', 'progressiva', 'yujaira_fan']
```

### D. LOGS DE CONVERSAS - DADOS FALSOS

**197 arquivos de logs, mas:**

**Conteúdo idêntico em TODOS:**
```markdown
**[2026-02-27 23:16] CLIENTE:** Simm
**[2026-02-27 23:20] EU:** me passa as informações do presente de hoje por gentileza para colocar na planilha
```

**Problemas:**
1. Dados de placeholder, não conversas reais
2. Mesmo conteúdo em 197 arquivos diferentes
3. Sem metadados (sentiment, urgency, intent)
4. Sem link para cliente específico
5. Dashboard queries falham (campos não existem)

**O que deveria ter:**
```yaml
---
tags: [crm, chat]
client_id: <uuid>
client_name: Maria Silva
sentiment: positive
urgency: 3
intent: agendamento
objections: ["preco_alto"]
---
# Chat Log: 5549991112233

**[2026-02-28 10:30] CLIENTE:** Oi, quero agendar uma progressiva
**[2026-02-28 10:31] LUNA:** Oi! Qual dia você prefere?
...
```

### E. DUPLICAÇÃO DE ESTRUTURA

**Confusão arquitetural:**
```
/Brain/FAQs/     vs  /FAQs/
/Brain/Services/ vs  /Services/
/Brain/Insights/ vs  /Insights/
/Brain/Prompts/  vs  /Prompts/  vs  /copilot/
```

**Problema:**
- Qual é o correto?
- Conteúdo ativo vs. personalidade da IA misturados
- Navegação confusa

### F. DASHBOARD QUEBRADO

**Dataview queries com erros:**

```dataview
# ERRO 1: Caminho errado
FROM "Clients"
# ❌ Deveria: FROM "CRM/Clients"

# ERRO 2: Caminho inexistente
FROM "Chats"
# ❌ Deveria: FROM "CRM/Logs/Recent"

# ERRO 3: Pasta não existe
FROM "Knowledge/Campaigns"
# ❌ Knowledge/ não existe

# ERRO 4: Sintaxe JavaScript inválida
dv.date('now')
# ❌ Deveria: date(now)

# ERRO 5: Campos não existem
WHERE sentiment = "negative"
# ❌ sentiment não existe nos logs
```

### G. CONFIGURAÇÃO QUEBRADA

**`.obsidian/app.json`:**
```json
{
  "attachmentFolderPath": "Archive/Attachments",  // ❌ Pasta não existe
  "newFileFolderPath": "Knowledge"                // ❌ Pasta não existe
}
```

---

## 3️⃣ IMPACTO NA LUNA 🤖

### Como LUNA Usa o Obsidian

**Fluxo Ideal:**
```
1. WhatsApp → Evolution API
2. Mensagem → Brain (classifica intenção)
3. RAG → Busca no Obsidian contexto relevante
4. System Prompt → Monta resposta com contexto
5. LLM → Gera resposta
6. Obsidian → Salva log e insights
```

**Fluxo Atual (Quebrado):**
```
1. WhatsApp → Evolution API
2. Mensagem → Brain (classifica intenção)
3. RAG → ❌ Não encontra serviços/FAQs (estão em Archive)
4. System Prompt → ❌ Brain personality não documentada
5. LLM → Gera resposta sem contexto rico
6. Obsidian → ❌ Salva logs com dados falsos
```

### Consequências

| Problema | Impacto na LUNA |
|----------|-----------------|
| Serviços em Archive | LUNA não consegue consultar preços reais |
| FAQs em Archive | LUNA repete respostas em vez de usar KB |
| Brain/ vazio | Personalidade da LUNA não está documentada |
| Clientes vazios | LUNA não tem histórico do cliente |
| Logs falsos | LUNA não aprende com conversas reais |
| Dashboard quebrado | CEO não tem visibilidade |

---

## 4️⃣ PLANO DE OTIMIZAÇÃO 📋

### FASE 1: Fundação (Dia 1-2)

#### 1.1 Criar Pastas Missing
```bash
cd backend/app/knowledge/obsidian_vault

# Pastas essenciais
mkdir -p Brain/Services
mkdir -p Brain/FAQs
mkdir -p Brain/Insights
mkdir -p Brain/Prompts
mkdir -p Brain/Business Info

# Pastas de suporte
mkdir -p Archive/Attachments
mkdir -p Knowledge
```

#### 1.2 Mover Conteúdo Ativo
```bash
# Mover serviços para ativo
mv "Archive/Legacy Knowledge/SVC-"*.md Brain/Services/

# Mover FAQs para ativo
mv "Archive/Legacy Knowledge/FAQ-"*.md Brain/FAQs/

# Opcional: renomear arquivos (remover prefixo)
for f in Brain/Services/SVC-*.md; do
  mv "$f" "Brain/Services/${f#Brain/Services/SVC-}"
done

for f in Brain/FAQs/FAQ-*.md; do
  mv "$f" "Brain/FAQs/${f#Brain/FAQs/FAQ-}"
done
```

#### 1.3 Atualizar Tags
```bash
# Batch update: archive → active
# Usar Find & Replace em massa ou script Python
```

### FASE 2: Dados de Clientes (Dia 3-5)

#### 2.1 Script de Enriquecimento

```python
# scripts/enrich_clients.py
"""
Enriquece perfis de clientes com dados do Supabase
"""
import json
from supabase import create_client

# Conectar ao Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Buscar clientes com histórico
clients = supabase.table("clients").select("""
  id, phone, name, tags, preferences, 
  total_visits, total_spent
""").execute()

# Para cada cliente, atualizar .md no Obsidian
for client in clients.data:
    md_file = f"CRM/Clients/{client['phone']}.md"
    
    # Ler arquivo existente
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Atualizar frontmatter
    # Adicionar notas inteligentes
    # Salvar
    
print(f"✅ {len(clients.data)} clientes enriquecidos")
```

#### 2.2 Template de Cliente Melhorado

```markdown
---
phone: {{phone}}
tags: [{{tag}}]
total_visits: {{visits}}
total_spent: {{spent}}
first_contact: {{date}}
last_contact: {{date}}
servicos_favoritos: []
profissional_preferida: null
observacoes: null
---

# 👥 Perfil: {{name}}

## 📞 Contato
- **Telefone**: {{phone}}
- **Status**: {{status}}

## 📝 Histórico de Serviços
| Data | Serviço | Profissional | Valor |
|------|---------|--------------|-------|
{% for appointment in appointments %}
| {{appointment.date}} | {{appointment.service}} | {{appointment.professional}} | R$ {{appointment.value}} |
{% endfor %}

## 🧠 Inteligência (LUNA)
- **Preferências:** 
- **Objeções comuns:**
- **Melhor horário:**
- **Aniversário:**

## 📊 Métricas
- **Ticket médio:** R$ {{avg_ticket}}
- **Frequência:** {{frequency}} dias
- **Última visita:** {{days_since}} dias

---
[[Dashboard|🏠 Voltar]]
```

### FASE 3: Logs Reais (Dia 6-7)

#### 3.1 Script de Sync de Conversas

```python
# scripts/sync_conversations.py
"""
Sincroniza conversas reais do Supabase para Obsidian
"""
from datetime import datetime

# Buscar conversas reais
conversations = supabase.table("conversations").select("""
  id, phone, status, intent, sentiment, 
  started_at, messages_count
""").order("started_at", desc=True).limit(50).execute()

for conv in conversations.data:
    # Buscar mensagens
    messages = supabase.table("messages")
        .select("*")
        .eq("conversation_id", conv['id'])
        .order("created_at", asc=True)
        .execute()
    
    # Gerar arquivo .md
    md_content = f"""---
tags: [crm, chat]
client_phone: {conv['phone']}
sentiment: {conv['sentiment'] or 'unknown'}
urgency: {calculate_urgency(conv)}
intent: {conv['intent'] or 'unknown'}
---

# Chat Log: {conv['phone']}

"""
    
    for msg in messages.data:
        role = "CLIENTE" if msg['direction'] == "inbound" else "LUNA"
        timestamp = msg['created_at'][:16].replace('T', ' ')
        md_content += f"**[{timestamp}] {role}:** {msg['content']}\n\n"
    
    # Salvar arquivo
    filename = f"CRM/Logs/Recent/Chat-{conv['phone']}.md"
    with open(filename, 'w') as f:
        f.write(md_content)
```

#### 3.2 Limpar Logs Falsos

```bash
# Backup primeiro
cp -r CRM/Logs/Recent CRM/Logs/Recent.backup

# Deletar logs com conteúdo placeholder
# (script Python para identificar e remover)
```

### FASE 4: Brain Personality (Dia 8-10)

#### 4.1 Documentar LUNA Brain

**Criar:** `Brain/Prompts/system-prompt.md`

```markdown
---
tags: [brain, prompt, system]
version: 3.0
---

# 🤖 LUNA System Prompt

## Identidade
Você é LUNA, assistente virtual da Haven Escovaria & Esmalteria.

## Tom de Voz
- Acolhedora
- Empática
- Profissional mas acessível
- Usa emojis moderadamente 🌙

## Regras Soberanas
1. **Nunca invente preços** - Consulte `[[Brain/Services]]`
2. **Nunca confirme horários sem base** - Use scheduler
3. **Handoff quando inseguro** - Transferir para humano
4. **Orientada à conversão** - Sempre guie para agendamento

## Conhecimento Base
- Serviços: `[[Brain/Services]]`
- FAQs: `[[Brain/FAQs]]`
- Profissionais: `[[Brain/Business Info/Profissionais]]`
- Regras: `[[Brain/Business Info/Regras]]`
```

#### 4.2 Criar Knowledge Items

**Usar prompt:** `MCT - Extrair Knowledge Item`

Exemplos para criar:
- `Brain/Insights/regra-progressiva.md`
- `Brain/Insights/objecao-preco.md`
- `Brain/Insights/horarios-pico.md`

### FASE 5: Dashboard Funcional (Dia 11-12)

#### 5.1 Corrigir Dataview Queries

```dataview
# ✅ Clientes Ativos (corrigido)
TABLE total_visits as "Visitas", total_spent as "Total Gasto"
FROM "CRM/Clients"
WHERE total_spent > 0
SORT total_spent DESC
LIMIT 10
```

```dataview
# ✅ Logs Recentes (corrigido)
TABLE sentiment as "Humor", intent as "Intenção"
FROM "CRM/Logs/Recent"
SORT file.mday DESC
LIMIT 10
```

```dataview
# ✅ Serviços Mais Procurados
TABLE duracao_min as "Duração", valor as "Preço"
FROM "Brain/Services"
WHERE categoria = "cabelo"
SORT valor DESC
```

#### 5.2 Adicionar Novas Views

```dataview
# 🔥 Urgências do Dia
TABLE urgency as "Nível", client_phone as "Cliente"
FROM "CRM/Logs/Recent"
WHERE urgency >= 4
SORT urgency DESC
```

```dataview
# 💰 Receita do Mês
SUM(total_spent) as "Receita Total"
FROM "CRM/Clients"
WHERE last_contact >= date(this month)
```

### FASE 6: Automação (Dia 13-15)

#### 6.1 Script de Sync Contínuo

```python
# scripts/obsidian_sync_daemon.py
"""
Sync contínuo: Supabase → Obsidian (a cada 5 min)
"""
import schedule
import time

def sync_clients():
    """Sincroniza clientes"""
    pass

def sync_conversations():
    """Sincroniza conversas recentes"""
    pass

def generate_insights():
    """Gera insights automáticos"""
    pass

# Agendar
schedule.every(5).minutes.do(sync_conversations)
schedule.every(1).hours.do(sync_clients)
schedule.every(1).days.do(generate_insights)

while True:
    schedule.run_pending()
    time.sleep(1)
```

#### 6.2 Templater Scripts Avançados

```javascript
// Templates/scripts/analyze-client.js
module.exports = async (params) => {
  const phone = params.phone;
  // Buscar dados do Supabase
  // Calcular métricas
  // Gerar insights
  return {
    total_visits: 10,
    avg_ticket: 150.00,
    last_service: "Progressiva"
  };
};
```

---

## 5️⃣ RECOMENDAÇÕES PRIORITÁRIAS 🎯

### P0 - Crítico (Semana 1)

| # | Ação | Impacto | Esforço |
|---|------|---------|---------|
| 1 | Mover serviços/FAQs para Brain/ | LUNA acessa KB | 1h |
| 2 | Criar pastas missing | Sistema funciona | 30min |
| 3 | Corrigir Dashboard queries | Visibilidade CEO | 2h |
| 4 | Script sync conversas reais | LUNA aprende | 4h |

### P1 - Alto (Semana 2)

| # | Ação | Impacto | Esforço |
|---|------|---------|---------|
| 5 | Enriquecer perfis de clientes | LUNA personaliza | 6h |
| 6 | Documentar Brain personality | LUNA consistente | 4h |
| 7 | Template cliente melhorado | Onboarding fácil | 2h |
| 8 | Limpar logs falsos | Dados limpos | 1h |

### P2 - Médio (Semana 3-4)

| # | Ação | Impacto | Esforço |
|---|------|---------|---------|
| 9 | Sync daemon contínuo | Auto-atualização | 8h |
| 10 | Knowledge items automáticos | Insights CEO | 6h |
| 11 | Icon system | UX navigation | 2h |
| 12 | Advanced Dataviews | Analytics rico | 4h |

---

## 6️⃣ ARQUITETURA RECOMENDADA 🏛️

### Estrutura Final Sugerida

```
obsidian_vault/
├── .obsidian/                    [Config]
│
├── CRM/                          [Dados Ativos]
│   ├── Clients/                  [92 clientes → enriquecer]
│   └── Logs/
│       └── Recent/               [197 logs → dados reais]
│
├── Brain/                        [Personalidade LUNA]
│   ├── Services/                 [36 serviços ← mover de Archive]
│   ├── FAQs/                     [4 FAQs ← mover de Archive]
│   ├── Prompts/                  [System prompts]
│   ├── Business Info/            [Regras, profissionais]
│   └── Insights/                 [Knowledge items]
│
├── Knowledge/                    [Conhecimento Gerado]
│   ├── Campaigns/                [Campanhas ativas]
│   └── Patterns/                 [Padrões detectados]
│
├── Archive/                      [Histórico]
│   ├── Legacy Knowledge/         [Manter como backup]
│   ├── Logs/                     [Logs antigos >30 dias]
│   └── Attachments/              [Mídia]
│
├── Templates/                    [Modelos]
│   ├── Novo Cliente.md
│   ├── Chat Log.md
│   └── Knowledge Item.md
│
├── copilot/                      [Prompts Copilot]
│   └── copilot-custom-prompts/   [19 prompts → manter]
│
├── 000_MCT_MASTER_INDEX.md       [Hub]
└── Dashboard.md                  [Executivo]
```

---

## 7️⃣ MÉTRICAS DE SUCESSO 📈

### Após Otimização

| Métrica | Antes | Depois Esperado |
|---------|-------|-----------------|
| **Clientes com notas** | 0% | 80%+ |
| **Clientes com preferências** | 2% | 70%+ |
| **Logs com dados reais** | 0% | 100% |
| **Serviços em Brain/** | 0 | 36 |
| **FAQs em Brain/** | 0 | 4 |
| **Dashboard queries funcionando** | 0% | 100% |
| **Knowledge items** | 0 | 20+ |
| **Tempo sync** | N/A | <5 min |

---

## 8️⃣ CONCLUSÃO 🎯

### Diagnóstico Final

**O Obsidian Vault do LUNA OS tem:**
- ✅ **Excelente arquitetura** base
- ✅ **Copilot integration** sofisticada
- ✅ **Schema de dados** bem pensado
- ❌ **Migração incompleta** (conteúdo em Archive)
- ❌ **Dados vazios/falsos** (clientes, logs)
- ❌ **Configuração quebrada** (pastas, queries)

### Potencial Não Realizado

**Hoje:**
- LUNA não acessa conhecimento rico via RAG
- CEO não tem visibilidade real (Dashboard quebrado)
- Clientes não têm histórico/personalização
- LUNA não aprende com conversas (logs falsos)

**Com otimizações:**
- LUNA responde com contexto completo (serviços, FAQs, histórico)
- CEO vê urgências, sentimentos, receita em tempo real
- Clientes têm experiência personalizada
- LUNA melhora continuamente (insights automáticos)

### ROI Esperado

| Investimento | Retorno |
|--------------|---------|
| 40-50 horas (2-3 semanas) | LUNA 10x mais inteligente |
| Script de sync | Economia: 5h/semana manual |
| Enriquecimento clientes | +20% conversão |
| Dashboard funcional | Decisões em minutos |

---

**Próxima Ação Recomendada:**
Começar pela **FASE 1** (mover serviços/FAQs, criar pastas) - impacto imediato em 1-2 dias.

---

*Documento gerado via Agent Flow - MCT OS v3.0*
