"""Base event classes - Modular."""

from typing import Optional


class GameEvent:
    """Base class for all game events."""
    
    def __init__(self, event_type: str):
        """
        Initialize event.
        
        Args:
            event_type: Event type identifier
        """
        self.event_type = event_type
        self.timestamp = None  # Can be set by event bus


class GameStartEvent(GameEvent):
    """Event fired when a game starts."""
    
    def __init__(self, game_name: str):
        """
        Initialize game start event.
        
        Args:
            game_name: Name of the game
        """
        super().__init__("game_start")
        self.game_name = game_name


class GameEndEvent(GameEvent):
    """Event fired when a game ends."""
    
    def __init__(self, game_name: str, score: int = 0):
        """
        Initialize game end event.
        
        Args:
            game_name: Name of the game
            score: Final game score
        """
        super().__init__("game_end")
        self.game_name = game_name
        self.score = score


class SceneChangeEvent(GameEvent):
    """Event fired when scene changes."""
    
    def __init__(self, scene_name: str):
        """
        Initialize scene change event.
        
        Args:
            scene_name: Name of the new scene
        """
        super().__init__("scene_change")
        self.scene_name = scene_name


class QuitEvent(GameEvent):
    """Event fired when game should quit."""
    
    def __init__(self):
        """Initialize quit event."""
        super().__init__("quit")

