"""
Analytics service.

Tracks gameplay analytics, performance metrics, and user behavior.
Privacy-compliant analytics system.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time
import json


@dataclass
class AnalyticsEvent:
    """Analytics event."""
    event_type: str
    properties: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)


@dataclass
class Metric:
    """Analytics metric."""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)


class AnalyticsService:
    """Service for analytics tracking."""
    
    def __init__(self):
        """Initialize analytics service."""
        self._events: List[AnalyticsEvent] = []
        self._metrics: Dict[str, List[float]] = {}
        self._batch_size = 50
        self._privacy_mode = False
        self._session_id = str(time.time())
    
    def track_event(
        self,
        event_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Track an analytics event.
        
        Args:
            event_type: Event type name
            properties: Event properties
        """
        if self._privacy_mode:
            # Filter sensitive data
            properties = self._filter_sensitive_data(properties or {})
        
        event = AnalyticsEvent(
            event_type=event_type,
            properties=properties or {}
        )
        
        self._events.append(event)
        
        # Auto-batch if needed
        if len(self._events) >= self._batch_size:
            self._flush_events()
    
    def track_metric(self, name: str, value: float) -> None:
        """
        Track a metric.
        
        Args:
            name: Metric name
            value: Metric value
        """
        if name not in self._metrics:
            self._metrics[name] = []
        
        self._metrics[name].append(value)
    
    def get_events(self, limit: Optional[int] = None) -> List[AnalyticsEvent]:
        """Get tracked events."""
        events = self._events.copy()
        if limit:
            events = events[-limit:]
        return events
    
    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """
        Get statistics for a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Dictionary with min, max, avg, count
        """
        if name not in self._metrics or not self._metrics[name]:
            return {'min': 0, 'max': 0, 'avg': 0, 'count': 0}
        
        values = self._metrics[name]
        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'count': len(values)
        }
    
    def set_batch_size(self, size: int) -> None:
        """Set event batch size."""
        self._batch_size = max(1, size)
    
    def enable_privacy_mode(self, enabled: bool) -> None:
        """Enable/disable privacy mode."""
        self._privacy_mode = enabled
    
    @property
    def privacy_mode_enabled(self) -> bool:
        """Check if privacy mode is enabled."""
        return self._privacy_mode
    
    def _filter_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter sensitive data for privacy."""
        filtered = {}
        sensitive_keys = ['username', 'email', 'password', 'ip', 'address']
        
        for key, value in data.items():
            if key.lower() not in sensitive_keys:
                filtered[key] = value
        
        return filtered
    
    def _flush_events(self) -> None:
        """Flush events (would send to analytics backend in real implementation)."""
        # In real implementation, would send to analytics service
        # For now, just clear old events
        if len(self._events) > self._batch_size * 2:
            self._events = self._events[-self._batch_size:]
    
    def export_data(self, filepath: str) -> bool:
        """
        Export analytics data.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if successful
        """
        try:
            data = {
                'events': [
                    {
                        'type': e.event_type,
                        'properties': e.properties,
                        'timestamp': e.timestamp
                    }
                    for e in self._events
                ],
                'metrics': {
                    name: values
                    for name, values in self._metrics.items()
                },
                'session_id': self._session_id
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

