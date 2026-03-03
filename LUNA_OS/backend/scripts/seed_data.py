"""
LUNA OS - Seed Data Script
Popular banco com dados de exemplo para testes e demonstração
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
import random
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.config import settings
from app.integrations.supabase_client import SupabaseClient, create_client

# Dados de exemplo
CLIENTS = [
    {
        "name": "Ana Silva",
        "phone": "5549999111222",
        "email": "ana.silva@email.com",
        "status": "active",
        "notes": "Cliente fiel, vem toda semana",
    },
    {
        "name": "Beatriz Costa",
        "phone": "5549999222333",
        "email": "bia.costa@email.com",
        "status": "active",
        "notes": "Prefere atendimento pela manhã",
    },
    {
        "name": "Carla Oliveira",
        "phone": "5549999333444",
        "email": "carla.oliveira@email.com",
        "status": "active",
        "notes": "Gosta de experimentar serviços novos",
    },
    {
        "name": "Daniela Santos",
        "phone": "5549999444555",
        "email": "dani.santos@email.com",
        "status": "active",
        "notes": "Indicada pela Ana",
    },
    {
        "name": "Eduarda Ferreira",
        "phone": "5549999555666",
        "email": "edu.ferreira@email.com",
        "status": "active",
        "notes": "Primeira vez na Haven",
    },
]

SERVICES = [
    "Escova Simples",
    "Escova Modelada",
    "Manicure",
    "Pedicure",
    "Manicure + Pedicure",
    "Hidratação",
    "Cronograma Capilar",
    "Maquiagem",
    "Sobrancelha",
    "Cílios",
]

INTENTS = [
    "agendamento",
    "preco",
    "horario",
    "localizacao",
    "duvida",
    "elogio",
    "reclamacao",
]

SENTIMENTS = ["positive", "neutral", "negative"]

PROFESSIONALS = [
    "Julia",
    "Mariana",
    "Fernanda",
    "Patricia",
    "Camila",
]


async def seed_database():
    """Popular banco com dados de exemplo"""

    print("🌙 LUNA OS - Seed Data Script")
    print("=" * 50)

    # Initialize Supabase
    try:
        db = create_client(settings.supabase_url, settings.supabase_key)
        print("✅ Supabase conectado")
    except Exception as e:
        print(f"❌ Erro ao conectar no Supabase: {e}")
        return

    # 1. Insert Clients
    print("\n📋 Inserindo clientes...")
    client_ids = []
    for client in CLIENTS:
        try:
            result = db.table("clients").insert(client).execute()
            if result.data:
                client_ids.append(result.data[0]["id"])
                print(f"  ✅ {client['name']}")
        except Exception as e:
            print(f"  ⚠️  {client['name']}: {e}")

    if not client_ids:
        print("⚠️  Nenhum cliente inserido (podem já existir)")
        # Try to get existing clients
        try:
            result = db.table("clients").select("id").limit(5).execute()
            client_ids = [c["id"] for c in result.data or []]
        except:
            pass

    # 2. Insert Conversations
    print("\n💬 Inserindo conversas...")
    conversation_ids = []
    base_date = datetime.now() - timedelta(days=30)

    for i in range(20):
        conv_date = base_date + timedelta(days=random.randint(0, 30))
        client_id = random.choice(client_ids) if client_ids else None

        if not client_id:
            continue

        conversation = {
            "id": str(uuid.uuid4()),
            "client_id": client_id,
            "phone": CLIENTS[i % len(CLIENTS)]["phone"],
            "status": random.choice(["active", "completed", "archived"]),
            "started_at": conv_date.isoformat(),
            "last_message_at": (conv_date + timedelta(hours=random.randint(1, 48))).isoformat(),
            "source": "whatsapp",
        }

        try:
            result = db.table("conversations").insert(conversation).execute()
            if result.data:
                conversation_ids.append(result.data[0]["id"])
                print(f"  ✅ Conversa {i+1}/20")
        except Exception as e:
            print(f"  ⚠️  Conversa {i+1}: {e}")

    # 3. Insert Messages
    print("\n📨 Inserindo mensagens...")
    message_count = 0

    SAMPLE_MESSAGES = [
        "Oi! Gostaria de agendar um horário",
        "Qual o valor da escova modelada?",
        "Vocês atendem domingo?",
        "Onde fica o salão?",
        "Quero fazer manicure e pedicure",
        "Tem horário para hoje às 15h?",
        "Adorei o atendimento!",
        "Posso pagar com cartão?",
        "Demorou para responder 😕",
        "Obrigada, ficou perfeito!",
    ]

    for conv_id in conversation_ids[:10]:
        # Get client info for this conversation
        conv_result = db.table("conversations").select("client_id, phone").eq("id", conv_id).execute()
        if not conv_result.data:
            continue

        client_id = conv_result.data[0].get("client_id")
        phone = conv_result.data[0].get("phone")

        # Insert 3-8 messages per conversation
        num_messages = random.randint(3, 8)
        for j in range(num_messages):
            is_inbound = j % 2 == 0
            msg_text = random.choice(SAMPLE_MESSAGES)

            message = {
                "id": str(uuid.uuid4()),
                "conversation_id": conv_id,
                "client_id": client_id,
                "phone": phone,
                "direction": "inbound" if is_inbound else "outbound",
                "content": msg_text,
                "intent": random.choice(INTENTS) if is_inbound else None,
                "sentiment": random.choice(SENTIMENTS) if is_inbound else None,
                "created_at": (base_date + timedelta(days=random.randint(0, 30), hours=random.randint(8, 20))).isoformat(),
            }

            try:
                db.table("messages").insert(message).execute()
                message_count += 1
            except Exception as e:
                pass

    print(f"  ✅ {message_count} mensagens inseridas")

    # 4. Insert Appointments
    print("\n📅 Inserindo agendamentos...")
    appointment_count = 0

    for i in range(15):
        appt_date = base_date + timedelta(days=random.randint(0, 60))
        client_id = random.choice(client_ids) if client_ids else None

        if not client_id:
            continue

        appointment = {
            "id": str(uuid.uuid4()),
            "client_id": client_id,
            "phone": CLIENTS[i % len(CLIENTS)]["phone"],
            "service": random.choice(SERVICES),
            "professional": random.choice(PROFESSIONALS),
            "scheduled_for": appt_date.isoformat(),
            "status": random.choice(["scheduled", "completed", "cancelled", "no_show"]),
            "notes": "Agendamento via WhatsApp",
        }

        try:
            db.table("appointments").insert(appointment).execute()
            appointment_count += 1
            print(f"  ✅ Agendamento {i+1}/15")
        except Exception as e:
            print(f"  ⚠️  Agendamento {i+1}: {e}")

    print(f"  ✅ {appointment_count} agendamentos inseridos")

    # 5. Insert Knowledge Base Items
    print("\n📚 Inserindo base de conhecimento...")
    knowledge_items = [
        {
            "id": str(uuid.uuid4()),
            "category": "services",
            "key": "Serviços Oferecidos",
            "data": {
                "services": [
                    {"name": "Escova Simples", "price": 35, "duration": 30},
                    {"name": "Escova Modelada", "price": 50, "duration": 45},
                    {"name": "Manicure", "price": 30, "duration": 30},
                    {"name": "Pedicure", "price": 35, "duration": 30},
                    {"name": "Manicure + Pedicure", "price": 60, "duration": 60},
                    {"name": "Hidratação", "price": 45, "duration": 30},
                    {"name": "Cronograma Capilar", "price": 120, "duration": 90},
                    {"name": "Maquiagem", "price": 80, "duration": 45},
                    {"name": "Sobrancelha", "price": 25, "duration": 15},
                    {"name": "Cílios", "price": 40, "duration": 30},
                ]
            },
            "source": "seed",
        },
        {
            "id": str(uuid.uuid4()),
            "category": "business",
            "key": "Informações do Negócio",
            "data": {
                "name": "Haven Escovaria & Esmalteria",
                "hours": "Segunda a Sábado, 8h às 20h",
                "address": "Rua Mato Grosso, 837E - Jardim Itália, Chapecó - SC",
                "phone": "(49) 99999-9999",
                "instagram": "@haven.escovaria",
            },
            "source": "seed",
        },
        {
            "id": str(uuid.uuid4()),
            "category": "faq",
            "key": "Perguntas Frequentes",
            "data": {
                "questions": [
                    {"q": "Aceita cartão?", "a": "Sim! Aceitamos cartão de crédito, débito e PIX."},
                    {"q": "Precisa agendar?", "a": "Recomendamos agendamento para garantir seu horário."},
                    {"q": "Tem estacionamento?", "a": "Sim, temos estacionamento gratuito para clientes."},
                    {"q": "Atendem domingo?", "a": "Não, funcionamos de segunda a sábado."},
                ]
            },
            "source": "seed",
        },
    ]

    for item in knowledge_items:
        try:
            db.table("knowledge_base").insert(item).execute()
            print(f"  ✅ {item['key']}")
        except Exception as e:
            print(f"  ⚠️  {item['key']}: {e}")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Seed data concluído!")
    print(f"   - Clientes: {len(client_ids)}")
    print(f"   - Conversas: {len(conversation_ids)}")
    print(f"   - Mensagens: {message_count}")
    print(f"   - Agendamentos: {appointment_count}")
    print(f"   - Knowledge items: {len(knowledge_items)}")
    print("\n🌙 Luna está pronta para demonstração!")


if __name__ == "__main__":
    asyncio.run(seed_database())
