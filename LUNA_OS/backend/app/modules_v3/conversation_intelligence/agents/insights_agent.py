"""
💡 Insights Agent - Agente de Geração de Insights

Sintetiza análises de todos os agentes e gera:
- Insights acionáveis
- Recomendações específicas
- Alertas importantes
- Oportunidades identificadas
- Riscos detectados

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentContext, AgentResult


class InsightsAgent(BaseAgent):
    """Agente de síntese e geração de insights"""

    def get_name(self) -> str:
        return "InsightsAgent"

    def get_expertise(self) -> str:
        return "Síntese de análises e geração de insights acionáveis"

    def analyze(
        self, context: AgentContext, agent_results: List[AgentResult]
    ) -> AgentResult:
        """
        Sintetiza resultados de todos os agentes e gera insights.
        """
        start_time = time.time()
        errors = []

        try:
            # Extrair dados de cada agente
            insights_data = {
                "summary": self._generate_summary(agent_results),
                "key_insights": self._generate_key_insights(agent_results),
                "actionable_recommendations": self._generate_recommendations(
                    agent_results
                ),
                "alerts": self._generate_alerts(agent_results),
                "opportunities": self._identify_opportunities(agent_results),
                "risks": self._identify_risks(agent_results),
                "priority_score": self._calculate_priority_score(agent_results),
            }

            # === LLAMA 3.2 NATIVE INTEGRATION ===
            prompt = self._build_ollama_prompt(insights_data, context)
            ai_summary = self._ask_local_brain(
                prompt=prompt,
                system_prompt="Você é um especialista em vendas e inteligência de negócios sênior.",
            )
            if ai_summary:
                insights_data["ai_executive_summary"] = ai_summary
            # ====================================

            confidence = self._calculate_confidence(agent_results)
            processing_time = int((time.time() - start_time) * 1000)

            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=insights_data,
                confidence=confidence,
                processing_time_ms=processing_time,
                errors=errors,
            )

        except Exception as e:
            errors.append(str(e))
            return AgentResult(
                agent_name=self.get_name(),
                success=False,
                data={},
                confidence=0.0,
                processing_time_ms=int((time.time() - start_time) * 1000),
                errors=errors,
            )

    def _generate_summary(self, results: List[AgentResult]) -> Dict:
        """Gera resumo executivo"""
        return {
            "total_agents": len(results),
            "successful_analyses": sum(1 for r in results if r.success),
            "average_confidence": (
                sum(r.confidence for r in results) / len(results) if results else 0
            ),
            "processing_time_total": sum(r.processing_time_ms for r in results),
        }

    def _generate_key_insights(self, results: List[AgentResult]) -> List[Dict]:
        """Gera insights principais"""
        insights = []

        for result in results:
            if not result.success:
                continue

            # Extrair insights por agente
            if result.agent_name == "PsychologyAgent":
                data = result.data
                if data.get("emotions", {}).get("dominant_emotion"):
                    insights.append(
                        {
                            "category": "psicologia",
                            "insight": f"Emoção predominante: {data['emotions']['dominant_emotion']}",
                            "action": f"Adaptar comunicação para ressoar com {data['emotions']['dominant_emotion']}",
                            "priority": (
                                "alta"
                                if data["emotions"].get("emotional_intensity") == "alta"
                                else "média"
                            ),
                        }
                    )

                if data.get("personality", {}).get("dominant_type"):
                    insights.append(
                        {
                            "category": "personalidade",
                            "insight": f"Tipo DISC: {data['personality']['dominant_type']}",
                            "action": data.get("communication_style", {}).get(
                                "approach_recommendation", ""
                            ),
                            "priority": "média",
                        }
                    )

            elif result.agent_name == "SalesAgent":
                data = result.data
                if data.get("funnel_stage", {}).get("stage"):
                    insights.append(
                        {
                            "category": "vendas",
                            "insight": f"Estágio no funil: {data['funnel_stage']['stage']}",
                            "action": f"Avançar para próximo estágio: {data.get('next_steps', ['fechar venda'])[0]}",
                            "priority": (
                                "alta"
                                if data["funnel_stage"]["stage"] == "decision"
                                else "média"
                            ),
                        }
                    )

                if data.get("objections"):
                    for obj in data["objections"]:
                        insights.append(
                            {
                                "category": "vendas",
                                "insight": f"Objeção detectada: {obj['type']}",
                                "action": obj.get("handling_suggestion", ""),
                                "priority": "alta",
                            }
                        )

            elif result.agent_name == "BehaviorAgent":
                data = result.data
                if data.get("churn_risk", {}).get("risk_level") == "alto":
                    insights.append(
                        {
                            "category": "comportamento",
                            "insight": "Alto risco de churn detectado",
                            "action": "Intervenção imediata necessária",
                            "priority": "crítica",
                        }
                    )

                if data.get("loyalty_indicators", {}).get("loyalty_level") == "alto":
                    insights.append(
                        {
                            "category": "comportamento",
                            "insight": "Alta lealdade do cliente",
                            "action": "Considerar para programa de indicação",
                            "priority": "média",
                        }
                    )

        return insights

    def _generate_recommendations(self, results: List[AgentResult]) -> List[str]:
        """Gera recomendações acionáveis"""
        recommendations = []

        # Baseado em objeções
        sales_result = next((r for r in results if r.agent_name == "SalesAgent"), None)
        if sales_result and sales_result.data.get("objections"):
            for obj in sales_result.data["objections"]:
                recommendations.append(
                    f"Contornar objeção de {obj['type']}: {obj.get('handling_suggestion', '')}"
                )

        # Baseado em personalidade
        psych_result = next(
            (r for r in results if r.agent_name == "PsychologyAgent"), None
        )
        if psych_result:
            style = psych_result.data.get("communication_style", {})
            if style.get("approach_recommendation"):
                recommendations.append(
                    f"Estilo de comunicação: {style['approach_recommendation']}"
                )

        # Baseado em comportamento
        behavior_result = next(
            (r for r in results if r.agent_name == "BehaviorAgent"), None
        )
        if behavior_result:
            if behavior_result.data.get("churn_risk", {}).get("risk_level") == "alto":
                recommendations.append("URGENTE: Implementar ação de retenção")

        return recommendations

    def _generate_alerts(self, results: List[AgentResult]) -> List[Dict]:
        """Gera alertas importantes"""
        alerts = []

        for result in results:
            if not result.success:
                alerts.append(
                    {
                        "type": "erro",
                        "message": f"Falha na análise do agente {result.agent_name}",
                        "priority": "alta",
                    }
                )

        # Alertas específicos
        behavior_result = next(
            (r for r in results if r.agent_name == "BehaviorAgent"), None
        )
        if behavior_result:
            if behavior_result.data.get("churn_risk", {}).get("risk_level") == "alto":
                alerts.append(
                    {
                        "type": "churn",
                        "message": "Cliente em alto risco de abandono",
                        "priority": "crítica",
                    }
                )

        return alerts

    def _identify_opportunities(self, results: List[AgentResult]) -> List[Dict]:
        """Identifica oportunidades"""
        opportunities = []

        # Upsell
        sales_result = next((r for r in results if r.agent_name == "SalesAgent"), None)
        if sales_result:
            if sales_result.data.get("potential_value", {}).get("upsell_opportunity"):
                opportunities.append(
                    {
                        "type": "upsell",
                        "description": "Oportunidade de vender serviços adicionais",
                        "estimated_value": sales_result.data["potential_value"].get(
                            "estimated_value", 0
                        ),
                        "priority": "média",
                    }
                )

            # Alta probabilidade de conversão
            if (
                sales_result.data.get("conversion_probability", {}).get(
                    "probability", 0
                )
                > 70
            ):
                opportunities.append(
                    {
                        "type": "conversao",
                        "description": "Alta probabilidade de fechamento",
                        "probability": sales_result.data["conversion_probability"][
                            "probability"
                        ],
                        "priority": "alta",
                    }
                )

        # Advocacy
        behavior_result = next(
            (r for r in results if r.agent_name == "BehaviorAgent"), None
        )
        if behavior_result:
            if (
                behavior_result.data.get("loyalty_indicators", {}).get(
                    "advocacy_potential"
                )
                == "alto"
            ):
                opportunities.append(
                    {
                        "type": "advocacy",
                        "description": "Cliente potencialmente promotor da marca",
                        "priority": "média",
                    }
                )

        return opportunities

    def _identify_risks(self, results: List[AgentResult]) -> List[Dict]:
        """Identifica riscos"""
        risks = []

        # Churn
        behavior_result = next(
            (r for r in results if r.agent_name == "BehaviorAgent"), None
        )
        if behavior_result:
            churn = behavior_result.data.get("churn_risk", {})
            if churn.get("risk_level") in ["alto", "médio"]:
                risks.append(
                    {
                        "type": "churn",
                        "description": f"Risco de churn: {churn.get('risk_level')}",
                        "score": churn.get("risk_score", 0),
                        "priority": (
                            "alta" if churn.get("risk_level") == "alto" else "média"
                        ),
                    }
                )

        # Objeções não resolvidas
        sales_result = next((r for r in results if r.agent_name == "SalesAgent"), None)
        if sales_result:
            objections = sales_result.data.get("objections", [])
            if len(objections) > 2:
                risks.append(
                    {
                        "type": "objecoes",
                        "description": f"Múltiplas objeções detectadas ({len(objections)})",
                        "priority": "alta",
                    }
                )

        # Emoção negativa
        psych_result = next(
            (r for r in results if r.agent_name == "PsychologyAgent"), None
        )
        if psych_result:
            emotions = psych_result.data.get("emotions", {})
            if emotions.get("dominant_emotion") in ["raiva", "tristeza", "nojo"]:
                risks.append(
                    {
                        "type": "emocao_negativa",
                        "description": f"Emoção negativa predominante: {emotions['dominant_emotion']}",
                        "priority": "alta",
                    }
                )

        return risks

    def _calculate_priority_score(self, results: List[AgentResult]) -> Dict:
        """Calcula score de prioridade da conversa"""
        score = 50  # Base

        # Aumentar score para alta probabilidade de conversão
        sales_result = next((r for r in results if r.agent_name == "SalesAgent"), None)
        if sales_result:
            conv_prob = sales_result.data.get("conversion_probability", {}).get(
                "probability", 0
            )
            score += conv_prob * 0.3

        # Diminuir score para alto risco de churn
        behavior_result = next(
            (r for r in results if r.agent_name == "BehaviorAgent"), None
        )
        if behavior_result:
            churn_risk = behavior_result.data.get("churn_risk", {}).get("risk_score", 0)
            score -= churn_risk * 0.3

        # Aumentar score para alto valor potencial
        if sales_result:
            potential_value = sales_result.data.get("potential_value", {}).get(
                "estimated_value", 0
            )
            score += min(20, potential_value / 50)

        score = max(0, min(100, score))

        return {
            "score": score,
            "level": "alta" if score > 70 else "média" if score > 40 else "baixa",
            "factors": {
                "conversion_probability": (
                    sales_result.data.get("conversion_probability", {}).get(
                        "probability", 0
                    )
                    if sales_result
                    else 0
                ),
                "churn_risk": (
                    behavior_result.data.get("churn_risk", {}).get("risk_score", 0)
                    if behavior_result
                    else 0
                ),
                "potential_value": (
                    sales_result.data.get("potential_value", {}).get(
                        "estimated_value", 0
                    )
                    if sales_result
                    else 0
                ),
            },
        }

    def _calculate_confidence(self, results: List[AgentResult]) -> float:
        """Calcula confiança da síntese"""
        if not results:
            return 0.0

        successful = sum(1 for r in results if r.success)
        avg_confidence = (
            sum(r.confidence for r in results if r.success) / successful
            if successful > 0
            else 0
        )

        return avg_confidence * (successful / len(results))

    def _build_ollama_prompt(self, insights_data: Dict, context: AgentContext) -> str:
        """Constrói o prompt rico para a rede neural local."""
        texto_cliente = " ".join(
            [
                m.get("content", "")
                for m in context.messages
                if m.get("direction") == "inbound"
            ]
        )

        return f"""
Analise os seguintes dados extraídos de uma conversa de WhatsApp com um cliente e forneça um resumo executivo inteligente e estratégico (máximo 3 parágrafos curtos) focado em FECHAMENTO DE VENDAS e RETENÇÃO.

COMPORTAMENTO BRUTO DETECTADO:
- Prioridade da Conversa: {insights_data.get('priority_score', {}).get('level')} ({insights_data.get('priority_score', {}).get('score')}/100)
- Alertas Importantes: {len(insights_data.get('alerts', []))}
- Oportunidades: {len(insights_data.get('opportunities', []))}
- Recomendações Técnicas: {', '.join(insights_data.get('actionable_recommendations', []))}

TEXTO ORIGINAL DO CLIENTE:
"{texto_cliente}"

Gere um insight profundo sobre qual deve ser a exata próxima mensagem humana enviada para este cliente para maximizar a conversão ou evitar o cancelamento.
"""
