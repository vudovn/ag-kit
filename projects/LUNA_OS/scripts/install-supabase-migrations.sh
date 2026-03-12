#!/bin/bash
# ============================================================
# LUNA OS — Multi-Brain V2 Supabase Migration Installer
# ============================================================
# Este script aplica as migrations no Supabase automaticamente
# Uso: ./scripts/install-supabase-migrations.sh
# ============================================================

set -e

echo "🌙 LUNA OS — Multi-Brain V2 Migration Installer"
echo "==============================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretórios
LUNA_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATION_FILE="$LUNA_OS_DIR/database/migrations/001_multi_brain_v2.sql"

echo "📁 Migration file: $MIGRATION_FILE"
echo ""

# Verificar se arquivo existe
if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}❌ Migration file não encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Migration file encontrado${NC}"
echo ""

# Instruções
echo "==============================================="
echo "📋 COMO APLICAR NO SUPABASE"
echo "==============================================="
echo ""
echo "Opção 1: Supabase Dashboard (Recomendado)"
echo "-----------------------------------------"
echo "1. Acesse: https://supabase.com/dashboard"
echo "2. Selecione seu projeto LUNA OS"
echo "3. Vá em: SQL Editor → New Query"
echo "4. Copie o conteúdo de:"
echo "   $MIGRATION_FILE"
echo "5. Cole no SQL Editor"
echo "6. Clique em 'Run' ou Ctrl+Enter"
echo "7. Verifique:"
echo "   SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
echo ""
echo "Opção 2: psql (Command Line)"
echo "-----------------------------"
echo "psql \"postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres\" \\"
echo "  -f $MIGRATION_FILE"
echo ""
echo "Opção 3: Supabase CLI"
echo "---------------------"
echo "supabase db push $MIGRATION_FILE"
echo ""

# Perguntar se quer abrir Supabase
read -p "Quer abrir Supabase Dashboard agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    # Abrir no navegador (funciona em Mac, Linux, Windows)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "https://supabase.com/dashboard"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "https://supabase.com/dashboard" 2>/dev/null || echo "Abra manualmente: https://supabase.com/dashboard"
    else
        echo "Abra manualmente: https://supabase.com/dashboard"
    fi
fi

echo ""
echo "==============================================="
echo "✅ VERIFICAÇÃO PÓS-MIGRATION"
echo "==============================================="
echo ""
echo "Após aplicar, execute no SQL Editor:"
echo ""
echo "-- Verificar tabelas criadas:"
echo "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
echo ""
echo "-- Verificar feature flags:"
echo "SELECT * FROM feature_flags;"
echo ""
echo "-- Verificar views:"
echo "SELECT viewname FROM pg_views WHERE schemaname = 'public';"
echo ""

echo "==============================================="
echo "📊 TABELAS ESPERADAS (10)"
echo "==============================================="
echo ""
echo "1. cache_entries (Smart Caching)"
echo "2. handoff_requests (Human Handoff)"
echo "3. memory_chain (Audit Trail)"
echo "4. behavioral_dna (Personalização)"
echo "5. brain_decisions (Multi-Brain Router)"
echo "6. analytics_events (Analytics)"
echo "7. feature_flags (Feature Flags)"
echo "8. daily_metrics (View)"
echo "9. cache_performance (View)"
echo "10. handoff_metrics (View)"
echo ""

echo "==============================================="
echo "🎉 INSTALAÇÃO CONCLUÍDA!"
echo "==============================================="
echo ""
echo "Próximos passos:"
echo "1. Aplicar migration no Supabase (veja instruções acima)"
echo "2. Verificar tabelas criadas"
echo "3. Testar integração: python3 backend/app/core/multi_brain_integration.py"
echo ""
echo -e "${GREEN}✅ Script concluído!${NC}"
