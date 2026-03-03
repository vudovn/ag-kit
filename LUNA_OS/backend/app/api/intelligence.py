"""
🧠 Conversation Intelligence Endpoints

Endpoints para acesso à inteligência de conversas.

Endpoints:
- GET  /api/intelligence/{conversation_id} → Análise de uma conversa
- GET  /api/intelligence/client/{phone}    → Inteligência de um cliente
- GET  /api/intelligence/insights          → Insights agregados

Autor: MCT Agent Flow
Data: 2026-03-01
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/intelligence", tags=["Conversation Intelligence"])


@router.get("/{conversation_id}")
async def get_conversation_intelligence(conversation_id: str):
    """
    Retorna análise completa de uma conversa específica.
    
    - **conversation_id**: ID da conversa no Supabase
    """
    try:
        from app.integrations.supabase_client import get_supabase
        supabase = get_supabase()
        
        # Buscar inteligência da conversa
        result = supabase.table("conversation_intelligence") \
            .select("*") \
            .eq("conversation_id", conversation_id) \
            .order("processed_at", desc=True) \
            .limit(1) \
            .execute()
        
        if not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"No intelligence found for conversation {conversation_id}"
            )
        
        intelligence = result.data[0]
        
        # Buscar dados da conversa original
        conv_result = supabase.table("conversations") \
            .select("id, phone, status, intent, sentiment, messages_count, started_at, ended_at") \
            .eq("id", conversation_id) \
            .execute()
        
        conversation = conv_result.data[0] if conv_result.data else None
        
        return {
            "success": True,
            "conversation": conversation,
            "intelligence": intelligence
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/client/{phone}")
async def get_client_intelligence(phone: str):
    """
    Retorna inteligência consolidada de um cliente.
    
    - **phone**: Telefone do cliente
    """
    try:
        from app.integrations.supabase_client import get_supabase
        supabase = get_supabase()
        
        # Buscar cliente
        client_result = supabase.table("clients") \
            .select("*") \
            .eq("phone", phone) \
            .limit(1) \
            .execute()
        
        if not client_result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Client {phone} not found"
            )
        
        client = client_result.data[0]
        
        # Buscar todas as inteligências de conversas deste cliente
        intelligence_result = supabase.table("conversation_intelligence") \
            .select("*") \
            .eq("client_id", client["id"]) \
            .order("processed_at", desc=True) \
            .limit(50) \
            .execute()
        
        intelligences = intelligence_result.data or []
        
        # Consolidar dados
        consolidated = _consolidate_client_intelligence(client, intelligences)
        
        return {
            "success": True,
            "client": client,
            "intelligence": consolidated,
            "recent_analyses": intelligences[:10]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_business_insights(
    days: int = Query(30, description="Days to analyze"),
    group_by: str = Query("day", description="Group by: day, week, emotional_state, trust_level")
):
    """
    Retorna insights do negócio agregados.
    
    - **days**: Quantos dias analisar
    - **group_by**: Como agrupar dados
    """
    try:
        from app.integrations.supabase_client import get_supabase
        supabase = get_supabase()
        
        # Calcular data inicial
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Buscar inteligências do período
        result = supabase.table("conversation_intelligence") \
            .select("*") \
            .gte("processed_at", start_date.isoformat()) \
            .execute()
        
        intelligences = result.data or []
        
        if not intelligences:
            return {
                "success": True,
                "period_days": days,
                "total_analyses": 0,
                "insights": []
            }
        
        # Agrupar e consolidar
        insights = _aggregate_insights(intelligences, group_by)
        
        # Calcular métricas de negócio
        metrics = _calculate_business_metrics(intelligences)
        
        return {
            "success": True,
            "period_days": days,
            "total_analyses": len(intelligences),
            "insights": insights,
            "metrics": metrics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _consolidate_client_intelligence(
    client: Dict[str, Any],
    intelligences: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Consolida inteligência de múltiplas conversas de um cliente.
    """
    if not intelligences:
        return {
            "total_conversations": 0,
            "emotional_states": [],
            "trust_level": client.get("preferences", {}).get("trust_level", "new"),
            "opportunities": [],
            "objections": []
        }
    
    # Contar estados emocionais
    emotional_states = {}
    for intel in intelligences:
        state = intel.get("emotional_state", "neutral")
        emotional_states[state] = emotional_states.get(state, 0) + 1
    
    # Consolidar oportunidades
    all_opportunities = []
    for intel in intelligences:
        opps = intel.get("upsell_opportunities", [])
        all_opportunities.extend(opps)
    
    # Consolidar objeções
    all_objections = []
    for intel in intelligences:
        objs = intel.get("objections_raised", [])
        all_objections.extend(objs)
    
    # Calcular trust level médio
    trust_scores = {"new": 1, "building": 2, "established": 3, "loyal": 4}
    avg_trust = sum(
        trust_scores.get(intel.get("trust_level", "new"), 1)
        for intel in intelligences
    ) / len(intelligences)
    
    trust_level = "new"
    if avg_trust >= 3.5:
        trust_level = "loyal"
    elif avg_trust >= 2.5:
        trust_level = "established"
    elif avg_trust >= 1.5:
        trust_level = "building"
    
    return {
        "total_conversations": len(intelligences),
        "emotional_states": emotional_states,
        "dominant_emotional_state": max(emotional_states, key=emotional_states.get) if emotional_states else "neutral",
        "trust_level": trust_level,
        "opportunities": list(set(all_opportunities)),
        "objections": list(set(all_objections)),
        "last_processed_at": intelligences[0].get("processed_at")
    }


def _aggregate_insights(
    intelligences: List[Dict[str, Any]],
    group_by: str
) -> List[Dict[str, Any]]:
    """
    Agrega insights por grupo.
    """
    from collections import defaultdict
    
    grouped = defaultdict(lambda: {
        "count": 0,
        "emotional_states": defaultdict(int),
        "conversion_likelihood": defaultdict(int),
        "opportunities": [],
        "objections": []
    })
    
    for intel in intelligences:
        # Determinar chave de grupo
        if group_by == "day":
            key = intel.get("processed_at", "")[:10]  # YYYY-MM-DD
        elif group_by == "week":
            key = intel.get("processed_at", "")[:7]   # YYYY-MM
        elif group_by == "emotional_state":
            key = intel.get("emotional_state", "neutral")
        elif group_by == "trust_level":
            key = intel.get("trust_level", "new")
        else:
            key = "all"
        
        # Agregar dados
        grouped[key]["count"] += 1
        grouped[key]["emotional_states"][intel.get("emotional_state", "neutral")] += 1
        grouped[key]["conversion_likelihood"][intel.get("conversion_likelihood", "medium")] += 1
        
        opps = intel.get("upsell_opportunities", [])
        grouped[key]["opportunities"].extend(opps)
        
        objs = intel.get("objections_raised", [])
        grouped[key]["objections"].extend(objs)
    
    # Converter para lista
    insights = []
    for key, data in grouped.items():
        insights.append({
            "group": key,
            "count": data["count"],
            "dominant_emotion": max(data["emotional_states"], key=data["emotional_states"].get) if data["emotional_states"] else "neutral",
            "dominant_conversion": max(data["conversion_likelihood"], key=data["conversion_likelihood"].get) if data["conversion_likelihood"] else "medium",
            "unique_opportunities": len(set(data["opportunities"])),
            "unique_objections": len(set(data["objections"]))
        })
    
    # Ordenar por count
    insights.sort(key=lambda x: x["count"], reverse=True)
    
    return insights


def _calculate_business_metrics(
    intelligences: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calcula métricas de negócio a partir das inteligências.
    """
    if not intelligences:
        return {}
    
    # Contar por estado emocional
    emotional_distribution = {}
    for intel in intelligences:
        state = intel.get("emotional_state", "neutral")
        emotional_distribution[state] = emotional_distribution.get(state, 0) + 1
    
    # Contar por trust level
    trust_distribution = {}
    for intel in intelligences:
        level = intel.get("trust_level", "new")
        trust_distribution[level] = trust_distribution.get(level, 0) + 1
    
    # Contar por conversão
    conversion_distribution = {}
    for intel in intelligences:
        likelihood = intel.get("conversion_likelihood", "medium")
        conversion_distribution[likelihood] = conversion_distribution.get(likelihood, 0) + 1
    
    # Calcular score médio de conversão
    conversion_scores = {"low": 1, "medium": 2, "high": 3}
    avg_conversion = sum(
        conversion_scores.get(intel.get("conversion_likelihood", "medium"), 2)
        for intel in intelligences
    ) / len(intelligences)
    
    # Top objeções
    all_objections = []
    for intel in intelligences:
        all_objections.extend(intel.get("objections_raised", []))
    
    objection_counts = {}
    for obj in all_objections:
        objection_counts[obj] = objection_counts.get(obj, 0) + 1
    
    top_objections = sorted(objection_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Top oportunidades
    all_opportunities = []
    for intel in intelligences:
        all_opportunities.extend(intel.get("upsell_opportunities", []))
    
    opportunity_counts = {}
    for opp in all_opportunities:
        opportunity_counts[opp] = opportunity_counts.get(opp, 0) + 1
    
    top_opportunities = sorted(opportunity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_conversations": len(intelligences),
        "emotional_distribution": emotional_distribution,
        "trust_distribution": trust_distribution,
        "conversion_distribution": conversion_distribution,
        "avg_conversion_score": round(avg_conversion, 2),
        "top_objections": top_objections,
        "top_opportunities": top_opportunities,
        "health_score": round(
            (avg_conversion / 3) * 100,
            1
        )  # Score de 0-100 baseado na conversão média
    }
