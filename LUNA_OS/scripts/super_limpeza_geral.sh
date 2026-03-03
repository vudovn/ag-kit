#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙🔧 LUNA OS v3.0 — SUPER LIMPEZA GERAL
# Roda auditoria + limpeza + validação
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙🔧 LUNA OS v3.0 — SUPER LIMPEZA GERAL          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

cd backend

# 1. Auditoria
echo "─" * 50
log_info "PASSO 1: AUDITORIA DE BANCO DE DADOS"
echo "─" * 50

python3 app/scripts/auditoria_banco_dados.py

if [ $? -eq 0 ]; then
    log_info "✅ Auditoria CONCLUÍDA"
else
    log_error "❌ Auditoria FALHOU"
    exit 1
fi

echo ""

# 2. Limpeza
echo "─" * 50
log_info "PASSO 2: LIMPEZA DE BANCO DE DADOS"
echo "─" * 50

python3 app/scripts/limpeza_banco_dados.py

if [ $? -eq 0 ]; then
    log_info "✅ Limpeza CONCLUÍDA"
else
    log_error "❌ Limpeza FALHOU"
    exit 1
fi

echo ""

# 3. Dojo de Histórico Real
echo "─" * 50
log_info "PASSO 3: DOJO DE HISTÓRICO REAL"
echo "─" * 50

python3 app/scripts/dojo_historico_real.py

if [ $? -eq 0 ]; then
    log_info "✅ Dojo CONCLUÍDO"
else
    log_warn "⚠️ Dojo FALHOU (pode ser normal se sem dados)"
fi

echo ""

# 4. Doce das Contas
echo "─" * 50
log_info "PASSO 4: DOCE DAS CONTAS"
echo "─" * 50

python3 app/scripts/doce_das_contas.py

if [ $? -eq 0 ]; then
    log_info "✅ Doce das Contas CONCLUÍDO"
else
    log_warn "⚠️ Doce das Contas FALHOU (pode ser normal se sem dados)"
fi

echo ""

# 5. Resumo final
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ SUPER LIMPEZA GERAL CONCLUÍDA                  ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║  📊 Relatórios em: logs/                           ║"
echo "║  🔧 Auditoria: auditoria_banco_dados_relatorio.json║"
echo "║  🧹 Limpeza: limpeza_banco_dados_relatorio.json    ║"
echo "║  🥋 Dojo: dojo_historico_real_relatorio.json       ║"
echo "║  💰 Doce: doce_das_contas_relatorio.json           ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

log_info "SUPER LIMPEZA CONCLUÍDA!"
echo ""
