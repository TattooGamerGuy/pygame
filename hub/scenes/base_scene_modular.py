"""Modular base scene class using services and event bus."""

from abc import ABC, abstractmethod
from typing import Optional
import pygame
from hub.events.event_bus import EventBus
from hub.events.events import SceneChangeEvent, QuitEvent
from hub.services.input_service import InputService
from hub.core.display import DisplayManager


class BaseScene(ABC):
    """Abstract base class for all game scenes using dependency injection."""
    
    def __init__(
        self,
        display_manager: DisplayManager,
        input_service: InputService,
        event_bus: EventBus
    ):
        """
        Initialize the base scene.
        
        Args:
            display_manager: Display manager for screen access
            input_service: Input service for handling input
            event_bus: Event bus for communication
        """
        self.display_manager = display_manager
        self.input_service = input_service
        self.event_bus = event_bus
        self.next_scene: Optional[str] = None
        self.quit_requested: bool = False
        
        # Subscribe to events
        self.event_bus.subscribe("quit", self._handle_quit_event)
    
    @property
    def screen(self) -> pygame.Surface:
        """Get the screen surface."""
        return self.display_manager.screen
    
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
            self.event_bus.publish(QuitEvent())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.event_bus.publish(QuitEvent())
    
    def switch_scene(self, scene_name: str) -> None:
        """
        Request a scene switch via event bus.
        
        Args:
            scene_name: Name of the scene to switch to
        """
        self.event_bus.publish(SceneChangeEvent(scene_name))
    
    def should_quit(self) -> bool:
        """Check if quit was requested."""
        return self.quit_requested
    
    def get_next_scene(self) -> Optional[str]:
        """Get the name of the next scene to switch to, or None."""
        return self.next_scene
    
    def cleanup(self) -> None:
        """Cleanup resources when scene is ending."""
        self.event_bus.unsubscribe("quit", self._handle_quit_event)
    
    def _handle_quit_event(self, event: QuitEvent) -> None:
        """Handle quit event."""
        self.quit_requested = True

