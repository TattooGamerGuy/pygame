"""Main renderer with batching - Modular."""

from typing import List, Tuple
import pygame
from hub.core.rendering.sprite_batch import SpriteBatch
from hub.core.rendering.layer_manager import LayerManager


class Renderer:
    """Main rendering coordinator with batching and layers."""
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize renderer.
        
        Args:
            screen: Target screen surface
        """
        self.screen = screen
        self.sprite_batch = SpriteBatch()
        self.layer_manager = LayerManager()
        self._clear_color = (0, 0, 0)
    
    def begin(self) -> None:
        """Begin rendering frame."""
        self.sprite_batch.begin()
        self.screen.fill(self._clear_color)
    
    def end(self) -> None:
        """End rendering frame and flush to screen."""
        self.sprite_batch.end()
        self.sprite_batch.render(self.screen)
        pygame.display.flip()
    
    def draw_sprite(
        self,
        surface: pygame.Surface,
        position: Tuple[float, float],
        layer: int = 0,
        rotation: float = 0.0,
        scale: float = 1.0
    ) -> None:
        """
        Draw a sprite.
        
        Args:
            surface: Sprite surface
            position: (x, y) position
            layer: Rendering layer (higher = drawn on top)
            rotation: Rotation angle in degrees
            scale: Scale factor
        """
        self.layer_manager.add(
            surface=surface,
            position=position,
            layer=layer,
            rotation=rotation,
            scale=scale
        )
    
    def set_clear_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set clear color.
        
        Args:
            color: RGB color tuple
        """
        self._clear_color = color
    
    def clear(self) -> None:
        """Clear the screen."""
        self.screen.fill(self._clear_color)

