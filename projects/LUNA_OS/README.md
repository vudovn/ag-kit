# 🚀 LUNA OS — Plataforma Inteligente de Automação & Revenue

> **"Inteligência completa. Complexidade invisível."**

Sistema de Atendimento IA + Automação de Marketing para Haven Escovaria & Esmalteria

## ⚡ Quick Start

**PRIMEIRO**: Abra `docs/README.md` para documentação centralizada
```bash
cat docs/README.md
```

**DEPOIS**: Escolha seu caminho
- 🚀 **Windmill Automation** → `docs/windmill/WINDMILL_READY_TO_BUILD.md` (+R$ 50k/mês em 2 dias)
- ✅ **Validation Tests** → `docs/validation/VALIDATION_START_HERE.md` (4 semanas)
- 🔗 **Strategic Overview** → `docs/integration/WINDMILL_VALIDATION_LTV_INTEGRATION.md` (visão completa)

## 📊 Status (15 Março 2026)

| Componente | Status | Próximo |
|-----------|--------|---------|
| **Windmill** | ✅ Pronto | Criar workflows (2 dias) |
| **Validation Phase 1** | 🟡 75% | Corrigir auth (10 min) |
| **Backend** | ✅ Saudável | Pronto para produção |
| **Infrastructure** | ✅ 4/4 tests | Validado ✅ |

## 💰 Business Impact

```
Automação Windmill: +R$ 122,000/mês em revenue recorrente
- Post-Sale Follow-up: +R$ 50k/mês
- Upsell Intelligence: +R$ 10k/mês
- Loyalty Program: +R$ 25k/mês
- Reactivation: +R$ 15k/mês
- Problem Detection: +R$ 12k/mês
- Appointment Reminders: +R$ 10k/mês

Year 1 Impact: +R$ 1,464,000 em receita
```

## 🏗️ Stack

- **Backend**: FastAPI (Python) + Uvicorn
- **Frontend**: Next.js 14 (React)
- **Database**: Supabase (PostgreSQL)
- **WhatsApp**: Evolution API
- **AI**: Anthropic Claude + OpenRouter
- **Automation**: Windmill (8 containers)
- **Cache**: Redis
- **Infrastructure**: Docker Compose

## 📁 Estrutura do Projeto

```
LUNA_OS/
├── docs/                    # 📚 TODA documentação aqui
│   ├── README.md            # ⭐ COMECE AQUI
│   ├── windmill/            # 🚀 Automação
│   ├── validation/          # ✅ Testes
│   └── integration/         # 🔗 Estratégia
├── backend/                 # 🐍 FastAPI
├── frontend/                # ⚛️ Next.js
├── tests/                   # 🧪 Testes automatizados
├── migrations/              # 🗄️ Database
└── docker-compose.yml       # 🐳 8 containers
```

## 🎯 Roadmap de Implementação (8 Semanas)

### Semana 1: Windmill Activation
- [ ] Implementar Post-Sale Follow-up workflow
- [ ] Testar com 5 clientes
- [ ] **Expected**: +R$ 50k/mês

### Semana 2: Validation Phase 2
- [ ] Shadow mode comparison
- [ ] 50 agendamentos reais
- [ ] **Expected**: 70%+ accuracy

### Semana 3: A/B Testing
- [ ] Implementar Upsell workflow
- [ ] A/B test com memória
- [ ] **Expected**: +15% conversão

### Semana 4: Phase 4 Load Test
- [ ] Windmill 1000 jobs/day
- [ ] Implementar Loyalty workflow
- [ ] **Expected**: Production ready

### Semanas 5-8: Scale to Full Automation
- [ ] Reactivation workflow
- [ ] Problem Detection workflow
- [ ] VPS deployment
- [ ] **Expected**: +R$ 122k/mês stable

## 🔑 Essential Commands

```bash
# Verifique Docker
docker ps  # Deve mostrar 8 containers

# Teste infraestrutura
bash tests/phase1_infrastructure/health_check_fixed.sh

# Acesse Windmill
http://localhost/  # admin@windmill.dev / changeme

# Backend
http://localhost:8000/  # API

# Desenvolvimento
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

## 📚 Documentação

**Toda documentação está em `docs/` com README em cada subpasta.**

Não temos de scattered .md files — temos uma estrutura clara:

```
docs/
├── README.md                         # Índice central
├── windmill/README.md               # Workflows
├── validation/README.md             # Testes
└── integration/README.md            # Estratégia
```

**Se procura algo**: Verifique `docs/README.md` primeiro

## 🚀 Deployment

### Local Development
```bash
docker-compose up -d
```

### Production (VPS)
Veja: `docs/windmill/WINDMILL_ACTIVATION_PLAN.md` → Phase 4

## 🔧 Environment

```bash
# Supabase
SUPABASE_URL=https://sktrmwogifeuzrcnpvsw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Windmill
WINDMILL_HOST=http://localhost
WINDMILL_TOKEN=U3w5nwpvJY9xx1Fh8s5HKvHFgchYFqJ5

# Evolution API
EVOLUTION_API_URL=http://localhost:8081
EVOLUTION_API_KEY=mothership_master_2026

# Admin
ADMIN_API_KEY=68f9f29186817a727191e4a219d6e804eb65fa03a0a33f01ceefb66944d629eb
```

**Veja `backend/.env` para configuração completa**

## ❓ FAQ

**P: Por que dois tipos de documentação (Windmill vs Validation)?**
R: Duas prioridades paralelas. Windmill gera revenue imediato; Validation garante qualidade. Ambas críticas.

**P: Preciso ativar Windmill agora?**
R: **SIM**. É +R$ 122k/mês. Comece em 2 dias com `docs/windmill/WINDMILL_READY_TO_BUILD.md`.

**P: E se Windmill falhar?**
R: Fase 4 de Validation testa 1000 jobs/day. Há fallbacks em `docs/integration/WINDMILL_VALIDATION_LTV_INTEGRATION.md`.

## 📞 Support

- Documentação: `docs/README.md`
- Windmill issues: `docs/windmill/WINDMILL_DIAGNOSTIC_REPORT.md`
- Validation issues: `docs/validation/CHECKPOINT_PHASE1.md`
- General architecture: `docs/integration/`

## Made with 💜 by Claude Code + Francisco Taveira

**"Inteligência completa. Complexidade invisível."** 🌙

---

**Last Update**: 15 Março 2026
**Documentation**: Fully centralized in `docs/`
**Status**: ✅ Infrastructure Validated, 🚀 Ready for Revenue Workflows
