"""Player component for Space Invaders."""

import pygame
from hub.config.defaults import SCREEN_WIDTH, GREEN


class Player:
    """Player ship component."""
    
    def __init__(self, x: float, y: float, speed: float):
        """
        Initialize player.
        
        Args:
            x: X position
            y: Y position
            speed: Player max speed
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.max_speed = speed
        self.velocity = 0.0  # Current velocity for smooth acceleration
        self.acceleration = speed * 8.0  # Acceleration rate
        self.deceleration = speed * 10.0  # Deceleration rate
    
    def update(self, dt: float, direction: int) -> None:
        """
        Update player position with acceleration/deceleration.
        
        Args:
            dt: Delta time
            direction: Movement direction (-1 left, 1 right, 0 stop)
        """
        # Apply acceleration or deceleration
        if direction != 0:
            # Accelerate in direction
            target_velocity = direction * self.max_speed
            velocity_diff = target_velocity - self.velocity
            acceleration_amount = self.acceleration * dt
            
            if abs(velocity_diff) < acceleration_amount:
                self.velocity = target_velocity
            else:
                self.velocity += acceleration_amount * (1 if velocity_diff > 0 else -1)
        else:
            # Decelerate when no input
            if abs(self.velocity) < self.deceleration * dt:
                self.velocity = 0.0
            else:
                decel_amount = self.deceleration * dt
                self.velocity -= decel_amount * (1 if self.velocity > 0 else -1)
        
        # Update position
        self.x += self.velocity * dt
        
        # Boundary clamping (keep player on screen)
        self.x = max(0.0, min(self.x, SCREEN_WIDTH - self.width))
    
    def get_rect(self) -> pygame.Rect:
        """Get player rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface, sprite_renderer=None) -> None:
        """
        Render player.
        
        Args:
            surface: Surface to render to
            sprite_renderer: Optional sprite renderer for custom drawing
        """
        if sprite_renderer:
            sprite_renderer.draw_player(
                surface,
                self.x + self.width // 2,
                self.y + self.height // 2,
                self.width,
                self.height
            )
        else:
            # Fallback to rectangle
            pygame.draw.rect(surface, GREEN, self.get_rect())

