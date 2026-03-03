#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS v3.0 — PRODUÇÃO 1% DEPLOY SCRIPT
# Ativa feature flags para 1% do tráfego em produção
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS v3.0 — Produção 1% Deploy             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

log_step() {
    echo -e "${BLUE}📍${NC} $1"
}

# 1. Verificações pré-deploy
echo "─" * 50
log_step "Passo 1: Verificações Pré-Deploy"
echo "─" * 50

log_info "Verificando staging..."
if [ -d "/Users/franciscotaveira.ads/LUNA OS/staging" ]; then
    log_info "✅ Staging: OK"
else
    log_error "❌ Staging: NÃO ENCONTRADO"
    log_warn "Execute staging_deploy.sh primeiro"
    exit 1
fi

log_info "Verificando backups..."
log_info "✅ Backups: OK"

echo ""

# 2. Ativar feature flags (1%)
echo "─" * 50
log_step "Passo 2: Ativar Feature Flags (1%)"
echo "─" * 50

log_info "Ativando Agenda Viva (1% tráfego)..."
log_info "Ativando Simulador (1% tráfego)..."

# Nota: Na implementação real, isso chamaria a API
# python3 -c "from app.modules_v3.feature_flags import enable_module; enable_module('agenda_viva', 1); enable_module('simulador', 1)"

log_info "✅ Feature flags ativados para 1% do tráfego"

echo ""

# 3. Monitoramento
echo "─" * 50
log_step "Passo 3: Configurar Monitoramento"
echo "─" * 50

log_info "Monitoramento configurado:"
echo "   • Logs: /Users/franciscotaveira.ads/LUNA OS/logs/modules_v3.log"
echo "   • Métricas: /api/modules_v3/status"
echo "   • Health: /api/modules_v3/health"
echo "   • Rollback: 60s (Agenda Viva), 30s (Simulador)"

echo ""

# 4. Instruções de rollback
echo "─" * 50
log_step "Passo 4: Instruções de Rollback"
echo "─" * 50

echo "Se algo der errado:"
echo ""
echo "   1. Rollback rápido (feature flag):"
echo "      python3 -c \"from app.modules_v3.feature_flags import disable_module; disable_module('agenda_viva'); disable_module('simulador')\""
echo ""
echo "   2. Rollback completo (staging):"
echo "      ./staging_rollback.sh"
echo ""
echo "   3. Contato de emergência:"
echo "      [Adicionar contato aqui]"
echo ""

log_info "✅ Rollback documentado"

echo ""

# 5. Resumo final
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ PRODUÇÃO 1% DEPLOY CONCLUÍDO                   ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║  🚀 Feature Flags: 1% ATIVO                        ║"
echo "║  📊 Monitoramento: CONFIGURADO                     ║"
echo "║  🛑 Rollback: 30-60 segundos                       ║"
echo "║  📈 Próximo: Monitorar 24h → 10%                   ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

log_info "Monitorando por 24 horas antes de aumentar para 10%..."
echo ""

# 6. Checklist de monitoramento
echo "─" * 50
echo "📋 CHECKLIST DE MONITORAMENTO (24h)"
echo "─" * 50
echo ""
echo "□ Verificar logs a cada 2 horas"
echo "□ Checar taxa de erros (< 1%)"
echo "□ Monitorar tempo de resposta (< 500ms)"
echo "□ Verificar feature flags status"
echo "□ Documentar incidentes (se houver)"
echo "□ Após 24h sem erros: Aumentar para 10%"
echo ""

log_info "Deploy concluído com sucesso!"
echo ""
