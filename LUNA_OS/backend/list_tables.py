import os
import sys

# Add backend directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.integrations.supabase_client import get_supabase


def list_tables():
    db = get_supabase()
    # Para obter as tabelas do schema public usando supabase python client
    # A API RPC ou uma query no postgrest não permite consultar information_schema facilmente
    # Mas podemos tentar via edge function ou rest se exposto, ou verificar se funciona.
    # Outra forma é verificar o status de RLS num log ou tentando habilitar.

    # Vamos tentar pegar information_schema, mas geralmente o anon key nao tem acesso.
    # O backend usa a do root/service_role
    try:
        # Tivemos problemas anteriormente consultando information_schema usando a REST API
        # Supabase API REST por padrao nao expoe information_schema.
        pass
    except Exception as e:
        print(e)


if __name__ == "__main__":
    list_tables()
