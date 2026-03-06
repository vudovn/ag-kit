"""
LUNA Brain - Core Intelligence
Padrão Elite MCT - Framework de 5 Camadas
Blindagem Soberana: Resiliência + Fallback + Auditoria

Arquitetura:
- Pipeline modular com separação clara de responsabilidades
- Fallback em 3 níveis (Local → IA → Safety Net)
- RAG-based context building
- Intelligence extraction para BI

DEBT #B3: Comentários padronizados em português
"""

import json
import os
import re
import time
import httpx
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple, Dict, Any
from loguru import logger

from app.config import settings
from app.integrations.openrouter import openrouter
from app.integrations.wascript import wascript
from app.core.memory import MemoryManager
from app.knowledge.loader import KnowledgeBase
# [LAZY LOADING] Não importar campaign_manager na importação do módulo
# from app.core.campaign_manager import campaign_manager
from app.core.scheduler import scheduler

# Singletons
memory = MemoryManager()
kb = KnowledgeBase()


# ═══════════════════════════════════════════════
# DOMAIN MODELS
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# IMPORTAÇÕES DA FÍSICA DOS PROCEDIMENTOS
# ═══════════════════════════════════════════════
from app.core.config_haven import (
    PROFISSIONAIS,
    SERVICOS,
    FISICA_PROCEDIMENTOS,
    REGRAS_FISICAS_ATENDIMENTO,
    COMPATIBILIDADE_SERVICOS,
    TEMPOS_REAIS,
)
from app.core.schemas_brain import (
    IntentType,
    SentimentType,
    CustomerMood,
    PotentialValue,
    IntelligenceData,
    BrainResult,
)

# Novos Módulos Especializados (Refatoração Kimi)
from app.core import physics
from app.core import marketing
from app.core import intelligence
from app.core import rules

# [AUTOMELHORIA] Módulos de proteção e aprendizado contínuo
from app.core import guardrails
from app.core.learning import learning, calculate_confidence, decide_action


# ═══════════════════════════════════════════════
# INTENT PATTERNS (Knowledge Base)
# ═══════════════════════════════════════════════

INTENT_PATTERNS: Dict[IntentType, List[str]] = {
    IntentType.AGENDAR: [
        "agendar",
        "marcar",
        "tem horário",
        "tem vaga",
        "quero fazer",
        "vaga",
        "horário para",
    ],
    IntentType.PRECO: [
        "quanto custa",
        "qual valor",
        "preço",
        "tabela",
        "valor do",
        "custo",
    ],
    IntentType.SERVICOS_TECNICOS: [
        "gel",
        "blindagem",
        "remocao",
        "remoção",
        "gelinho",
    ],
    IntentType.SAUDACAO: [
        "oi",
        "olá",
        "ola",
        "bom dia",
        "boa tarde",
        "boa noite",
        "hey",
        "opa",
    ],
    IntentType.AGRADECIMENTO: [
        "obrigado",
        "obrigada",
        "valeu",
        "thanks",
        "vlw",
    ],
    IntentType.DISPONIBILIDADE: [
        "tem horário",
        "disponível",
        "vaga",
    ],
    IntentType.SERVICOS: [
        "quais serviços",
        "o que vocês fazem",
        "cardápio",
        "menu",
    ],
    IntentType.PACOTE: [
        "pacote",
        "pacotes",
        "combo",
        "promoção",
    ],
    IntentType.CUPOM: [
        "cupom",
        "desconto",
        "PRISCILA10",
        "EWYLIN10",
    ],
    IntentType.LOCALIZACAO: [
        "onde fica",
        "endereco",
        "endereço",
        "localização",
        "localizacao",
        "como chegar",
        "onde voces ficam",
        "onde vcs ficam",
        "onde fica a loja",
    ],
    IntentType.HORARIO_FUNC: [
        "horário",
        "que horas abre",
        "fecha",
        "funciona",
    ],
    IntentType.RECLAMACAO: [
        "problema",
        "ruim",
        "não gostei",
        "reclamação",
    ],
    IntentType.HANDOFF: [
        "falar com humano",
        "pessoa real",
        "atendente",
    ],
}

# Rotas de processamento
QUICK_INTENTS = {
    IntentType.SAUDACAO,
    IntentType.AGRADECIMENTO,
    IntentType.LOCALIZACAO,
    IntentType.HORARIO_FUNC,
}

COMPLEX_INTENTS = {
    IntentType.AGENDAR,
    IntentType.RECLAMACAO,
    IntentType.HANDOFF,
    IntentType.PACOTE,
    IntentType.MULTI_SERVICO,
}


# ═══════════════════════════════════════════════
# CLASSIFIERS
# ═══════════════════════════════════════════════


def classify_intent(message: str) -> Tuple[IntentType, float]:
    """
    Classificação de intenção via pattern matching.
    Retorna (intent, confidence_score)
    """
    msg_lower = message.lower().strip()

    # Prioridade para intenções específicas
    specific_intents = [
        IntentType.AGENDAR,
        IntentType.PRECO,
        IntentType.SERVICOS_TECNICOS,
        IntentType.LOCALIZACAO,
        IntentType.PACOTE,
    ]

    for intent in specific_intents:
        patterns = INTENT_PATTERNS.get(intent, [])
        for pattern in patterns:
            if pattern in msg_lower:
                return intent, 0.95

    # Outras intenções
    for intent, patterns in INTENT_PATTERNS.items():
        if intent in specific_intents:
            continue
        for pattern in patterns:
            if pattern in msg_lower:
                # Saudação em mensagem longa = baixa confiança
                if intent == IntentType.SAUDACAO and len(msg_lower) > 15:
                    return intent, 0.4
                return intent, 0.9

    # Multi-serviço detection
    service_keywords = {"escova", "unha", "make", "cabelo", "sobrancelha"}
    service_mentions = sum(1 for s in service_keywords if s in msg_lower)
    if service_mentions > 1:
        return IntentType.MULTI_SERVICO, 0.8

    # INTENT PERSISTENCE: Se a mensagem for curta e contiver indicadores de data/hora,
    # e o usuário estava agendando recentemente, mantém AGENDAR.
    is_time_or_date = re.search(r"(\d{1,2}h|\d{1,2}/\d{1,2}|amanhã|hoje)", msg_lower)
    if is_time_or_date and len(msg_lower) < 20:
        return IntentType.AGENDAR, 0.7

    return IntentType.CONVERSA, 0.5


# Sentiment detection moved to intelligence.py


def select_model(intent: IntentType, message: str) -> str:
    """
    Seleção de modelo baseada na complexidade - MCT Token Economy.

    Args:
        intent: Intenção classificada
        message: Mensagem original do usuário

    Returns:
        ID do modelo a ser usado (quick, standard, ou complex)
    """
    if intent in QUICK_INTENTS:
        return settings.model_quick
    if intent in COMPLEX_INTENTS or len(message) > 300:
        return settings.model_complex
    return settings.model_standard


# ═══════════════════════════════════════════════
# RESPONSE BUILDERS
# ═══════════════════════════════════════════════


async def get_quick_response(intent: IntentType) -> Optional[str]:
    """
    Respostas rápidas: KB primeiro, fallback local depois.
    Zero dependência de serviços externos.

    Args:
        intent: Intenção classificada

    Returns:
        Resposta rápida para a intenção, ou None se não encontrada
    """
    # Tenta Knowledge Base
    try:
        intent_val = intent.value if hasattr(intent, "value") else intent
        faq_result = kb.search_faq(intent_val)
        if faq_result:
            return faq_result.get("answer", faq_result.get("response", ""))
    except Exception as e:
        logger.debug(f"KB indisponível, usando fallback: {e}")

    # Fallback local garantido
    fallbacks = {
        IntentType.SAUDACAO: "Oi! Sou a Luna, assistente da Haven. Em que posso te ajudar hoje? ✨",
        IntentType.AGRADECIMENTO: "Por nada! Se precisar de mais alguma coisa, estou aqui. 😊",
        IntentType.LOCALIZACAO: "Estamos na Rua Mato Grosso, 837E - Jardim Itália, Chapecó. Esperamos você!",
        IntentType.HORARIO_FUNC: "Funcionamos de Segunda a Sábado, das 8h às 20h. 🕒",
    }
    return fallbacks.get(intent)


# ═══════════════════════════════════════════════
# CONTEXT BUILDERS (RAG)
# ═══════════════════════════════════════════════


async def build_context(client: Dict[str, Any], intent: IntentType, message: str) -> str:
    """
    Construção de contexto RAG baseado na intenção.

    Args:
        client: Perfil do cliente
        intent: Intenção classificada
        message: Mensagem original do usuário

    Returns:
        String de contexto formatado para o prompt da IA
    """
    context_parts = []

    # 1. Campanhas Ativas (Prioridade)
    await campaign_manager.sync_campaigns()
    camp = campaign_manager.detect_campaign(message)
    if camp:
        context_parts.append(campaign_manager.get_campaign_context(camp))

    # Serviços relevantes
    if intent in {
        IntentType.PRECO,
        IntentType.AGENDAR,
        IntentType.SERVICOS,
        IntentType.PACOTE,
        IntentType.SERVICOS_TECNICOS,
    }:
        services = kb.search_services(message)
        if services:
            context_parts.append(
                f"### SERVIÇOS RELEVANTES:\n{json.dumps(services[:5], ensure_ascii=False)}"
            )

    # Profissionais mencionados
    professionals = kb.search_professionals(message)
    if professionals:
        context_parts.append(
            f"### PROFISSIONAIS MENCIONADOS:\n{json.dumps(professionals, ensure_ascii=False)}"
        )

    # FAQ
    faq = kb.search_faq(message)
    if faq:
        context_parts.append(f"### FAQ:\n{json.dumps(faq, ensure_ascii=False)}")

    # Pacotes/Combos
    if intent == IntentType.PACOTE:
        packages = kb.get_packages()
        context_parts.append(
            f"### COMBO/PACOTES:\n{json.dumps(packages, ensure_ascii=False)}"
        )

    return "\n\n".join(context_parts)


def build_logic_prompt(client: Dict, recent: Dict, context: str) -> str:
    """
    Cérebro Lógico (DeepSeek/MiniMax): Frio, calculista, auditor matemático.
    Zero empatia. Foco apenas em REGRAS e PROTEÇÃO DE DADOS.
    """
    return f"""
<layer1_identity>
Você é o Cérebro Lógico Soberano da Haven Escovaria.
Seu objetivo é analisar o pedido do cliente contra as Regras de Negócio e o Banco de Dados.
Você NÃO fala com o cliente. Você apenas responde com comandos estruturados para a IA de Voz.
</layer1_identity>

<layer2_context>
Cliente: {client.get('name', 'Pessoa')}
Histórico: {recent.get('services_done', 'Nenhum')}
</layer2_context>

<layer3_rules_to_enforce>
1. ORDEM: Unhas → Cabelo → Maquiagem (NEGAR inversão).
2. ESCOVA: NÃO inclusa em Penteados e Tratamentos. (OBRIGAR A AVISAR SE NÃO INCLUIR).
3. GEL: Se pediu unha (feita por Dávila/Luisa/Mariana), PERGUNTA OBRIGATÓRIA: "Você já está com gel ou alongamento nas unhas?". Se sim, avisar taxa de remoção (R$30) e +30 min.
4. QUÍMICA: Para Progressiva/Mechas, fazer DIAGNÓSTICO (4 perguntas):
   a) Tem alguma química recente?
   b) Amamentando ou gestante? (Se sim, proibir Borabella se houver contraindicação).
   c) Qual o comprimento/volume? (Pedir foto se possível).
   d) Alguma alergia?
5. CÍNTIA: Fitagem até 16h (semana) ou 17h (sábado) - JAMAIS prometer horário, dizer que vai "ver com ela".
6. SUZANA: Alongamento exclusivo dela (R$450).
7. RETENÇÃO: Nunca fechar com "não". Se não tem horário, oferecer lista de espera ou profissional alternativa.
</layer3_rules_to_enforce>

<layer4_database>
{context}
</layer4_database>

<layer5_campaigns>
Se uma CAMPANHA ATIVA foi detectada no contexto acima, você DEVE priorizar a aplicação do desconto ou regra da campanha.
</layer5_campaigns>

Siga EXATAMENTE o formato:
[AÇÃO PRINCIPAL]: (Aprovar / Negar / Redirecionar / Coletar Dados / Handoff)
[REGRA APLICADA]: (Qual regra ou restrição guiou sua decisão)
[MANDAMENTO PARA A VOZ]: (Instrução direta e imperativa para a IA que vai escrever o texto. Ex: Diga que a escova é cobrada por fora).
[INTELLIGENCE_JSON]: (Crie um JSON puro com: insight, objections (lista), customer_mood (happy/frustrated/hesitant/hurry), urgency_level (1-5), potential_value (high/medium/low))
"""


def build_voice_prompt(
    client: Dict, recent: Dict, context: str, logic_directive: str
) -> str:
    """
    Cérebro de Voz (Claude 3.5 Sonnet): Carismático, vendedor, empático.
    Traduz os comandos frios da Lógica em Copywriting HIVE OS.
    """
    client_name = client.get("name", "Cliente")

    return f"""
<layer1_identity>
Você é Luna, a alma da recepção da Haven Escovaria & Esmalteria.
Sua voz é calorosa, profissional e tipicamente de Chapecó-SC.
Você cuida da autoestima das pessoas.
</layer1_identity>

<layer2_directive_from_logic_brain>
O Cérebro Operacional mapeou a seguinte realidade. Você DEVE obedecer e transformar isso em uma resposta natural:
{logic_directive}
</layer2_directive_from_logic_brain>

<layer3_voice_guidelines>
NO GO ZONE (Nunca use):
'prezada', 'senhora', 'aguarde', 'infelizmente', 'minutinho', 'verificar', 'desculpe o transtorno'

TOM E ESTILO (HIVE OS):
- Tom: Acolhedor, resolutivo, elegante e ágil.
- Saudação: "Oi [nome]! Que bom ter você aqui na Haven! 🌸"
- 1-2 emojis por mensagem.
- Chame o cliente pelo nome: {client_name}.
- Se a Diretriz mandar você negar algo, use a técnica de "Retenção": Ofereça uma alternativa imediata e positiva.
- LOCALIZAÇÃO: "Ficamos na Rua Mato Grosso, 837E - Jardim Itália (perto da pracinha). Temos estacionamento em frente! 🚗"
- FINALIZAÇÃO: Sempre confirme os detalhes e envie a localização ao fechar.
</layer3_voice_guidelines>
"""


# ═══════════════════════════════════════════════
# PARSERS
# ═══════════════════════════════════════════════


# Response parsing and field extraction moved to intelligence.py


# ═══════════════════════════════════════════════
# BRAIN ENGINE (Main Pipeline)
# ═══════════════════════════════════════════════


class BrainEngine:
    """
    Motor de Inteligência Soberana
    Pipeline de 5 estágios com fallback progressivo
    """

    async def process_message(
        self,
        phone: str,
        name: str,
        message: str,
        history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Pipeline principal de processamento.

        Garantia de Certeza Total:
          - Nível 1: Resposta local rápida (QUICK_INTENTS)
          - Nível 2: Resposta via IA (OpenRouter)
          - Nível 3: Fallback local seguro (nunca quebra)
        """
        start_time = time.time()

        # [KIMI-P5] Logger estruturado por sessão — rastreamento completo em produção
        log = logger.bind(phone=phone, name=name)
        log.info(f"🧠 Brain: Processing message for {phone} ({name})")

        # Safety fallback - NUNCA quebra
        safety_response = BrainResult(
            response="Oi! No momento estou processando algumas informações. Pode me dar um minutinho ou tentar novamente? 😊",
            intent=IntentType.UNKNOWN,
            model="local_resilience",
            processing_ms=int((time.time() - start_time) * 1000),
            intent_confidence=1.0,
        )

        try:
            # ── 1. Classificação Local ──
            intent, confidence = classify_intent(message)
            intent_val = intent.value if hasattr(intent, "value") else intent
            log.info(f"🎯 Intent classified: {intent_val} (conf: {confidence:.2f})")

            # ── 2. Fast-Path: Respostas locais ──
            if intent in QUICK_INTENTS and confidence > 0.8:
                response_text = await get_quick_response(intent)
                if response_text:
                    log.info(f"⚡ Fast-path activated for intent '{intent_val}'")
                    result = BrainResult(
                        response=response_text,
                        intent=intent,
                        model="local_rules",
                        processing_ms=int((time.time() - start_time) * 1000),
                        intent_confidence=confidence,
                    )
                    if intent == IntentType.LOCALIZACAO:
                        result.action = "send_location"
                    elif intent == IntentType.HANDOFF:
                        result.action = "handoff"
                    return result.to_dict()

            # ── 3. Detect Campaign ──
            camp = campaign_manager.detect_campaign(message)

            # ── 4. IA Processing ──
            try:
                return await self._process_with_ai(
                    phone, name, message, intent, confidence, history, start_time, camp
                )
            except Exception as ai_err:
                log.error(
                    f"🚨 AI failure (fallback activated): {type(ai_err).__name__}: {ai_err}"
                )
                safety_response.processing_ms = int((time.time() - start_time) * 1000)
                return safety_response.to_dict()

        except Exception as e:
            logger.bind(phone=phone).exception(
                f"❌ Critical error in Brain pipeline: {e}"
            )
            safety_response.processing_ms = int((time.time() - start_time) * 1000)
            return safety_response.to_dict()

    async def _process_with_ai(
        self,
        phone: str,
        name: str,
        message: str,
        intent: IntentType,
        confidence: float,
        history: Optional[List[Dict]],
        start_time: float,
        camp: Optional[Dict] = None,
    ) -> Dict:
        """Processamento via IA (OpenRouter)"""
        # Cliente e Conversa
        client = await memory.get_or_create_client(phone, name)
        client_id = client.get("id")
        logger.debug(f"Cliente identificado: {client_id}")

        # Garante conversa ativa para persistência de dados extraídos
        active_conv = await memory.get_active_conversation(phone)
        if not active_conv:
            await memory.start_conversation(phone, client_id)

        # Modelo
        model = select_model(intent, message)
        logger.info(f"🤖 Model selected: {model}")

        # Contexto RAG
        context = await build_context(client, intent, message)
        logger.debug(f"Context built: {'RAG OK' if context else 'Empty'}")

        # Histórico recente
        recent = await memory.get_recent_history(phone)

        # System prompt
        logic_prompt = build_logic_prompt(client, recent, context)

        # Chamada 1: Cérebro Lógico (DeepSeek-R1 / MiniMax / Modelos de Raciocínio)
        # O OpenRouter envia para um modelo focado apenas em Extração de Regras
        # [DEBT #M5] Usar settings.model_quick como fallback (configurável via ENV)
        logic_model = os.getenv("LOGIC_MODEL_ID", settings.model_quick)
        logger.info(f"🧠 Pass 1: Logic Engine ({logic_model})")

        logic_messages = history.copy() if history else []
        logic_messages.append({"role": "user", "content": message})

        logic_text = await openrouter.complete(
            messages=logic_messages,
            system=logic_prompt,
            model=logic_model,
            temperature=0.1,  # Muito baixo para zero alucinação
        )

        logger.debug(f"📐 Logic Directive:\n{logic_text}")

        # Parse rudimentar da inteligência de dentro da lógica
        intelligence = extract_intelligence_fallback(logic_text)
        try:
            json_match = re.search(r"\[INTELLIGENCE_JSON\]:(.*)", logic_text, re.DOTALL)
            if json_match:
                intel_str = re.sub(
                    r"```json\n?|\n?```", "", json_match.group(1)
                ).strip()
                intelligence = parse_intelligence_safe(json.loads(intel_str))

                # [NEW] Push Instantâneo para o CRM Front-end (WAScript)
                # Formata o DDI apenas se não for um teste simulado
                import asyncio

                clean_phone = phone.replace("temp_", "")

                # Convert Pydantic object to dict for the CRM payload
                intel_dict = {}
                if hasattr(intelligence, "model_dump"):
                    intel_dict = intelligence.model_dump()
                elif hasattr(intelligence, "dict"):
                    intel_dict = intelligence.dict()
                elif isinstance(intelligence, dict):
                    intel_dict = intelligence

                if intel_dict.get("insight"):
                    asyncio.create_task(
                        wascript.add_client_note(clean_phone, intel_dict)
                    )
        except Exception as json_e:
            logger.warning(f"Error parsing logic brain JSON: {json_e}")

        # Chamada 2: Cérebro Interator / Voz (Claude 3.5 Sonnet / Llama)
        voice_prompt = build_voice_prompt(client, recent, context, logic_text)
        voice_model = os.getenv("VOICE_MODEL_ID", "anthropic/claude-3.5-sonnet")

        logger.info(f"🗣️ Pass 2: Voice Engine ({voice_model})")

        # Para a voz, mandamos o histórico, mas o "System" agora traz o peso do Logic Brain
        voice_messages = history.copy() if history else []
        voice_messages.append({"role": "user", "content": message})

        # OpenRouter call
        response_text = await openrouter.complete(
            messages=voice_messages,
            system=voice_prompt,
            model=voice_model,
            temperature=0.7,
        )

        # Como a voz só gera a resposta limpa agora (sem o payload JSON embutido na string)
        response_part = response_text.replace("---RESPONSE---", "").strip()

        # Build result
        result = BrainResult(
            response=response_part,
            intent=intent,
            model=f"DualBrain({logic_model} -> {voice_model})",
            sentiment=intelligence.detect_sentiment(message),
            intent_confidence=confidence,
            processing_ms=int((time.time() - start_time) * 1000),
            intelligence=intelligence,
        )

        # Actions based on intent
        if intent == IntentType.LOCALIZACAO:
            result.action = "send_location"
        elif intent == IntentType.HANDOFF:
            result.action = "handoff"

        # Extração de campos via módulo especializado
        extracted = intelligence.extract_fields(message, result.response)

        # [NEW] Belasis Scheduling Integration
        if intent == IntentType.AGENDAR:
            logger.info("📅 Scheduling Intent detected. Processing with Scheduler...")
            # Combina dados da memória com dados novos
            all_extracted = await memory.get_extracted_data(phone)
            all_extracted.update(extracted)

            # [FISICA DO ATENDIMENTO] Analisar múltiplos serviços
            servicos_lista = all_extracted.get("services", [])
            if len(servicos_lista) > 1:
                analise = physics.analisar_compatibilidade_servicos(servicos_lista)
                feedback_fisica = physics.gerar_script_multi_servicos(
                    servicos_lista, analise
                )
                logger.info(
                    f"🧬 Física do Atendimento Ativada: {len(servicos_lista)} serviços"
                )
            else:
                feedback_fisica = None

            success, feedback_scheduler, booking_data = await scheduler.process_booking(
                {**all_extracted, "phone": phone, "name": name}
            )

            # Prioriza o feedback da "Física" se houver múltiplos serviços e sucesso no agendamento básico
            if feedback_fisica:
                result.response = f"{feedback_fisica}\n\n{feedback_scheduler}"
            else:
                result.response = feedback_scheduler

            if success:
                result.action = "confirm_appointment"
                if isinstance(intelligence, dict):
                    intelligence["planned_appointment"] = booking_data
                else:
                    setattr(intelligence, "planned_appointment", booking_data)

        # [ANTI-ALUCINAÇÃO] Aplicar regras de negativação via módulo especializado
        result.response = rules.verificar_regras_negativação(result.response)

        # ═══════════════════════════════════════════════
        # [AUTOMELHORIA] Guardrails + Confidence + Learning
        # ═══════════════════════════════════════════════

        # Passo 1: Validar contra Source of Truth
        guardrail_result = guardrails.validate(result.response, intent=intent_val)

        if not guardrail_result.passed:
            # Substituir resposta se guardrails bloquearam
            result.response = guardrail_result.response
            logger.bind(phone=phone).warning(
                f"🛡️ Guardrails ativados | {len(guardrail_result.violations)} violações"
            )
            # Log cada violação no Supabase
            active_conv = await memory.get_active_conversation(phone)
            conv_id = active_conv.get("id") if active_conv else None
            for v in guardrail_result.violations:
                try:
                    await guardrails.log_violation(phone, conv_id, v)
                except Exception:
                    pass

        # Passo 2: Buscar padrões aprendidos (golden examples)
        learned_patterns = await learning.get_relevant_patterns(
            message=message, intent=intent_val, limit=2
        )
        has_learning = len(learned_patterns) > 0

        # Passo 3: Calcular confidence score
        conf_score = calculate_confidence(
            intent_confidence=confidence,
            guardrail_penalty=guardrail_result.confidence_penalty,
            data_completeness=min(1.0, len(extracted) / 3.0) if extracted else 0.3,
            has_learning_match=has_learning,
        )

        # Passo 4: Decidir ação baseada no score
        conf_action = decide_action(conf_score)

        if conf_action == "escalate":
            result.action = "handoff"
            result.response = (
                "Oi! Vou te transferir para uma das nossas atendentes "
                "para garantir que você tenha o melhor atendimento 💙"
            )
            logger.bind(phone=phone).warning(
                f"📊 Confidence BAIXA ({conf_score:.2f}) → ESCALAÇÃO automática"
            )
        elif conf_action == "send_flagged":
            logger.bind(phone=phone).info(
                f"📊 Confidence MÉDIA ({conf_score:.2f}) → Enviado com flag"
            )

        # Adicionar metadata de confiança ao resultado
        if isinstance(result.intelligence, IntelligenceData):
            result.intelligence.metadata["confidence_score"] = conf_score
            result.intelligence.metadata["guardrail_passed"] = guardrail_result.passed
            result.intelligence.metadata["learning_patterns_used"] = len(
                learned_patterns
            )

        # [NEW] Campaign Attribution
        if camp:
            extracted["campaign_id"] = camp.get("id")

        for field_name, value in extracted.items():
            if value:
                logger.debug(f"Extracted field: {field_name}={value}")
                await memory.save_extracted_data(phone, field_name, value)

        logger.info(
            f"✅ Brain: Response generated in {result.processing_ms}ms | "
            f"confidence={conf_score:.2f} | action={conf_action}"
        )
        return result.to_dict()


# Legacy wrapper for backward compatibility
async def process_message(
    phone: str,
    name: str,
    message: str,
    history: Optional[List[Dict]] = None,
) -> Dict:
    """Wrapper para compatibilidade com código legado"""
    brain = BrainEngine()
    return await brain.process_message(phone, name, message, history)
