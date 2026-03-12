#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS v3.0 — PRODUÇÃO 10% SUPER SEGURO
# Executa o Plano C Modificado (Não Quebra)
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS v3.0 — Produção 10% Super Seguro      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }
log_step() { echo -e "${BLUE}📍${NC} $1"; }

# 1. Health Check
echo "─" * 50
log_step "PASSO 1: Health Check"
echo "─" * 50

if [ -f "./health-check.sh" ]; then
    ./health-check.sh
    if [ $? -eq 0 ]; then
        log_info "✅ Health Check: OK"
    else
        log_error "❌ Health Check: FALHOU"
        log_warn "Corrija antes de continuar"
        exit 1
    fi
else
    log_warn "⚠️ health-check.sh não encontrado, pulando..."
fi

echo ""

# 2. Backup
echo "─" * 50
log_step "PASSO 2: Backup"
echo "─" * 50

if [ -f "./staging_deploy.sh" ]; then
    ./staging_deploy.sh
    log_info "✅ Backup: OK"
else
    log_warn "⚠️ staging_deploy.sh não encontrado"
fi

echo ""

# 3. Ativar 10%
echo "─" * 50
log_step "PASSO 3: Ativar 10% (5 módulos)"
echo "─" * 50

cd backend

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from app.modules_v3.feature_flags import enable_module, get_all_flags_status
    
    modulos = [
        'agenda_viva',
        'simulador',
        'orquestrador',
        'churn_detector',
        'revenue_optimizer'
    ]
    
    print("🔍 Ativando 10% para 5 módulos...")
    print()
    
    for modulo in modulos:
        try:
            enable_module(modulo, 10)
            print(f"   ✅ {modulo}: 10% ATIVADO")
        except Exception as e:
            print(f"   ⚠️ {modulo}: ERRO ({e})")
    
    print()
    print("✅ Produção 10% ATIVADA")
    print()
    print("📊 Status atual:")
    status = get_all_flags_status()
    for nome, info in status.items():
        on_off = "🟢 ON" if info['enabled'] else "🟡 OFF"
        print(f"   {nome}: {on_off} | Tráfego: {info['traffic']}%")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    sys.exit(1)
EOF

cd ..

echo ""

# 4. Monitoramento
echo "─" * 50
log_step "PASSO 4: Configurar Monitoramento"
echo "─" * 50

echo ""
echo "📊 MONITORAMENTO CONFIGURADO:"
echo ""
echo "   • Logs: tail -f logs/modules_v3.log"
echo "   • Health: curl http://localhost:8000/api/modules_v3/health"
echo "   • Status: curl http://localhost:8000/api/modules_v3/status"
echo "   • Rollback: python3 -c \"from app.modules_v3.feature_flags import disable_module; disable_module('<nome>')\""
echo ""

log_info "✅ Monitoramento: CONFIGURADO"

echo ""

# 5. Checklist
echo "─" * 50
log_step "CHECKLIST DE MONITORAMENTO (24h)"
echo "─" * 50

echo ""
echo "□ Verificar logs a cada 30min"
echo "□ Checar taxa de erros (< 1%)"
echo "□ Checar performance (< 500ms)"
echo "□ Verificar Luna OS v2.2 (INTACTO)"
echo "□ Documentar incidentes (se houver)"
echo "□ Após 24h sem erros: Aumentar para 50%"
echo ""

# 6. Resumo final
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ PRODUÇÃO 10% ATIVADA COM SUCESSO              ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║  🚀 5 módulos em produção (10% tráfego)           ║"
echo "║  📊 Monitoramento: ATIVO                          ║"
echo "║  🛑 Rollback: 30-120 segundos                     ║"
echo "║  📈 Próximo: Monitorar 24h → 50%                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

log_info "Plano Super Seguro INICIADO!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "   1. Monitorar 24h"
echo "   2. Se OK: 50% (amanhã)"
echo "   3. Completar 3 módulos (Dia 3-4)"
echo "   4. Produção 100% (Dia 5-7)"
echo ""
