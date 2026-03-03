"""
Vector Database Manager - Milvus
Para: Busca semântica de clientes similares, comportamento, churn
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from pymilvus import Collection, connections, FieldSchema, CollectionSchema, DataType

logger = logging.getLogger(__name__)


class VectorDBManager:
    """Gerenciador de banco de dados vetorial"""

    COLLECTION_NAME = "customer_embeddings"
    COLLECTION_NAME_BEHAVIOR = "customer_behavior"

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None):
        self.host = host
        self.port = port
        self.is_connected = False

    def connect(self, host: Optional[str] = None, port: Optional[int] = None):
        """Conectar ao Milvus (Manual ou via Startup)"""
        if host:
            self.host = host
        if port:
            self.port = port

        if not self.host:
            from app.config import settings

            self.host = settings.milvus_host
            self.port = settings.milvus_port

        try:
            connections.connect(alias="default", host=self.host, port=self.port)
            self.is_connected = True
            logger.info(f"✅ Conectado ao Milvus em {self.host}:{self.port}")
            self._init_collections()
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao Milvus: {e}")
            # Não trava a startup, mas loga o erro

    def _init_collections(self):
        """Inicializar coleções"""
        try:
            self._create_customer_collection()
            self._create_behavior_collection()
        except Exception as e:
            logger.warning(f"⚠️ Erro ao inicializar coleções: {e}")

    def _create_customer_collection(self):
        """Criar coleção de embeddings de clientes"""
        fields = [
            FieldSchema(
                name="customer_id",
                dtype=DataType.VARCHAR,
                max_length=100,
                is_primary=True,
            ),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="phone", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="timestamp", dtype=DataType.INT64),
        ]

        schema = CollectionSchema(fields=fields, description="Embeddings de clientes")

        try:
            if not connections.has_connection("default"):
                return

            collection = Collection(name=self.COLLECTION_NAME, schema=schema)
            # Index...
            logger.info(f"Coleção {self.COLLECTION_NAME} verificada")
        except Exception as e:
            logger.debug(f"Coleção {self.COLLECTION_NAME} já existe ou erro: {e}")

    def _create_behavior_collection(self):
        """Criar coleção de padrões de comportamento"""
        fields = [
            FieldSchema(
                name="customer_id",
                dtype=DataType.VARCHAR,
                max_length=100,
                is_primary=True,
            ),
            FieldSchema(name="behavior_vector", dtype=DataType.FLOAT_VECTOR, dim=128),
            FieldSchema(name="churn_score", dtype=DataType.FLOAT),
            FieldSchema(name="loyalty_score", dtype=DataType.FLOAT),
            FieldSchema(name="purchase_frequency", dtype=DataType.FLOAT),
        ]

        schema = CollectionSchema(fields=fields, description="Padrões de comportamento")

        try:
            Collection(name=self.COLLECTION_NAME_BEHAVIOR, schema=schema)
            logger.info(f"Coleção {self.COLLECTION_NAME_BEHAVIOR} verificada")
        except Exception as e:
            logger.debug(f"Coleção {self.COLLECTION_NAME_BEHAVIOR} já existe: {e}")


# Instância global (Lazy)
vector_db_manager = VectorDBManager()
