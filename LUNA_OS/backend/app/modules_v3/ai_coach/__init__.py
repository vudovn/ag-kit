"""
🌙 LUNA OS v3.0 — Módulo 6: AI Coach
"""

from .trainer import ai_coach, AICoach
from .api import gerar_treino, avaliar_resposta, gerar_relatorio, get_ai_coach_status

__all__ = [
    'ai_coach',
    'AICoach',
    'gerar_treino',
    'avaliar_resposta',
    'gerar_relatorio',
    'get_ai_coach_status'
]
