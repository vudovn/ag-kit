#!/usr/bin/env python3
"""
🌙 Seed Haven - Popular Supabase com Dados Oficiais

Este script popula o Supabase com:
- Todos os 41 serviços
- 9 profissionais
- 5 cupons de blogueiras
- 4 FAQs
- Pacotes e upsells

Autor: Agent Flow
Data: 2026-03-01
"""

import os
import sys
import json
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from app.core.config_haven import (
    PROFISSIONAIS,
    SERVICOS,
    CUPONS,
    PACOTES,
    HORARIOS_FUNCIONAMENTO,
    ENDERECO,
)


def load_haven_json() -> dict:
    """Carrega dados do haven.json"""
    # Tentar caminhos diferentes para maior robustez
    possibilities = [
        backend_path / "app" / "knowledge" / "data" / "haven.json",
        backend_path / "knowledge" / "data" / "haven.json",
        Path("/app/app/knowledge/data/haven.json"),
        Path("backend/app/knowledge/data/haven.json"),
    ]

    haven_path = None
    for p in possibilities:
        if p.exists():
            haven_path = p
            break

    if not haven_path:
        raise FileNotFoundError(
            f"Não foi possível encontrar haven.json em nenhuma das localizações: {possibilities}"
        )

    with open(haven_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_services(supabase, haven_data: dict):
    """Popular tabela de serviços"""
    print("📊 Seed services...")

    services = haven_data.get("services", [])

    for service in services:
        try:
            # Verificar se já existe
            existing = (
                supabase.table("knowledge_base")
                .select("id")
                .eq("key", f"service_{service['id']}")
                .execute()
            )

            if existing.data:
                print(f"  ⏭️  Service {service['id']} já existe")
                continue

            # Inserir serviço
            data = {
                "category": "services",
                "key": f"service_{service['id']}",
                "data": service,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ Service {service['id']} criado")

        except Exception as e:
            print(f"  ❌ Erro service {service['id']}: {e}")

    print(f"✅ {len(services)} services seeds\n")


def seed_professionals(supabase, haven_data: dict):
    """Popular tabela de profissionais"""
    print("👩‍🦱 Seed professionals...")

    professionals = haven_data.get("professionals", [])

    for prof in professionals:
        try:
            # Verificar se já existe
            existing = (
                supabase.table("knowledge_base")
                .select("id")
                .eq("key", f"professional_{prof['id']}")
                .execute()
            )

            if existing.data:
                print(f"  ⏭️  Professional {prof['id']} já existe")
                continue

            # Inserir profissional
            data = {
                "category": "professionals",
                "key": f"professional_{prof['id']}",
                "data": prof,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ Professional {prof['id']} criado")

        except Exception as e:
            print(f"  ❌ Erro professional {prof['id']}: {e}")

    print(f"✅ {len(professionals)} professionals seeds\n")


def seed_coupons(supabase, haven_data: dict):
    """Popular tabela de cupons"""
    print("🎟️  Seed coupons...")

    coupons = haven_data.get("coupons", [])

    for coupon in coupons:
        try:
            # Verificar se já existe
            existing = (
                supabase.table("knowledge_base")
                .select("id")
                .eq("key", f"coupon_{coupon['code']}")
                .execute()
            )

            if existing.data:
                print(f"  ⏭️  Coupon {coupon['code']} já existe")
                continue

            # Inserir cupom
            data = {
                "category": "coupons",
                "key": f"coupon_{coupon['code']}",
                "data": coupon,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ Coupon {coupon['code']} criado")

        except Exception as e:
            print(f"  ❌ Erro coupon {coupon['code']}: {e}")

    print(f"✅ {len(coupons)} coupons seeds\n")


def seed_packages(supabase, haven_data: dict):
    """Popular tabela de pacotes"""
    print("📦 Seed packages...")

    packages = haven_data.get("packages", [])

    for package in packages:
        try:
            # Verificar se já existe
            existing = (
                supabase.table("knowledge_base")
                .select("id")
                .eq("key", f"package_{package['id']}")
                .execute()
            )

            if existing.data:
                print(f"  ⏭️  Package {package['id']} já existe")
                continue

            # Inserir pacote
            data = {
                "category": "packages",
                "key": f"package_{package['id']}",
                "data": package,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ Package {package['id']} criado")

        except Exception as e:
            print(f"  ❌ Erro package {package['id']}: {e}")

    print(f"✅ {len(packages)} packages seeds\n")


def seed_faqs(supabase):
    """Popular tabela de FAQs"""
    print("❓ Seed FAQs...")

    faqs = [
        {
            "id": "horario_funcionamento",
            "question": "Qual o horário de funcionamento?",
            "answer": "Atendemos de segunda a sábado, das 8h às 20h, sem pausa para almoço!",
            "category": "geral",
        },
        {
            "id": "precisa_agendar",
            "question": "Precisa agendar?",
            "answer": "Sim! Trabalhamos somente com horário agendado para melhor atendê-la.",
            "category": "geral",
        },
        {
            "id": "aceita_cartao",
            "question": "Aceita cartão?",
            "answer": "Sim! Aceitamos cartão de crédito, débito e PIX. Parcelamos no crédito em até 3x sem juros.",
            "category": "pagamento",
        },
        {
            "id": "tem_estacionamento",
            "question": "Tem estacionamento?",
            "answer": "Temos estacionamento em frente ao salão e também 4 vagas na esquina!",
            "category": "localizacao",
        },
    ]

    for faq in faqs:
        try:
            # Verificar se já existe
            existing = (
                supabase.table("knowledge_base")
                .select("id")
                .eq("key", f"faq_{faq['id']}")
                .execute()
            )

            if existing.data:
                print(f"  ⏭️  FAQ {faq['id']} já existe")
                continue

            # Inserir FAQ
            data = {
                "category": "faqs",
                "key": f"faq_{faq['id']}",
                "data": faq,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ FAQ {faq['id']} criado")

        except Exception as e:
            print(f"  ❌ Erro FAQ {faq['id']}: {e}")

    print(f"✅ {len(faqs)} FAQs seeds\n")


def seed_business_info(supabase):
    """Popular informações do negócio"""
    print("🏠 Seed business info...")

    try:
        business_data = {
            "name": "Haven Escovaria & Esmalteria",
            "address": ENDERECO,
            "hours": HORARIOS_FUNCIONAMENTO,
            "parking": "Estacionamento em frente + 4 vagas na esquina",
            "coordinates": {"lat": -27.0922, "lng": -52.6158},
        }

        # Verificar se já existe
        existing = (
            supabase.table("knowledge_base")
            .select("id")
            .eq("key", "business_info")
            .execute()
        )

        if existing.data:
            print(f"  ⏭️  Business info já existe")
        else:
            data = {
                "category": "business",
                "key": "business_info",
                "data": business_data,
                "is_active": True,
            }

            result = supabase.table("knowledge_base").insert(data).execute()
            print(f"  ✅ Business info criado")

        print(f"✅ Business info seed\n")

    except Exception as e:
        print(f"  ❌ Erro business info: {e}\n")


def main():
    """Função principal"""
    print("=" * 60)
    print("🌙 LUNA OS - Seed Haven")
    print("Popular Supabase com dados oficiais da Haven")
    print("=" * 60)
    print()

    # Conectar ao Supabase
    print("🔗 Conectando ao Supabase...")
    try:
        supabase = get_supabase()
        print("✅ Conectado!\n")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return

    # Carregar dados do haven.json
    print("📄 Carregando haven.json...")
    try:
        haven_data = load_haven_json()
        print(f"✅ {len(haven_data.get('services', []))} serviços carregados")
        print(f"✅ {len(haven_data.get('professionals', []))} profissionais carregados")
        print(f"✅ {len(haven_data.get('coupons', []))} cupons carregados")
        print(f"✅ {len(haven_data.get('packages', []))} pacotes carregados")
        print()
    except Exception as e:
        print(f"❌ Erro ao carregar haven.json: {e}")
        return

    # Executar seeds
    print("🚀 Executando seeds...\n")

    seed_services(supabase, haven_data)
    seed_professionals(supabase, haven_data)
    seed_coupons(supabase, haven_data)
    seed_packages(supabase, haven_data)
    seed_faqs(supabase)
    seed_business_info(supabase)

    print("=" * 60)
    print("✅ Seed Haven completado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
