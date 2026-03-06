#!/bin/bash
# 🚀 Script de Deploy Otimizado - LUNA OS v3.0
# Com cache Docker e builds paralelos

set -e

echo "🚀 LUNA OS v3.0 - Deploy Otimizado"
echo "=================================="

# Limpeza seletiva (mantém cache de build)
echo "🧹 Limpando containers antigos..."
docker compose down --remove-orphans

# Build paralelo com cache
echo "🏗️  Construindo imagens com cache..."
docker compose build --parallel

# Start
echo "🚀 Subindo serviços..."
docker compose up -d

# Status
echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📊 Status dos containers:"
docker compose ps

echo ""
echo "🔗 Endpoints:"
echo "  Backend:   http://localhost:8000/health"
echo "  Frontend:  http://localhost:3000"
echo "  Grafana:   http://localhost:3001"
echo "  Jaeger:    http://localhost:16686"
echo ""
echo "📈 Logs em tempo real: docker compose logs -f"
