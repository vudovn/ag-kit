#!/bin/bash
# LUNA OS - Docker Cleanup & Next.js Start
# Libera portas 3000/3001 e inicia Next.js na 3001

set -e

echo "🚀 LUNA OS - Docker Cleanup & Start"
echo "===================================="

# 1. Stop Docker containers
echo "🐳 Stopping Docker containers..."
docker stop luna-frontend 2>/dev/null || echo "   Frontend container not running"
docker stop luna-backend 2>/dev/null || echo "   Backend container not running"

# 2. Remove containers
echo "🗑️  Removing containers..."
docker rm luna-frontend 2>/dev/null || true
docker rm luna-backend 2>/dev/null || true

# 3. Kill any remaining processes
echo "📌 Killing remaining processes..."
killall -9 node next-server 2>/dev/null || true

# 4. Clean Next.js cache
echo "🧹 Cleaning Next.js cache..."
cd '/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/frontend'
rm -rf .next node_modules/.cache .turbo

# 5. Start Next.js
echo "🚀 Starting Next.js on port 3001..."
PORT=3001 npm run dev > /tmp/luna-nextjs.log 2>&1 &

# 6. Wait for startup
echo "⏳ Waiting for Next.js to start..."
sleep 15

# 7. Verify
echo "📊 Verifying..."
if curl -s http://localhost:3001 | grep "Luna Core" > /dev/null; then
    echo "✅ Next.js running on http://localhost:3001"
    echo ""
    echo "🎯 Available pages:"
    echo "   - Dashboard:     http://localhost:3001/"
    echo "   - Dojo Arena:    http://localhost:3001/dojo"
    echo "   - Clients:       http://localhost:3001/clients"
    echo "   - Analytics:     http://localhost:3001/analytics-super"
    echo ""
    echo "✅ Ready to use!"
else
    echo "❌ Next.js failed to start"
    echo "📄 Logs: /tmp/luna-nextjs.log"
    exit 1
fi
