# 🔧 Next.js Troubleshooting Guide

**Data**: 2026-02-27  
**Status**: ✅ RESOLVIDO

---

## 🎯 Problema Relatado

**Erro:**
```
Error: Could not find the module "/path/to/app/page.tsx#" 
in the React Client Manifest
```

**Sintoma:** Analytics carregando sem fim + erro no Dashboard

---

## ✅ Solução Aplicada

### 1. **Matar Processos**
```bash
killall -9 node next-server
```

### 2. **Limpar Cache do Next.js**
```bash
cd LUNA_OS/frontend
rm -rf .next
rm -rf node_modules/.cache
```

### 3. **Reiniciar na Porta Correta**
```bash
PORT=3001 npm run dev
```

---

## 🔍 Causa Raiz

O Next.js mantém um cache de build (`.next` folder) que pode corromper quando:
- Arquivos são modificados durante o build
- Múltiplas instâncias rodam simultaneamente
- Mudanças de porta (3000 ↔ 3001)
- Atualizações de dependências

---

## 🛠️ Comandos de Recuperação

### Cleanup Completo

```bash
# 1. Matar tudo
killall -9 node next-server

# 2. Limpar cache
cd LUNA_OS/frontend
rm -rf .next
rm -rf node_modules/.cache

# 3. Reiniciar
PORT=3001 npm run dev
```

### Script Automático

Salve como `fix-nextjs.sh`:

```bash
#!/bin/bash
echo "🔧 Fixing Next.js..."

# Kill processes
killall -9 node next-server 2>/dev/null
echo "✅ Processes killed"

# Clear cache
cd LUNA_OS/frontend
rm -rf .next
rm -rf node_modules/.cache
echo "✅ Cache cleared"

# Restart
echo "🚀 Starting on port 3001..."
PORT=3001 npm run dev
```

---

## 📊 Erros Comuns

### 1. **Module Not Found in Client Manifest**

**Causa:** Cache corrompido  
**Solução:** Limpar `.next` folder

```bash
rm -rf .next
```

### 2. **Loading Infinito**

**Causa:** Build em estado inconsistente  
**Solução:** Matar processos + limpar cache

```bash
killall -9 node
rm -rf .next
npm run dev
```

### 3. **Port Already in Use**

**Causa:** Múltiplas instâncias  
**Solução:** Matar instâncias antigas

```bash
lsof -ti:3001 | xargs kill -9
```

### 4. **Error: NEXT_NOT_FOUND**

**Causa:** Rota não existe ou cache corrompido  
**Solução:** Limpar cache + verificar arquivo existe

```bash
rm -rf .next
ls app/page.tsx  # Deve existir
```

---

## 🎯 Prevenção

### 1. **Sempre usar uma porta**

```bash
# Oficial
PORT=3001 npm run dev

# Nunca rodar sem especificar
npm run dev  # ❌ Pode pegar porta aleatória
```

### 2. **Não rodar múltiplas instâncias**

```bash
# Verificar antes de iniciar
lsof -i :3001

# Se já estiver rodando, usar ou matar
```

### 3. **Limpar cache periodicamente**

```bash
# Uma vez por semana ou após erros
rm -rf .next
```

### 4. **Usar script de start**

```bash
cd LUNA_OS
./start.sh --clean  # Limpa portas + mostra status
```

---

## 📋 Checklist de Diagnóstico

Quando algo não funcionar:

- [ ] 1. Verificar porta correta (3001)
  ```bash
  lsof -i :3001
  ```

- [ ] 2. Verificar se há múltiplas instâncias
  ```bash
  lsof -i :3000 -i :3001
  ```

- [ ] 3. Matar processos antigos
  ```bash
  killall -9 node next-server
  ```

- [ ] 4. Limpar cache
  ```bash
  rm -rf .next
  ```

- [ ] 5. Reiniciar na porta correta
  ```bash
  PORT=3001 npm run dev
  ```

- [ ] 6. Aguardar compilação (10-30s)
  ```bash
  sleep 10
  curl http://localhost:3001
  ```

---

## 🚀 Performance Tips

### 1. **Build em Produção**

```bash
npm run build
npm start
```

### 2. **Desabilitar Fast Refresh (dev)**

Se estiver muito lento:
```bash
# next.config.js
module.exports = {
  reactStrictMode: true,
  fastRefresh: false  // Desabilita
}
```

### 3. **Aumentar memória**

```bash
NODE_OPTIONS="--max-old-space-size=4096" npm run dev
```

---

## 📞 Comandos Úteis

```bash
# Ver processos Node
ps aux | grep node

# Ver portas ocupadas
lsof -i :3000 -i :3001 -i :8000

# Matar por porta
lsof -ti:3001 | xargs kill -9

# Limpar tudo
killall -9 node
rm -rf .next
rm -rf node_modules/.cache

# Verificar se está rodando
curl -s http://localhost:3001 | grep "Luna Core"
```

---

## ✅ Status Atual

```
✅ Cache limpo
✅ Processos mortos
✅ Servidor rodando na 3001
✅ Dashboard funcionando
✅ Analytics carregando
```

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Next.js recuperado e rodando na porta oficial 3001!* 🚀
