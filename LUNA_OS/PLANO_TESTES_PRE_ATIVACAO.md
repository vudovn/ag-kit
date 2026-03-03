# 🧪 PLANO DE TESTES - PRÉ-ATIVAÇÃO LUNA OS

**Data:** 2026-03-01  
**Status:** ⚠️ **EM TESTES**  
**Ativação:** ⚠️ **BLOQUEADA ATÉ APROVAÇÃO**

---

## 🎯 OBJETIVO

Garantir que LUNA OS funcione corretamente **ANTES** de ativar `LUNA_MODE=active`.

**Critério de Aprovação:** 95% de sucesso nos testes

---

## 📋 CHECKLIST DE TESTES

### FASE 1: Testes Unitários (Brain.py)

#### Teste 1.1: `analisar_compatibilidade_servicos()`
```python
# Teste: Progressiva + Manicure
servicos = ["progressiva_curtos", "manicure"]
resultado = analisar_compatibilidade_servicos(servicos)

# Esperado:
assert resultado["compativel"] == True
assert "manicure" in resultado["servicos_simultaneos"]
assert resultado["tempo_total_min"] < 230  # Economia de 50 min
assert "pausa química" in resultado["justificativa"].lower()
```

#### Teste 1.2: `analisar_compatibilidade_servicos()` - Make + Cabelo
```python
# Teste: Make + Escova
servicos = ["make_casual", "escova_lisa"]
resultado = analisar_compatibilidade_servicos(servicos)

# Esperado:
assert resultado["compativel"] == True
assert resultado["ordem_recomendada"] == ["escova_lisa", "make_casual"]
assert "último" in resultado["justificativa"].lower()
```

#### Teste 1.3: `calcular_tempo_total()`
```python
# Teste: Progressiva + Manicure (com otimização)
servicos = ["progressiva_curtos", "manicure"]
tempo = calcular_tempo_total(servicos, simultaneo=True)

# Esperado:
assert tempo < 230  # 180 + 40 - 50 (economia)
assert tempo > 170  # Mínimo razoável
```

#### Teste 1.4: `calcular_tempo_total()` - Sem otimização
```python
# Teste: Make + Escova (sem otimização)
servicos = ["make_casual", "escova_lisa"]
tempo = calcular_tempo_total(servicos, simultaneo=False)

# Esperado:
assert tempo == 90  # 50 + 40
```

---

### FASE 2: Testes de Integração (Seed Supabase)

#### Teste 2.1: Executar seed_haven.py
```bash
cd backend
python app/scripts/seed_haven.py
```

**Critério de Sucesso:**
- ✅ 41 serviços inseridos
- ✅ 9 profissionais inseridos
- ✅ 5 cupons inseridos
- ✅ 4 pacotes inseridos
- ✅ 4 FAQs inseridos
- ✅ 1 business_info inserido
- ✅ Total: 64 registros

#### Teste 2.2: Validar dados no Supabase
```python
# Verificar serviços
services = supabase.table("knowledge_base").select("*").eq("category", "services").execute()
assert len(services.data) == 41

# Verificar profissionais
professionals = supabase.table("knowledge_base").select("*").eq("category", "professionals").execute()
assert len(professionals.data) == 9

# Verificar preços
progressiva = supabase.table("knowledge_base").select("*").eq("key", "service_progressiva_curtos").execute()
assert progressiva.data[0]["data"]["price"] == 250.00
```

---

### FASE 3: Testes Dojo Scenarios

#### Teste 3.1: Executar 10 cenários de atendimento
```bash
cd backend
python app/dojo/run_scenarios.py --scenarios haven --min-pass 8
```

**Critério de Sucesso:**
- ✅ 8/10 cenários aprovados (80%)
- ✅ Pontos críticos (handoff, remoção gel) 100%

#### Teste 3.2: Executar 5 cenários de estresse
```bash
cd backend
python app/dojo/run_scenarios.py --scenarios haven-stress --min-pass 4
```

**Critério de Sucesso:**
- ✅ 4/5 cenários aprovados (80%)
- ✅ Handoff em reclamações 100%

---

### FASE 4: Testes End-to-End (WhatsApp Simulation)

#### Teste 4.1: Agendamento Progressiva + Manicure
```
Cliente: "Quero fazer progressiva e manicure sábado"
Esperado:
- ✅ LUNA oferece otimização de tempo
- ✅ Explica pausa química (50 min economia)
- ✅ Pergunta profissional preferência
- ✅ Tempo total: ~3h (não 3h50)
```

#### Teste 4.2: Pergunta Obrigatória Remoção
```
Cliente: "Quero manicure amanhã"
Esperado:
- ✅ Pergunta "Tem gel ou alongamento?"
- ✅ Informa remoção: R$ 30, 30 min
- ✅ Soma ao tempo total
```

#### Teste 4.3: Cupom Blogueira
```
Cliente: "Tenho cupom PRISCILA10"
Esperado:
- ✅ Confirma cupom válido
- ✅ Calcula 10% desconto
- ✅ Aplica no valor total
```

#### Teste 4.4: Make + Cabelo - Ordem
```
Cliente: "Quero make e escova para casamento"
Esperado:
- ✅ Explica make sempre por último
- ✅ Sugere escova primeiro
- ✅ Explica razão (calor estraga make)
```

#### Teste 4.5: Fitagem - Confirmar Cíntia
```
Cliente: "Quero fitagem sábado 10h"
Esperado:
- ✅ Alerta precisa confirmar com Cíntia
- ✅ Menciona horário limite 16h
- ✅ NÃO confirma sem verificar
```

#### Teste 4.6: Alongamento - Exclusivo Suzana
```
Cliente: "Quero alongamento"
Esperado:
- ✅ Informa exclusivo Suzana
- ✅ Informa valor R$ 450
- ✅ Confirma disponibilidade antes
```

#### Teste 4.7: Reclamação - Handoff
```
Cliente: "Unha descascou em 2 dias!"
Esperado:
- ✅ Recebe com educação
- ✅ Pede fotos
- ✅ Aciona handoff Suzana
```

---

### FASE 5: Testes de Performance

#### Teste 5.1: Tempo de Resposta Brain.py
```python
import time

start = time.time()
analisar_compatibilidade_servicos(["progressiva_curtos", "manicure", "pedicure"])
end = time.time()

# Esperado:
assert (end - start) < 0.5  # < 500ms
```

#### Teste 5.2: Tempo de Resposta seed_haven.py
```bash
time python app/scripts/seed_haven.py

# Esperado:
# real < 10s
```

---

### FASE 6: Testes de Validação com Protocolo Haven

#### Teste 6.1: Todos Preços Corretos
```python
# Verificar 41 serviços com preços do protocolo
servicos_precos = {
    "escova_lisa": 59.00,
    "escova_modelada": 69.00,
    "penteado_basico": 115.00,
    "progressiva_curtos": 250.00,
    "progressiva_medios": 295.00,
    "progressiva_longos": 380.00,
    "manicure": 50.00,
    "pedicure": 60.00,
    "gel_maos": 140.00,
    "make_casual": 120.00,
    # ... todos os 41 serviços
}

for servico, preco_esperado in servicos_precos.items():
    servico_db = supabase.table("knowledge_base").select("*").eq("key", f"service_{servico}").execute()
    assert servico_db.data[0]["data"]["price"] == preco_esperado
```

#### Teste 6.2: Profissionais com Horários Corretos
```python
# Verificar 9 profissionais com horários do protocolo
profissionais_horarios = {
    "yujaira": {"folga": "terca", "horario": "08:00-20:00"},
    "carla": {"horario": "08:00-20:00", "spa": True},
    "mariana": {"horario": "12:00-17:30 ter-qui, 12:00-20:00 sex-sáb"},
    # ... todos os 9 profissionais
}
```

#### Teste 6.3: Cupons Blogueiras
```python
# Verificar 5 cupons
cupons_esperados = ["PRISCILA10", "EWYLIN10", "SOLANGE10", "CAROLINE10", "KETLYN10"]

for cupom in cupons_esperados:
    cupom_db = supabase.table("knowledge_base").select("*").eq("key", f"coupon_{cupom}").execute()
    assert len(cupom_db.data) == 1
    assert cupom_db.data[0]["data"]["discount"] == 0.10
```

---

## 📊 CRITÉRIOS DE APROVAÇÃO

### Para Ativar LUNA_MODE=active:

| Fase | Testes | Mínimo Aprovação | Status |
|------|--------|------------------|--------|
| **Fase 1: Unitários** | 4 testes | 100% | ⏳ Pendente |
| **Fase 2: Seed Supabase** | 2 testes | 100% | ⏳ Pendente |
| **Fase 3: Dojo** | 15 cenários | 80% | ⏳ Pendente |
| **Fase 4: End-to-End** | 7 testes | 100% | ⏳ Pendente |
| **Fase 5: Performance** | 2 testes | 100% | ⏳ Pendente |
| **Fase 6: Protocolo** | 3 testes | 100% | ⏳ Pendente |

### **APROVAÇÃO FINAL:**
- ✅ **Todas as 6 fases aprovadas**
- ✅ **Mínimo 95% sucesso geral**
- ✅ **Críticos (handoff, remoção, preços) 100%**

---

## 🧪 SCRIPT DE TESTES AUTOMATIZADOS

### Criar: `backend/tests/test_luna_production.py`

```python
#!/usr/bin/env python3
"""
🧪 Testes de Produção - LUNA OS

Executa todos os testes antes de ativar LUNA_MODE=active
"""

import pytest
import sys
from app.core.brain import (
    analisar_compatibilidade_servicos,
    calcular_tempo_total,
    gerar_script_multi_servicos
)

class TestBrainFisica:
    """Testes da física dos procedimentos"""
    
    def test_progressiva_manicure_compativel(self):
        """Progressiva + Manicure devem ser compatíveis com otimização"""
        servicos = ["progressiva_curtos", "manicure"]
        resultado = analisar_compatibilidade_servicos(servicos)
        
        assert resultado["compativel"] == True
        assert "manicure" in resultado["servicos_simultaneos"]
        assert resultado["tempo_total_min"] < 230
        assert "pausa" in resultado["justificativa"].lower()
    
    def test_make_cabelo_ordem(self):
        """Make deve ser sempre por último"""
        servicos = ["make_casual", "escova_lisa"]
        resultado = analisar_compatibilidade_servicos(servicos)
        
        assert resultado["compativel"] == True
        assert resultado["ordem_recomendada"][0] == "escova_lisa"
        assert resultado["ordem_recomendada"][1] == "make_casual"
        assert "último" in resultado["justificativa"].lower()
    
    def test_calcular_tempo_otimizado(self):
        """Tempo deve ser otimizado para progressiva + unhas"""
        servicos = ["progressiva_curtos", "manicure"]
        tempo = calcular_tempo_total(servicos, simultaneo=True)
        
        assert tempo < 230  # Economia de 50 min
        assert tempo > 170  # Mínimo razoável
    
    def test_calcular_tempo_sequencial(self):
        """Tempo sequencial sem otimização"""
        servicos = ["make_casual", "escova_lisa"]
        tempo = calcular_tempo_total(servicos, simultaneo=False)
        
        assert tempo == 90  # 50 + 40

# ... mais testes ...

if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__, "-v", "--tb=short"])
```

---

## 📋 CHECKLIST PRÉ-ATIVAÇÃO

### Antes de mudar LUNA_MODE para "active":

- [ ] **Fase 1:** Todos testes unitários aprovados
- [ ] **Fase 2:** Seed Supabase executado com sucesso
- [ ] **Fase 3:** Dojo Scenarios 80% aprovação
- [ ] **Fase 4:** End-to-End 100% aprovação
- [ ] **Fase 5:** Performance dentro do esperado
- [ ] **Fase 6:** Protocolo Haven 100% validado
- [ ] **Review:** Suzana aprovou atendimentos de teste
- [ ] **Backup:** Backup do banco realizado
- [ ] **Monitoramento:** Logs configurados
- [ ] **Rollback:** Plano de rollback definido

### **SOMENTE DEPOIS DISSO:**
- [ ] **Aprovação Final:** Todos acima ✅
- [ ] **Comando:** `curl -X POST ... mode=active`
- [ ] **Validação:** Testar resposta real no WhatsApp

---

## 🚨 CRITÉRIOS DE BLOQUEIO

### NÃO ATIVAR SE:

- ❌ Algum teste crítico falhou (handoff, remoção, preços)
- ❌ Aprovação geral < 95%
- ❌ Suzana não validou atendimentos de teste
- ❌ Seed Supabase falhou
- ❌ Performance > 2s por resposta
- ❌ Algum serviço com preço errado
- ❌ Algum profissional com horário errado

---

## 📊 STATUS ATUAL

| Fase | Status | Aprovação |
|------|--------|-----------|
| **Fase 1: Unitários** | ⏳ Pendente | - |
| **Fase 2: Seed** | ⏳ Pendente | - |
| **Fase 3: Dojo** | ⏳ Pendente | - |
| **Fase 4: End-to-End** | ⏳ Pendente | - |
| **Fase 5: Performance** | ⏳ Pendente | - |
| **Fase 6: Protocolo** | ⏳ Pendente | - |

### **STATUS GERAL:** ⚠️ **EM TESTES - NÃO ATIVAR**

---

## 🎯 PRÓXIMOS PASSOS

### Semana 2 (Testes):
```bash
# 1. Criar script de testes automatizados
touch backend/tests/test_luna_production.py

# 2. Executar testes unitários
cd backend
pytest tests/test_luna_production.py -v

# 3. Executar seed Supabase
python app/scripts/seed_haven.py

# 4. Executar Dojo Scenarios
python app/dojo/run_scenarios.py --scenarios haven

# 5. Validar com Suzana
# (Testes manuais de atendimento)
```

### Semana 3 (Ativação - SE APROVADO):
```bash
# 6. Mudar LUNA_MODE para active
curl -X POST http://localhost:8000/api/webhooks/mode -d '{"mode":"active"}'

# 7. Validar resposta real
# (Enviar mensagem no WhatsApp)

# 8. Monitorar primeiras 24h
```

---

## ✅ CONCLUSÃO

**DECISÃO CORRETA:** ✅ **NÃO ATIVAR SEM TESTES**

**Plano:**
1. ✅ Criar testes automatizados
2. ✅ Executar todas as 6 fases
3. ✅ Validar com Suzana
4. ✅ Aprovação > 95%
5. ⏳ **SÓ DEPOIS:** Ativar LUNA_MODE

**Status:** ⚠️ **EM TESTES - BLOQUEADO ATÉ APROVAÇÃO**

---

**Documento Criado:** 2026-03-01  
**Próxima Ação:** Criar testes automatizados  
**Ativação:** ⚠️ **BLOQUEADA ATÉ APROVAÇÃO DOS TESTES**
