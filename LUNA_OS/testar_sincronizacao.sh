#!/bin/bash

# 🧪 Testar Sincronização de Dados - Marketing & Upsell

echo "============================================================"
echo "🧪 TESTANDO SINCRONIZAÇÃO DE DADOS"
echo "============================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Testar Campanhas Ativas
echo -e "${YELLOW}📢 1. TESTANDO CAMPANHAS ATIVAS${NC}"
echo "------------------------------------------------------------"
CAMPAGNAS=$(curl -s http://localhost:8000/api/campaigns/active)
echo "$CAMPAGNAS" | python3 -m json.tool

CAMPAGNAS_COUNT=$(echo "$CAMPAGNAS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null)

if [ "$CAMPAGNAS_COUNT" -gt 0 ] 2>/dev/null; then
    echo -e "${GREEN}✅ $CAMPAGNAS_COUNT campanhas encontradas!${NC}"
else
    echo -e "${RED}❌ Nenhuma campanha encontrada${NC}"
    echo -e "${YELLOW}💡 Execute o SQL no Supabase primeiro!${NC}"
fi

echo ""

# 2. Testar Upsell para Escova Lisa
echo -e "${YELLOW}💰 2. TESTANDO UPSELL - ESCOVA LISA${NC}"
echo "------------------------------------------------------------"
UPSELL=$(curl -s http://localhost:8000/api/campaigns/upsell/escova_lisa)
echo "$UPSELL" | python3 -m json.tool

UPSELL_COUNT=$(echo "$UPSELL" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null)

if [ "$UPSELL_COUNT" -gt 0 ] 2>/dev/null; then
    echo -e "${GREEN}✅ $UPSELL_COUNT oportunidades de upsell encontradas!${NC}"
else
    echo -e "${RED}❌ Nenhum upsell encontrado${NC}"
fi

echo ""

# 3. Testar Sugestão de Campanha
echo -e "${YELLOW}🎯 3. TESTANDO SUGESTÃO DE CAMPANHA${NC}"
echo "------------------------------------------------------------"
SUGGEST=$(curl -s "http://localhost:8000/api/campaigns/suggest/escova_lisa")
echo "$SUGGEST" | python3 -m json.tool

if [[ "$SUGGEST" == *"PGRST202"* ]] || [[ "$SUGGEST" == *"function"* ]]; then
    echo -e "${RED}❌ Funções não encontradas no Supabase${NC}"
    echo -e "${YELLOW}💡 Execute o SQL no Supabase primeiro!${NC}"
else
    echo -e "${GREEN}✅ Sugestão de campanha encontrada!${NC}"
fi

echo ""

# 4. Testar Outros Serviços
echo -e "${YELLOW}🎯 4. TESTANDO OUTROS SERVIÇOS${NC}"
echo "------------------------------------------------------------"

echo "Testando: progressiva_curtos"
curl -s "http://localhost:8000/api/campaigns/suggest/progressiva_curtos" | python3 -m json.tool | head -20

echo ""
echo "Testando: design_sobrancelha"
curl -s "http://localhost:8000/api/campaigns/suggest/design_sobrancelha" | python3 -m json.tool | head -20

echo ""

# 5. Resumo Final
echo "============================================================"
echo -e "${YELLOW}📊 RESUMO FINAL${NC}"
echo "============================================================"
echo ""

if [ "$CAMPAGNAS_COUNT" -gt 0 ] 2>/dev/null && [ "$UPSELL_COUNT" -gt 0 ] 2>/dev/null && [[ "$SUGGEST" != *"PGRST202"* ]]; then
    echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM!${NC}"
    echo ""
    echo -e "${GREEN}🎉 APIs de campanhas e upsell estão funcionando!${NC}"
    echo ""
    echo -e "${GREEN}📝 PRÓXIMOS PASSOS:${NC}"
    echo "   1. ✅ SQL executado no Supabase"
    echo "   2. ✅ APIs testadas e funcionando"
    echo "   3. 🔄 Acessar painel frontend"
    echo "   4. 🔄 Testar no Dojo"
else
    echo -e "${RED}⚠️  ALGUNS TESTES FALHARAM${NC}"
    echo ""
    echo -e "${YELLOW}📝 PRÓXIMOS PASSOS:${NC}"
    echo "   1. Acessar: https://supabase.com/dashboard"
    echo "   2. Abrir SQL Editor"
    echo "   3. Copiar: backend/database/migrations/03_marketing_and_upsell.sql"
    echo "   4. Executar SQL no Supabase"
    echo "   5. Voltar aqui e testar novamente: bash testar_sincronizacao.sh"
fi

echo ""
echo "============================================================"
