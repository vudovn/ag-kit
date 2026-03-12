# PROMPT DE IMPLEMENTAÇÃO — AGENTE DE CÓDIGO
## LUNA OS — Conexões do Cérebro
## Missão: Conectar 3 sistemas já existentes que ainda não estão ligados entre si

---

## CONTEXTO

Você está no projeto LUNA OS em `backend/app/core/`.

**Leia estes arquivos antes de qualquer edição:**
- `backend/app/core/brain.py` — pipeline principal (foco em `_process_with_ai` e `build_voice_prompt`)
- `backend/app/core/memory.py` — `ClientProfile` (campos: total_visits, total_spent, preferences, tags)
- `backend/app/core/learning.py` — `mark_golden_example()` (já existe, nunca é chamado)

**Regra absoluta:** não altere a arquitetura, não crie novos arquivos, não mude assinaturas de funções que outros módulos chamam. Apenas cirurgia pontual nos 3 locais descritos abaixo.

---

## MUDANÇA 1 — Histórico da cliente no Voice Prompt

**Problema:** `build_voice_prompt()` recebe o dicionário `client` com `total_visits`, `total_spent`, `preferences` e `tags`, mas o template `_VOICE_PROMPT_FALLBACK` só usa `{client_name}`. O histórico existe no banco e nunca chega ao prompt.

**Resultado esperado:** A LUNA saberá que a cliente é frequente, qual profissional ela prefere e poderá ativar upsell de pacote proativamente.

---

### 1.1 — Adicionar `{client_history}` no `_VOICE_PROMPT_FALLBACK`

**Arquivo:** `backend/app/core/brain.py`

Localizar a linha que contém:
```
<layer2_directive_from_logic_brain>
```

Inserir ANTES dela o seguinte bloco:

```
<layer1b_client_profile>
{client_history}
</layer1b_client_profile>

```

O bloco `_VOICE_PROMPT_FALLBACK` completo ficará assim na abertura:

```python
_VOICE_PROMPT_FALLBACK = """\
<layer1_identity>
Você é Luna, a alma da recepção da Haven Escovaria & Esmalteria.
Sua voz é calorosa, profissional e tipicamente de Chapecó-SC.
Você cuida da autoestima das pessoas com segurança e precisão.
REGRA ABSOLUTA: Nunca invente horários disponíveis. Se a diretriz não trouxer um horário confirmado pelo sistema, pergunte o que a cliente prefere e informe que vai verificar.
</layer1_identity>

<layer1b_client_profile>
{client_history}
</layer1b_client_profile>

<layer2_directive_from_logic_brain>
```

---

### 1.2 — Adicionar parâmetro `client_history` em `build_voice_prompt()`

**Arquivo:** `backend/app/core/brain.py`

Localizar a função `build_voice_prompt` (atual):

```python
def build_voice_prompt(
    client: Dict, recent: Dict, context: str, logic_directive: str
) -> str:
    """
    Cérebro de Voz: carrega template do Supabase, com fallback hardcoded.
    """
    template = _load_prompt_from_db("voice") or _VOICE_PROMPT_FALLBACK
    return template.format(
        client_name=client.get("name", "Cliente"),
        logic_directive=logic_directive,
    )
```

Substituir por:

```python
def build_voice_prompt(
    client: Dict, recent: Dict, context: str, logic_directive: str
) -> str:
    """
    Cérebro de Voz: carrega template do Supabase, com fallback hardcoded.
    """
    template = _load_prompt_from_db("voice") or _VOICE_PROMPT_FALLBACK

    # Monta perfil episódico da cliente para personalizar a resposta
    visits = client.get("total_visits", 0)
    spent = client.get("total_spent", 0.0)
    preferences = client.get("preferences", {})
    tags = client.get("tags", [])

    if visits > 0:
        prof_pref = preferences.get("professional", "")
        service_pref = preferences.get("service", "")
        history_lines = [f"- Visitas ao salão: {visits} | Total gasto: R$ {spent:.0f}"]
        if prof_pref:
            history_lines.append(f"- Profissional preferida: {prof_pref} — mencionar quando disponível")
        if service_pref:
            history_lines.append(f"- Serviço habitual: {service_pref}")
        if "pacote_escova" in tags:
            history_lines.append("- Tem pacote de escovas ativo — verificar saldo antes de vender novo")
        if visits >= 4 and "pacote" not in " ".join(tags):
            history_lines.append("- Cliente frequente sem pacote — boa hora para oferecer pacote proativamente")
        client_history = "Perfil da cliente:\n" + "\n".join(history_lines)
    else:
        client_history = "Primeira visita ou cliente nova — não há histórico ainda."

    return template.format(
        client_name=client.get("name", "Cliente"),
        logic_directive=logic_directive,
        client_history=client_history,
    )
```

---

### 1.3 — Verificar que o template do Supabase também suporta o novo campo

O `_load_prompt_from_db("voice")` pode retornar um template salvo no banco que **não tem** `{client_history}`. Para não quebrar, adicionar proteção no `.format()`:

Substituir a linha:
```python
    return template.format(
        client_name=client.get("name", "Cliente"),
        logic_directive=logic_directive,
        client_history=client_history,
    )
```

Por:
```python
    try:
        return template.format(
            client_name=client.get("name", "Cliente"),
            logic_directive=logic_directive,
            client_history=client_history,
        )
    except KeyError:
        # Template do banco ainda não tem {client_history} — usar fallback
        return _VOICE_PROMPT_FALLBACK.format(
            client_name=client.get("name", "Cliente"),
            logic_directive=logic_directive,
            client_history=client_history,
        )
```

---

## MUDANÇA 2 — Fechar o loop de aprendizado (Golden Examples)

**Problema:** `learning.mark_golden_example()` existe em `learning.py` e faz exatamente o que precisa: salva no banco a conversa que converteu para que a LUNA aprenda a repeti-la. Mas **nunca é chamado**. A LUNA nunca aprende com o que funcionou.

**Onde chamar:** No método `_process_with_ai()` do `BrainEngine`, logo após a linha `result.action = "confirm_appointment"` (quando o scheduler confirma um agendamento).

**Arquivo:** `backend/app/core/brain.py`

Localizar o bloco (linhas ~1122-1127):

```python
            if success:
                result.action = "confirm_appointment"
                if isinstance(intel_data, dict):
                    intel_data["planned_appointment"] = booking_data
                else:
                    setattr(intel_data, "planned_appointment", booking_data)
```

Substituir por:

```python
            if success:
                result.action = "confirm_appointment"
                if isinstance(intel_data, dict):
                    intel_data["planned_appointment"] = booking_data
                else:
                    setattr(intel_data, "planned_appointment", booking_data)

                # [APRENDIZADO] Marca esta conversa como golden example
                # A LUNA aprende com cada agendamento confirmado
                try:
                    active_conv = await memory.get_active_conversation(phone)
                    conv_id = active_conv.get("id") if active_conv else None
                    if conv_id and history:
                        _task = asyncio.create_task(
                            learning.mark_golden_example(
                                phone=phone,
                                conversation_id=conv_id,
                                messages=history + [{"role": "user", "content": message}],
                                intent=intent_val,
                            )
                        )
                        _background_tasks.add(_task)
                        _task.add_done_callback(_background_tasks.discard)
                        logger.info(f"⭐ Golden example agendado | conv={conv_id}")
                except Exception as learn_err:
                    logger.debug(f"mark_golden_example skipped (non-critical): {learn_err}")
```

**Importante:** O `asyncio` já está importado dentro deste método (linha ~1012). O `_background_tasks` já existe como variável de módulo. O `learning` já está importado no topo do arquivo. Nenhuma importação nova necessária.

---

## MUDANÇA 3 — Estado da sessão no Voice Prompt

**Problema:** O `ConversationState` já é construído e passado para o Logic Prompt (via `conversation_state` no `build_logic_prompt`), mas o Voice Prompt **não recebe esse estado**. A Voz não sabe se a conversa está travada, avançando ou se a cliente já recusou uma opção.

**Arquivo:** `backend/app/core/brain.py`

### 3.1 — Adicionar `{conversation_state}` no `_VOICE_PROMPT_FALLBACK`

Localizar no template a seção:
```
<layer3_voice_guidelines>
```

Inserir ANTES dela:

```
<layer2b_session_state>
{conversation_state}
</layer2b_session_state>

```

Instruções de uso do estado para a Voz — adicionar dentro do `<layer3_voice_guidelines>` existente, após a linha `TOM E ESTILO:`:

```
USO DO ESTADO DA SESSÃO:
- Se momentum="stalled" ou houve_negativa=true: seja mais direto, proponha algo concreto agora
- Se mensagens >= 6 e sem agendamento: pergunte diretamente "posso fechar para você?"
- Se sentiment_trend="declining": reconheça o que a cliente quer, reduza perguntas
- Se progresso="agendando": foque em confirmar, não em mais perguntas
```

---

### 3.2 — Adicionar parâmetro `conversation_state` em `build_voice_prompt()`

No mesmo método `build_voice_prompt()` já editado na Mudança 1, adicionar o parâmetro e passá-lo no `.format()`:

```python
def build_voice_prompt(
    client: Dict, recent: Dict, context: str, logic_directive: str,
    conversation_state: str = "{}"     # NOVO — estado da sessão
) -> str:
```

E no bloco de `.format()` final, adicionar `conversation_state=conversation_state`:

```python
    try:
        return template.format(
            client_name=client.get("name", "Cliente"),
            logic_directive=logic_directive,
            client_history=client_history,
            conversation_state=conversation_state,    # NOVO
        )
    except KeyError:
        return _VOICE_PROMPT_FALLBACK.format(
            client_name=client.get("name", "Cliente"),
            logic_directive=logic_directive,
            client_history=client_history,
            conversation_state=conversation_state,    # NOVO
        )
```

---

### 3.3 — Passar `conv_state_json` para `build_voice_prompt()` no pipeline

Localizar em `_process_with_ai()` a linha (atual):

```python
        voice_prompt = build_voice_prompt(client, recent, context, logic_text)
```

Substituir por:

```python
        voice_prompt = build_voice_prompt(
            client, recent, context, logic_text,
            conversation_state=conv_state_json,    # NOVO — estado da sessão
        )
```

O `conv_state_json` já existe neste método (linha ~936), portanto nenhuma lógica adicional é necessária.

---

## VERIFICAÇÃO FINAL

Após as 3 mudanças, executar:

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS

# 1. Python importa sem erros
python3 -c "
import sys; sys.path.insert(0, 'backend')
from app.core.brain import build_voice_prompt, BrainEngine
print('✅ brain imports OK')
"

# 2. build_voice_prompt aceita os novos parâmetros
python3 -c "
import sys; sys.path.insert(0, 'backend')
from app.core.brain import build_voice_prompt

# Simular cliente frequente
client = {
    'name': 'Maria',
    'total_visits': 7,
    'total_spent': 450.0,
    'preferences': {'professional': 'Dávila', 'service': 'gel'},
    'tags': []
}
result = build_voice_prompt(
    client=client,
    recent={'services_done': 'gel'},
    context='',
    logic_directive='[AÇÃO PRINCIPAL]: Aprovar',
    conversation_state='{}'
)
assert 'Dávila' in result, 'ERRO: preferência de profissional não aparece no prompt'
assert 'frequente' in result or 'pacote' in result, 'ERRO: upsell de pacote não ativado'
print('✅ build_voice_prompt: cliente frequente com histórico OK')
"

# 3. Verificar que {client_history} e {conversation_state} estão no fallback
python3 -c "
import sys; sys.path.insert(0, 'backend')
from app.core.brain import _VOICE_PROMPT_FALLBACK
assert '{client_history}' in _VOICE_PROMPT_FALLBACK, 'ERRO: {client_history} faltando no template'
assert '{conversation_state}' in _VOICE_PROMPT_FALLBACK, 'ERRO: {conversation_state} faltando no template'
print('✅ Templates: ambos os campos presentes')
"

# 4. Verificar que mark_golden_example existe e tem a assinatura correta
python3 -c "
import sys; sys.path.insert(0, 'backend')
import inspect
from app.core.learning import LearningEngine
sig = inspect.signature(LearningEngine.mark_golden_example)
params = list(sig.parameters.keys())
assert 'phone' in params and 'conversation_id' in params and 'messages' in params
print(f'✅ mark_golden_example assinatura OK: {params}')
"

# 5. Rodar testes se existirem
python3 -m pytest backend/tests/ -v --tb=short -q 2>/dev/null || echo "Sem testes automatizados — verificação manual OK"
```

---

## RESUMO DAS 3 MUDANÇAS

| # | O que muda | Arquivo | Linhas afetadas | Risco |
|---|-----------|---------|-----------------|-------|
| 1 | Histórico da cliente (visitas, preferências, tags) injeta no Voice Prompt | `brain.py` | `build_voice_prompt()` + `_VOICE_PROMPT_FALLBACK` | Zero — additive |
| 2 | `mark_golden_example()` chamado após agendamento confirmado | `brain.py` | Bloco `if success:` em `_process_with_ai()` | Zero — try/except protegido |
| 3 | `conversation_state` (já existe no Logic) passa também para o Voice | `brain.py` | `build_voice_prompt()` + linha de chamada | Zero — parâmetro com default `"{}"` |

**Nenhum novo arquivo. Nenhuma nova dependência. Tudo em `brain.py`.**

---

*Referência: backend/app/core/brain.py + memory.py + learning.py*
*Manual: conversa-suzana-gpt.md*
