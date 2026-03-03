"""
Evolution API Proxy - Espelha todos os endpoints da Evolution API
"""

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import httpx

from app.config import settings
from app.core.evolution import EvolutionEngine
from loguru import logger

router = APIRouter(prefix="/api/evolution", tags=["Evolution Proxy"])
engine = EvolutionEngine()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request, path: str):
    """
    Proxy reverso para Evolution API
    Espelha todos os endpoints
    """
    try:
        # Build URL
        url = f"{settings.evolution_url}/{path}"

        # Get headers (exclude host)
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in ["host", "content-length"]
        }
        headers["apikey"] = settings.evolution_key

        # Get body
        body = await request.body()

        # Forward request
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params,
            )

            # Return response
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.content else {},
            )

    except httpx.ConnectError as e:
        raise HTTPException(
            status_code=503, detail=f"Evolution API unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/maturity")
async def get_maturity():
    """
    Retorna o Score de Maturidade da LUNA.
    """
    try:
        maturity = await engine.calculate_maturity_score()
        return maturity
    except Exception as e:
        logger.error(f"Error in maturity endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
