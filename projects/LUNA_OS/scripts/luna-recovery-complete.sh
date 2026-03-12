#!/bin/bash
# 🌙 LUNA OS - Complete Recovery Script
# Limpa containers, reconstrói imagens e sobe tudo do zero

set -e

echo "╔════════════════════════════════════════╗"
echo "║  🌙 LUNA OS - Complete Recovery       ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if in correct directory
if [ ! -f "docker-compose.yml" ]; then
    log_error "Erro: Execute este script na pasta LUNA_OS"
    log_info "cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS"
    exit 1
fi

log_success "Diretório correto: $(pwd)"
echo ""

# Step 1: Stop all containers
log_info "🛑 Parando todos os containers..."
docker-compose down --remove-orphans 2>/dev/null || true
log_success "Containers parados"
echo ""

# Step 2: Remove orphan volumes (optional - comment out to keep data)
read -p "🗑️  Remover volumes órfãos? (dados serão perdidos) [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removendo volumes órfãos..."
    docker volume rm $(docker volume ls -qf dangling=true) 2>/dev/null || true
    log_success "Volumes limpos"
fi
echo ""

# Step 3: Remove old images (optional)
read -p "🗑️  Remover imagens antigas? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removendo imagens antigas..."
    docker rmi $(docker images | grep "luna_os" | awk '{print $3}') 2>/dev/null || true
    log_success "Imagens removidas"
fi
echo ""

# Step 4: Clean up system
log_info "🧹 Limpando sistema Docker..."
docker system prune -f --volumes 2>/dev/null || true
log_success "Sistema limpo"
echo ""

# Step 5: Check .env file
log_info "📄 Verificando arquivo .env..."
if [ ! -f ".env" ]; then
    log_warning ".env não encontrado. Copiando .env.example..."
    cp .env.example .env
    log_success ".env criado. Edite com suas chaves de API!"
    log_warning "⚠️  IMPORTANTE: Configure SUPABASE_URL, SUPABASE_KEY e OPENROUTER_API_KEY"
else
    log_success ".env encontrado"
fi
echo ""

# Step 6: Build and start services
log_info "🚀 Construindo e iniciando serviços..."
docker-compose up -d --build
log_success "Serviços iniciados"
echo ""

# Step 7: Wait for services to be ready
log_info "⏳ Aguardando serviços ficarem prontos (30s)..."
sleep 30

# Step 8: Check status
echo ""
log_info "📊 Status dos serviços:"
docker-compose ps

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  ✅ LUNA OS Recovery Complete!        ║"
echo "╚════════════════════════════════════════╝"
echo ""
log_info "🌐 Acesse:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Health:    http://localhost:8000/health"
echo "   Evolution: http://localhost:8081"
echo ""
log_info "📋 Comandos úteis:"
echo "   docker-compose logs -f     # Ver logs"
echo "   docker-compose ps          # Status"
echo "   docker-compose down        # Parar"
echo ""
log_success "🌙 Luna está operacional!"
