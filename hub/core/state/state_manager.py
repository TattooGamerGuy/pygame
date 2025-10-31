"""State machine for game states - Modular."""

from typing import Dict, Optional
from hub.core.state.game_state import GameState


class StateManager:
    """Manages game state transitions."""
    
    def __init__(self):
        """Initialize state manager."""
        self._states: Dict[str, GameState] = {}
        self._current_state: Optional[GameState] = None
        self._previous_state: Optional[GameState] = None
    
    def register_state(self, name: str, state: GameState) -> None:
        """
        Register a game state.
        
        Args:
            name: State identifier
            state: GameState instance
        """
        self._states[name] = state
    
    def change_state(self, name: str) -> bool:
        """
        Change to a different state.
        
        Args:
            name: State identifier
            
        Returns:
            True if state changed successfully
        """
        if name not in self._states:
            print(f"Warning: State '{name}' not registered")
            return False
        
        new_state = self._states[name]
        
        # Exit current state
        if self._current_state:
            self._current_state.exit()
            self._previous_state = self._current_state
        
        # Enter new state
        self._current_state = new_state
        self._current_state.enter()
        
        return True
    
    def update(self, dt: float) -> None:
        """
        Update current state.
        
        Args:
            dt: Delta time in seconds
        """
        if self._current_state:
            self._current_state.update(dt)
    
    def render(self, surface) -> None:
        """
        Render current state.
        
        Args:
            surface: Target surface
        """
        if self._current_state:
            self._current_state.render(surface)
    
    @property
    def current_state(self) -> Optional[GameState]:
        """Get current state."""
        return self._current_state
    
    @property
    def previous_state(self) -> Optional[GameState]:
        """Get previous state."""
        return self._previous_state

