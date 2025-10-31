"""Sprite batching for performance - Modular."""

from typing import List, Tuple, Optional
import pygame
import math


class SpriteBatch:
    """Batches sprites for efficient rendering."""
    
    def __init__(self):
        """Initialize sprite batch."""
        self._sprites: List[dict] = []
        self._active = False
    
    def begin(self) -> None:
        """Begin sprite batching."""
        self._sprites.clear()
        self._active = True
    
    def end(self) -> None:
        """End sprite batching."""
        self._active = False
    
    def add(
        self,
        surface: pygame.Surface,
        position: Tuple[float, float],
        rotation: float = 0.0,
        scale: float = 1.0,
        tint: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """
        Add sprite to batch.
        
        Args:
            surface: Sprite surface
            position: (x, y) position
            rotation: Rotation in degrees
            scale: Scale factor
            tint: Optional color tint
        """
        if not self._active:
            return
        
        self._sprites.append({
            'surface': surface,
            'position': position,
            'rotation': rotation,
            'scale': scale,
            'tint': tint
        })
    
    def render(self, target: pygame.Surface) -> None:
        """
        Render all batched sprites.
        
        Args:
            target: Target surface to render to
        """
        for sprite in self._sprites:
            surface = sprite['surface']
            x, y = sprite['position']
            rotation = sprite['rotation']
            scale = sprite['scale']
            tint = sprite['tint']
            
            # Apply transformations
            if scale != 1.0:
                new_size = (int(surface.get_width() * scale), int(surface.get_height() * scale))
                surface = pygame.transform.scale(surface, new_size)
            
            if rotation != 0.0:
                surface = pygame.transform.rotate(surface, rotation)
            
            if tint:
                # Apply color tint
                tinted = surface.copy()
                tinted.fill(tint, special_flags=pygame.BLEND_MULT)
                surface = tinted
            
            # Render
            target.blit(surface, (x, y))

