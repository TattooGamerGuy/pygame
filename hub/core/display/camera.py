"""Camera and viewport management - Modular."""

from typing import Tuple, Optional
import pygame


class Camera:
    """Camera for viewport tracking and transformation."""
    
    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        width: int = 800,
        height: int = 600,
        bounds: Optional[pygame.Rect] = None
    ):
        """
        Initialize camera.
        
        Args:
            x: Camera X position
            y: Camera Y position
            width: Viewport width
            height: Viewport height
            bounds: Optional camera bounds (cannot move outside)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounds = bounds
        self.zoom = 1.0
        self.target: Optional[Tuple[float, float]] = None
        self.follow_speed: float = 0.1
    
    def set_position(self, x: float, y: float) -> None:
        """Set camera position."""
        self.x = x
        self.y = y
        self._clamp_to_bounds()
    
    def move(self, dx: float, dy: float) -> None:
        """Move camera by offset."""
        self.x += dx
        self.y += dy
        self._clamp_to_bounds()
    
    def set_target(self, target_x: float, target_y: float, speed: float = 0.1) -> None:
        """Set camera to follow a target with smooth movement."""
        self.target = (target_x, target_y)
        self.follow_speed = speed
    
    def update(self, dt: float) -> None:
        """Update camera (smooth follow if target set)."""
        if self.target:
            target_x, target_y = self.target
            dx = (target_x - self.x) * self.follow_speed
            dy = (target_y - self.y) * self.follow_speed
            self.move(dx, dy)
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        screen_x = int((world_x - self.x) * self.zoom)
        screen_y = int((world_y - self.y) * self.zoom)
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates."""
        world_x = (screen_x / self.zoom) + self.x
        world_y = (screen_y / self.zoom) + self.y
        return (world_x, world_y)
    
    def get_view_rect(self) -> pygame.Rect:
        """Get camera view rectangle in world space."""
        return pygame.Rect(
            self.x, self.y,
            self.width / self.zoom,
            self.height / self.zoom
        )
    
    def _clamp_to_bounds(self) -> None:
        """Clamp camera position to bounds if set."""
        if self.bounds:
            view_rect = self.get_view_rect()
            if view_rect.left < self.bounds.left:
                self.x = self.bounds.left
            if view_rect.top < self.bounds.top:
                self.y = self.bounds.top
            if view_rect.right > self.bounds.right:
                self.x = self.bounds.right - view_rect.width
            if view_rect.bottom > self.bounds.bottom:
                self.y = self.bounds.bottom - view_rect.height

