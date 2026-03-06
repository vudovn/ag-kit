"""
Knowledge Base Loader
"""
import json
import os
from typing import List, Dict, Optional
from loguru import logger

class KnowledgeBase:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data")
        self.services = []
        self.professionals = []
        self.rules = {}
        self.faq = []
        self.packages = {}
        self.coupons = []
        self.business = {}
        self._load()

    def _load(self):
        """Load all knowledge files"""
        try:
            with open(os.path.join(self.data_path, "haven.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.services = data.get("services", [])
                self.professionals = data.get("professionals", [])
                self.rules = data.get("rules", {})
                self.faq = data.get("faq", [])
                self.packages = data.get("packages", {})
                self.coupons = data.get("coupons", [])
                self.business = data.get("business", {})
            # [DEBT #M1] Substituir print() por logger
            logger.info(f"✅ Knowledge Base loaded: {len(self.services)} services, {len(self.professionals)} professionals")
        except Exception as e:
            # [DEBT #M1] Substituir print() por logger
            logger.error(f"⚠️ Knowledge Base load error: {e}")
    
    def search_services(self, query: str) -> List[dict]:
        """Search services by query"""
        query_lower = query.lower()
        results = []
        
        for service in self.services:
            name = service.get("name", "").lower()
            category = service.get("category", "").lower()
            keywords = service.get("keywords", [])
            
            if query_lower in name or query_lower in category:
                results.append(service)
            elif any(kw in query_lower for kw in keywords):
                results.append(service)
        
        return results
    
    def search_professionals(self, query: str) -> List[dict]:
        """Search professionals by query"""
        query_lower = query.lower()
        results = []
        
        for prof in self.professionals:
            name = prof.get("name", "").lower()
            nickname = prof.get("nickname", "").lower()
            
            if query_lower in name or query_lower in nickname:
                results.append(prof)
        
        return results
    
    def search_faq(self, query: str) -> Optional[dict]:
        """Find matching FAQ"""
        query_lower = query.lower()
        
        for faq_item in self.faq:
            patterns = faq_item.get("patterns", [])
            if any(p.lower() in query_lower for p in patterns):
                return faq_item
        
        return None
    
    def find_coupon(self, text: str) -> Optional[dict]:
        """Find coupon in text"""
        text_upper = text.upper()
        
        for coupon in self.coupons:
            if coupon.get("code", "").upper() in text_upper:
                return coupon
        
        return None
    
    def get_packages(self) -> dict:
        """Get all packages"""
        return self.packages
    
    def get_service_by_id(self, service_id: str) -> Optional[dict]:
        """Get service by ID"""
        for service in self.services:
            if service.get("id") == service_id:
                return service
        return None
    
    def get_professional_by_id(self, prof_id: str) -> Optional[dict]:
        """Get professional by ID"""
        for prof in self.professionals:
            if prof.get("id") == prof_id:
                return prof
        return None
