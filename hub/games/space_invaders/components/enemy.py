"""Enemy component for Space Invaders."""

from typing import Optional
import pygame
from hub.config.defaults import YELLOW


class Enemy:
    """Enemy ship component with formation AI."""
    
    def __init__(self, x: float, y: float, speed: float, enemy_type: int = 1, 
                 row: int = 0, col: int = 0):
        """
        Initialize enemy.
        
        Args:
            x: X position
            y: Y position
            speed: Enemy speed
            enemy_type: Enemy type (1=top/30pts, 2=middle/20pts, 3=bottom/10pts)
            row: Row in formation (0-based)
            col: Column in formation (0-based)
        """
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.width = 30
        self.height = 20
        self.speed = speed
        self.direction = 1
        self.enemy_type = enemy_type
        self.row = row
        self.col = col
        self.sprite_renderer: Optional[object] = None
        
        # Formation integrity - track relative position
        self.formation_offset_x = 0.0
        self.formation_offset_y = 0.0
    
    def update(self, dt: float, direction: int) -> None:
        """
        Update enemy position maintaining formation.
        
        Args:
            dt: Delta time
            direction: Movement direction (-1 left, 1 right)
        """
        self.direction = direction
        self.x += self.speed * dt * direction
        
        # Maintain formation integrity (keep relative spacing)
        self.formation_offset_x = self.x - self.initial_x
        self.formation_offset_y = self.y - self.initial_y
    
    def move_down(self, amount: float) -> None:
        """
        Move enemy down while maintaining formation.
        
        Args:
            amount: Amount to move down
        """
        self.y += amount
        self.initial_y += amount
    
    def get_rect(self) -> pygame.Rect:
        """Get enemy rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self) -> tuple:
        """Get enemy center position."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def set_sprite_renderer(self, renderer) -> None:
        """Set sprite renderer for animations."""
        self.sprite_renderer = renderer
    
    def render(self, surface: pygame.Surface) -> None:
        """Render enemy using sprite renderer."""
        if self.sprite_renderer:
            self.sprite_renderer.draw_enemy(
                surface, 
                self.x + self.width // 2, 
                self.y + self.height // 2,
                self.enemy_type,
                self.width,
                self.height
            )
        else:
            # Fallback to rectangle
            pygame.draw.rect(surface, YELLOW, self.get_rect())

