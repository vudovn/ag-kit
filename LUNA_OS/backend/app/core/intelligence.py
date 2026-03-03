"""
LUNA Intelligence - Parsers e Extração de BI
Padrão Elite MCT: Blindagem tripla e 'Truth in Data'.
"""

import json
import re
from typing import Tuple, Dict, Any, List
from loguru import logger

from app.core.schemas_brain import (
    IntentType,
    CustomerMood,
    PotentialValue,
    IntelligenceData,
    SentimentType,
)


def parse_response(text: str) -> Tuple[str, IntelligenceData]:
    """
    Analisa a resposta do LLM com blindagem tripla:
    1. Delimitadores Soberanos
    2. JSON Parsing
    3. Fallback Regex
    """
    try:
        # 1. Separação por delimitadores
        parts = text.split("---INTELLIGENCE---")
        response_part = parts[0].replace("---RESPONSE---", "").strip()

        intelligence_data = IntelligenceData()

        if len(parts) > 1:
            intel_json = parts[1].strip()
            try:
                # Limpeza de markdown no JSON
                intel_json = re.sub(r"```json\n?|\n?```", "", intel_json).strip()
                raw_intel = json.loads(intel_json)

                # Parse com validação de enums
                intelligence_data = parse_intelligence_safe(raw_intel)

            except json.JSONDecodeError as e:
                logger.warning(f"⚠️ JSON parsing failed, using regex fallback: {e}")
                intelligence_data = extract_intelligence_fallback(text)
        else:
            logger.warning("⚠️ ---INTELLIGENCE--- delimiter missing, using fallback")
            intelligence_data = extract_intelligence_fallback(text)

        return response_part, intelligence_data

    except Exception as e:
        logger.error(f"🚨 Critical parser failure: {e}")
        return text, extract_intelligence_fallback(text)


def parse_intelligence_safe(raw: Dict) -> IntelligenceData:
    """Parse seguro de intelligence com validação de enums"""
    valid_moods = {m.value for m in CustomerMood}
    valid_potentials = {v.value for v in PotentialValue}

    # Customer mood
    mood_raw = str(raw.get("customer_mood", "unknown")).lower()
    valid_moods_dict = {m.value.lower(): m for m in CustomerMood}

    if mood_raw in valid_moods_dict:
        mood = valid_moods_dict[mood_raw]
    elif "frustrad" in mood_raw:
        mood = CustomerMood.FRUSTRATED
    else:
        mood = CustomerMood.UNKNOWN

    # Potential value
    potential_raw = str(raw.get("potential_value", "medium")).lower()
    valid_potentials_dict = {v.value.lower(): v for v in PotentialValue}

    if potential_raw in valid_potentials_dict:
        potential = valid_potentials_dict[potential_raw]
    else:
        potential = PotentialValue.MEDIUM

    # Urgency level (1-5)
    try:
        urgency = int(raw.get("urgency_level", 3))
        urgency = max(1, min(5, urgency))
    except (TypeError, ValueError):
        urgency = 3

    return IntelligenceData(
        insight=raw.get("insight", "Insight não detectado"),
        objections=raw.get("objections", []) or [],
        customer_mood=mood,
        urgency_level=urgency,
        potential_value=potential,
        metadata=raw.get("metadata", {}),
    )


def extract_intelligence_fallback(text: str) -> IntelligenceData:
    """
    Camada de Proteção: Extrai BI via Regex quando a IA falha.
    """
    text_lower = text.lower()

    # Detecção de humor
    mood = CustomerMood.UNKNOWN
    if any(w in text_lower for w in ["pressa", "agora", "rápido", "logo"]):
        mood = CustomerMood.HURRY
    elif any(w in text_lower for w in ["caro", "dúvida", "medo", "não sei"]):
        mood = CustomerMood.HESITANT
    elif any(w in text_lower for w in ["ruim", "erro", "péssimo", "odeio"]):
        mood = CustomerMood.FRUSTRATED
    elif any(w in text_lower for w in ["legal", "ótimo", "perfeito", "obrigado"]):
        mood = CustomerMood.HAPPY

    # Detecção de urgência
    urgency = 3
    if any(w in text_lower for w in ["hoje", "agora", "urgente"]):
        urgency = 5
    elif any(w in text_lower for w in ["depois", "mês que vem", "olhando"]):
        urgency = 1

    # Detecção de objeções
    objections = []
    if any(w in text_lower for w in ["preço", "caro", "valor", "custa"]):
        objections.append("preco")
    if any(w in text_lower for w in ["horário", "agenda", "marcar", "agendar"]):
        objections.append("agenda")

    return IntelligenceData(
        insight="Extraído via Fallback Soberano",
        objections=objections,
        customer_mood=mood,
        urgency_level=urgency,
        potential_value=PotentialValue.MEDIUM,
    )


def extract_fields(message: str, response: str) -> Dict[str, Any]:
    """Extração de campos para memória persistente e agendamento"""
    extracted = {}
    msg = message.lower()
    from datetime import datetime, timedelta

    # Data mencionada (ex: 12/03, amanhã, hoje)
    date_match = re.search(r"(\d{1,2}/\d{1,2})", msg)
    if date_match:
        try:
            day, month = date_match.group(1).split("/")
            year = datetime.now().year
            extracted["date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        except:
            extracted["date"] = date_match.group(1)
    elif "amanhã" in msg:
        extracted["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "hoje" in msg:
        extracted["date"] = datetime.now().strftime("%Y-%m-%d")

    # Horário mencionado (ex: 14h, 14:30)
    time_match = re.search(r"(\d{1,2})h(\d{2})?", msg)
    if time_match:
        hour = time_match.group(1).zfill(2)
        minute = time_match.group(2) if time_match.group(2) else "00"
        extracted["time"] = f"{hour}:{minute}"

    # Detecção básica de serviço
    services_list = [
        "escova",
        "manicure",
        "pedicure",
        "gel",
        "progressiva",
        "corte",
        "tintura",
    ]
    extracted["services"] = []
    for s in services_list:
        if s in msg:
            extracted["services"].append(s)

    if extracted["services"]:
        extracted["service"] = extracted["services"][0]

    # Detecção básica de profissional
    profs = ["ju", "dávila", "carla", "lu", "tay", "mariana"]
    for p in profs:
        if p in msg:
            extracted["professional"] = p
            break

    return extracted


def detect_sentiment(message: str) -> str:
    """Análise simples de sentimento via keywords"""
    msg = message.lower()

    positive_words = {"amei", "ótimo", "perfeito", "obrigado", "legal"}
    negative_words = {"ruim", "problema", "não gostei", "péssimo", "demora"}

    if any(w in msg for w in positive_words):
        return SentimentType.POSITIVE
    if any(w in msg for w in negative_words):
        return SentimentType.NEGATIVE
    return SentimentType.NEUTRAL
