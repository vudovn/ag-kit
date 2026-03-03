#!/bin/bash

# ⚡ Testar Sovereign Switch

echo "============================================================"
echo "⚡ TESTANDO SOVEREIGN SWITCH"
echo "============================================================"
echo ""

# 1. Testar Estado Atual
echo "📊 1. ESTADO ATUAL"
echo "------------------------------------------------------------"
curl -s http://localhost:8000/api/settings/sovereign | python3 -m json.tool

echo ""

# 2. Ativar LUNA
echo "🚀 2. ATIVANDO LUNA (MODO ACTIVE)"
echo "------------------------------------------------------------"
curl -s -X POST http://localhost:8000/api/settings/sovereign \
  -H "Content-Type: application/json" \
  -d '{"luna_mode": "active"}' | python3 -m json.tool

echo ""

# 3. Verificar Saúde
echo "💚 3. SAÚDE DO SISTEMA"
echo "------------------------------------------------------------"
curl -s http://localhost:8000/api/settings/sovereign/health | python3 -m json.tool

echo ""

# 4. Testar Campanhas
echo "📢 4. TESTANDO CAMPANHAS"
echo "------------------------------------------------------------"
curl -s http://localhost:8000/api/campaigns/active | python3 -m json.tool

echo ""

# 5. Testar Upsell
echo "💰 5. TESTANDO UPSELL"
echo "------------------------------------------------------------"
curl -s http://localhost:8000/api/campaigns/upsell/escova_lisa | python3 -m json.tool

echo ""

# 6. Resumo
echo "============================================================"
echo "📊 RESUMO"
echo "============================================================"
echo ""

LUNA_MODE=$(curl -s http://localhost:8000/api/settings/sovereign | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('luna_mode', 'unknown'))" 2>/dev/null)

if [ "$LUNA_MODE" == "active" ]; then
    echo "✅ LUNA_MODE: ACTIVE"
    echo ""
    echo "🎉 LUNA está ativa e respondendo!"
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "   1. ✅ LUNA ativada"
    echo "   2. 🔄 Executar SQL no Supabase"
    echo "   3. 🔄 Testar campanhas"
    echo "   4. 🔄 Validar no Dojo"
else
    echo "⚠️  LUNA_MODE: $LUNA_MODE"
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "   1. ⏳ Ativar LUNA: bash testar_sovereign.sh"
    echo "   2. ⏳ Executar SQL no Supabase"
    echo "   3. ⏳ Testar campanhas"
fi

echo ""
echo "============================================================"
