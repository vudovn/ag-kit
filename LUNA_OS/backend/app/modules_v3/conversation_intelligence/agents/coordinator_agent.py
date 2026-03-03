"""
🎯 Coordinator Agent - Coordenador da Equipe

Orquestra todos os agentes:
- Gerencia pipeline de execução
- Coordena dependências entre agentes
- Consolida resultados
- Gerencia erros e retries

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from .base_agent import AgentContext, AgentResult
from .extractor_agent import ExtractorAgent
from .psychology_agent import PsychologyAgent
from .sales_agent import SalesAgent
from .behavior_agent import BehaviorAgent
from .insights_agent import InsightsAgent
from .storage_agent import StorageAgent
from .learning_agent import LearningAgent


class CoordinatorAgent:
    """
    Coordenador da equipe de agentes de análise.

    Pipeline de execução:
    1. ExtractorAgent → Extrai dados brutos
    2. PsychologyAgent → Analisa aspectos psicológicos
    3. SalesAgent → Analisa aspectos de vendas
    4. BehaviorAgent → Analisa comportamento
    5. InsightsAgent → Gera insights consolidados
    6. StorageAgent → Armazena resultados
    7. LearningAgent → Aprende com resultados
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.debug_mode = self.config.get("debug", False)

        # Inicializar agentes
        self.agents = {
            "extractor": ExtractorAgent(self.config.get("extractor", {})),
            "psychology": PsychologyAgent(self.config.get("psychology", {})),
            "sales": SalesAgent(self.config.get("sales", {})),
            "behavior": BehaviorAgent(self.config.get("behavior", {})),
            "insights": InsightsAgent(self.config.get("insights", {})),
            "storage": StorageAgent(self.config.get("storage", {})),
            "learning": LearningAgent(self.config.get("learning", {})),
        }

        logger.info("🎯 CoordinatorAgent inicializado com 7 agentes")

    def analyze_conversation(
        self, context: AgentContext, enable_learning: bool = True
    ) -> Dict[str, Any]:
        """
        Executa análise completa da conversa.

        Args:
            context: Contexto da conversa
            enable_learning: Se deve executar learning agent

        Returns:
            Dict com todos os resultados consolidados
        """
        start_time = time.time()
        results = {}
        errors = []

        try:
            # Pipeline de execução
            logger.info(f"🚀 Iniciando análise da conversa {context.conversation_id}")

            # 1. Extractor
            logger.info("📥 Executando ExtractorAgent...")
            results["extractor"] = self.agents["extractor"].analyze(context)

            # 2. Psychology
            logger.info("🧠 Executando PsychologyAgent...")
            results["psychology"] = self.agents["psychology"].analyze(context)

            # 3. Sales
            logger.info("💰 Executando SalesAgent...")
            results["sales"] = self.agents["sales"].analyze(context)

            # 4. Behavior
            logger.info("👥 Executando BehaviorAgent...")
            results["behavior"] = self.agents["behavior"].analyze(context)

            # 5. Insights (usa resultados dos anteriores)
            logger.info("💡 Executando InsightsAgent...")
            agent_results = [
                results[k]
                for k in ["extractor", "psychology", "sales", "behavior"]
                if k in results
            ]
            results["insights"] = self.agents["insights"].analyze(
                context, agent_results
            )

            # 6. Storage
            logger.info("💾 Executando StorageAgent...")

            # Precisamos passar TODOS os resultados pro Storage, incluindo o do Insights
            all_results = agent_results + [results["insights"]]

            results["storage"] = self.agents["storage"].analyze(context, all_results)

            # 7. Learning (opcional)
            if enable_learning:
                logger.info("🎓 Executando LearningAgent...")
                results["learning"] = self.agents["learning"].analyze(
                    context, agent_results
                )

            # Consolidar resultados
            consolidated = self._consolidate_results(context, results)

            total_time = int((time.time() - start_time) * 1000)
            logger.info(f"✅ Análise concluída em {total_time}ms")

            return consolidated

        except Exception as e:
            logger.error(f"❌ Erro na análise: {e}")
            errors.append(str(e))

            return {
                "success": False,
                "error": str(e),
                "partial_results": results,
            }

    def _consolidate_results(
        self, context: AgentContext, results: Dict[str, AgentResult]
    ) -> Dict:
        """Consolida todos os resultados em um único relatório"""

        # Extrair dados principais de cada agente
        extractor_data = (
            results.get("extractor", {}).data if results.get("extractor") else {}
        )
        psychology_data = (
            results.get("psychology", {}).data if results.get("psychology") else {}
        )
        sales_data = results.get("sales", {}).data if results.get("sales") else {}
        behavior_data = (
            results.get("behavior", {}).data if results.get("behavior") else {}
        )
        insights_data = (
            results.get("insights", {}).data if results.get("insights") else {}
        )

        # Calcular confiança média
        confidences = [
            r.confidence
            for r in results.values()
            if isinstance(r, AgentResult) and r.success
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            "success": True,
            "conversation_id": context.conversation_id,
            "phone": context.phone,
            "client_name": context.client_name,
            "timestamp": datetime.utcnow().isoformat(),
            # Dados extraídos
            "extracted_data": extractor_data,
            # Análise psicológica
            "psychology": {
                "dominant_emotion": psychology_data.get("emotions", {}).get(
                    "dominant_emotion"
                ),
                "personality_type": psychology_data.get("personality", {}).get(
                    "dominant_type"
                ),
                "communication_style": psychology_data.get(
                    "communication_style", {}
                ).get("dominant_style"),
            },
            # Análise de vendas
            "sales": {
                "funnel_stage": sales_data.get("funnel_stage", {}).get("stage"),
                "conversion_probability": sales_data.get(
                    "conversion_probability", {}
                ).get("probability"),
                "objections_count": len(sales_data.get("objections", [])),
                "potential_value": sales_data.get("potential_value", {}).get(
                    "estimated_value"
                ),
            },
            # Análise comportamental
            "behavior": {
                "dominant_pattern": behavior_data.get("behavior_patterns", {}).get(
                    "dominant_pattern"
                ),
                "churn_risk": behavior_data.get("churn_risk", {}).get("risk_level"),
                "loyalty_level": behavior_data.get("loyalty_indicators", {}).get(
                    "loyalty_level"
                ),
            },
            # Insights consolidados
            "insights": {
                "key_insights": insights_data.get("key_insights", []),
                "recommendations": insights_data.get("actionable_recommendations", []),
                "alerts": insights_data.get("alerts", []),
                "opportunities": insights_data.get("opportunities", []),
                "priority_score": insights_data.get("priority_score", {}).get("score"),
                "ai_executive_summary": insights_data.get("ai_executive_summary", ""),
            },
            # Metadados
            "metadata": {
                "total_agents": len(results),
                "successful_analyses": sum(
                    1
                    for r in results.values()
                    if isinstance(r, AgentResult) and r.success
                ),
                "average_confidence": avg_confidence,
                "processing_time_ms": sum(
                    r.processing_time_ms
                    for r in results.values()
                    if isinstance(r, AgentResult)
                ),
            },
        }

    def get_agent_status(self) -> Dict:
        """Retorna status de todos os agentes"""
        return {
            name: {
                "name": agent.get_name(),
                "expertise": agent.get_expertise(),
                "enabled": agent.enabled,
            }
            for name, agent in self.agents.items()
        }
