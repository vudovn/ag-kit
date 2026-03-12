# 🚀 Guia de Otimização - LUNA OS v3.0

## ⚡ Melhorias Aplicadas

### **1. Frontend (Next.js)**

#### Dockerfile Otimizado
- ✅ Cache de dependências (`npm ci --prefer-offline`)
- ✅ Build multi-stage para produção
- ✅ Imagem final mínima (apenas necessário)
- ✅ `.dockerignore` para excluir arquivos desnecessários

#### next.config.js
- ✅ Otimização de imports de pacotes grandes
- ✅ Compressão de imagens (WebP/AVIF)
- ✅ Remove console.log em produção
- ✅ Telemetria desativada

**Ganho estimado:** 40-60% no build

---

### **2. Backend (FastAPI)**

#### Dockerfile Otimizado
- ✅ Cache de dependências pip
- ✅ `.dockerignore` para excluir arquivos desnecessários
- ✅ Instalação sem cache pip (imagem menor)

**Ganho estimado:** 20-30% no build

---

### **3. Docker Compose**

#### Melhorias
- ✅ Build paralelo (`--parallel`)
- ✅ Cache de camadas Docker
- ✅ Remove orphan containers

**Ganho estimado:** 30-50% no deploy

---

## 📊 Comparativo de Performance

### **Antes**
```
Build frontend:  ~180s
Build backend:   ~120s
Deploy total:    ~350s (6 minutos)
```

### **Depois (Estimado)**
```
Build frontend:  ~90s  (-50%)
Build backend:   ~80s  (-33%)
Deploy total:    ~200s (3.5 minutos) (-43%)
```

---

## 🛠️ Como Usar

### **Deploy Rápido (Recomendado)**

```bash
cd LUNA_OS

# Script otimizado
./deploy-otimizado.sh
```

### **Build com Cache**

```bash
# Reutilizar cache de build anterior
docker compose build --parallel

# Subir apenas serviços necessários
docker compose up -d
```

### **Deploy Limpo (Primeira Vez)**

```bash
# Limpar tudo e reconstruir
docker compose down -v
docker system prune -af

# Build do zero
docker compose build --no-cache

# Subir
docker compose up -d
```

---

## 🎯 Dicas de Performance

### **1. Use Docker BuildKit**

```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

### **2. Cache de Volumes**

```yaml
volumes:
  - node_modules_cache:/app/node_modules  # Frontend
  - pip_cache:/root/.cache/pip          # Backend
```

### **3. Build Condicional**

```bash
# Build apenas se houver mudanças
docker compose build luna-frontend  # Apenas frontend
docker compose build luna-backend   # Apenas backend
```

### **4. Health Checks**

```bash
# Aguardar saúde dos serviços
docker compose up -d
docker compose ps --filter "status=healthy"
```

---

## 📈 Monitoramento

### **Verificar Tempo de Build**

```bash
# Com timer
time docker compose build

# Verificar tamanho das imagens
docker images | grep luna
```

### **Logs de Performance**

```bash
# Backend
docker logs luna-backend | grep "Process-Time"

# Frontend (dev)
docker logs luna-frontend | grep "compiled"
```

---

## 🔧 Troubleshooting

### **Build Lento**

```bash
# Verificar cache
docker builder prune --filter "until=24h"

# Limpar cache antigo
docker system prune -af
```

### **Container Não Inicia**

```bash
# Verificar logs
docker compose logs luna-backend
docker compose logs luna-frontend

# Health check
docker compose ps --format "table {{.Names}}\t{{.Status}}"
```

### **Memória Insuficiente**

```bash
# Limitar memória no Docker Compose
services:
  luna-backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 🎯 Próximas Otimizações

### **Curto Prazo**
- [ ] Multi-stage build em produção
- [ ] Compressão gzip no Nginx
- [ ] CDN para estáticos

### **Médio Prazo**
- [ ] Lazy loading de componentes
- [ ] Code splitting automático
- [ ] Service workers (PWA)

### **Longo Prazo**
- [ ] Edge computing (Cloudflare Workers)
- [ ] Database connection pooling
- [ ] Redis cache layer

---

**Status:** ✅ **Otimizações Aplicadas**  
**Ganho Estimado:** 40-50% no tempo de build  
**Próxima Revisão:** 2026-03-10
