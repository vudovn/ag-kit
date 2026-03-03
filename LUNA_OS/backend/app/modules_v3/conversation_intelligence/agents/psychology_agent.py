"""
🧠 Psychology Agent - Agente de Análise Psicológica

Responsável por analisar aspectos psicológicos das conversas:
- Emoções e sentimentos
- Personalidade do cliente (DISC, Big Five)
- Gatilhos mentais identificados
- Estado emocional
- Necessidades psicológicas
- Padrões de comunicação

Baseado em:
- Psicologia das Emoções (Paul Ekman)
- Big Five Personality Traits
- DISC Assessment
- PNL (Programação Neurolinguística)
- Gatilhos Mentais (Robert Cialdini)

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import re
import time
from typing import Dict, List, Any, Optional
from loguru import logger

from .base_agent import BaseAgent, AgentContext, AgentResult


class PsychologyAgent(BaseAgent):
    """
    Agente especializado em análise psicológica de conversas.
    
    Analisa:
    - Emoções predominantes (alegria, tristeza, raiva, medo, surpresa, nojo)
    - Tipo de personalidade (DISC: Dominância, Influência, Estabilidade, Conformidade)
    - Gatilhos mentais ativados (urgência, escassez, autoridade, etc.)
    - Estado emocional (calmo, ansioso, frustrado, empolgado)
    - Necessidades (segurança, pertencimento, reconhecimento, autoestima)
    - Estilo de comunicação (direto, detalhista, emocional, racional)
    """
    
    # Emoções básicas (Paul Ekman)
    EMOTION_KEYWORDS = {
        "alegria": [
            "feliz", "alegre", "ótimo", "maravilhoso", "perfeito", "amei", "adoro",
            "incrível", "fantástico", "excelente", "bom", "legal", "joia", "😊", "😍", "🥰"
        ],
        "tristeza": [
            "triste", "chateado", "decepcionado", "péssimo", "ruim", "infeliz",
            "desanimado", "desapontado", "😢", "😞", "😔"
        ],
        "raiva": [
            "raiva", "bravo", "irritado", "puto", "puta", "ódio", "odeio",
            "inaceitável", "absurdo", "revoltado", "😠", "😡", "🤬"
        ],
        "medo": [
            "medo", "receio", "preocupado", "ansioso", "nervoso", "tenso",
            "assustado", "apreensivo", "inseguro", "😰", "😨", "😱"
        ],
        "surpresa": [
            "surpreso", "surpresa", "uau", "nossa", "caramba", "incrível",
            "não acredito", "impressionado", "😮", "😯", "😲"
        ],
        "nojo": [
            "nojo", "nojento", "horrível", "terrível", "péssimo", "😷", "🤢", "🤮"
        ],
    }
    
    # Gatilhos mentais (Cialdini)
    MENTAL_TRIGGERS = {
        "urgencia": [
            "hoje", "agora", "já", "ja", "urgente", "imediat", "última", "ultima",
            "acaba", "termina", "corre", "rápido", "rapido"
        ],
        "escassez": [
            "pouco", "poucos", "última", "ultima", "únicos", "unicos", "restante",
            "acabando", "esgotando", "limitado", "exclusivo"
        ],
        "autoridade": [
            "especialista", "profissional", "experiente", "recomendado", "indicação",
            "melhor", "top", "premium", "master", "senior"
        ],
        "prova_social": [
            "todo mundo", "todos", "muita gente", "popular", "famoso", "viral",
            "recomendam", "indicam", "amam", "adoram"
        ],
        "reciprocidade": [
            "presente", "brinde", "bônus", "bonus", "desconto", "cortesia",
            "oferta", "promoção", "promo", "grátis", "gratis"
        ],
        "compromisso": [
            "garantia", "compromisso", "confiança", "seguro", "certeza",
            "pode confiar", "garantido", "assegurado"
        ],
        "afinidade": [
            "igual", "mesmo", "parecido", "semelhante", "como você", "também",
            "nós", "gente", "aqui", "nosso", "nosso"
        ],
    }
    
    # Indicadores DISC
    DISC_INDICATORS = {
        "dominancia": [
            "quero", "preciso", "exijo", "faça", "agora", "já", "ja", "decida",
            "direto", "objetivo", "resultado", "eficiente", "rápido", "rapido"
        ],
        "influencia": [
            "adoro", "amei", "maravilhoso", "fantástico", "incrível", "social",
            "amigos", "gente", "pessoas", "divertido", "legal", "top"
        ],
        "estabilidade": [
            "calma", "tranquilo", "seguro", "confiável", "sempre", "costumo",
            "habitual", "tradicional", "conhecido", "paz", "sossegado"
        ],
        "conformidade": [
            "preciso", "exato", "detalhe", "informação", "documento", "regra",
            "padrão", "qualidade", "técnico", "especificação", "correto"
        ],
    }
    
    # Necessidades psicológicas
    PSYCHOLOGICAL_NEEDS = {
        "seguranca": [
            "seguro", "segurança", "confiança", "garantia", "proteção", "proteccao",
            "risco", "cuidado", "atenção", "atencao"
        ],
        "pertencimento": [
            "grupo", "parte", "junto", "comunidade", "time", "equipe", "nós",
            "nosso", "aceito", "aceitação", "incluso"
        ],
        "reconhecimento": [
            "especial", "único", "unico", "importante", "valorizado", "reconhecido",
            "elogio", "parabéns", "parabens", "mérito", "merito"
        ],
        "autoestima": [
            "bonito", "beleza", "lindo", "maravilhoso", "confiante", "autoestima",
            "eleva", "melhora", "realizado", "feliz"
        ],
        "controle": [
            "decido", "escolho", "controlo", "comando", "decisão", "escolha",
            "poder", "opção", "opcao", "liberdade"
        ],
    }
    
    # Estilos de comunicação
    COMMUNICATION_STYLES = {
        "direto": [
            "quero", "preciso", "faça", "manda", "envia", "agora", "já", "ja",
            "direto", "objetivo", "resumo", "curto"
        ],
        "detalhista": [
            "detalhe", "informação", "informacoes", "explica", "como", "porque",
            "por que", "qual", "quando", "onde", "especifico"
        ],
        "emocional": [
            "sinto", "acho", "parece", "emoção", "emocao", "sentimento", "amo",
            "odeio", "adoro", "detesto", "feliz", "triste"
        ],
        "racional": [
            "lógico", "logico", "razão", "razao", "concordo", "discordo", "análise",
            "analise", "estudo", "pesquisa", "dados", "números", "numeros"
        ],
    }
    
    def get_name(self) -> str:
        return "PsychologyAgent"
    
    def get_expertise(self) -> str:
        return "Análise psicológica: emoções, personalidade, gatilhos mentais, necessidades"
    
    def analyze(self, context: AgentContext) -> AgentResult:
        """
        Analisa aspectos psicológicos da conversa.
        
        Pipeline:
        1. Extrair texto completo
        2. Analisar emoções predominantes
        3. Identificar tipo de personalidade (DISC)
        4. Detectar gatilhos mentais
        5. Identificar necessidades psicológicas
        6. Determinar estilo de comunicação
        7. Calcular estado emocional geral
        """
        start_time = time.time()
        errors = []
        warnings = []
        
        try:
            full_text = self._concatenate_messages(context.messages)
            client_messages = self._get_client_messages(context.messages)
            
            psychology_data = {
                "emotions": self._analyze_emotions(client_messages),
                "personality": self._analyze_personality(client_messages),
                "mental_triggers": self._analyze_mental_triggers(client_messages),
                "psychological_needs": self._analyze_psychological_needs(client_messages),
                "communication_style": self._analyze_communication_style(client_messages),
                "emotional_state": self._determine_emotional_state(client_messages),
                "rapport_indicators": self._analyze_rapport(client_messages),
            }
            
            confidence = self._calculate_confidence_score(psychology_data, len(client_messages))
            processing_time = int((time.time() - start_time) * 1000)
            
            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=psychology_data,
                confidence=confidence,
                processing_time_ms=processing_time,
                errors=errors,
                warnings=warnings,
            )
            
        except Exception as e:
            self._log_error("Falha na análise psicológica", e)
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
    
    def _concatenate_messages(self, messages: List[Dict]) -> str:
        """Concatena mensagens do cliente"""
        return " ".join([m.get("content", "") for m in messages if m.get("direction") == "inbound"])
    
    def _get_client_messages(self, messages: List[Dict]) -> List[str]:
        """Retorna apenas mensagens do cliente"""
        return [m.get("content", "") for m in messages if m.get("direction") == "inbound"]
    
    def _analyze_emotions(self, messages: List[str]) -> Dict:
        """Analisa emoções predominantes"""
        text = " ".join(messages).lower()
        
        emotion_scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(text.count(kw.lower()) for kw in keywords)
            emotion_scores[emotion] = score
        
        # Normalizar scores
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v / total for k, v in emotion_scores.items()}
        
        # Identificar emoção predominante
        dominant_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else "neutro"
        
        return {
            "scores": emotion_scores,
            "dominant_emotion": dominant_emotion,
            "emotional_intensity": "alta" if total > 5 else "média" if total > 2 else "baixa",
            "emoji_usage": sum(1 for c in " ".join(messages) if c in "😊😍🥰😢😞😔😠😡🤬😰😨😱😮😯😲😷🤢🤮"),
        }
    
    def _analyze_personality(self, messages: List[str]) -> Dict:
        """Analisa tipo de personalidade (DISC)"""
        text = " ".join(messages).lower()
        
        disc_scores = {}
        for trait, keywords in self.DISC_INDICATORS.items():
            score = sum(text.count(kw.lower()) for kw in keywords)
            disc_scores[trait] = score
        
        # Normalizar
        total = sum(disc_scores.values())
        if total > 0:
            disc_scores = {k: v / total for k, v in disc_scores.items()}
        
        # Identificar tipo predominante
        dominant_type = max(disc_scores, key=disc_scores.get) if disc_scores else "indeterminado"
        
        # Mapear para tipo DISC
        disc_types = {
            "dominancia": "D - Dominante",
            "influencia": "I - Influente",
            "estabilidade": "S - Estável",
            "conformidade": "C - Conformista",
        }
        
        return {
            "disc_scores": disc_scores,
            "dominant_type": dominant_type,
            "disc_type_description": disc_types.get(dominant_type, "Indeterminado"),
            "confidence": max(disc_scores.values()) if disc_scores else 0.0,
        }
    
    def _analyze_mental_triggers(self, messages: List[str]) -> Dict:
        """Analisa gatilhos mentais presentes"""
        text = " ".join(messages).lower()
        
        triggers_found = {}
        for trigger, keywords in self.MENTAL_TRIGGERS.items():
            count = sum(text.count(kw.lower()) for kw in keywords)
            if count > 0:
                triggers_found[trigger] = {
                    "count": count,
                    "strength": "forte" if count > 3 else "média" if count > 1 else "fraca",
                }
        
        # Identificar gatilho predominante
        dominant_trigger = max(triggers_found, key=lambda x: triggers_found[x]["count"]) if triggers_found else None
        
        return {
            "triggers_detected": triggers_found,
            "dominant_trigger": dominant_trigger,
            "total_triggers": len(triggers_found),
            "persuasion_susceptibility": "alta" if len(triggers_found) > 3 else "média" if len(triggers_found) > 1 else "baixa",
        }
    
    def _analyze_psychological_needs(self, messages: List[str]) -> Dict:
        """Analisa necessidades psicológicas"""
        text = " ".join(messages).lower()
        
        needs_scores = {}
        for need, keywords in self.PSYCHOLOGICAL_NEEDS.items():
            score = sum(text.count(kw.lower()) for kw in keywords)
            needs_scores[need] = score
        
        # Normalizar
        total = sum(needs_scores.values())
        if total > 0:
            needs_scores = {k: v / total for k, v in needs_scores.items()}
        
        # Identificar necessidade predominante
        dominant_need = max(needs_scores, key=needs_scores.get) if needs_scores else None
        
        return {
            "needs_scores": needs_scores,
            "dominant_need": dominant_need,
            "unmet_needs": [need for need, score in needs_scores.items() if score > 0.2],
        }
    
    def _analyze_communication_style(self, messages: List[str]) -> Dict:
        """Analisa estilo de comunicação"""
        text = " ".join(messages).lower()
        
        style_scores = {}
        for style, keywords in self.COMMUNICATION_STYLES.items():
            score = sum(text.count(kw.lower()) for kw in keywords)
            style_scores[style] = score
        
        # Normalizar
        total = sum(style_scores.values())
        if total > 0:
            style_scores = {k: v / total for k, v in style_scores.items()}
        
        # Identificar estilo predominante
        dominant_style = max(style_scores, key=style_scores.get) if style_scores else "indeterminado"
        
        # Recomendações de abordagem
        approach_recommendations = {
            "direto": "Seja direto e objetivo. Vá direto ao ponto.",
            "detalhista": "Forneça informações detalhadas e completas.",
            "emocional": "Use linguagem emocional e crie conexão pessoal.",
            "racional": "Apresente fatos, dados e lógica.",
        }
        
        return {
            "style_scores": style_scores,
            "dominant_style": dominant_style,
            "approach_recommendation": approach_recommendations.get(dominant_style, ""),
        }
    
    def _determine_emotional_state(self, messages: List[str]) -> Dict:
        """Determina estado emocional geral"""
        if not messages:
            return {"state": "desconhecido", "confidence": 0.0}
        
        # Analisar última mensagem (mais recente)
        last_message = messages[-1].lower() if messages else ""
        
        # Padrões de estado emocional
        states = {
            "calmo": ["ok", "obrigado", "valeu", "belez", "joia", "certo", "sim"],
            "ansioso": ["urgente", "agora", "já", "ja", "hoje", "preciso", "rápido"],
            "frustrado": ["não", "nao", "mas", "porém", "porem", "infelizmente", "problema"],
            "empolgado": ["amei", "quero", "adoro", "perfeito", "ótimo", "maravilha", "!!!"],
            "duvidoso": ["?", "talvez", "não sei", "nao sei", "penso", "verificar", "ver"],
        }
        
        state_scores = {
            state: sum(last_message.count(kw) for kw in keywords)
            for state, keywords in states.items()
        }
        
        dominant_state = max(state_scores, key=state_scores.get) if state_scores else "neutro"
        confidence = state_scores[dominant_state] / sum(state_scores.values()) if sum(state_scores.values()) > 0 else 0.5
        
        return {
            "current_state": dominant_state,
            "confidence": confidence,
            "state_scores": state_scores,
            "message_count": len(messages),
        }
    
    def _analyze_rapport(self, messages: List[str]) -> Dict:
        """Analisa indicadores de rapport (conexão)"""
        text = " ".join(messages).lower()
        
        rapport_indicators = {
            "uso_nome": bool(re.search(r"\b(ana|maria|ju|carla|davila|tay|lu)\b", text)),
            "linguagem_positiva": any(kw in text for kw in ["ótimo", "maravilha", "perfeito", "amei"]),
            "perguntas_feitas": text.count("?"),
            "concordancias": sum(text.count(kw) for kw in ["sim", "isso", "exato", "certo", "concordo"]),
            "emoji_positivos": sum(text.count(e) for e in ["😊", "😍", "🥰", "👍", "❤️"]),
        }
        
        rapport_score = sum(rapport_indicators.values()) / len(rapport_indicators)
        
        return {
            "indicators": rapport_indicators,
            "rapport_score": rapport_score,
            "rapport_level": "alto" if rapport_score > 0.7 else "médio" if rapport_score > 0.4 else "baixo",
        }
    
    def _calculate_confidence_score(self, psychology_data: Dict, message_count: int) -> float:
        """Calcula confiança da análise"""
        factors = []
        
        # Fator 1: Quantidade de mensagens (mais dados = mais confiança)
        message_factor = min(1.0, message_count / 10)
        factors.append(message_factor)
        
        # Fator 2: Emoções detectadas
        emotions = psychology_data.get("emotions", {})
        emotion_factor = 1.0 if emotions.get("dominant_emotion") != "neutro" else 0.5
        factors.append(emotion_factor)
        
        # Fator 3: Personalidade detectada
        personality = psychology_data.get("personality", {})
        personality_factor = personality.get("confidence", 0.5)
        factors.append(personality_factor)
        
        # Fator 4: Gatilhos detectados
        triggers = psychology_data.get("mental_triggers", {})
        trigger_factor = min(1.0, triggers.get("total_triggers", 0) / 3)
        factors.append(trigger_factor)
        
        return self._calculate_confidence(factors)
