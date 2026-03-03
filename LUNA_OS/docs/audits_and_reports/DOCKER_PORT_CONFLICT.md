# 🐳 Docker Port Conflict Resolution

**Data**: 2026-02-27  
**Status**: ✅ RESOLVIDO

---

## 🎯 Problema Identificado

**Porta 3000 não funciona** porque Docker está usando:
```
luna-frontend container: 0.0.0.0:3000->3000/tcp
```

**Porta 3001 funciona** porque está livre.

---

## ✅ Solução Aplicada

### 1. **Parar Container Docker**

```bash
docker stop luna-frontend
docker rm luna-frontend
```

### 2. **Script Automático**

Criado `reset-and-start.sh`:
- Para containers Docker
- Limpa portas
- Limpa cache Next.js
- Inicia Next.js na 3001

---

## 🚀 Como Usar

### Script Automático (Recomendado)

```bash
cd LUNA_OS
./reset-and-start.sh
```

### Manual

```bash
# 1. Parar Docker
docker stop luna-frontend
docker rm luna-frontend

# 2. Matar processos Node
killall -9 node next-server

# 3. Limpar cache
cd LUNA_OS/frontend
rm -rf .next

# 4. Iniciar Next.js
PORT=3001 npm run dev
```

---

## 📊 Portas Oficiais

| Serviço | Porta | Status |
|---------|-------|--------|
| **Next.js (Local)** | **3001** | ✅ Oficial |
| Docker Frontend | 3000 | ❌ Conflito |
| Backend API | 8000 | ✅ OK |
| Evolution | 8081 | ✅ OK |

---

## 🔍 Verificar Portas

```bash
# Ver o que está usando cada porta
lsof -i :3000
lsof -i :3001

# Ver containers Docker
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

---

## 🎯 URLs

```
✅ Oficial: http://localhost:3001
❌ Não usar: http://localhost:3000 (Docker)
```

---

## 🛠️ Em Caso de Conflito

### Verificar Docker

```bash
# Listar containers
docker ps

# Ver portas
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### Parar Containers

```bash
# Parar frontend
docker stop luna-frontend

# Parar backend
docker stop luna-backend

# Remover todos
docker rm luna-frontend luna-backend
```

### Ou Usar Script

```bash
./reset-and-start.sh  # Faz tudo automaticamente
```

---

## 📋 Lições Aprendidas

### 1. **Docker vs Local**

- Docker usa porta 3000 por padrão
- Next.js local tenta usar 3000
- **Solução**: Next.js usa 3001

### 2. **Sempre Verificar Portas**

Antes de iniciar:
```bash
lsof -i :3000 -i :3001
```

### 3. **Script de Reset**

Sempre usar `reset-and-start.sh` para:
- Limpar Docker
- Limpar processos
- Limpar cache
- Iniciar corretamente

---

## ✅ Status Atual

```
✅ Docker: parado (portas liberadas)
✅ Next.js: rodando na 3001
✅ Porta 3000: livre
✅ Porta 3001: em uso
✅ Dashboard: funcionando
```

---

## 🎯 Comandos Úteis

```bash
# Reset completo
./reset-and-start.sh

# Ver Docker
docker ps

# Ver portas
lsof -i :3000 -i :3001

# Parar Docker
docker stop luna-frontend luna-backend

# Iniciar Next.js
cd LUNA_OS/frontend && PORT=3001 npm run dev
```

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Conflito Docker resolvido! Porta 3001 é a oficial!* 🚀
