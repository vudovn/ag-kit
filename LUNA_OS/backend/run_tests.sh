#!/bin/bash
# Script para rodar testes unitários - LUNA OS Backend
# Padrão MCT: Rápido, isolado, sem dependências externas

set -e

echo "🧪 LUNA OS - Test Suite"
echo "======================="
echo ""

# Mudar para diretório do backend
cd "$(dirname "$0")"

# Verificar se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest não encontrado. Instalando..."
    pip install pytest pytest-async pytest-mock
fi

# Rodar testes
echo "📍 Diretório: $(pwd)"
echo ""

# Opções
VERBOSE="-v"
COVERAGE=""
SPECIFIC_TEST=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage)
            COVERAGE="--cov=app --cov-report=term-missing"
            shift
            ;;
        --test=*)
            SPECIFIC_TEST="${1#*=}"
            shift
            ;;
        -q|--quiet)
            VERBOSE=""
            shift
            ;;
        *)
            echo "Opção desconhecida: $1"
            echo "Uso: ./run_tests.sh [--coverage] [--test=test_file.py] [-q]"
            exit 1
            ;;
    esac
done

# Build command
CMD="pytest tests $VERBOSE"

if [ -n "$SPECIFIC_TEST" ]; then
    CMD="$CMD tests/$SPECIFIC_TEST"
fi

if [ -n "$COVERAGE" ]; then
    # Verificar se pytest-cov está instalado
    if ! command -v pytest-cov &> /dev/null; then
        echo "⚠️ pytest-cov não encontrado. Instalando..."
        pip install pytest-cov
    fi
    CMD="$CMD $COVERAGE"
fi

echo "🚀 Executando: $CMD"
echo ""

# Executar
eval $CMD

echo ""
echo "✅ Testes completados!"
