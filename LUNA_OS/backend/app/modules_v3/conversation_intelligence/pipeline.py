"""
🧠 Conversation Intelligence Pipeline

Orquestra a execução dos 8 agentes especializados para analisar conversas encerradas.

Responsabilidades:
1. Receber conversa encerrada (conversation_id, messages, client_id)
2. Executar os 8 agentes em ordem coordenada
3. Consolidar outputs de todos os agentes
4. Chamar storage_agent para persistir no Supabase e Obsidian
5. Retornar resumo do processamento

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from .agents.base_agent import AgentContext, AgentResult
from .agents.extractor_agent import ExtractorAgent
from .agents.psychology_agent import PsychologyAgent
from .agents.behavior_agent import BehaviorAgent
from .agents.sales_agent import SalesAgent
from .agents.insights_agent import InsightsAgent
from .agents.learning_agent import LearningAgent
from .agents.storage_agent import StorageAgent
from .agents.coordinator_agent import CoordinatorAgent


# Ordem de execução dos agentes
PIPELINE_ORDER = [
    "extractor",        # 1. Extrai dados estruturados da conversa
    "psychology",       # 2. Perfil emocional e estado da cliente
    "behavior",         # 3. Padrão de comportamento e preferências
    "sales",            # 4. Oportunidades e objeções identificadas
    "insights",         # 5. Insights acionáveis para o negócio
    "learning",         # 6. O que a LUNA pode aprender desta conversa
    # coordinator orquestra — não executa na sequência linear
    # storage executa por último — persiste tudo
]


class ConversationIntelligencePipeline:
    """
    Pipeline de Inteligência de Conversas.
    
    Executa os 8 agentes especializados em sequência coordenada
    e consolida os resultados para armazenamento.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.debug_mode = self.config.get("debug", False)
        
        # Inicializar agentes
        self.agents = {
            "extractor": ExtractorAgent(self.config.get("extractor", {})),
            "psychology": PsychologyAgent(self.config.get("psychology", {})),
            "behavior": BehaviorAgent(self.config.get("behavior", {})),
            "sales": SalesAgent(self.config.get("sales", {})),
            "insights": InsightsAgent(self.config.get("insights", {})),
            "learning": LearningAgent(self.config.get("learning", {})),
            "storage": StorageAgent(self.config.get("storage", {})),
        }
        
        # Coordinator para orquestração
        self.coordinator = CoordinatorAgent(self.config.get("coordinator", {}))
        
        logger.info("🧠 Conversation Intelligence Pipeline initialized")
    
    async def process_conversation(
        self,
        conversation_id: str,
        client_id: str,
        phone: str,
        messages: List[Dict[str, Any]],
        client_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Processa uma conversa encerrada através do pipeline.
        
        Args:
            conversation_id: ID da conversa no Supabase
            client_id: ID do cliente no Supabase
            phone: Telefone do cliente
            messages: Lista de mensagens da conversa
            client_name: Nome do cliente (opcional)
            metadata: Metadados adicionais (opcional)
            
        Returns:
            Dict com resumo do processamento e resultados consolidados
        """
        start_time = time.time()
        results: Dict[str, AgentResult] = {}
        errors: List[str] = []
        
        logger.info(f"🧠 Starting pipeline for conversation {conversation_id}")
        
        try:
            # Criar contexto compartilhado
            context = AgentContext(
                conversation_id=conversation_id,
                phone=phone,
                client_name=client_name,
                messages=messages,
                metadata=metadata or {},
                timestamp=datetime.utcnow().isoformat()
            )
            
            # Executar agentes em sequência
            for agent_name in PIPELINE_ORDER:
                agent = self.agents.get(agent_name)
                if not agent:
                    logger.warning(f"⚠️ Agent {agent_name} not found, skipping")
                    continue
                
                logger.debug(f"▶️ Executing {agent_name} agent...")
                
                try:
                    # Executar agente
                    result = await asyncio.wait_for(
                        agent.analyze(context),
                        timeout=30.0  # Timeout de 30 segundos por agente
                    )
                    
                    results[agent_name] = result
                    
                    if result.success:
                        logger.debug(f"✅ {agent_name} completed successfully")
                    else:
                        logger.warning(f"⚠️ {agent_name} completed with errors: {result.errors}")
                        errors.extend(result.errors)
                    
                    # Adicionar resultado ao contexto para próximos agentes
                    context.metadata[f"{agent_name}_result"] = result.data
                    
                except asyncio.TimeoutError:
                    error_msg = f"Timeout executing {agent_name} agent (30s)"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    results[agent_name] = AgentResult(
                        agent_name=agent_name,
                        success=False,
                        data={},
                        confidence=0.0,
                        processing_time_ms=30000,
                        errors=[error_msg]
                    )
                    
                except Exception as e:
                    error_msg = f"Error executing {agent_name} agent: {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    results[agent_name] = AgentResult(
                        agent_name=agent_name,
                        success=False,
                        data={},
                        confidence=0.0,
                        processing_time_ms=0,
                        errors=[error_msg]
                    )
            
            # Consolidar resultados
            consolidated = self._consolidate_results(results, errors)
            
            # Executar storage_agent para persistir
            logger.debug("▶️ Executing storage agent...")
            storage_result = await self.agents["storage"].analyze(
                context,
                consolidated,
                conversation_id,
                client_id
            )
            
            results["storage"] = storage_result
            
            # Calcular tempo total
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"✅ Pipeline completed for {conversation_id} in {processing_time_ms}ms")
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "client_id": client_id,
                "processing_time_ms": processing_time_ms,
                "agents_executed": list(results.keys()),
                "agents_success": sum(1 for r in results.values() if r.success),
                "agents_failed": sum(1 for r in results.values() if not r.success),
                "errors": errors,
                "consolidated": consolidated,
                "storage_result": storage_result.to_dict() if storage_result else None
            }
            
        except Exception as e:
            processing_time_ms = int((time.time() - start_time) * 1000)
            logger.exception(f"❌ Pipeline failed for {conversation_id}: {e}")
            
            return {
                "success": False,
                "conversation_id": conversation_id,
                "client_id": client_id,
                "processing_time_ms": processing_time_ms,
                "error": str(e),
                "errors": errors + [str(e)]
            }
    
    def _consolidate_results(
        self,
        results: Dict[str, AgentResult],
        errors: List[str]
    ) -> Dict[str, Any]:
        """
        Consolida resultados de todos os agentes em um único dicionário.
        
        Args:
            results: Resultados de cada agente
            errors: Lista de erros ocorridos
            
        Returns:
            Dict consolidado com todos os dados extraídos
        """
        consolidated = {
            "processed_at": datetime.utcnow().isoformat(),
            "errors": errors,
            "agents": {}
        }
        
        # Extrator
        if "extractor" in results and results["extractor"].success:
            extractor_data = results["extractor"].data
            consolidated.update({
                "services_mentioned": extractor_data.get("services", []),
                "professionals_mentioned": extractor_data.get("professionals", []),
                "dates_mentioned": extractor_data.get("temporal", {}).get("dates", []),
                "times_mentioned": extractor_data.get("temporal", {}).get("times", []),
                "price_sensitivity": extractor_data.get("monetary", {}).get("sensitivity", "medium")
            })
            consolidated["agents"]["extractor"] = True
        
        # Psychology
        if "psychology" in results and results["psychology"].success:
            psychology_data = results["psychology"].data
            consolidated.update({
                "emotional_state": psychology_data.get("emotional_state", "neutral"),
                "communication_style": psychology_data.get("communication_style", "neutral"),
                "trust_level": psychology_data.get("trust_level", "new"),
                "personality_type": psychology_data.get("personality_type", "unknown")
            })
            consolidated["agents"]["psychology"] = True
        
        # Behavior
        if "behavior" in results and results["behavior"].success:
            behavior_data = results["behavior"].data
            consolidated.update({
                "preferred_professional": behavior_data.get("preferred_professional"),
                "preferred_time_of_day": behavior_data.get("preferred_time_of_day"),
                "booking_pattern": behavior_data.get("booking_pattern", "spontaneous")
            })
            consolidated["agents"]["behavior"] = True
        
        # Sales
        if "sales" in results and results["sales"].success:
            sales_data = results["sales"].data
            consolidated.update({
                "upsell_opportunities": sales_data.get("upsell_opportunities", []),
                "objections_raised": sales_data.get("objections", []),
                "conversion_likelihood": sales_data.get("conversion_probability", "medium"),
                "funnel_stage": sales_data.get("funnel_stage", "awareness")
            })
            consolidated["agents"]["sales"] = True
        
        # Insights
        if "insights" in results and results["insights"].success:
            insights_data = results["insights"].data
            consolidated.update({
                "key_insights": insights_data.get("key_insights", []),
                "recommended_actions": insights_data.get("recommended_actions", [])
            })
            consolidated["agents"]["insights"] = True
        
        # Learning
        if "learning" in results and results["learning"].success:
            learning_data = results["learning"].data
            consolidated.update({
                "luna_performance_notes": learning_data.get("performance_notes"),
                "improvement_suggestions": learning_data.get("suggestions", [])
            })
            consolidated["agents"]["learning"] = True
        
        return consolidated
    
    async def process_batch(
        self,
        conversations: List[Dict[str, Any]],
        max_concurrent: int = 5
    ) -> Dict[str, Any]:
        """
        Processa múltiplas conversas em batch.
        
        Args:
            conversations: Lista de conversas para processar
            max_concurrent: Número máximo de processamentos concorrentes
            
        Returns:
            Dict com resumo do processamento em batch
        """
        logger.info(f"🧠 Starting batch processing for {len(conversations)} conversations")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(conv):
            async with semaphore:
                return await self.process_conversation(
                    conversation_id=conv.get("conversation_id"),
                    client_id=conv.get("client_id"),
                    phone=conv.get("phone"),
                    messages=conv.get("messages", []),
                    client_name=conv.get("client_name"),
                    metadata=conv.get("metadata")
                )
        
        tasks = [process_with_semaphore(conv) for conv in conversations]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Consolidar resultados do batch
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
        failed = len(results) - successful
        
        logger.info(f"✅ Batch processing completed: {successful} successful, {failed} failed")
        
        return {
            "total": len(conversations),
            "successful": successful,
            "failed": failed,
            "results": results
        }


# Singleton global
pipeline = ConversationIntelligencePipeline()


async def process_conversation_intelligence(
    conversation_id: str,
    client_id: str,
    phone: str,
    messages: List[Dict[str, Any]],
    client_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Função utilitária para processar inteligência de conversa.
    
    Pode ser chamada diretamente do brain.py ou outros módulos.
    """
    return await pipeline.process_conversation(
        conversation_id=conversation_id,
        client_id=client_id,
        phone=phone,
        messages=messages,
        client_name=client_name
    )
