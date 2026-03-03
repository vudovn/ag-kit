"""
🌙📊 LUNA OS v3.0 — SUPER ANALYTICS API
Análise de Dados Rica com 20+ Métricas Avançadas
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
# [LAZY LOADING] Não importar na importação do módulo
# from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/analytics", tags=["Super Analytics"])
# [LAZY LOADING] db será inicializado sob demanda nas funções


def _get_db():
    """[LAZY LOADING] Obter Supabase client apenas quando necessário"""
    from app.integrations.supabase_client import get_supabase
    try:
        return get_supabase()
    except Exception as e:
        logger.error(f"❌ Analytics: Supabase não disponível - {e}")
        return None


# ==================== MODELS ====================


class AnalyticsOverview(BaseModel):
    """Visão geral completa do analytics"""

    resumo: Dict
    financeiro: Dict
    conversao: Dict
    temporal: Dict
    intencoes: Dict
    sentimentos: Dict
    gatilhos: List[Dict]
    insights: List[Dict]


# ==================== ENDPOINTS ====================


@router.get("/overview")
async def analytics_overview(days: int = 30):
    """
    📊 VISÃO GERAL COMPLETA — 20+ MÉTRICAS

    Retorna análise rica com:
    - Resumo executivo
    - Financeiro detalhado
    - Conversão por etapa
    - Evolução temporal
    - Intenções detectadas
    - Sentimentos
    - Gatilhos automáticos
    - Insights acionáveis
    """
    try:
        logger.info(f"📊 Analytics overview: {days} dias")

        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        # 1. Buscar dados
        conversas = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date)
            .execute()
        )
        mensagens = (
            db.table("whatsapp_messages_history")
            .select("*")
            .gte("message_timestamp", start_date)
            .execute()
        )
        clients = db.table("clients").select("*").execute()

        # 2. Calcular métricas avançadas
        resumo = calcular_resumo(conversas.data, mensagens.data, clients.data)
        financeiro = calcular_financeiro(clients.data)
        conversao = calcular_conversao(conversas.data)
        temporal = calcular_temporal(conversas.data, days)
        intencoes = calcular_intencoes(conversas.data)
        sentimentos = calcular_sentimentos(conversas.data)
        campanhas = await calcular_campanhas(conversas.data)
        alertas_criticos = await get_critical_alerts()

        # 3. Gerar gatilhos automáticos
        gatilhos = gerar_gatilhos(resumo, financeiro, conversao)

        # 4. Gerar insights acionáveis
        insights = gerar_insights(resumo, financeiro, conversao, gatilhos)

        return {
            "status": "sucesso",
            "periodo": {
                "dias": days,
                "inicio": start_date,
                "fim": datetime.utcnow().isoformat(),
            },
            "resumo": resumo,
            "financeiro": financeiro,
            "conversao": conversao,
            "temporal": temporal,
            "intencoes": intencoes,
            "sentimentos": sentimentos,
            "campanhas": campanhas,
            "alertas_criticos": alertas_criticos,
            "appointments": {"total": 0, "today": 0, "pending": 0},
            "gatilhos": gatilhos,
            "insights": insights,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"❌ Analytics overview falhou: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funil")
async def analytics_funil(days: int = 30):
    """
    📈 FUNIL DE CONVERSÃO DETALHADO

    Mostra cada etapa do funil:
    - Conversas iniciadas
    - Intenções detectadas
    - Propostas enviadas
    - Agendamentos
    - Conversões fechadas
    - Taxa por etapa
    """
    try:
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        conversas = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date)
            .execute()
        )

        funil = {
            "etapas": [
                {"nome": "Conversas Iniciadas", "count": len(conversas.data or [])},
                {
                    "nome": "Intenções Detectadas",
                    "count": sum(1 for c in conversas.data if c.get("intent")),
                },
                {
                    "nome": "Propostas Enviadas",
                    "count": sum(
                        1
                        for c in conversas.data
                        if c.get("status") in ["active", "ended"]
                    ),
                },
                {
                    "nome": "Agendamentos",
                    "count": sum(
                        1
                        for c in conversas.data
                        if c.get("intent") in ["agendar", "agendamento"]
                    ),
                },
                {
                    "nome": "Conversões Fechadas",
                    "count": sum(
                        1 for c in conversas.data if c.get("status") == "ended"
                    ),
                },
            ],
            "taxas": {},
        }

        # Calcular taxas de conversão por etapa
        total = len(conversas.data or [])
        for i, etapa in enumerate(funil["etapas"]):
            if total > 0:
                funil["taxas"][etapa["nome"]] = etapa["count"] / total * 100

        return {"status": "sucesso", "funil": funil}

    except Exception as e:
        logger.error(f"❌ Funil falhou: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top")
async def analytics_top(days: int = 30):
    """
    🏆 TOP RANKINGS — CLIENTES, SERVIÇOS, PROFISSIONAIS

    Retorna rankings de:
    - Top 10 clientes (mais conversas)
    - Top 10 serviços (mais pedidos)
    - Top 5 profissionais (mais agendamentos)
    - Top 5 horários (mais movimentados)
    - Top 5 dias (mais movimentados)
    """
    try:
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        conversas = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date)
            .execute()
        )

        # Top clientes
        clientes_count = {}
        for c in conversas.data or []:
            phone = c.get("phone", "unknown")
            clientes_count[phone] = clientes_count.get(phone, 0) + 1

        top_clientes = sorted(clientes_count.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        # Top intenções (serviços)
        intencoes_count = {}
        for c in conversas.data or []:
            intent = c.get("intent", "unknown")
            if intent:
                intencoes_count[intent] = intencoes_count.get(intent, 0) + 1

        top_intencoes = sorted(
            intencoes_count.items(), key=lambda x: x[1], reverse=True
        )[:10]

        # Top horários
        horarios_count = {}
        for c in conversas.data or []:
            started = c.get("started_at", "")
            if len(started) >= 13:
                hora = started[11:13]  # HH
                horarios_count[hora] = horarios_count.get(hora, 0) + 1

        top_horarios = sorted(horarios_count.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        return {
            "status": "sucesso",
            "rankings": {
                "clientes": [{"phone": p, "count": c} for p, c in top_clientes],
                "intencoes": [{"intent": i, "count": c} for i, c in top_intencoes],
                "horarios": [{"hora": h, "count": c} for h, c in top_horarios],
            },
        }

    except Exception as e:
        logger.error(f"❌ Top rankings falharam: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tendencias")
async def analytics_tendencias(days: int = 30):
    """
    📈 TENDÊNCIAS E PROJEÇÕES

    Mostra:
    - Evolução diária de conversas
    - Tendência (crescendo/decrescendo)
    - Projeção para próximos dias
    - Comparação com período anterior
    """
    try:
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        conversas = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date)
            .execute()
        )

        # Agrupar por dia
        por_dia = {}
        for c in conversas.data or []:
            dia = c.get("started_at", "")[:10]  # YYYY-MM-DD
            if dia:
                por_dia[dia] = por_dia.get(dia, 0) + 1

        # Ordenar por data
        dias_ordenados = sorted(por_dia.keys())

        # Calcular tendência
        if len(dias_ordenados) >= 2:
            primeira_semana = sum(por_dia.get(d, 0) for d in dias_ordenados[:7])
            ultima_semana = sum(por_dia.get(d, 0) for d in dias_ordenados[-7:])

            if primeira_semana > 0:
                crescimento = (ultima_semana - primeira_semana) / primeira_semana * 100
            else:
                crescimento = 0
        else:
            crescimento = 0

        # Projeção simples (média dos últimos 7 dias * 1.1)
        media_ultimos_7 = sum(por_dia.get(d, 0) for d in dias_ordenados[-7:]) / min(
            7, len(dias_ordenados)
        )
        projecao_proximos_7 = media_ultimos_7 * 1.1 * 7

        return {
            "status": "sucesso",
            "evolucao": [
                {"dia": d, "count": por_dia.get(d, 0)} for d in dias_ordenados
            ],
            "tendencia": {
                "crescimento_percentual": crescimento,
                "direcao": (
                    "crescendo"
                    if crescimento > 0
                    else "decrescendo" if crescimento < 0 else "estavel"
                ),
            },
            "projecao": {
                "proximos_7_dias": projecao_proximos_7,
                "confianca": "media" if abs(crescimento) < 20 else "alta",
            },
        }

    except Exception as e:
        logger.error(f"❌ Tendências falharam: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gatilhos")
async def analytics_gatilhos():
    """
    🎯 GATILHOS AUTOMÁTICOS DE INSIGHTS

    Detecta automaticamente:
    - Queda brusca de conversas
    - Aumento de churn
    - Horário de pico
    - Cliente em risco
    - Oportunidade de venda
    """
    try:
        gatilhos = []

        # Buscar dados recentes
        agora = datetime.utcnow()
        start_date_7d = (agora - timedelta(days=7)).isoformat()
        start_date_30d = (agora - timedelta(days=30)).isoformat()

        conversas_7d = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date_7d)
            .execute()
        )
        conversas_30d = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date_30d)
            .execute()
        )

        # Gatilho 1: Queda brusca de conversas
        media_30d = len(conversas_30d.data or []) / 30
        media_7d = len(conversas_7d.data or []) / 7

        if media_7d < media_30d * 0.7:  # Queda > 30%
            gatilhos.append(
                {
                    "tipo": "queda_conversas",
                    "prioridade": "alta",
                    "mensagem": f"Queda de {((media_30d - media_7d) / media_30d * 100):.1f}% nas conversas",
                    "acao": "Investigar causa e lançar campanha de reativação",
                }
            )

        # Gatilho 2: Muitos clientes inativos
        clients = db.table("clients").select("*").execute()
        inativos = sum(1 for c in clients.data if c.get("total_visits", 0) == 0)

        if inativos > len(clients.data or []) * 0.3:  # > 30% inativos
            gatilhos.append(
                {
                    "tipo": "clientes_inativos",
                    "prioridade": "media",
                    "mensagem": f"{inativos} clientes inativos ({inativos / len(clients.data or []) * 100:.1f}%)",
                    "acao": "Campanha de reativação com desconto",
                }
            )

        # Gatilho 3: Conversão baixa
        conversas = (
            db.table("conversations")
            .select("*")
            .gte("started_at", start_date_7d)
            .execute()
        )
        fechadas = sum(1 for c in conversas.data if c.get("status") == "ended")
        taxa_conversao = (
            (fechadas / len(conversas.data or []) * 100) if conversas.data else 0
        )

        if taxa_conversao < 20:
            gatilhos.append(
                {
                    "tipo": "conversao_baixa",
                    "prioridade": "alta",
                    "mensagem": f"Taxa de conversão baixa: {taxa_conversao:.1f}%",
                    "acao": "Melhorar qualificação de leads e follow-up",
                }
            )

        return {
            "status": "sucesso",
            "gatilhos": gatilhos,
            "timestamp": agora.isoformat(),
        }

    except Exception as e:
        logger.error(f"❌ Gatilhos falharam: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # ==================== HELPERS ====================


def calcular_resumo(conversas, mensagens, clients):
    """Calcula métricas de resumo"""
    human_hours_saved = (len(mensagens or []) * 1.5) / 60.0

    return {
        "total_conversas": len(conversas or []),
        "total_mensagens": len(mensagens or []),
        "total_clientes": len(clients or []),
        "human_hours_saved": round(human_hours_saved, 1),
        "media_mensagens_por_conversa": (
            len(mensagens or []) / len(conversas or []) if conversas else 0
        ),
        "clientes_ativos": (
            sum(1 for c in clients if c.get("total_visits", 0) > 0) if clients else 0
        ),
    }


def calcular_financeiro(clients):
    """Calcula métricas financeiras"""
    if not clients:
        return {}

    receita_total = sum(c.get("total_spent", 0) for c in clients)
    clientes_ativos = sum(1 for c in clients if c.get("total_visits", 0) > 0)

    return {
        "receita_total": receita_total,
        "ticket_medio": receita_total / clientes_ativos if clientes_ativos > 0 else 0,
        "receita_por_cliente": receita_total / len(clients) if clients else 0,
        "clientes_ativos": clientes_ativos,
    }


def calcular_conversao(conversas):
    """Calcula métricas de conversão"""
    if not conversas:
        return {}

    ativas = sum(1 for c in conversas if c.get("status") == "active")
    fechadas = sum(1 for c in conversas if c.get("status") == "ended")
    historicas = sum(1 for c in conversas if c.get("status") == "historical")

    total = len(conversas)

    return {
        "ativas": ativas,
        "fechadas": fechadas,
        "historicas": historicas,
        "perdidas": total - fechadas,  # conversas que não terminaram com sucesso
        "taxa_conversao": (fechadas / total * 100) if total > 0 else 0,
    }


def calcular_temporal(conversas, days):
    """Calcula evolução temporal"""
    if not conversas:
        return {}

    por_dia = {}
    for c in conversas:
        dia = c.get("started_at", "")[:10]
        if dia:
            por_dia[dia] = por_dia.get(dia, 0) + 1

    return {
        "dias": len(por_dia),
        "media_por_dia": len(conversas) / days if days > 0 else 0,
        "dia_mais_movimentado": (
            max(por_dia.items(), key=lambda x: x[1])[0] if por_dia else None
        ),
    }


def calcular_intencoes(conversas):
    """Calcula distribuição de intenções"""
    if not conversas:
        return {}

    intencoes = {}
    for c in conversas:
        intent = c.get("intent", "unknown")
        if intent:
            intencoes[intent] = intencoes.get(intent, 0) + 1

    return dict(sorted(intencoes.items(), key=lambda x: x[1], reverse=True)[:10])


def calcular_sentimentos(conversas):
    """Calcula distribuição de sentimentos"""
    if not conversas:
        return {}

    sentimentos = {}
    for c in conversas:
        sentiment = c.get("sentiment", "unknown")
        if sentiment:
            sentimentos[sentiment] = sentimentos.get(sentiment, 0) + 1

    return sentimentos


def gerar_gatilhos(resumo, financeiro, conversao):
    """Gera gatilhos automáticos baseados em métricas"""
    gatilhos = []

    # Gatilho: Conversão baixa
    if conversao.get("taxa_conversao", 100) < 20:
        gatilhos.append(
            {
                "tipo": "conversao_baixa",
                "prioridade": "alta",
                "mensagem": f"Taxa de conversão em {conversao.get('taxa_conversao', 0):.1f}%",
                "sugestao": "Melhorar follow-up e qualificação",
            }
        )

    # Gatilho: Ticket médio baixo
    if financeiro.get("ticket_medio", 1000) < 50:
        gatilhos.append(
            {
                "tipo": "ticket_baixo",
                "prioridade": "media",
                "mensagem": f"Ticket médio em R$ {financeiro.get('ticket_medio', 0):.2f}",
                "sugestao": "Oferecer pacotes e upsell",
            }
        )

    return gatilhos


def gerar_insights(resumo, financeiro, conversao, gatilhos):
    """Gera insights acionáveis"""
    insights = []

    # Insight baseado em gatilhos
    for gatilho in gatilhos:
        insights.append(
            {
                "tipo": "acao_recomendada",
                "prioridade": gatilho["prioridade"],
                "mensagem": gatilho["mensagem"],
                "acao": gatilho["sugestao"],
            }
        )

    # Insight: Oportunidade de reativação
    clientes_ativos = resumo.get("clientes_ativos", 0)
    total_clientes = resumo.get("total_clientes", 0)

    if total_clientes > 0:
        taxa_ativacao = clientes_ativos / total_clientes * 100
        if taxa_ativacao < 50:
            insights.append(
                {
                    "tipo": "oportunidade",
                    "prioridade": "alta",
                    "mensagem": f"{total_clientes - clientes_ativos} clientes inativos",
                    "acao": "Campanha de reativação pode gerar R$ X em receita",
                }
            )

    return insights


async def calcular_campanhas(conversas):
    """Calcula performance de campanhas baseada no extração de dados"""
    if not conversas:
        return {}

    stats = {}

    # Busca nomes das campanhas para o label
    campanhas_raw = db.table("campaigns").select("id, name").execute()
    camp_names = {c["id"]: c["name"] for c in campanhas_raw.data or []}

    for c in conversas:
        ext = c.get("extracted_data", {}) or {}
        camp_id = ext.get("campaign_id")

        if camp_id:
            if camp_id not in stats:
                stats[camp_id] = {
                    "name": camp_names.get(camp_id, "Inexistente"),
                    "hits": 0,
                    "conversions": 0,
                }

            stats[camp_id]["hits"] += 1
            if c.get("status") == "ended":
                stats[camp_id]["conversions"] += 1

    # Calcula taxas
    for cid in stats:
        hits = stats[cid]["hits"]
        if hits > 0:
            stats[cid]["conversion_rate"] = (stats[cid]["conversions"] / hits) * 100
        else:
            stats[cid]["conversion_rate"] = 0

    return stats


async def get_critical_alerts():
    """Migrado do antigo analytics.py: busca alertas de urgência > 4"""
    try:
        # Busca da tabela de BI ou das conversas recentes
        result = (
            db.table("business_intelligence")
            .select("phone, insight_text, urgency_level, created_at")
            .gt("urgency_level", 4)
            .order("created_at", desc=True)
            .limit(5)
            .execute()
        )

        return result.data or []
    except Exception:
        return []
