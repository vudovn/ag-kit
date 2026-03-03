# ✅ ATUALIZAÇÃO COMPLETA - PROTOCOLO HAVEN

**Data:** 2026-03-01  
**Status:** ✅ **ATUALIZADO COM PROTOCOLO OFICIAL**  
**Base:** Protocolo WhatsApp Haven.pdf (Aprovado pela Proprietária)

---

## 📋 ARQUIVOS ATUALIZADOS

### 1. `backend/app/core/config_haven.py` ✅

**O Que Mudou:**

#### Profissionais (7 Fixas + 1 Freelancer + 1 Exclusivo)
- ✅ **Yujaira (Ju)**: Cabelo completo, penteados, folga terça
- ✅ **Carla**: Progressiva + Spa (agenda dividida), verificar conflito
- ✅ **Mariana**: Cores complexas, atende tarde ter-qui (12h+)
- ✅ **Dávila**: Manicure avançada, seg-sáb 8h-17h
- ✅ **Lu**: Manicure e gel, ter-sáb 8h-20h
- ✅ **Edna**: Manicure tradicional, seg-ter e qui-sáb
- ✅ **Tay**: Maquiagem + sobrancelhas, ter-sáb
- ✅ **Cíntia**: Freelancer fitagem, confirmar antes (até 16h)
- ✅ **Suzana**: Alongamento EXCLUSIVO, R$450

#### Serviços e Preços Oficiais
- ✅ **40+ serviços** com preços atualizados
- ✅ **Promoções seg-qua** implementadas
- ✅ **Alertas de "não inclui escova"** em tratamentos
- ✅ **Pausas químicas** para progressiva/tintura
- ✅ **Pergunta obrigatória de remoção de gel**

#### Regras de Negócio
- ✅ Ordem: cabelo → unhas → maquiagem
- ✅ Upsell de lavatório (coreanos +R$30, Labrizza +R$25, Kérastase +R$30)
- ✅ Cupons blogueiras (10%: PRISCILA10, EWYLIN10, etc.)
- ✅ Pacotes de gel e escova com validade
- ✅ Gatilhos de handoff para reclamações

---

### 2. `backend/app/knowledge/data/haven.json` ✅

**Estrutura Atualizada:**
```json
{
  "business": {...},
  "services": [40+ serviços],
  "professionals": [9 profissionais],
  "coupons": [5 cupons],
  "packages": [4 pacotes],
  "upsell": {...},
  "rules": {...}
}
```

---

## 🎯 MUDANÇAS CRÍTICAS

### 1. Preços Atualizados

| Serviço | Preço Antigo | Preço Novo |
|---------|--------------|------------|
| Escova Lisa | R$59 | R$59 (promo seg-qua: R$49) |
| Escova Modelada | R$69 | R$69 (promo seg-qua: R$49) |
| Penteado Básico | R$115 | R$115 (promo seg-qua: R$99) |
| Manicure | R$42-50 | R$42-50 (correto) |
| Gel | R$120-140 | R$120-140 (correto) |
| Remoção Gel | ❌ Não tinha | ✅ R$30 (30 min) |
| Alongamento | ❌ Genérico | ✅ R$450 (Suzana exclusivo) |

### 2. Profissionais com Horários Reais

| Profissional | Horário | Observação |
|--------------|---------|------------|
| Ju | Seg/Qua-Sáb 8h-20h | Folga terça |
| Carla | Ter-Sáb 8h-20h | Verificar Spa |
| Mariana | Ter-Qui 12h-17:30, Sex-Sáb 8h-20h | Tarde ter-qui |
| Dávila | Seg-Sáb 8h-17h | Fecha 17h |
| Lu | Ter-Sáb 8h-20h | - |
| Edna | Seg-Ter, Qui-Sáb 8h-20h | Folga qua |
| Tay | Ter-Sáb 8h-20h | - |
| Cíntia | Seg-Sáb até 16h | Freelancer |
| Suzana | Por confirmar | Exclusivo alongamento |

### 3. Regras de Negócio Implementadas

#### ✅ Pergunta Obrigatória de Remoção
```python
# Quando cliente pede manicure/pedicure/gel
"Você está com gel ou alongamento nas mãos ou nos pés?"
# Remoção: R$30, 30 minutos
```

#### ✅ Alertas de "Não Inclui Escova"
```python
# Tratamentos, penteados, corte sem escova
"Esse valor é só do tratamento; escova é à parte."
"Penteado não inclui escova; se quiser escova antes, soma."
```

#### ✅ Ordem dos Procedimentos
```
1. Cabelo (primeiro, lavar antes da maquiagem)
2. Unhas (dá para fazer junto)
3. Maquiagem (sempre por último)
```

#### ✅ Pausas Químicas
```
Progressiva: 40-90 min de pausa (produto agindo)
Tintura: ~40 min de pausa
Durante pausa: pode encaixar serviço rápido
```

### 4. Cupons Oficiais

| Cupom | Blogueira | Desconto |
|-------|-----------|----------|
| PRISCILA10 | Priscila Kuhn | 10% |
| EWYLIN10 | Ewylin Salvatori | 10% |
| SOLANGE10 | Solange | 10% |
| CAROLINE10 | Caroline | 10% |
| KETLYN10 | Ketlyn | 10% |

### 5. Pacotes Oficiais

#### Pacote Gel (Mãos)
- **3 aplicações**: R$99 (Lu) / R$120 (Dávila) → 60 dias
- **6 aplicações**: R$99 (Lu) / R$120 (Dávila) → 120 dias

#### Pacote Escovas
- **4 escovas**: Lisa R$55, Modelada R$65 → 30 dias
- **8 escovas**: Lisa R$52, Modelada R$59 → 60 dias

#### Pacote Unhas Tradicionais
- **4 mãos**: R$45 (Dávila) / R$38 (outras) → 30 dias
- **4 mãos + 1 pé**: 30 dias
- **4 mãos + 2 pés**: 40 dias

---

## 🧠 SCRIPTS DE ATENDIMENTO IMPLEMENTADOS

### Abertura
```
"Oi! Seja bem-vinda à Haven 😊
Me diz por favor: qual procedimento você quer fazer e para qual dia/horário você está pensando?"
```

### Diagnóstico Rápido
```
"É para algum evento com horário certo?
E nas unhas: você está com gel ou alongamento hoje?"
```

### Pergunta de Remoção (OBRIGATÓRIA)
```
"Você está com gel ou alongamento nas mãos ou nos pés?"
```

### Otimização de Tempo
```
"Você tem preferência por alguma profissional?
Se não tiver, eu consigo otimizar seu tempo e organizar para fazer com duas profissionais e você sair mais rápido!"
```

### Retenção (Sem Horário)
```
"Entendi, para {procedimento} no {dia} nesse horário específico, hoje a agenda fechou.
Mas eu consigo te ajudar agora com duas opções bem próximas: {opcao1} ou {opcao2}.
Se você tiver flexibilidade, eu também posso tentar encaixe.
E se preferir, te coloco na lista de prioridade para te chamar se surgir vaga."
```

### Confirmação Final
```
"Fechado, {nome} 😊
Agendado {procedimento} no {dia} às {hora}.
Você já sabe nossa localização ou quer que eu te envie o endereço certinho?
Temos estacionamento em frente ao prédio e também 4 vagas na esquina, caso você prefira não deixar na rua."
```

### Upsell Lavatório
```
"Na conversa eu já te passo o valor base com os produtos da casa 😊
No lavatório, se você quiser, a equipe oferece opções premium com acréscimo (coreanos, Labriza ou Kérastase), sempre informando o valor antes.
Você só escolhe se quiser, tá!"
```

### Reclamação
```
"Entendi, obrigada por avisar.
Me manda por favor as fotos e confirma pra mim a data e o procedimento?
Vou encaminhar para avaliação e a gente já te dá a melhor solução pra você sair satisfeita."
```

---

## 🚨 GATILHOS DE HANDOFF (Blindados)

```python
HANDOFF_TRIGGERS = [
    "procon", "advogado", "processar", "reclamação formal",
    "danos morais", "jurídico", "defesa do consumidor",
    "quero falar com a proprietária", "quero falar com a Suzana",
    "isso é um absurdo", "vou denunciar"
]
```

**Script de Handoff:**
```
"Entendi perfeitamente. Vou encaminhar seu caso para avaliação da nossa equipe.
Alguém entrará em contato em breve para te dar a melhor solução. 😊"
```

---

## ✅ CORREÇÕES DE BUGS

### 1. Validação Explícita no Learning Cycle

**Antes:**
```python
if not feedbacks:
    # Retornava vazio sem log claro
```

**Depois:**
```python
if not feedbacks:
    logger.info("✅ No negative feedbacks to process this week")
    return {
        "success": True,
        "message": "No feedbacks found - system working well",
        "proposals_generated": 0
    }
```

### 2. Fallback Seguro no Pipeline

**Antes:**
```python
# Processava mesmo sem mensagens
```

**Depois:**
```python
if not messages or len(messages) < 2:
    return {
        "success": False,
        "error": "Insufficient messages for intelligence analysis"
    }
```

### 3. Handoff Blindado

**Adicionado:**
```python
HANDOFF_TRIGGERS = [...]  # Lista oficial do protocolo

if any(trigger in message_lower for trigger in HANDOFF_TRIGGERS):
    return "handoff", "Legal/Regulatory issue - requires human"
```

---

## 📊 PRÓXIMOS PASSOS

### 1. Testar com Dados Reais
```bash
# Reiniciar backend
docker compose restart luna-backend

# Testar endpoint
curl http://localhost:8000/api/dojo/proposals
```

### 2. Validar no Dojo Arena
- Criar cenários baseados no protocolo
- Testar scripts de atendimento
- Validar gatilhos de handoff

### 3. Popular Knowledge Base
```bash
# Executar seed
python backend/app/scripts/seed_haven.py
```

### 4. Treinar Equipe
- Distribuir scripts de atendimento
- Validar conhecimento de preços
- Treinar pergunta de remoção de gel

---

## 📞 SUPORTE

**Dúvidas sobre o protocolo:**
- Consultar `Protocolo WhatsApp Haven.pdf`
- Verificar `config_haven.py` para regras
- Checar `haven.json` para preços

**Erros encontrados:**
- Reportar com screenshot
- Incluir log do erro
- Especificar cenário do Dojo

---

**Atualização Finalizada:** 2026-03-01  
**Próxima Revisão:** 2026-03-08 (7 dias)  
**Responsável:** Dev Team
