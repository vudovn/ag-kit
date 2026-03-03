import asyncio
from app.integrations.supabase_client import get_supabase

async def check_db():
    db = get_supabase()
    try:
        res = db.table("whatsapp_messages_history").select("id", count="exact").limit(1).execute()
        print("Table whatsapp_messages_history exists.", res.count)
    except Exception as e:
        print("Error checking whatsapp_messages_history:", e)

asyncio.run(check_db())
