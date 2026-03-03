"""
Dojo Metrics — Calculation and evaluation functions
"""

import re
from typing import Dict, List, Optional

# ==================== METRIC CALCULATORS ====================

def calculate_empathy_score(response: str) -> int:
    """
    Calculate empathy score (0-100) based on response content.
    Higher score = more empathetic response.
    """
    response_lower = response.lower()
    score = 50  # Base score
    
    # Empathy indicators (+ points)
    empathy_phrases = [
        "entendo", "compreendo", "sinto", "desculpe", "lamento",
        "posso ajudar", "estou aqui", "fique tranquila", "não se preocupe",
        "vou te ajudar", "pode contar", "importa para nós"
    ]
    
    for phrase in empathy_phrases:
        if phrase in response_lower:
            score += 5
    
    # Cold indicators (- points)
    cold_phrases = [
        "não temos", "não posso", "não é possível", "impossível",
        "não funciona assim", "isso não é", "você tem que", "precisa"
    ]
    
    for phrase in cold_phrases:
        if phrase in response_lower:
            score -= 5
    
    return max(0, min(100, score))

def calculate_clarity_score(response: str) -> int:
    """
    Calculate clarity score (0-100) based on response structure.
    Higher score = clearer response.
    """
    score = 50  # Base score
    
    # Clarity indicators
    if len(response.split()) < 10:
        score -= 10  # Too short
    elif len(response.split()) > 100:
        score -= 10  # Too long
    
    # Good structure indicators
    if any(c in response for c in ['\n', '- ', '• ', '1.', '2.']):
        score += 15  # Structured response
    
    # Clear information
    if any(word in response.lower() for word in ['horário', 'preço', 'endereço', 'agendar']):
        score += 10  # Specific information
    
    # Call to action
    if any(word in response.lower() for word in ['quer', 'pode', 'gostaria', 'vamos']):
        score += 10  # Engagement
    
    return max(0, min(100, score))

def calculate_actionability_score(response: str) -> int:
    """
    Calculate actionability score (0-100) based on whether response leads to action.
    Higher score = more actionable response.
    """
    response_lower = response.lower()
    score = 50  # Base score
    
    # Action indicators
    action_phrases = [
        "vou verificar", "deixa eu ver", "posso te passar", "te chamo",
        "me confirma", "me diz", "qual dia", "qual horário", "com qual profissional",
        "vamos agendar", "quer marcar", "posso deixar reservado"
    ]
    
    for phrase in action_phrases:
        if phrase in response_lower:
            score += 10
    
    # Passive indicators (- points)
    passive_phrases = [
        "não sei", "não tenho certeza", "talvez", "provavelmente",
        "acho que", "deve ter", "creio que"
    ]
    
    for phrase in passive_phrases:
        if phrase in response_lower:
            score -= 5
    
    return max(0, min(100, score))

def calculate_success_metrics(
    response: str,
    expected_intent: str,
    detected_intent: str,
    scenario_criteria: list
) -> dict:
    """
    Calculate comprehensive success metrics for a test scenario.
    """
    # Initialize with defaults
    metrics = {
        "intent_match": expected_intent == detected_intent,
        "empathy_score": calculate_empathy_score(response),
        "clarity_score": calculate_clarity_score(response),
        "actionability_score": calculate_actionability_score(response),
        "criteria_met": [],
        "criteria_missing": [],
        "overall_success": False,
        "points_earned": 0
    }

    # Handle empty criteria
    if not scenario_criteria:
        scenario_criteria = []

    # Check criteria
    criteria_checks = {
        "warm_response": any(w in response.lower() for w in ["oi", "olá", "bom dia", "boa tarde", "✨", "😊"]),
        "offer_help": any(w in response.lower() for w in ["ajudar", "posso", "quer", "gostaria"]),
        "accurate_hours": any(w in response.lower() for w in ["8h", "20h", "segunda", "sábado", "segunda a sábado"]),
        "accurate_address": any(w in response.lower() for w in ["mato grosso", "837", "jardim itália", "chapecó"]),
        "accurate_price": bool(re.search(r"r\$\s*\d+", response.lower())),
        "value_proposition": any(w in response.lower() for w in ["qualidade", "profissional", "resultado", "durabilidade"]),
        "collect_service": any(w in response.lower() for w in ["qual serviço", "qual procedimento", "o que quer fazer"]),
        "collect_time": any(w in response.lower() for w in ["qual dia", "qual horário", "que horas"]),
        "collect_professional": any(w in response.lower() for w in ["qual profissional", "com quem", "preferência"]),
        "upsell_package": any(w in response.lower() for w in ["pacote", "combo", "junto", "aproveitar"]),
        "empathy": calculate_empathy_score(response) > 70,
        "solution_offered": any(w in response.lower() for w in ["solução", "resolver", "arrumar", "fazer"]),
        "urgency_detected": any(w in response.lower() for w in ["hoje", "agora", "urgente", "rápido"]),
        "fast_response": len(response.split()) < 50,
        "clear_explanation": calculate_clarity_score(response) > 70,
        "educational": len(response.split()) > 30,
        "recommendation": any(w in response.lower() for w in ["recomendo", "sugiro", "aconselho"]),
        "differentiate": any(w in response.lower() for w in ["diferencial", "único", "especial", "exclusivo"]),
        "confidence": calculate_actionability_score(response) > 60,
        "apology": any(w in response.lower() for w in ["desculpe", "lamento", "perdão", "sinto"]),
        "handoff_if_needed": any(w in response.lower() for w in ["equipe", "supervisora", "gerente", "humano"]),
        "policy_explained": any(w in response.lower() for w in ["política", "regra", "norma", "procedimento"]),
        "crisis_management": any(w in response.lower() for w in ["resolver", "prioridade", "imediato"]),
        "immediate_handoff": any(w in response.lower() for w in ["já te passo", "agora mesmo", "imediatamente"]),
        "creativity": len(set(response.split())) > 20,
        "boundaries": any(w in response.lower() for w in ["podemos", "dentro do possível", "viabilizar"]),
        "alternative_offered": any(w in response.lower() for w in ["alternativa", "outra opção", "também temos"]),
        "handle_all_objections": response.count("mas") < 2,
        "patience": len(response) > 100,
        "close_attempt": any(w in response.lower() for w in ["vamos", "fechamos", "confirmamos", "agendamos"]),
        # Critérios faltantes adicionados
        "friendly_tone": any(w in response.lower() for w in ["por favor", "gentileza", "amável", "gentil", "querida", "querido"]),
        "offer_directions": any(w in response.lower() for w in ["endereço", "localização", "como chegar", "rua", "avenida", "número"]),
        "value_not_price": any(w in response.lower() for w in ["valor", "benefício", "qualidade", "resultado", "profissional", "experiência"]),
        "enforce_order": any(w in response.lower() for w in ["primeiro", "depois", "ordem", "sequência", "antes de", "em seguida"]),
        "explain_logic": any(w in response.lower() for w in ["porque", "por que", "razão", "motivo", "explicar", "explicação", "lógica"])
    }

    for criterion in scenario_criteria:
        if criteria_checks.get(criterion, False):
            if isinstance(metrics["criteria_met"], list):
                metrics["criteria_met"].append(criterion)
        else:
            if isinstance(metrics["criteria_missing"], list):
                metrics["criteria_missing"].append(criterion)

    # Determine overall success (70% of criteria must be met)
    if len(scenario_criteria) > 0:
        success_rate = len(metrics["criteria_met"]) / len(scenario_criteria) if isinstance(metrics["criteria_met"], list) else 0
        metrics["overall_success"] = success_rate >= 0.7
        metrics["points_earned"] = int(10 * len(metrics["criteria_met"])) if isinstance(metrics["criteria_met"], list) else 0
    else:
        # No criteria = success by default
        metrics["overall_success"] = True
        metrics["points_earned"] = 10

    return metrics

def calculate_dojo_summary(feedback_list: List[Dict]) -> Dict:
    """
    Calculate summary statistics from dojo feedback.
    """
    if not feedback_list:
        return {
            "total_tests": 0,
            "success_rate": 0,
            "avg_rating": 0,
            "avg_empathy": 0,
            "avg_clarity": 0,
            "avg_actionability": 0
        }
    
    total = len(feedback_list)
    success_count = sum(1 for f in feedback_list if f.get("success", False))
    ratings = [f.get("rating", 0) for f in feedback_list if f.get("rating")]
    
    metrics_list = [f.get("metrics", {}) for f in feedback_list]
    empathy_scores = [m.get("empathy_score", 0) for m in metrics_list if m]
    clarity_scores = [m.get("clarity_score", 0) for m in metrics_list if m]
    actionability_scores = [m.get("actionability_score", 0) for m in metrics_list if m]
    
    return {
        "total_tests": total,
        "success_rate": round((success_count / total) * 100, 1) if total > 0 else 0,
        "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
        "avg_empathy": round(sum(empathy_scores) / len(empathy_scores), 1) if empathy_scores else 0,
        "avg_clarity": round(sum(clarity_scores) / len(clarity_scores), 1) if clarity_scores else 0,
        "avg_actionability": round(sum(actionability_scores) / len(actionability_scores), 1) if actionability_scores else 0
    }
