# 📋 LUNA OS - Rotina de Operações Diárias

**Para:** Operadores do Sistema  
**Tempo:** 5-10 minutos por dia  
**Frequência:** Diário (manhã)

---

## 🌅 Checklist Matinal (5 min)

### 1. Health Check Rápido (2 min)

```bash
# Vá para a pasta do LUNA OS
cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS

# Rode o health check
./scripts/health-check.sh
```

**O que procurar:**
- ✅ Todos os checks verdes = OK, pode ir para o próximo passo
- ⚠️ Algum amarelo = Anote, mas continue
- ❌ Algum vermelho = Pare e me avise

---

### 2. Verificar Backups (1 min)

```bash
# Verifique se backup foi feito hoje
ls -lh /tmp/luna_backups/ | grep $(date +%Y%m%d)
```

**Deveria ver:**
- `windmill_db_YYYYMMDD_HHMMSS.sql`
- `evolution_db_YYYYMMDD_HHMMSS.sql`
- `configs_YYYYMMDD_HHMMSS.tar.gz`

**Se não tiver backup de hoje:**
```bash
# Rode backup manual
./scripts/backup.sh
```

---

### 3. Verificar Jobs do Windmill (2 min)

```
1. Acesse: http://localhost:8001
2. Vá em: Jobs
3. Filtre por: Failed (últimas 24h)
```

**O que procurar:**
- ✅ Nenhum job falho = OK
- ⚠️ 1-2 jobs falhos = Anote, investigue se persistir
- ❌ 3+ jobs falhos = Me avise

---

### 4. Verificar Logs de Erro (2 min)

```bash
# Backend
docker logs luna-backend --tail 50 | grep -i error

# Windmill
docker logs luna-windmill-server --tail 50 | grep -i error

# Evolution
docker logs luna-evo-api --tail 50 | grep -i error
```

**O que procurar:**
- ✅ Sem erros = OK
- ⚠️ Erros ocasionais = Anote
- ❌ Muitos erros repetidos = Me avise

---

### 5. Verificar WhatsApp (1 min)

```
1. Acesse: http://localhost:8081/manager
2. Verifique se instância "haven" está conectada
3. Mande um "oi" de teste para seu número
```

**Deveria:**
- ✅ Instância conectada
- ✅ Mensagem enviada e recebida

---

## 📊 Checklist Semanal (15 min - Toda Segunda)

### 1. Revisar Métricas da Semana (5 min)

```bash
# Jobs executados na semana
curl -H "X-API-Key: YOUR_KEY" \
  "http://localhost:8000/api/windmill/jobs?limit=1000" | \
  python3 -c "import sys,json; jobs=json.load(sys.stdin); print(f'Total: {len(jobs)}')"

# Health dos serviços
./scripts/health-check.sh
```

**Anote:**
- Total de jobs na semana
- Quantos falharam
- Quais serviços tiveram problema

---

### 2. Limpar Backups Antigos (2 min)

```bash
# O script já faz isso automaticamente, mas pode verificar
ls -lh /tmp/luna_backups/
```

**Deveria ter:**
- Backups dos últimos 7 dias
- Nenhum backup com > 30 dias

---

### 3. Testar Restore de Backup (5 min - uma vez por mês)

```bash
# Escolha um backup antigo
# Teste restore em ambiente de staging (NÃO em produção)

# Exemplo (NÃO RODE EM PRODUÇÃO SEM TESTAR):
# docker exec -i luna-windmill-db psql -U luna_user -d windmill < backup.sql
```

---

### 4. Revisar Logs de Segurança (3 min)

```bash
# Tentativas de login falhas
docker logs luna-backend --since 7d | grep -i "401\|403"

# Acessos não autorizados
docker logs luna-frontend --since 7d | grep -i "error"
```

---

## 🚨 O Que Fazer Quando Algo Der Errado

### Cenário 1: Backend Não Responde

```bash
# 1. Verifique se está rodando
docker ps | grep luna-backend

# 2. Se não estiver, reinicie
docker restart luna-backend

# 3. Verifique logs
docker logs luna-backend --tail 100

# 4. Se persistir, me avise com os logs
```

---

### Cenário 2: WhatsApp Não Envia

```bash
# 1. Verifique Evolution API
curl -H "apikey: mothership_master_2026" \
  http://localhost:8081/instance/connectionStatus/haven

# 2. Se estiver "close", reinicie
docker restart luna-evo-api

# 3. Verifique se reconectou
# Acesse: http://localhost:8081/manager
```

---

### Cenário 3: Windmill Jobs Falhando

```bash
# 1. Veja quais jobs falharam
# Acesse: http://localhost:8001 → Jobs → Filter: Failed

# 2. Verifique logs do Windmill
docker logs luna-windmill-server --tail 100

# 3. Se for erro de banco, reinicie
docker restart luna-windmill-db
docker restart luna-windmill-server

# 4. Se persistir, me avise
```

---

### Cenário 4: Disco Cheio

```bash
# 1. Verifique espaço
df -h

# 2. Limpe logs antigos
docker system prune -af

# 3. Limpe backups antigos
find /tmp/luna_backups -mtime +7 -delete

# 4. Se ainda estiver cheio, me avise
```

---

## 📞 Quando Me Chamar

### **Imediato (Pare Tudo)**
```
❌ Backend não inicia após restart
❌ WhatsApp não envia mensagens há > 1 hora
❌ Disco 100% cheio
❌ Dados corrompidos/perdidos
```

### **Urgente (Mesmo Dia)**
```
⚠️ Jobs falhando repetidamente
⚠️ Health check vermelho há > 4 horas
⚠️ Backup falhando há > 2 dias
⚠️ Lentidão extrema (> 10s por operação)
```

### **Não Urgente (Próximo Dia Útil)**
```
• Health check amarelo
• 1-2 jobs falhos isolados
• Dúvidas de operação
• Sugestões de melhoria
```

---

## 📝 Template de Report de Problema

Quando precisar me avisar de um problema, use este formato:

```markdown
### Problema:
[Descreva o que está acontecendo]

### Quando começou:
[Data/hora aproximada]

### O Que Já Tentou:
[Passos que já fez para resolver]

### Logs (se tiver):
[Cole os logs relevantes]

### Impacto:
[O que está afetado: clientes não recebem mensagem, etc]
```

---

## ✅ Checklist de Fim de Dia (Opcional - 2 min)

```
[ ] Health check está verde
[ ] WhatsApp está enviando normalmente
[ ] Nenhum job crítico falhou
[ ] Backup foi feito (se for fim de dia)
```

**Se tudo OK, pode ir para casa tranquilo!** 🎉

---

## 📚 Recursos Úteis

| Recurso | URL/Comando |
|---------|-------------|
| Health Check | `./scripts/health-check.sh` |
| Backup | `./scripts/backup.sh` |
| Backend Logs | `docker logs luna-backend -f` |
| Windmill UI | http://localhost:8001 |
| Evolution Manager | http://localhost:8081/manager |
| Frontend | http://localhost:3000 |

---

**Próxima revisão:** 2026-03-18  
**Versão:** 1.0
