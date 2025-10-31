"""Base scene class for all game scenes."""

from abc import ABC, abstractmethod
from typing import Optional
import pygame
from hub.utils.constants import SCREEN_SIZE


class BaseScene(ABC):
    """Abstract base class for all game scenes."""
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the base scene.
        
        Args:
            screen: The pygame Surface to render to
        """
        self.screen = screen
        self.next_scene: Optional[str] = None
        self.quit_requested: bool = False
        self.clock = pygame.time.Clock()
    
    @abstractmethod
    def init(self) -> None:
        """Initialize scene-specific resources. Called once when scene starts."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update scene logic.
        
        Args:
            dt: Delta time in seconds since last update
        """
        pass
    
    @abstractmethod
    def render(self) -> None:
        """Render the scene to the screen."""
        pass
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a pygame event.
        
        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.QUIT:
            self.quit_requested = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit_requested = True
    
    def switch_scene(self, scene_name: str) -> None:
        """
        Request a scene switch.
        
        Args:
            scene_name: Name of the scene to switch to
        """
        self.next_scene = scene_name
    
    def should_quit(self) -> bool:
        """Check if quit was requested."""
        return self.quit_requested
    
    def get_next_scene(self) -> Optional[str]:
        """Get the name of the next scene to switch to, or None."""
        return self.next_scene
    
    def cleanup(self) -> None:
        """Cleanup resources when scene is ending. Override if needed."""
        pass

