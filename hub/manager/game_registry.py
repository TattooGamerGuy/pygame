"""Game registry for auto-discovery and registration."""

from typing import Dict, List, Optional, Type, Callable
from dataclasses import dataclass
from hub.games.base_game import BaseGame


@dataclass
class GameMetadata:
    """Metadata for a registered game."""
    name: str
    display_name: str
    description: str
    game_class: Type[BaseGame]
    factory: Callable[[], BaseGame]


class GameRegistry:
    """Registry for game discovery and registration."""
    
    def __init__(self):
        """Initialize game registry."""
        self._games: Dict[str, GameMetadata] = {}
    
    def register(
        self,
        name: str,
        display_name: str,
        description: str = "",
        factory: Optional[Callable[[], BaseGame]] = None
    ) -> Callable:
        """
        Register a game.
        
        Args:
            name: Internal game name (identifier)
            display_name: Display name for UI
            description: Game description
            factory: Factory function to create game instance
        
        Returns:
            Decorator function
        """
        def decorator(game_class: Type[BaseGame]) -> Type[BaseGame]:
            if factory is None:
                def default_factory(screen):
                    return game_class(screen)
                game_factory = default_factory
            else:
                game_factory = factory
            
            self._games[name] = GameMetadata(
                name=name,
                display_name=display_name,
                description=description,
                game_class=game_class,
                factory=game_factory
            )
            return game_class
        return decorator
    
    def get_game(self, name: str) -> Optional[GameMetadata]:
        """Get game metadata by name."""
        return self._games.get(name)
    
    def get_all_games(self) -> List[GameMetadata]:
        """Get all registered games."""
        return list(self._games.values())
    
    def get_game_names(self) -> List[str]:
        """Get list of all game names."""
        return list(self._games.keys())
    
    def create_game(self, name: str, screen) -> Optional[BaseGame]:
        """
        Create a game instance.
        
        Args:
            name: Game name
            screen: Pygame screen surface
        
        Returns:
            Game instance or None if not found
        """
        metadata = self._games.get(name)
        if metadata:
            return metadata.factory(screen)
        return None
    
    def is_registered(self, name: str) -> bool:
        """Check if game is registered."""
        return name in self._games

