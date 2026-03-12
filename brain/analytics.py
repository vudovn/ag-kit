"""
📊 LUNA Analytics Dashboard - Metrics Tracking

Real-time analytics and metrics tracking for LUNA Multi-Brain V2.

Usage:
    from brain.analytics import AnalyticsDashboard
    
    dashboard = AnalyticsDashboard()
    
    # Track event
    dashboard.track("handoff_created", {"conversation_id": "conv_001"})
    
    # Get metrics
    metrics = dashboard.get_metrics(period="24h")
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


@dataclass
class Event:
    """Single analytics event"""
    event_type: str
    timestamp: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class AnalyticsDashboard:
    """
    Real-time analytics dashboard for LUNA.
    
    Tracks:
    - Cache performance
    - Handoff metrics
    - Brain routing decisions
    - API usage
    - Cost tracking
    - Error rates
    - Response times
    
    Usage:
        dashboard = AnalyticsDashboard()
        dashboard.track("cache_hit", {"contact_id": "123"})
        metrics = dashboard.get_metrics(period="24h")
    """
    
    def __init__(self, storage_file: Optional[Path] = None):
        """
        Initialize Analytics Dashboard.
        
        Args:
            storage_file: Optional file to store events
        """
        self.storage_file = storage_file
        self._events: List[Event] = []
        self._metrics_cache: Dict[str, Any] = {}
        self._cache_ttl = 60  # 1 minute
        
        # Load existing events
        if storage_file and storage_file.exists():
            self._load_events(storage_file)
    
    def track(self, event_type: str, metadata: Optional[Dict] = None):
        """
        Track analytics event.
        
        Args:
            event_type: Type of event (e.g., "cache_hit", "handoff_created")
            metadata: Additional event data
        """
        event = Event(
            event_type=event_type,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self._events.append(event)
        
        # Invalidate metrics cache
        self._metrics_cache = {}
        
        # Auto-save if storage configured
        if self.storage_file and len(self._events) % 100 == 0:
            self._save_events(self.storage_file)
    
    def get_metrics(self, period: str = "24h") -> Dict[str, Any]:
        """
        Get aggregated metrics for time period.
        
        Args:
            period: Time period ("1h", "24h", "7d", "30d")
            
        Returns:
            Aggregated metrics
        """
        # Check cache
        cache_key = f"{period}:{int(time.time() / self._cache_ttl)}"
        if cache_key in self._metrics_cache:
            return self._metrics_cache[cache_key]
        
        # Parse period
        seconds = self._parse_period(period)
        cutoff = time.time() - seconds
        
        # Filter events
        filtered = [e for e in self._events if e.timestamp >= cutoff]
        
        # Calculate metrics
        metrics = {
            "period": period,
            "total_events": len(filtered),
            "cache": self._calculate_cache_metrics(filtered),
            "handoff": self._calculate_handoff_metrics(filtered),
            "brain": self._calculate_brain_metrics(filtered),
            "api": self._calculate_api_metrics(filtered),
            "cost": self._calculate_cost_metrics(filtered),
            "errors": self._calculate_error_metrics(filtered),
            "performance": self._calculate_performance_metrics(filtered)
        }
        
        # Cache and return
        self._metrics_cache[cache_key] = metrics
        return metrics
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Get real-time stats (last 5 minutes)"""
        return self.get_metrics(period="5m")
    
    def get_trends(self, periods: List[str] = None) -> Dict[str, Any]:
        """
        Get trends across multiple periods.
        
        Args:
            periods: List of periods to compare
            
        Returns:
            Trend data
        """
        if periods is None:
            periods = ["1h", "24h", "7d"]
        
        trends = {}
        for period in periods:
            trends[period] = self.get_metrics(period)
        
        # Calculate changes
        if len(periods) >= 2:
            current = trends[periods[0]]
            previous = trends[periods[1]]
            
            trends["change"] = self._calculate_change(current, previous)
        
        return trends
    
    def export_report(self, period: str = "24h", format: str = "json") -> str:
        """
        Export analytics report.
        
        Args:
            period: Time period
            format: Export format ("json", "csv")
            
        Returns:
            Formatted report
        """
        metrics = self.get_metrics(period)
        
        if format == "json":
            return json.dumps(metrics, indent=2)
        elif format == "csv":
            return self._to_csv(metrics)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _parse_period(self, period: str) -> int:
        """Parse period string to seconds"""
        units = {
            "m": 60,
            "h": 3600,
            "d": 86400,
            "w": 604800
        }
        
        try:
            unit = period[-1]
            value = int(period[:-1])
            return value * units.get(unit, 3600)
        except (ValueError, IndexError):
            return 86400  # Default to 24h
    
    def _calculate_cache_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate cache performance metrics"""
        hits = [e for e in events if e.event_type == "cache_hit"]
        misses = [e for e in events if e.event_type == "cache_miss"]
        
        total = len(hits) + len(misses)
        hit_rate = (len(hits) / total * 100) if total > 0 else 0
        
        return {
            "hits": len(hits),
            "misses": len(misses),
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total
        }
    
    def _calculate_handoff_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate handoff metrics"""
        created = [e for e in events if e.event_type == "handoff_created"]
        accepted = [e for e in events if e.event_type == "handoff_accepted"]
        resolved = [e for e in events if e.event_type == "handoff_resolved"]
        
        # Calculate avg time to accept
        accept_times = []
        for create_event in created:
            conv_id = create_event.metadata.get("conversation_id")
            for accept_event in accepted:
                if accept_event.metadata.get("conversation_id") == conv_id:
                    time_diff = accept_event.timestamp - create_event.timestamp
                    accept_times.append(time_diff)
        
        avg_accept_time = sum(accept_times) / len(accept_times) if accept_times else 0
        
        return {
            "created": len(created),
            "accepted": len(accepted),
            "resolved": len(resolved),
            "acceptance_rate": f"{(len(accepted) / len(created) * 100) if created else 0:.2f}%",
            "avg_time_to_accept_sec": f"{avg_accept_time:.2f}"
        }
    
    def _calculate_brain_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate brain routing metrics"""
        quick = [e for e in events if e.event_type == "brain_routed" and e.metadata.get("brain") == "quick"]
        standard = [e for e in events if e.event_type == "brain_routed" and e.metadata.get("brain") == "standard"]
        complex_brain = [e for e in events if e.event_type == "brain_routed" and e.metadata.get("brain") == "complex"]
        
        return {
            "quick": len(quick),
            "standard": len(standard),
            "complex": len(complex_brain),
            "total": len(quick) + len(standard) + len(complex_brain)
        }
    
    def _calculate_api_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate API usage metrics"""
        calls = [e for e in events if e.event_type == "api_call"]
        
        return {
            "total_calls": len(calls),
            "unique_endpoints": len(set(e.metadata.get("endpoint", "") for e in calls))
        }
    
    def _calculate_cost_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate cost tracking metrics"""
        cost_events = [e for e in events if e.event_type == "cost_incurred"]
        
        total_cost = sum(e.metadata.get("cost", 0) for e in cost_events)
        
        return {
            "total_cost_usd": f"${total_cost:.4f}",
            "api_calls": len(cost_events),
            "avg_cost_per_call": f"${(total_cost / len(cost_events)) if cost_events else 0:.6f}"
        }
    
    def _calculate_error_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate error rate metrics"""
        errors = [e for e in events if e.event_type == "error"]
        total_ops = len([e for e in events if e.event_type in ["api_call", "cache_hit", "cache_miss"]])
        
        error_rate = (len(errors) / total_ops * 100) if total_ops > 0 else 0
        
        return {
            "total_errors": len(errors),
            "error_rate": f"{error_rate:.2f}%",
            "by_type": self._group_errors(errors)
        }
    
    def _group_errors(self, errors: List[Event]) -> Dict[str, int]:
        """Group errors by type"""
        grouped = defaultdict(int)
        for error in errors:
            error_type = error.metadata.get("error_type", "unknown")
            grouped[error_type] += 1
        return dict(grouped)
    
    def _calculate_performance_metrics(self, events: List[Event]) -> Dict[str, Any]:
        """Calculate performance metrics"""
        latency_events = [e for e in events if "latency_ms" in e.metadata]
        
        if not latency_events:
            return {"avg_latency_ms": 0, "p95_latency_ms": 0, "p99_latency_ms": 0}
        
        latencies = [e.metadata["latency_ms"] for e in latency_events]
        latencies.sort()
        
        return {
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": latencies[int(len(latencies) * 0.95)],
            "p99_latency_ms": latencies[int(len(latencies) * 0.99)],
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies)
        }
    
    def _calculate_change(self, current: Dict, previous: Dict) -> Dict[str, Any]:
        """Calculate change between two periods"""
        change = {}
        
        # Cache hit rate change
        current_hit = float(current.get("cache", {}).get("hit_rate", "0%").rstrip("%"))
        prev_hit = float(previous.get("cache", {}).get("hit_rate", "0%").rstrip("%"))
        change["cache_hit_rate_change"] = f"{(current_hit - prev_hit):+.2f}%"
        
        # Error rate change
        current_error = float(current.get("errors", {}).get("error_rate", "0%").rstrip("%"))
        prev_error = float(previous.get("errors", {}).get("error_rate", "0%").rstrip("%"))
        change["error_rate_change"] = f"{(current_error - prev_error):+.2f}%"
        
        return change
    
    def _to_csv(self, metrics: Dict) -> str:
        """Convert metrics to CSV format"""
        lines = ["metric,value"]
        
        def flatten(d, parent_key=""):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten(v, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat = flatten(metrics)
        for key, value in flat.items():
            lines.append(f"{key},{value}")
        
        return "\n".join(lines)
    
    def _load_events(self, file_path: Path):
        """Load events from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        event = Event(
                            event_type=data["event_type"],
                            timestamp=data["timestamp"],
                            metadata=data["metadata"]
                        )
                        self._events.append(event)
        except Exception as e:
            print(f"Warning: Could not load events: {e}")
    
    def _save_events(self, file_path: Path):
        """Save events to file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for event in self._events[-10000:]:  # Keep last 10k events
                f.write(json.dumps(event.to_dict()) + '\n')


# Global singleton
analytics_dashboard = AnalyticsDashboard()


def get_analytics() -> AnalyticsDashboard:
    """Get global analytics instance"""
    return analytics_dashboard


# Convenience functions
def track_event(event_type: str, metadata: Optional[Dict] = None):
    """Track analytics event"""
    analytics_dashboard.track(event_type, metadata)


def get_metrics(period: str = "24h") -> Dict[str, Any]:
    """Get metrics for period"""
    return analytics_dashboard.get_metrics(period)
