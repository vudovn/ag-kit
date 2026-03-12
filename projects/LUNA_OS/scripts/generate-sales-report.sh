#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌙 LUNA OS — GENERATE ENTERPRISE SALES INTELLIGENCE REPORT
# Gera relatório completo de vendas via WhatsApp (GRANDE ESCALA)
# Pasta Oficial: /Users/franciscotaveira.ads/LUNA OS
# ═══════════════════════════════════════════════════════════════

set -e

# Pasta oficial
OFFICIAL_DIR="/Users/franciscotaveira.ads/LUNA OS"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA OS — Enterprise Report Generator         ║"
echo "║     Pasta Oficial: $OFFICIAL_DIR                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

cd "$OFFICIAL_DIR/backend"

# Run Python script
echo "📊 Generating enterprise report (pode demorar)..."
python3 app/scripts/enterprise_sales_report.py

echo ""
echo "✅ Enterprise report generated successfully!"
echo ""
echo "📁 Files created:"
echo "   - $OFFICIAL_DIR/ENTERPRISE_SALES_REPORT.md"
echo "   - $OFFICIAL_DIR/logs/enterprise_report_*.json"
echo ""
echo "📖 To view the report:"
echo "   cat $OFFICIAL_DIR/ENTERPRISE_SALES_REPORT.md"
echo ""
