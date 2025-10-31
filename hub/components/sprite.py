"""Sprite component for game objects."""

from typing import Optional, Tuple
import pygame
from dataclasses import dataclass


@dataclass
class SpriteComponent:
    """Component for rendering sprites."""
    
    image: Optional[pygame.Surface]
    position: Tuple[float, float]
    rotation: float = 0.0
    scale: Tuple[float, float] = (1.0, 1.0)
    visible: bool = True
    alpha: int = 255
    
    def __init__(
        self,
        image: Optional[pygame.Surface] = None,
        position: Tuple[float, float] = (0.0, 0.0),
        rotation: float = 0.0,
        scale: Tuple[float, float] = (1.0, 1.0),
        visible: bool = True,
        alpha: int = 255
    ):
        """Initialize sprite component."""
        self.image = image
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.visible = visible
        self.alpha = alpha
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render sprite to surface.
        
        Args:
            surface: Surface to render to
        """
        if not self.visible or self.image is None:
            return
        
        # Apply transformations
        img = self.image
        if self.scale != (1.0, 1.0):
            size = (int(img.get_width() * self.scale[0]), int(img.get_height() * self.scale[1]))
            img = pygame.transform.scale(img, size)
        
        if self.rotation != 0.0:
            img = pygame.transform.rotate(img, self.rotation)
        
        if self.alpha != 255:
            img = img.copy()
            img.set_alpha(self.alpha)
        
        # Draw
        rect = img.get_rect(center=self.position)
        surface.blit(img, rect)
    
    def get_rect(self) -> Optional[pygame.Rect]:
        """
        Get bounding rectangle of sprite.
        
        Returns:
            Rectangle or None if no image
        """
        if self.image is None:
            return None
        
        width = int(self.image.get_width() * self.scale[0])
        height = int(self.image.get_height() * self.scale[1])
        return pygame.Rect(
            self.position[0] - width // 2,
            self.position[1] - height // 2,
            width,
            height
        )

