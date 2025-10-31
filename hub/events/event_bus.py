"""Event bus for publisher/subscriber pattern."""

from typing import Callable, Dict, List, Type
from hub.events.events import Event


class EventBus:
    """Event bus for decoupled communication between components."""
    
    def __init__(self):
        """Initialize event bus."""
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type name
            handler: Function to call when event is published
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Event type name
            handler: Handler function to remove
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
            except ValueError:
                pass
    
    def publish(self, event: Event) -> None:
        """
        Publish an event.
        
        Args:
            event: Event to publish
        """
        event_type = event.name
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type][:]:  # Copy list to avoid modification during iteration
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler for {event_type}: {e}")
    
    def clear(self) -> None:
        """Clear all subscribers."""
        self._subscribers.clear()

