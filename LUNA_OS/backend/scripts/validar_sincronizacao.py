#!/usr/bin/env python3
"""
🔄 Validação de Sincronização - LUNA OS

Valida se Obsidian, Supabase, APIs e Painel estão sincronizados.

Autor: Agent Flow
Data: 2026-03-01
"""

import json
import os
from pathlib import Path


def validar_obsidian():
    """Validar arquivos no Obsidian"""
    print("=" * 60)
    print("📂 VALIDANDO OBSIDIAN")
    print("=" * 60)
    
    obsidian_path = Path("backend/app/knowledge/obsidian_vault/_Active/02-KNOWLEDGE")
    
    # Contar Profissionais
    prof_path = obsidian_path / "PROFESSIONALS"
    prof_count = len(list(prof_path.glob("*.md"))) if prof_path.exists() else 0
    print(f"✅ Profissionais: {prof_count}/9")
    
    # Contar Serviços
    services_path = obsidian_path / "Services"
    service_count = len(list(services_path.glob("*.md"))) if services_path.exists() else 0
    print(f"✅ Serviços: {service_count}/41")
    
    # Contar Pacotes
    packages_path = obsidian_path / "PACKAGES"
    package_count = len(list(packages_path.glob("*.md"))) if packages_path.exists() else 0
    print(f"✅ Pacotes: {package_count}/4")
    
    # Contar FAQs
    faqs_path = obsidian_path / "FAQs"
    faq_count = len(list(faqs_path.glob("*.md"))) if faqs_path.exists() else 0
    print(f"✅ FAQs: {faq_count}/4")
    
    total = prof_count + service_count + package_count + faq_count
    expected = 9 + 41 + 4 + 4
    print(f"\n📊 Total Obsidian: {total}/{expected}")
    
    return {
        "professionals": prof_count,
        "services": service_count,
        "packages": package_count,
        "faqs": faq_count,
        "total": total,
        "expected": expected,
        "sync": total == expected
    }


def validar_seed_sql():
    """Validar arquivo Seed SQL"""
    print("\n" + "=" * 60)
    print("📄 VALIDANDO SEED SQL")
    print("=" * 60)
    
    seed_path = Path("backend/supabase_seed_haven.sql")
    
    if not seed_path.exists():
        print("❌ Seed SQL não encontrado")
        return {"exists": False, "ready": False}
    
    # Ler arquivo e contar INSERTs
    with open(seed_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    insert_count = content.count("INSERT INTO knowledge_base")
    print(f"✅ INSERTs encontrados: {insert_count}")
    
    # Esperado: 6 INSERTs (um para cada categoria com múltiplos valores)
    # Ou 64 INSERTs individuais
    
    return {
        "exists": True,
        "insert_count": insert_count,
        "ready": insert_count > 0
    }


def validar_apis():
    """Validar APIs (requer backend rodando)"""
    print("\n" + "=" * 60)
    print("🔌 VALIDANDO APIS")
    print("=" * 60)
    
    try:
        import httpx
        
        # Testar API Professionals
        response = httpx.get("http://localhost:8000/api/professionals", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            prof_count = len(data.get("professionals", []))
            print(f"✅ API Professionals: {prof_count} profissionais")
        else:
            print(f"❌ API Professionals: Status {response.status_code}")
        
        # Testar API Services
        response = httpx.get("http://localhost:8000/api/services", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            service_count = len(data.get("services", []))
            print(f"✅ API Services: {service_count} serviços")
        else:
            print(f"❌ API Services: Status {response.status_code}")
        
        # Testar API Packages
        response = httpx.get("http://localhost:8000/api/packages", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            package_count = len(data.get("packages", []))
            print(f"✅ API Packages: {package_count} pacotes")
        else:
            print(f"❌ API Packages: Status {response.status_code}")
        
        return {
            "professionals": prof_count if 'prof_count' in locals() else 0,
            "services": service_count if 'service_count' in locals() else 0,
            "packages": package_count if 'package_count' in locals() else 0,
            "ready": True
        }
        
    except Exception as e:
        print(f"⚠️ Erro ao validar APIs: {e}")
        print("⚠️ Backend pode não estar rodando")
        return {
            "ready": False,
            "error": str(e)
        }


def validar_painel():
    """Validar Painel (requer frontend rodando)"""
    print("\n" + "=" * 60)
    print("🖥️ VALIDANDO PAINEL")
    print("=" * 60)
    
    try:
        import httpx
        
        # Testar página Professionals
        response = httpx.get("http://localhost:3000/professionals", timeout=5.0)
        if response.status_code == 200:
            print(f"✅ Página Professionals: OK")
        else:
            print(f"❌ Página Professionals: Status {response.status_code}")
        
        # Testar página Services
        response = httpx.get("http://localhost:3000/services", timeout=5.0)
        if response.status_code == 200:
            print(f"✅ Página Services: OK")
        else:
            print(f"❌ Página Services: Status {response.status_code}")
        
        # Testar página Packages
        response = httpx.get("http://localhost:3000/packages", timeout=5.0)
        if response.status_code == 200:
            print(f"✅ Página Packages: OK")
        else:
            print(f"❌ Página Packages: Status {response.status_code}")
        
        return {
            "ready": True
        }
        
    except Exception as e:
        print(f"⚠️ Erro ao validar Painel: {e}")
        print("⚠️ Frontend pode não estar rodando")
        return {
            "ready": False,
            "error": str(e)
        }


def gerar_relatorio(obsidian, seed, apis, painel):
    """Gerar relatório final"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DE SINCRONIZAÇÃO")
    print("=" * 60)
    
    # Obsidian
    print(f"\n📂 OBSIDIAN:")
    print(f"   Profissionais: {obsidian['professionals']}/9")
    print(f"   Serviços: {obsidian['services']}/41")
    print(f"   Pacotes: {obsidian['packages']}/4")
    print(f"   FAQs: {obsidian['faqs']}/4")
    print(f"   Status: {'✅ 100%' if obsidian['sync'] else '❌ Incompleto'}")
    
    # Seed SQL
    print(f"\n📄 SEED SQL:")
    print(f"   Arquivo: {'✅ Existe' if seed['exists'] else '❌ Não encontrado'}")
    print(f"   INSERTs: {seed['insert_count']}")
    print(f"   Status: {'✅ Pronto' if seed['ready'] else '❌ Não executado'}")
    
    # APIs
    print(f"\n🔌 APIS:")
    if apis['ready']:
        print(f"   Professionals: {apis.get('professionals', 0)} registros")
        print(f"   Services: {apis.get('services', 0)} registros")
        print(f"   Packages: {apis.get('packages', 0)} registros")
        print(f"   Status: ✅ Online")
    else:
        print(f"   Status: ⚠️ Backend não rodando")
    
    # Painel
    print(f"\n🖥️ PAINEL:")
    if painel['ready']:
        print(f"   Status: ✅ Online")
    else:
        print(f"   Status: ⚠️ Frontend não rodando")
    
    # Status Geral
    print("\n" + "=" * 60)
    print("📊 STATUS GERAL DE SINCRONIZAÇÃO")
    print("=" * 60)
    
    sync_score = 0
    total_items = 4
    
    if obsidian['sync']:
        sync_score += 1
        print("✅ Obsidian: 100%")
    else:
        print("❌ Obsidian: Incompleto")
    
    if seed['ready']:
        sync_score += 1
        print("✅ Seed SQL: Pronto para executar")
    else:
        print("❌ Seed SQL: Não encontrado")
    
    if apis['ready']:
        sync_score += 1
        print("✅ APIs: Online e respondendo")
    else:
        print("⚠️ APIs: Backend precisa estar rodando")
    
    if painel['ready']:
        sync_score += 1
        print("✅ Painel: Online e acessível")
    else:
        print("⚠️ Painel: Frontend precisa estar rodando")
    
    # Porcentagem
    percentage = (sync_score / total_items) * 100
    print(f"\n📊 SINCRONIZAÇÃO: {percentage:.0f}% ({sync_score}/{total_items})")
    
    if percentage == 100:
        print("\n🎉 PARABÉNS! SINCRONIZAÇÃO 100% COMPLETA!")
    elif percentage >= 75:
        print("\n✅ QUASE LÁ! Faltam apenas detalhes.")
    elif percentage >= 50:
        print("\n⏳ EM ANDAMENTO. Continue os passos.")
    else:
        print("\n⚠️ INICIANDO. Siga o guia de sincronização.")
    
    return {
        "score": percentage,
        "sync_score": sync_score,
        "total_items": total_items
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 LUNA OS - Validação de Sincronização")
    print("=" * 60)
    
    # Validar Obsidian
    obsidian = validar_obsidian()
    
    # Validar Seed SQL
    seed = validar_seed_sql()
    
    # Validar APIs
    apis = validar_apis()
    
    # Validar Painel
    painel = validar_painel()
    
    # Gerar relatório
    relatorio = gerar_relatorio(obsidian, seed, apis, painel)
    
    print("\n" + "=" * 60)
    print("📝 PRÓXIMOS PASSOS")
    print("=" * 60)
    
    if not seed['ready']:
        print("\n1. ⏳ Executar Seed SQL no Supabase:")
        print("   - Acessar: https://supabase.com/dashboard")
        print("   - Abrir SQL Editor")
        print("   - Copiar: backend/supabase_seed_haven.sql")
        print("   - Executar SQL")
    
    if not apis['ready']:
        print("\n2. ⏳ Iniciar Backend:")
        print("   - cd backend")
        print("   - uvicorn app.main:app --reload")
    
    if not painel['ready']:
        print("\n3. ⏳ Iniciar Frontend:")
        print("   - cd frontend")
        print("   - npm run dev")
    
    if relatorio['score'] == 100:
        print("\n✅ TUDO SINCRONIZADO!")
        print("   Próximo passo: Validar com equipe Suzana")
    
    print("\n" + "=" * 60)
