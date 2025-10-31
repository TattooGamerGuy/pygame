"""Bullet component for Space Invaders."""

import pygame
from hub.config.defaults import GREEN, RED


class Bullet:
    """Bullet component with trail effects."""
    
    def __init__(self, x: float, y: float, speed: float, is_enemy: bool = False):
        """
        Initialize bullet.
        
        Args:
            x: X position
            y: Y position
            speed: Bullet speed (always positive, direction handled here)
            is_enemy: Whether this is an enemy bullet
        """
        self.x = x
        self.y = y
        # Player bullets go UP (negative speed, toward enemies at top)
        # Enemy bullets go DOWN (positive speed, toward player at bottom)
        self.speed = -speed if not is_enemy else speed
        self.is_enemy = is_enemy
        self.width = 4
        self.height = 10
        self.trail_positions: list = []  # Store trail positions for visual effect
    
    def update(self, dt: float) -> bool:
        """
        Update bullet position.
        
        Returns:
            True if still on screen
        """
        old_y = self.y
        self.y += self.speed * dt
        
        # Update trail (store last few positions for visual effect)
        self.trail_positions.append((self.x + self.width // 2, old_y))
        if len(self.trail_positions) > 3:  # Keep last 3 positions
            self.trail_positions.pop(0)
        
        from hub.config.defaults import SCREEN_HEIGHT
        return 0 <= self.y <= SCREEN_HEIGHT
    
    def get_rect(self) -> pygame.Rect:
        """Get bullet rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render bullet with trail effect."""
        color = RED if self.is_enemy else GREEN
        rect = self.get_rect()
        
        # Draw trail (fading effect)
        if len(self.trail_positions) > 1:
            trail_color = (color[0] // 2, color[1] // 2, color[2] // 2) if len(color) == 3 else color
            for i, (trail_x, trail_y) in enumerate(self.trail_positions):
                # Simple trail as small circles
                pygame.draw.circle(surface, trail_color, (int(trail_x), int(trail_y)), 2)
        
        # Draw bullet body
        pygame.draw.rect(surface, color, rect)
        
        # Add glow/outline for 8-bit effect
        if self.is_enemy:
            # Enemy bullet - red with darker outline
            pygame.draw.rect(surface, (200, 0, 0), rect, 1)
        else:
            # Player bullet - green with brighter center
            center_x = rect.centerx
            center_y = rect.centery
            pygame.draw.circle(surface, (150, 255, 150), (center_x, center_y), 2)

