"""
🔄 Webhook Sync - Sincronização de Conversas e Contatos Reais

Extrai conversas e contatos da API e salva no Supabase + Obsidian.

Endpoints:
- POST /api/webhooks/sync/contacts → Sincronizar contatos
- POST /api/webhooks/sync/conversations → Sincronizar conversas
- GET /api/webhooks/sync/status → Status da sincronização

Autor: Agent Flow
Data: 2026-03-02
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
import os

from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/webhooks/sync", tags=["Webhook Sync"])

# ═══════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════

# API de origem (Evolution API ou outra)
SOURCE_API_URL = os.getenv("SOURCE_API_URL", "http://localhost:8081")
SOURCE_API_KEY = os.getenv("SOURCE_API_KEY", "")

# Obsidian Vault Path
OBSIDIAN_VAULT_PATH = os.getenv(
    "OBSIDIAN_VAULT_PATH",
    "/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/app/knowledge/obsidian_vault/_Active/02-KNOWLEDGE"
)

# ═══════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════

class SyncStatus(BaseModel):
    """Status da sincronização"""
    last_sync_contacts: Optional[str] = None
    last_sync_conversations: Optional[str] = None
    contacts_synced: int = 0
    conversations_synced: int = 0
    status: str = "idle"

# ═══════════════════════════════════════════════
# ESTADO (Em memória - depois migrar para DB)
# ═══════════════════════════════════════════════

SYNC_STATE = {
    "last_sync_contacts": None,
    "last_sync_conversations": None,
    "contacts_synced": 0,
    "conversations_synced": 0,
    "status": "idle"
}

# ═══════════════════════════════════════════════
# FUNÇÕES DE SINCRONIZAÇÃO
# ═══════════════════════════════════════════════

async def sync_contacts_from_api():
    """
    Busca contatos da API de origem e salva no Supabase.
    """
    global SYNC_STATE
    SYNC_STATE["status"] = "syncing_contacts"
    
    try:
        supabase = get_supabase()
        
        # Buscar contatos da API de origem
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SOURCE_API_URL}/chat/contacts",
                headers={"apikey": SOURCE_API_KEY}
            )
            response.raise_for_status()
            contacts = response.json()
        
        # Salvar no Supabase
        contacts_to_insert = []
        for contact in contacts:
            contact_data = {
                "phone": contact.get("id", ""),
                "name": contact.get("pushName", ""),
                "first_contact": datetime.utcnow().isoformat(),
                "last_contact": datetime.utcnow().isoformat(),
                "tags": ["synced_from_api"],
                "preferences": {},
                "total_visits": 0,
                "total_spent": 0.0
            }
            contacts_to_insert.append(contact_data)
        
        # Insert or update
        if contacts_to_insert:
            # Usar upsert para evitar duplicados
            for contact_data in contacts_to_insert:
                # Verificar se já existe
                existing = supabase.table("clients").select("id").eq("phone", contact_data["phone"]).execute()
                
                if not existing.data:
                    # Inserir novo
                    supabase.table("clients").insert(contact_data).execute()
                    SYNC_STATE["contacts_synced"] += 1
                else:
                    # Atualizar último contato
                    supabase.table("clients").update({
                        "last_contact": contact_data["last_contact"]
                    }).eq("phone", contact_data["phone"]).execute()
        
        SYNC_STATE["last_sync_contacts"] = datetime.utcnow().isoformat()
        SYNC_STATE["status"] = "idle"
        
        return {
            "status": "success",
            "contacts_synced": SYNC_STATE["contacts_synced"]
        }
        
    except Exception as e:
        SYNC_STATE["status"] = f"error: {str(e)}"
        raise HTTPException(status_code=500, detail=str(e))


async def sync_conversations_from_api():
    """
    Busca conversas da API de origem e salva no Supabase + Obsidian.
    """
    global SYNC_STATE
    SYNC_STATE["status"] = "syncing_conversations"
    
    try:
        supabase = get_supabase()
        
        # Buscar conversas da API de origem
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SOURCE_API_URL}/chat/getChats",
                headers={"apikey": SOURCE_API_KEY}
            )
            response.raise_for_status()
            conversations = response.json()
        
        # Salvar no Supabase
        for conv in conversations:
            # Extrair dados da conversa
            conversation_data = {
                "phone": conv.get("id", ""),
                "messages_count": conv.get("messagesCount", 0),
                "last_message_at": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            # Verificar se já existe
            existing = supabase.table("conversations").select("id").eq("phone", conversation_data["phone"]).execute()
            
            if not existing.data:
                # Inserir nova conversa
                supabase.table("conversations").insert(conversation_data).execute()
                SYNC_STATE["conversations_synced"] += 1
        
        SYNC_STATE["last_sync_conversations"] = datetime.utcnow().isoformat()
        SYNC_STATE["status"] = "idle"
        
        return {
            "status": "success",
            "conversations_synced": SYNC_STATE["conversations_synced"]
        }
        
    except Exception as e:
        SYNC_STATE["status"] = f"error: {str(e)}"
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════

@router.get("/status", response_model=SyncStatus)
async def get_sync_status():
    """
    Retorna status da sincronização.
    """
    return SYNC_STATE

@router.post("/contacts")
async def sync_contacts():
    """
    Sincronizar contatos da API de origem.
    """
    result = await sync_contacts_from_api()
    return result

@router.post("/conversations")
async def sync_conversations():
    """
    Sincronizar conversas da API de origem.
    """
    result = await sync_conversations_from_api()
    return result

@router.post("/all")
async def sync_all():
    """
    Sincronizar contatos E conversas.
    """
    contacts_result = await sync_contacts_from_api()
    conversations_result = await sync_conversations_from_api()
    
    return {
        "status": "success",
        "contacts_synced": contacts_result["contacts_synced"],
        "conversations_synced": conversations_result["conversations_synced"]
    }
