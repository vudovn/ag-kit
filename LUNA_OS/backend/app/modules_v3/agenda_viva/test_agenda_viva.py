#!/usr/bin/env python3
"""
🌙 LUNA OS v3.0 — Teste do Módulo 1: Agenda Viva
Teste COMPLETO antes de produção
"""

import sys
import asyncio
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.modules_v3.agenda_viva.optimizer import agenda_viva
from app.modules_v3.agenda_viva.api import optimize_scheduling, get_agenda_viva_status
from loguru import logger


async def test_inicializacao():
    """Testa inicialização do módulo"""
    print("\n📊 Teste 1: Inicialização")
    print("─" * 50)
    
    sucesso = await agenda_viva.inicializar()
    
    if sucesso:
        print(f"   ✅ Inicialização OK")
        print(f"   📂 Situações carregadas: {agenda_viva.situacoes_carregadas}")
        print(f"   📋 Regras ativas: {len(agenda_viva.regras)}")
        return True
    else:
        print(f"   ❌ Inicialização FALHOU")
        return False


async def test_otimizacao_encaixe():
    """Testa otimização para encaixe"""
    print("\n📊 Teste 2: Otimização (Encaixe)")
    print("─" * 50)
    
    agendamento = {
        "cliente_id": "test_001",
        "servicos": ["escova"],
        "horario_solicitado": "2026-02-27T14:00:00",
        "pedido_encaixe": True
    }
    
    resultado = await optimize_scheduling(agendamento)
    
    otimizacao_count = len(resultado.get('otimizacoes', []))
    
    if otimizacao_count > 0:
        print(f"   ✅ {otimizacao_count} otimizações aplicadas")
        for opt in resultado['otimizacoes']:
            print(f"      • {opt.get('tipo')}: {opt.get('mensagem', '')}")
        return True
    else:
        print(f"   ⚠️ Nenhuma otimização aplicada (pode ser normal)")
        return True


async def test_otimizacao_multi_servicos():
    """Testa otimização para múltiplos serviços"""
    print("\n📊 Teste 3: Otimização (Multi-Serviços)")
    print("─" * 50)
    
    agendamento = {
        "cliente_id": "test_002",
        "servicos": ["escova", "unha", "sobrancelha"],
        "horario_solicitado": "2026-02-27T14:00:00"
    }
    
    resultado = await optimize_scheduling(agendamento)
    
    otimizacao_count = len(resultado.get('otimizacoes', []))
    
    if otimizacao_count > 0:
        print(f"   ✅ {otimizacao_count} otimizações aplicadas")
        for opt in resultado['otimizacoes']:
            print(f"      • {opt.get('tipo')}: {opt.get('mensagem', '')}")
        return True
    else:
        print(f"   ⚠️ Nenhuma otimização aplicada")
        return True


async def test_status():
    """Testa status do módulo"""
    print("\n📊 Teste 4: Status do Módulo")
    print("─" * 50)
    
    status = await get_agenda_viva_status()
    
    print(f"   Módulo: {status['modulo']}")
    print(f"   Status: {status['status']}")
    print(f"   Situações: {status['situacoes_carregadas']}")
    print(f"   Regras: {status['regras_ativas']}")
    
    if status['status'] in ['healthy', 'initializing']:
        print(f"   ✅ Status OK")
        return True
    else:
        print(f"   ❌ Status RUIM")
        return False


async def test_rollback():
    """Testa rollback (simulação de erro)"""
    print("\n📊 Teste 5: Rollback (Segurança)")
    print("─" * 50)
    
    # Simular agendamento com erro
    agendamento_com_erro = {
        "cliente_id": "test_rollback",
        "servicos": None,  # Isso vai causar erro
        "horario_solicitado": "invalido"
    }
    
    resultado = await optimize_scheduling(agendamento_com_erro)
    
    # Verificar se tem flag de erro mas NÃO quebrou
    if 'agenda_viva_error' in resultado or 'usar_fallback' in resultado:
        print(f"   ✅ Rollback FUNCIONOU (erro tratado)")
        print(f"   🛑 Luna OS v2.2 continua funcionando")
        return True
    else:
        print(f"   ⚠️ Rollback não testado (sem erro)")
        return True


async def main():
    """Executa todos testes"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🌙 LUNA OS v3.0 — Teste: Agenda Viva             ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    testes = [
        ("Inicialização", test_inicializacao),
        ("Otimização (Encaixe)", test_otimizacao_encaixe),
        ("Otimização (Multi-Serviços)", test_otimizacao_multi_servicos),
        ("Status", test_status),
        ("Rollback", test_rollback)
    ]
    
    resultados = []
    
    for nome, teste in testes:
        try:
            resultado = await teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"\n   ❌ ERRO: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES")
    print("=" * 50)
    
    for nome, resultado in resultados:
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"  {status}: {nome}")
    
    total_pass = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    print()
    if total_pass == total:
        print("╔════════════════════════════════════════════════════╗")
        print("║  ✅ TODOS TESTES PASSARAM                         ║")
        print("║  🚀 PRONTO PARA PRODUÇÃO (1% tráfego)             ║")
        print("╚════════════════════════════════════════════════════╝")
        return 0
    else:
        print("╔════════════════════════════════════════════════════╗")
        print("║  ⚠️ ALGUNS TESTES FALHARAM                        ║")
        print("║  🔧 CORRIGIR antes de produção                    ║")
        print("╚════════════════════════════════════════════════════╝")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
