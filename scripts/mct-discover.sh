#!/bin/bash
# Antigravity Meta-Broker Shell Wrapper
# Facilita a execução da descoberta de ferramentas MCP

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🌌 Iniciando Descoberta Dinâmica de Ferramentas (Meta-Broker)..."

# Executa o script python
python3 "$SCRIPT_DIR/mcp-discover.py"

echo "✨ Descoberta concluída."
