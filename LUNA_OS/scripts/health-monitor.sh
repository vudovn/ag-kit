#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS v2.2 — REAL-TIME HEALTH MONITOR
# ═══════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
NC='\033[0m'

# Configuration
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
EVOLUTION_URL="http://localhost:8081"
TIMEOUT=10

# Counters
PASS=0
FAIL=0
WARN=0

# Functions
print_header() {
    echo -e "\n${CYAN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  $1${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════╝${NC}\n"
}

print_check() {
    local name="$1"
    local status="$2"
    local details="$3"
    
    if [ "$status" == "PASS" ]; then
        echo -e "${GREEN}✅${NC} $name"
        ((PASS++))
    elif [ "$status" == "FAIL" ]; then
        echo -e "${RED}❌${NC} $name"
        ((FAIL++))
    else
        echo -e "${YELLOW}⚠️${NC} $name"
        ((WARN++))
    fi
    
    if [ -n "$details" ]; then
        echo -e "   ${WHITE}$details${NC}"
    fi
}

check_http() {
    local name="$1"
    local url="$2"
    local expected="${3:-200}"
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$url" 2>/dev/null || echo "000")
    
    if [ "$response" == "$expected" ] || [ "$response" == "200" ]; then
        print_check "$name" "PASS" "HTTP $response"
        return 0
    elif [ "$response" == "000" ]; then
        print_check "$name" "FAIL" "No response (timeout: ${TIMEOUT}s)"
        return 1
    else
        print_check "$name" "WARN" "HTTP $response (expected: $expected)"
        return 2
    fi
}

check_json_field() {
    local name="$1"
    local url="$2"
    local field="$3"
    
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null || echo "{}")
    
    if echo "$response" | grep -q "$field"; then
        print_check "$name" "PASS" "Field '$field' found"
        return 0
    else
        print_check "$name" "FAIL" "Field '$field' not found"
        echo -e "   ${WHITE}Response: $response${NC}"
        return 1
    fi
}

check_json_value() {
    local name="$1"
    local url="$2"
    local field="$3"
    local expected="$4"
    
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null || echo "{}")
    local value=$(echo "$response" | grep -o "\"$field\":\"[^\"]*\"" | cut -d'"' -f4)
    
    if [ "$value" == "$expected" ]; then
        print_check "$name" "PASS" "$field = $value"
        return 0
    else
        print_check "$name" "WARN" "$field = $value (expected: $expected)"
        return 2
    fi
}

check_docker() {
    local name="$1"
    local container="$2"
    
    local status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "not_found")
    
    if [ "$status" == "running" ]; then
        print_check "$name" "PASS" "Container running"
        return 0
    elif [ "$status" == "not_found" ]; then
        print_check "$name" "FAIL" "Container not found"
        return 1
    else
        print_check "$name" "WARN" "Container $status"
        return 2
    fi
}

# Main
print_header "🌙 LUNA OS v2.2 — REAL-TIME HEALTH MONITOR"

echo -e "${WHITE}Timestamp: $(date -Iseconds)${NC}"
echo -e "${WHITE}Timeout: ${TIMEOUT}s per check${NC}\n"

# ═══════════════════════════════════════════════════════════════
# DOCKER CONTAINERS
# ═══════════════════════════════════════════════════════════════

print_header "🐳 DOCKER CONTAINERS"

check_docker "Luna Backend" "luna-backend"
check_docker "Luna Frontend" "luna-frontend"
check_docker "Evolution API" "command-tower-evo-api"
check_docker "Evolution DB" "command-tower-evo-db"
check_docker "Redis" "command-tower-redis"

# ═══════════════════════════════════════════════════════════════
# BACKEND ENDPOINTS
# ═══════════════════════════════════════════════════════════════

print_header "🔧 BACKEND ENDPOINTS"

check_http "Root API" "$BACKEND_URL/"
check_http "Basic Health" "$BACKEND_URL/health"
check_json_field "Health Status" "$BACKEND_URL/api/health/status" "status"
check_json_field "Analytics Overview" "$BACKEND_URL/api/analytics/overview" "status"
check_json_field "Evolution Maturity" "$BACKEND_URL/api/evolution/maturity" "status"
check_http "Dojo Scenarios" "$BACKEND_URL/api/dojo/scenarios"
check_http "Knowledge Base" "$BACKEND_URL/api/knowledge"
check_http "Brain Status" "$BACKEND_URL/api/brain/status"

# ═══════════════════════════════════════════════════════════════
# INTEGRATION HEALTH
# ═══════════════════════════════════════════════════════════════

print_header "🔗 INTEGRATION HEALTH"

# Supabase
check_json_value "Supabase Status" "$BACKEND_URL/api/health/status" "supabase" "connected"

# Evolution API
check_http "Evolution API Root" "$EVOLUTION_URL" "404"

# OpenRouter
check_json_field "OpenRouter Status" "$BACKEND_URL/api/health/status" "openrouter"

# Frontend
check_http "Frontend UI" "$FRONTEND_URL"

# ═══════════════════════════════════════════════════════════════
# DETAILED HEALTH ANALYSIS
# ═══════════════════════════════════════════════════════════════

print_header "📊 DETAILED HEALTH ANALYSIS"

# Get detailed health
HEALTH_RESPONSE=$(curl -s --max-time $TIMEOUT "$BACKEND_URL/api/health/status" 2>/dev/null || echo "{}")

# Supabase Latency
SUPABASE_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"supabase":{[^}]*}' || echo "{}")
if echo "$SUPABASE_STATUS" | grep -q "connected"; then
    LATENCY=$(echo "$SUPABASE_STATUS" | grep -o '"latency":[0-9.]*' | cut -d':' -f2)
    if [ -n "$LATENCY" ]; then
        if (( $(echo "$LATENCY < 500" | bc -l 2>/dev/null || echo 0) )); then
            print_check "Supabase Latency" "PASS" "${LATENCY}ms (meta: <500ms)"
        else
            print_check "Supabase Latency" "WARN" "${LATENCY}ms (meta: <500ms)"
        fi
    else
        print_check "Supabase Latency" "WARN" "Latency not reported"
    fi
else
    print_check "Supabase Connection" "FAIL" "Not connected"
fi

# Evolution Status
EVOLUTION_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"evolution":{[^}]*}' || echo "{}")
if echo "$EVOLUTION_STATUS" | grep -q "connected"; then
    print_check "Evolution Connection" "PASS" "Connected"
elif echo "$EVOLUTION_STATUS" | grep -q "warning"; then
    EVOLUTION_DETAILS=$(echo "$EVOLUTION_STATUS" | grep -o '"details":"[^"]*"' | cut -d'"' -f4)
    print_check "Evolution Connection" "WARN" "$EVOLUTION_DETAILS"
else
    print_check "Evolution Connection" "FAIL" "Not connected"
fi

# System Health
SYSTEM_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"system":{[^}]*}' || echo "{}")
if echo "$SYSTEM_STATUS" | grep -q "connected"; then
    SYSTEM_DETAILS=$(echo "$SYSTEM_STATUS" | grep -o '"details":"[^"]*"' | cut -d'"' -f4)
    print_check "System Health" "PASS" "$SYSTEM_DETAILS"
else
    print_check "System Health" "WARN" "Status unknown"
fi

# Overall Status
OVERALL=$(echo "$HEALTH_RESPONSE" | grep -o '"overall":"[^"]*"' | cut -d'"' -f4)
if [ "$OVERALL" == "healthy" ]; then
    print_check "Overall Status" "PASS" "HEALTHY"
elif [ "$OVERALL" == "degraded" ]; then
    print_check "Overall Status" "WARN" "DEGRADED"
else
    print_check "Overall Status" "FAIL" "${OVERALL:-unknown}"
fi

# ═══════════════════════════════════════════════════════════════
# DATABASE TABLES
# ═══════════════════════════════════════════════════════════════

print_header "🗄️  DATABASE TABLES (Supabase)"

# Note: This would require direct DB access, using API as proxy
check_json_field "Clients Table" "$BACKEND_URL/api/clients" "clients"
check_json_field "Conversations Table" "$BACKEND_URL/api/conversations" "conversations"

# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════

print_header "📚 KNOWLEDGE BASE"

KB_RESPONSE=$(curl -s --max-time $TIMEOUT "$BACKEND_URL/api/knowledge" 2>/dev/null || echo "{}")

if echo "$KB_RESPONSE" | grep -q "haven.json"; then
    print_check "Knowledge Base" "PASS" "haven.json loaded"
else
    print_check "Knowledge Base" "WARN" "Status unknown"
fi

# ═══════════════════════════════════════════════════════════════
# DOJO ARENA
# ═══════════════════════════════════════════════════════════════

print_header "🥋 DOJO ARENA"

DOJO_RESPONSE=$(curl -s --max-time $TIMEOUT "$BACKEND_URL/api/dojo/scenarios" 2>/dev/null || echo "{}")

if echo "$DOJO_RESPONSE" | grep -q '"total":'; then
    TOTAL_SCENARIOS=$(echo "$DOJO_RESPONSE" | grep -o '"total":[0-9]*' | cut -d':' -f2)
    print_check "Dojo Scenarios" "PASS" "$TOTAL_SCENARIOS scenarios loaded"
else
    print_check "Dojo Scenarios" "WARN" "Status unknown"
fi

DOJO_PERSONAS=$(curl -s --max-time $TIMEOUT "$BACKEND_URL/api/dojo/personas" 2>/dev/null || echo "{}")

if echo "$DOJO_PERSONAS" | grep -q '"total":'; then
    TOTAL_PERSONAS=$(echo "$DOJO_PERSONAS" | grep -o '"total":[0-9]*' | cut -d':' -f2)
    print_check "Dojo Personas" "PASS" "$TOTAL_PERSONAS personas loaded"
else
    print_check "Dojo Personas" "WARN" "Status unknown"
fi

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

print_header "📊 HEALTH CHECK SUMMARY"

TOTAL=$((PASS + FAIL + WARN))
SCORE=$((PASS * 100 / TOTAL))

echo -e "${WHITE}Total Checks: $TOTAL${NC}"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo -e "${YELLOW}Warnings: $WARN${NC}"
echo ""
echo -e "${WHITE}Health Score: ${GREEN}${SCORE}%${NC}"
echo ""

# Verdict
if [ $FAIL -eq 0 ] && [ $WARN -le 2 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🏆 EXCELLENT! LUNA OS is in PEAK PERFORMANCE     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
    EXIT_CODE=0
elif [ $FAIL -le 2 ] && [ $WARN -le 5 ]; then
    echo -e "${YELLOW}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠️  GOOD! Some improvements needed               ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════╝${NC}"
    EXIT_CODE=0
else
    echo -e "${RED}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ CRITICAL! Immediate attention required         ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════╝${NC}"
    EXIT_CODE=1
fi

# Save results
RESULTS_FILE="logs/health_check_$(date +%Y%m%d_%H%M%S).json"
mkdir -p logs
cat > "$RESULTS_FILE" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "total_checks": $TOTAL,
  "passed": $PASS,
  "failed": $FAIL,
  "warnings": $WARN,
  "health_score": $SCORE,
  "exit_code": $EXIT_CODE
}
EOF

echo -e "\n${WHITE}Results saved to: $RESULTS_FILE${NC}\n"

exit $EXIT_CODE
