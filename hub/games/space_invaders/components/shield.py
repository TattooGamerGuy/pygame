"""Shield/barrier component for Space Invaders."""

from typing import List, Tuple
import pygame
from hub.games.space_invaders.graphics.sprites import draw_shield, draw_shield_damage


class Shield:
    """Shield barrier component that protects player."""
    
    def __init__(self, x: float, y: float, width: int = 80, height: int = 60):
        """
        Initialize shield.
        
        Args:
            x: Top-left X position
            y: Top-left Y position
            width: Shield width
            height: Shield height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.segment_size = 4
        
        # Create damage mask (2D grid of segments)
        self.segments_x = width // self.segment_size
        self.segments_y = height // self.segment_size
        self.damage_mask: List[List[bool]] = [
            [False for _ in range(self.segments_x)] 
            for _ in range(self.segments_y)
        ]
        
        # Initialize shield shape (arc at top, walls on sides)
        self._initialize_shield_shape()
    
    def _initialize_shield_shape(self) -> None:
        """Initialize shield shape - arc at top, solid sides."""
        # Clear center area (where bullets should pass through gaps)
        center_start_x = self.segments_x // 4
        center_end_x = 3 * self.segments_x // 4
        arc_height = self.segments_y // 3
        
        for row in range(self.segments_y):
            for col in range(self.segments_x):
                # Top arc - create curved opening
                if row < arc_height:
                    # Calculate distance from center
                    center_col = self.segments_x // 2
                    dist_from_center = abs(col - center_col)
                    # Curve formula: wider opening at top, narrower at bottom
                    max_width = int((arc_height - row) * 1.5)
                    if dist_from_center > max_width:
                        self.damage_mask[row][col] = True  # Mark as destroyed (empty)
                
                # Left and right walls - solid except for small gaps
                elif col < self.segments_x // 6 or col >= 5 * self.segments_x // 6:
                    # Solid walls
                    pass  # Keep as False (not damaged)
                
                # Center area - mostly solid but with some gaps
                elif row < 2 * self.segments_y // 3:
                    # Small gap in center for gameplay
                    if abs(col - self.segments_x // 2) < 2 and row > arc_height:
                        self.damage_mask[row][col] = True
    
    def check_bullet_collision(self, bullet_rect: pygame.Rect) -> bool:
        """
        Check if bullet collides with shield and damage segments.
        
        Args:
            bullet_rect: Bullet rectangle
            
        Returns:
            True if bullet hit shield (and was destroyed)
        """
        # Check if bullet is within shield bounds
        if (bullet_rect.right < self.x or bullet_rect.left > self.x + self.width or
            bullet_rect.bottom < self.y or bullet_rect.top > self.y + self.height):
            return False
        
        # Convert bullet position to segment coordinates
        rel_x = bullet_rect.centerx - self.x
        rel_y = bullet_rect.centery - self.y
        
        seg_x = int(rel_x // self.segment_size)
        seg_y = int(rel_y // self.segment_size)
        
        # Check bounds
        if 0 <= seg_y < self.segments_y and 0 <= seg_x < self.segments_x:
            # Damage surrounding area (bullet destroys multiple segments)
            damage_radius = 2
            hit = False
            
            for dy in range(-damage_radius, damage_radius + 1):
                for dx in range(-damage_radius, damage_radius + 1):
                    check_y = seg_y + dy
                    check_x = seg_x + dx
                    
                    if (0 <= check_y < self.segments_y and 
                        0 <= check_x < self.segments_x and
                        not self.damage_mask[check_y][check_x]):
                        # Check if within circular damage radius
                        if dx * dx + dy * dy <= damage_radius * damage_radius:
                            self.damage_mask[check_y][check_x] = True
                            hit = True
            
            return hit
        
        return False
    
    def get_rect(self) -> pygame.Rect:
        """Get shield bounding rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render shield with damage."""
        # Draw base shield shape
        draw_shield(surface, self.x + self.width // 2, self.y + self.height // 2, 
                   self.width, self.height)
        
        # Draw damaged/destroyed segments
        draw_shield_damage(surface, self.x, self.y, self.damage_mask, self.segment_size)
    
    def is_destroyed(self) -> bool:
        """Check if shield is completely destroyed."""
        return all(all(row) for row in self.damage_mask)

