#!/bin/bash
# ================================
# LUNA OS v3.0 — Script de Deploy
# Contorna bloqueio TCC do Docker Desktop no Mac
# ================================

set -e

COMPOSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_BASE="$COMPOSE_DIR/docker-compose.yml"
COMPOSE_EXT="$COMPOSE_DIR/docker-compose.extended.yml"

echo "🌙 LUNA OS v3.0 — Deploy Iniciado"
echo "=================================="

# Tentar carregar variáveis — em ordem de prioridade:
# 1. .env real (se acessível)
# 2. .env.example (como fallback de template)
ENV_LOADED=false

if source "$COMPOSE_DIR/.env" 2>/dev/null; then
  echo "📦 Variáveis carregadas de .env"
  ENV_LOADED=true
elif source "$COMPOSE_DIR/.env.example" 2>/dev/null; then
  echo "⚠️  Usando .env.example como fallback (configure .env com valores reais!)"
  ENV_LOADED=true
fi

set -a
[ "$ENV_LOADED" = true ] || echo "⚠️  Nenhum arquivo env encontrado, usando defaults do compose"
set +a

ACTION="${1:-up}"

case "$ACTION" in
  up)
    echo "🚀 Subindo stack completa (base + v3.0)..."
    docker-compose \
      -f "$COMPOSE_BASE" \
      -f "$COMPOSE_EXT" \
      up -d --build --remove-orphans
    ;;
  up-base)
    echo "🚀 Subindo apenas stack base..."
    docker-compose -f "$COMPOSE_BASE" up -d --build
    ;;
  down)
    echo "🛑 Parando stack completa..."
    docker-compose \
      -f "$COMPOSE_BASE" \
      -f "$COMPOSE_EXT" \
      down
    ;;
  restart)
    echo "🔄 Reiniciando..."
    docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" down
    docker-compose -f "$COMPOSE_BASE" -f "$COMPOSE_EXT" up -d --build
    ;;
  status)
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    exit 0
    ;;
  logs)
    SERVICE="${2:-luna-backend}"
    docker logs -f "$SERVICE" --tail=100
    exit 0
    ;;
  *)
    echo "Uso: ./up.sh [up|up-base|down|restart|status|logs <service>]"
    exit 1
    ;;
esac

echo ""
echo "✅ Concluído!"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "🔗 Endpoints:"
echo "  Backend:   http://localhost:8000/health"
echo "  Frontend:  http://localhost:3000"
echo "  Jaeger:    http://localhost:16686"
echo "  Grafana:   http://localhost:3001"
echo "  Prometheus:http://localhost:9090"
