# 🚦 LUNA OS - Port Architecture

**Data**: 2026-02-27
**Status**: ✅ Documentado

---

## 📊 Arquitetura de Portas Oficial

| Serviço | Porta | URL | Status |
|---------|-------|-----|--------|
| **Frontend (Next.js)** | **3001** | http://localhost:3001 | ✅ **OFICIAL** |
| **Backend (FastAPI)** | 8000 | http://localhost:8000 | ✅ Oficial |
| **Evolution API** | 8081 | http://localhost:8081 | ✅ WhatsApp |
| ~~Porta 3000~~ | 3000 | ~~http://localhost:3000~~ | ❌ **NÃO USAR** |

---

## ⚠️ Problema: Duas Instâncias Frontend

### Cenário Comum

1. Você inicia o frontend: `npm run dev` → **Porta 3001** (oficial)
2. Algo trava ou você abre outro terminal
3. Inicia novamente: `npm run dev` → **Porta 3000** (porque 3001 está ocupada)
4. Resultado: **Dois frontends rodando!**

### Como Resolver

```bash
# Opção 1: Script automático (Recomendado)
cd LUNA_OS
./start.sh --clean

# Opção 2: Manual
lsof -ti:3000 | xargs kill -9
lsof -ti:3001 | xargs kill -9

# Depois inicie apenas um servidor na porta oficial
cd LUNA_OS/frontend
PORT=3001 npm run dev
```

---

## 🔧 Comandos Úteis

### Verificar Portas

```bash
# O que está rodando em cada porta
lsof -i :3000
lsof -i :3001
lsof -i :8000

# Todos processos Node
ps aux | grep node

# Todos processos Python
ps aux | grep python
```

### Matar Processos

```bash
# Matar tudo e limpar
killall -9 node
killall -9 uvicorn
killall -9 python

# Ou por porta
lsof -ti:3000 | xargs kill -9
lsof -ti:3001 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Iniciar Corretamente

```bash
# Frontend (porta 3000)
cd LUNA_OS/frontend
npm run dev

# Backend (porta 8000)
cd LUNA_OS/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🐳 Docker (Produção)

Com Docker, as portas são:

| Serviço | Porta Host | Porta Container | URL |
|---------|------------|-----------------|-----|
| **Frontend** | 3000 | 3000 | http://localhost:3000 |
| **Backend** | 8000 | 8000 | http://localhost:8000 |
| **Evolution** | 8081 | 8081 | http://localhost:8081 |

```bash
# Iniciar tudo com Docker
cd LUNA_OS
docker-compose up -d

# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f frontend
docker-compose logs -f backend
```

---

## 🔍 Como Saber Qual Frontend Está Usando

### Teste Rápido

Acesse no browser:
- http://localhost:3000 → Deve mostrar LUNA OS
- http://localhost:3001 → **NÃO ACESSAR** (instância duplicada)

### Ver no Terminal

```bash
# PID do processo na porta 3000
lsof -i :3000 | grep LISTEN

# Ver comando exato
ps aux | grep <PID>
```

---

## 📝 Fluxo Correto

### Desenvolvimento Local

```bash
# 1. Limpar portas (se necessário)
cd LUNA_OS
./start.sh --clean

# 2. Iniciar backend (Terminal 1)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# 3. Iniciar frontend (Terminal 2)
cd frontend
npm run dev

# 4. Acessar
# http://localhost:3000/clients
```

### Docker

```bash
# 1. Iniciar tudo
cd LUNA_OS
docker-compose up -d

# 2. Acessar
# http://localhost:3000/clients
```

---

## 🎯 Resumo

| Porta | Usar? | Por quê |
|-------|-------|---------|
| **3000** | ✅ SIM | Frontend oficial (Next.js default) |
| **3001** | ❌ NÃO | Instância duplicada (conflito) |
| **8000** | ✅ SIM | Backend oficial (FastAPI) |
| **8081** | ✅ SIM | Evolution API (WhatsApp) |

---

## 🛠️ Script de Cleanup

Salve como `cleanup.sh`:

```bash
#!/bin/bash
echo "🧹 Cleaning LUNA OS ports..."

for port in 3000 3001 8000; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "   Killing port $port (PID: $pid)"
        kill -9 $pid 2>/dev/null || true
    fi
done

echo "✅ All ports cleaned!"
```

---

## ✅ Checklist

- [ ] **Uma única instância** na porta 3000
- [ ] **Nenhuma instância** na porta 3001
- [ ] **Backend rodando** na porta 8000
- [ ] **Acessando** http://localhost:3000 (não 3001!)

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**
