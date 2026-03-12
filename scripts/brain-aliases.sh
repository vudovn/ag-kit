#!/bin/bash
# 🚀 Antigravity Core - Atalhos de Terminal
# Adicione ao seu ~/.zshrc ou ~/.bashrc:
#   source /caminho/para/antigravity-kit/scripts/brain-aliases.sh

# Detectar diretório base automaticamente
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Define MCT_KIT_DIR for new aliases
MCT_KIT_DIR="$BASE_DIR"

# Navegação
alias mct='cd "$BASE_DIR"'

# Projetos
alias mct-init='"$BASE_DIR/scripts/init-project.sh"'
alias mct-list="bash $MCT_KIT_DIR/scripts/mct-list.sh"
alias mct-sync="bash $MCT_KIT_DIR/scripts/mct-sync.sh"
alias mct-brain="python3 $MCT_KIT_DIR/brain/query_skills.py"
alias mct-discover="bash $MCT_KIT_DIR/scripts/mct-discover.sh"
alias mct-runtime="python3 $MCT_KIT_DIR/brain/runtime.py"

# Stats (This alias was partially shown in the instruction, assuming it's removed or changed)
# alias mct-stats='python3 "$BASE_DIR/brain/query_skills.py stats"'

# Mensagem de boas-vindas (opcional)
if [ -t 1 ]; then
    echo "🧠 Antigravity Core carregado!"
    echo ""
    echo "Comandos:"
    echo "  mct-init [nome]  - Criar novo projeto"
    echo "  mct-list         - Listar projetos"
    echo "  mct-brain [term] - Buscar skills"
    echo "  mct-stats        - Ver estatísticas do Brain"
    echo "  mct              - Ir para antigravity-kit"
    echo ""
fi
