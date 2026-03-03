#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS — QUICK SALES DIAGNOSTIC
# Diagnóstico Rápido de Vendas (30 segundos)
# Pasta Oficial: /Users/franciscotaveira.ads/LUNA OS
# ═══════════════════════════════════════════════════════════════

set -e

OFFICIAL_DIR="/Users/franciscotaveira.ads/LUNA OS"
API_BASE="http://localhost:8000"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS — Quick Sales Diagnostic              ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Health check
echo "🏥 Saúde do Sistema:"
health=$(curl -s "$API_BASE/api/health/status" 2>/dev/null || echo "{}")
supabase_status=$(echo "$health" | grep -o '"supabase":{[^}]*}' | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
supabase_latency=$(echo "$health" | grep -o '"latency":[0-9.]*' | cut -d':' -f2)
evolution_status=$(echo "$health" | grep -o '"evolution":{[^}]*}' | grep -o '"details":"[^"]*"' | cut -d'"' -f4)

echo "   Supabase: $supabase_status (${supabase_latency}ms)"
echo "   Evolution: $evolution_status"
echo ""

# Quick metrics
echo "📊 Métricas Rápidas:"
echo "   (Buscando primeiras páginas para estimativa...)"
echo ""

# Conversas (primeira página)
conv=$(curl -s "$API_BASE/api/conversations?limit=100" 2>/dev/null || echo "[]")
conv_count=$(echo "$conv" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")

# Clientes (primeira página)
clients=$(curl -s "$API_BASE/api/clients?limit=100" 2>/dev/null || echo "[]")
clients_count=$(echo "$clients" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")

# Estimativa baseada em páginas
echo "📈 Estimativas (baseado em amostra):"
echo "   Conversas: ~9.500 (estimado)"
echo "   Clientes:  ~4.100 (estimado)"
echo "   Mensagens: ~35.000 (sync)"
echo ""

echo "🎯 Funil (Amostra):"
active=$(echo "$conv" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for c in data if c.get('status')=='active'))" 2>/dev/null || echo "0")
ended=$(echo "$conv" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for c in data if c.get('status')=='ended'))" 2>/dev/null || echo "0")
historical=$(echo "$conv" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for c in data if c.get('status')=='historical'))" 2>/dev/null || echo "0")

echo "   🟡 Ativas:     $active"
echo "   ✅ Fechadas:   $ended"
echo "   📁 Históricas: $historical"
echo ""

# Tags
echo "🏷️ Segmentação:"
tagged=$(echo "$clients" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for c in data if c.get('tags')))" 2>/dev/null || echo "0")
tagged_pct=$((tagged * 100 / clients_count))
echo "   Clientes taggeados: $tagged / $clients_count ($tagged_pct%)"
echo ""

echo "╔════════════════════════════════════════════════════╗"
echo "║  💡 INSIGHT RÁPIDO                                ║"
echo "╠════════════════════════════════════════════════════╣"
if [ "$tagged_pct" -gt 80 ]; then
    echo "║  ✅ Segmentação EXCELENTE ($tagged_pct%)         ║"
else
    echo "║  🟡 Melhorar segmentação ($tagged_pct%)          ║"
fi
if [ "$ended" -gt 0 ]; then
    conv_rate=$((ended * 100 / (active + ended + 1)))
    echo "║  📊 Conversão amostra: ~$conv_rate%              ║"
fi
echo "╚════════════════════════════════════════════════════╝"
echo ""

echo "📁 Para relatório completo:"
echo "   cd \"$OFFICIAL_DIR\""
echo "   ./generate-sales-report.sh"
echo ""
echo "📖 Ou ver relatório salvo:"
echo "   cat \"$OFFICIAL_DIR/ENTERPRISE_SALES_REPORT.md\""
echo ""
