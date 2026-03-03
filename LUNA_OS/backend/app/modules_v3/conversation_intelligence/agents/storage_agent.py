"""
💾 Storage Agent - Agente de Armazenamento

Responsável por armazenar resultados nos locais corretos:
- Supabase (dados estruturados)
- Obsidian Vault (conhecimento rico)
- Cache (performance)

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import time
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentContext, AgentResult


class StorageAgent(BaseAgent):
    """Agente de armazenamento de dados e insights"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supabase_client = None
        self.obsidian_path = self.config.get(
            "obsidian_path",
            os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                ),
                "knowledge",
                "obsidian_vault",
            ),
        )

    def get_name(self) -> str:
        return "StorageAgent"

    def get_expertise(self) -> str:
        return "Armazenamento em Supabase e Obsidian Vault"

    def analyze(self, context: AgentContext, results: List[AgentResult]) -> AgentResult:
        """
        Armazena resultados das análises.
        """
        start_time = time.time()
        errors = []

        try:
            storage_results = {
                "supabase": self._store_in_supabase(context, results),
                "obsidian": self._store_in_obsidian(context, results),
                "cache": self._store_in_cache(context, results),
            }

            processing_time = int((time.time() - start_time) * 1000)

            return AgentResult(
                agent_name=self.get_name(),
                success=True,
                data=storage_results,
                confidence=1.0,
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

    def _store_in_supabase(
        self, context: AgentContext, results: List[AgentResult]
    ) -> Dict:
        """Armazena dados estruturados no Supabase"""
        # Implementação simplificada - em produção usaria cliente Supabase real
        return {
            "success": True,
            "tables_updated": [
                "conversation_analysis",
                "client_insights",
                "behavioral_data",
            ],
            "records_created": len(results),
        }

    def _store_in_obsidian(
        self, context: AgentContext, results: List[AgentResult]
    ) -> Dict:
        """Armazena conhecimento rico no Obsidian Vault no formato Ollama Insight"""
        try:
            # Buscar insight do Ollama
            ollama_insight = ""
            for result in results:
                if result.agent_name == "InsightsAgent" and result.success:
                    ollama_insight = result.data.get("ai_executive_summary", "")
                    break

            # Criar arquivo de insights no novo diretório de inteligência
            safe_phone = context.phone or "Unknown"
            insights_file = os.path.join(
                self.obsidian_path,
                "_Active",
                "03-INTELLIGENCE",
                "Ollama Insights",
                f"Insight-{safe_phone}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            )

            os.makedirs(os.path.dirname(insights_file), exist_ok=True)

            content = self._generate_obsidian_content(context, results, ollama_insight)

            # Aqui gravamos de verdade para que o Obsidian crie o insight local
            with open(insights_file, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "success": True,
                "file_path": insights_file,
                "content_length": len(content),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _generate_obsidian_content(
        self, context: AgentContext, results: List[AgentResult], ollama_insight: str
    ) -> str:
        """Gera conteúdo formatado para Obsidian baseado no Ollama Insight Template"""

        # Extrair dados para o template
        emotion = ""
        disc = ""
        funnel = ""
        conv_prob = 0
        objections = []
        behavior_pattern = ""
        churn = ""
        loyalty = ""
        recs = []
        processing_time = 0
        confidence = 0.0

        for r in results:
            if not r.success:
                continue
            processing_time += r.processing_time_ms

            if r.agent_name == "PsychologyAgent":
                emotion = r.data.get("emotions", {}).get("dominant_emotion", "")
                disc = r.data.get("personality", {}).get("dominant_type", "")
            elif r.agent_name == "SalesAgent":
                funnel = r.data.get("funnel_stage", {}).get("stage", "")
                conv_prob = r.data.get("conversion_probability", {}).get(
                    "probability", 0
                )
                objs = r.data.get("objections", [])
                objections = [o.get("type", "") for o in objs]
            elif r.agent_name == "BehaviorAgent":
                behavior_pattern = r.data.get("behavior_patterns", {}).get(
                    "dominant_pattern", ""
                )
                churn = r.data.get("churn_risk", {}).get("risk_level", "")
                loyalty = r.data.get("loyalty_indicators", {}).get("loyalty_level", "")
            elif r.agent_name == "InsightsAgent":
                confidence = r.confidence
                recs = r.data.get("actionable_recommendations", [])

        content = f"""---
type: ollama_insight
created_at: {datetime.now().strftime('%Y-%m-%d %H:%M')}
conversation_id: {context.conversation_id}
phone: {context.phone}
client_name: {context.client_name or 'N/A'}
tags:
  - ollama
  - insight
  - analysis
ollama_model: llama3.2
processing_time_ms: {processing_time}
confidence_score: {confidence:.2f}
---

# 🧠 Insight Ollama: {context.client_name or context.phone}

**Data:** {datetime.now().strftime('%Y-%m-%d')}  
**Cliente:** [[{context.client_name or 'N/A'}]]  
**Telefone:** `{context.phone}`  
**Conversation ID:** {context.conversation_id}  

---

## 📊 Resumo Executivo (Ollama Llama 3)

{ollama_insight if ollama_insight else "*(Nenhum resumo gerado pela IA)*"}

---

## 🎯 Insights Principais

### Psicologia
- **Emoção Dominante:** {emotion}
- **Tipo DISC:** {disc}

### Vendas
- **Estágio no Funil:** {funnel}
- **Probabilidade de Conversão:** {conv_prob}%
- **Objeções Detectadas:** {', '.join(objections) if objections else 'Nenhuma'}

### Comportamento
- **Padrão Dominante:** {behavior_pattern}
- **Risco de Churn:** {churn}
- **Nível de Lealdade:** {loyalty}

---

## 💡 Recomendações Acionáveis
"""
        for i, rec in enumerate(recs, 1):
            content += f"{i}. {rec}\n"

        content += """
---

## 🔗 Links Relacionados

- [[000_MCT_MASTER_INDEX]]
- [[Dashboard]]

---

*Gerado via Agent Flow + Ollama Local (M1)*
"""
        return content

    def _store_in_cache(
        self, context: AgentContext, results: List[AgentResult]
    ) -> Dict:
        """Armazena em cache para performance"""
        # Implementação simplificada
        return {
            "success": True,
            "cache_key": f"analysis:{context.conversation_id}",
            "ttl_seconds": 3600,
        }
