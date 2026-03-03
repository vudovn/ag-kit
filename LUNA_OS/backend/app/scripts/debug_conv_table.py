"""
Debug Supabase Conversations Table
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


def debug_table():
    print(f"🔍 Auditando tabela 'conversations' em {url}")

    # 1. Tentar buscar uma linha para ver as colunas
    try:
        res = supabase.table("conversations").select("*").limit(1).execute()
        if res.data:
            print("\n✅ Colunas detectadas:")
            for k in res.data[0].keys():
                print(f"   - {k}")

            print("\n✅ Dados da última conversa:")
            print(res.data[0])
        else:
            print("\n⚠️ Tabela vazia ou sem acesso.")

    except Exception as e:
        print(f"\n❌ Erro ao acessar 'conversations': {e}")


if __name__ == "__main__":
    debug_table()
