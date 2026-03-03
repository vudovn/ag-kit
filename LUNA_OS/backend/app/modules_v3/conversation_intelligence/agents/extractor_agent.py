"""
📥 Extractor Agent - Agente de Extração de Dados

Responsável por extrair dados estruturados das conversas brutas do WhatsApp.
Extrai:
- Informações do cliente (nome, phone, perfil)
- Serviços mencionados
- Profissionais mencionados
- Datas e horários
- Valores e preços
- Intenções detectadas
- Metadados da conversa

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import re
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from loguru import logger

from .base_agent import BaseAgent, AgentContext, AgentResult


class ExtractorAgent(BaseAgent):
    """
    Agente especializado em extração de dados estruturados de conversas.
    
    Usa regex, NLP básico e pattern matching para identificar:
    - Entidades nomeadas (serviços, profissionais, clientes)
    - Informações temporais (datas, horários)
    - Informações numéricas (preços, quantidades)
    - Intenções e sentimentos
    """
    
    # Patterns para extração
    PATTERNS = {
        "phone": r"\d{10,11}",
        "money": r"R?\$?\s?\d+[,.]\d{2}",
        "time": r"\d{1,2}[:h]\d{2}",
        "date": r"\d{1,2}[/-]\d{1,2}[/-]?\d{2,4}?",
        "quantity": r"\d+\s*(vezes|unidades|pacotes)",
    }
    
    # Keywords por categoria
    KEYWORDS = {
        "servicos_cabelo": [
            "escova", "progressiva", "corte", "hidratação", "hidratacao",
            "nutrição", "nutricao", "reconstrução", "reconstrucao",
            "tintura", "mechas", "luzes", "alisamento", "ondulado",
            "babyliss", "chapinha", "pentead", "tranç", "tranca"
        ],
        "servicos_unhas": [
            "manicure", "pedicure", "unha", "gel", "acrílico", "acrilico",
            "fibra", "blindagem", "esmalte", "cutilagem", "russa"
        ],
        "servicos_estetica": [
            "maquiagem", "make", "sobrancelh", "design", "henna",
            "epilação", "epilacao", "lash", "brow", "laminação", "laminacao"
        ],
        "profissionais": [
            "ju", "yujaira", "carla", "davila", "dávil", "tay", "lu",
            "luisa", "edna", "sheydis", "suzana", "cintia"
        ],
        "saudacao": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "hey"],
        "agradecimento": ["obrigado", "obrigada", "valeu", "thanks", "vlw", "grata"],
        "objecao": ["caro", "demora", "não posso", "nao posso", "vou pensar", "verificar"],
        "urgencia": ["hoje", "agora", "urgente", "preciso", "amanhã", "amanha"],
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Carrega base de conhecimento (serviços, profissionais, etc.)"""
        # Aqui poderia carregar de JSON, banco de dados, etc.
        self.knowledge = {
            "services": [],
            "professionals": [],
            "coupons": [],
        }
    
    def get_name(self) -> str:
        return "ExtractorAgent"
    
    def get_expertise(self) -> str:
        return "Extração de dados estruturados de conversas WhatsApp"
    
    def analyze(self, context: AgentContext) -> AgentResult:
        """
        Analisa conversa e extrai dados estruturados.
        
        Pipeline de extração:
        1. Extrair metadados da conversa
        2. Extrair informações do cliente
        3. Extrair serviços mencionados
        4. Extrair profissionais mencionados
        5. Extrair informações temporais
        6. Extrair valores monetários
        7. Detectar intenções
        8. Calcular métricas
        """
        start_time = time.time()
        errors = []
        warnings = []
        
        try:
            # Concatenar todas as mensagens
            full_text = self._concatenate_messages(context.messages)
            
            # Extrair dados
            extracted_data = {
                "metadata": self._extract_metadata(context, context.messages),
                "client_info": self._extract_client_info(context, full_text),
                "services": self._extract_services(full_text),
                "professionals": self._extract_professionals(full_text),
                "temporal": self._extract_temporal_info(full_text),
                "monetary": self._extract_monetary_info(full_text),
                "intents": self._extract_intents(full_text, context.messages),
                "metrics": self._calculate_metrics(context.messages),
            }
            
            # Calcular confiança
            confidence = self._calculate_confidence_score(extracted_data)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=extracted_data,
                confidence=confidence,
                processing_time_ms=processing_time,
                errors=errors,
                warnings=warnings,
            )
            
        except Exception as e:
            self._log_error("Falha na extração", e)
            errors.append(str(e))
            
            return AgentResult(
                agent_name=self.get_name(),
                success=False,
                data={},
                confidence=0.0,
                processing_time_ms=int((time.time() - start_time) * 1000),
                errors=errors,
                warnings=warnings,
            )
    
    def _concatenate_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Concatena todas as mensagens em um único texto"""
        return " ".join([msg.get("content", "") for msg in messages])
    
    def _extract_metadata(self, context: AgentContext, messages: List[Dict]) -> Dict:
        """Extrai metadados da conversa"""
        inbound_count = sum(1 for m in messages if m.get("direction") == "inbound")
        outbound_count = sum(1 for m in messages if m.get("direction") == "outbound")
        
        # Calcular tempo médio de resposta
        response_times = []
        for i in range(1, len(messages)):
            # Simplificado - em produção usaria timestamps reais
            response_times.append(1)  # Placeholder
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "conversation_id": context.conversation_id,
            "phone": context.phone,
            "total_messages": len(messages),
            "inbound_messages": inbound_count,
            "outbound_messages": outbound_count,
            "avg_response_time": avg_response_time,
            "conversation_date": context.timestamp,
        }
    
    def _extract_client_info(self, context: AgentContext, text: str) -> Dict:
        """Extrai informações do cliente"""
        # Detectar nome (simplificado - em produção usaria NLP)
        name = context.client_name or "Desconhecido"
        
        # Detectar gênero baseado em palavras
        feminine_words = ["obrigada", "grata", "quero", "gostaria"]
        masculine_words = ["obrigado", "grato", "quero", "gostaria"]
        
        feminine_count = sum(text.lower().count(w) for w in feminine_words)
        masculine_count = sum(text.lower().count(w) for w in masculine_words)
        
        inferred_gender = "feminino" if feminine_count > masculine_count else "masculino"
        
        return {
            "name": name,
            "phone": context.phone,
            "inferred_gender": inferred_gender,
            "is_new_client": "nova" in context.metadata.get("tags", []),
        }
    
    def _extract_services(self, text: str) -> List[Dict]:
        """Extrai serviços mencionados"""
        text_lower = text.lower()
        found_services = []
        
        # Buscar serviços de cabelo
        for service in self.KEYWORDS["servicos_cabelo"]:
            if service in text_lower:
                found_services.append({
                    "name": service,
                    "category": "cabelo",
                    "confidence": 0.8,
                })
        
        # Buscar serviços de unhas
        for service in self.KEYWORDS["servicos_unhas"]:
            if service in text_lower:
                found_services.append({
                    "name": service,
                    "category": "unhas",
                    "confidence": 0.8,
                })
        
        # Buscar serviços de estética
        for service in self.KEYWORDS["servicos_estetica"]:
            if service in text_lower:
                found_services.append({
                    "name": service,
                    "category": "estetica",
                    "confidence": 0.8,
                })
        
        # Remover duplicatas
        unique_services = {s["name"]: s for s in found_services}.values()
        
        return list(unique_services)
    
    def _extract_professionals(self, text: str) -> List[Dict]:
        """Extrai profissionais mencionados"""
        text_lower = text.lower()
        found_professionals = []
        
        for prof in self.KEYWORDS["profissionais"]:
            if prof in text_lower:
                found_professionals.append({
                    "name": prof,
                    "confidence": 0.9,
                })
        
        return found_professionals
    
    def _extract_temporal_info(self, text: str) -> Dict:
        """Extrai informações temporais (datas, horários)"""
        temporal_data = {
            "dates_mentioned": [],
            "times_mentioned": [],
            "urgency_detected": False,
            "time_references": [],
        }
        
        # Detectar urgência
        urgency_words = ["hoje", "agora", "urgente", "amanhã", "amanha", "já", "ja"]
        temporal_data["urgency_detected"] = any(word in text.lower() for word in urgency_words)
        
        # Extrair horários (pattern simples)
        time_pattern = r"\d{1,2}[:h]\d{2}"
        times = re.findall(time_pattern, text)
        temporal_data["times_mentioned"] = times
        
        # Extrair datas (pattern simples)
        date_pattern = r"\d{1,2}[/-]\d{1,2}"
        dates = re.findall(date_pattern, text)
        temporal_data["dates_mentioned"] = dates
        
        # Detectar referências temporais
        if "manhã" in text.lower() or "manha" in text.lower():
            temporal_data["time_references"].append("manha")
        if "tarde" in text.lower():
            temporal_data["time_references"].append("tarde")
        if "noite" in text.lower():
            temporal_data["time_references"].append("noite")
        if "fim de semana" in text.lower() or "final de semana" in text.lower():
            temporal_data["time_references"].append("fim_de_semana")
        
        return temporal_data
    
    def _extract_monetary_info(self, text: str) -> Dict:
        """Extrai informações monetárias (preços, valores)"""
        monetary_data = {
            "values_mentioned": [],
            "price_concern": False,
            "discount_mentioned": False,
        }
        
        # Extrair valores (R$, $, etc.)
        money_pattern = r"R?\$?\s?\d+[,.]\d{2}"
        values = re.findall(money_pattern, text)
        monetary_data["values_mentioned"] = values
        
        # Detectar preocupação com preço
        price_concern_words = ["caro", "barato", "preço", "valor", "custo", "pagar"]
        monetary_data["price_concern"] = any(word in text.lower() for word in price_concern_words)
        
        # Detectar menção a desconto
        discount_words = ["desconto", "promoção", "promo", "oferta", "barato"]
        monetary_data["discount_mentioned"] = any(word in text.lower() for word in discount_words)
        
        return monetary_data
    
    def _extract_intents(self, text: str, messages: List[Dict]) -> List[Dict]:
        """Extrai intenções detectadas"""
        text_lower = text.lower()
        intents = []
        
        # Detectar intenção de agendamento
        if any(word in text_lower for word in ["agendar", "marcar", "horário", "vaga"]):
            intents.append({
                "type": "agendamento",
                "confidence": 0.9,
                "stage": "interesse",
            })
        
        # Detectar intenção de preço
        if any(word in text_lower for word in ["quanto", "preço", "valor", "custa"]):
            intents.append({
                "type": "consulta_preco",
                "confidence": 0.9,
                "stage": "consideracao",
            })
        
        # Detectar objeção
        if any(word in text_lower for word in self.KEYWORDS["objecao"]):
            intents.append({
                "type": "objecao",
                "confidence": 0.8,
                "stage": "objecao",
            })
        
        # Detectar urgência
        if any(word in text_lower for word in self.KEYWORDS["urgencia"]):
            intents.append({
                "type": "urgencia",
                "confidence": 0.85,
                "stage": "decisao",
            })
        
        return intents
    
    def _calculate_metrics(self, messages: List[Dict]) -> Dict:
        """Calcula métricas da conversa"""
        if not messages:
            return {}
        
        # Contar mensagens por direção
        inbound = sum(1 for m in messages if m.get("direction") == "inbound")
        outbound = sum(1 for m in messages if m.get("direction") == "outbound")
        
        # Calcular razão cliente/atendente
        ratio = inbound / outbound if outbound > 0 else 0
        
        # Detectar tamanho da conversa
        conversation_size = "curta" if len(messages) < 5 else "média" if len(messages) < 15 else "longa"
        
        return {
            "total_messages": len(messages),
            "inbound_count": inbound,
            "outbound_count": outbound,
            "client_atendente_ratio": ratio,
            "conversation_size": conversation_size,
            "engagement_score": min(100, len(messages) * 5),  # Score simples
        }
    
    def _calculate_confidence_score(self, extracted_data: Dict) -> float:
        """Calcula confiança geral da extração"""
        factors = []
        
        # Fator 1: Quantidade de serviços extraídos
        services_count = len(extracted_data.get("services", []))
        factors.append(min(1.0, services_count / 3))  # Normalizado
        
        # Fator 2: Quantidade de intenções detectadas
        intents_count = len(extracted_data.get("intents", []))
        factors.append(min(1.0, intents_count / 2))
        
        # Fator 3: Metadados completos
        metadata = extracted_data.get("metadata", {})
        metadata_completeness = sum(1 for v in metadata.values() if v) / len(metadata) if metadata else 0
        factors.append(metadata_completeness)
        
        # Fator 4: Informações temporais
        temporal = extracted_data.get("temporal", {})
        has_temporal = bool(temporal.get("dates_mentioned") or temporal.get("times_mentioned"))
        factors.append(1.0 if has_temporal else 0.5)
        
        return self._calculate_confidence(factors)
