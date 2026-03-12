#!/bin/bash
# 🔄 sync-context.sh - Consolida contexto completo para IA

NAME=$1
if [ -z "$NAME" ]; then
    echo "❌ Erro: Informe o nome do projeto."
    exit 1
fi

PROJECT_DIR="/Users/franciscotaveira.ads/Documents/antigravity-kit/projects/$NAME"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Erro: Projeto '$NAME' não encontrado."
    exit 1
fi

echo "🔄 Sincronizando contexto Soberano: $NAME..."

MASTER_FILE="$PROJECT_DIR/MCT-MASTER-DIRECTIVE.md"

# Coletar informações
CHARTER_PATH="$PROJECT_DIR/PROJECT_CHARTER.md"
CODEBASE_PATH="$PROJECT_DIR/CODEBASE.md"

cat > "$MASTER_FILE" <<EOF
# 📜 MCT MASTER DIRECTIVE — $NAME

> [!IMPORTANT]
> Este arquivo é a ÚNICA fonte de verdade para a IA. Leia-o antes de qualquer ação.

## 🏛️ Constituição (Charter)
$(cat "$CHARTER_PATH" 2>/dev/null || echo "Charter não definido.")

## 🗺️ Mapa Atual (Codebase)
$(cat "$CODEBASE_PATH" 2>/dev/null || echo "Codebase não mapeado.")

## 🛠️ Notas de Execução
- Use 'mct-brain' se precisar de playbooks extras.
- Mantenha a modularidade descrita no Charter.

EOF

echo "✨ Master Directive atualizado com sucesso!"
