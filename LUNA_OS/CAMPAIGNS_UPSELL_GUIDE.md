# 🎯 CAMPANHAS DE MARKETING & UPSELL - GUIA DE USO

**Data:** 2026-03-01  
**Status:** ✅ **IMPLEMENTADO**

---

## 📊 O QUE FOI IMPLEMENTADO

### 1. ✅ Tabelas no Supabase
- `marketing_campaigns` - Campanhas com datas de início/fim
- `upsell_opportunities` - Oportunidades de upsell por serviço

### 2. ✅ APIs Criadas
- `GET /api/campaigns/active` - Campanhas ativas
- `GET /api/campaigns/{id}` - Campanha específica
- `GET /api/upsell/{service_id}` - Upsell para serviço
- `GET /api/campaigns/suggest/{service_id}` - Sugestões para Brain

### 3. ✅ Funções no Brain.py
- `get_marketing_suggestion(service_id)` - Busca sugestões
- `generate_upsell_script(service_id, client_name)` - Gera script

---

## 🚀 COMO USAR NO DIA A DIA

### Cenário 1: Cliente Pede Escova

**Cliente:** "Quero agendar uma escova lisa"

**Fluxo Automático:**
1. Brain identifica serviço: `escova_lisa`
2. Chama API: `/api/campaigns/suggest/escova_lisa`
3. Retorna campanha ativa + upsell
4. Brain usa script durante espera

**Resposta do Brain:**
```
Perfeito! Escova Lisa sai por R$ 59,00.

Enquanto consulto os horários de escova, você sabia que 
estamos com uma campanha especial?

Fazendo escova + manicure juntas, você ganha 15% de desconto!
Consigo encaixar tudo no mesmo horário. O que acha?

Me diz: qual dia você prefere?
```

---

### Cenário 2: Cliente Pede Progressiva

**Cliente:** "Quero fazer progressiva"

**Fluxo Automático:**
1. Brain identifica: `progressiva_curtos`
2. Chama API de sugestões
3. Retorna upsell: manicure + pedicure + hidratação

**Resposta do Brain:**
```
Excelente escolha! A progressiva leva um tempinho (3h em média).

Que tal já deixar unhas e sobrancelhas prontas?
Temos uma campanha de manicure + pedicure com 15% de desconto!

E temos hidratação especial pós-progressiva também!
Quer que eu verifique os horários para tudo junto?
```

---

### Cenário 3: Cliente Pede Penteado

**Cliente:** "Quero fazer um penteado para casamento"

**Fluxo Automático:**
1. Brain identifica: `penteado_basico`
2. Chama API de sugestões
3. Retorna: make + manicure + sobrancelha

**Resposta do Brain:**
```
Ótima escolha! Para seu evento ficar perfeito...

Temos o pacote noiva completo!
Penteado + make + unhas + sobrancelha com 20% de desconto!

Quer que eu verifique a disponibilidade completa?
```

---

## 📝 SCRIPTS PRONTOS (CAMPAIGNS)

### Campanha 1: Combo Beleza Completa

**Válida:** 01/03/2026 - 31/03/2026  
**Desconto:** 15%  
**Serviços Alvo:** Escova Lisa, Escova Modelada  
**Add-ons:** Manicure, Pedicure, Design Sobrancelha

**Script Pronto:**
```
Enquanto consulto os horários de escova, você sabia que 
estamos com uma campanha especial?

Fazendo escova + manicure juntas, você ganha 15% de desconto!
Consigo encaixar tudo no mesmo horário. O que acha?
```

---

### Campanha 2: Dia da Noiva

**Válida:** 01/03/2026 - 31/03/2026  
**Desconto:** 20%  
**Serviços Alvo:** Penteado Premium, Make Premium  
**Add-ons:** Manicure, Pedicure, Design Sobrancelha, Lash Lifting

**Script Pronto:**
```
Para seu dia especial, temos o pacote noiva completo!
Penteado + make + unhas + sobrancelha com 20% de desconto.

Quer que eu verifique a disponibilidade?
```

---

### Campanha 3: Sobrancelha Perfeita

**Válida:** 01/03/2026 - 31/03/2026  
**Desconto:** 10%  
**Serviços Alvo:** Design Sobrancelha  
**Add-ons:** Brow Lamination, Lash Lifting

**Script Pronto:**
```
Enquanto isso, você conheceu nosso Brow Lamination?
Dura até 6 semanas e deixa as sobrancelhas perfeitas!

Está com 10% de desconto essa semana!
Quer adicionar?
```

---

## 🎯 UPSELL AUTOMÁTICO POR SERVIÇO

### Escova Lisa → Sugere:
- Manicure
- Pedicure
- Design Sobrancelha

**Script:**
```
Enquanto consulto os horários de escova, você sabia que 
conseguimos encaixar também sua manicure e pedicure no 
mesmo horário?

Assim você já sai completa! O que acha?
```

---

### Progressiva → Sugere:
- Manicure
- Pedicure
- Design Sobrancelha
- Hidratação (pós-progressiva)

**Script:**
```
Excelente! A progressiva leva um tempinho...

Que tal já deixar unhas e sobrancelhas prontas?
E temos hidratação especial pós-progressiva com 15% de desconto!

Quer que eu verifique os horários?
```

---

### Manicure → Sugere:
- Pedicure
- Gel Mãos

**Script:**
```
Já que vai fazer as unhas das mãos, que tal aproveitar 
e fazer os pés também?

E temos o gel que dura até 3 semanas!
Quer que eu verifique os horários?
```

---

## 📊 COMO ADICIONAR NOVAS CAMPANHAS

### Via API (Recomendado):

```bash
curl -X POST http://localhost:8000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nova Campanha",
    "description": "Descrição da campanha",
    "discount_percent": 15.00,
    "start_date": "2026-04-01",
    "end_date": "2026-04-30",
    "target_services": ["escova_lisa"],
    "add_on_services": ["manicure", "pedicure"],
    "campaign_script": "Script de vendas pronto"
  }'
```

### Via Supabase Dashboard:

1. Acessar https://supabase.com/dashboard
2. Abrir Table Editor
3. Selecionar `marketing_campaigns`
4. Clicar em "Insert"
5. Preencher dados da campanha

---

## 🚀 PRÓXIMOS PASSOS

### 1. Executar Migration no Supabase

```bash
# Acessar Supabase SQL Editor
# Copiar e colar: backend/marketing_campaigns_migration.sql
# Executar
```

### 2. Popular Dados de Exemplo

```bash
# O próprio migration já popula 3 campanhas e 6 upsells
# Validar no Supabase Dashboard
```

### 3. Testar APIs

```bash
# Testar campanhas ativas
curl http://localhost:8000/api/campaigns/active | python3 -m json.tool

# Testar upsell para escova
curl http://localhost:8000/api/upsell/escova_lisa | python3 -m json.tool

# Testar sugestão completa
curl http://localhost:8000/api/campaigns/suggest/escova_lisa | python3 -m json.tool
```

### 4. Integrar com Brain

```bash
# Reiniciar backend
docker compose restart luna-backend

# Testar conversa real
# Cliente pede "escova"
# Brain deve sugerir campanha automaticamente
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Backend:
- [x] Migration SQL criado
- [x] API de campanhas criada
- [x] API de upsell criada
- [x] Funções no brain.py adicionadas
- [x] API registrada no main.py
- [ ] Migration executado no Supabase ⏳
- [ ] Dados populados ⏳
- [ ] Testes realizados ⏳

### Frontend:
- [ ] Dashboard de campanhas (opcional)
- [ ] Visualizar campanhas ativas (opcional)

---

## 📝 RESUMO FINAL

### O Que Você Pode Fazer Agora:

1. ✅ **Campanhas com datas** (início e fim)
2. ✅ **Upsell automático** por serviço
3. ✅ **Scripts prontos** para usar na espera
4. ✅ **Descontos automáticos** (15%, 20%, 10%)
5. ✅ **Sugestões contextuais** (baseado no serviço)

### Exemplo de Uso Real:

**Cliente:** "Quero escova"

**Brain:**
1. Identifica serviço
2. Busca campanha ativa
3. Retorna script: "Enquanto consulto, sabia que temos 15% off em manicure?"
4. Cliente aceita
5. Brain agenda ambos serviços

---

**Próximo Passo:** Executar migration no Supabase! 🚀

```bash
# Acessar Supabase Dashboard
# SQL Editor
# Copiar: backend/marketing_campaigns_migration.sql
# Executar
```
