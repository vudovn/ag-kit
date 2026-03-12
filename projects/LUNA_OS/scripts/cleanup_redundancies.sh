#!/bin/bash
# ============================================================
# LUNA OS — Cleanup Redundancies
# ============================================================
# Remove redundant files and clean cache
# ============================================================

set -e

echo "🧹 LUNA OS — Limpando Redundâncias..."
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Directories
LUNA_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$LUNA_OS_DIR/backend"
FRONTEND_DIR="$LUNA_OS_DIR/frontend"

# ============================================================
# 1. BACKEND CLEANUP
# ============================================================

echo "📦 Backend Cleanup..."
cd "$BACKEND_DIR"

# Create archive directory
mkdir -p archive/redundant

# Files to archive
declare -a BACKEND_FILES=(
    "app/core/schemas_brain.py"
    "app/services/brain_structurer.py"
    "app/dojo/multi_llm_replay.py"
    "app/api/brain.py"
)

# Archive files
for file in "${BACKEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" archive/redundant/
        echo -e "${GREEN}✓${NC} Archived: $file"
    else
        echo -e "${YELLOW}○${NC} Not found: $file"
    fi
done

# Clean Python cache
echo ""
echo "🗑️  Cleaning Python cache..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Cache cleaned"

# ============================================================
# 2. FRONTEND CLEANUP
# ============================================================

echo ""
echo "📦 Frontend Cleanup..."
cd "$FRONTEND_DIR"

# Create archive directory
mkdir -p archive/pages

# Files to archive
declare -a FRONTEND_FILES=(
    "app/analytics/page.tsx"
    "app/analytics-super/page.tsx"
)

# Archive files
for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" archive/pages/
        echo -e "${GREEN}✓${NC} Archived: $file"
    else
        echo -e "${YELLOW}○${NC} Not found: $file"
    fi
done

# ============================================================
# 3. SUMMARY
# ============================================================

echo ""
echo "========================================"
echo "✅ CLEANUP COMPLETED!"
echo "========================================"
echo ""
echo "Archived files:"
echo "  Backend: ${#BACKEND_FILES[@]} files"
echo "  Frontend: ${#FRONTEND_FILES[@]} files"
echo ""
echo "Next steps:"
echo "  1. Test backend: cd backend && python -m pytest tests/ -v"
echo "  2. Test frontend: cd frontend && npm run dev"
echo "  3. Commit: git add . && git commit -m 'Cleanup redundancies'"
echo ""
echo -e "${GREEN}✓${NC} Done!"
