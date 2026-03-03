"""
🤖 Base Agent - Classe Base para Todos os Agentes

Define a interface comum e funcionalidades compartilhadas entre todos os agentes
da equipe de Conversation Intelligence.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from loguru import logger
import json
import requests


@dataclass
class AgentContext:
    """Contexto compartilhado entre agentes"""

    conversation_id: str
    phone: str
    client_name: Optional[str]
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AgentResult:
    """Resultado padronizado de análise do agente"""

    agent_name: str
    success: bool
    data: Dict[str, Any]
    confidence: float  # 0.0 - 1.0
    processing_time_ms: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "agent_name": self.agent_name,
            "success": self.success,
            "data": self.data,
            "confidence": self.confidence,
            "processing_time_ms": self.processing_time_ms,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class BaseAgent(ABC):
    """
    Classe base abstrata para todos os agentes.

    Cada agente deve implementar:
    - analyze(): Método principal de análise
    - get_name(): Nome do agente
    - get_expertise(): Área de especialização
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)
        self.debug_mode = self.config.get("debug", False)
        self._cache = {}

        logger.info(f"🤖 Agente {self.get_name()} inicializado")

    @abstractmethod
    def analyze(self, context: AgentContext) -> AgentResult:
        """
        Método principal de análise.

        Args:
            context: Contexto da conversa

        Returns:
            AgentResult: Resultado padronizado da análise
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Retorna nome do agente"""
        pass

    @abstractmethod
    def get_expertise(self) -> str:
        """Retorna área de especialização do agente"""
        pass

    def get_knowledge_base(self) -> Dict[str, Any]:
        """
        Retorna base de conhecimento do agente.
        Pode ser carregada de arquivos JSON, banco de dados, etc.
        """
        return {}

    def _log_debug(self, message: str):
        """Log de debug (apenas se debug_mode ativado)"""
        if self.debug_mode:
            logger.debug(f"[{self.get_name()}] {message}")

    def _log_error(self, message: str, error: Exception):
        """Log de erro com detalhes"""
        logger.error(f"[{self.get_name()}] {message}: {error}")

    def _calculate_confidence(self, factors: List[float]) -> float:
        """
        Calcula confiança baseada em múltiplos fatores.

        Args:
            factors: Lista de pesos (0.0-1.0)

        Returns:
            float: Confiança média ponderada
        """
        if not factors:
            return 0.0
        return sum(factors) / len(factors)

    def _extract_keywords(self, text: str, keywords: List[str]) -> Dict[str, int]:
        """
        Extrai frequência de keywords no texto.

        Args:
            text: Texto para análise
            keywords: Lista de keywords para buscar

        Returns:
            Dict[str, int]: Frequência de cada keyword
        """
        text_lower = text.lower()
        return {
            kw: text_lower.count(kw.lower())
            for kw in keywords
            if kw.lower() in text_lower
        }

    def _detect_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """
        Detecta padrões regex no texto.

        Args:
            text: Texto para análise
            patterns: Lista de padrões regex

        Returns:
            List[str]: Padrões encontrados
        """
        import re

        found = []
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(pattern)
        return found

    def to_json(self) -> str:
        """Serializa agente para JSON (para logging/debug)"""
        return json.dumps(
            {
                "name": self.get_name(),
                "expertise": self.get_expertise(),
                "enabled": self.enabled,
                "config": self.config,
            },
            indent=2,
            ensure_ascii=False,
        )

    def _ask_local_brain(self, prompt: str, system_prompt: str = "") -> str:
        """
        Interroga o modelo local Ollama (Llama 3) via API rodando no M1
        sem gastar tokens na nuvem.
        """
        # Se for mockado nos testes
        if getattr(self, "mock_local_brain", False):
            return ""

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }

        try:
            response = requests.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as e:
            self._log_error("Falha ao consultar LLM local", e)
            return ""
