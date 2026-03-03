#!/bin/bash
# bootstrap.sh - Prepara o ambiente Kimi-Dev

set -e

echo "🚀 Iniciando ambiente Kimi-Dev..."

# Verificar se repo_structures está vazio e baixar se necessário
if [ -z "$(ls -A /app/repo_structures)" ]; then
    echo "📦 Baixando estruturas de repositório (SWE-bench)..."
    curl -L "https://drive.google.com/file/d/15-4XjTmY48ystrsc_xcvtOkMs3Fx8RoW/view" -o /tmp/repo_structure.zip || echo "⚠️ Aviso: Download direto do GDrive via curl falhou. Configure manualmente em /app/repo_structures."
    # unzip /tmp/repo_structure.zip -d /app/repo_structures
fi

echo "✅ Ambiente pronto. Use 'docker exec' para rodar os comandos do Kimi-Dev."

# Mantém o container vivo
tail -f /dev/null
