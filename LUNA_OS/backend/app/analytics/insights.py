"""
Analytics - Insights Engine
"""

from datetime import datetime, timedelta
from typing import Dict, List
from dateutil.parser import isoparse
from app.integrations.supabase_client import get_supabase


class InsightsEngine:
    def __init__(self):
        self.supabase = None

    def _get_db(self):
        if self.supabase is None:
            self.supabase = get_supabase()
        return self.supabase

    async def get_dashboard_metrics(self, days: int = 7) -> Dict:
        """Get main dashboard metrics"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        # Conversations
        conversations = (
            db.table("conversations")
            .select("status, conversion_result, intent")
            .gte("started_at", since)
            .execute()
        )

        total = len(conversations.data or [])
        converted = len(
            [
                c
                for c in (conversations.data or [])
                if c.get("conversion_result") == "agendado"
            ]
        )
        abandoned = len(
            [c for c in (conversations.data or []) if c.get("status") == "abandoned"]
        )
        handoffs = len(
            [c for c in (conversations.data or []) if c.get("status") == "handed_off"]
        )

        conversion_rate = (converted / total * 100) if total > 0 else 0

        # Messages
        messages = (
            db.table("messages")
            .select("direction, response_time_ms")
            .gte("created_at", since)
            .execute()
        )

        total_messages = len(messages.data or [])
        response_times = [
            m["response_time_ms"]
            for m in (messages.data or [])
            if m.get("response_time_ms")
        ]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )

        # Appointments
        appointments = (
            db.table("appointments")
            .select("status, service_name")
            .gte("created_at", since)
            .execute()
        )

        return {
            "period_days": days,
            "conversations": {
                "total": total,
                "converted": converted,
                "abandoned": abandoned,
                "handoffs": handoffs,
                "conversion_rate": round(conversion_rate, 1),
            },
            "messages": {
                "total": total_messages,
                "avg_response_time_ms": round(avg_response_time, 0),
            },
            "appointments": {
                "total": len(appointments.data or []),
                "completed": len(
                    [
                        a
                        for a in (appointments.data or [])
                        if a.get("status") == "completed"
                    ]
                ),
            },
        }

    async def get_hourly_distribution(self, days: int = 30) -> List[Dict]:
        """Get message distribution by hour"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        messages = (
            db.table("messages")
            .select("created_at")
            .eq("direction", "inbound")
            .gte("created_at", since)
            .execute()
        )

        # Count by hour
        hours = {h: 0 for h in range(24)}
        for msg in messages.data or []:
            try:
                # isoparse handles Z, offsets and microseconds safely
                dt = isoparse(msg["created_at"])
                hours[dt.hour] += 1
            except Exception:
                continue

        return [{"hour": h, "count": c} for h, c in hours.items()]

    async def get_top_services(self, days: int = 30, limit: int = 10) -> List[Dict]:
        """Get most requested services"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        appointments = (
            db.table("appointments")
            .select("service_name")
            .gte("created_at", since)
            .execute()
        )

        # Count services
        service_counts = {}
        for apt in appointments.data or []:
            service = apt.get("service_name", "Desconhecido")
            service_counts[service] = service_counts.get(service, 0) + 1

        # Sort and return top
        sorted_services = sorted(
            service_counts.items(), key=lambda x: x[1], reverse=True
        )
        return [{"service": s, "count": c} for s, c in sorted_services[:limit]]

    async def get_top_professionals(
        self, days: int = 30, limit: int = 10
    ) -> List[Dict]:
        """Get most requested professionals"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        appointments = (
            db.table("appointments")
            .select("professional_name")
            .gte("created_at", since)
            .execute()
        )

        # Count professionals
        prof_counts = {}
        for apt in appointments.data or []:
            prof = apt.get("professional_name", "Sem preferência")
            prof_counts[prof] = prof_counts.get(prof, 0) + 1

        sorted_profs = sorted(prof_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"professional": p, "count": c} for p, c in sorted_profs[:limit]]

    async def get_intent_distribution(self, days: int = 30) -> List[Dict]:
        """Get distribution of conversation intents"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        conversations = (
            db.table("conversations")
            .select("intent")
            .gte("started_at", since)
            .execute()
        )

        intent_counts = {}
        for conv in conversations.data or []:
            intent = conv.get("intent", "outros")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        return [{"intent": i, "count": c} for i, c in intent_counts.items()]

    async def get_sentiment_distribution(self, days: int = 30) -> Dict:
        """Get sentiment distribution"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        messages = (
            db.table("messages")
            .select("sentiment")
            .eq("direction", "inbound")
            .gte("created_at", since)
            .execute()
        )

        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for msg in messages.data or []:
            sentiment = msg.get("sentiment", "neutral")
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

        total = sum(sentiment_counts.values())
        return {
            "distribution": sentiment_counts,
            "percentages": {
                k: round(v / total * 100, 1) if total > 0 else 0
                for k, v in sentiment_counts.items()
            },
            "period_days": days,
        }


insights = InsightsEngine()
