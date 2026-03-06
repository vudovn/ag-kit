#!/bin/bash
# sync_recommended_skills.sh
# Syncs only the 35 recommended skills from GitHub repo to local central library

set -e

# Paths
GITHUB_REPO="/Users/nicco/Antigravity Projects/antigravity-awesome-skills/skills"
LOCAL_LIBRARY="/Users/nicco/.gemini/antigravity/scratch/.agent/skills"
BACKUP_DIR="/Users/nicco/.gemini/antigravity/scratch/.agent/skills_backup_$(date +%Y%m%d_%H%M%S)"

# 35 Recommended Skills
RECOMMENDED_SKILLS=(
    # Tier S - Core Development (13)
    "systematic-debugging"
    "test-driven-development"
    "writing-skills"
    "doc-coauthoring"
    "planning-with-files"
    "concise-planning"
    "software-architecture"
    "senior-architect"
    "senior-fullstack"
    "verification-before-completion"
    "git-pushing"
    "address-github-comments"
    "javascript-mastery"
    
    # Tier A - Your Projects (12)
    "docx-official"
    "pdf-official"
    "pptx-official"
    "xlsx-official"
    "react-best-practices"
    "web-design-guidelines"
    "frontend-dev-guidelines"
    "webapp-testing"
    "playwright-skill"
    "mcp-builder"
    "notebooklm"
    "ui-ux-pro-max"
    
    # Marketing & SEO (1)
    "content-creator"
    
    # Corporate (4)
    "brand-guidelines-anthropic"
    "brand-guidelines-community"
    "internal-comms-anthropic"
    "internal-comms-community"
    
    # Planning & Documentation (1)
    "writing-plans"
    
    # AI & Automation (5)
    "workflow-automation"
    "llm-app-patterns"
    "autonomous-agent-patterns"
    "prompt-library"
    "github-workflow-automation"
)

echo "🔄 Sync Recommended Skills"
echo "========================="
echo ""
echo "📍 Source: $GITHUB_REPO"
echo "📍 Target: $LOCAL_LIBRARY"
echo "📊 Skills to sync: ${#RECOMMENDED_SKILLS[@]}"
echo ""

# Create backup
echo "📦 Creating backup at: $BACKUP_DIR"
cp -r "$LOCAL_LIBRARY" "$BACKUP_DIR"
echo "✅ Backup created"
echo ""

# Clear local library (keep README.md if exists)
echo "🗑️  Clearing local library..."
cd "$LOCAL_LIBRARY"
for item in */; do
    rm -rf "$item"
done
echo "✅ Local library cleared"
echo ""

# Copy recommended skills
echo "📋 Copying recommended skills..."
SUCCESS_COUNT=0
MISSING_COUNT=0

for skill in "${RECOMMENDED_SKILLS[@]}"; do
    if [ -d "$GITHUB_REPO/$skill" ]; then
        cp -r "$GITHUB_REPO/$skill" "$LOCAL_LIBRARY/"
        echo "  ✅ $skill"
        ((SUCCESS_COUNT++))
    else
        echo "  ⚠️  $skill (not found in repo)"
        ((MISSING_COUNT++))
    fi
done

echo ""
echo "📊 Summary"
echo "=========="
echo "✅ Copied: $SUCCESS_COUNT skills"
echo "⚠️  Missing: $MISSING_COUNT skills"
echo "📦 Backup: $BACKUP_DIR"
echo ""

# Verify
FINAL_COUNT=$(find "$LOCAL_LIBRARY" -maxdepth 1 -type d ! -name "." | wc -l | tr -d ' ')
echo "🎯 Final count in local library: $FINAL_COUNT skills"
echo ""
echo "Done! Your local library now has only the recommended skills."
