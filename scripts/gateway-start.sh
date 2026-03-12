#!/bin/bash
# Neural Gateway - Inicialização Rápida
# Mantém o gateway ativo e pronto para uso

echo "🧠 ANTIGRAVITY NEURAL GATEWAY"
echo "============================================================"
echo ""

# Verificar se o cérebro existe
if [ ! -f "brain/antigravity-skills-brain.json" ]; then
    echo "❌ Cérebro não encontrado!"
    echo "Execute: python3 extract_skills_brain.py"
    exit 1
fi

# Mostrar status
echo "⚡ Status: SEMPRE ATIVO"
echo ""
echo "📊 Cérebro carregado:"
python3 brain/query_skills.py stats 2>/dev/null | grep -E "(Total|Categorias|Palavras)"
echo ""

# Mostrar últimas ativações (se existir log)
if [ -f "logs/gateway_activations.json" ]; then
    echo "📈 Últimas ativações:"
    python3 -c "
import json
with open('logs/gateway_activations.json') as f:
    data = json.load(f)
    print(f\"  Total ativações: {data['total_activations']}\")
    print(f\"  Skills únicas: {data['unique_skills_activated']}\")
    if data['top_skills']:
        print('  Top skills:')
        for skill, count in data['top_skills'][:5]:
            print(f'    • {skill}: {count}x')
" 2>/dev/null
    echo ""
fi

# Mostrar atalhos
echo "🚀 Comandos rápidos:"
echo "  python3 brain/query_skills.py search 'security'     # Buscar skills"
echo "  python3 neural_gateway_runtime.py dashboard         # Ver dashboard"
echo "  python3 neural_gateway_runtime.py analyze -r '...'  # Analisar request"
echo ""

# Menu interativo (opcional)
echo "O que você quer fazer?"
echo "  1) Ver dashboard completo"
echo "  2) Analisar uma solicitação"
echo "  3) Buscar skills por termo"
echo "  4) Sair"
echo ""
read -p "Escolha (1-4): " choice

case $choice in
    1)
        python3 neural_gateway_runtime.py dashboard
        ;;
    2)
        read -p "Sua solicitação: " request
        python3 neural_gateway_runtime.py analyze --request "$request"
        python3 neural_gateway_runtime.py search --request "$request" --limit 5
        ;;
    3)
        read -p "Termo de busca: " term
        python3 brain/query_skills.py search "$term" --limit 10
        ;;
    4)
        echo "✅ Gateway permanece ativo. Até logo!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Gateway permanece em estado de alerta contínuo."
echo "   Basta fazer sua solicitação normalmente."
