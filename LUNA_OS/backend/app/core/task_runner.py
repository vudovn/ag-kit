"""
⏰ Task Runner - Scheduler Interno

Processos periódicos que rodam em horários definidos usando apenas Python + Docker.

Tasks implementadas:
1. Processar conversas encerradas sem intelligence (a cada hora)
2. Rodar ciclo de aprendizado do Dojo (segunda-feira 07:00)
3. Gerar edge cases do Dojo (semanal)
4. Health check das integrações (30 minutos)

Autor: MCT Agent Flow
Data: 2026-03-01
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger

import schedule

from app.integrations.supabase_client import get_supabase
from app.modules_v3.conversation_intelligence.pipeline import (
    process_conversation_intelligence,
)
from app.dojo.learning_cycle import run_weekly_learning_analysis


class TaskRunner:
    """
    Runner de tarefas periódicas.

    Agenda e executa tasks em horários definidos.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.supabase = get_supabase()
        self.running = False

        # Configurações de rate limiting
        self.max_conversations_per_run = self.config.get("max_conversations", 10)
        self.max_concurrent_tasks = self.config.get("max_concurrent", 5)

        logger.info("⏰ Task Runner initialized")

    def start(self):
        """Inicia o scheduler."""
        logger.info("⏰ Starting Task Runner scheduler...")

        # Task 1: Processar conversas encerradas (a cada hora)
        schedule.every().hour.do(
            self._run_task_wrapper, self._process_ended_conversations
        )

        # Task 2: Dojo Learning Cycle (segunda-feira 07:00)
        schedule.every().monday.at("07:00").do(
            self._run_task_wrapper, self._run_dojo_learning
        )

        # Task 3: Gerar edge cases (semanal - domingo 23:00)
        schedule.every().sunday.at("23:00").do(
            self._run_task_wrapper, self._generate_edge_cases
        )

        # Task 4: Health check (30 minutos)
        schedule.every(30).minutes.do(self._run_task_wrapper, self._health_check)

        self.running = True
        logger.info("✅ Task Runner scheduler started")

        # Loop principal
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Checar a cada minuto

    def stop(self):
        """Para o scheduler."""
        logger.info("⏰ Stopping Task Runner...")
        self.running = False
        schedule.clear()
        logger.info("✅ Task Runner stopped")

    def _run_task_wrapper(self, task_func):
        """Wrapper para executar tasks com tratamento de erro."""
        try:
            logger.info(f"▶️ Running task: {task_func.__name__}")
            asyncio.run(task_func())
            logger.info(f"✅ Task completed: {task_func.__name__}")
        except Exception as e:
            logger.exception(f"❌ Task failed: {task_func.__name__} - {e}")

    async def _process_ended_conversations(self):
        """
        TASK 1: Processar conversas encerradas que ainda não passaram pelo pipeline.

        Busca conversas com status=ended ou handed_off sem registro em conversation_intelligence.
        Executa o pipeline para cada uma (máximo 10 por execução).
        """
        logger.info("📊 Task 1: Processing ended conversations...")

        try:
            # Buscar conversas encerradas sem intelligence
            result = (
                self.supabase.table("conversations")
                .select("id, phone, client_id, messages_count, status, ended_at")
                .in_("status", ["ended", "handed_off"])
                .is_("extracted_data", None)
                .order("ended_at", desc=True)
                .limit(self.max_conversations_per_run)
                .execute()
            )

            conversations = result.data or []

            if not conversations:
                logger.info("✅ No ended conversations to process")
                return

            logger.info(f"📊 Found {len(conversations)} conversations to process")

            # Processar cada conversa
            processed = 0
            failed = 0

            for conv in conversations:
                try:
                    # Buscar mensagens da conversa
                    messages_result = (
                        self.supabase.table("messages")
                        .select(
                            "direction, content, intent_detected, sentiment, created_at"
                        )
                        .eq("conversation_id", conv["id"])
                        .order("created_at", asc=True)
                        .execute()
                    )

                    messages = messages_result.data or []

                    if not messages:
                        logger.warning(
                            f"⚠️ No messages found for conversation {conv['id']}"
                        )
                        continue

                    # Buscar nome do cliente
                    client_name = None
                    if conv.get("client_id"):
                        client_result = (
                            self.supabase.table("clients")
                            .select("name")
                            .eq("id", conv["client_id"])
                            .execute()
                        )
                        if client_result.data:
                            client_name = client_result.data[0].get("name")

                    # Executar pipeline
                    pipeline_result = await process_conversation_intelligence(
                        conversation_id=conv["id"],
                        client_id=conv.get("client_id"),
                        phone=conv["phone"],
                        messages=messages,
                        client_name=client_name,
                    )

                    if pipeline_result.get("success"):
                        processed += 1
                        logger.debug(f"✅ Processed conversation {conv['id']}")
                    else:
                        failed += 1
                        logger.error(
                            f"❌ Failed to process conversation {conv['id']}: {pipeline_result.get('error')}"
                        )

                    # Rate limiting: esperar 1 segundo entre conversas
                    await asyncio.sleep(1)

                except Exception as e:
                    failed += 1
                    logger.error(f"❌ Error processing conversation {conv['id']}: {e}")

            logger.info(f"✅ Task 1 completed: {processed} processed, {failed} failed")

        except Exception as e:
            logger.exception(f"❌ Task 1 failed: {e}")

    async def _run_dojo_learning(self):
        """
        TASK 2: Rodar ciclo de aprendizado do Dojo.

        Agrega feedbacks da semana anterior e gera propostas de melhoria.
        """
        logger.info("🎓 Task 2: Running Dojo Learning Cycle...")

        try:
            # Calcular semana anterior
            last_week = datetime.utcnow() - timedelta(days=7)
            week_reference = last_week.strftime("%Y-W%W")

            # Executar análise semanal
            result = await run_weekly_learning_analysis(week_reference)

            if result.get("success"):
                logger.info(
                    f"✅ Task 2 completed: {result.get('proposals_generated', 0)} proposals generated"
                )
            else:
                logger.error(f"❌ Task 2 failed: {result.get('error')}")

        except Exception as e:
            logger.exception(f"❌ Task 2 failed: {e}")

    async def _generate_edge_cases(self):
        """
        TASK 3: Gerar novos cenários do Dojo a partir de edge cases.

        Busca conversas que terminaram em handed_off sem resolução.
        Converte em novos cenários para o Dojo.
        Salva em tabela dojo_edge_cases no Supabase.
        """
        logger.info("🎯 Task 3: Generating edge cases...")

        try:
            # Buscar conversas handed_off sem resolução
            result = (
                self.supabase.table("conversations")
                .select("id, phone, status, intent, sentiment, ended_at")
                .eq("status", "handed_off")
                .gte("ended_at", (datetime.utcnow() - timedelta(days=7)).isoformat())
                .order("ended_at", desc=True)
                .limit(20)
                .execute()
            )

            conversations = result.data or []

            if not conversations:
                logger.info("✅ No edge cases found this week")
                return

            logger.info(f"📊 Found {len(conversations)} potential edge cases")

            # Processar cada conversa para identificar edge cases
            edge_cases = []

            for conv in conversations:
                # Analisar se é um edge case real
                # (conversa que deveria ter sido resolvida mas não foi)

                # Buscar mensagens para análise
                messages_result = (
                    self.supabase.table("messages")
                    .select("direction, content")
                    .eq("conversation_id", conv["id"])
                    .order("created_at", asc=True)
                    .limit(10)
                    .execute()
                )

                messages = messages_result.data or []

                # Extrair descrição da situação
                situation_description = "\n".join(
                    [
                        f"{'CLIENTE' if m['direction'] == 'inbound' else 'LUNA'}: {m['content']}"
                        for m in messages[-5:]  # Últimas 5 mensagens
                    ]
                )

                edge_case = {
                    "source_conversation_id": conv["id"],
                    "client_phone": conv["phone"],
                    "situation_description": situation_description,
                    "why_luna_failed": f"Conversation escalated to handoff with intent={conv.get('intent')}",
                    "expected_behavior": "LUNA should have resolved without human escalation",
                    "status": "new",
                }

                edge_cases.append(edge_case)

            # Salvar edge cases no Supabase
            if edge_cases:
                insert_result = (
                    self.supabase.table("dojo_edge_cases").insert(edge_cases).execute()
                )

                logger.info(f"✅ Task 3 completed: {len(edge_cases)} edge cases saved")
            else:
                logger.info("✅ Task 3 completed: No edge cases to save")

        except Exception as e:
            logger.exception(f"❌ Task 3 failed: {e}")

    async def _health_check(self):
        """
        TASK 4: Health check das integrações.

        Verifica Evolution API, Supabase, OpenRouter.
        Loga status em tabela health_checks.
        """
        logger.debug("🏥 Task 4: Running health checks...")

        try:
            checks = []

            # Check 1: Supabase
            try:
                start = time.time()
                result = (
                    self.supabase.table("clients")
                    .select("count", count="exact")
                    .limit(1)
                    .execute()
                )
                response_time = int((time.time() - start) * 1000)

                checks.append(
                    {
                        "service_name": "supabase",
                        "status": "healthy",
                        "response_time_ms": response_time,
                        "details": {"rows": len(result.data) if result.data else 0},
                    }
                )
            except Exception as e:
                checks.append(
                    {
                        "service_name": "supabase",
                        "status": "unhealthy",
                        "response_time_ms": 0,
                        "error_message": str(e),
                    }
                )

            # Check 2: Evolution API
            try:
                from app.integrations.evolution import evolution

                start = time.time()
                status = await evolution.get_instance_status()
                response_time = int((time.time() - start) * 1000)

                checks.append(
                    {
                        "service_name": "evolution",
                        "status": (
                            "healthy"
                            if status.get("instance", {}).get("state") == "open"
                            else "degraded"
                        ),
                        "response_time_ms": response_time,
                        "details": status,
                    }
                )
            except Exception as e:
                checks.append(
                    {
                        "service_name": "evolution",
                        "status": "unhealthy",
                        "response_time_ms": 0,
                        "error_message": str(e),
                    }
                )

            # Check 3: OpenRouter
            try:
                from app.integrations.openrouter import openrouter

                start = time.time()
                models = await openrouter.get_models()
                response_time = int((time.time() - start) * 1000)

                checks.append(
                    {
                        "service_name": "openrouter",
                        "status": "healthy" if models else "degraded",
                        "response_time_ms": response_time,
                        "details": {"models_count": len(models) if models else 0},
                    }
                )
            except Exception as e:
                checks.append(
                    {
                        "service_name": "openrouter",
                        "status": "unhealthy",
                        "response_time_ms": 0,
                        "error_message": str(e),
                    }
                )

            # Salvar health checks no Supabase
            for check in checks:
                self.supabase.table("health_checks").insert(check).execute()

            # Logar resumo
            healthy = sum(1 for c in checks if c["status"] == "healthy")
            total = len(checks)

            if healthy == total:
                logger.info(f"✅ Task 4 completed: All {total} services healthy")
            else:
                logger.warning(
                    f"⚠️ Task 4 completed: {healthy}/{total} services healthy"
                )

        except Exception as e:
            logger.exception(f"❌ Task 4 failed: {e}")


# Singleton global
task_runner = TaskRunner()


def start_scheduler():
    """
    Inicia o scheduler como background task.

    Deve ser chamado no lifespan do FastAPI.
    """
    import threading

    def run_scheduler():
        task_runner.start()

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    logger.info("✅ Scheduler started in background thread")


def stop_scheduler():
    """Para o scheduler."""
    task_runner.stop()
