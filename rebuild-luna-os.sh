#!/bin/bash
# LUNA OS v2.0 - Reconstrução Completa
# Execute este script para recriar tudo do zero

set -e

echo "=========================================="
echo "🌙 LUNA OS v2.0 - Reconstrução Completa"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== FASE 1: Limpando containers antigos ===${NC}"
docker stop luna-frontend luna-backend 2>/dev/null || true
docker rm luna-frontend luna-backend 2>/dev/null || true
echo "✅ Containers LUNA removidos"
echo ""

echo -e "${GREEN}=== FASE 2: Criando estrutura de diretórios ===${NC}"
BASE_DIR="/Users/franciscotaveira.ads/LUNA OS"
mkdir -p "$BASE_DIR"/{backend/app/{api,core,analytics,campaigns,integrations,knowledge/data},frontend/{app,components,lib}}
echo "✅ Diretórios criados em: $BASE_DIR"
echo ""

echo -e "${GREEN}=== FASE 3: Criando arquivos de configuração ===${NC}"

# .env
cat > "$BASE_DIR/.env" << 'EOF'
# LUNA CORE v2.0 - Environment Variables
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
EVOLUTION_API_URL=http://command-tower-evo-api:8080
EVOLUTION_API_KEY=mothership_master_2026
EVOLUTION_INSTANCE=haven
ANTHROPIC_API_KEY=your-anthropic-key
APP_DEBUG=true
NEXT_PUBLIC_API_URL=http://luna-backend:8000
EOF
echo "✅ .env criado"

# docker-compose.yml
cat > "$BASE_DIR/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  luna-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: luna-backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - EVOLUTION_API_URL=${EVOLUTION_API_URL}
      - EVOLUTION_API_KEY=${EVOLUTION_API_KEY}
      - EVOLUTION_INSTANCE=${EVOLUTION_INSTANCE}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./backend:/app
    networks:
      - luna-network
      - evolution-net
    depends_on:
      - command-tower-evo-api
    restart: unless-stopped

  luna-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: luna-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - luna-network
    depends_on:
      - luna-backend
    restart: unless-stopped

networks:
  luna-network:
    driver: bridge
  evolution-net:
    external: true
EOF
echo "✅ docker-compose.yml criado"
echo ""

echo -e "${GREEN}=== FASE 4: Subindo LUNA OS ===${NC}"
cd "$BASE_DIR"
docker-compose up -d --build
echo ""

echo -e "${GREEN}=== FASE 5: Aguardando serviços ===${NC}"
echo "Aguardando 15 segundos para os serviços inicializarem..."
sleep 15
echo ""

echo -e "${GREEN}=== FASE 6: Verificando status ===${NC}"
docker ps --filter "name=luna" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo -e "${GREEN}=== FASE 7: Testando endpoints ===${NC}"
echo "Backend health:"
curl -s http://localhost:8000/health | python3 -m json.tool || echo "⚠️ Backend ainda inicializando"
echo ""
echo "Frontend:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3000 || echo "⚠️ Frontend ainda inicializando"
echo ""

echo -e "${YELLOW}=== PRÓXIMOS PASSOS ===${NC}"
echo ""
echo "1. Acesse o Evolution Manager:"
echo "   http://localhost:8081/manager"
echo "   API Key: mothership_master_2026"
echo ""
echo "2. Crie a instância 'haven':"
echo "   - Instances → Create Instance"
echo "   - Name: haven"
echo "   - Webhook URL: http://luna-backend:8000/api/webhooks/evolution"
echo "   - Events: messages.upsert"
echo ""
echo "3. Conecte o WhatsApp:"
echo "   - Clique em 'Connect' na instância haven"
echo "   - Escaneie o QR Code com seu WhatsApp"
echo ""
echo "4. Acesse o Dashboard LUNA:"
echo "   http://localhost:3000"
echo ""
echo -e "${GREEN}✅ Reconstrução concluída!${NC}"
