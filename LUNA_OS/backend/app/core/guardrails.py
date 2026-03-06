"""
LUNA Guardrails Engine — Anti-Alucinação Dinâmica
Padrão Kimi-SWE: Validação pós-resposta contra Source of Truth.

Pipeline:
  LLM → guardrails.validate() → [OK?] → Cliente
                                  ↓ [FAIL]
                               Resposta segura + log violação

DEBT #M3: Type hints completos
DEBT #M4: Docstrings em todas as funções públicas
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from loguru import logger

from app.core.config_haven import PROFISSIONAIS, SERVICOS


# ═══════════════════════════════════════════════
# SOURCE OF TRUTH (extraído do config_haven)
# ═══════════════════════════════════════════════


def _build_known_professionals() -> Dict[str, str]:
    """Constrói mapa de nomes/apelidos válidos → chave interna."""
    known = {}
    for key, prof in PROFISSIONAIS.items():
        nome = prof.get("nome", "").lower()
        apelido = prof.get("apelido", "").lower()
        if nome:
            known[nome] = key
        if apelido and apelido != nome:
            known[apelido] = key
    return known


def _build_known_services() -> Dict[str, Dict]:
    """Constrói mapa de nomes de serviço normalizados → dados."""
    known = {}
    for key, svc in SERVICOS.items():
        nome = svc.get("nome", "").lower()
        known[nome] = {"key": key, **svc}
        # Também registrar a chave como alias
        known[key.replace("_", " ")] = {"key": key, **svc}
    return known


# Caches construídos na importação (inicialização zero-cost)
KNOWN_PROFESSIONALS = _build_known_professionals()
KNOWN_SERVICES = _build_known_services()

# Nomes válidos para menção (títulos capitalizados)
VALID_PROF_NAMES = {prof.get("nome", "") for prof in PROFISSIONAIS.values()}


# ═══════════════════════════════════════════════
# VIOLATION TYPES
# ═══════════════════════════════════════════════


@dataclass
class GuardrailViolation:
    """
    Registro de uma violação detectada.

    Attributes:
        violation_type: Tipo de violação ("fake_professional", "fake_price", etc.)
        original_text: Texto original que causou a violação
        corrected_text: Texto corrigido
        source_of_truth: Fonte de verdade usada para validação
        severity: Severidade da violação ("low", "medium", "high")
    """

    violation_type: str
    original_text: str
    corrected_text: str
    source_of_truth: str
    severity: str = "medium"


@dataclass
class GuardrailResult:
    """
    Resultado da validação.

    Attributes:
        passed: True se passou por todas as validações
        response: Resposta (original ou corrigida)
        violations: Lista de violações encontradas
        confidence_penalty: Penalidade aplicada ao confidence score (0.0-1.0)
    """

    passed: bool = True
    response: str = ""
    violations: List[GuardrailViolation] = field(default_factory=list)
    confidence_penalty: float = 0.0  # 0.0 = sem penalidade, 1.0 = confiança zero


# ═══════════════════════════════════════════════
# GUARDRAIL CHECKS
# ═══════════════════════════════════════════════


def _check_professionals(response: str) -> Optional[GuardrailViolation]:
    """
    Verifica se profissionais mencionados existem na equipe.
    Padrão: qualquer nome próprio capitalizado é verificado.
    """
    # Procurar menções tipo "com a [Nome]", "profissional [Nome]", "a [Nome]"
    patterns = [
        r"com (?:a |o )?([A-ZÀ-Ú][a-zà-ú]+)",
        r"profissional (?:é )?(?:a |o )?([A-ZÀ-Ú][a-zà-ú]+)",
        r"(?:a |o )([A-ZÀ-Ú][a-zà-ú]+) (?:vai|faz|atende|pode)",
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, response)
        for match in matches:
            name = match.group(1)
            name_lower = name.lower()

            # Ignorar palavras comuns que parecem nomes
            common_words = {
                "oi",
                "olá",
                "temos",
                "posso",
                "vou",
                "claro",
                "dias",
                "hoje",
                "amanhã",
                "segunda",
                "terça",
                "quarta",
                "quinta",
                "sexta",
                "sábado",
                "domingo",
                "sim",
                "não",
                "bom",
                "boa",
                "haven",
                "luna",
                "escova",
                "gel",
                "tudo",
            }
            if name_lower in common_words:
                continue

            # Verificar se é profissional conhecida
            if name_lower not in KNOWN_PROFESSIONALS:
                return GuardrailViolation(
                    violation_type="fake_professional",
                    original_text=name,
                    corrected_text=f"Profissional '{name}' não está na nossa equipe",
                    source_of_truth=f"Equipe atual: {', '.join(VALID_PROF_NAMES)}",
                    severity="high",
                )
    return None


def _check_prices(response: str) -> Optional[GuardrailViolation]:
    """
    Verifica se preços mencionados correspondem aos reais.
    Detecta padrões: R$ XX, R$XX,XX, XX reais.
    """
    price_patterns = [
        r"R\$\s*(\d+(?:[.,]\d{2})?)",
        r"(\d+(?:[.,]\d{2})?)\s*reais",
    ]

    for pattern in price_patterns:
        matches = re.finditer(pattern, response, re.IGNORECASE)
        for match in matches:
            price_str = match.group(1).replace(",", ".")
            try:
                mentioned_price = float(price_str)
            except ValueError:
                continue

            # Coletar todos os preços reais do cardápio
            all_real_prices = set()
            for svc in SERVICOS.values():
                valor = svc.get("valor")
                if isinstance(valor, (int, float)):
                    all_real_prices.add(float(valor))
                promo = svc.get("valor_promo_seg_qua")
                if isinstance(promo, (int, float)):
                    all_real_prices.add(float(promo))
                # Preços por profissional
                for key in ["valor_davila", "valor_lu_edna"]:
                    v = svc.get(key)
                    if isinstance(v, (int, float)):
                        all_real_prices.add(float(v))
                # Valores em sub-dicts
                vals = svc.get("valores", {})
                if isinstance(vals, dict):
                    for v in vals.values():
                        if isinstance(v, (int, float)):
                            all_real_prices.add(float(v))

            # Verificar se o preço mencionado existe no cardápio
            if mentioned_price not in all_real_prices:
                # Tolerância de R$ 1 para arredondamentos
                close_match = any(
                    abs(mentioned_price - rp) <= 1.0 for rp in all_real_prices
                )
                if not close_match:
                    return GuardrailViolation(
                        violation_type="fake_price",
                        original_text=f"R$ {mentioned_price:.2f}",
                        corrected_text="Preço mencionado não encontrado no cardápio",
                        source_of_truth=f"Preços válidos: {sorted(all_real_prices)}",
                        severity="high",
                    )

    return None


def _check_time_confirmation(response: str) -> Optional[GuardrailViolation]:
    """
    Detecta se a LUNA está CONFIRMANDO um horário sem checagem.
    Padrões perigosos: "agendei", "confirmado às", "seu horário é"
    """
    confirmation_patterns = [
        r"(?:agendei|confirmei|reservei|marquei).*(?:\d{1,2}h|\d{1,2}:\d{2})",
        r"seu (?:horário|agendamento) (?:é|está|ficou).*(?:\d{1,2}h|\d{1,2}:\d{2})",
        r"(?:confirmado|agendado) (?:para|às).*(?:\d{1,2}h|\d{1,2}:\d{2})",
    ]

    for pattern in confirmation_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return GuardrailViolation(
                violation_type="unverified_time",
                original_text="Confirmação de horário detectada",
                corrected_text="Vou verificar a disponibilidade e confirmo em seguida!",
                source_of_truth="Regra: nunca confirmar horário sem checar agenda Belasis/Supabase",
                severity="high",
            )

    return None


def _check_services(response: str) -> Optional[GuardrailViolation]:
    """
    Detecta menção a serviços inexistentes.
    Verifica quando LUNA diz "oferecemos [X]" ou "temos [X]".
    """
    service_mention_patterns = [
        r"(?:oferecemos|temos|fazemos|realizamos)\s+(?:o\s+)?(?:serviço\s+de\s+)?([a-zà-úA-ZÀ-Ú\s]{3,30}?)(?:\.|,|!|\?|$)",
    ]

    # Não verificar se for uma frase genérica
    generic = ["tudo", "vários", "diversos", "todos os serviços"]

    for pattern in service_mention_patterns:
        matches = re.finditer(pattern, response, re.IGNORECASE)
        for match in matches:
            service_name = match.group(1).strip().lower()
            if service_name in generic or len(service_name) < 4:
                continue

            # Verificar se o serviço existe (fuzzy match simples)
            found = False
            for known_name in KNOWN_SERVICES:
                if service_name in known_name or known_name in service_name:
                    found = True
                    break

            if not found:
                return GuardrailViolation(
                    violation_type="fake_service",
                    original_text=service_name,
                    corrected_text=f"Serviço '{service_name}' não está no nosso cardápio",
                    source_of_truth="Cardápio: config_haven.SERVICOS",
                    severity="medium",
                )

    return None


def _check_past_date(response: str) -> Optional[GuardrailViolation]:
    """
    Detecta se a LUNA está sugerindo/confirmando uma data no passado.
    """
    today = datetime.now()
    date_patterns = [
        r"(\d{1,2})/(\d{1,2})",
        r"dia (\d{1,2}) de (\w+)",
    ]

    for pattern in date_patterns:
        match = re.search(pattern, response)
        if match:
            try:
                day = int(match.group(1))
                month_str = match.group(2)

                # Tentar parsing numérico
                try:
                    month = int(month_str)
                except ValueError:
                    # É um nome de mês — ignorar parsing complexo por agora
                    continue

                candidate = datetime(today.year, month, day)
                if candidate.date() < today.date():
                    return GuardrailViolation(
                        violation_type="past_date",
                        original_text=f"{day}/{month}",
                        corrected_text="Data no passado detectada",
                        source_of_truth=f"Data atual: {today.strftime('%d/%m/%Y')}",
                        severity="medium",
                    )
            except (ValueError, IndexError):
                continue

    return None


# ═══════════════════════════════════════════════
# MAIN VALIDATION
# ═══════════════════════════════════════════════


def validate(response: str, intent: str = None) -> GuardrailResult:
    """
    Valida uma resposta gerada pelo LLM contra a Source of Truth.

    Returns:
        GuardrailResult com passed=True se OK, ou passed=False com violações.
    """
    result = GuardrailResult(response=response, passed=True)
    log = logger.bind(module="guardrails")

    checks = [
        _check_professionals,
        _check_prices,
        _check_time_confirmation,
        _check_services,
        _check_past_date,
    ]

    for check_fn in checks:
        try:
            violation = check_fn(response)
            if violation:
                result.violations.append(violation)
                result.passed = False

                # Aplicar penalidade proporcional à severidade
                severity_penalty = {"low": 0.1, "medium": 0.2, "high": 0.4}
                result.confidence_penalty += severity_penalty.get(
                    violation.severity, 0.2
                )

                log.warning(
                    f"🛡️ GUARDRAIL [{violation.violation_type}] | "
                    f"'{violation.original_text}' → {violation.corrected_text}"
                )

        except Exception as e:
            log.error(f"Guardrail check {check_fn.__name__} error: {e}")
            continue

    # Se houve violações de alta severidade, substituir resposta inteira
    high_violations = [v for v in result.violations if v.severity == "high"]

    if high_violations:
        # Dá precedência para erros de confirmação de horário não verificada e preços errados.
        has_time_error = any(
            v.violation_type == "unverified_time" for v in high_violations
        )
        has_price_error = any(v.violation_type == "fake_price" for v in high_violations)
        has_prof_error = any(
            v.violation_type == "fake_professional" for v in high_violations
        )

        # Padrão de respostas de fuga predefinidas (Segurança Total)
        if has_price_error:
            result.response = (
                "Oi! Desculpe, mas houve uma divergência na leitura do nosso cardápio. "
                "Para garantir que eu não te passe o valor errado, vou deixar anotado aqui e uma de nossas meninas "
                "da recepção já confirma o valor exato desse procedimento para você, tá bem? 💛"
            )
        elif has_time_error:
            # Pega o texto da violação de tempo específica para aplicar a resposta corrigida do guardrail
            time_violation = next(
                v for v in high_violations if v.violation_type == "unverified_time"
            )
            result.response = time_violation.corrected_text
        elif has_prof_error:
            result.response = (
                f"Deixa eu verificar isso direitinho com a nossa equipe! 😉 "
                f"Lembrando que nossas profissionais maravilhosas hoje são: {', '.join(sorted(VALID_PROF_NAMES))}. "
                f"Qualquer dúvida, eu peço para a gerente entrar em contato contigo!"
            )
        else:
            # Fallback genérico para HIGH severity
            v = high_violations[0]
            result.response = v.corrected_text

        log.error(
            f"🚫 RESPOSTA SUBSTITUÍDA | {len(high_violations)} violações graves | "
            f"principais_tipos={', '.join([v.violation_type for v in high_violations])}"
        )

    # Cap penalty
    result.confidence_penalty = min(1.0, result.confidence_penalty)

    return result


async def log_violation(
    phone: str,
    conversation_id: str,
    violation: GuardrailViolation,
    db=None,
):
    """Persiste violação no Supabase para auditoria."""
    if not db:
        try:
            from app.integrations.supabase_client import get_supabase

            db = get_supabase()
        except Exception:
            logger.warning("Supabase indisponível — violação não persistida")
            return

    try:
        db.table("guardrail_violations").insert(
            {
                "phone": phone,
                "conversation_id": conversation_id,
                "violation_type": violation.violation_type,
                "original_response": violation.original_text,
                "corrected_response": violation.corrected_text,
                "source_of_truth": violation.source_of_truth,
            }
        ).execute()
    except Exception as e:
        logger.error(f"Erro ao salvar violação: {e}")
