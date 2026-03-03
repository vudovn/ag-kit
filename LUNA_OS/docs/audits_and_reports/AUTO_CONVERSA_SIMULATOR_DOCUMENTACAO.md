# 🌙🤖 AUTO-CONVERSA SIMULATOR — LUNA vs CLIENTE

## Simulação de Conversas Reais entre Dois Agentes

**Data:** 27 de Fevereiro de 2026  
**Status:** ✅ **IMPLEMENTADO**  
**Foco:** **CONECTAR TODOS OS MÓDULOS + TESTAR SEM PRODUÇÃO**

---

## 🎯 O QUE É

### **Sistema de Auto-Conversa:**
```
🤖 Agente Luna (IA Real)  ←→  🧑 Agente Cliente (Simulado)
```

**Objetivo:**
- ✅ Testar Luna em conversas reais sem impacto em produção
- ✅ Simular clientes com diferentes perfis (fácil, médio, difícil)
- ✅ Conectar Brain + Dojo + Analytics + Modules V3
- ✅ Gerar métricas de performance
- ✅ Identificar pontos de melhoria

---

## 📊 COMO FUNCIONA

### **1. Agente Cliente Simulado:**

**Perfis Disponíveis:**
| Perfil | Paciência | Exigente | Claro |
|--------|-----------|----------|-------|
| **Fácil** | 150 | Não | Sim |
| **Médio** | 100 | Não | Sim |
| **Difícil** | 50 | Sim | Não |
| **Com Pressa** | 30 | Sim | Sim |

**Comportamento:**
- ✅ Gera mensagens baseadas em intenções reais (das 40K)
- ✅ Tem humor (feliz, neutro, irritado, com_pressa)
- ✅ Paciência diminui com respostas ruins
- ✅ Desiste se paciência zerar
- ✅ Satisfeito se problema resolvido

**Intenções Reais:**
```
agendar, preco, horario_func, localizacao,
servicos, pacote, cupom, reclamacao,
handoff, saudacao, agradecimento
```

---

### **2. Agente Luna (IA Real):**

**Usa:**
- ✅ Brain real (`process_message`)
- ✅ Knowledge Base (haven.json)
- ✅ Modules V3 (orquestrador, revenue, etc.)
- ✅ Analytics em tempo real
- ✅ Dojo para aprendizado

**Métricas Coletadas:**
- ✅ Total respostas
- ✅ Taxa de sucesso
- ✅ Tempo médio de resposta (ms)
- ✅ Intents detectadas
- ✅ Sentimentos

---

### **3. Loop de Conversa:**

```
┌─────────────────────────────────────────────────────────┐
│  TURNO 1                                                │
├─────────────────────────────────────────────────────────┤
│  1. Cliente gera mensagem baseada em intenção          │
│     🧑 "Vcs teriam horário às 15h?"                     │
│                                                         │
│  2. Luna processa com Brain real                        │
│     🤖 "Temos! 15h ou 15h30. Qual prefere?"            │
│                                                         │
│  3. Sistema avalia resposta                             │
│     ✅ Intent correta (agendar)                         │
│     ✅ Resposta empática                                │
│     ✅ Resposta completa                                │
│                                                         │
│  4. Cliente atualiza estado                             │
│     💚 Paciência: 100 → 110                             │
│     😊 Humor: neutro → feliz                            │
│                                                         │
│  5. Verifica se continua                                │
│     ✅ Problema não resolvido → Continua                │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  TURNO 2... (repete até 10 turnos ou fim)              │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 COMO USAR

### **Comando Único:**
```bash
cd "/Users/franciscotaveira.ads/LUNA OS/backend"
python3 app/scripts/auto_conversa_simulator.py
```

**Isso vai:**
1. ✅ Criar Agente Luna + Agente Cliente
2. ✅ Simular 1 conversa (demonstração)
3. ✅ Simular 10 conversas (lote)
4. ✅ Gerar relatórios
5. ✅ Salvar em `logs/auto_conversa_*.json`

---

## 📊 EXEMPLO DE RELATÓRIO

### **Relatório Único:**
```json
{
  "status_final": "sucesso",
  "perfil_cliente": "medio",
  "turnos": 4,
  "sucessos": 3,
  "taxa_sucesso": 75.0,
  "paciencia_final": 120,
  "humor_final": "feliz",
  "metricas_luna": {
    "total_respostas": 4,
    "respostas_sucesso": 4,
    "taxa_sucesso": 100.0,
    "tempo_medio_ms": 125
  },
  "conversa": [
    {
      "turno": 1,
      "mensagem_cliente": "Vcs teriam horário às 15h?",
      "intencao": "agendar",
      "resposta_luna": "Temos! 15h ou 15h30...",
      "intent_detectada": "agendar",
      "avaliacao": {"sucesso": true, "pontos": 100},
      "humor_cliente": "neutro",
      "paciencia_cliente": 100
    }
  ]
}
```

### **Relatório Consolidado (Lote):**
```json
{
  "total_simulacoes": 40,
  "sucessos": 28,
  "parciais": 8,
  "desistencias": 4,
  "taxa_sucesso_geral": 70.0,
  "metricas_por_perfil": {
    "facil": {"taxa_sucesso": 90.0, "paciencia_media": 130},
    "medio": {"taxa_sucesso": 75.0, "paciencia_media": 100},
    "dificil": {"taxa_sucesso": 50.0, "paciencia_media": 40},
    "com_pressa": {"taxa_sucesso": 60.0, "paciencia_media": 25}
  }
}
```

---

## 📈 MÉTRICAS DE AVALIAÇÃO

### **Critérios de Sucesso:**

| Critério | Pontos | Descrição |
|----------|--------|-----------|
| **Intent Correta** | +30 | Detectou intenção do cliente |
| **Resposta OK** | +30 | Não foi erro |
| **Resposta Completa** | +20 | Mais de 10 caracteres |
| **Resposta Empática** | +20 | Usou palavras empáticas |

**Sucesso:** ≥ 60 pontos  
**Parcial:** 40-59 pontos  
**Falha:** < 40 pontos

---

## 🎯 PERFIS DE CLIENTE

### **Fácil:**
```
💚 Paciência: 150
😊 Exigente: Não
💬 Claro: Sim
📊 Taxa Sucesso Esperada: 90%+
```

### **Médio:**
```
💚 Paciência: 100
😊 Exigente: Não
💬 Claro: Sim
📊 Taxa Sucesso Esperada: 70-80%
```

### **Difícil:**
```
💚 Paciência: 50
😊 Exigente: Sim
💬 Claro: Não
📊 Taxa Sucesso Esperada: 50-60%
```

### **Com Pressa:**
```
💚 Paciência: 30
😊 Exigente: Sim
💬 Claro: Sim
📊 Taxa Sucesso Esperada: 60-70%
```

---

## 🔗 CONEXÃO COM OUTROS MÓDULOS

### **Brain:**
```python
# Usa process_message real
resposta = await process_message(
    phone=cliente.phone,
    name=cliente.nome,
    message=mensagem,
    history=[]
)
```

### **Dojo:**
```python
# Carrega intenções reais das 5.908 situações
self.intencoes_reais = self._carregar_intencoes_reais()
```

### **Analytics:**
```python
# Coleta métricas em tempo real
self.metricas = {
    "total_respostas": 0,
    "respostas_sucesso": 0,
    "tempo_medio_ms": 0
}
```

### **Modules V3:**
```python
# Pode usar modules V3 para enriquecer resposta
# (orquestrador, revenue, ai_coach, etc.)
```

---

## 📁 ARQUIVOS CRIADOS

### **Script:**
```
backend/app/scripts/
└── auto_conversa_simulator.py    ✅ 22KB
```

### **Logs (Gerados na Execução):**
```
logs/
├── auto_conversa_simulator.log       ← Log da execução
├── auto_conversa_unico.json          ← 1 conversa
└── auto_conversa_lote.json           ← 40 conversas
```

---

## 💡 CASOS DE USO

### **1. Testar Nova Funcionalidade:**
```bash
# Antes de subir para produção
python3 auto_conversa_simulator.py

# Verificar taxa de sucesso
# Se < 70%, melhorar antes de produzir
```

### **2. Comparar Versões:**
```bash
# Versão 1.0
python3 auto_conversa_simulator.py
# Taxa sucesso: 65%

# Versão 2.0 (melhorada)
python3 auto_conversa_simulator.py
# Taxa sucesso: 75% ✅
```

### **3. Identificar Pontos Fracos:**
```bash
# Se clientes "difíceis" têm 30% sucesso
# → Melhorar respostas para casos difíceis

# Se intent "reclamacao" tem 40% sucesso
# → Melhorar handling de reclamações
```

### **4. Treinar Equipe:**
```bash
# Usar conversas simuladas como exemplo
# Mostrar respostas boas vs ruins
# Treinar com perfis difíceis
```

---

## 🎯 PRÓXIMOS PASSOS

### **1. Executar Simulator:**
```bash
cd "/Users/franciscotaveira.ads/LUNA OS/backend"
python3 app/scripts/auto_conversa_simulator.py
```

### **2. Ver Relatórios:**
```bash
cat logs/auto_conversa_lote.json | jq
```

### **3. Identificar Melhorias:**
- Perfis com baixa taxa de sucesso
- Intenções com detecção ruim
- Respostas muito curtas
- Tempo de resposta alto

### **4. Implementar Melhorias:**
- Ajustar Brain
- Melhorar Knowledge Base
- Refinar Modules V3

### **5. Re-testar:**
```bash
python3 auto_conversa_simulator.py
# Comparar com anterior
```

---

## 📊 EXEMPLO DE CONVERSA REAL

### **Simulação:**
```
🧑 Cliente (medio): "Vcs teriam horário às 15h?"
   Intenção: agendar
   Humor: neutro, Paciência: 100

🤖 Luna: "Temos! 15h ou 15h30. Qual prefere?"
   Intent: agendar ✅
   Avaliação: 100 pontos ✅
   
🧑 Cliente: "15h30 é melhor"
   Intenção: agendar
   Humor: feliz, Paciência: 110

🤖 Luna: "Perfeito! Agendado às 15h30. Qual serviço?"
   Intent: agendar ✅
   Avaliação: 100 pontos ✅
   
🧑 Cliente: "Escova e unha"
   Intenção: multi_servico
   Humor: feliz, Paciência: 120

🤖 Luna: "Ótimo! São 75 minutos. Posso confirmar?"
   Intent: agendar ✅
   Avaliação: 100 pontos ✅
   
🧑 Cliente: "Sim, obrigado!"
   Intenção: agradecimento
   Humor: feliz, Paciência: 130

✅ CONVERSA ENCERRADA: SUCESSO
```

---

## 🎯 BENEFÍCIOS

### **Para Desenvolvimento:**
- ✅ Testa sem impacto em produção
- ✅ Identifica bugs antes de produzir
- ✅ Compara versões facilmente
- ✅ Gera dados para analytics

### **Para Negócio:**
- ✅ Melhora taxa de conversão
- ✅ Reduz clientes perdidos
- ✅ Treina equipe com exemplos
- ✅ Identifica pontos fracos

### **Para IA:**
- ✅ Aprende com erros simulados
- ✅ Refina respostas
- ✅ Melhora detecção de intent
- ✅ Otimiza tempo de resposta

---

**🌙 "Inteligência completa. Complexidade invisível."**

**Status:** ✅ **AUTO-CONVERSA SIMULATOR IMPLEMENTADO**

**Próximo:** **EXECUTAR `python3 auto_conversa_simulator.py`**

**Benefício:** **TESTAR TUDO SEM IMPACTO EM PRODUÇÃO**
