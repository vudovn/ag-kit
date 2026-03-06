#!/bin/bash
# ═══════════════════════════════════════════════
# LUNA OS v3.0 - Execute All Migrations
# ═══════════════════════════════════════════════
# Uso: ./run_migrations.sh [SUPABASE_DB_URL]
# ═══════════════════════════════════════════════

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}" >&2; }

# Verificar se psql está instalado
if ! command -v psql &> /dev/null; then
    log_error "psql não encontrado. Instale PostgreSQL client primeiro."
    exit 1
fi

# Obter URL do banco
if [ -n "${1:-}" ]; then
    DB_URL="$1"
elif [ -n "${SUPABASE_DB_URL:-}" ]; then
    DB_URL="$SUPABASE_DB_URL"
elif [ -f "../.env" ]; then
    source ../.env
    DB_URL="${SUPABASE_DB_URL:-}"
fi

if [ -z "$DB_URL" ]; then
    log_error "SUPABASE_DB_URL não configurado"
    echo ""
    echo "Uso:"
    echo "  1. Exporte a variável: export SUPABASE_DB_URL='postgresql://...'"
    echo "  2. Ou passe como argumento: $0 'postgresql://...'"
    echo "  3. Ou configure no .env: SUPABASE_DB_URL=..."
    exit 1
fi

log_info "🗄️  LUNA OS v3.0 - Migrations"
log_info "================================"
log_info "Banco: ${DB_URL:0:30}..."
echo ""

# Testar conexão
log_info "Testando conexão..."
if ! psql "$DB_URL" -c "SELECT 1" &>/dev/null; then
    log_error "Falha ao conectar. Verifique a URL e permissões."
    exit 1
fi
log_success "Conexão estabelecida"
echo ""

# Executar migrations em ordem
MIGRATIONS_DIR="$(dirname "$0")"
TOTAL=0
SUCCESS=0
FAILED=0

for migration in "$MIGRATIONS_DIR"/0*.sql; do
    if [ ! -f "$migration" ]; then
        continue
    fi
    
    filename=$(basename "$migration")
    TOTAL=$((TOTAL + 1))
    
    log_info "Executando: $filename..."
    
    if psql "$DB_URL" -f "$migration" &>/dev/null; then
        log_success "  ✓ $filename completado"
        SUCCESS=$((SUCCESS + 1))
    else
        log_error "  ✗ $filename falhou"
        FAILED=$((FAILED + 1))
        
        # Continuar com próxima migration (não crítica)
        log_warning "  Continuando para próxima..."
    fi
done

echo ""
log_info "================================"
log_info "Resumo:"
log_success "  Total: $TOTAL"
log_success "  Sucesso: $SUCCESS"

if [ $FAILED -gt 0 ]; then
    log_warning "  Falhas: $FAILED"
    echo ""
    log_warning "Algumas migrations falharam. Verifique os erros acima."
    exit 1
else
    log_success "  Todas as migrations executadas com sucesso!"
fi

# Validação pós-migration
echo ""
log_info "Validando migrations..."

# Contar tabelas
TABLE_COUNT=$(psql "$DB_URL" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
log_success "  Tabelas criadas: $TABLE_COUNT"

# Verificar RLS
RLS_COUNT=$(psql "$DB_URL" -t -c "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = true;" | tr -d ' ')
log_success "  Tabelas com RLS: $RLS_COUNT"

# Verificar seed data
SETTINGS_COUNT=$(psql "$DB_URL" -t -c "SELECT COUNT(*) FROM system_settings;" | tr -d ' ')
log_success "  Settings: $SETTINGS_COUNT"

KNOWLEDGE_COUNT=$(psql "$DB_URL" -t -c "SELECT COUNT(*) FROM knowledge_base;" | tr -d ' ')
log_success "  Knowledge items: $KNOWLEDGE_COUNT"

echo ""
log_success "✅ Migrations validadas com sucesso!"
echo ""
log_info "Próximos passos:"
log_info "  1. Crie buckets no Storage: models, conversations, exports"
log_info "  2. Valide no Supabase Dashboard"
log_info "  3. Teste a aplicação"
