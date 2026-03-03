#!/bin/bash
# LUNA OS - Sovereign Sync Daemon
# Este script roda o sincronizador Obsidian em loop, ideal para rodar em background via tmux, pm2 ou launchd.

INTERVAL=3600 # Intervalo em segundos (3600 = 60 minutos)

echo "🤖 [LUNA OS] Iniciando Continuous Brain Sync Daemon..."
echo "⏱️  Intervalo de atualização configurado: $(($INTERVAL / 60)) minutos."

# Pegar o diretório raiz do backend
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BACKEND_DIR="$( dirname "$( dirname "$DIR" )" )"

cd "$BACKEND_DIR" || exit 1

# Ativar virtualenv se existir
if [ -f "venv/bin/activate" ]; then
    source "venv/bin/activate"
fi

export PYTHONPATH="$BACKEND_DIR"

while true; do
  echo "⏳ [$(date '+%Y-%m-%d %H:%M:%S')] Executando sincronização Supabase -> Obsidian..."
  
  python3 app/scripts/obsidian_sync.py > /tmp/luna_sync_last.log 2>&1
  
  if [ $? -eq 0 ]; then
      echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] Sync concluído com sucesso."
  else
      echo "⚠️ [$(date '+%Y-%m-%d %H:%M:%S')] Algo falhou durante o sync. Cheque /tmp/luna_sync_last.log"
  fi
  
  echo "💤 Próxima extração em $(($INTERVAL / 60)) minutos..."
  sleep $INTERVAL
done
