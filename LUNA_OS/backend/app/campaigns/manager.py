"""
Campaign Manager
"""
from datetime import datetime, date
from typing import List, Optional, Dict
from app.integrations.supabase_client import get_supabase

class CampaignManager:
    def __init__(self):
        self.supabase = None
    
    def _get_db(self):
        if self.supabase is None:
            self.supabase = get_supabase()
        return self.supabase
    
    async def create_campaign(self, data: Dict) -> Dict:
        """Create new campaign"""
        db = self._get_db()
        campaign = {
            "name": data["name"],
            "type": data["type"],  # seasonal, followup, reactivation
            "status": "draft",
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "discount_percent": data.get("discount_percent"),
            "discount_fixed": data.get("discount_fixed"),
            "services": data.get("services", []),
            "trigger_keywords": data.get("trigger_keywords", []),
            "message_template": data.get("message_template"),
            "target_segment": data.get("target_segment", "all"),
            "stats": {"sent": 0, "opened": 0, "converted": 0},
            "created_at": datetime.utcnow().isoformat()
        }
        result = db.table("campaigns").insert(campaign).execute()
        return result.data[0] if result.data else campaign
    
    async def get_active_campaigns(self) -> List[Dict]:
        """Get all active campaigns"""
        db = self._get_db()
        today = date.today().isoformat()
        
        result = db.table("campaigns")\
            .select("*")\
            .eq("status", "active")\
            .lte("start_date", today)\
            .gte("end_date", today)\
            .execute()
        
        return result.data or []
    
    async def check_campaign_trigger(self, message: str, client: Dict) -> Optional[Dict]:
        """Check if message triggers any campaign"""
        campaigns = await self.get_active_campaigns()
        msg_lower = message.lower()
        
        for campaign in campaigns:
            keywords = campaign.get("trigger_keywords", [])
            if any(kw.lower() in msg_lower for kw in keywords):
                # Check target segment
                segment = campaign.get("target_segment", "all")
                if segment == "all":
                    return campaign
                elif segment == "vip" and "vip" in (client.get("tags") or []):
                    return campaign
                elif segment == "new" and client.get("total_visits", 0) == 0:
                    return campaign
        
        return None
    
    async def update_campaign_stats(self, campaign_id: str, stat: str):
        """Update campaign statistics"""
        db = self._get_db()
        campaign = db.table("campaigns").select("stats").eq("id", campaign_id).execute()
        
        if campaign.data:
            stats = campaign.data[0].get("stats", {})
            stats[stat] = stats.get(stat, 0) + 1
            db.table("campaigns").update({"stats": stats}).eq("id", campaign_id).execute()

campaign_manager = CampaignManager()
