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


async def list_all_tables():
    supabase = get_supabase()

    # RPC or query information_schema if enabled
    # Since we can't do arbitrary SQL through the client easily without an RPC,
    # we can try to use the REST API to query a common system table if allowed

    print("📋 Tentando descobrir tabelas via REST API (Supabase)...")

    # We can try to guess some more common names or just check if there's an RPC
    # But a better way is to check the documentation or previous KIs if they mention the schema.

    # Let's try to query 'knowledge' again but with a different guess
    # Maybe 'brain_knowledge' or something?

    # Alternatively, let's look at how the frontend saves knowledge.
    # Checked earlier: api/knowledge.py use 'knowledge_base'.

    # If knowledge_base is 0, maybe the user wants me to seed it or it's in a different project?
    # No, the user said "Truth in Data preenchida na outra aba".
    # If the user SEES it in the UI, but I see 0 in the DB, there is a mismatch.

    # Let's check `whatsapp_messages_history` sample to see if knowledge is there.
    print("\n🔍 Amostra de whatsapp_messages_history:")
    try:
        res = supabase.table("whatsapp_messages_history").select("*").limit(3).execute()
        print(json.dumps(res.data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import json

    asyncio.run(list_all_tables())
