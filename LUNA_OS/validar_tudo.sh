#!/bin/bash

# 🧪 LUNA OS - Validação Completa de Sincronização
# Testa: Docker, APIs, Supabase e Painel
# Data: 2026-03-01

echo "============================================================"
echo "🧪 LUNA OS - Validação Completa de Sincronização"
echo "============================================================"
echo ""

# Contador de testes
PASS=0
FAIL=0

# ═══════════════════════════════════════════════
# 1. VALIDAR DOCKER
# ═══════════════════════════════════════════════

echo "📦 1. VALIDANDO DOCKER COMPOSE"
echo "------------------------------------------------------------"

if /usr/local/bin/docker --version &> /dev/null; then
    echo "✅ Docker instalado"
    ((PASS++))
    
    # Verificar containers
    CONTAINERS=$(/usr/local/bin/docker compose ps -q 2>/dev/null | wc -l | tr -d ' ')
    if [ "$CONTAINERS" -gt 0 ]; then
        echo "✅ $CONTAINERS containers rodando"
        ((PASS++))
        
        # Mostrar containers
        /usr/local/bin/docker compose ps
    else
        echo "⚠️  Nenhum container rodando"
        echo "💡 Execute: docker compose up -d"
        ((FAIL++))
    fi
else
    echo "❌ Docker não instalado"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════
# 2. VALIDAR BACKEND
# ═══════════════════════════════════════════════

echo "🔌 2. VALIDANDO BACKEND"
echo "------------------------------------------------------------"

# Health Check
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ 2>/dev/null)
if [ "$HEALTH" == "200" ]; then
    echo "✅ Backend respondendo (HTTP $HEALTH)"
    ((PASS++))
else
    echo "❌ Backend não respondendo (HTTP $HEALTH)"
    echo "💡 Verifique: docker compose logs luna-backend"
    ((FAIL++))
fi

# Testar API Professionals
PROF=$(curl -s http://localhost:8000/api/professionals 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('total', 0))" 2>/dev/null)
if [ "$PROF" == "9" ]; then
    echo "✅ Professionals API: $PROF/9 profissionais"
    ((PASS++))
else
    echo "⚠️  Professionals API: $PROF/9 profissionais (esperado 9)"
    ((FAIL++))
fi

# Testar API Services
SERV=$(curl -s http://localhost:8000/api/services | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('total', 0))" 2>/dev/null)
if [ "$SERV" == "34" ]; then
    echo "✅ Services API: $SERV/34 serviços"
    ((PASS++))
else
    echo "⚠️  Services API: $SERV/34 serviços (esperado 34)"
    ((FAIL++))
fi

# Testar API Packages
PACK=$(curl -s http://localhost:8000/api/packages 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('total', 0))" 2>/dev/null)
if [ "$PACK" == "4" ]; then
    echo "✅ Packages API: $PACK/4 pacotes"
    ((PASS++))
else
    echo "⚠️  Packages API: $PACK/4 pacotes (esperado 4)"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════
# 3. VALIDAR FRONTEND
# ═══════════════════════════════════════════════

echo "🖥️  3. VALIDANDO FRONTEND"
echo "------------------------------------------------------------"

FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/ 2>/dev/null)
if [ "$FRONTEND" == "200" ]; then
    echo "✅ Frontend respondendo (HTTP $FRONTEND)"
    ((PASS++))
else
    echo "❌ Frontend não respondendo (HTTP $FRONTEND)"
    echo "💡 Verifique: docker compose logs luna-frontend"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════
# 4. VALIDAR OBSIDIAN
# ═══════════════════════════════════════════════

echo "📂 4. VALIDANDO OBSIDIAN"
echo "------------------------------------------------------------"

OBSIDIAN_PATH="backend/app/knowledge/obsidian_vault/_Active/02-KNOWLEDGE"

if [ -d "$OBSIDIAN_PATH" ]; then
    echo "✅ Obsidian Knowledge existe"
    ((PASS++))

    # Contar Profissionais
    PROF_COUNT=$(find "$OBSIDIAN_PATH/Professionals" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$PROF_COUNT" == "9" ]; then
        echo "✅ Profissionais: $PROF_COUNT/9"
        ((PASS++))
    else
        echo "⚠️  Profissionais: $PROF_COUNT/9"
        ((FAIL++))
    fi

    # Contar Serviços
    SERV_COUNT=$(find "$OBSIDIAN_PATH/Services" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$SERV_COUNT" == "34" ]; then
        echo "✅ Serviços: $SERV_COUNT/34"
        ((PASS++))
    else
        echo "⚠️  Serviços: $SERV_COUNT/34"
        ((FAIL++))
    fi

    # Contar Pacotes
    PACK_COUNT=$(find "$OBSIDIAN_PATH/Packages" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$PACK_COUNT" == "4" ]; then
        echo "✅ Pacotes: $PACK_COUNT/4"
        ((PASS++))
    else
        echo "⚠️  Pacotes: $PACK_COUNT/4"
        ((FAIL++))
    fi
else
    echo "❌ Obsidian Knowledge não encontrado"
    ((FAIL+=4))
fi

echo ""

# ═══════════════════════════════════════════════
# 5. VALIDAR SEED SQL
# ═══════════════════════════════════════════════

echo "📄 5. VALIDANDO SEED SQL"
echo "------------------------------------------------------------"

SEED_FILE="backend/marketing_campaigns_migration.sql"

if [ -f "$SEED_FILE" ]; then
    echo "✅ Seed SQL existe"
    ((PASS++))

    # Contar INSERTs
    INSERT_COUNT=$(grep -c "INSERT INTO" "$SEED_FILE" 2>/dev/null)
    if [ "$INSERT_COUNT" -gt 0 ]; then
        echo "✅ Seed SQL tem $INSERT_COUNT INSERTs"
        ((PASS++))
    else
        echo "⚠️  Seed SQL sem INSERTs"
        ((FAIL++))
    fi
else
    echo "❌ Seed SQL não encontrado"
    ((FAIL+=2))
fi

echo ""

# ═══════════════════════════════════════════════
# RESUMO FINAL
# ═══════════════════════════════════════════════

echo "============================================================"
echo "📊 RESUMO FINAL"
echo "============================================================"
echo ""

TOTAL=$((PASS + FAIL))
PORCENTAGEM=$((PASS * 100 / TOTAL))

echo "✅ Testes Passados: $PASS/$TOTAL"
echo "❌ Testes Falhados: $FAIL/$TOTAL"
echo "📊 Porcentagem: $PORCENTAGEM%"
echo ""

if [ "$PORCENTAGEM" == "100" ]; then
    echo "🎉 PARABÉNS! SINCRONIZAÇÃO 100% COMPLETA!"
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "   1. Acessar Painel: http://localhost:3000"
    echo "   2. Validar páginas:"
    echo "      - /professionals"
    echo "      - /services"
    echo "      - /packages"
    echo "   3. Executar testes automatizados"
    echo "   4. Validar com equipe"
elif [ "$PORCENTAGEM" -ge 80 ]; then
    echo "✅ QUASE LÁ! Quase tudo sincronizado."
    echo ""
    echo "📝 FALTA POUCO:"
    echo "   - Verifique os testes falhados acima"
    echo "   - Execute: docker compose logs <container>"
elif [ "$PORCENTAGEM" -ge 50 ]; then
    echo "⏳ EM ANDAMENTO. Continue os passos."
    echo ""
    echo "📝 RECOMENDAÇÕES:"
    echo "   - Execute: docker compose up -d"
    echo "   - Verifique os logs: docker compose logs"
else
    echo "⚠️ INICIANDO. Siga o guia de sincronização."
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "   1. Executar Seed SQL no Supabase"
    echo "   2. Executar: docker compose up -d"
    echo "   3. Validar APIs"
fi

echo ""
echo "============================================================"

# Exit code
if [ "$FAIL" -gt 0 ]; then
    exit 1
else
    exit 0
fi
