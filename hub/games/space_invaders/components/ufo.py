"""UFO bonus enemy component for Space Invaders."""

import random
from typing import Optional
import pygame
from hub.config.defaults import SCREEN_WIDTH, GREEN


class UFO:
    """UFO bonus enemy that moves across screen."""
    
    # Point values and their probabilities
    POINT_VALUES = [50, 100, 150, 300]
    POINT_PROBS = [0.4, 0.3, 0.2, 0.1]  # Probability for each value
    
    def __init__(self, x: float, y: float, speed: float):
        """
        Initialize UFO.
        
        Args:
            x: Starting X position
            y: Y position (top of screen)
            speed: UFO speed
        """
        self.x = x
        self.y = y
        self.width = 48
        self.height = 16
        self.speed = speed
        self.direction = 1 if x < SCREEN_WIDTH // 2 else -1
        self.points = self._randomize_points()
        self.sprite_renderer: Optional[object] = None
    
    @staticmethod
    def _randomize_points() -> int:
        """Get random point value based on probabilities."""
        rand = random.random()
        cumulative = 0.0
        for points, prob in zip(UFO.POINT_VALUES, UFO.POINT_PROBS):
            cumulative += prob
            if rand <= cumulative:
                return points
        return 50  # Default fallback
    
    def update(self, dt: float) -> bool:
        """
        Update UFO position.
        
        Args:
            dt: Delta time
            
        Returns:
            True if UFO is still on screen, False if gone
        """
        self.x += self.speed * dt * self.direction
        
        # Check if off screen
        if self.direction > 0 and self.x > SCREEN_WIDTH:
            return False
        elif self.direction < 0 and self.x + self.width < 0:
            return False
        
        return True
    
    def get_rect(self) -> pygame.Rect:
        """Get UFO rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self) -> tuple:
        """Get UFO center position."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def set_sprite_renderer(self, renderer) -> None:
        """Set sprite renderer for rendering."""
        self.sprite_renderer = renderer
    
    def render(self, surface: pygame.Surface) -> None:
        """Render UFO using sprite renderer."""
        if self.sprite_renderer:
            self.sprite_renderer.draw_ufo_bonus(
                surface,
                self.x + self.width // 2,
                self.y + self.height // 2,
                self.width,
                self.height
            )
        else:
            # Fallback to rectangle
            pygame.draw.rect(surface, GREEN, self.get_rect())

