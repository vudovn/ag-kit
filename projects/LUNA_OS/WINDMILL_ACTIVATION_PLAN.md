# 🌬️ WINDMILL ACTIVATION PLAN - LUNA OS
**Status:** Iniciando | **Timeline:** 1-2 horas | **Impacto Financeiro:** R$ 180.000+/ano

---

## 📋 FASE 1: Docker Local (EM ANDAMENTO)

### Step 1: Iniciar Windmill Docker ✅ (em progresso)
```bash
# Localização: projects/LUNA_OS/windmill/
# Status: Puxando imagens Windmill (20-30min em primeira execução)
docker-compose up -d
```

**Containers que vão subir:**
- `db`: PostgreSQL 16 (porta 5432)
- `windmill_server`: Windmill API (porta 8000)
- `windmill_worker` (x3): Workers para executar scripts

### Step 2: Acessar Windmill Dashboard (após Docker subir)
```
URL: http://localhost/
Login: admin@windmill.dev
Password: changeme
```

### Step 3: Gerar API Token Local
```
No dashboard:
1. Vá em Profile → Settings
2. Create new token
3. Nome: "LUNA_OS_DEV"
4. Guarde o token: wm_xxxxx
```

### Step 4: Atualizar .env com Token Real
```bash
# Em /Users/franciscotaveira.ads/Documents/antigravity-kit/projects/LUNA_OS/backend/.env

WINDMILL_HOST=http://localhost  # Docker local
WINDMILL_TOKEN=wm_xxxxx         # Token gerado acima
WINDMILL_WORKSPACE=unalux
```

---

## 🎯 FASE 2: Criar Workflows Críticos (2-3 horas)

### Workflow 1: Post-Sale Follow-up (CRÍTICO - Começa HOJE)
```
Objective: 70% retenção de clientes
Timeline: Dia 0, 3, 7, 14, 30, 45+
Revenue: +R$ 50.000/mês (100 clientes × 12 manutenções/ano)
```

**Steps:**
1. Create script no Windmill: `post_sale_followup.ts`
2. Set triggers: Quando agendamento é finalizado
3. Configure sequences: Dias 0, 3, 7, 14, 30, 45
4. Connect com WhatsApp via Evolution API
5. Test com 5 clientes reais

### Workflow 2: Upsell Inteligente
```
Objective: +25% ticket médio
Revenue: +R$ 10.000/mês
```

### Workflow 3: Reativação de Clientes Inativos
```
Objective: 30-40% recuperação de churned customers
Revenue: +R$ 15.000/mês
```

### Workflow 4: Lembretes de Agendamento
```
Objective: 95% show rate
Revenue: -R$ 0 (prevenção de perda)
```

### Workflow 5: Programa de Fidelidade
```
Objective: 95% repeat rate em VIP tier
Revenue: +R$ 25.000/mês
```

### Workflow 6: Detecção de Problema & Upsell
```
Objective: 80% convertem problema em venda
Revenue: +R$ 12.000/mês
```

---

## 🔗 FASE 3: Integração com LUNA_OS Backend

### Conexões Necessárias:

#### 1. Windmill → Supabase
```javascript
// Windmill precisa acessar dados de clientes/agendamentos
- Resource: Supabase Connection
- URL: https://sktrmwogifeuzrcnpvsw.supabase.co
- Key: [usar SUPABASE_KEY do backend]
- Queries: customers, appointments, services, professionals
```

#### 2. Windmill → Evolution API (WhatsApp)
```javascript
// Para enviar mensagens WhatsApp
- Resource: Evolution API Connection
- URL: http://localhost:8081
- Key: mothership_master_2026
- Instância: Haven
```

#### 3. Windmill → Backend API
```javascript
// Para atualizar estado quando workflow completa
- POST /api/windmill/callback
- Registrar execução
- Atualizar customer status
```

---

## ✅ VALIDAÇÃO LOCAL (Antes de Produção)

### Test Plan:
1. **Post-Sale Workflow:**
   - [ ] Criar agendamento de teste
   - [ ] Validar mensagem no dia 0
   - [ ] Validar mensagem no dia 3
   - [ ] Validar mensagem no dia 7
   - [ ] Conferir conteúdo de cada mensagem

2. **Upsell Workflow:**
   - [ ] Testar com 3 serviços diferentes (progressiva, manicure, escova)
   - [ ] Validar upsell apropriado para cada tipo
   - [ ] Testar aceitação do upsell

3. **Reativação Workflow:**
   - [ ] Criar cliente inativo de teste (marca como 45+ dias)
   - [ ] Validar mensagem de reativação
   - [ ] Testar resposta

4. **Lembretes:**
   - [ ] Criar agendamento com horário específico
   - [ ] Validar lembrete 2h antes
   - [ ] Testar escalação se não confirmar

5. **End-to-End:**
   - [ ] 10 clientes testando durante 1 semana
   - [ ] Coletar feedback
   - [ ] Validar valores de receita esperados
   - [ ] Validar qualidade das respostas

---

## 🚀 FASE 4: Deploy em VPS (Após Validação 100%)

### Opções Recomendadas:

#### Opção A: DigitalOcean App Platform (Recomendado)
```
- Custo: $12-25/mês para Windmill + PostgreSQL
- Deploy: 5 minutos
- Suporte: Excelente
- Escala: Automática
```

#### Opção B: Linode
```
- Custo: $5/mês (Nanode) + $15/mês (PostgreSQL)
- Deploy: 15 minutos
- Suporte: Muito bom
- Escala: Manual
```

#### Opção C: AWS + RDS
```
- Custo: $20-50/mês (mínimo)
- Deploy: 30 minutos
- Suporte: Documentação
- Escala: Complexa
```

**Minha Recomendação:** DigitalOcean App Platform
- Mais simples
- Menos configuração
- Custo transparente
- Escala automática

---

## 📊 REVENUE PROJECTION

### Conservador (Month 1):
```
- Post-Sale: 50 clientes × R$ 150 (1 manutenção) = R$ 7.500
- Upsell: 20 clientes × R$ 80 = R$ 1.600
- Reativation: 5 clientes × R$ 200 = R$ 1.000
─────────────────────────
Month 1 Revenue: R$ 10.100
```

### Realista (Month 3):
```
- Post-Sale: 80 clientes × R$ 450 (3 manutenções) = R$ 36.000
- Upsell: 50 clientes × R$ 100 = R$ 5.000
- Reactivation: 15 clientes × R$ 300 = R$ 4.500
- Fidelidade: 30 VIP × R$ 500 = R$ 15.000
─────────────────────────
Month 3 Revenue: R$ 60.500
```

### Agressivo (Month 6):
```
- Post-Sale: 100 clientes × R$ 600 (4 manutenções) = R$ 60.000
- Upsell: 80 clientes × R$ 150 = R$ 12.000
- Reactivation: 30 clientes × R$ 400 = R$ 12.000
- Fidelidade: 60 VIP × R$ 800 = R$ 48.000
- Problema-Venda: 50 clientes × R$ 120 = R$ 6.000
─────────────────────────
Month 6 Revenue: R$ 138.000
```

**ROI:** Deploy Windmill custa R$ 500 um setup único
**Payback:** 1 hora de revenue de Month 1

---

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

### HOJE:
- [ ] Docker Windmill sobe (em progresso agora)
- [ ] Acessar dashboard e gerar token
- [ ] Atualizar .env com credenciais reais

### AMANHÃ (2-3 horas):
- [ ] Implementar Post-Sale Workflow (Priority 1)
- [ ] Testar com 5 clientes
- [ ] Coletar feedback

### FIM DE SEMANA:
- [ ] Implementar Upsell Workflow
- [ ] Implementar Reativação
- [ ] Começar validação com 20 clientes

### PRÓXIMA SEMANA:
- [ ] Todos os 6 workflows rodando
- [ ] 50+ clientes em teste
- [ ] Análise de dados
- [ ] Preparar para deploy em VPS

---

## 📞 SUPORTE TÉCNICO

Se Docker não subir:
1. Verificar espaço em disco: `df -h` (precisa de 20GB+)
2. Limpar Docker: `docker system prune -a`
3. Verificar permissões: `docker ps`
4. Ver logs: `docker logs windmill_server`

Se token não funciona:
1. Refresh em http://localhost/
2. Logout e login novamente
3. Gerar novo token

---

## 🎉 CONCLUSÃO

**Windmill vai transformar a receita do salão.**

Investimento: R$ 500 setup + 10 horas desenvolvimento
Retorno esperado: R$ 60.000/mês em Month 3
**ROI: 12.000% em 3 meses**

Vamos começar agora! 🚀
