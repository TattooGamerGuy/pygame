"""Base game state class - Modular."""

from abc import ABC, abstractmethod


class GameState(ABC):
    """Base class for game states."""
    
    def __init__(self, name: str):
        """
        Initialize game state.
        
        Args:
            name: State name/identifier
        """
        self.name = name
    
    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """Called when exiting this state."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update state logic.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    @abstractmethod
    def render(self, surface) -> None:
        """
        Render state.
        
        Args:
            surface: Target surface
        """
        pass

