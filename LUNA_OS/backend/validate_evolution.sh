#!/bin/bash
# LUNA OS Evolution - Validation Script
# Data: 2026-03-01
# Uso: ./validate_evolution.sh

echo "🧪 LUNA OS Evolution - Validation Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to check endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" == "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} ($response)"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC} (expected $expected_status, got $response)"
        ((FAILED++))
    fi
}

# Function to check JSON response
check_json() {
    local name=$1
    local url=$2
    local field=$3
    
    echo -n "Testing $name... "
    
    response=$(curl -s "$url" 2>/dev/null)
    
    if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); assert '$field' in data" 2>/dev/null; then
        echo -e "${GREEN}✅ PASS${NC} (has $field)"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC} (missing $field)"
        ((FAILED++))
    fi
}

echo "1. Testing Core Endpoints..."
echo "----------------------------"
check_endpoint "Health Check" "http://localhost:8000/health"
check_endpoint "Root API" "http://localhost:8000/"
check_json "Dojo Proposals" "http://localhost:8000/api/dojo/proposals" "success"
check_json "Edge Cases" "http://localhost:8000/api/dojo/edge-cases" "success"
check_json "Intelligence Insights" "http://localhost:8000/api/intelligence/insights?days=7" "success"
echo ""

echo "2. Testing Database Tables..."
echo "------------------------------"
# These require Supabase credentials, so we'll just check if the migration file exists
if [ -f "supabase_evolution_migration.sql" ]; then
    echo -e "${GREEN}✅ Migration file exists${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ Migration file not found${NC}"
    ((FAILED++))
fi

if grep -q "CREATE TABLE.*prompt_proposals" supabase_evolution_migration.sql 2>/dev/null; then
    echo -e "${GREEN}✅ prompt_proposals table defined${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  prompt_proposals table not found in migration${NC}"
fi

if grep -q "CREATE TABLE.*conversation_intelligence" supabase_evolution_migration.sql 2>/dev/null; then
    echo -e "${GREEN}✅ conversation_intelligence table defined${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  conversation_intelligence table not found in migration${NC}"
fi

if grep -q "CREATE TABLE.*dojo_edge_cases" supabase_evolution_migration.sql 2>/dev/null; then
    echo -e "${GREEN}✅ dojo_edge_cases table defined${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  dojo_edge_cases table not found in migration${NC}"
fi
echo ""

echo "3. Testing Python Modules..."
echo "-----------------------------"
# Check if files exist
files=(
    "app/dojo/learning_cycle.py"
    "app/modules_v3/conversation_intelligence/pipeline.py"
    "app/core/task_runner.py"
    "app/api/dojo_learning.py"
    "app/api/intelligence.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $file not found${NC}"
        ((FAILED++))
    fi
done
echo ""

echo "4. Testing Frontend..."
echo "----------------------"
if [ -f "../frontend/app/intelligence/page.tsx" ]; then
    echo -e "${GREEN}✅ Intelligence page exists${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ Intelligence page not found${NC}"
    ((FAILED++))
fi
echo ""

echo "5. Testing main.py Integration..."
echo "----------------------------------"
if grep -q "dojo_learning_router" ../backend/app/main.py 2>/dev/null || grep -q "dojo_learning" app/main.py 2>/dev/null; then
    echo -e "${GREEN}✅ Dojo Learning router registered${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Dojo Learning router not found in main.py${NC}"
fi

if grep -q "intelligence_router" ../backend/app/main.py 2>/dev/null || grep -q "intelligence_router" app/main.py 2>/dev/null; then
    echo -e "${GREEN}✅ Intelligence router registered${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Intelligence router not found in main.py${NC}"
fi

if grep -q "task_runner" ../backend/app/main.py 2>/dev/null || grep -q "task_runner" app/main.py 2>/dev/null; then
    echo -e "${GREEN}✅ Task Runner imported${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Task Runner not found in main.py${NC}"
fi
echo ""

echo "=========================================="
echo "RESULTS:"
echo "  ${GREEN}✅ Passed: $PASSED${NC}"
echo "  ${RED}❌ Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Evolution is ready!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. Please review.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run migration in Supabase SQL Editor:"
    echo "   backend/supabase_evolution_migration.sql"
    echo ""
    echo "2. Restart backend to load new modules:"
    echo "   cd backend && docker compose restart luna-backend"
    echo ""
    echo "3. Test frontend at:"
    echo "   http://localhost:3000/intelligence"
    exit 1
fi
