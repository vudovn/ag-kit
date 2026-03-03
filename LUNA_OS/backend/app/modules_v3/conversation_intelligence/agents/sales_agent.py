"""
💰 Sales Agent - Agente de Análise de Vendas

Analisa conversas sob perspectiva de vendas:
- Estágio no funil (awareness, consideration, decision)
- Objeções identificadas
- Técnicas de vendas usadas
- Probabilidade de conversão
- Valor potencial do negócio
- Próximos passos recomendados

Baseado em:
- SPIN Selling (Neil Rackham)
- Challenger Sale
- Funil de Vendas tradicional
- Gatilhos de compra

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentContext, AgentResult


class SalesAgent(BaseAgent):
    """Agente especializado em análise de vendas"""
    
    # Estágios do funil
    FUNNEL_STAGES = {
        "awareness": ["o que é", "como funciona", "vocês fazem", "tem", "fazem"],
        "interest": ["quero saber", "me conta", "informações", "detalhes", "preço", "valor"],
        "consideration": ["agendar", "marcar", "horário", "disponível", "quando"],
        "decision": ["fechar", "confirmar", "pagar", "forma pagamento", "faço"],
        "retention": ["voltar", "próxima", "manutenção", "retorno", "gostei"],
    }
    
    # Objeções comuns
    OBJECTIONS = {
        "preco": ["caro", "preço", "valor", "custo", "pagar", "não tenho", "nao tenho"],
        "tempo": ["demora", "tempo", "não tenho tempo", "nao tenho tempo", "correria"],
        "confianca": ["será", "funciona mesmo", "já ouvi", "recomendam", "confio"],
        "necessidade": ["preciso mesmo", "realmente", "vou pensar", "verificar"],
        "autoridade": ["marido", "esposo", "chefe", "perguntar", "ver com"],
    }
    
    # Sinais de compra
    BUYING_SIGNALS = [
        "quero", "faço", "fecho", "agendo", "marco", "posso", "como funciona",
        "forma pagamento", "desconto", "tem garantia", "quando posso", "próximo",
        "recomendo", "indico", "volto",
    ]
    
    def get_name(self) -> str:
        return "SalesAgent"
    
    def get_expertise(self) -> str:
        return "Análise de vendas: funil, objeções, conversão, técnicas"
    
    def analyze(self, context: AgentContext) -> AgentResult:
        start_time = time.time()
        errors = []
        
        try:
            client_messages = [m.get("content", "") for m in context.messages if m.get("direction") == "inbound"]
            full_text = " ".join(client_messages).lower()
            
            sales_data = {
                "funnel_stage": self._identify_funnel_stage(full_text),
                "objections": self._identify_objections(full_text),
                "buying_signals": self._identify_buying_signals(full_text),
                "conversion_probability": self._calculate_conversion_probability(full_text, client_messages),
                "potential_value": self._estimate_potential_value(full_text),
                "next_steps": self._recommend_next_steps(full_text),
                "sales_techniques_used": self._identify_sales_techniques(context.messages),
            }
            
            confidence = self._calculate_confidence(sales_data)
            processing_time = int((time.time() - start_time) * 1000)
            
            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=sales_data,
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
    
    def _identify_funnel_stage(self, text: str) -> Dict:
        stage_scores = {
            stage: sum(text.count(kw) for kw in keywords)
            for stage, keywords in self.FUNNEL_STAGES.items()
        }
        
        dominant_stage = max(stage_scores, key=stage_scores.get) if any(stage_scores.values()) else "unknown"
        
        stage_descriptions = {
            "awareness": "Cliente descobrindo serviços",
            "interest": "Cliente demonstrando interesse",
            "consideration": "Cliente considerando agendar",
            "decision": "Cliente pronto para fechar",
            "retention": "Cliente fidelizado",
            "unknown": "Estágio indeterminado",
        }
        
        return {
            "stage": dominant_stage,
            "description": stage_descriptions.get(dominant_stage, ""),
            "scores": stage_scores,
            "confidence": stage_scores[dominant_stage] / sum(stage_scores.values()) if sum(stage_scores.values()) > 0 else 0.3,
        }
    
    def _identify_objections(self, text: str) -> List[Dict]:
        objections_found = []
        
        for objection_type, keywords in self.OBJECTIONS.items():
            count = sum(text.count(kw) for kw in keywords)
            if count > 0:
                objections_found.append({
                    "type": objection_type,
                    "count": count,
                    "strength": "forte" if count > 2 else "média" if count > 0 else "fraca",
                    "handling_suggestion": self._get_objection_handling(objection_type),
                })
        
        return objections_found
    
    def _get_objection_handling(self, objection_type: str) -> str:
        suggestions = {
            "preco": "Destaque valor, não preço. Ofereça parcelamento.",
            "tempo": "Mostre eficiência. Ofereça horários flexíveis.",
            "confianca": "Apresente depoimentos, garantias, portfólio.",
            "necessidade": "Faça perguntas SPIN. Descubra dor real.",
            "autoridade": "Ofereça material para decisão em conjunto.",
        }
        return suggestions.get(objection_type, "Entenda a objeção e contorne com benefícios.")
    
    def _identify_buying_signals(self, text: str) -> Dict:
        signals_found = [signal for signal in self.BUYING_SIGNALS if signal in text]
        
        return {
            "signals": signals_found,
            "count": len(signals_found),
            "strength": "forte" if len(signals_found) > 3 else "média" if len(signals_found) > 1 else "fraca",
            "readiness": "alto" if len(signals_found) > 3 else "médio" if len(signals_found) > 1 else "baixo",
        }
    
    def _calculate_conversion_probability(self, text: str, messages: List[str]) -> Dict:
        # Fatores que aumentam conversão
        positive_factors = 0
        
        # Tem sinal de compra
        if any(signal in text for signal in self.BUYING_SIGNALS):
            positive_factors += 30
        
        # Está em estágio avançado
        if "decision" in text or "agendar" in text or "marcar" in text:
            positive_factors += 25
        
        # Fez pergunta específica
        if "?" in text:
            positive_factors += 15
        
        # Usou linguagem positiva
        if any(kw in text for kw in ["quero", "amei", "ótimo", "perfeito"]):
            positive_factors += 20
        
        # Sem objeções fortes
        has_objection = any(any(kw in text for kw in keywords) for keywords in self.OBJECTIONS.values())
        if not has_objection:
            positive_factors += 10
        
        probability = min(100, positive_factors)
        
        return {
            "probability": probability,
            "level": "alta" if probability > 70 else "média" if probability > 40 else "baixa",
            "factors": positive_factors,
        }
    
    def _estimate_potential_value(self, text: str) -> Dict:
        # Estimativa baseada em palavras-chave de serviços
        service_values = {
            "progressiva": 300,
            "corte": 150,
            "escova": 60,
            "manicure": 45,
            "pedicure": 55,
            "gel": 130,
            "make": 150,
            "sobrancelh": 60,
        }
        
        estimated_value = 0
        services_mentioned = []
        
        for service, value in service_values.items():
            if service in text:
                estimated_value += value
                services_mentioned.append(service)
        
        return {
            "estimated_value": estimated_value,
            "services_mentioned": services_mentioned,
            "upsell_opportunity": estimated_value > 0 and len(services_mentioned) < 2,
        }
    
    def _recommend_next_steps(self, text: str) -> List[str]:
        recommendations = []
        
        # Baseado no estágio
        if any(kw in text for kw in self.FUNNEL_STAGES["awareness"]):
            recommendations.append("Educar sobre serviços e benefícios")
        
        if any(kw in text for kw in self.FUNNEL_STAGES["interest"]):
            recommendations.append("Fornecer informações detalhadas e preços")
        
        if any(kw in text for kw in self.FUNNEL_STAGES["consideration"]):
            recommendations.append("Oferecer horários disponíveis")
        
        if any(kw in text for kw in self.FUNNEL_STAGES["decision"]):
            recommendations.append("Fechar agendamento e confirmar")
        
        # Baseado em objeções
        if any(kw in text for kw in self.OBJECTIONS["preco"]):
            recommendations.append("Contornar objeção de preço com valor")
        
        # Call to action
        if not recommendations:
            recommendations.append("Fazer pergunta aberta para entender necessidade")
        
        return recommendations
    
    def _identify_sales_techniques(self, messages: List[Dict]) -> Dict:
        # Analisa mensagens da atendente
        outbound = [m.get("content", "").lower() for m in messages if m.get("direction") == "outbound"]
        full_outbound = " ".join(outbound)
        
        techniques = {
            "spinning": sum(full_outbound.count(kw) for kw in ["como", "o que", "qual", "por que", "quando"]),
            "active_listening": sum(full_outbound.count(kw) for kw in ["entendo", "compreendo", "percebo", "vejo"]),
            "rapport_building": sum(full_outbound.count(kw) for kw in ["😊", "😍", "linda", "querida", "amor"]),
            "urgency_creation": sum(full_outbound.count(kw) for kw in ["hoje", "agora", "último", "acaba"]),
            "social_proof": sum(full_outbound.count(kw) for kw in ["outras", "clientes", "adoram", "recomendam"]),
        }
        
        return {
            "techniques": techniques,
            "most_used": max(techniques, key=techniques.get) if techniques else "none",
            "effectiveness": "alta" if sum(techniques.values()) > 10 else "média" if sum(techniques.values()) > 5 else "baixa",
        }
    
    def _calculate_confidence(self, sales_data: Dict) -> float:
        factors = []
        
        # Confiança baseada em dados disponíveis
        factors.append(1.0 if sales_data.get("funnel_stage", {}).get("stage") != "unknown" else 0.3)
        factors.append(min(1.0, len(sales_data.get("objections", [])) / 3))
        factors.append(min(1.0, sales_data.get("buying_signals", {}).get("count", 0) / 5))
        
        return self._calculate_confidence(factors)
