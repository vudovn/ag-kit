"""
Previsão de Churn e Clustering de Clientes
Usa: SKlearn, XGBoost, Milvus
"""

import logging
import pickle
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
    """Preditor de churn com ML"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=128)
        
        if model_path:
            self.load_model(model_path)
        else:
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
        logger.info("Modelo XGBoost inicializado")
    
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
        logger.info(f"Modelo treinado com {len(labels)} exemplos")
    
    def save_model(self, path: str):
        """Salvar modelo treinado"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler
            }, f)
        logger.info(f"Modelo salvo em {path}")
    
    def load_model(self, path: str):
        """Carregar modelo treinado"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
        logger.info(f"Modelo carregado de {path}")


# Instância global
churn_predictor = ChurnPredictor()