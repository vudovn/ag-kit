import asyncio
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.integrations.evolution import evolution
from loguru import logger


async def test_conn():
    logger.info("🧪 Testando conectividade com Evolution API...")
    try:
        status = await evolution.get_instance_status()
        logger.info(f"✅ Status: {status}")
    except Exception as e:
        logger.error(f"❌ Falha de conexão: {e}")


if __name__ == "__main__":
    asyncio.run(test_conn())
