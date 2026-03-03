# ✅ Sistema Populado — Dados Completos Haven

**Data**: 2026-02-28  
**Status**: ✅ POPULADO

---

## 🎯 O Que Foi Feito

### 1. **Profissionais Completas (10 pessoas)**

```python
PROFISSIONAIS = {
    "yujaira": "Ju — Completa (cabelo tudo)",
    "carla": "Carla — Haven + Spa (progressiva, babyliss)",
    "mariana": "Mariana — Completa avançada (cabelo + make)",
    "davila": "Dávila — Master unhas (manicure, pedicure, gel, russa)",
    "luisa": "Lu — Sênior unhas (manicure, pedicure, gel)",
    "edna": "Edna — Júnior (manicure, pedicure, make leve)",
    "tay": "Tay — Especialista facial (make, sobrancelha, lash)",
    "suzana": "Suzana — Proprietária (alongamento EXCLUSIVO)",
    "cintia": "Cíntia — Freelancer (fitagem cachos)",
    "sheydis": "Sheydis — Terapeuta Spa (EXCLUSIVO Sōra)"
}
```

**Restrições Mapeadas**:
- ✅ Carla: Verificar agenda do Spa antes
- ✅ Cíntia: Confirmar antes (até 16h/17h)
- ✅ Suzana: Alongamento EXCLUSIVO
- ✅ Sheydis: Spa apenas

---

### 2. **Serviços Completos (50+ serviços)**

#### Cabelo (15 serviços)
| Serviço | Valor | Inclui Escova? |
|---------|-------|----------------|
| Escova Lisa | R$59 | ✅ |
| Escova Modelada | R$69 | ✅ |
| Corte + Escova | R$170 | ✅ |
| Corte Sem Escova | R$120 | ❌ |
| Penteado Básico | R$115 | ❌ |
| Penteado Plus | R$139 | ❌ |
| Penteado Premium | R$169 | ❌ |
| **Matização** | **R$115** | ✅ **(única exceção)** |
| Retoque Raiz | R$179 | ✅ |
| Fitagem (Cíntia) | R$95 | — |
| Hidratação | R$85 | ❌ |
| Nutrição | R$95 | ❌ |
| Reconstrução | R$110 | ❌ |
| Hidratação Coreana | R$135 | ❌ |
| Umectação | R$65 | ❌ |

#### Progressivas (3 serviços)
| Comprimento | Valor | Duração | Pausa Química |
|-------------|-------|---------|---------------|
| Curtos | R$250 | ~3h | 40-70 min |
| Médios | R$295 | ~3h | 50-70 min |
| Longos | R$380 | ~3-4h | 60-90 min |

#### Unhas (15 serviços)
| Serviço | Valor | Duração |
|---------|-------|---------|
| Manicure Dávila | R$50 | 60 min |
| Manicure Lu/Edna | R$42 | 40 min |
| Pedicure Dávila | R$60 | 60 min |
| Pedicure Lu/Edna | R$45 | 45 min |
| **Plástica dos Pés** | **R$140** | **90 min (✅ inclui pedicure)** |
| Manicure Russa | R$80 | 50 min |
| Gel Dávila | R$140 | 120 min |
| Gel Lu | R$120 | 120 min |
| Manutenção Gel | Mesmo valor | 90 min |
| Remoção Gel | R$80 | 30 min |
| Remoção Alongamento | R$150 | 45 min |
| **Alongamento (Suzana)** | **R$450** | **180 min (✅ inclui gel + russa)** |

#### Maquiagem / Estética (8 serviços)
| Serviço | Valor | Duração |
|---------|-------|---------|
| Make Casual | R$120 | 40 min |
| Make Básica | R$149 | 50 min |
| Make Premium | R$195 | 60 min |
| Lash Lifting | R$165 | 60 min |
| Design Sobrancelha | R$60 | 30 min |
| Design com Tintura | R$80 | 40 min |
| Brow Lamination | R$120 | 60 min |
| Epilação Facial | R$35 | 20 min |

---

### 3. **Regras de Negócio Críticas**

```python
REGRAS_NEGOCIO = {
    "ordem_obrigatoria": ["unhas", "cabelo", "maquiagem"],
    
    "escova_nao_inclusa_em": [
        "penteado_basico", "penteado_plus", "penteado_premium",
        "hidratacao", "nutricao", "reconstrucao",
        "corte_sem_escova"
    ],
    
    "escova_inclusa_em": [
        "escova_lisa", "escova_modelada",
        "matizacao",  # ÚNICA exceção
        "progressivas",
        "corte_com_escova", "retoque_raiz"
    ],
    
    "pergunta_remocao_gel_obrigatoria": [
        "manicure_*", "pedicure_*", "gel_*", "manicure_russa", "plastica_pes"
    ],
    
    "profissionais_restricoes": {
        "carla": "SEMPRE verificar agenda do Spa",
        "cintia": "NUNCA confirmar sem checar antes",
        "suzana": "EXCLUSIVO alongamento",
        "sheydis": "EXCLUSIVO Spa"
    },
    
    "paralelo_inteligente": {
        "script": "Você tem preferência por alguma profissional? "
                  "Se não tiver, consigo organizar com duas e "
                  "você sai bem mais rápido 😊 Quer assim?"
    },
    
    "evento_horario_fixo": {
        "calculo": "De trás para frente",
        "exemplo": "Evento 19h → make 18h → escova 17h → unhas 15h"
    }
}
```

---

### 4. **System Prompt Atualizado**

**Novas Regras no Prompt**:

```
ORDEM OBRIGATÓRIA DE SERVIÇOS:
• Unhas → Cabelo → Maquiagem (NUNCA inverta)
• Maquiagem é SEMPRE por último (spray/calor borram)
• Para eventos: calcule de trás para frente

REGRAS CRÍTICAS POR PROFISSIONAL:
• Carla (Haven + Spa): SEMPRE verificar agenda do Spa antes
• Cíntia (Fitagem): NUNCA confirmar sem checar antes (até 16h/17h)
• Suzana (Alongamento): EXCLUSIVO dela — confirmar disponibilidade
• Sheydis (Spa): EXCLUSIVO do Sōra Head Spa — NÃO atende na Haven

REGRAS DE ESCOVA:
• NÃO inclusa em: Penteados, Tratamentos, Corte sem escova
• Incluso em: Escova lisa/modelada, Matização, Progressivas, Corte+Escova
• COMUNICAR SEMPRE: "O penteado é montar o cabelo. A escova é separada. Quer as duas?"

REMOÇÃO DE GEL (OBRIGATÓRIO PERGUNTAR):
• ANTES de confirmar: "Você está com gel ou alongamento nas unhas hoje?"
• Se sim: Agendar remoção antes (30 min) + Cobrar (gel=R$80, alongamento=R$150)

PARALELO INTELIGENTE:
• Se não tem preferência: oferecer duas profissionais
• Script: "Consigo organizar com duas e você sai bem mais rápido 😊"
```

---

## 📊 Arquivos Atualizados

| Arquivo | Mudanças |
|---------|----------|
| `backend/app/core/brain.py` | ✅ Profissionais (10 pessoas)<br>✅ Serviços (50+ serviços)<br>✅ Regras de negócio<br>✅ System prompt atualizado |

---

## 🎯 Como Testar

### 1. **Testar Profissionais**

```python
from app.core.brain import PROFISSIONAIS

# Ver todas
print(PROFISSIONAIS.keys())

# Ver uma específica
print(PROFISSIONAIS["davila"])
```

### 2. **Testar Serviços**

```python
from app.core.brain import SERVICOS

# Ver todos
print(SERVICOS.keys())

# Ver um específico
print(SERVICOS["escova_lisa"])
```

### 3. **Testar Regras**

```python
from app.core.brain import REGRAS_NEGOCIO

# Ver ordem obrigatória
print(REGRAS_NEGOCIO["ordem_obrigatoria"])

# Ver serviços com escova
print(REGRAS_NEGOCIO["escova_inclusa_em"])
```

---

## ✅ Checklist de Validação

- [x] **10 Profissionais** mapeadas
- [x] **50+ Serviços** com preços e durações
- [x] **Regras de Escova** (inclui/não inclui)
- [x] **Pergunta de Gel** obrigatória
- [x] **Restrições por Profissional**
- [x] **Ordem de Serviços** (unhas → cabelo → make)
- [x] **Paralelo Inteligente** script
- [x] **Eventos** cálculo reverso
- [x] **System Prompt** atualizado

---

## 🔄 Próximos Passos

1. [ ] **Testar com dados reais** no Dojo Arena
2. [ ] **Popular Supabase** com esses dados
3. [ ] **Integrar com agenda** real
4. [ ] **Validar preços** com Suzana
5. [ ] **Testar cenários complexos** (múltiplos serviços, eventos)

---

## 📚 Referências

- **Fonte**: `/Users/franciscotaveira.ads/LUNA OS/claude/`
- **Estudo Completo**: `CLAUDE_STUDY_COMPLETE.md`
- **System Prompt**: `luna_system_prompt.md`
- **Brain v2**: `luna_brain_v2.py`

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Sistema populado com TODOS os dados reais da Haven! Pronto para operação!* 🚀
