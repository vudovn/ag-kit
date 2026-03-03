---
tags:
  - moc
  - index
  - dashboard
cssclasses:
  - dashboard
---

# 🧠 MCT Master Sovereign Index

**Última Atualização:** 2026-03-01  
**Status:** ✅ Refatorado - Estrutura Limpa

---

## 🚀 Navegação Rápida

### 📊 Visão Geral
- [[Intelligence Dashboard|📈 Dashboard Principal]]
- [[_Active/03-INTELLIGENCE/Ollama-Insights/|🧠 Insights Ollama]]
- [[_Active/03-INTELLIGENCE/Agent-Analysis/|🤖 Análise de Agentes]]

### 👥 CRM
- [[_Active/01-CRM/Clients/|👥 Clientes (758)]]
- [[_Active/01-CRM/Journals/|💬 Journals (204)]]

### 📚 Conhecimento
- [[_Active/02-KNOWLEDGE/Services/|📋 Serviços (38)]]
- [[_Active/02-KNOWLEDGE/FAQs/|❓ FAQs (4)]]
- [[_Active/02-KNOWLEDGE/Professionals/|👩‍💼 Profissionais (5)]]
- [[_Active/02-KNOWLEDGE/Rules/|📜 Regras de Negócio]]

### 🛠️ Sistema
- [[_Active/04-SYSTEM/Templates/|📝 Templates]]
- [[_Active/04-SYSTEM/Prompts/|🤖 Prompts]]
- [[_Active/04-SYSTEM/Workflows/|⚡ Workflows Copilot]]

---

## 📊 Analytics em Tempo Real

### Últimos Insights (Ollama)
```dataview
TABLE without id file.link as "Cliente", file.mday as "Data", confidence_score as "Confiança"
FROM "_Active/03-INTELLIGENCE/Ollama-Insights"
SORT file.mday DESC
LIMIT 5
```

### Últimas Conversas
```dataview
TABLE without id file.link as "Cliente", file.mday as "Data"
FROM "_Active/01-CRM/Journals"
SORT file.mday DESC
LIMIT 5
```

### Clientes Ativos (Últimos 7 dias)
```dataview
TABLE without id file.link as "Cliente", last_contact as "Último Contato"
FROM "_Active/01-CRM/Clients"
WHERE last_contact >= date(now) - dur(7 days)
SORT last_contact DESC
LIMIT 10
```

---

## 🗂️ Estrutura do Vault

```
_Archive/                         # Histórico (>90 dias)
├── 2025/
└── 2026/

_Active/                          # Dados Ativos
├── 00-INDEX/                     # Este arquivo
├── 01-CRM/                       # Clientes e Conversas
│   ├── Clients/                  (758 perfis)
│   ├── Journals/                 (204 logs)
│   └── Logs/
│
├── 02-KNOWLEDGE/                 # Base de Conhecimento
│   ├── Services/                 (38 serviços)
│   ├── FAQs/                     (4 FAQs)
│   ├── Professionals/            (5 profissionais)
│   ├── Rules/                    (Regras)
│   └── Business-Info/            (Dados empresa)
│
├── 03-INTELLIGENCE/              # Inteligência Gerada
│   ├── Ollama-Insights/          (IA Local)
│   ├── Agent-Analysis/           (5 Agentes)
│   ├── Psychology-Profiles/      (Perfis DISC)
│   └── Sales-Patterns/           (Padrões)
│
└── 04-SYSTEM/                    # Ferramentas
    ├── Templates/                (Todos templates)
    ├── Dashboards/               (Dashboards)
    ├── Prompts/                  (System prompts)
    └── Workflows/                (Copilot)
```

---

## ⚡ Ações Rápidas

### Copilot Workflows
1. **MCT: Extrair Knowledge Item** → Cria inteligência oficial
2. **LUNA: Auditor do Dojo** → Valida testes anti-alucinação
3. **MCT: Code Review** → Audita código "Truth in Data"
4. **MCT: Gerar Implementation Plan** → Gera planos
5. **Ollama: Gerar Insight** → Insight com IA local

### Atalhos de Teclado
- `Ctrl/Cmd + O` → Buscar arquivo
- `Ctrl/Cmd + E` → Editar modo live preview
- `Ctrl/Cmd + P` → Palette de comandos

---

## 📈 Métricas do Vault

| Métrica | Valor |
|---------|-------|
| **Total Arquivos** | 1.041 |
| **Clientes** | 758 |
| **Journals** | 204 |
| **Serviços** | 38 |
| **FAQs** | 4 |
| **Insights Ollama** | 0 |
| **Templates** | 5 |
| **Workflows Copilot** | 19 |

---

## 🔗 Links Externos

- [Documentação da Refatoração](REFACTORING_DOCUMENTATION.md)
- [Ollama Integration](_Active/04-SYSTEM/Prompts/Ollama Integration.md)
- [Conversation Intelligence Module](../../../../modules_v3/conversation_intelligence/README.md)

---

*Refatorado via Agent Flow - 2026-03-01*
