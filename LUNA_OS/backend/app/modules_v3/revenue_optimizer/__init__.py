"""
🌙 LUNA OS v3.0 — Módulo 5: Revenue Optimizer
"""

from .optimizer import revenue_optimizer, RevenueOptimizer
from .api import calcular_preco_dinamico, sugerir_pacote, get_revenue_status

__all__ = [
    'revenue_optimizer',
    'RevenueOptimizer',
    'calcular_preco_dinamico',
    'sugerir_pacote',
    'get_revenue_status'
]
