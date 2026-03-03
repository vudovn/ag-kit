import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.supabase_client import get_supabase
from loguru import logger


def apply_schema():
    logger.info("🌙 Iniciando aplicação do Schema de Histórico...")
    db = get_supabase()

    schema_path = Path(__file__).parent / "history_schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Infelizmente o cliente Supabase Python não tem um método .sql() direto para comandos arbitrários
    # Mas podemos usar rpc se houver uma função exec_sql definida, ou tentaremos via terminal se possível.
    # Como não temos exec_sql, vamos informar que o schema está pronto para ser aplicado via Dashboard
    # ou tentaremos rodar cada comando se soubermos os métodos.

    print("\n⚠️ O Schema de Histórico foi gerado!")
    print(f"📍 Local: {schema_path}")
    print("\nPor favor, execute o conteúdo deste arquivo no SQL Editor do Supabase.")


if __name__ == "__main__":
    apply_schema()
