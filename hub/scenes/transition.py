"""Scene transition effects."""

from typing import Optional, Callable
import pygame
from abc import ABC, abstractmethod


class Transition(ABC):
    """Abstract base class for scene transitions."""
    
    def __init__(self, duration: float = 0.5):
        """
        Initialize transition.
        
        Args:
            duration: Transition duration in seconds
        """
        self.duration = duration
        self.elapsed = 0.0
        self.complete = False
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update transition.
        
        Args:
            dt: Delta time
        """
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface, current_scene: pygame.Surface, next_scene: pygame.Surface) -> None:
        """
        Render transition.
        
        Args:
            surface: Target surface
            current_scene: Current scene surface
            next_scene: Next scene surface
        """
        pass


class FadeTransition(Transition):
    """Fade transition between scenes."""
    
    def update(self, dt: float) -> None:
        """Update fade transition."""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.complete = True
    
    def render(self, surface: pygame.Surface, current_scene: pygame.Surface, next_scene: pygame.Surface) -> None:
        """Render fade transition."""
        progress = min(1.0, self.elapsed / self.duration)
        alpha = int(255 * progress)
        
        # Render current scene
        surface.blit(current_scene, (0, 0))
        
        # Fade in next scene
        next_scene_copy = next_scene.copy()
        next_scene_copy.set_alpha(alpha)
        surface.blit(next_scene_copy, (0, 0))


class SlideTransition(Transition):
    """Slide transition between scenes."""
    
    def __init__(self, duration: float = 0.5, direction: str = "right"):
        """
        Initialize slide transition.
        
        Args:
            duration: Transition duration
            direction: Slide direction ("left", "right", "up", "down")
        """
        super().__init__(duration)
        self.direction = direction
    
    def update(self, dt: float) -> None:
        """Update slide transition."""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.complete = True
    
    def render(self, surface: pygame.Surface, current_scene: pygame.Surface, next_scene: pygame.Surface) -> None:
        """Render slide transition."""
        progress = min(1.0, self.elapsed / self.duration)
        width, height = surface.get_size()
        
        if self.direction == "right":
            offset_x = int(width * progress)
            surface.blit(next_scene, (offset_x - width, 0))
            surface.blit(current_scene, (offset_x, 0))
        elif self.direction == "left":
            offset_x = int(width * progress)
            surface.blit(next_scene, (width - offset_x, 0))
            surface.blit(current_scene, (-offset_x, 0))
        elif self.direction == "down":
            offset_y = int(height * progress)
            surface.blit(next_scene, (0, offset_y - height))
            surface.blit(current_scene, (0, offset_y))
        else:  # up
            offset_y = int(height * progress)
            surface.blit(next_scene, (0, height - offset_y))
            surface.blit(current_scene, (0, -offset_y))


class TransitionManager:
    """Manages scene transitions."""
    
    def __init__(self):
        """Initialize transition manager."""
        self.current_transition: Optional[Transition] = None
    
    def start_transition(self, transition: Transition) -> None:
        """Start a transition."""
        self.current_transition = transition
    
    def update(self, dt: float) -> None:
        """Update current transition."""
        if self.current_transition:
            self.current_transition.update(dt)
            if self.current_transition.complete:
                self.current_transition = None
    
    def is_transitioning(self) -> bool:
        """Check if transition is active."""
        return self.current_transition is not None and not self.current_transition.complete
    
    def render(
        self,
        surface: pygame.Surface,
        current_scene: pygame.Surface,
        next_scene: pygame.Surface
    ) -> None:
        """Render transition."""
        if self.current_transition:
            self.current_transition.render(surface, current_scene, next_scene)
        else:
            surface.blit(next_scene, (0, 0))

