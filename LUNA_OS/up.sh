#!/bin/bash
# ================================
# LUNA OS v3.0 — Script de Deploy
# Contorna bloqueio TCC do Docker Desktop no Mac
# 
# DEBT #17: Tratamento de erro robusto com rollback automático
# ================================

# [DEBT #17] Modo estrito: exit on error, undefined vars, pipe failures
set -euo pipefail

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

# Cleanup function for rollback
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deploy falhou com código $exit_code"
        log_info "Iniciando rollback..."
        
        # Tentar rollback se estiver em produção
        if [ "${ENV:-development}" = "production" ]; then
            log_info "Rollback em produção detectada..."
            docker-compose -f "$COMPOSE_BASE" down --remove-orphans 2>/dev/null || true
        fi
        
        log_error "Verifique os logs: docker logs luna-backend --tail=100"
    fi
    exit $exit_code
}

# Set trap for cleanup on error
trap cleanup EXIT ERR

# Get script directory
COMPOSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_BASE="$COMPOSE_DIR/docker-compose.yml"
COMPOSE_EXT="$COMPOSE_DIR/docker-compose.extended.yml"

log_info "🌙 LUNA OS v3.0 — Deploy Iniciado"
log_info "=================================="

# Check Docker is running
if ! docker info &>/dev/null; then
    log_error "Docker não está rodando. Inicie o Docker Desktop e tente novamente."
    exit 1
fi
log_success "Docker detectado"

# Check required files exist
for file in "$COMPOSE_BASE" "$COMPOSE_EXT"; do
    if [ ! -f "$file" ]; then
        log_error "Arquivo não encontrado: $file"
        exit 1
    fi
done
log_success "Arquivos de compose encontrados"

# Tentar carregar variáveis — em ordem de prioridade:
# 1. .env real (se acessível)
# 2. .env.example (como fallback de template)
ENV_LOADED=false

if [ -f "$COMPOSE_DIR/.env" ]; then
    if source "$COMPOSE_DIR/.env" 2>/dev/null; then
        log_success "Variáveis carregadas de .env"
        ENV_LOADED=true
    else
        log_warning "Erro ao carregar .env, tentando .env.example..."
    fi
fi

if [ "$ENV_LOADED" = false ] && [ -f "$COMPOSE_DIR/.env.example" ]; then
    if source "$COMPOSE_DIR/.env.example" 2>/dev/null; then
        log_warning "Usando .env.example como fallback (configure .env com valores reais!)"
        ENV_LOADED=true
    fi
fi

# Export variables for docker-compose
if [ "$ENV_LOADED" = true ]; then
    set -a
    set +a
else
    log_warning "Nenhum arquivo env encontrado, usando defaults do compose"
fi

# Validate critical environment variables (production only)
if [ "${ENV:-development}" = "production" ]; then
    log_info "Validando variáveis críticas para produção..."
    
    required_vars=(
        "SUPABASE_URL"
        "SUPABASE_KEY"
        "OPENROUTER_API_KEY"
        "WEBHOOK_API_KEY"
        "EVO_DB_PASSWORD"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_error "Variáveis críticas faltando em produção: ${missing_vars[*]}"
        exit 1
    fi
    log_success "Variáveis de produção validadas"
fi

ACTION="${1:-up}"

case "$ACTION" in
    up)
        log_info "🚀 Subindo stack completa (base + v3.0)..."
        
        # Pre-flight check
        log_info "Verificando containers existentes..."
        docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" ps || true
        
        # Build and start
        docker-compose \
            -f "$COMPOSE_BASE" \
            -f "$COMPOSE_EXT" \
            up -d --build --remove-orphans
        
        log_success "Stack iniciada com sucesso"
        ;;
        
    up-base)
        log_info "🚀 Subindo apenas stack base..."
        docker-compose -f "$COMPOSE_BASE" up -d --build
        log_success "Stack base iniciada"
        ;;
        
    down)
        log_info "🛑 Parando stack completa..."
        docker-compose \
            -f "$COMPOSE_BASE" \
            -f "$COMPOSE_EXT" \
            down
        log_success "Stack parada"
        ;;
        
    restart)
        log_info "🔄 Reiniciando..."
        docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" down
        docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" up -d --build
        log_success "Reiniciado com sucesso"
        ;;
        
    rebuild)
        log_info "🔨 Reconstruindo imagens..."
        docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" build --no-cache
        log_success "Imagens reconstruídas"
        ;;
        
    status)
        log_info "Status dos containers:"
        echo ""
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        log_info "Health checks:"
        docker inspect --format='{{.Name}}: {{.State.Health.Status}}' $(docker ps -q) 2>/dev/null || echo "Health checks não disponíveis"
        exit 0
        ;;
        
    logs)
        SERVICE="${2:-luna-backend}"
        log_info "Logs de $SERVICE:"
        docker logs -f "$SERVICE" --tail=100
        exit 0
        ;;
        
    prune)
        log_warning "Limpando recursos Docker não utilizados..."
        docker system prune -af --volumes
        log_success "Limpeza concluída"
        ;;
        
    *)
        log_error "Comando desconhecido: $ACTION"
        echo ""
        echo "Uso: ./up.sh [comando] [opções]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  up          - Sobe stack completa (default)"
        echo "  up-base     - Sobe apenas stack base"
        echo "  down        - Para stack completa"
        echo "  restart     - Reinicia stack completa"
        echo "  rebuild     - Reconstrói imagens sem cache"
        echo "  status      - Mostra status dos containers"
        echo "  logs [svc]  - Mostra logs de um serviço"
        echo "  prune       - Limpa recursos Docker não utilizados"
        echo ""
        exit 1
        ;;
esac

# Remove trap on success
trap - EXIT ERR

echo ""
log_success "✅ Concluído!"
echo ""
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
log_info "🔗 Endpoints:"
echo "  Backend:    http://localhost:8000/health"
echo "  Frontend:   http://localhost:3000"
echo "  Jaeger:     http://localhost:16686"
echo "  Grafana:    http://localhost:3001"
echo "  Prometheus: http://localhost:9090"
echo "  Windmill:   http://localhost:8001"
echo "  PgAdmin:    http://localhost:5050"
echo ""
log_info "Dica: Use './up.sh logs <servico>' para ver logs em tempo real"
