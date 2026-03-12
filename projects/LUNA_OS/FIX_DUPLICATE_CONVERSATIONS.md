# 🔧 Correção: Duplicação de Conversas

## 📋 Problema Identificado

**Sintoma:**
- Mesmas conversas aparecendo múltiplas vezes no sistema
- Números de telefone em formatos diferentes criavam registros duplicados
- Exemplo: `5549999999999@lid` e `5549999999999@s.whatsapp.net` eram tratados como clientes diferentes

**Causa Raiz:**
- A Evolution API retorna números em formatos inconsistentes:
  - `@s.whatsapp.net` - Número normal do WhatsApp
  - `@lid` - ID Local do WhatsApp (pode variar entre dispositivos)
  - Números puros sem sufixo
- O sistema não estava normalizando esses formatos antes de salvar no banco
- Resultado: mesmo cliente com múltiplos IDs, múltiplas conversas, múltiplos históricos

---

## ✅ Solução Implementada

### 1. Módulo de Normalização de Telefones

**Arquivo:** `backend/app/utils/phone_normalization.py`

**Funções principais:**

```python
# Normaliza para formato padrão: 55<DDD><NUMERO>@s.whatsapp.net
normalize_phone_number(phone: str) -> str

# Normaliza para formato plano: 55<DDD><NUMERO>
normalize_phone_plain(phone: str) -> str

# Verifica se dois números são o mesmo
are_same_phone(phone1: str, phone2: str) -> bool

# Formata para exibição
format_phone_for_display(phone: str) -> str
```

**Exemplos de normalização:**

| Entrada | Saída |
|---------|-------|
| `5549999999999` | `5549999999999@s.whatsapp.net` |
| `49999999999` | `5549999999999@s.whatsapp.net` |
| `+55 49 99999-9999` | `5549999999999@s.whatsapp.net` |
| `5549999999999@lid` | `5549999999999@s.whatsapp.net` |
| `5549999999999@s.whatsapp.net` | `5549999999999@s.whatsapp.net` |

---

### 2. Correção no Webhook

**Arquivo:** `backend/app/api/webhooks.py`

**Mudanças:**

```python
# ANTES (linha ~277)
remote_jid = key.get("remoteJid", "")

# DEPOIS
remote_jid_raw = key.get("remoteJid", "")
remote_jid = normalize_phone_number(remote_jid_raw)
logger.debug(f"🔢 Phone normalized: {remote_jid_raw} → {remote_jid}")
```

**Impacto:**
- Todas as mensagens recebidas agora usam formato padronizado
- Previne criação de novas duplicatas

---

### 3. Correção no Serviço de Sincronização

**Arquivo:** `backend/app/core/whatsapp_sync_service.py`

**Mudanças:**

```python
# ANTES (sync_contacts)
jid = contact.get("remoteJid", "")

# DEPOIS
jid_raw = contact.get("remoteJid", "")
jid = normalize_phone_number(jid_raw)
```

```python
# ANTES (sync_chats_and_messages)
jid = chat.get("remoteJid", "")

# DEPOIS
jid_raw = chat.get("remoteJid", "")
jid = normalize_phone_number(jid_raw)
```

**Impacto:**
- Sincronização usa formato padronizado
- Histórico consolidado corretamente

---

### 4. Script de Migração

**Arquivo:** `backend/scripts/migrate_consolidate_duplicates.py`

**O que faz:**
1. Identifica todos os números duplicados no banco
2. Encontra conversas duplicadas
3. Consolida clients (mantém o mais antigo como primário)
4. Move mensagens para conversas consolidadas
5. Atualiza formato dos telefones

**Uso:**

```bash
# 1. Dry run (apenas simula)
python backend/scripts/migrate_consolidate_duplicates.py

# 2. Executar de verdade (edite o script primeiro)
# Mude: DRY_RUN = False
python backend/scripts/migrate_consolidate_duplicates.py
```

**Output esperado:**

```
══════════════════════════════════════════════════════════
🔄 MIGRAÇÃO: CONSOLIDAR CONVERSAS DUPLICADAS
📅 2026-03-11T23:45:00
🔍 DRY_RUN: True
══════════════════════════════════════════════════════════
⚠️  DRY RUN MODE - Nenhuma alteração será feita no banco
💡 Para executar de verdade, mude DRY_RUN = False no script
✅ Supabase conectado

🔍 Buscando telefones duplicados...
📊 Total de clients encontrados: 150
🔴 Duplicatas encontradas: 23 grupos
🔴 Registros extras para consolidar: 31

🔍 Buscando conversas duplicadas...
📊 Conversas encontradas: 89
🔴 Grupos de conversas duplicadas: 15

🔄 Consolidando clients duplicados...
...

✅ MIGRAÇÃO CONCLUÍDA
📊 Grupos duplicados consolidados: 23
📊 Clients consolidados: 31
📊 Conversas consolidadas: 15
```

---

## 🚀 Como Aplicar a Correção

### Passo 1: Testar a Normalização

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend

# Testar módulo de normalização
python app/utils/phone_normalization.py
```

**Output esperado:**
```
Testing normalize_phone_number:
  ✅ 5549999999999                  → 5549999999999@s.whatsapp.net
  ✅ 49999999999                    → 5549999999999@s.whatsapp.net
  ✅ +55 49 99999-9999              → 5549999999999@s.whatsapp.net
  ✅ 5549999999999@lid              → 5549999999999@s.whatsapp.net
  ...
```

---

### Passo 2: Reiniciar o Backend

```bash
# No container do backend
docker restart luna-backend

# Ou, se estiver rodando localmente
# Reinicie o processo do FastAPI
```

**Verificar logs:**
```bash
docker logs -f luna-backend | grep "Phone normalized"
```

**Output esperado:**
```
🔢 Phone normalized: 5549999999999@lid → 5549999999999@s.whatsapp.net
🔢 Phone normalized: 5549999999999@s.whatsapp.net → 5549999999999@s.whatsapp.net
```

---

### Passo 3: Rodar Migração (Dry Run)

```bash
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend

# Dry run primeiro (não altera nada)
python scripts/migrate_consolidate_duplicates.py
```

**Verificar output:**
- Quantas duplicatas foram encontradas?
- Quantos clients serão consolidados?
- Quantas conversas serão consolidadas?

---

### Passo 4: Rodar Migração (Produção)

**⚠️ ATENÇÃO: Backup primeiro!**

```bash
# 1. Backup do banco
docker exec luna-supabase pg_dump -U postgres -d postgres > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Edite o script
# Mude: DRY_RUN = False

# 3. Execute
python scripts/migrate_consolidate_duplicates.py
```

---

### Passo 5: Verificar Resultado

```bash
# Verificar se duplicatas foram consolidadas
# (Rode uma query no Supabase ou use o dashboard)

SELECT 
    phone,
    COUNT(*) as count
FROM clients
GROUP BY phone
HAVING COUNT(*) > 1;
```

**Resultado esperado:** `0 rows` (nenhuma duplicata)

---

## 📊 Monitoramento Pós-Correção

### O que monitorar:

1. **Logs de normalização:**
   ```bash
   docker logs luna-backend | grep "Phone normalized" | tail -20
   ```

2. **Novas duplicatas:**
   ```sql
   SELECT phone, COUNT(*) 
   FROM clients 
   GROUP BY phone 
   HAVING COUNT(*) > 1;
   ```

3. **Conversas ativas:**
   ```sql
   SELECT phone, COUNT(*) as conversations
   FROM conversations
   WHERE status = 'active'
   GROUP BY phone
   HAVING COUNT(*) > 1;
   ```

### Métricas de sucesso:

| Métrica | Antes | Depois |
|---------|-------|--------|
| Clients duplicados | 23 grupos | 0 |
| Conversas duplicadas | 15 grupos | 0 |
| Normalizações/dia | 0 | ~100-500 |

---

## 🐛 Troubleshooting

### Problema: Script de migração falha

**Causa:** Permissão de banco ou conexão

**Solução:**
```bash
# Verificar conexão
docker exec -it luna-backend python -c "from app.integrations.supabase_client import get_supabase; print(get_supabase())"

# Verificar permissões
docker exec luna-supabase psql -U postgres -c "\dt"
```

---

### Problema: Normalização não funciona

**Causa:** Módulo não importado corretamente

**Solução:**
```bash
# Verificar import
docker exec -it luna-backend python -c "from app.utils.phone_normalization import normalize_phone_number; print(normalize_phone_number('49999999999'))"
```

---

### Problema: Duplicatas persistem após migração

**Causa:** DRY_RUN ainda está True ou migração falhou

**Solução:**
```bash
# Verificar se DRY_RUN = False
grep "DRY_RUN" scripts/migrate_consolidate_duplicates.py

# Rodar novamente
python scripts/migrate_consolidate_duplicates.py
```

---

## 📚 Arquivos Modificados

| Arquivo | Mudança | Status |
|---------|---------|--------|
| `app/utils/phone_normalization.py` | Criado | ✅ Novo |
| `app/api/webhooks.py` | Normalização no webhook | ✅ Corrigido |
| `app/core/whatsapp_sync_service.py` | Normalização na sync | ✅ Corrigido |
| `scripts/migrate_consolidate_duplicates.py` | Script de migração | ✅ Novo |

---

## ✅ Checklist de Aplicação

- [ ] Testar módulo de normalização
- [ ] Reiniciar backend
- [ ] Verificar logs de normalização
- [ ] Rodar migração (dry run)
- [ ] Fazer backup do banco
- [ ] Rodar migração (produção)
- [ ] Verificar resultado
- [ ] Monitorar por 24h

---

*Criado: 2026-03-11*
*LUNA OS v3.0*
