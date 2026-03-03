#!/usr/bin/env python3
"""
🌙📊 LUNA OS — Readiness Report Generator

Gera relatório de prontidão para GO-LIVE baseado nos resultados do Batch Dojo Test.
"""

import sys
import os
import json
from datetime import datetime
from loguru import logger

logger.add("logs/readiness_report.log", rotation="10 MB", retention="30 days")


def generate_readiness_report(results_file: str = None):
    """
    Gera relatório de prontidão baseado nos resultados do batch test.
    """
    logger.info("🌙 Gerando Readiness Report...")
    
    # Carregar resultados
    if results_file:
        results_path = os.path.join(os.path.dirname(__file__), results_file)
    else:
        results_path = os.path.join(os.path.dirname(__file__), "batch_dojo_results.json")
    
    if not os.path.exists(results_path):
        logger.error(f"❌ Arquivo não encontrado: {results_path}")
        logger.info("💡 Execute primeiro: batch_dojo_test.py")
        return None
    
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = data.get("results", [])
    total_tests = data.get("total_tests", 0)
    
    if not results:
        logger.error("❌ Nenhum resultado encontrado!")
        return None
    
    # Calcular métricas
    stats = calculate_detailed_statistics(results)
    
    # Gerar relatório
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_tests": total_tests,
        "readiness_score": stats["readiness_score"],
        "metrics": stats,
        "recommendation": get_recommendation(stats["readiness_score"]),
        "gaps": identify_gaps(results),
        "strengths": identify_strengths(results),
        "action_items": generate_action_items(stats)
    }
    
    # Salvar relatório
    output_path = os.path.join(os.path.dirname(__file__), "readiness_report.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"💾 Relatório salvo em: {output_path}")
    
    # Exibir relatório
    display_report(report)
    
    return report


def calculate_detailed_statistics(results: list) -> dict:
    """
    Calcula estatísticas detalhadas dos resultados.
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
    
    # Critérios mais falhos
    criteria_failures = {}
    for r in results:
        if "metrics" in r:
            for criterion in r["metrics"].get("criteria_missing", []):
                criteria_failures[criterion] = criteria_failures.get(criterion, 0) + 1
    
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
        "readiness_score": round(readiness_score, 1),
        "criteria_failures": dict(sorted(criteria_failures.items(), key=lambda x: x[1], reverse=True)[:10])
    }


def get_recommendation(score: float) -> dict:
    """
    Retorna recomendação baseada no score.
    """
    if score >= 80:
        return {
            "status": "READY",
            "message": "✅ PRONTO PARA GO-LIVE",
            "emoji": "🚀",
            "next_steps": [
                "Escanear QR Code no Evolution Manager",
                "Ativar mode=active no .env",
                "Monitorar primeiras interações reais"
            ]
        }
    elif score >= 60:
        return {
            "status": "ALMOST_READY",
            "message": "⚠️ QUASE PRONTO (treinar mais)",
            "emoji": "🔧",
            "next_steps": [
                "Revisar critérios com maior taxa de falha",
                "Expandir knowledge base",
                "Executar novo batch test após ajustes"
            ]
        }
    else:
        return {
            "status": "NOT_READY",
            "message": "❌ NÃO PRONTO (precisa treinar)",
            "emoji": "📚",
            "next_steps": [
                "Revisar system prompt do Brain",
                "Expandir knowledge base significativamente",
                "Executar múltiplos batch tests",
                "Considerar mode=observe por mais tempo"
            ]
        }


def identify_gaps(results: list) -> list:
    """
    Identifica gaps de conhecimento.
    """
    gaps = []
    
    # Agrupar falhas por intent
    intent_failures = {}
    for r in results:
        if not r.get("success", False):
            intent = r.get("intent_expected", "unknown")
            if intent not in intent_failures:
                intent_failures[intent] = []
            intent_failures[intent].append(r)
    
    for intent, failures in intent_failures.items():
        gaps.append({
            "intent": intent,
            "failure_count": len(failures),
            "examples": [f["user_message"][:100] for f in failures[:3]]
        })
    
    return sorted(gaps, key=lambda x: x["failure_count"], reverse=True)[:10]


def identify_strengths(results: list) -> list:
    """
    Identifica pontos fortes.
    """
    strengths = []
    
    # Agrupar sucessos por intent
    intent_successes = {}
    for r in results:
        if r.get("success", False):
            intent = r.get("intent_expected", "unknown")
            if intent not in intent_successes:
                intent_successes[intent] = []
            intent_successes[intent].append(r)
    
    for intent, successes in intent_successes.items():
        if len(successes) >= 3:  # Pelo menos 3 sucessos
            strengths.append({
                "intent": intent,
                "success_count": len(successes),
                "success_rate": len(successes) / sum(1 for r in results if r.get("intent_expected") == intent) * 100
            })
    
    return sorted(strengths, key=lambda x: x["success_count"], reverse=True)[:10]


def generate_action_items(stats: dict) -> list:
    """
    Gera lista de ações baseadas nas estatísticas.
    """
    action_items = []
    
    # Baixa empatia
    if stats["avg_empathy"] < 70:
        action_items.append({
            "priority": "HIGH",
            "area": "Empatia",
            "issue": f"Média atual: {stats['avg_empathy']}/100",
            "action": "Adicionar mais frases de acolhimento no system prompt"
        })
    
    # Baixa clareza
    if stats["avg_clarity"] < 70:
        action_items.append({
            "priority": "HIGH",
            "area": "Clareza",
            "issue": f"Média atual: {stats['avg_clarity']}/100",
            "action": "Simplificar respostas e usar estrutura mais direta"
        })
    
    # Baixa acionabilidade
    if stats["avg_actionability"] < 70:
        action_items.append({
            "priority": "MEDIUM",
            "area": "Acionabilidade",
            "issue": f"Média atual: {stats['avg_actionability']}/100",
            "action": "Adicionar mais call-to-action nas respostas"
        })
    
    # Baixa precisão de intent
    if stats["intent_accuracy"] < 80:
        action_items.append({
            "priority": "HIGH",
            "area": "Classificação de Intent",
            "issue": f"Precisão atual: {stats['intent_accuracy']}%",
            "action": "Expandir patterns de intent no brain.py"
        })
    
    # Critérios com muitas falhas
    for criterion, count in list(stats["criteria_failures"].items())[:3]:
        action_items.append({
            "priority": "MEDIUM",
            "area": f"Critério: {criterion}",
            "issue": f"Falhou {count} vezes",
            "action": f"Revisar lógica de avaliação para '{criterion}'"
        })
    
    return action_items


def display_report(report: dict):
    """
    Exibe relatório formatado.
    """
    rec = report["recommendation"]
    stats = report["metrics"]
    
    logger.info(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  LUNA OS — READINESS REPORT                                ║
    ║  Gerado em: {report['generated_at']}
    ╠════════════════════════════════════════════════════════════╣
    ║  {rec['emoji']} {rec['message']}
    ╠════════════════════════════════════════════════════════════╣
    ║  READINESS SCORE: {report['readiness_score']}/100
    ╠════════════════════════════════════════════════════════════╣
    ║  MÉTRICAS:                                                 ║
    ║  • Testes: {stats['total_tests']}
    ║  • Sucesso: {stats['successful_tests']}/{stats['total_tests']} ({stats['success_rate']}%)
    ║  • Intent Accuracy: {stats['intent_accuracy']}%
    ║  • Empatia: {stats['avg_empathy']}/100
    ║  • Clareza: {stats['avg_clarity']}/100
    ║  • Acionabilidade: {stats['avg_actionability']}/100
    ║  • Tempo Médio: {stats['avg_processing_time_ms']:.0f}ms
    ╠════════════════════════════════════════════════════════════╣
    ║  PRÓXIMOS PASSOS:                                          ║
    """ + "\n".join([f"║  • {step}" for step in rec["next_steps"]]) + """
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Exibir gaps
    if report["gaps"]:
        logger.info("\n🔍 GAPS IDENTIFICADOS:")
        for gap in report["gaps"][:5]:
            logger.info(f"  • {gap['intent']}: {gap['failure_count']} falhas")
    
    # Exibir ações
    if report["action_items"]:
        logger.info("\n📋 AÇÕES RECOMENDADAS:")
        for item in report["action_items"][:5]:
            logger.info(f"  [{item['priority']}] {item['area']}: {item['action']}")


if __name__ == "__main__":
    try:
        report = generate_readiness_report()
        
        if report:
            print(f"\n✅ Readiness Report gerado!")
            print(f"📁 Arquivo: readiness_report.json")
            print(f"🏆 Score: {report['readiness_score']}/100")
            print(f"💡 Recomendação: {report['recommendation']['message']}")
        else:
            print("\n❌ Erro ao gerar relatório.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Erro ao gerar relatório: {e}")
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
