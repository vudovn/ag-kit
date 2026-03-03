#!/bin/bash
# LUNA OS - Start Production Server
# Evita erros de cache usando build estático

set -e

echo "🚀 LUNA OS - Starting Production Server"
echo "========================================"

cd '/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/frontend'

# 1. Kill existing processes
echo "📌 Stopping existing processes..."
killall -9 node next-server 2>/dev/null || true
sleep 1

# 2. Clean cache
echo "🧹 Cleaning cache..."
rm -rf .next node_modules/.cache .turbo

# 3. Build
echo "🏗️  Building production version..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# 4. Start production server
echo "🚀 Starting production server on port 3001..."
PORT=3001 npm start &

# 5. Wait for server
echo "⏳ Waiting for server to start..."
sleep 10

# 6. Verify
echo "📊 Verifying server..."
if curl -s http://localhost:3001 | grep "Luna Core" > /dev/null; then
    echo "✅ Server running on http://localhost:3001"
    echo ""
    echo "🎯 Available pages:"
    echo "   - Dashboard:     http://localhost:3001/"
    echo "   - Dojo Arena:    http://localhost:3001/dojo"
    echo "   - Clients:       http://localhost:3001/clients"
    echo "   - Analytics:     http://localhost:3001/analytics-super"
    echo ""
    echo "✅ Ready to use!"
else
    echo "❌ Server failed to start"
    exit 1
fi
