# 🚀 Antigravity Core - Guia Rápido

## Visão Geral

O **Antigravity Core** é seu sistema para criar projetos com IA de forma organizada, segura e inquebrável.

---

## ⚡ Comandos Principais

### Criar Novo Projeto

```bash
./scripts/init-project.sh NomeDoProjeto
```

**O que faz:**
- Cria estrutura organizada em `projects/NomeDoProjeto/`
- Gera `CONTEXT.md` (único arquivo de contexto para IA)
- Setup inicial com `.gitignore`, `README.md`

### Listar Projetos

```bash
./scripts/mct-list
# ou
ls projects/
```

### Buscar Skills no Brain

```bash
./scripts/mct-brain security
python3 brain/query_skills.py search "react patterns"
```

### Ver Estatísticas do Brain

```bash
./scripts/mct-stats
python3 brain/query_skills.py stats
```

---

## 📁 Estrutura de um Projeto

```
projects/NomeDoProjeto/
├── CONTEXT.md          ← Arquivo PRINCIPAL para IA
├── README.md           # Quick start do projeto
├── .gitignore          # Git ignore configurado
├── docs/               # Documentação detalhada
├── src/                # Código fonte
└── .agent/skills/      # Skills específicas do projeto
```

---

## 🤖 Como Usar com IA (Qwen Code, Cursor, etc.)

### Passo 1: Criar Projeto

```bash
./scripts/init-project.sh MeuSaaS
```

### Passo 2: Editar CONTEXT.md

Edite `projects/MeuSaaS/CONTEXT.md`:

```markdown
# 📜 PROJECT CONTEXT — MeuSaaS

## 🎯 Leis do Projeto (P0 - Não Quebrar)

1. **Sempre use TypeScript estrito**
2. **Nunca commitar sem testes passando**
3. **API deve seguir REST conventions**

## 📋 Objetivo

Sistema de gestão para pequenas empresas

## 🛠️ Stack

- **Linguagem**: TypeScript 5.x
- **Framework**: Next.js 14
- **Database**: PostgreSQL + Prisma
- **Infra**: Vercel + Supabase
```

### Passo 3: Apontar IA para CONTEXT.md

Na IA (Qwen Code, Cursor):
```
"Leia projects/MeuSaaS/CONTEXT.md antes de começar"
```

Ou abra o arquivo como referência.

---

## 🎯 Por Que CONTEXT.md Único?

**Problema Anterior:**
- 3 arquivos separados (Charter + Codebase + Master Directive)
- IA não lia todos
- Informação desatualizada

**Solução:**
- ✅ 1 arquivo único
- ✅ Fácil de manter atualizado
- ✅ IA lê tudo em 1 vez
- ✅ Menos redundância

---

## 🧠 Integrando com Antigravity Brain

O Brain tem **1.256 skills** que você pode usar nos projetos.

### Exemplo: Adicionar Skills ao Projeto

No `CONTEXT.md`:

```markdown
## 🧠 Skills do Antigravity Brain

- `typescript-expert` - Padrões TypeScript
- `react-patterns` - Componentes React
- `security-auditor` - Revisão de segurança
- `test-driven-development` - TDD
```

### Buscar Skills

```bash
# Buscar skills de React
python3 brain/query_skills.py search "react"

# Buscar skills de Security
python3 brain/query_skills.py search "security audit"

# Ver stats
python3 brain/query_skills.py stats
```

---

## 📋 Workflow Completo

### 1. Iniciar Projeto

```bash
./scripts/init-project.sh DashboardApp
```

### 2. Editar CONTEXT.md

```bash
code projects/DashboardApp/CONTEXT.md
```

Defina:
- Leis do projeto (P0)
- Stack tecnológico
- Skills do Brain

### 3. Começar a Codar com IA

```
"Vamos criar o dashboard. Siga o CONTEXT.md"
```

### 4. Atualizar CONTEXT.md Após Mudanças

```markdown
## 📝 Estado Atual

- [x] Projeto inicializado
- [x] Setup do Next.js
- [x] Configuração do Prisma
- [ ] Implementar dashboard
```

---

## 🔧 Atalhos de Terminal

Adicione ao `~/.zshrc` ou `~/.bashrc`:

```bash
# Antigravity Core
source /caminho/para/antigravity-kit/scripts/brain-aliases.sh
```

**Comandos disponíveis:**

| Comando | O que faz |
|---------|-----------|
| `mct` | Vai para antigravity-kit |
| `mct-init [nome]` | Cria novo projeto |
| `mct-list` | Lista projetos |
| `mct-brain [term]` | Busca skills |
| `mct-stats` | Stats do Brain |

---

## 📊 Estatísticas

```
📦 Projetos: Em projects/
🧠 Brain: 1.256 skills
📄 Contexto: 1 arquivo por projeto (CONTEXT.md)
⚡ Scripts: 4 em scripts/
```

---

## 🎯 Exemplo Real

### Criando SaaS de Agendamento

```bash
# 1. Criar projeto
./scripts/init-project.sh AgendaSaaS

# 2. Editar CONTEXT.md
# Adicionar:
# - Leis: "Sempre UTC", "Multi-tenant"
# - Stack: "Python + FastAPI + PostgreSQL"
# - Skills: "fastapi-pro", "postgresql-optimization"

# 3. Usar com IA
# "Leia projects/AgendaSaaS/CONTEXT.md"
# "Crie endpoint de agendamento"

# 4. Buscar skills relevantes
python3 brain/query_skills.py search "calendar scheduling"
python3 brain/query_skills.py search "multi-tenant"
```

---

## 📖 Documentação Completa

| Arquivo | Descrição |
|---------|-----------|
| `docs/BRAIN.md` | Guia do Antigravity Brain |
| `docs/PROJECT_STATUS.md` | Status do projeto |
| `docs/ORGANIZATION_SUMMARY.md` | Resumo da organização |
| `projects/[nome]/CONTEXT.md` | Contexto do projeto |

---

## ✅ Checklist de Novo Projeto

- [ ] `./scripts/init-project.sh NomeDoProjeto`
- [ ] Editar `CONTEXT.md` com leis e stack
- [ ] Adicionar skills do Brain relevantes
- [ ] Testar com IA
- [ ] Atualizar `CONTEXT.md` após mudanças

---

**Status:** ✅ Funcional  
**Última atualização:** 2026-03-12  
**Versão:** 2.0 - Simplificada
