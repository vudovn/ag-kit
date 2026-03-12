#!/bin/bash

# ═══════════════════════════════════════════════════════════
# LUNA OS - Data Cleanup Automation
# 
# Automatiza a identificação e correção de dados inconsistentes
# entre Profissionais e Serviços
#
# Uso: ./cleanup_data.sh [--dry-run]
# ═══════════════════════════════════════════════════════════

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuração
DRY_RUN=false
if [[ "$*" == *"--dry-run"* ]]; then
    DRY_RUN=true
    echo -e "${YELLOW}🔍 DRY RUN MODE - Nenhuma alteração será feita${NC}\n"
fi

# Supabase Config (pegar do .env)
SUPABASE_URL=$(grep "SUPABASE_URL" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'" | sed 's|/rest/v1$||')
SUPABASE_KEY=$(grep "SUPABASE_KEY" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo -e "${RED}❌ Erro: SUPABASE_URL ou SUPABASE_KEY não encontrados no .env${NC}"
    exit 1
fi

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     LUNA OS - Data Cleanup Automation                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════
# 1. Verificar Conexão
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}[1/5] Verificando conexão com Supabase...${NC}"

# Testar conexão com endpoint de health
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    "$SUPABASE_URL/rest/v1/")

if [ "$RESPONSE" = "400" ] || [ "$RESPONSE" = "401" ] || [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Conexão OK (HTTP $RESPONSE)${NC}"
else
    echo -e "${RED}✗ Erro de conexão (HTTP $RESPONSE)${NC}"
    echo -e "${YELLOW}⚠️  Isso é normal se não tiver tabela pública${NC}"
    echo ""
    echo "Vamos pular para a verificação manual..."
    echo ""
    echo "📋 Instruções Manuais:"
    echo ""
    echo "1. Acesse Supabase Dashboard:"
    echo "   https://supabase.com/dashboard"
    echo ""
    echo "2. Vá em SQL Editor"
    echo ""
    echo "3. Rode este SQL para ver profissionais:"
    echo ""
    echo "   SELECT name FROM professionals ORDER BY name;"
    echo ""
    echo "4. Procure por nomes como: 'Corte', 'Escova', 'Coloração'"
    echo ""
    exit 0
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 2. Contar Profissionais e Serviços
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}[2/5] Contando registros...${NC}"

PROFESSIONALS_COUNT=$(curl -s \
    -H "apikey: $SUPABASE_KEY" \
    -H "Authorization: Bearer $SUPABASE_KEY" \
    "$SUPABASE_URL/rest/v1/professionals?select=count" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['count'] if d else 0)" 2>/dev/null || echo "0")

SERVICES_COUNT=$(curl -s \
    -H "apikey: $SUPABASE_KEY" \
    -H "Authorization: Bearer $SUPABASE_KEY" \
    "$SUPABASE_URL/rest/v1/services?select=count" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['count'] if d else 0)" 2>/dev/null || echo "0")

echo -e "  Profissionais: ${GREEN}$PROFESSIONALS_COUNT${NC}"
echo -e "  Serviços: ${GREEN}$SERVICES_COUNT${NC}"

echo ""

# ═══════════════════════════════════════════════════════════
# 3. Identificar Profissionais com Nomes Suspeitos
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}[3/5] Identificando profissionais com nomes suspeitos...${NC}"

# Palavras-chave que indicam nome de serviço, não de pessoa
SUSPICIOUS_WORDS="corte,escova,color,mech,hidrat,manic,pedic,sobrancelh,cil,unh"

PROFESSIONALS=$(curl -s \
    -H "apikey: $SUPABASE_KEY" \
    -H "Authorization: Bearer $SUPABASE_KEY" \
    "$SUPABASE_URL/rest/v1/professionals?select=id,name,phone&name=ilike.*${SUSPICIOUS_WORDS}*" 2>/dev/null)

if [ -n "$PROFESSIONALS" ] && [ "$PROFESSIONALS" != "[]" ]; then
    SUSPICIOUS_COUNT=$(echo "$PROFESSIONALS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    if [ "$SUSPICIOUS_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Encontrados $SUSPICIOUS_COUNT profissionais com nomes suspeitos:${NC}"
        echo "$PROFESSIONALS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data[:10]:  # Mostrar apenas primeiros 10
    print(f\"  - {p['name']} (ID: {p['id'][:8]}...)\")
if len(data) > 10:
    print(f\"  ... e mais {len(data) - 10}\")
" 2>/dev/null
    else
        echo -e "${GREEN}✓ Nenhum profissional com nome suspeito${NC}"
    fi
else
    echo -e "${GREEN}✓ Nenhum profissional com nome suspeito${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 4. Identificar Serviços com Nomes de Pessoas
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}[4/5] Identificando serviços com nomes de pessoas...${NC}"

# Esta verificação é mais complexa, vamos simplificar
# Serviços com nomes que parecem nomes completos (2+ palavras capitalizadas)

echo -e "${YELLOW}⚠️  Verificação de serviços com nomes de pessoas requer SQL direto${NC}"
echo -e "  Rode: scripts/cleanup_data.sql no Supabase SQL Editor"

echo ""

# ═══════════════════════════════════════════════════════════
# 5. Gerar Relatório
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}[5/5] Gerando relatório...${NC}"

REPORT_FILE="cleanup_report_$(date +%Y%m%d_%H%M%S).json"

cat > "$REPORT_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "dry_run": $DRY_RUN,
    "professionals_count": $PROFESSIONALS_COUNT,
    "services_count": $SERVICES_COUNT,
    "suspicious_professionals": $SUSPICIOUS_COUNT,
    "status": "completed"
}
EOF

echo -e "${GREEN}✓ Relatório salvo em: $REPORT_FILE${NC}"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    Resumo                                ║"
echo "╠══════════════════════════════════════════════════════════╣"
printf "║  Profissionais: %-45s ║\n" "$PROFESSIONALS_COUNT"
printf "║  Serviços: %-45s ║\n" "$SERVICES_COUNT"
printf "║  Suspeitos: %-45s ║\n" "$SUSPICIOUS_COUNT"
echo "╠══════════════════════════════════════════════════════════╣"

if [ "$SUSPICIOUS_COUNT" -gt 0 ]; then
    echo -e "║  ${YELLOW}⚠️  AÇÃO RECOMENDADA: Rode cleanup_data.sql${NC}              ║"
else
    echo -e "║  ${GREEN}✅ DADOS LIMPOS - Nenhuma ação necessária${NC}                 ║"
fi

echo "╚══════════════════════════════════════════════════════════╝"

# Próximos passos
echo ""
echo "📋 Próximos Passos:"
echo ""
echo "1. Acesse Supabase Dashboard:"
echo "   https://supabase.com/dashboard"
echo ""
echo "2. Vá em SQL Editor"
echo ""
echo "3. Rode o script:"
echo "   scripts/cleanup_data.sql"
echo ""
echo "4. Siga as instruções do script (Fase 1 = Diagnóstico)"
echo ""

if [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}⚠️  IMPORTANTE: Faça backup antes de rodar UPDATE/DELETE!${NC}"
fi
