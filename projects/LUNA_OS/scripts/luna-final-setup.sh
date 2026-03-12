#!/bin/bash
# ============================================================
# LUNA OS — Setup Final para Produção
# ============================================================
# Este script configura o LUNA OS para produção
# Executar: ./scripts/luna-final-setup.sh
# ============================================================

set -e

echo "🌙 LUNA OS — Setup Final para Produção"
echo "========================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretórios
LUNA_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANTIGRAVITY_DIR="$(dirname "$LUNA_OS_DIR")"

echo "📁 LUNA OS: $LUNA_OS_DIR"
echo "📁 Antigravity: $ANTIGRAVITY_DIR"
echo ""

# ============================================================
# 1. Verificar .env
# ============================================================
echo "1️⃣  Verificando .env..."

if [ ! -f "$LUNA_OS_DIR/.env" ]; then
    echo -e "${RED}❌ .env não encontrado${NC}"
    echo "Copie .env.example para .env e configure:"
    echo "  cp .env.example .env"
    exit 1
fi

echo -e "${GREEN}✅ .env encontrado${NC}"
echo ""

# ============================================================
# 2. Verificar Belasis API
# ============================================================
echo "2️⃣  Verificando configuração do Belasis..."

BELASIS_MOCK=$(grep "^BELASIS_MOCK=" "$LUNA_OS_DIR/.env" | cut -d'=' -f2)
BELASIS_API_KEY=$(grep "^BELASIS_API_KEY=" "$LUNA_OS_DIR/.env" | cut -d'=' -f2)

if [ "$BELASIS_MOCK" == "true" ]; then
    echo -e "${YELLOW}⚠️  BELASIS_MOCK=true (dados fictícios)${NC}"
    echo ""
    echo "Para produção, obtenha API Key em: https://belasis.com.br"
    echo "Depois edite .env:"
    echo "  BELASIS_MOCK=false"
    echo "  BELASIS_API_KEY=bpk_SEU_TOKEN_AQUI"
    echo ""
    read -p "Quer configurar Belasis agora? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Belasis API Key: " BELASIS_KEY
        sed -i.bak "s/BELASIS_MOCK=true/BELASIS_MOCK=false/" "$LUNA_OS_DIR/.env"
        sed -i.bak "s/BELASIS_API_KEY=.*/BELASIS_API_KEY=$BELASIS_KEY/" "$LUNA_OS_DIR/.env"
        echo -e "${GREEN}✅ Belasis configurado${NC}"
    fi
else
    echo -e "${GREEN}✅ BELASIS_MOCK=false (dados reais)${NC}"
fi

echo ""

# ============================================================
# 3. Aplicar Migrations no Supabase
# ============================================================
echo "3️⃣  Aplicar migrations no Supabase..."
echo ""
echo "Acesse: https://supabase.com/dashboard"
echo "Vá em: SQL Editor → New Query"
echo "Execute: $ANTIGRAVITY_DIR/database/migrations/002_supabase_complete.sql"
echo ""
read -p "Migrations aplicadas? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${GREEN}✅ Migrations aplicadas${NC}"
else
    echo -e "${YELLOW}⚠️  Migrations pendentes${NC}"
fi

echo ""

# ============================================================
# 4. Testar Backend
# ============================================================
echo "4️⃣  Testar backend..."
echo ""
cd "$LUNA_OS_DIR/backend"

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "Iniciando backend em modo teste..."
python3 -c "
import sys
sys.path.insert(0, '$ANTIGRAVITY_DIR')

# Testar imports do Multi-Brain V2
try:
    from brain.cache import contact_cache
    from brain.handoff import check_handoff
    from brain.behavioral_dna import get_customer_dna
    from brain.memory_chain import MemoryChain
    print('✅ Multi-Brain V2 imports OK')
except Exception as e:
    print(f'❌ Erro nos imports: {e}')
    sys.exit(1)

# Testar Memory Chain
chain = MemoryChain()
entry = chain.add_interaction({'test': 'luna_os_integration'})
print(f'✅ Memory Chain hash: {entry.current_hash[:32]}...')

print('✅ Backend teste OK')
"

echo ""

# ============================================================
# 5. Resumo
# ============================================================
echo "========================================"
echo "📊 RESUMO DO SETUP"
echo "========================================"
echo ""

if [ "$BELASIS_MOCK" == "false" ]; then
    echo -e "${GREEN}✅ Belasis: Produção (dados reais)${NC}"
else
    echo -e "${YELLOW}⚠️  Belasis: Mock (dados fictícios)${NC}"
fi

echo ""
echo "📁 Próximos passos:"
echo ""
echo "1. Se Belasis Mock=true, obtenha API Key em https://belasis.com.br"
echo "2. Aplique migrations no Supabase (SQL Editor)"
echo "3. Inicie backend: cd backend && python -m uvicorn app.main:app --reload"
echo "4. Inicie frontend: cd frontend && npm run dev"
echo ""
echo -e "${GREEN}✅ Setup concluído!${NC}"
