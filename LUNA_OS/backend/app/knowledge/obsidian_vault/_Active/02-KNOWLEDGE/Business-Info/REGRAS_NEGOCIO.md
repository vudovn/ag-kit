---
tags:
  - business
  - regras
  - haven
created_at: 2026-03-01
source: config_haven.py
---

# 📜 Regras de Negócio Haven

**Última Atualização:** 2026-03-01  
**Fonte:** `backend/app/core/config_haven.py`

---

## 🎯 Regras Soberanas

### 1. Ordem Obrigatória de Serviços

Para múltiplos serviços, seguir ordem:
```
1. Unhas
2. Cabelo
3. Maquiagem
```

**Motivo:** Unhas primeiro para não danificar com produtos de cabelo.

---

### 2. Escova Incluída vs Não Incluída

#### ✅ Escova NÃO Incluída em:
- Penteado Básico/Plus/Premium
- Hidratação
- Nutrição
- Reconstrução Capilar
- Hidratação Coreana
- Umectação
- Corte (Sem Escova)
- Matização Sem Escova

#### ✅ Escova Incluída em:
- Escova Lisa
- Escova Modelada
- Matização + Escova
- Corte + Escova Lisa
- Progressiva (todos)

**Regra:** SEMPRE comunicar se escova está incluída ou não.

---

### 3. Pergunta de Remoção de Gel

**Obrigatório perguntar** para serviços de unhas:
- Manicure (Dávila/Lu)
- Pedicure (Dávila/Lu)
- Gel (Dávila/Lu)
- Manicure Russa
- Plástica dos Pés

**Script:**
> "Você tem gel ou alongamento para remover? 😊"

---

### 4. Profissionais com Restrições

#### Carla (Haven + Sōra Spa)
- ⚠️ **SEMPRE** verificar agenda do Spa antes de confirmar Haven
- Manicure somente em contingência

#### Tay (Estética Facial)
- ⚠️ **NUNCA** confirmar sem checar com Cíntia antes
- Disponibilidade limitada (até 16h)

#### Sheydis (Sōra Spa)
- 🔴 **EXCLUSIVO** Sōra Head Spa
- **NÃO** atende na Haven Escovaria

#### Suzana (Proprietária)
- 🔴 **EXCLUSIVO** Alongamento de Unhas
- Confirmar disponibilidade antes de vender

---

### 5. Paralelo Inteligente

**Quando cliente não tem preferência:**
> "Você tem preferência por alguma profissional? Se não tiver, consigo organizar com duas e você sai bem mais rápido! 😊 Quer assim?"

**Benefício:** Reduz tempo de espera em 40-60%.

---

### 6. Evento com Horário Fixo

**Calcular de trás para frente:**

Exemplo: Evento às 19h
```
19h → Evento
18h → Make (1h antes)
17h → Escova (1h antes da make)
15h → Unhas (2h antes da escova)
```

**Regra:** Sempre perguntar horário do evento e calcular backwards.

---

### 7. Pausa Química

**Obrigatório para serviços químicos:**

| Serviço | Pausa Mínima | Pausa Máxima |
|---------|--------------|--------------|
| Progressiva Curtos | 40 min | 70 min |
| Progressiva Médios | 50 min | 70 min |
| Progressiva Longos | 60 min | 90 min |
| Retoque de Raiz | 30 min | - |

**Regra:** Agendar janela adequada para pausa química.

---

### 8. Valores e Preços

**NUNCA inventar preços!** Sempre consultar:
- `Brain/Services/SVC-*.md`
- `backend/app/core/config_haven.py`
- `backend/app/knowledge/data/haven.json`

**Fallback se não encontrar:**
> "Deixa eu verificar o valor exato para você! 😊 Um momento..."

---

### 9. Confirmação de Horário

**NUNCA confirmar horário sem verificar disponibilidade:**
- Consultar Belasis API (ou mock)
- Verificar agenda da profissional
- Confirmar com cliente

**Script de confirmação:**
> "Tenho horário às [HORÁRIO] com [PROFISSIONAL]. Posso confirmar para você? 😊"

---

### 10. Handoff (Transferência para Humano)

**Quando acionar handoff:**
- Cliente pede "falar com humano"
- Reclamação não resolvida
- Dúvida complexa sobre preços/serviços
- Sistema indisponível
- Cliente insatisfeito

**Script:**
> "Claro! Vou chamar uma pessoa da nossa equipe para te atender melhor. Um momento! 😊"

---

## 📊 Matriz de Decisão

| Situação | Ação |
|----------|------|
| Cliente sem preferência | Oferecer paralelo inteligente |
| Cliente com horário fixo | Calcular backwards |
| Múltiplos serviços | Seguir ordem: unhas → cabelo → make |
| Serviço químico | Agendar pausa química |
| Dúvida de preço | Consultar KB, nunca inventar |
| Horário indisponível | Oferecer alternativas |
| Cliente insatisfeito | Handoff |

---

## 🔗 Links Relacionados

- [[PROFISSIONAIS_HAVEN]]
- [[SERVICOS_HAVEN]]
- [[LUNA_SYSTEM_PROMPT]]
- [[000_MCT_MASTER_INDEX]]

---

*Documento gerado automaticamente via Agent Flow - 2026-03-01*
