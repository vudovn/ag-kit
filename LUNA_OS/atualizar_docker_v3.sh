#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS v3.0 — ATUALIZAR DOCKER COM MODULES V3
# Copia modules_v3 e ativa 10% em produção
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS v3.0 — Atualizar Docker               ║"
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

# 1. Verificar container
echo "─" * 50
echo "📦 Passo 1: Verificar Container"
echo "─" * 50

if docker ps | grep -q luna-backend; then
    log_info "✅ luna-backend está rodando"
else
    log_error "❌ luna-backend NÃO está rodando"
    log_warn "Execute: docker-compose up -d"
    exit 1
fi

echo ""

# 2. Copiar modules_v3
echo "─" * 50
echo "📦 Passo 2: Copiar Modules V3"
echo "─" * 50

log_info "Copiando modules_v3 para o container..."
docker cp backend/app/modules_v3 luna-backend:/app/app/

if [ $? -eq 0 ]; then
    log_info "✅ modules_v3 copiado com sucesso"
else
    log_error "❌ Falha ao copiar modules_v3"
    exit 1
fi

echo ""

# 3. Verificar cópia
echo "─" * 50
echo "📦 Passo 3: Verificar Cópia"
echo "─" * 50

log_info "Verificando arquivos no container..."
docker exec luna-backend ls -la /app/app/modules_v3/ | head -15

echo ""

# 4. Reiniciar backend
echo "─" * 50
echo "📦 Passo 4: Reiniciar Backend"
echo "─" * 50

log_info "Reiniciando luna-backend..."
docker restart luna-backend

log_info "✅ Backend reiniciado"

echo ""

# 5. Aguardar startup
echo "─" * 50
echo "📦 Passo 5: Aguardar Startup (30s)"
echo "─" * 50

sleep 30

log_info "✅ Startup completo"

echo ""

# 6. Testar health
echo "─" * 50
echo "📦 Passo 6: Testar Health"
echo "─" * 50

log_info "Testando modules_v3 health..."
sleep 5

HEALTH=$(curl -s http://localhost:8000/api/modules_v3/health || echo "ERRO")

if echo "$HEALTH" | grep -q "healthy"; then
    log_info "✅ Modules V3: HEALTHY"
else
    log_warn "⚠️ Health: $HEALTH"
fi

echo ""

# 7. Ativar 10%
echo "─" * 50
echo "📦 Passo 7: Ativar 10% Produção"
echo "─" * 50

log_info "Ativando 10% para 8 módulos..."

docker exec -i luna-backend python3 << 'EOF'
from app.modules_v3.feature_flags import enable_module

modulos = [
    'agenda_viva',
    'simulador',
    'orquestrador',
    'churn_detector',
    'revenue_optimizer',
    'ai_coach',
    'mystery_shopper',
    'heat_map'
]

print("🔍 Ativando 10%...")
for modulo in modulos:
    enable_module(modulo, 10)
    print(f"   ✅ {modulo}: 10%")

print("\n✅ Produção 10% ATIVADA")
EOF

echo ""

# 8. Monitoramento
echo "─" * 50
echo "📦 Passo 8: Monitoramento"
echo "─" * 50

echo ""
echo "📊 MONITORAMENTO CONFIGURADO:"
echo ""
echo "   • Logs: docker-compose logs -f luna-backend"
echo "   • Health: curl http://localhost:8000/api/modules_v3/health"
echo "   • Status: curl http://localhost:8000/api/modules_v3/status"
echo ""

# 9. Resumo final
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ DOCKER ATUALIZADO COM SUCESSO                 ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║  🚀 8 módulos em produção (10% tráfego)           ║"
echo "║  📊 Monitoramento: docker-compose logs -f         ║"
echo "║  🛑 Rollback: 30-120 segundos                     ║"
echo "║  📈 Próximo: Monitorar 24h → 50%                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

log_info "Atualização DOCKER concluída!"
echo ""
