# 🧠 LUNA OS - Knowledge Items Sync

**Data:** 2026-03-01  
**Status:** Mid-Term Knowledge Base Atualizada  
**Fonte:** Agent Flow Execution

---

## 📚 KNOWLEDGE ITEMS EXISTENTES

### 1. Diagnósticos Completos
- `DIAGNOSTICO_COMPLETO.md` - Diagnóstico geral do sistema
- `PROTOCOLO_100x_REAVALIACAO.md` - Avaliação 100x completa (Score: 61.875/100)
- `OBSIDIAN_OTIMIZACAO.md` - Análise completa do Obsidian Vault
- `VARREDURA_COMPLETA_HOME.md` - Varredura da home directory

### 2. Estado Atual do Sistema (Truth in Data)

#### Backend
- **Status:** ✅ Online (porta 8000)
- **Health:** ✅ Healthy
- **Supabase:** ✅ Conectado (latência: 648ms)
- **OpenRouter:** ✅ Conectado
- **Evolution API:** ⚠️ Online mas estado: **close** (não conectado ao WhatsApp)

#### Frontend
- **Status:** ✅ Online (porta 3000)
- **Build:** Next.js 14.1.0

#### Configuração Ativa
- **LUNA_MODE:** `observe` (NÃO responde automaticamente)
- **BELASIS_MOCK:** `true` (agendamentos simulados)
- **Knowledge Base:** ⚠️ **VAZIA** no Supabase

### 3. Issues Críticos (Top 5)

| # | Issue | Impacto | Prazo |
|---|-------|---------|-------|
| 1 | Chaves de API expostas no .env | 🔴 Crítico | Imediato |
| 2 | .gitignore inexistente (agora existe ✅) | 🔴 Crítico | Feito |
| 3 | Evolution API estado: close | 🔴 Alto | 24h |
| 4 | LUNA_MODE=observe | 🟡 Alto | 48h |
| 5 | Knowledge base vazia | 🟡 Médio | 7 dias |

### 4. Arquitetura Mapeada

**Backend (129 arquivos Python, 25.296 LOC):**
- Core: brain.py (1.438 linhas), memory.py, evolution.py, scheduler.py
- API: webhooks.py, conversations.py, clients.py, analytics_super.py
- Modules V3: 8 módulos (agenda_viva, ai_coach, churn_detector, heat_map, etc.)
- Scripts: 40+ scripts de diagnóstico

**Frontend (23 arquivos .tsx):**
- 14 páginas principais
- Components: Sidebar, MetricCard, HourlyChart, etc.

**Obsidian Vault (1.165 arquivos .md):**
- CRM: 92 clientes + 197 logs
- Archive: 36 serviços + 4 FAQs
- Copilot: 19 prompts customizados
- **Problema:** Conteúdo ativo está em Archive, não em Brain/

### 5. Lições de Debugging (Wisdom Captured)

#### Lição 1: Evolution API Estado Close
**Contexto:** Evolution API responde na porta 8081, mas estado é "close"
**Causa:** Instância não conectada ao WhatsApp (QR Code não escaneado)
**Solução:** 
```bash
curl http://localhost:8081/instance/connect/haven
# Escanear QR Code via frontend /whatsapp page
```

#### Lição 2: Knowledge Base Vazia
**Contexto:** Supabase conectado mas knowledge_base sem dados
**Causa:** Scripts de seed não executados ou falharam
**Solução:** Executar `backend/app/scripts/seed_haven.py`

#### Lição 3: Obsidian Content Misplacement
**Contexto:** Serviços e FAQs estão em Archive/Legacy Knowledge
**Causa:** Migração incompleta do sistema de conhecimento
**Solução:** Mover para Brain/Services/ e Brain/FAQs/

#### Lição 4: BELASIS_MOCK=true
**Contexto:** Integração Belasis usa dados mockados
**Causa:** Sem chave de API de produção
**Solução:** Obter chave de API ou implementar mock mais realista

### 6. Sovereign Rules Aplicadas

1. **Truth in Data:** Zero mocks na interface - se não existe no Supabase, mostra vazio
2. **Domain Sovereignty:** Usar @skills para decisões de infra (portas, DNS)
3. **Continuous Wisdom:** Todo aprendizado vai para knowledge/*.md

---

## 📊 METRICS SNAPSHOT

| Métrica | Valor | Status |
|---------|-------|--------|
| Score 100x | 61.875/100 | 🟡 Staging |
| Endpoints API | 22+ | ✅ |
| Arquivos Backend | 129 | ✅ |
| Arquivos Frontend | 27 | ✅ |
| TODOs/FIXMEs | 143 | ⚠️ |
| Clientes Obsidian | 92 | ✅ |
| Logs Obsidian | 197 | ✅ |
| Serviços | 36 (Archive) | ⚠️ |
| FAQs | 4 (Archive) | ⚠️ |

---

**Próxima Atualização:** 2026-03-08 (7 dias)
**Responsável:** Agente MCT via Agent Flow
