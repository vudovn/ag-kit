"""Clients API - Padrão Elite MCT"""

from fastapi import APIRouter, HTTPException
from typing import List
from loguru import logger
from app.integrations.supabase_client import get_supabase
from app.schemas import ClientRead

router = APIRouter()


@router.get("", response_model=List[ClientRead])
@router.get("/", response_model=List[ClientRead])
async def list_clients(limit: int = 50):
    logger.info(f"Listando clientes (limit={limit})")
    db = get_supabase()

    try:
        clients_data = (
            db.table("clients")
            .select("*, conversations(count)")
            .order("last_contact", desc=True)
            .limit(limit)
            .execute()
            .data
            or []
        )

        # Flatten conversation_count
        for c in clients_data:
            conv = c.pop("conversations", [])
            c["conversation_count"] = conv[0]["count"] if conv else 0

        return clients_data
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {e}")
        raise HTTPException(
            status_code=500, detail="Erro ao recuperar base de clientes"
        )


@router.get("/{client_id}")
async def get_client(client_id: str):
    logger.info(f"Buscando perfil completo do cliente {client_id}")
    db = get_supabase()

    try:
        client = db.table("clients").select("*").eq("id", client_id).execute()
        if not client.data:
            logger.warning(f"Cliente {client_id} não encontrado")
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        conversations = (
            db.table("conversations")
            .select("*")
            .eq("client_id", client_id)
            .order("started_at", desc=True)
            .limit(20)
            .execute()
        )

        try:
            appointments = (
                db.table("appointments")
                .select("*")
                .eq("client_id", client_id)
                .order("date", desc=True)
                .limit(20)
                .execute()
            )
            appts_data = appointments.data or []
        except Exception as e:
            logger.warning(
                f"Erro ao buscar appointments (tabela pode não existir): {e}"
            )
            appts_data = []

        return {
            "client": client.data[0],
            "conversations": conversations.data or [],
            "appointments": appts_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes do cliente {client_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Falha ao processar dossiê do cliente"
        )
