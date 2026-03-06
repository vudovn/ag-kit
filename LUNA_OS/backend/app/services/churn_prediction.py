"""
Previsão de Churn e Clustering de Clientes (com Persistência)
Usa: SKlearn, XGBoost, Milvus, Supabase Storage

DEBT #7: Modelo agora é persistido automaticamente no Supabase Storage.
"""

import logging
import pickle
import io
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Preditor de churn com ML e persistência"""

    MODEL_PATH_DEFAULT = "/tmp/churn_model.pkl"
    STORAGE_PATH_DEFAULT = "models/churn_model.pkl"

    def __init__(self, model_path: Optional[str] = None, use_supabase_storage: bool = True):
        self.model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=128)
        self.use_supabase_storage = use_supabase_storage
        self._model_version: Optional[str] = None

        # Tentar carregar modelo persistido
        if model_path:
            self.load_model(model_path)
        elif use_supabase_storage:
            self._try_load_from_supabase()
        else:
            self._init_model()

    def _try_load_from_supabase(self):
        """Tenta carregar modelo do Supabase Storage"""
        try:
            from app.integrations.supabase_client import get_supabase
            
            supabase = get_supabase()
            if supabase is None:
                logger.warning("Supabase não disponível, inicializando modelo vazio")
                self._init_model()
                return
            
            # Buscar metadados do modelo mais recente
            result = (
                supabase.table("ml_models")
                .select("id, version, storage_path, created_at")
                .eq("model_type", "churn_prediction")
                .eq("status", "active")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            
            if result.data and len(result.data) > 0:
                model_info = result.data[0]
                storage_path = model_info.get("storage_path", self.STORAGE_PATH_DEFAULT)
                self._model_version = model_info.get("version", "unknown")
                
                logger.info(f"Carregando modelo de churn: {storage_path} (v{self._model_version})")
                self._load_from_storage(supabase, storage_path)
            else:
                logger.info("Nenhum modelo de churn encontrado, inicializando novo")
                self._init_model()
                
        except Exception as e:
            logger.warning(f"Falha ao carregar modelo do Supabase: {e}, usando modelo vazio")
            self._init_model()

    def _load_from_storage(self, supabase, storage_path: str):
        """Carrega modelo do Supabase Storage"""
        try:
            # Download do arquivo
            response = supabase.storage.from_("models").download(storage_path)
            
            if response:
                data = pickle.loads(response)
                self.model = data['model']
                self.scaler = data['scaler']
                logger.info(f"✅ Modelo de churn carregado do storage: {storage_path}")
            else:
                logger.warning("Arquivo do modelo não encontrado no storage")
                self._init_model()
        except Exception as e:
            logger.error(f"Erro ao baixar modelo: {e}")
            self._init_model()

    def _init_model(self):
        """Inicializar modelo XGBoost"""
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            scale_pos_weight=3  # Desbalanceamento (menos churn)
        )
        self._model_version = "untrained"
        logger.info("Modelo XGBoost inicializado (não treinado)")

    def extract_features(self, customer_data: Dict) -> np.ndarray:
        """Extrair features para previsão"""
        features = []

        # Features de compra
        last_purchase_days = customer_data.get("last_purchase_days", 999)
        purchase_frequency = customer_data.get("purchase_frequency", 0)
        total_spent = customer_data.get("total_spent", 0)
        avg_ticket = customer_data.get("avg_ticket", 0)

        # Features de comunicação
        messages_count = customer_data.get("messages_count", 0)
        response_time_avg = customer_data.get("response_time_avg", 999)
        engagement_score = customer_data.get("engagement_score", 0)

        # Features de produto
        service_variety = customer_data.get("service_variety", 0)
        repeat_rate = customer_data.get("repeat_rate", 0)

        # Features temporais
        customer_age_days = customer_data.get("customer_age_days", 1)
        messages_in_last_30d = customer_data.get("messages_in_last_30d", 0)

        # Features de emoção/satisfação
        avg_sentiment = customer_data.get("avg_sentiment", 0.5)
        complaint_count = customer_data.get("complaint_count", 0)
        satisfaction_score = customer_data.get("satisfaction_score", 5)

        features = [
            # Recência, Frequência, Monetário
            min(last_purchase_days, 365),
            purchase_frequency,
            total_spent,
            avg_ticket,

            # Comunicação
            messages_count,
            min(response_time_avg, 86400),  # Cap em 24h
            engagement_score,
            messages_in_last_30d,

            # Comportamento
            service_variety,
            repeat_rate,
            customer_age_days,

            # Sentimento
            avg_sentiment,
            complaint_count,
            satisfaction_score,

            # Derived
            purchase_frequency / max(customer_age_days, 1),  # Compras por dia
            messages_count / max(customer_age_days, 1),  # Engajamento por dia
            total_spent / max(purchase_frequency, 1),  # Valor médio
        ]

        return np.array(features).reshape(1, -1)

    def predict_churn_score(self, customer_data: Dict) -> Tuple[float, List[str]]:
        """Prever score de churn (0-1) e ações"""
        if self.model is None:
            logger.warning("Modelo não treinado, usando heurística")
            return self._heuristic_churn(customer_data), []

        # Extrair features
        features = self.extract_features(customer_data)

        # Normalizar
        features_scaled = self.scaler.transform(features)

        # Prever
        churn_prob = self.model.predict_proba(features_scaled)[0][1]

        # Gerar recomendações
        actions = self._recommend_actions(customer_data, churn_prob)

        return float(churn_prob), actions

    def _heuristic_churn(self, customer_data: Dict) -> float:
        """Heurística para churn quando modelo não está treinado"""
        last_purchase_days = customer_data.get("last_purchase_days", 30)
        messages_count = customer_data.get("messages_count", 0)
        satisfaction = customer_data.get("satisfaction_score", 5)

        # Fórmula simples
        score = 0.0

        if last_purchase_days > 180:
            score += 0.5
        elif last_purchase_days > 90:
            score += 0.3
        elif last_purchase_days > 30:
            score += 0.1

        if messages_count < 5:
            score += 0.2

        score = max(0, min(1, score - (satisfaction - 3) * 0.1))

        return score

    def _recommend_actions(self, customer_data: Dict, churn_prob: float) -> List[str]:
        """Recomendar ações para reter cliente"""
        actions = []

        if churn_prob > 0.8:
            actions.append("send_retention_offer")
            actions.append("call_customer")
            actions.append("assign_to_manager")
        elif churn_prob > 0.6:
            actions.append("send_personalized_offer")
            actions.append("increase_engagement")
        elif churn_prob > 0.4:
            actions.append("send_reminder")
            actions.append("suggest_new_service")

        return actions

    def train(self, training_data: pd.DataFrame, labels: np.ndarray):
        """Treinar modelo com dados históricos"""
        features_list = []

        for _, row in training_data.iterrows():
            features = self.extract_features(row.to_dict())
            features_list.append(features[0])

        X = np.array(features_list)
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, labels)
        self._model_version = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        logger.info(f"✅ Modelo treinado com {len(labels)} exemplos (v{self._model_version})")

    def save_model(self, path: str):
        """Salvar modelo treinado (local)"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'version': self._model_version
            }, f)
        logger.info(f"Modelo salvo em {path}")

    def load_model(self, path: str):
        """Carregar modelo treinado (local)"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self._model_version = data.get('version', 'unknown')
        logger.info(f"✅ Modelo carregado de {path} (v{self._model_version})")

    async def save_to_supabase(self, supabase=None) -> bool:
        """
        Salvar modelo treinado no Supabase Storage.
        Retorna True se sucesso, False se falha.
        """
        if self.model is None:
            logger.warning("Não há modelo treinado para salvar")
            return False

        try:
            if supabase is None:
                from app.integrations.supabase_client import get_supabase
                supabase = get_supabase()
            
            if supabase is None:
                logger.error("Supabase não disponível")
                return False

            # Serializar modelo
            model_data = pickle.dumps({
                'model': self.model,
                'scaler': self.scaler,
                'version': self._model_version or datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            })

            # Upload para storage
            storage_path = f"churn/{self._model_version or 'latest'}.pkl"
            
            supabase.storage.from_("models").upload(
                storage_path,
                io.BytesIO(model_data),
                {"content-type": "application/octet-stream"}
            )

            # Registrar metadados no banco
            supabase.table("ml_models").insert({
                "model_type": "churn_prediction",
                "version": self._model_version,
                "storage_path": storage_path,
                "status": "active",
                "metrics": {
                    "training_samples": len(self.scaler.mean_) if hasattr(self.scaler, 'mean_') else 0
                }
            }).execute()

            logger.info(f"✅ Modelo salvo no Supabase Storage: {storage_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao salvar modelo no Supabase: {e}")
            return False

    def get_model_info(self) -> Dict:
        """Retorna informações do modelo atual"""
        return {
            "version": self._model_version,
            "is_trained": self.model is not None,
            "scaler_fitted": hasattr(self.scaler, 'mean_'),
            "storage_enabled": self.use_supabase_storage
        }


# Instância global
churn_predictor = ChurnPredictor()
