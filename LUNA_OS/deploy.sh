#!/bin/bash

set -e

echo "🌙 Luna v3.0 - Deployment Script"
echo "=================================="

# 1. Build e validação
echo "📦 Construindo containers..."
docker-compose -f docker-compose.yml -f docker-compose.extended.yml build

# 2. Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose -f docker-compose.yml -f docker-compose.extended.yml up -d

# 3. Aguardar inicialização
echo "⏳ Aguardando serviços inicializarem..."
sleep 10

# 4. Testes de conexão
echo "🧪 Testando conexões..."
curl -f http://localhost:8000/health || echo "❌ Backend não respondeu"
curl -f http://localhost:16686 || echo "❌ Jaeger UI não respondeu"
curl -f http://localhost:9090 || echo "❌ Prometheus não respondeu"
curl -f http://localhost:3001 || echo "❌ Grafana não respondeu"

# 5. Setup inicial
echo "⚙️  Configurando banco de dados..."
docker-compose -f docker-compose.extended.yml exec -T postgres psql -U luna_user -d luna -f /docker-entrypoint-initdb.d/schema.sql

# 6. Status final
echo ""
echo "✅ Deployment completo!"
echo ""
echo "📊 Dashboards disponíveis:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - Jaeger Tracing: http://localhost:16686"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3001"
echo "  - PgAdmin: http://localhost:5050"
echo ""