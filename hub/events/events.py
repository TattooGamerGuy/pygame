"""Event type definitions."""

from typing import Any, Optional


class Event:
    """Base event class."""
    
    def __init__(self, name: str, data: Optional[Any] = None):
        """
        Initialize event.
        
        Args:
            name: Event name
            data: Optional event data
        """
        self.name = name
        self.data = data


class SceneChangeEvent(Event):
    """Event fired when scene changes."""
    
    def __init__(self, scene_name: str):
        """
        Initialize scene change event.
        
        Args:
            scene_name: Name of scene to change to
        """
        super().__init__("scene_change", {"scene_name": scene_name})
        self.scene_name = scene_name


class GameStartEvent(Event):
    """Event fired when a game starts."""
    
    def __init__(self, game_name: str):
        """
        Initialize game start event.
        
        Args:
            game_name: Name of game starting
        """
        super().__init__("game_start", {"game_name": game_name})
        self.game_name = game_name


class GameEndEvent(Event):
    """Event fired when a game ends."""
    
    def __init__(self, game_name: str, score: int):
        """
        Initialize game end event.
        
        Args:
            game_name: Name of game ending
            score: Final score
        """
        super().__init__("game_end", {"game_name": game_name, "score": score})
        self.game_name = game_name
        self.score = score


class QuitEvent(Event):
    """Event fired when application should quit."""
    
    def __init__(self):
        """Initialize quit event."""
        super().__init__("quit", None)

