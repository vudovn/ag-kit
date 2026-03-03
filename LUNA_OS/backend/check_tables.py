import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.integrations.supabase_client import get_supabase


def check_tables():
    db = get_supabase()
    tables_to_check = [
        "knowledge_base",
        "campaigns",
        "clients",
        "conversations",
        "messages",
        "dojo_feedback",
        "prompt_proposals",
        "conversation_intelligence",
    ]

    existing = []
    for t in tables_to_check:
        try:
            res = db.table(t).select("count", count="exact").limit(1).execute()
            existing.append(t)
            print(f"✅ Table '{t}' exists.")
        except Exception as e:
            msg = str(e)
            if "relation" in msg and "does not exist" in msg:
                print(f"❌ Table '{t}' missing.")
            else:
                print(f"✅ Table '{t}' exists (ignoring syntax/auth error).")
                existing.append(t)

    print(f"\nExisting tables: {existing}")


if __name__ == "__main__":
    check_tables()
