import asyncio
from app.integrations.supabase_client import get_supabase

async def check_db():
    db = get_supabase()
    
    convs = db.table("conversations").select("id", count="exact").execute()
    msgs = db.table("messages").select("id", count="exact").execute()
    # Check if there is an insights table or similar, if not check knowledge_base
    kb = db.table("knowledge_base").select("id", count="exact").execute()
    
    print(f"Total Conversations: {convs.count}")
    print(f"Total Messages: {msgs.count}")
    print(f"Total Knowledge Items: {kb.count}")

asyncio.run(check_db())
