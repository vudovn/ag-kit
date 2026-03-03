#!/bin/bash
# LUNA OS - Start Script
# Gerencia portas e inicia apenas os servidores necessários
# Porta Oficial Frontend: 3001

set -e

echo "🚀 LUNA OS - Starting..."
echo "========================"

# Função para matar processo na porta
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "⚠️  Killing process on port $port (PID: $pid)"
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

# Limpar portas se necessário
if [ "$1" == "--clean" ]; then
    echo "🧹 Cleaning ports..."
    kill_port 3000
    kill_port 3001
    kill_port 8000
fi

# Verificar portas ocupadas
echo "📊 Checking ports..."
PORT_3000=$(lsof -ti:3000 2>/dev/null)
PORT_3001=$(lsof -ti:3001 2>/dev/null)
PORT_8000=$(lsof -ti:8000 2>/dev/null)

if [ ! -z "$PORT_3000" ]; then
    echo "⚠️  Port 3000 already in use (PID: $PORT_3000) - THIS IS NOT THE OFFICIAL PORT!"
fi

if [ ! -z "$PORT_3001" ]; then
    echo "✅ Frontend running on port 3001 (PID: $PORT_3001)"
fi

if [ ! -z "$PORT_8000" ]; then
    echo "✅ Backend running on port 8000 (PID: $PORT_8000)"
else
    echo "❌ Backend not running on port 8000"
fi

# Status
echo ""
echo "📍 Current Status:"
echo "   Frontend (Next.js): Port 3001 ${PORT_3001:+✓ running} ${PORT_3001:+(PID: $PORT_3001)}"
echo "   Backend (FastAPI):  Port 8000 ${PORT_8000:+✓ running} ${PORT_8000:+(PID: $PORT_8000)}"
if [ ! -z "$PORT_3000" ]; then
    echo "   ⚠️  Extra (Conflict):   Port 3000 ✓ running (PID: $PORT_3000) - SHOULD BE KILLED!"
fi
echo ""

# Se tiver processo na 3000, matar (não é a oficial)
if [ ! -z "$PORT_3000" ]; then
    echo "⚠️  Found non-official server on port 3000 - killing..."
    kill -9 $PORT_3000 2>/dev/null || true
    sleep 1
    echo "✅ Port 3000 freed (non-official)"
fi

echo ""
echo "✅ Ports cleaned and ready!"
echo ""
echo "📚 Usage:"
echo "   cd LUNA_OS/frontend && PORT=3001 npm run dev    # Start frontend (port 3001 - OFFICIAL)"
echo "   cd LUNA_OS/backend && uvicorn ...     # Start backend (port 8000)"
echo ""
echo "   Or use Docker:"
echo "   docker-compose up -d"
echo ""
echo "🎯 Official URLs:"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:8000"
echo ""
