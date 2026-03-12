#!/bin/bash

# ═══════════════════════════════════════════════════════════
# LUNA OS - Health Check Unificado
# 
# Verifica saúde de TODOS os serviços em um só lugar
#
# Uso: ./health-check.sh [--verbose]
# ═══════════════════════════════════════════════════════════

# Configuração
VERBOSE="${VERBOSE:-false}"
if [[ "$*" == *"--verbose"* ]]; then
    VERBOSE=true
fi

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Contadores
PASS=0
FAIL=0
WARN=0

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         LUNA OS - Health Check Unificado                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════
# 1. Docker Containers
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[1/8] Docker Containers...${NC}"

CONTAINERS=(
    "luna-backend"
    "luna-frontend"
    "luna-redis"
    "luna-evo-api"
    "luna-evo-db"
    "luna-windmill-server"
    "luna-windmill-db"
)

for container in "${CONTAINERS[@]}"; do
    if docker ps | grep -q "$container"; then
        HEALTH=$(docker inspect "$container" --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' 2>/dev/null)
        
        if [ "$HEALTH" = "healthy" ] || [ "$HEALTH" = "no-healthcheck" ]; then
            echo -e "  ${GREEN}✓${NC} $container"
            ((PASS++))
        else
            echo -e "  ${YELLOW}⚠${NC} $container ($HEALTH)"
            ((WARN++))
        fi
    else
        echo -e "  ${RED}✗${NC} $container (not running)"
        ((FAIL++))
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════
# 2. Backend API
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[2/8] Backend API...${NC}"

BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)

if echo "$BACKEND_HEALTH" | grep -q "healthy"; then
    VERSION=$(echo "$BACKEND_HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('version', 'unknown'))" 2>/dev/null)
    echo -e "  ${GREEN}✓${NC} Backend healthy (v$VERSION)"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Backend unhealthy"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 3. Frontend
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[3/8] Frontend...${NC}"

FRONTEND_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)

if [ "$FRONTEND_CODE" = "200" ]; then
    echo -e "  ${GREEN}✓${NC} Frontend online"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Frontend offline (HTTP $FRONTEND_CODE)"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 4. Windmill
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[4/8] Windmill...${NC}"

WINDMILL_HEALTH=$(curl -s http://localhost:8001/api/health/status 2>/dev/null)

if echo "$WINDMILL_HEALTH" | grep -q "healthy"; then
    WORKERS=$(echo "$WINDMILL_HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('workers_alive', 0))" 2>/dev/null)
    echo -e "  ${GREEN}✓${NC} Windmill healthy ($WORKERS workers)"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Windmill unhealthy"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 5. Redis
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[5/8] Redis...${NC}"

REDIS_PING=$(docker exec luna-redis redis-cli ping 2>/dev/null)

if [ "$REDIS_PING" = "PONG" ]; then
    echo -e "  ${GREEN}✓${NC} Redis responding"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Redis not responding"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 6. Evolution API
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[6/8] Evolution API...${NC}"

EVO_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "apikey: mothership_master_2026" \
    http://localhost:8081/instance/fetchInstances 2>/dev/null)

if [ "$EVO_CODE" = "200" ]; then
    echo -e "  ${GREEN}✓${NC} Evolution API online"
    ((PASS++))
else
    echo -e "  ${YELLOW}⚠${NC} Evolution API status: HTTP $EVO_CODE"
    ((WARN++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 7. Databases
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[7/8] Databases...${NC}"

# Windmill DB
WINDMILL_DB=$(docker exec luna-windmill-db pg_isready -U luna_user -d windmill 2>/dev/null)
if echo "$WINDMILL_DB" | grep -q "accepting"; then
    echo -e "  ${GREEN}✓${NC} Windmill DB accepting connections"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Windmill DB not ready"
    ((FAIL++))
fi

# Evolution DB
EVO_DB=$(docker exec luna-evo-db pg_isready -U evolution -d evolution 2>/dev/null)
if echo "$EVO_DB" | grep -q "accepting"; then
    echo -e "  ${GREEN}✓${NC} Evolution DB accepting connections"
    ((PASS++))
else
    echo -e "  ${RED}✗${NC} Evolution DB not ready"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 8. Disk Space
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[8/8] Disk Space...${NC}"

DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "  ${GREEN}✓${NC} Disk usage: ${DISK_USAGE}%"
    ((PASS++))
elif [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "  ${YELLOW}⚠${NC} Disk usage: ${DISK_USAGE}% (warning)"
    ((WARN++))
else
    echo -e "  ${RED}✗${NC} Disk usage: ${DISK_USAGE}% (critical)"
    ((FAIL++))
fi

echo ""

# ═══════════════════════════════════════════════════════════
# Resumo
# ═══════════════════════════════════════════════════════════

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    Health Summary                        ║"
echo "╠══════════════════════════════════════════════════════════╣"
printf "║  ${GREEN}PASS${NC}: %-3d  ${YELLOW}WARN${NC}: %-3d  ${RED}FAIL${NC}: %-3d                   ║\n" "$PASS" "$WARN" "$FAIL"
echo "╠══════════════════════════════════════════════════════════╣"

if [ "$FAIL" -eq 0 ]; then
    echo -e "║  ${GREEN}✅ SYSTEM HEALTHY${NC}                                      ║"
else
    echo -e "║  ${RED}❌ SYSTEM DEGRADED - ACTION REQUIRED${NC}                     ║"
fi

echo "╚══════════════════════════════════════════════════════════╝"

# Exit code
if [ "$FAIL" -eq 0 ]; then
    exit 0
else
    exit 1
fi
