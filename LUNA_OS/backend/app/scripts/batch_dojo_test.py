#!/usr/bin/env python3
"""
🌙🧪 LUNA OS — Batch Dojo Test

Executa testes em batch no Dojo Arena usando cenários reais exportados.
"""

import sys
import os
import asyncio
import json
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.integrations.supabase_client import get_supabase
from app.core.brain import process_message
from app.dojo.metrics import calculate_success_metrics, calculate_empathy_score, calculate_clarity_score, calculate_actionability_score
from loguru import logger
from datetime import datetime

logger.add("logs/batch_dojo_test.log", rotation="10 MB", retention="7 days")


async def run_batch_test(scenarios_file: str = None, limit: int = 100):
    """
    Executa testes em batch nos cenários reais.
    """
    logger.info("🌙 Iniciando Batch Dojo Test...")
    
    # Carregar cenários
    if scenarios_file:
        scenarios_path = os.path.join(os.path.dirname(__file__), scenarios_file)
    else:
        scenarios_path = os.path.join(os.path.dirname(__file__), "real_conversations_scenarios.json")
    
    if not os.path.exists(scenarios_path):
        logger.error(f"❌ Arquivo não encontrado: {scenarios_path}")
        logger.info("💡 Execute primeiro: export_real_conversations.py")
        return None
    
    with open(scenarios_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    scenarios = data.get("scenarios", [])[:limit]
    logger.info(f"📊 {len(scenarios)} cenários carregados")
    
    # Executar testes
    results = []
    start_time = time.time()
    
    for i, scenario in enumerate(scenarios, 1):
        logger.info(f"🧪 Teste {i}/{len(scenarios)}: {scenario['name']}")
        
        try:
            # Processar mensagem com Brain
            test_start = time.time()
            
            result = await process_message(
                phone=scenario.get("metadata", {}).get("phone", "5549999999999"),
                name="Teste Dojo",
                message=scenario["sample_message"],
                history=[]
            )
            
            processing_time = (time.time() - test_start) * 1000
            
            # Calcular métricas
            response_text = result.get("response", "")
            detected_intent = result.get("intent", "unknown")
            confidence = result.get("intent_confidence", 0)
            
            # Critérios de sucesso
            scenario_criteria = scenario.get("success_criteria", [])
            expected_intent = scenario.get("expected_intent", "")
            
            metrics = calculate_success_metrics(
                response=response_text,
                expected_intent=expected_intent,
                detected_intent=detected_intent,
                scenario_criteria=scenario_criteria
            )
            
            # Adicionar métricas adicionais
            metrics["empathy_score"] = calculate_empathy_score(response_text)
            metrics["clarity_score"] = calculate_clarity_score(response_text)
            metrics["actionability_score"] = calculate_actionability_score(response_text)
            
            # Salvar resultado
            test_result = {
                "scenario_id": scenario["id"],
                "scenario_name": scenario["name"],
                "user_message": scenario["sample_message"],
                "luna_response": response_text,
                "intent_detected": detected_intent,
                "intent_expected": expected_intent,
                "confidence_score": confidence,
                "processing_time_ms": round(processing_time, 2),
                "metrics": metrics,
                "success": metrics["overall_success"],
                "points_earned": metrics["points_earned"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            results.append(test_result)
            
            status = "✅" if test_result["success"] else "❌"
            logger.info(f"{status} {scenario['name']} - Intent: {expected_intent} → {detected_intent}")
            
        except Exception as e:
            logger.error(f"❌ Erro no teste {scenario['name']}: {e}")
            results.append({
                "scenario_id": scenario["id"],
                "scenario_name": scenario["name"],
                "error": str(e),
                "success": False
            })
    
    total_time = time.time() - start_time
    
    # Salvar resultados
    output_path = os.path.join(os.path.dirname(__file__), "batch_dojo_results.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_tests": len(results),
            "total_time_seconds": round(total_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    logger.info(f"💾 Resultados salvos em: {output_path}")
    
    # Calcular estatísticas
    stats = calculate_statistics(results)
    
    # Exibir resumo
    display_summary(stats, total_time)
    
    return stats


def calculate_statistics(results: list) -> dict:
    """
    Calcula estatísticas dos resultados.
    """
    total = len(results)
    successful = [r for r in results if r.get("success", False)]
    
    # Métricas básicas
    success_rate = len(successful) / total * 100 if total > 0 else 0
    
    # Métricas de qualidade
    empathy_scores = [r["metrics"]["empathy_score"] for r in results if "metrics" in r]
    clarity_scores = [r["metrics"]["clarity_score"] for r in results if "metrics" in r]
    actionability_scores = [r["metrics"]["actionability_score"] for r in results if "metrics" in r]
    
    avg_empathy = sum(empathy_scores) / len(empathy_scores) if empathy_scores else 0
    avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0
    avg_actionability = sum(actionability_scores) / len(actionability_scores) if actionability_scores else 0
    
    # Intent accuracy
    intent_matches = [r for r in results if r.get("intent_detected") == r.get("intent_expected")]
    intent_accuracy = len(intent_matches) / total * 100 if total > 0 else 0
    
    # Processing time
    processing_times = [r["processing_time_ms"] for r in results if "processing_time_ms" in r]
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    # Readiness score (ponderado)
    readiness_score = (
        success_rate * 0.3 +
        avg_empathy * 0.2 +
        avg_clarity * 0.2 +
        avg_actionability * 0.15 +
        intent_accuracy * 0.15
    )
    
    return {
        "total_tests": total,
        "successful_tests": len(successful),
        "failed_tests": total - len(successful),
        "success_rate": round(success_rate, 1),
        "avg_empathy": round(avg_empathy, 1),
        "avg_clarity": round(avg_clarity, 1),
        "avg_actionability": round(avg_actionability, 1),
        "intent_accuracy": round(intent_accuracy, 1),
        "avg_processing_time_ms": round(avg_processing_time, 1),
        "readiness_score": round(readiness_score, 1)
    }


def display_summary(stats: dict, total_time: float):
    """
    Exibe resumo dos resultados.
    """
    # Determinar recomendação
    if stats["readiness_score"] >= 80:
        recommendation = "✅ PRONTO PARA GO-LIVE"
        emoji = "🚀"
    elif stats["readiness_score"] >= 60:
        recommendation = "⚠️ QUASE PRONTO (treinar mais)"
        emoji = "🔧"
    else:
        recommendation = "❌ NÃO PRONTO (precisa treinar)"
        emoji = "📚"
    
    logger.info(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  BATCH DOJO TEST — RESUMO                                  ║
    ╠════════════════════════════════════════════════════════════╣
    ║  {emoji} {recommendation}
    ╠════════════════════════════════════════════════════════════╣
    ║  Total Testes: {stats['total_tests']}
    ║  Tempo Total: {total_time:.2f}s ({stats['total_tests']/total_time:.1f} testes/seg)
    ╠════════════════════════════════════════════════════════════╣
    ║  ✅ Sucessos: {stats['successful_tests']}/{stats['total_tests']} ({stats['success_rate']}%)
    ║  ❌ Falhas: {stats['failed_tests']}/{stats['total_tests']} ({100-stats['success_rate']:.1f}%)
    ╠════════════════════════════════════════════════════════════╣
    ║  🎯 Intent Accuracy: {stats['intent_accuracy']}%
    ║  💚 Empatia Média: {stats['avg_empathy']}/100
    ║  📖 Clareza Média: {stats['avg_clarity']}/100
    ║  ⚡ Acionabilidade: {stats['avg_actionability']}/100
    ║  ⏱️ Tempo Médio: {stats['avg_processing_time_ms']:.0f}ms
    ╠════════════════════════════════════════════════════════════╣
    ║  🏆 READINESS SCORE: {stats['readiness_score']}/100
    ╚════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    try:
        stats = asyncio.run(run_batch_test(limit=100))
        
        if stats:
            print(f"\n✅ Batch Dojo Test concluído!")
            print(f"📁 Resultados: batch_dojo_results.json")
            print(f"🏆 Readiness Score: {stats['readiness_score']}/100")
        else:
            print("\n❌ Erro ao executar testes.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Erro no batch test: {e}")
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
