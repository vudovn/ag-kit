---
tags:
  - business
  - profissionais
  - haven
created_at: 2026-03-01
source: config_haven.py
---

# 👥 Profissionais Haven - Fonte da Verdade

**Última Atualização:** 2026-03-01  
**Fonte:** `backend/app/core/config_haven.py`

---

## 📋 Resumo

| Profissional | Apelido | Empresa       | Nível        | Especialidade   |
| ------------ | ------- | ------------- | ------------ | --------------- |
| Yujaira      | Ju      | Haven         | completa     | Cabelo          |
| Carla        | Carla   | Haven + Sōra  | senior       | Progressiva/Spa |
| Dávila       | Dávila  | Haven         | master_unhas | Unhas           |
| Tay          | Tay     | Haven         | especialista | Estética Facial |
| Sheydis      | Sheydis | Sōra Head Spa | terapeuta    | Spa             |

---

## 👤 Yujaira (Ju)

**Empresa:** Haven  
**Nível:** Completa  
**Especialidade:** Cabelo

### ✅ Faz:
- Penteado
- Trancas
- Progressiva
- Tintura Simples
- Corte Feminino
- Escova
- Hidratação
- Sobrancelha Simples

### ❌ Não Faz:
- Unhas
- Maquiagem

### ⚠️ Restrições:
- Design sobrancelha somente quando Tay indisponível ou agenda lotada
- Penteados elaborados e progressivas: não agendar em janelas pequenas

---

## 👤 Carla

**Empresa:** Haven + Sōra Head Spa  
**Nível:** Senior  
**Especialidade:** Progressiva/Tratamentos

### ✅ Faz na Haven:
- Progressiva
- Escova Babyliss
- Tratamentos Capilares
- Penteado Básico
- Coloração

### ✅ Faz no Sōra Spa:
- Ritual Ashi
- Pausa Nagi
- Cuidado Hikari
- Conexão Mizu
- Spa Pés
- Spa Mãos

### ⚠️ Restrições:
- Manicure somente contingência, não atividade principal
- SEMPRE verificar agenda do Spa antes de confirmar horário na Haven

---

## 👤 Dávila

**Empresa:** Haven  
**Nível:** Master Unhas  
**Especialidade:** Unhas

### ✅ Faz:
- Manicure Tradicional
- Pedicure Tradicional
- Gel Mãos
- Gel Pés
- Blindagem
- Banho de Gel
- Fibra de Vidro
- Esmaltação em Gel
- Plástica Pés
- Spa Pés

### ⚠️ Exceções:
- Escova Básica
- Lavatório
- Manicure Tradicional
- Pedicure Tradicional
- Maquiagem Leve

### 💰 Valores:
- Manicure: R$ 42,00
- Pedicure: R$ 45,00

---

## 👤 Tay

**Empresa:** Haven  
**Nível:** Especialista Estética Facial  
**Especialidade:** Sobrancelha/Maquiagem

### ✅ Faz:
- Maquiagem Casual
- Maquiagem Social
- Maquiagem Festa
- Sobrancelha Henna
- Sobrancelha Simples
- Design Sobrancelha
- Brow Lamination
- Epilação Facial

### ⚠️ Exceções:
- Arrumar Cabelo Básico
- Babyliss Simples

### ❌ Não Faz:
- Unhas
- Química Cabelo
- Corte

### 🕐 Disponibilidade:
- Semana: até 16h
- Sábado: até 16h/17h máximo

### 📋 Protocolo:
- NUNCA confirmar sem checar com Cíntia antes

---

## 👤 Sheydis

**Empresa:** Sōra Head Spa  
**Nível:** Terapeuta Spa  
**Especialidade:** Tratamentos Spa

### ✅ Faz:
- Ritual Ashi
- Pausa Nagi
- Cuidado Hikari
- Conexão Mizu
- Spa Pés

### ❌ Não Faz:
- Cabelo
- Escova
- Unhas
- Maquiagem
- Sobrancelha

### ⚠️ Restrição Crítica:
**EXCLUSIVAMENTE Sōra Head Spa. NÃO atende na Haven Escovaria.**

---

## 📊 Matriz de Competências

| Serviço | Yujaira | Carla | Dávila | Tay | Sheydis |
|---------|---------|-------|--------|-----|---------|
| Cabelo | ✅ | ✅ | ❌ | ⚠️ | ❌ |
| Unhas | ❌ | ❌ | ✅ | ❌ | ❌ |
| Maquiagem | ❌ | ⚠️ | ⚠️ | ✅ | ❌ |
| Sobrancelha | ⚠️ | ❌ | ❌ | ✅ | ❌ |
| Spa | ❌ | ✅ | ⚠️ | ❌ | ✅ |

**Legenda:**
- ✅ = Faz regularmente
- ⚠️ = Faz exceções/emergências
- ❌ = Não faz

---

## 🔗 Links Relacionados

- [[REGRAS_NEGOCIO]]
- [[SERVICOS_HAVEN]]
- [[000_MCT_MASTER_INDEX]]

---

*Documento gerado automaticamente via Agent Flow - 2026-03-01*
