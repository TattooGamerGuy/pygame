"""Event dispatcher - Modular."""

from typing import Dict, List, Callable, Any
from collections import defaultdict


class EventBus:
    """Central event bus for pub/sub messaging."""
    
    def __init__(self):
        """Initialize event bus."""
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type identifier
            callback: Callback function to call when event is published
        """
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Event type identifier
            callback: Callback function to remove
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
    
    def publish(self, event_type: str, data: Any = None) -> None:
        """
        Publish an event.
        
        Args:
            event_type: Event type identifier
            data: Optional event data
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event callback for '{event_type}': {e}")
    
    def clear(self) -> None:
        """Clear all subscribers."""
        self._subscribers.clear()

