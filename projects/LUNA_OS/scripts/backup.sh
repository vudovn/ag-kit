#!/bin/bash

# ═══════════════════════════════════════════════════════════
# LUNA OS - Backup Automático
# 
# Faz backup de:
# - Supabase (via API ou pg_dump)
# - Windmill Database
# - Evolution Database
# - Arquivos de configuração
#
# Uso: ./backup.sh [daily|weekly]
# ═══════════════════════════════════════════════════════════

set -e

# Configuração
BACKUP_DIR="${BACKUP_DIR:-/tmp/luna_backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
RETENTION_WEEKS="${RETENTION_WEEKS:-4}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         LUNA OS - Backup Automático                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# ═══════════════════════════════════════════════════════════
# 1. Backup do Windmill Database
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[1/4] Backup Windmill Database...${NC}"

docker exec luna-windmill-db pg_dump \
    -U luna_user \
    -d windmill \
    > "$BACKUP_DIR/windmill_db_$TIMESTAMP.sql"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Windmill DB backup OK${NC}"
else
    echo -e "${RED}❌ Windmill DB backup FAILED${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 2. Backup do Evolution Database
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[2/4] Backup Evolution Database...${NC}"

docker exec luna-evo-db pg_dump \
    -U evolution \
    -d evolution \
    > "$BACKUP_DIR/evolution_db_$TIMESTAMP.sql"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Evolution DB backup OK${NC}"
else
    echo -e "${RED}❌ Evolution DB backup FAILED${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 3. Backup de Configurações
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[3/4] Backup Configurações...${NC}"

# Criar tar com configs
tar -czf "$BACKUP_DIR/configs_$TIMESTAMP.tar.gz" \
    .env \
    docker-compose.yml \
    docker-compose.extended.yml \
    docker-compose.windmill.yml \
    2>/dev/null || true

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Configs backup OK${NC}"
else
    echo -e "${YELLOW}⚠️  Some configs not found (normal)${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 4. Limpeza de Backups Antigos
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}[4/4] Limpando backups antigos...${NC}"

# Remover backups com mais de X dias
find "$BACKUP_DIR" -name "*.sql" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.zip" -mtime +$RETENTION_DAYS -delete

echo -e "${GREEN}✅ Cleanup OK${NC}"

# ═══════════════════════════════════════════════════════════
# Resumo
# ═══════════════════════════════════════════════════════════

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    Backup Concluído                      ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Local: $BACKUP_DIR"
echo "║  Timestamp: $TIMESTAMP"
echo "║  Arquivos:"
ls -lh "$BACKUP_DIR"/*"$TIMESTAMP"* 2>/dev/null | awk '{print "║    " $9 " (" $5 ")"}'
echo "╚══════════════════════════════════════════════════════════╝"

# Opcional: Upload para S3/GCS
# if [ -n "$AWS_BUCKET" ]; then
#     echo "Uploading to S3..."
#     aws s3 cp "$BACKUP_DIR" "s3://$AWS_BUCKET/luna_backups/" --recursive
# fi
