#!/bin/bash

# 🧪 Testar APIs de Campanhas e Upsell

echo "============================================================"
echo "🧪 TESTANDO APIS DE CAMPANHAS E UPSELL"
echo "============================================================"
echo ""

# 1. Testar Campanhas Ativas
echo "📢 1. TESTANDO CAMPANHAS ATIVAS"
echo "------------------------------------------------------------"
CAMPAGNAS=$(curl -s http://localhost:8000/api/campaigns/active)
echo "$CAMPAGNAS" | python3 -m json.tool

if [ "$CAMPAGNAS" == "[]" ]; then
    echo "⚠️  Nenhuma campanha encontrada"
    echo "💡 Execute o SQL no Supabase primeiro!"
else
    echo "✅ Campanhas encontradas!"
fi

echo ""

# 2. Testar Upsell para Escova Lisa
echo "💰 2. TESTANDO UPSELL - ESCOVA LISA"
echo "------------------------------------------------------------"
UPSELL=$(curl -s http://localhost:8000/api/campaigns/upsell/escova_lisa)
echo "$UPSELL" | python3 -m json.tool

if [[ "$UPSELL" == *"detail"* ]]; then
    echo "⚠️  API não encontrada"
else
    echo "✅ Upsell encontrado!"
fi

echo ""

# 3. Testar Sugestão de Campanha
echo "🎯 3. TESTANDO SUGESTÃO DE CAMPANHA"
echo "------------------------------------------------------------"
SUGGEST=$(curl -s "http://localhost:8000/api/campaigns/suggest/escova_lisa")
echo "$SUGGEST" | python3 -m json.tool

if [[ "$SUGGEST" == *"PGRST202"* ]]; then
    echo "⚠️  Função não encontrada no Supabase"
    echo "💡 Execute o SQL no Supabase primeiro!"
else
    echo "✅ Sugestão encontrada!"
fi

echo ""

# 4. Resumo
echo "============================================================"
echo "📊 RESUMO DOS TESTES"
echo "============================================================"
echo ""

if [ "$CAMPAGNAS" != "[]" ] && [[ "$UPSELL" != *"detail"* ]] && [[ "$SUGGEST" != *"PGRST202"* ]]; then
    echo "✅ TODOS OS TESTES PASSARAM!"
    echo ""
    echo "🎉 APIs de campanhas e upsell estão funcionando!"
else
    echo "⚠️  ALGUNS TESTES FALHARAM"
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "   1. Acessar: https://supabase.com/dashboard"
    echo "   2. Abrir SQL Editor"
    echo "   3. Copiar: backend/marketing_campaigns_migration.sql"
    echo "   4. Executar SQL no Supabase"
    echo "   5. Voltar aqui e testar novamente"
fi

echo ""
echo "============================================================"
