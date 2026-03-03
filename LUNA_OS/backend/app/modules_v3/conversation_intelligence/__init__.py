"""
🧠 CONVERSATION INTELLIGENCE - Módulo de Análise Psicológica de Conversas

Módulo de Inteligência para Análise Profunda de Conversas do WhatsApp
Utiliza psicologia, vendas, comportamento humano e neurociência para extrair
insights acionáveis que aumentam conversão e satisfação do cliente.

Arquitetura Multi-Agentes:
├── ExtractorAgent → Extrai dados brutos das conversas
├── PsychologyAgent → Analisa emoções, personalidade, gatilhos mentais
├── SalesAgent → Analisa técnicas de vendas, objeções, estágio do funil
├── BehaviorAgent → Analisa padrões comportamentais, intenções ocultas
├── InsightsAgent → Gera insights acionáveis e recomendações
├── StorageAgent → Armazena no local correto (Supabase/Obsidian)
└── LearningAgent → Aprende com padrões e melhora análises futuras

Autor: MCT Agent Flow
Data: 2026-03-01
Versão: 1.0.0
"""

from .agents.extractor_agent import ExtractorAgent
from .agents.psychology_agent import PsychologyAgent
from .agents.sales_agent import SalesAgent
from .agents.behavior_agent import BehaviorAgent
from .agents.insights_agent import InsightsAgent
from .agents.storage_agent import StorageAgent
from .agents.learning_agent import LearningAgent
from .agents.coordinator_agent import CoordinatorAgent

__version__ = "1.0.0"
__all__ = [
    "ExtractorAgent",
    "PsychologyAgent",
    "SalesAgent",
    "BehaviorAgent",
    "InsightsAgent",
    "StorageAgent",
    "LearningAgent",
    "CoordinatorAgent",
]
