#!/bin/bash
# 🌙 LUNA OS - Webhook Diagnostic Script
# Verifica se webhook está configurado e recebendo dados

set -e

echo "╔════════════════════════════════════════╗"
echo "║  🌙 LUNA OS - Webhook Diagnosis       ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "📋 Verificando configuração do webhook..."
echo ""

# 1. Check if Evolution API is running
echo -n "🔍 Evolution API está rodando? "
if docker-compose ps | grep -q "command-tower-evo-api"; then
    echo -e "${GREEN}✅ SIM${NC}"
else
    echo -e "${RED}❌ NÃO${NC}"
    echo "   Execute: docker-compose up -d"
    exit 1
fi

# 2. Check Evolution API health
echo -n "🔍 Evolution API responde? "
EVO_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/health 2>/dev/null || echo "000")
if [ "$EVO_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✅ SIM ($EVO_RESPONSE)${NC}"
else
    echo -e "${YELLOW}⚠️  NÃO ($EVO_RESPONSE)${NC}"
    echo "   Verifique: docker-compose logs command-tower-evo-api"
fi

# 3. Check Luna Backend
echo -n "🔍 Luna Backend está rodando? "
if docker-compose ps | grep -q "luna-backend"; then
    echo -e "${GREEN}✅ SIM${NC}"
else
    echo -e "${RED}❌ NÃO${NC}"
    echo "   Execute: docker-compose up -d"
    exit 1
fi

# 4. Check webhook endpoint
echo -n "🔍 Webhook endpoint responde? "
WEBHOOK_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/webhooks/evolution -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null || echo "000")
if [ "$WEBHOOK_RESPONSE" == "200" ] || [ "$WEBHOOK_RESPONSE" == "422" ]; then
    echo -e "${GREEN}✅ SIM ($WEBHOOK_RESPONSE)${NC}"
else
    echo -e "${RED}❌ NÃO ($WEBHOOK_RESPONSE)${NC}"
    echo "   Verifique: docker-compose logs luna-backend"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 5. Check recent webhook logs
echo "📊 Últimos 20 logs do webhook:"
echo ""
docker-compose logs luna-backend 2>/dev/null | grep -i webhook | tail -20 || echo "   Nenhum log encontrado"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 6. Check Evolution instance status
echo "📱 Status da instância Evolution:"
echo ""
EVO_STATUS=$(curl -s http://localhost:8081/instance/connectionState/haven \
  -H "apikey: mothership_master_2026" 2>/dev/null || echo '{"error": "failed"}')
echo "   $EVO_STATUS" | python3 -m json.tool 2>/dev/null || echo "   $EVO_STATUS"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 7. Test webhook with sample payload
echo "🧪 Testando webhook com payload de exemplo..."
echo ""

TEST_PAYLOAD='{
  "event": "messages.upsert",
  "instance": "haven",
  "data": {
    "message": {"conversation": "teste webhook"},
    "key": {
      "remoteJid": "5549999999999@s.whatsapp.net",
      "fromMe": false
    }
  }
}'

WEBHOOK_TEST=$(curl -s -X POST http://localhost:8000/api/webhooks/evolution \
  -H "Content-Type: application/json" \
  -d "$TEST_PAYLOAD" 2>/dev/null)

echo "   Resposta: $WEBHOOK_TEST" | python3 -m json.tool 2>/dev/null || echo "   Resposta: $WEBHOOK_TEST"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 8. Check Supabase tables
echo "🗄️  Verificando tables no Supabase..."
echo ""
echo "   Acesse: https://app.supabase.com → Table Editor"
echo "   Tables necessárias:"
echo "   - clients"
echo "   - conversations"
echo "   - messages"
echo "   - appointments"
echo ""
echo "   Se não existirem, execute o migration:"
echo "   ${BLUE}cat supabase-migration.sql${NC} → Copie e cole no SQL Editor"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 9. Instructions
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Configurar webhook no Evolution Manager:"
echo "   ${BLUE}http://localhost:8081${NC} → Manager → Webhooks"
echo "   URL: ${BLUE}http://luna-backend:8000/api/webhooks/evolution${NC}"
echo "   Events: messages.upsert"
echo ""
echo "2. Testar mensagem real no WhatsApp:"
echo "   Envie 'Oi' para o número da Haven"
echo ""
echo "3. Verificar logs em tempo real:"
echo "   ${BLUE}docker-compose logs -f luna-backend${NC}"
echo ""
echo "4. Se não funcionar, verifique:"
echo "   - Evolution API está conectada no WhatsApp? (veja QR Code)"
echo "   - Supabase URL e KEY estão corretos no .env?"
echo "   - Migration foi executado no Supabase?"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  ✅ Webhook Diagnosis Complete!       ║"
echo "╚════════════════════════════════════════╝"
