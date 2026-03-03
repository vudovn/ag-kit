#!/bin/bash
# 🌙 LUNA OS - Health Check Script
# Testa todos os endpoints e integrações

set -e

echo "╔════════════════════════════════════════╗"
echo "║  🌙 LUNA OS - Health Check            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

# Functions
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected="$3"

    echo -n "🔍 Testando $name... "

    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [ "$response" == "$expected" ] || [ "$response" == "200" ]; then
        echo -e "${GREEN}✅ OK ($response)${NC}"
        ((PASS++))
    elif [ "$response" == "000" ]; then
        echo -e "${RED}❌ FAIL (sem resposta)${NC}"
        ((FAIL++))
    else
        echo -e "${YELLOW}⚠️  WARN ($response)${NC}"
        ((WARN++))
    fi
}

test_json_endpoint() {
    local name="$1"
    local url="$2"
    local field="$3"

    echo -n "🔍 Testando $name... "

    response=$(curl -s "$url" 2>/dev/null || echo "{}")

    if echo "$response" | grep -q "$field"; then
        echo -e "${GREEN}✅ OK${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "   Response: $response"
        ((FAIL++))
    fi
}

# Check if Docker is running
echo -n "🐳 Verificando Docker... "
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Docker não está rodando!"
    ((FAIL++))
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test endpoints
echo "📡 Testando Endpoints:"
echo ""

test_endpoint "Root API" "http://localhost:8000/" "200"
test_endpoint "Health Check" "http://localhost:8000/health" "200"
test_json_endpoint "Health Status" "http://localhost:8000/api/health/status" "status"
test_endpoint "Frontend" "http://localhost:3000" "200"
test_endpoint "Evolution API" "http://localhost:8081" "200"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check containers
echo "📦 Status dos Containers:"
echo ""

docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
echo "📊 Resumo:"
echo ""
echo -e "  ${GREEN}✅ Pass:${PASS}${NC}"
echo -e "  ${RED}❌ Fail:${FAIL}${NC}"
echo -e "  ${YELLOW}⚠️  Warn:${WARN}${NC}"

echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ Todos os testes passaram!         ║${NC}"
    echo -e "${GREEN}║  🌙 Luna está operacional!            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ Alguns testes falharam            ║${NC}"
    echo -e "${RED}║  Verifique os logs: docker-compose logs${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    exit 1
fi
