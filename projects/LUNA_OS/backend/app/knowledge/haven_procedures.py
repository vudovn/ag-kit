"""
Haven Procedure Logic - Física dos Procedimentos

Imported from: docs/luna_os/FISICA_PROCEDIMENTOS.md
Purpose: Real service logistics for intelligent scheduling
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    """Types of salon services"""
    CABELO_ESCOVA = "cabelo_escova"
    CABELO_PROGRESSIVA = "cabelo_progressiva"
    CABELO_COLORACAO = "cabelo_coloracao"
    UNHAS_MAO = "unhas_mao"
    UNHAS_PE = "unhas_pe"
    MAQUIAGEM = "maquagem"
    SOBRANCELHA = "sobrancelha"
    CILIOS = "cilios"


@dataclass
class ServicePhase:
    """Phase of a service procedure"""
    name: str
    duration_min: int
    professional: str
    client_position: str
    can_do_concurrent: List[ServiceType]
    cannot_do_concurrent: List[ServiceType]


@dataclass
class ServiceProcedure:
    """Complete procedure for a service"""
    service_type: ServiceType
    total_duration_min: int
    phases: List[ServicePhase]
    chemical_pause_min: int = 0
    preparation_time_min: int = 0


# ═══════════════════════════════════════════════
# PROCEDURE DATABASE - FÍSICA DOS PROCEDIMENTOS
# ═══════════════════════════════════════════════

PROCEDURE_DATABASE: Dict[ServiceType, ServiceProcedure] = {
    
    # ───────────────────────────────────────────────
    # CABELO - ESCOVA SIMPLES
    # ───────────────────────────────────────────────
    ServiceType.CABELO_ESCOVA: ServiceProcedure(
        service_type=ServiceType.CABELO_ESCOVA,
        total_duration_min=60,
        preparation_time_min=0,
        chemical_pause_min=0,
        phases=[
            ServicePhase(
                name="Lavatório",
                duration_min=20,
                professional="Auxiliar ou Escovista",
                client_position="Deitada, molhada",
                can_do_concurrent=[],
                cannot_do_concurrent=[ServiceType.MAQUIAGEM]
            ),
            ServicePhase(
                name="Secagem + Escova",
                duration_min=40,
                professional="Escovista",
                client_position="Sentada, movimento mínimo",
                can_do_concurrent=[ServiceType.UNHAS_MAO, ServiceType.UNHAS_PE],
                cannot_do_concurrent=[ServiceType.MAQUIAGEM]
            )
        ]
    ),
    
    # ───────────────────────────────────────────────
    # CABELO - PROGRESSIVA (QUÍMICA COMPLEXA)
    # ───────────────────────────────────────────────
    ServiceType.CABELO_PROGRESSIVA: ServiceProcedure(
        service_type=ServiceType.CABELO_PROGRESSIVA,
        total_duration_min=240,  # 3-4 hours
        preparation_time_min=0,
        chemical_pause_min=90,  # 40-90 min product action
        phases=[
            ServicePhase(
                name="Lavatório com Antirresíduo",
                duration_min=20,
                professional="Auxiliar",
                client_position="Deitada",
                can_do_concurrent=[],
                cannot_do_concurrent=[]
            ),
            ServicePhase(
                name="Pausa Química (Produto Agindo)",
                duration_min=90,
                professional="Aguardando",
                client_position="Sentada, produto no cabelo",
                can_do_concurrent=[
                    ServiceType.UNHAS_MAO,
                    ServiceType.UNHAS_PE,
                    ServiceType.SOBRANCELHA
                ],
                cannot_do_concurrent=[ServiceType.MAQUIAGEM]
            ),
            ServicePhase(
                name="Enxágue + Secagem",
                duration_min=30,
                professional="Auxiliar + Escovista",
                client_position="Sentada",
                can_do_concurrent=[],
                cannot_do_concurrent=[]
            ),
            ServicePhase(
                name="Prancha + Finalização",
                duration_min=60,
                professional="Escovista",
                client_position="Sentada, imóvel",
                can_do_concurrent=[],
                cannot_do_concurrent=[ServiceType.MAQUIAGEM, ServiceType.SOBRANCELHA]
            )
        ]
    ),
    
    # ───────────────────────────────────────────────
    # CABELO - COLORAÇÃO
    # ───────────────────────────────────────────────
    ServiceType.CABELO_COLORACAO: ServiceProcedure(
        service_type=ServiceType.CABELO_COLORACAO,
        total_duration_min=180,  # 2-3 hours
        preparation_time_min=0,
        chemical_pause_min=45,  # Color processing time
        phases=[
            ServicePhase(
                name="Aplicação da Coloração",
                duration_min=30,
                professional="Colorista",
                client_position="Sentada",
                can_do_concurrent=[],
                cannot_do_concurrent=[]
            ),
            ServicePhase(
                name="Pausa Química (Cor Agindo)",
                duration_min=45,
                professional="Aguardando",
                client_position="Sentada, produto no cabelo",
                can_do_concurrent=[
                    ServiceType.UNHAS_MAO,
                    ServiceType.UNHAS_PE
                ],
                cannot_do_concurrent=[ServiceType.MAQUIAGEM]
            ),
            ServicePhase(
                name="Enxágue + Secagem + Finalização",
                duration_min=60,
                professional="Auxiliar + Colorista",
                client_position="Sentada",
                can_do_concurrent=[],
                cannot_do_concurrent=[]
            )
        ]
    ),
    
    # ───────────────────────────────────────────────
    # UNHAS - MÃOS
    # ───────────────────────────────────────────────
    ServiceType.UNHAS_MAO: ServiceProcedure(
        service_type=ServiceType.UNHAS_MAO,
        total_duration_min=40,
        preparation_time_min=0,
        chemical_pause_min=0,
        phases=[
            ServicePhase(
                name="Preparação + Esmaltação",
                duration_min=40,
                professional="Manicure",
                client_position="Sentada, mãos imóveis",
                can_do_concurrent=[
                    ServiceType.CABELO_ESCOVA,
                    ServiceType.CABELO_PROGRESSIVA,
                    ServiceType.CABELO_COLORACAO
                ],
                cannot_do_concurrent=[]
            )
        ]
    ),
    
    # ───────────────────────────────────────────────
    # UNHAS - PÉS
    # ───────────────────────────────────────────────
    ServiceType.UNHAS_PE: ServiceProcedure(
        service_type=ServiceType.UNHAS_PE,
        total_duration_min=30,
        preparation_time_min=0,
        chemical_pause_min=0,
        phases=[
            ServicePhase(
                name="Preparação + Esmaltação",
                duration_min=30,
                professional="Pedicure",
                client_position="Sentada, pés imóveis",
                can_do_concurrent=[
                    ServiceType.CABELO_ESCOVA,
                    ServiceType.CABELO_PROGRESSIVA,
                    ServiceType.CABELO_COLORACAO,
                    ServiceType.UNHAS_MAO
                ],
                cannot_do_concurrent=[]
            )
        ]
    ),
    
    # ───────────────────────────────────────────────
    # MAQUIAGEM
    # ───────────────────────────────────────────────
    ServiceType.MAQUIAGEM: ServiceProcedure(
        service_type=ServiceType.MAQUIAGEM,
        total_duration_min=60,
        preparation_time_min=0,
        chemical_pause_min=0,
        phases=[
            ServicePhase(
                name="Preparação da Pele",
                duration_min=15,
                professional="Maquiadora",
                client_position="Sentada, imóvel",
                can_do_concurrent=[],
                cannot_do_concurrent=[
                    ServiceType.CABELO_ESCOVA,
                    ServiceType.CABELO_PROGRESSIVA
                ]
            ),
            ServicePhase(
                name="Aplicação da Maquiagem",
                duration_min=45,
                professional="Maquiadora",
                client_position="Sentada, imóvel",
                can_do_concurrent=[],
                cannot_do_concurrent=[
                    ServiceType.CABELO_ESCOVA,
                    ServiceType.CABELO_PROGRESSIVA
                ]
            )
        ]
    ),
}


# ═══════════════════════════════════════════════
# SCHEDULING LOGIC
# ═══════════════════════════════════════════════

def get_service_procedure(service_type: ServiceType) -> Optional[ServiceProcedure]:
    """Get complete procedure for a service"""
    return PROCEDURE_DATABASE.get(service_type)


def can_combine_services(
    primary: ServiceType,
    secondary: ServiceType
) -> bool:
    """
    Check if two services can be done concurrently.
    
    Returns True if services can be combined, False otherwise.
    """
    primary_proc = get_service_procedure(primary)
    if not primary_proc:
        return False
    
    # Check each phase of primary service
    for phase in primary_proc.phases:
        # If secondary is in cannot_do_concurrent, return False
        if secondary in phase.cannot_do_concurrent:
            return False
    
    # If we find a phase where secondary is allowed, return True
    for phase in primary_proc.phases:
        if secondary in phase.can_do_concurrent:
            return True
    
    # Default: cannot combine
    return False


def calculate_total_duration(services: List[ServiceType]) -> int:
    """
    Calculate total duration for multiple services.
    Considers concurrent services during chemical pause.
    """
    if not services:
        return 0
    
    # Get primary service (longest)
    primary = max(services, key=lambda s: get_service_procedure(s).total_duration_min if get_service_procedure(s) else 0)
    primary_proc = get_service_procedure(primary)
    
    if len(services) == 1:
        return primary_proc.total_duration_min
    
    # Calculate with concurrency
    total = primary_proc.total_duration_min
    
    # Add secondary services that don't overlap
    for secondary in services:
        if secondary != primary and not can_combine_services(primary, secondary):
            secondary_proc = get_service_procedure(secondary)
            total += secondary_proc.total_duration_min
    
    return total


def get_optimal_scheduling(
    services: List[ServiceType]
) -> Dict:
    """
    Get optimal scheduling for multiple services.
    
    Returns:
        Dict with:
        - total_duration: Total time in minutes
        - concurrent_services: List of services that can be done together
        - sequence: Optimal sequence of services
    """
    if not services:
        return {"total_duration": 0, "concurrent_services": [], "sequence": []}
    
    # Find primary service
    primary = max(
        services,
        key=lambda s: get_service_procedure(s).total_duration_min if get_service_procedure(s) else 0
    )
    
    # Find concurrent services
    concurrent = [
        s for s in services
        if s != primary and can_combine_services(primary, s)
    ]
    
    # Find sequential services
    sequential = [
        s for s in services
        if s != primary and not can_combine_services(primary, s)
    ]
    
    total_duration = calculate_total_duration(services)
    
    return {
        "total_duration": total_duration,
        "concurrent_services": concurrent,
        "sequence": [primary] + sequential,
        "can_combine": len(concurrent) > 0
    }


# ═══════════════════════════════════════════════
# LUNA INTEGRATION
# ═══════════════════════════════════════════════

def get_scheduling_advice(services: List[str]) -> str:
    """
    Get natural language scheduling advice for LUNA.
    
    Args:
        services: List of service names (e.g., ["progressiva", "unhas"])
    
    Returns:
        Natural language advice string
    """
    # Map service names to enum
    service_map = {
        "escova": ServiceType.CABELO_ESCOVA,
        "progressiva": ServiceType.CABELO_PROGRESSIVA,
        "coloracao": ServiceType.CABELO_COLORACAO,
        "unhas": ServiceType.UNHAS_MAO,
        "unhas_mao": ServiceType.UNHAS_MAO,
        "unhas_pe": ServiceType.UNHAS_PE,
        "manicure": ServiceType.UNHAS_MAO,
        "pedicure": ServiceType.UNHAS_PE,
        "maquiagem": ServiceType.MAQUIAGEM,
    }
    
    service_types = [service_map.get(s.lower()) for s in services]
    service_types = [s for s in service_types if s is not None]
    
    if not service_types:
        return "Não foi possível identificar os serviços. Por favor, especifique melhor."
    
    scheduling = get_optimal_scheduling(service_types)
    
    # Generate advice
    if scheduling["can_combine"]:
        concurrent_names = [s.value.replace("_", " ") for s in scheduling["concurrent_services"]]
        advice = (
            f"✅ Ótima notícia! Enquanto fazemos {scheduling['sequence'][0].value.replace('_', ' ')}, "
            f"podemos fazer também {', '.join(concurrent_names)}. "
            f"Tempo total: {scheduling['total_duration']} minutos."
        )
    else:
        advice = (
            f"⏰ Para esses serviços, recomendamos {scheduling['total_duration']} minutos. "
            f"Sequência: {' → '.join([s.value.replace('_', ' ') for s in scheduling['sequence']])}."
        )
    
    return advice
