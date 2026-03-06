#!/bin/bash

# Release Cycle Automation Script
# Enforces protocols from .github/MAINTENANCE.md

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🤖 Initiating Antigravity Release Protocol...${NC}"

# 1. Validation Chain
echo -e "\n${YELLOW}Step 1: Running Validation Chain...${NC}"
echo "Running validate_skills.py..."
python3 scripts/validate_skills.py
echo "Running generate_index.py..."
python3 scripts/generate_index.py
echo "Running update_readme.py..."
python3 scripts/update_readme.py

# 2. Catalog (required for CI)
echo -e "\n${YELLOW}Step 2: Build catalog...${NC}"
npm run catalog

# 3. Stats Consistency Check
echo -e "\n${YELLOW}Step 3: Verifying Stats Consistency...${NC}"
JSON_COUNT=$(python3 -c "import json; print(len(json.load(open('skills_index.json'))))")
echo "Skills in Registry (JSON): $JSON_COUNT"

# Check README Intro
README_CONTENT=$(cat README.md)
if [[ "$README_CONTENT" != *"$JSON_COUNT high-performance"* ]]; then
    echo -e "${RED}❌ ERROR: README.md intro consistency failure!${NC}"
    echo "Expected: '$JSON_COUNT high-performance'"
    echo "Found mismatch. Please grep for 'high-performance' in README.md and fix it."
    exit 1
fi
echo -e "${GREEN}✅ Stats Consistent.${NC}"

# 4. Version check (package.json is source of truth for npm)
echo -e "\n${YELLOW}Step 4: Version check${NC}"
PKG_VERSION=$(node -p "require('./package.json').version")
echo "package.json version: $PKG_VERSION"
echo "Ensure this version is bumped before 'npm publish' (npm forbids republishing the same version)."

# 5. Contributor Check
echo -e "\n${YELLOW}Step 5: Contributor Check${NC}"
echo "Recent commits by author (check against README 'Repo Contributors'):"
git shortlog -sn --since="1 month ago" --all --no-merges | head -n 10

echo -e "${YELLOW}⚠️  MANUAL VERIFICATION REQUIRED:${NC}"
echo "1. Are all PR authors above listed in 'Repo Contributors'?"
echo "2. Are all External Sources listed in 'Credits & Sources'?"
read -p "Type 'yes' to confirm you have verified contributors: " CONFIRM_CONTRIB

if [ "$CONFIRM_CONTRIB" != "yes" ]; then
    echo -e "${RED}❌ Verification failed. Aborting.${NC}"
    exit 1
fi

echo -e "\n${GREEN}✅ Release Cycle Checks Passed. You may now commit and push.${NC}"
echo -e "${YELLOW}After tagging a release: run \`npm publish\` from repo root (or use GitHub Release + NPM_TOKEN for CI).${NC}"
exit 0
