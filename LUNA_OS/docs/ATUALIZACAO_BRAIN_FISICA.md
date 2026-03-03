# 🧠 ATUALIZAÇÃO BRAIN.PY - LÓGICA BASEADA EM FÍSICA

**Data:** 2026-03-01  
**Mudança:** Substituir regra fixa "ordem_obrigatoria" por lógica de compatibilidade física

---

## ❌ ANTES (ERRADO):

```python
# Regra fixa e arbitrária
REGRAS_NEGOCIO = {
    "ordem_obrigatoria_servicos": ["cabelo", "unhas", "maquiagem"]
}

# Brain respondia:
"Nosso protocolo exige começar pelo cabelo..."
```

**Problema:** Isso é FALSO. Não é protocolo - é física dos procedimentos.

---

## ✅ DEPOIS (CORRETO):

```python
# Física dos procedimentos
FISICA_PROCEDIMENTOS = {
    "progressiva": {
        "fases": [
            {"nome": "lavatorio", "duracao": 20},
            {"nome": "pausa_quimica", "duracao": 60, "janela_para_outros": True},
            {"nome": "chapinha", "duracao": 90, "calor": True}
        ],
        "compativel_durante_janela": ["manicure", "pedicure"],
        "pos_fases": ["maquiagem"]
    },
    "maquiagem": {
        "sempre_por_ultimo": True,
        "razao": "cliente_precisa_estar_imovel_sem_calor_sem_agua"
    }
}

# Brain responde:
"Começamos lavando seu cabelo. Enquanto o produto age (60 min), 
já fazemos suas unhas para otimizar! Depois finalizamos com a make, 
que precisa ser por último para não estragar com o calor da chapinha."
```

---

## 📝 NOVAS FUNÇÕES PARA ADICIONAR NO BRAIN.PY

### 1. Função para Analisar Compatibilidade

```python
def analisar_compatibilidade_servicos(servicos_solicitados: List[str]) -> Dict:
    """
    Analisa se serviços podem ser feitos juntos baseado na física dos procedimentos.
    
    Retorna:
    - compativel: bool
    - ordem_recomendada: List[str]
    - tempo_total_min: int
    - justificativa: str
    """
    from app.core.config_haven import FISICA_PROCEDIMENTOS, COMPATIBILIDADE_SERVICOS
    
    # Verificar se tem maquiagem + algo com calor
    tem_make = any("make" in s for s in servicos_solicitados)
    tem_calor = any("progressiva" in s or "chapinha" in s for s in servicos_solicitados)
    
    if tem_make and tem_calor:
        return {
            "compativel": False,
            "ordem_recomendada": [s for s in servicos_solicitados if "make" not in s] + ["maquiagem"],
            "justificativa": "Make é sempre por último porque o calor da chapinha/secador derrete a maquiagem"
        }
    
    # Verificar janelas de oportunidade
    tem_progressiva = any("progressiva" in s for s in servicos_solicitados)
    tem_unhas = any("manicure" in s or "pedicure" in s for s in servicos_solicitados)
    
    if tem_progressiva and tem_unhas:
        return {
            "compativel": True,
            "ordem_recomendada": ["progressiva_lavatorio", "unhas_durante_pausa", "progressiva_finalizacao", "maquiagem"],
            "tempo_economizado_min": 60,
            "justificativa": "Durante a pausa química da progressiva (60 min), conseguimos fazer suas unhas!"
        }
    
    # Default: sequencial
    return {
        "compativel": True,
        "ordem_recomendada": servicos_solicitados,
        "justificativa": "Serviços compatíveis em sequência"
    }
```

### 2. Função para Calcular Tempo Total

```python
def calcular_tempo_total(servicos: List[str], simultaneo: bool = False) -> int:
    """
    Calcula tempo total considerando janelas de simultaneidade.
    
    Se simultaneo=True e houver janela de oportunidade,
    subtrai o tempo da janela.
    """
    from app.core.config_haven import TEMPOS_REAIS, FISICA_PROCEDIMENTOS
    
    tempo_sequencial = sum(
        TEMPOS_REAIS.get(s, {}).get("medio", 60)
        for s in servicos
    )
    
    if not simultaneo:
        return tempo_sequencial
    
    # Verificar se tem progressiva com janela
    tem_progressiva = any("progressiva" in s for s in servicos)
    tem_unhas = any("manicure" in s or "pedicure" in s for s in servicos)
    
    if tem_progressiva and tem_unhas:
        # Economiza tempo da janela (40-60 min)
        economia = 50  # média
        return tempo_sequencial - economia
    
    return tempo_sequencial
```

### 3. Script de Resposta para Múltiplos Serviços

```python
def gerar_resposta_multi_servicos(servicos: List[str], disponibilidade: Dict) -> str:
    """
    Gera resposta explicando a logística de múltiplos serviços.
    """
    from app.core.config_haven import FISICA_PROCEDIMENTOS
    
    # Analisar compatibilidade
    analise = analisar_compatibilidade_servicos(servicos)
    
    # Calcular tempos
    tempo_sequencial = calcular_tempo_total(servicos, simultaneo=False)
    tempo_otimizado = calcular_tempo_total(servicos, simultaneo=True)
    
    resposta = []
    resposta.append(f"Perfeito! Para {' + '.join(servicos)}, podemos fazer assim:")
    resposta.append("")
    
    if analise["compativel"] and "janela" in analise.get("justificativa", "").lower():
        # Tem otimização possível
        resposta.append(f"⏱️ **Tempo total: {tempo_otimizado} min** (economizamos {tempo_sequencial - tempo_otimizado} min!)")
        resposta.append("")
        resposta.append(analise["justificativa"])
    else:
        # Sequencial
        resposta.append(f"⏱️ **Tempo total: {tempo_sequencial} min**")
        resposta.append("")
        resposta.append(analise["justificativa"])
    
    resposta.append("")
    resposta.append("Você tem preferência por alguma profissional?")
    resposta.append("Se não tiver, consigo organizar com duas profissionais e você sai bem mais rápido!")
    
    return "\n".join(resposta)
```

---

## 🧪 EXEMPLOS DE RESPOSTAS

### Exemplo 1: Progressiva + Manicure + Make

**Cliente:** "Quero fazer progressiva, manicure e make"

**Resposta CORRETA (baseada em física):**
```
Perfeito! Para progressiva + manicure + make, podemos fazer assim:

⏱️ Tempo total: 3h30 (economizamos 1h!)

1. Começamos lavando seu cabelo para a progressiva (20 min)
2. Enquanto o produto age (60 min), já fazemos suas unhas!
3. Finalizamos a progressiva com chapinha (90 min)
4. Terminamos com a make (40 min)

A make é sempre por último porque precisa de cliente imóvel, 
sem calor ou água por perto.

Você tem preferência por alguma profissional?
Se não tiver, consigo organizar com duas profissionais e você 
sai bem mais rápido!
```

**Resposta ERRADA (protocolo fixo):**
```
❌ "Nosso protocolo exige começar pelo cabelo, depois unhas, depois make"
```

---

### Exemplo 2: Make + Escova (ordem errada)

**Cliente:** "Quero fazer make primeiro e depois escova"

**Resposta CORRETA:**
```
Entendi! Mas preciso te alertar de uma coisa importante:

Se fizermos a make primeiro, ela vai estragar quando:
- Lavarmos seu cabelo no lavatório
- Usarmos o secador (calor derrete a maquiagem)
- Passarmos spray de cabelo

O ideal é fazermos:
1. Escova (50 min)
2. Make (40 min) - sempre por último

Assim você fica pronta em 1h30 e sua make fica perfeita!
Podemos seguir assim?
```

---

### Exemplo 3: Manicure durante Tintura

**Cliente:** "Quero fazer tintura e manicure"

**Resposta CORRETA:**
```
Ótima combinação! Dá para otimizar assim:

1. Aplicamos a tintura (35 min)
2. Enquanto o produto age (35 min), fazemos suas unhas!
3. Enxaguamos a tintura (20 min)
4. Finalizamos (35 min)

Total: 2h (fazemos as unhas durante a pausa da tintura!)

Você tem preferência por alguma profissional?
```

---

## ✅ CHECKLIST DE ATUALIZAÇÃO NO BRAIN.PY

### Adicionar imports:
```python
from app.core.config_haven import (
    FISICA_PROCEDIMENTOS,
    REGRAS_FISICAS_ATENDIMENTO,
    COMPATIBILIDADE_SERVICOS,
    TEMPOS_REAIS
)
```

### Substituir:
```python
# ❌ ANTES
if "ordem_obrigatoria" in REGRAS_NEGOCIO:
    # regra fixa

# ✅ DEPOIS
analise = analisar_compatibilidade_servicos(servicos)
if analise["compativel"]:
    # lógica baseada em física
```

### Atualizar scripts de resposta:
```python
# ❌ ANTES
"Nosso protocolo de atendimento exige..."

# ✅ DEPOIS
"Para otimizar seu tempo, podemos fazer assim..."
"A ordem ideal é baseada no tempo de preparação de cada serviço..."
"Durante a pausa química, conseguimos encaixar..."
```

---

**Documento Criado:** 2026-03-01  
**Próximo Passo:** Atualizar brain.py com essas funções  
**Validação:** Testar no Dojo com cenários de múltiplos serviços
