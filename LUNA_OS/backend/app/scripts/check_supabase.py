import os
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from app.integrations.supabase_client import get_supabase
except ImportError:
    from integrations.supabase_client import get_supabase


async def check_tables():
    supabase = get_supabase()
    tables = [
        "knowledge_base",
        "business_intelligence",
        "clients",
        "messages",
        "conversations",
        "system_settings",
        "knowledge",
        "learnings",
        "learning_log",
        "whatsapp_messages_history",
        "dojo_feedback",
        "campaigns",
    ]

    print("📊 Verificando contagem de linhas por tabela no Supabase:")
    for table in tables:
        try:
            response = (
                supabase.table(table).select("count", count="exact").limit(0).execute()
            )
            count = response.count
            print(f"   • {table}: {count} linhas")
        except Exception as e:
            # print(f"   • {table}: Erro ou Tabela inexistente ({str(e)})")
            # Silently check if it's just missing
            if (
                "search_path" in str(e).lower()
                or "not find the table" in str(e).lower()
            ):
                print(f"   • {table}: Tabela INEXISTENTE")
            else:
                print(f"   • {table}: ERRO -> {str(e)}")


if __name__ == "__main__":
    asyncio.run(check_tables())
