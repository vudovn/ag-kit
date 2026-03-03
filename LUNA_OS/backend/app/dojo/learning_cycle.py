"""
🎓 Dojo Learning Cycle

Ciclo de aprendizado que transforma feedback do Dojo em propostas de melhoria do system prompt.

Responsabilidades:
1. Ler todos os feedbacks com rating ≤ 3 do Supabase
2. Classificar cada falha em uma das 5 categorias:
   - INTENT: não entendeu o que a cliente queria
   - TONE: entendeu mas respondeu errado emocionalmente
   - INFORMATION: não sabia a resposta
   - FLOW: respondeu certo mas na hora errada ou fora de contexto
   - ESCALATION: deveria ter passado para humano e não passou
3. Agrupar por categoria e calcular frequência
4. Para cada categoria com >2 falhas na semana, gerar proposta de ajuste
5. Salvar propostas no Supabase em tabela prompt_proposals
6. Expor via endpoint para revisão humana

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger

from app.integrations.supabase_client import get_supabase
from app.integrations.openrouter import openrouter


# Categorias de falha
FAILURE_CATEGORIES = [
    "INTENT",  # Não entendeu o que a cliente queria
    "TONE",  # Entendeu mas respondeu com tom inadequado
    "INFORMATION",  # Não tinha a informação ou deu informação errada
    "FLOW",  # Respondeu fora de contexto ou momento errado
    "ESCALATION",  # Deveria ter transferido para humano mas não transferiu
]

# Prompt para classificar falhas
CLASSIFICATION_PROMPT = """
Você é um especialista em avaliação de assistentes de IA para salão de beleza.

Analise esta interação onde o assistente LUNA falhou (rating ≤ 3):

CENÁRIO: {scenario_name}
PERSONA: {persona_name}  
MENSAGEM DA CLIENTE: {user_message}
RESPOSTA DA LUNA: {luna_response}
MÉTRICAS: Empatia={empathy}, Clareza={clarity}, Acionabilidade={actionability}
RATING: {rating}/5
COMENTÁRIO DO AVALIADOR: {feedback_comment}

Classifique a falha em UMA das categorias:
- INTENT: LUNA não entendeu o que a cliente queria
- TONE: LUNA entendeu mas respondeu com tom inadequado para o momento emocional
- INFORMATION: LUNA não tinha a informação necessária ou deu informação errada
- FLOW: LUNA respondeu fora de contexto ou no momento errado da conversa
- ESCALATION: LUNA deveria ter transferido para humano mas não transferiu

Responda APENAS com um JSON:
{{"category": "CATEGORIA", "reasoning": "explicação em 1 frase", "suggested_fix": "o que mudar no comportamento da LUNA"}}
"""

# Prompt para gerar proposta de melhoria
PROPOSAL_PROMPT = """
Você é um especialista em prompt engineering para assistentes de IA de salão de beleza.

Esta semana a LUNA falhou {count} vezes na categoria {category}.

Falhas encontradas:
{failures_detail}

Trecho atual do system prompt relacionado a este comportamento:
{current_prompt_section}

Gere uma proposta de melhoria específica e aplicável. A proposta deve:
- Ser um parágrafo ou bloco de instruções pronto para inserir no system prompt
- Ser específica para o contexto de salão de beleza Haven Escovaria
- Não remover nada do prompt atual, apenas adicionar ou refinar
- Incluir exemplos concretos de como a LUNA deve se comportar

Responda APENAS com um JSON:
{{"proposed_text": "texto da instrução para o prompt", "insert_after": "título da seção onde inserir", "justification": "por que essa mudança resolve as falhas"}}
"""


class DojoLearningCycle:
    """
    Ciclo de Aprendizado do Dojo.

    Analisa feedbacks negativos e gera propostas de melhoria do system prompt.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.supabase = None  # [LAZY LOADING] Inicializar como None
        self.min_failures_for_proposal = self.config.get("min_failures", 2)

        logger.info("🎓 Dojo Learning Cycle initialized (lazy loading)")

    def _get_supabase(self):
        """[LAZY LOADING] Obter Supabase client apenas quando necessário"""
        if self.supabase is None:
            try:
                from app.integrations.supabase_client import get_supabase
                self.supabase = get_supabase()
            except Exception as e:
                logger.error(f"❌ DojoLearningCycle: Supabase não disponível - {e}")
                self.supabase = None
        return self.supabase

    async def run_weekly_analysis(
        self, week_reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa análise semanal de feedbacks e gera propostas.

        Args:
            week_reference: Referência da semana (ex: "2026-W09")
                           Se None, usa a semana anterior à atual

        Returns:
            Dict com resumo da análise e propostas geradas
        """
        if not week_reference:
            # Calcular semana anterior
            last_week = datetime.utcnow() - timedelta(days=7)
            week_reference = last_week.strftime("%Y-W%W")

        logger.info(f"🎓 Starting weekly analysis for {week_reference}")

        try:
            # 1. Buscar feedbacks negativos da semana
            feedbacks = await self._get_negative_feedbacks(week_reference)

            if not feedbacks:
                logger.info(f"✅ No negative feedbacks found for {week_reference}")
                return {
                    "success": True,
                    "week_reference": week_reference,
                    "feedbacks_analyzed": 0,
                    "proposals_generated": 0,
                }

            logger.info(f"📊 Found {len(feedbacks)} negative feedbacks")

            # 2. Classificar cada falha
            classified_failures = await self._classify_failures(feedbacks)

            # 3. Agrupar por categoria
            grouped = self._group_by_category(classified_failures)

            # 4. Gerar propostas para categorias com >2 falhas
            proposals = []
            for category, failures in grouped.items():
                if len(failures) >= self.min_failures_for_proposal:
                    proposal = await self._generate_proposal(
                        category, failures, week_reference
                    )
                    if proposal:
                        proposals.append(proposal)
                        # Salvar no Supabase
                        await self._save_proposal(proposal)

            logger.info(f"✅ Generated {len(proposals)} proposals for {week_reference}")

            return {
                "success": True,
                "week_reference": week_reference,
                "feedbacks_analyzed": len(feedbacks),
                "failures_classified": len(classified_failures),
                "categories_found": len(grouped),
                "proposals_generated": len(proposals),
                "proposals": proposals,
            }

        except Exception as e:
            logger.exception(f"❌ Weekly analysis failed: {e}")
            return {"success": False, "week_reference": week_reference, "error": str(e)}

    async def _get_negative_feedbacks(
        self, week_reference: str
    ) -> List[Dict[str, Any]]:
        """
        Busca feedbacks negativos (rating ≤ 3) da semana especificada.

        Args:
            week_reference: Referência da semana (ex: "2026-W09")

        Returns:
            Lista de feedbacks
        """
        try:
            # Calcular data inicial e final da semana
            year, week = week_reference.split("-W")
            week_num = int(week)

            # Primeira e última data da semana
            start_date = datetime.strptime(f"{year}-W{week_num}-1", "%Y-W%W-%w")
            end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

            # Buscar feedbacks no Supabase
            result = (
                self._get_supabase().table("dojo_feedback")
                .select("*")
                .gte("created_at", start_date.isoformat())
                .lte("created_at", end_date.isoformat())
                .lte("rating", 3)
                .eq("processed_for_learning", False)
                .execute()
            )

            feedbacks = result.data or []
            logger.debug(f"📊 Retrieved {len(feedbacks)} negative feedbacks")

            return feedbacks

        except Exception as e:
            logger.error(f"❌ Error fetching feedbacks: {e}")
            return []

    async def _classify_failures(
        self, feedbacks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Classifica cada falha em uma das 5 categorias.

        Args:
            feedbacks: Lista de feedbacks do Dojo

        Returns:
            Lista de falhas classificadas
        """
        classified = []

        for feedback in feedbacks:
            try:
                # Preparar prompt de classificação
                metrics = feedback.get("metrics", {})
                prompt = CLASSIFICATION_PROMPT.format(
                    scenario_name=feedback.get("scenario_name", "Unknown"),
                    persona_name=feedback.get("persona_name", "Unknown"),
                    user_message=feedback.get("user_message", ""),
                    luna_response=feedback.get("luna_response", ""),
                    empathy=metrics.get("empathy", 0),
                    clarity=metrics.get("clarity", 0),
                    actionability=metrics.get("actionability", 0),
                    rating=feedback.get("rating", 0),
                    feedback_comment=feedback.get("comment", ""),
                )

                # Chamar LLM para classificar
                response = await openrouter.generate(
                    prompt=prompt,
                    model="google/gemini-2.0-flash-001",
                    temperature=0.1,
                    max_tokens=200,
                )

                # Parse da resposta JSON
                import json

                try:
                    classification = json.loads(response.strip())
                    classified.append(
                        {
                            "feedback_id": feedback.get("id"),
                            "category": classification.get("category", "UNKNOWN"),
                            "reasoning": classification.get("reasoning", ""),
                            "suggested_fix": classification.get("suggested_fix", ""),
                            "feedback_data": feedback,
                        }
                    )

                    # Marcar feedback como processado e salvar categoria
                    await self._mark_feedback_processed(
                        feedback_id=feedback.get("id"),
                        category=classification.get("category", "UNKNOWN"),
                    )

                except json.JSONDecodeError:
                    logger.warning(
                        f"⚠️ Failed to parse classification response for feedback {feedback.get('id')}"
                    )
                    classified.append(
                        {
                            "feedback_id": feedback.get("id"),
                            "category": "UNKNOWN",
                            "reasoning": "Failed to parse LLM response",
                            "suggested_fix": "",
                            "feedback_data": feedback,
                        }
                    )

            except Exception as e:
                logger.error(f"❌ Error classifying feedback {feedback.get('id')}: {e}")
                classified.append(
                    {
                        "feedback_id": feedback.get("id"),
                        "category": "ERROR",
                        "reasoning": str(e),
                        "suggested_fix": "",
                        "feedback_data": feedback,
                    }
                )

        logger.debug(f"📊 Classified {len(classified)} failures")
        return classified

    def _group_by_category(
        self, classified_failures: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Agrupa falhas por categoria.

        Args:
            classified_failures: Lista de falhas classificadas

        Returns:
            Dict com categoria como chave e lista de falhas como valor
        """
        grouped = {}

        for failure in classified_failures:
            category = failure.get("category", "UNKNOWN")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(failure)

        logger.debug(
            f"📊 Grouped into {len(grouped)} categories: {list(grouped.keys())}"
        )
        return grouped

    async def _generate_proposal(
        self, category: str, failures: List[Dict[str, Any]], week_reference: str
    ) -> Optional[Dict[str, Any]]:
        """
        Gera proposta de melhoria para uma categoria de falha.

        Args:
            category: Categoria da falha
            failures: Lista de falhas desta categoria
            week_reference: Referência da semana

        Returns:
            Dict com proposta gerada ou None se falhar
        """
        try:
            # Preparar detalhe das falhas
            failures_detail = "\n\n".join(
                [
                    f"- Scenario: {f['feedback_data'].get('scenario_name', 'Unknown')}\n"
                    f"  Message: {f['feedback_data'].get('user_message', '')}\n"
                    f"  Response: {f['feedback_data'].get('luna_response', '')}\n"
                    f"  Reasoning: {f.get('reasoning', '')}"
                    for f in failures[
                        :5
                    ]  # Limitar a 5 falhas para não exceder token limit
                ]
            )

            # Obter trecho atual do prompt (placeholder - implementar conforme localização real)
            current_prompt_section = await self._get_current_prompt_section(category)

            # Preparar prompt de geração de proposta
            prompt = PROPOSAL_PROMPT.format(
                count=len(failures),
                category=category,
                failures_detail=failures_detail,
                current_prompt_section=current_prompt_section,
            )

            # Chamar LLM para gerar proposta
            response = await openrouter.generate(
                prompt=prompt,
                model="google/gemini-2.0-flash-001",
                temperature=0.3,
                max_tokens=500,
            )

            # Parse da resposta JSON
            import json

            try:
                proposal_data = json.loads(response.strip())

                # Extrair IDs dos cenários afetados
                affected_scenarios = list(
                    set(
                        [
                            f["feedback_data"].get("scenario_id", "")
                            for f in failures
                            if f["feedback_data"].get("scenario_id")
                        ]
                    )
                )

                proposal = {
                    "week_reference": week_reference,
                    "failure_category": category,
                    "failure_count": len(failures),
                    "affected_scenarios": affected_scenarios,
                    "current_prompt_excerpt": current_prompt_section,
                    "proposed_text": proposal_data.get("proposed_text", ""),
                    "insert_after": proposal_data.get("insert_after", ""),
                    "justification": proposal_data.get("justification", ""),
                    "proposed_change": proposal_data.get(
                        "proposed_text", ""
                    ),  # Para compatibilidade
                }

                logger.debug(f"📝 Generated proposal for {category}")
                return proposal

            except json.JSONDecodeError:
                logger.error(f"⚠️ Failed to parse proposal response for {category}")
                return None

        except Exception as e:
            logger.error(f"❌ Error generating proposal for {category}: {e}")
            return None

    async def _get_current_prompt_section(self, category: str) -> str:
        """
        Obtém trecho atual do system prompt relacionado à categoria.

        Args:
            category: Categoria da falha

        Returns:
            Trecho do prompt atual
        """
        # Mapeamento de categorias para seções do prompt
        category_sections = {
            "INTENT": "## Classificação de Intenções",
            "TONE": "## Tom de Voz e Personalidade",
            "INFORMATION": "## Base de Conhecimento",
            "FLOW": "## Fluxo de Conversação",
            "ESCALATION": "## Handoff e Escalamento",
        }

        section_title = category_sections.get(category, "")

        # TODO: Implementar leitura real do system prompt de config_haven.py ou arquivo
        # Por enquanto, retornar placeholder
        return f"[Seção do prompt relacionada a {category} - Implementar leitura real]"

    async def _save_proposal(self, proposal: Dict[str, Any]) -> bool:
        """
        Salva proposta no Supabase.

        Args:
            proposal: Dict com dados da proposta

        Returns:
            True se salvou com sucesso
        """
        try:
            result = self._get_supabase().table("prompt_proposals").insert(proposal).execute()

            logger.info(
                f"✅ Saved proposal to Supabase: {result.data[0].get('id') if result.data else 'unknown'}"
            )
            return True

        except Exception as e:
            logger.error(f"❌ Error saving proposal: {e}")
            return False

    async def _mark_feedback_processed(
        self, feedback_id: str, category: str = "UNKNOWN"
    ) -> bool:
        """
        Marca feedback como processado para aprendizado e registra categoria.

        Args:
            feedback_id: ID do feedback
            category: Categoria da falha identificada

        Returns:
            True se marcou com sucesso
        """
        try:
            self._get_supabase().table("dojo_feedback").update(
                {
                    "failure_category": category,
                    "processed_for_learning": True,
                    "processed_at": datetime.utcnow().isoformat(),
                }
            ).eq("id", feedback_id).execute()

            return True

        except Exception as e:
            logger.error(f"❌ Error marking feedback as processed: {e}")
            return False

    async def get_pending_proposals(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Busca propostas pendentes de aprovação.

        Args:
            limit: Limite de resultados

        Returns:
            Lista de propostas pendentes
        """
        try:
            result = (
                self._get_supabase().table("prompt_proposals")
                .select("*")
                .eq("status", "pending")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            return result.data or []

        except Exception as e:
            logger.error(f"❌ Error fetching pending proposals: {e}")
            return []

    async def approve_proposal(self, proposal_id: str, approved_by: str) -> bool:
        """
        Aprova proposta e aplica no system prompt.

        Args:
            proposal_id: ID da proposta
            approved_by: Usuário que aprovou

        Returns:
            True se aprovou com sucesso
        """
        try:
            # Buscar proposta
            result = (
                self._get_supabase().table("prompt_proposals")
                .select("*")
                .eq("id", proposal_id)
                .execute()
            )

            if not result.data:
                logger.error(f"❌ Proposal {proposal_id} not found")
                return False

            proposal = result.data[0]

            # TODO: Implementar aplicação real da proposta no system prompt
            # 1. Fazer backup do prompt atual
            # 2. Inserir proposed_text na seção indicada por insert_after
            # 3. Salvar novo prompt

            # Atualizar status para approved
            self._get_supabase().table("prompt_proposals").update(
                {
                    "status": "approved",
                    "approved_by": approved_by,
                    "approved_at": datetime.utcnow().isoformat(),
                }
            ).eq("id", proposal_id).execute()

            logger.info(f"✅ Approved proposal {proposal_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error approving proposal: {e}")
            return False

    async def reject_proposal(
        self, proposal_id: str, rejected_by: str, reason: str
    ) -> bool:
        """
        Rejeita proposta.

        Args:
            proposal_id: ID da proposta
            rejected_by: Usuário que rejeitou
            reason: Motivo da rejeição

        Returns:
            True se rejeitou com sucesso
        """
        try:
            self._get_supabase().table("prompt_proposals").update(
                {
                    "status": "rejected",
                    "rejected_by": rejected_by,
                    "rejected_at": datetime.utcnow().isoformat(),
                    "rejection_reason": reason,
                }
            ).eq("id", proposal_id).execute()

            logger.info(f"✅ Rejected proposal {proposal_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error rejecting proposal: {e}")
            return False


# Singleton global
learning_cycle = DojoLearningCycle()


async def run_weekly_learning_analysis(
    week_reference: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Função utilitária para executar análise semanal.

    Pode ser chamada pelo task_runner.
    """
    return await learning_cycle.run_weekly_analysis(week_reference)
