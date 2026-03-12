# PROMPT DE IMPLEMENTAÇÃO — AGENTE DE CÓDIGO
## LUNA OS — Haven Escovaria & Esmalteria
## Missão: Sincronizar o sistema com o Manual Operacional Oficial

---

## CONTEXTO DO PROJETO

Você está trabalhando no **LUNA OS**, um sistema de atendimento automático via WhatsApp para o salão **Haven Escovaria & Esmalteria** localizado em Chapecó-SC.

**Stack:** FastAPI + Supabase + Evolution API (WhatsApp) + Redis

**Arquivo principal de configuração:** `backend/app/core/config_haven.py`
**Arquivo do cérebro (IA):** `backend/app/core/brain.py`
**Manual de referência:** `conversa-suzana-gpt.md` (fonte da verdade — leia antes de qualquer edição)

**Arquitetura do sistema:**
- `config_haven.py` — Todas as regras de negócio: profissionais, serviços, preços, pacotes, cupons, scripts
- `brain.py` — Motor de IA com DualBrain (Lógico + Voz). Importa tudo de `config_haven.py`. Tem um `_LOGIC_PROMPT_FALLBACK` e um `_VOICE_PROMPT_FALLBACK` hardcoded que servem de sistema de regras para a IA
- `SCRIPTS_ATENDIMENTO` — Dicionário no `config_haven.py` com scripts prontos que brain.py injeta no contexto

**Regra crítica de imutabilidade:** Nunca mutate dicionários existentes. Sempre crie novas versões com `{**original, "nova_chave": valor}` nos testes. Nos arquivos de config, edite diretamente pois são constantes de módulo.

---

## TAREFA 1 — CORRIGIR DISCREPÂNCIAS DE PREÇO

**Arquivo:** `backend/app/core/config_haven.py`

### 1.1 Fitagem — Preço incorreto

**Atual (ERRADO):**
```python
"fitagem": {
    "nome": "Fitagem (com difusor)",
    "valor": 85.00,
    "valor_promo_seg_qua": 59.00,
    ...
}
```

**Correto (conforme Manual PARTE 2.1):**
```python
"fitagem": {
    "nome": "Fitagem (com difusor)",
    "valor": 95.00,          # Manual: R$95
    "valor_promo_seg_qua": 59.00,
    ...
}
```

**Também corrigir em TEMPOS_REAIS:** manter como está (tempo está correto: min 60, medio 70, max 90).

### 1.2 Verificar consistência de `PROFISSIONAIS["luisa"]`

A Lu aparece com `"valores": {"manicure": 42.00, "pedicure": 45.00, "gel": 120.00}` — correto conforme manual. Manter.

---

## TAREFA 2 — ADICIONAR SCRIPTS FALTANTES EM `SCRIPTS_ATENDIMENTO`

**Arquivo:** `backend/app/core/config_haven.py`

Localizar a variável `SCRIPTS_ATENDIMENTO` (linha ~1119) e adicionar as seguintes chaves DENTRO do dicionário existente, mantendo as que já existem:

```python
# --- BLINDAGEM DE PRODUTO ---
"blindagem_produto_curiosa": (
    "Aqui a gente trabalha com linha profissional de alta performance, "
    "escolhida para entregar resultado com conforto e segurança. "
    "É livre de formol e não tem cheiro forte. "
    "A indicação exata depende do seu tipo de fio e histórico de química."
),

"blindagem_produto_insistente": (
    "Eu consigo te explicar tudo presencialmente com transparência, "
    "porque aí a gente avalia o fio antes e indica o que é mais adequado pra você. "
    "Pelo WhatsApp eu prefiro não cravar marca sem ver o cabelo."
),

"blindagem_produto_insegura": (
    "Pode ficar tranquila. A linha que usamos é profissional, livre de formol, "
    "pensada para alinhar com conforto. "
    "Antes de qualquer procedimento, avaliamos seu fio para indicar a melhor opção."
),

"blindagem_autoridade": (
    "O produto é importante, mas a técnica e a avaliação do fio fazem toda diferença no resultado."
),

"blindagem_conversao": (
    "Você está pensando em fazer o procedimento em breve? "
    "Me conta como está seu cabelo hoje e qual resultado você quer alcançar. "
    "Aí já organizo um horário ideal para você."
),

# --- DIFERENCIAÇÃO DE TRATAMENTOS ---
"diferenciacao_progressiva": (
    "A nossa progressiva é a Perfecta da Borabella. "
    "Ela é livre de formol, não tem aquele cheiro forte e não costuma causar ardência — "
    "é muito mais confortável que as progressivas antigas. "
    "Ela deixa o fio bem liso e alinhado, e na maioria dos casos a cliente consegue "
    "lavar, secar naturalmente e o cabelo já fica disciplinado."
),

"diferenciacao_progressiva_duracao": (
    "Sim. A Perfecta entrega um efeito bem liso e alinhado. "
    "Depois de feita, muitas clientes conseguem lavar, secar naturalmente e o cabelo já fica disciplinado. "
    "O cabelo que já foi tratado fica alinhado. "
    "Conforme vai crescendo a raiz, ela cresce do jeitinho natural do seu fio. "
    "Com o tempo a gente faz só o retoque da raiz para manter o efeito."
),

"diferenciacao_cauterizacao": (
    "A Cauter Gloss é um tratamento de reconstrução + selagem. "
    "Ela melhora porosidade, dá maciez e aquele brilho espelhado, "
    "e é excelente para recuperar o fio. "
    "Atenção: a cauterização NÃO alisa. Se você quer reduzir volume, o certo é a progressiva."
),

"diferenciacao_umectacao": (
    "A umectação é um tratamento nutritivo para repor lipídios — "
    "indicado para cabelo muito ressecado, áspero ou sem brilho. "
    "Ela devolve maciez e reduz o ressecamento. "
    "Não alisa e não inclui escova — se quiser finalizar com escova, somamos o valor."
),

"diferenciacao_detox": (
    "O detox é uma limpeza profunda do couro cabeludo. "
    "Remove acúmulo de produtos, oleosidade e resíduos — deixa a raiz mais leve. "
    "Não alisa, não reconstrói e não inclui escova."
),

"diferenciacao_matriz_decisao": (
    "Só pra eu te indicar certinho: você quer alisar e reduzir volume ou quer recuperar o fio? "
    "A progressiva é para alinhar. A cauterização é para reconstruir e dar brilho. "
    "A umectação é para nutrir. E o detox é para limpar profundamente. "
    "Me diz o que mais te incomoda no cabelo hoje que eu te indico o procedimento certo."
),

# --- POLÍTICAS OPERACIONAIS ---
"politica_atraso": (
    "Só pra te avisar: a gente tenta manter a agenda bem certinha. "
    "Se atrasar mais de 10 min, pode ser que a gente precise ajustar o serviço "
    "ou reagendar conforme a agenda do dia."
),

"remarcacao": (
    "Claro, remarcamos sim. Qual melhor janela: manhã, tarde ou noite? "
    "Vou te mandar 2 opções."
),

"reativacao_lead": (
    "Oi, {nome}! Passando pra ver se você ainda quer agendar sua {procedimento}. "
    "Tenho {horario1} ou {horario2}. Quer garantir?"
),

"pos_atendimento": (
    "{nome}, obrigada por vir hoje! "
    "Se quiser, já deixo seu próximo horário pré-agendado pra você não ficar sem vaga."
),

"cliente_pedindo_desconto": (
    "A gente trabalha com valores bem justos e consistentes pra manter a experiência "
    "e qualidade do atendimento. "
    "Mas eu consigo te ajudar escolhendo o melhor horário e serviço pra ficar perfeito pra você."
),

"oferta_horarios": "Tenho {dia} às {hora1} ou {dia2} às {hora2}. Qual fica melhor pra você?",

"urgencia_horario": "Passando pra confirmar antes que eu libere aqui: prefere {hora1} ou {hora2}?",

"qual_profissional_melhor": (
    "Temos profissionais excelentes. Me diz o que você busca: mais rápido, mais detalhista "
    "ou um acabamento bem marcado? Aí eu te indico a melhor pra esse estilo."
),

# --- AGENDA PARA EVENTO ---
"evento_pergunta": "Qual o horário do seu evento? Assim eu já monto a agenda de trás pra frente e você chega com tudo certinho e com folga.",

"simultaneidade_proposta": (
    "Aqui na Haven a gente tenta otimizar seu tempo ao máximo. "
    "Se você quiser fazer {procedimento1} + {procedimento2}, eu consigo organizar pra acontecer tudo próximo. "
    "Se não tiver preferência por profissional, dá até pra fazer com duas profissionais ao mesmo tempo "
    "pra você sair mais rápido. Quer assim?"
),

# --- PACOTES ---
"pacote_escova_pitch": (
    "Você faz escova com frequência? A gente tem pacote que reduz o valor por escova. "
    "No pacote com 4, a lisa fica R$ 55 e a modelada R$ 65. "
    "No pacote com 8, baixa mais: lisa R$ 52 e modelada R$ 59. "
    "O pacote é à vista (Pix ou dinheiro) e vale para produtos da casa. "
    "Se quiser coreanos, Labriza ou Kérastase, tem adicional por escova."
),

"pacote_pagamento_regra": (
    "Como é pacote com valor reduzido, ele funciona somente à vista no Pix ou dinheiro, tá?"
),

"pacote_prazo_gel": (
    "O pacote tem validade para acompanhar o ciclo de manutenção do gel. "
    "O de 3 aplicações vale 60 dias e o de 6 aplicações vale 120 dias."
),

# --- UPSELL LAVATÓRIO ---
"upsell_lavatorio_explicacao": (
    "Na conversa eu já te passo o valor base com os produtos da casa. "
    "No lavatório, se você quiser, a equipe oferece opções premium com acréscimo — "
    "coreanos, Labriza ou Kérastase — sempre informando o valor antes. "
    "Você só escolhe se quiser, tá?"
),
```

---

## TAREFA 3 — ADICIONAR PERGUNTAS DIFÍCEIS AO `config_haven.py`

**Arquivo:** `backend/app/core/config_haven.py`

Após o bloco `SCRIPTS_ATENDIMENTO`, adicionar uma nova constante `PERGUNTAS_DIFICEIS`:

```python
# ═══════════════════════════════════════════════
# 11. RESPOSTAS PARA PERGUNTAS DIFÍCEIS (Documento 13)
# ═══════════════════════════════════════════════

PERGUNTAS_DIFICEIS = {
    "qual_produto_marca": (
        "Trabalhamos com linha profissional de alta performance, livre de formol e sem cheiro forte. "
        "A indicação exata depende do seu tipo de fio. "
        "Quer me dizer qual seu objetivo e para que dia você pensa em fazer?"
    ),
    "tem_formol": "Não. A linha que usamos é livre de formol.",
    "tem_acido_glioxilico": (
        "É uma linha profissional, livre de formol e pensada para ser mais confortável. "
        "A parte técnica a gente explica presencialmente. "
        "Você quer alinhar e reduzir volume ou está buscando tratamento e recuperação?"
    ),
    "alisa_100_porcento": (
        "A proposta é alinhar muito e deixar bem liso — para facilitar seu dia a dia. "
        "Em muitos casos a cliente consegue lavar, secar e o cabelo já fica disciplinado. "
        "O que cresce depois é a raiz natural, então com o tempo fazemos o retoque da raiz para manter o efeito."
    ),
    "quanto_tempo_dura": (
        "Dura conforme o crescimento da sua raiz. "
        "O comprimento tratado fica alinhado, e quando a raiz começa a aparecer natural, "
        "a gente faz o retoque. Me diz seu tipo de cabelo que eu te oriento melhor."
    ),
    "posso_comprar_produto_casa": (
        "Não recomendo. Esse procedimento depende de técnica, tempo de pausa, temperatura "
        "e finalização correta pra ficar seguro e bonito. "
        "Aqui fazemos com avaliação e aplicação profissional. Quer que eu te encaixe um horário?"
    ),
    "por_que_preco_diferente": (
        "A diferença está na soma de três coisas: qualidade do produto, técnica da profissional "
        "e padrão de atendimento. "
        "Aqui trabalhamos com linha profissional, execução bem feita e ambiente organizado. "
        "Posso te passar o valor certinho do seu caso?"
    ),
    "tem_garantia": (
        "A gente trabalha para você sair satisfeita. "
        "Fazemos avaliação antes e alinhamos expectativa de resultado. "
        "Se acontecer qualquer insatisfação, seguimos um protocolo interno — "
        "você manda fotos e a gestão avalia para dar a melhor solução."
    ),
    "cabelo_loiro_pode_progressiva": (
        "Pode ser possível, mas precisa de avaliação porque a fibra pode estar mais sensível. "
        "Às vezes é melhor fortalecer com tratamento primeiro. "
        "Seu loiro é recente? E o fio está quebrando ou elástico?"
    ),
    "cabelo_quebrando_pode_progressiva": (
        "Se o fio estiver quebrando ou elástico, o ideal é avaliar antes. "
        "Muitas vezes a gente fortalece primeiro com cauterização e depois faz a progressiva. "
        "Assim você não corre risco e o resultado fica melhor."
    ),
    "diferenca_progressiva_cauterizacao_umectacao_detox": (
        "Progressiva é para alinhar e reduzir volume. "
        "Cauterização é para reconstruir e selar fios danificados (não alisa). "
        "Umectação é nutrição com óleo para cabelo ressecado. "
        "Detox é limpeza profunda do couro cabeludo. "
        "Me diz qual seu incômodo principal que eu te indico certinho."
    ),
    "tratamento_inclui_escova": (
        "Não. Os tratamentos (hidratação, nutrição, reconstrução, umectação e detox) "
        "são o valor do tratamento. A escova é cobrada à parte. "
        "A única exceção é a matização de loiros, que já inclui escova."
    ),
    "penteado_inclui_escova": (
        "Não. Penteado não inclui escova. "
        "Se você quiser escova antes do penteado, a gente agenda os dois e soma o valor e o tempo."
    ),
    "ja_tem_gel_quer_fazer_gel": (
        "Antes de fazer gel, a gente precisa agendar a remoção do gel que você está usando. "
        "Ela leva cerca de 30 minutos e é cobrada à parte. "
        "Você está com gel nas mãos, nos pés ou nos dois?"
    ),
    "tem_cupom_blogueira": (
        "Ótimo! Qual cupom você tem? "
        "(PRISCILA10, EWYLIN10, SOLANGE10, CAROLINE10 ou KETLYN10). "
        "Com o cupom você tem 10% de desconto. "
        "Me diz qual procedimento e para que dia que eu já fecho com o valor final."
    ),
    "nao_tem_horario_que_quero": (
        "Entendi. Nesse horário específico hoje fechou, mas eu consigo te ajudar "
        "com duas opções bem próximas: {opcao1} ou {opcao2}. "
        "Se você tiver flexibilidade, também tento encaixe. "
        "Ou te coloco na lista de prioridade pra te chamar se abrir vaga. "
        "Qual dessas opções te atende melhor?"
    ),
}
```

---

## TAREFA 4 — ADICIONAR MATRIZ DE DIAGNÓSTICO DE TRATAMENTOS AO `config_haven.py`

Após `PERGUNTAS_DIFICEIS`, adicionar:

```python
# ═══════════════════════════════════════════════
# 12. MATRIZ DE DIAGNÓSTICO DE TRATAMENTOS (Documento 7)
# ═══════════════════════════════════════════════

DIAGNOSTICO_TRATAMENTOS = {
    "muito_volume_frizz_quer_alisar": {
        "procedimento": "progressiva",
        "script": "A progressiva é o certo pra você. Ela alinha, disciplina e reduz o frizz. Duracao média 3h.",
    },
    "cabelo_quebrando_elastico_poroso": {
        "procedimento": "cauterizacao",
        "script": "Com o fio elástico ou quebrando, o melhor é a cauterização primeiro. Ela reconstrói e protege o fio. Depois a gente pode pensar em progressiva se quiser alisar.",
    },
    "muito_ressecado_aspero_sem_brilho": {
        "procedimento": "umectacao",
        "script": "Para ressecamento e falta de brilho, a umectação é o certo. Ela nutre e devolve maciez.",
    },
    "raiz_oleosa_cabelo_pesado_acumulo_produto": {
        "procedimento": "detox",
        "script": "Para raiz oleosa e cabelo pesado com acúmulo, o detox limpa fundo e deixa tudo mais leve.",
    },
}

DIFERENCIAIS_PRODUTO = {
    "borabella_perfecta": {
        "nome": "Borabella Perfecta",
        "servico": "progressiva",
        "atributos": [
            "Livre de formol",
            "Sem ácido glioxílico",
            "Sem cheiro forte",
            "Sem ardência durante procedimento",
            "Blend de 12 óleos + 19 aminoácidos",
            "Regularizado no mercado",
            "Efeito liso intenso e duradouro",
        ],
        "nao_e": [
            "Não é tratamento reconstrutor para cabelo quebrando",
            "Não substitui cauterização em fio fragilizado",
            "Não é hidratação",
        ],
    },
    "borabella_cauter_gloss": {
        "nome": "Borabella Cauter Gloss",
        "servico": "cauterizacao",
        "atributos": [
            "Repõe proteína no fio",
            "Sela cutículas abertas",
            "Reduz porosidade",
            "Dá maciez e brilho espelhado (efeito gloss)",
            "Mantém resultado de progressivas por mais tempo",
            "Recupera fios pós-química e pós-descoloração",
        ],
        "nao_e": [
            "Não alisa — quem quer alinhar precisa da progressiva",
        ],
    },
}
```

---

## TAREFA 5 — ATUALIZAR O `_LOGIC_PROMPT_FALLBACK` NO `brain.py`

**Arquivo:** `backend/app/core/brain.py`

Localizar `_LOGIC_PROMPT_FALLBACK` (linha ~465) e adicionar as seguintes regras no bloco `<layer3_rules_to_enforce>`, após a regra 12 existente:

```
13. DIAGNÓSTICO DE TRATAMENTOS: Quando cliente perguntar sobre tratamento capilar,
    usar DIAGNOSTICO_TRATAMENTOS para identificar e recomendar:
    - Volume/frizz → Progressiva
    - Quebra/elástico/poroso → Cauterização (NUNCA progressiva diretamente)
    - Ressecado/opaco → Umectação
    - Raiz oleosa/acúmulo → Detox
    Se sinais de fio fragilizado: recomendar cauterização ANTES da progressiva.

14. BLINDAGEM DE PRODUTO: Se cliente perguntar marca/produto, NUNCA informar.
    Diretriz: valorizar resultado, conduzir para presencial.
    Usar scripts em SCRIPTS_ATENDIMENTO["blindagem_produto_*"].

15. CARLA — RESTRIÇÃO CRÍTICA: Carla tem agenda dupla (Haven + Spa Sora).
    SEMPRE verificar conflito antes de confirmar qualquer horário com Carla.
    [AÇÃO PRINCIPAL]: Coletar Dados quando cliente escolher Carla.

16. MANICURE + PEDIDO DE GEL NOVO (cliente com gel externo):
    Se cliente pede gel E já tem gel feito fora da Haven:
    - Adicionar remoção OBRIGATÓRIA antes (+30min +R$30)
    - Perguntar: mãos, pés ou ambos?

17. AGENDA PARA EVENTO: Se cliente mencionar evento/formatura/casamento/festa,
    [AÇÃO PRINCIPAL]: Coletar Dados — perguntar horário do evento.
    Montar agenda de trás pra frente: Maquiagem termina 1h antes do evento.
    Ordem: Unhas → Cabelo → Sobrancelha → Maquiagem.

18. RETENÇÃO DE LEAD — ALTERNATIVAS POR PROCEDIMENTO (usar quando sem horário):
    - Escova modelada sem vaga → oferecer escova lisa ou modelada babyliss
    - Penteado sem vaga → penteado básico próximo
    - Matização sem vaga → tratamento + escova disponível
    - Gel sem vaga → tradicional ou outra profissional
    NUNCA encerrar sem oferecer 2 alternativas concretas + lista de espera.

19. SIMULTANEIDADE — DETALHE FÍSICO:
    - Durante pausa PROGRESSIVA (40-90min): possível manicure + pedicure
    - Durante pausa TINTURA (30-40min): possível apenas manicure das MÃOS
    - NUNCA agendar maquiagem durante qualquer serviço de cabelo
    - Unhas SEMPRE antes do lavatório
```

---

## TAREFA 6 — ATUALIZAR O `_VOICE_PROMPT_FALLBACK` NO `brain.py`

**Arquivo:** `backend/app/core/brain.py`

Localizar `_VOICE_PROMPT_FALLBACK` (linha ~531) e enriquecer o bloco `<layer3_voice_guidelines>` adicionando estas seções após os SCRIPTS OBRIGATÓRIOS existentes:

```
SCRIPTS — DIAGNÓSTICO DE TRATAMENTO:
- DIAGNÓSTICO CAPILAR: "Só pra eu te indicar certinho: você quer alisar e reduzir volume ou quer recuperar o fio? A progressiva é para alinhar. A cauterização é para reconstruir e dar brilho. A umectação é para nutrir. E o detox é para limpar profundamente. Me diz o que mais te incomoda no cabelo hoje."
- CABELO FRAGILIZADO: "Com o fio quebrando ou elástico, o ideal é fortalecer com cauterização primeiro. Depois a gente pode pensar em progressiva. Assim você não corre risco e o resultado fica melhor."

SCRIPTS — BLINDAGEM DE PRODUTO:
- QUANDO PEDIR MARCA: "Aqui a gente trabalha com linha profissional de alta performance, livre de formol e sem cheiro forte. A indicação exata depende do seu tipo de fio. Quer me contar como está seu cabelo que eu te oriento?"
- SE INSISTIR: "Eu consigo te explicar presencialmente com transparência, porque aí avaliamos o fio antes. Pelo WhatsApp prefiro não cravar marca sem ver o cabelo."
- FRASE DE AUTORIDADE: "O produto é importante, mas a técnica e a avaliação do fio fazem toda diferença no resultado."

SCRIPTS — AGENDA PARA EVENTO:
- EVENTO DETECTADO: "Para evento, preciso saber: qual horário você precisa estar pronta? Assim eu monto a agenda de trás pra frente e você chega com tudo certinho e com folga."
- MONTAR EXEMPLO: "Se o evento é às [X]h, a maquiagem termina às [X-1]h, que começa às [X-2]h. Escova das [X-3]h às [X-2]h. Unhas a partir das [X-4]h. Quer que eu organize assim?"

SCRIPTS — PACOTES (ativar quando cliente faz procedimento com frequência):
- UPSELL ESCOVA: "Você faz escova com frequência? No pacote com 4, a lisa fica R$ 55 e a modelada R$ 65. No de 8, ainda mais barato. À vista no Pix. Quer saber mais?"
- UPSELL GEL: "Você costuma fazer gel sempre? No pacote de 3 aplicações o valor cai. Vale a pena! Quer que eu te explique?"

REGRAS DE TOM:
- Nunca diga "não podemos informar" ou "não posso falar" — parece evasivo
- Em vez de negar, valorize e redirecione sempre
- Reclamação: acolha, peça fotos, encaminhe para Suzana. NUNCA decida sozinha
- Atraso de cliente: avise com gentileza sobre política dos 10min antes de confirmar
```

---

## TAREFA 7 — ATUALIZAR IMPORTAÇÕES NO `brain.py`

**Arquivo:** `backend/app/core/brain.py`

Localizar o bloco de importações de `config_haven` (linha ~49) e adicionar `PERGUNTAS_DIFICEIS` e `DIAGNOSTICO_TRATAMENTOS` às importações:

```python
from app.core.config_haven import (
    PROFISSIONAIS,
    SERVICOS,
    FISICA_PROCEDIMENTOS,
    REGRAS_FISICAS_ATENDIMENTO,
    COMPATIBILIDADE_SERVICOS,
    TEMPOS_REAIS,
    SCRIPTS_ATENDIMENTO,
    HANDOFF_TRIGGERS,
    UPSELL_LAVATORIO,
    CUPONS,
    PACOTES,
    HORARIOS_FUNCIONAMENTO,
    PERGUNTAS_DIFICEIS,        # NOVO
    DIAGNOSTICO_TRATAMENTOS,  # NOVO
    DIFERENCIAIS_PRODUTO,     # NOVO
)
```

---

## TAREFA 8 — INJETAR DIAGNÓSTICO E PERGUNTAS DIFÍCEIS NO CONTEXTO RAG

**Arquivo:** `backend/app/core/brain.py`

Localizar a função `build_context` (linha ~389) e adicionar os seguintes blocos no final da função, antes do `return`:

```python
# Diagnóstico de tratamentos (quando relevante)
if intent in {IntentType.PRECO, IntentType.AGENDAR, IntentType.DUVIDA, IntentType.SERVICOS}:
    tratamento_keywords = {
        "progressiva", "cauterização", "cauterizacao", "umectação", "umectacao",
        "detox", "hidratação", "hidratacao", "tratamento", "alisamento",
        "quebrando", "poroso", "elástico", "elastico", "ressecado", "oleoso"
    }
    msg_words = set(message.lower().split())
    if msg_words & tratamento_keywords:
        context_parts.append(
            f"### DIAGNÓSTICO TRATAMENTOS:\n{json.dumps(DIAGNOSTICO_TRATAMENTOS, ensure_ascii=False)}"
        )
        context_parts.append(
            f"### DIFERENCIAIS DE PRODUTO:\n{json.dumps(DIFERENCIAIS_PRODUTO, ensure_ascii=False)}"
        )

# Perguntas difíceis (sempre disponível para consulta)
if intent in {IntentType.DUVIDA, IntentType.PRECO, IntentType.SERVICOS_TECNICOS}:
    context_parts.append(
        f"### RESPOSTAS PERGUNTAS DIFÍCEIS:\n{json.dumps(PERGUNTAS_DIFICEIS, ensure_ascii=False)}"
    )
```

---

## TAREFA 9 — VERIFICAÇÃO E TESTES

Após todas as edições, executar:

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS

# 1. Verificar se Python importa sem erros
python -c "from backend.app.core.config_haven import PROFISSIONAIS, SERVICOS, SCRIPTS_ATENDIMENTO, PERGUNTAS_DIFICEIS, DIAGNOSTICO_TRATAMENTOS, DIFERENCIAIS_PRODUTO; print('✅ config_haven imports OK')"

# 2. Verificar brain imports
python -c "import sys; sys.path.insert(0, 'backend'); from app.core import brain; print('✅ brain imports OK')"

# 3. Verificar preços corrigidos
python -c "
import sys; sys.path.insert(0, 'backend')
from app.core.config_haven import SERVICOS
assert SERVICOS['fitagem']['valor'] == 95.00, 'ERRO: fitagem valor incorreto'
print(f'✅ fitagem: R\${SERVICOS[\"fitagem\"][\"valor\"]}')
"

# 4. Verificar novos scripts presentes
python -c "
import sys; sys.path.insert(0, 'backend')
from app.core.config_haven import SCRIPTS_ATENDIMENTO
required = ['blindagem_produto_curiosa', 'diferenciacao_progressiva', 'pacote_escova_pitch', 'evento_pergunta']
for k in required:
    assert k in SCRIPTS_ATENDIMENTO, f'FALTANDO: {k}'
    print(f'✅ {k}')
"

# 5. Rodar testes existentes (se houver)
docker exec luna-backend pytest tests/ -v --tb=short 2>/dev/null || python -m pytest backend/tests/ -v --tb=short
```

---

## TAREFA 10 — ATUALIZAR PROMPT NO SUPABASE (OPCIONAL — se sistema usa DB)

Se o sistema tiver prompts salvos no Supabase (tabela `system_prompts`), sincronizar os novos conteúdos dos prompts Logic e Voice. Verificar com:

```sql
SELECT name, is_active, updated_at FROM system_prompts ORDER BY updated_at DESC;
```

Se existirem registros ativos, atualizar com os novos conteúdos usando UPDATE na tabela `system_prompts`.

---

## RESUMO DAS MUDANÇAS

| # | Arquivo | O que muda | Impacto |
|---|---------|-----------|---------|
| 1 | `config_haven.py` | Preço fitagem R$85 → R$95 | Corrige dado errado |
| 2 | `config_haven.py` | +23 scripts em SCRIPTS_ATENDIMENTO | Luna responde com scripts corretos |
| 3 | `config_haven.py` | +Nova constante PERGUNTAS_DIFICEIS (16 Q&A) | Respostas padronizadas oficiais |
| 4 | `config_haven.py` | +DIAGNOSTICO_TRATAMENTOS | Luna diagnostica corretamente progressiva vs cauterização |
| 5 | `config_haven.py` | +DIFERENCIAIS_PRODUTO (Borabella) | Luna sabe o produto sem revelar nome |
| 6 | `brain.py` | +7 regras no Logic Prompt (13-19) | Lógica mais robusta de agendamento |
| 7 | `brain.py` | +Scripts de diagnóstico e blindagem no Voice Prompt | Voz mais precisa |
| 8 | `brain.py` | +Importações novas constantes | Compila sem erro |
| 9 | `brain.py` | +Injeção de diagnóstico/perguntas no RAG | Contexto mais rico |

---

## RESTRIÇÕES IMPORTANTES

1. **NÃO alterar** a arquitetura existente — apenas adicionar/corrigir
2. **NÃO remover** nenhuma constante existente em `config_haven.py`
3. **NÃO alterar** a lógica de fallback do brain (apenas enriquecer os prompts)
4. **Manter** o padrão de documentação em português do projeto
5. **Respeitar** o limite de 800 linhas por arquivo — se `config_haven.py` ultrapassar, extrair as novas constantes para `config_haven_scripts.py` e importar em `config_haven.py`
6. Após edições, o sistema deve passar nos testes da Tarefa 9 sem erros

---

*Gerado a partir do Manual Operacional Haven — conversa-suzana-gpt.md*
*Referência de arquivos: backend/app/core/config_haven.py + backend/app/core/brain.py*
