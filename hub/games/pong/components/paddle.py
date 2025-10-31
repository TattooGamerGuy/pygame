"""Paddle component for Pong game."""

from typing import Optional
import pygame
from hub.config.defaults import SCREEN_HEIGHT, WHITE


class Paddle:
    """Paddle component for Pong game."""
    
    def __init__(self, x: int, y: int, width: int, height: int, speed: int):
        """
        Initialize paddle.
        
        Args:
            x: X position
            y: Y position
            width: Paddle width
            height: Paddle height
            speed: Paddle speed (pixels per second)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.score = 0
    
    def update(self, dt: float, direction: int = 0) -> None:
        """
        Update paddle position.
        
        Args:
            dt: Delta time
            direction: Direction (-1 up, 1 down, 0 none)
        """
        move_amount = self.speed * dt * direction
        self.rect.y += move_amount
        
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the paddle."""
        pygame.draw.rect(surface, WHITE, self.rect)
    
    def get_center_y(self) -> float:
        """Get paddle center Y position."""
        return self.rect.centery

