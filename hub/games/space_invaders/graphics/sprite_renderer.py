"""Sprite renderer for managing 8-bit sprite animations and rendering."""

from typing import Optional, Tuple
import pygame
from hub.games.space_invaders.graphics.sprites import (
    draw_player_ship, draw_enemy_type1, draw_enemy_type2, 
    draw_enemy_type3, draw_ufo, draw_explosion
)


class SpriteRenderer:
    """Manages sprite rendering and animations."""
    
    def __init__(self):
        """Initialize sprite renderer."""
        self.frame_timer = 0.0
        self.animation_speed = 0.5  # seconds per frame
        self.current_frame = 0
    
    def update(self, dt: float) -> None:
        """
        Update animation timer.
        
        Args:
            dt: Delta time in seconds
        """
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.current_frame = 1 - self.current_frame  # Toggle 0/1
    
    def get_animation_frame(self) -> int:
        """Get current animation frame (0 or 1)."""
        return self.current_frame
    
    @staticmethod
    def draw_player(surface: pygame.Surface, x: float, y: float, width: int = 40, height: int = 30) -> None:
        """Draw player ship."""
        draw_player_ship(surface, x, y, width, height)
    
    def draw_enemy(self, surface: pygame.Surface, x: float, y: float, 
                   enemy_type: int, width: int = 30, height: int = 20) -> None:
        """
        Draw enemy by type.
        
        Args:
            surface: Surface to draw on
            x: X position
            y: Y position
            enemy_type: Enemy type (1, 2, or 3)
            width: Enemy width
            height: Enemy height
        """
        frame = self.get_animation_frame()
        if enemy_type == 1:
            draw_enemy_type1(surface, x, y, width, height, frame)
        elif enemy_type == 2:
            draw_enemy_type2(surface, x, y, width, height, frame)
        elif enemy_type == 3:
            draw_enemy_type3(surface, x, y, width, height, frame)
    
    @staticmethod
    def draw_ufo_bonus(surface: pygame.Surface, x: float, y: float, width: int = 48, height: int = 16) -> None:
        """Draw UFO bonus enemy."""
        draw_ufo(surface, x, y, width, height)
    
    @staticmethod
    def draw_explosion_effect(surface: pygame.Surface, x: float, y: float, 
                             frame: int, size: int = 20) -> None:
        """Draw explosion animation."""
        draw_explosion(surface, x, y, frame, size)

