#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS v3.0 — STAGING DEPLOY SCRIPT
# Deploy seguro dos módulos v3 em staging
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS v3.0 — Staging Deploy                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Configurações
STAGING_DIR="/Users/franciscotaveira.ads/LUNA OS/staging"
BACKUP_DIR="/Users/franciscotaveira.ads/LUNA OS/backups"
MODULES_DIR="/Users/franciscotaveira.ads/LUNA OS/backend/app/modules_v3"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funções
log_info() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

# 1. Backup
echo "─" * 50
echo "📦 Passo 1: Backup"
echo "─" * 50

if [ -d "$STAGING_DIR" ]; then
    log_info "Criando backup do staging..."
    cp -r "$STAGING_DIR" "$BACKUP_DIR/staging_backup_$(date +%Y%m%d_%H%M%S)"
    log_info "Backup criado com sucesso"
else
    log_warn "Staging não existe, criando..."
    mkdir -p "$STAGING_DIR"
fi

echo ""

# 2. Copiar módulos v3
echo "─" * 50
echo "📦 Passo 2: Copiar Módulos v3"
echo "─" * 50

log_info "Copiando módulos para staging..."
cp -r "$MODULES_DIR" "$STAGING_DIR/"

log_info "Módulos copiados:"
echo "   • feature_flags.py"
echo "   • integration_endpoint.py"
echo "   • agenda_viva/"
echo "   • simulador/"
echo "   • [outros módulos]"

echo ""

# 3. Verificar dependências
echo "─" * 50
echo "📦 Passo 3: Verificar Dependências"
echo "─" * 50

log_info "Verificando Python..."
python3 --version

log_info "Verificando pacotes..."
pip3 list | grep -E "(fastapi|pydantic|loguru|httpx)" || log_warn "Alguns pacotes podem estar faltando"

echo ""

# 4. Testes em staging
echo "─" * 50
echo "📦 Passo 4: Testes em Staging"
echo "─" * 50

log_info "Rodando testes de integração..."
cd "$STAGING_DIR/modules_v3" || exit 1

if python3 test_integration_simples.py; then
    log_info "✅ Testes em staging: PASSARAM"
else
    log_error "❌ Testes em staging: FALHARAM"
    exit 1
fi

echo ""

# 5. Health check
echo "─" * 50
echo "📦 Passo 5: Health Check"
echo "─" * 50

log_info "Verificando saúde dos módulos..."

# Verificar se arquivos existem
if [ -f "$STAGING_DIR/modules_v3/feature_flags.py" ]; then
    log_info "✅ feature_flags.py: OK"
else
    log_error "❌ feature_flags.py: FALTANDO"
    exit 1
fi

if [ -f "$STAGING_DIR/modules_v3/integration_endpoint.py" ]; then
    log_info "✅ integration_endpoint.py: OK"
else
    log_error "❌ integration_endpoint.py: FALTANDO"
    exit 1
fi

if [ -d "$STAGING_DIR/modules_v3/agenda_viva" ]; then
    log_info "✅ agenda_viva/: OK"
else
    log_error "❌ agenda_viva/: FALTANDO"
    exit 1
fi

if [ -d "$STAGING_DIR/modules_v3/simulador" ]; then
    log_info "✅ simulador/: OK"
else
    log_error "❌ simulador/: FALTANDO"
    exit 1
fi

echo ""

# 6. Resumo
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ STAGING DEPLOY CONCLUÍDO                       ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║  📂 Staging: $STAGING_DIR                          ║"
echo "║  📂 Backup:  $BACKUP_DIR                           ║"
echo "║  ✅ Testes:  PASSARAM                              ║"
echo "║  🚀 Pronto para: Produção 1%                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

log_info "Próximo passo: Ativar feature flag 1% em produção"
echo ""
