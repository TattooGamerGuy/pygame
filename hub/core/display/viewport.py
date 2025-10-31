"""Viewport calculations and scaling - Modular."""

from typing import Tuple
import pygame


class Viewport:
    """Manages viewport scaling and aspect ratio."""
    
    def __init__(
        self,
        virtual_width: int = 800,
        virtual_height: int = 600,
        screen_width: int = 800,
        screen_height: int = 600
    ):
        """
        Initialize viewport.
        
        Args:
            virtual_width: Virtual screen width (game logic resolution)
            virtual_height: Virtual screen height (game logic resolution)
            screen_width: Actual screen width
            screen_height: Actual screen height
        """
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._scale_x = 1.0
        self._scale_y = 1.0
        self._offset_x = 0
        self._offset_y = 0
        self._update_scaling()
    
    def _update_scaling(self) -> None:
        """Update scale factors based on aspect ratio."""
        scale_x = self.screen_width / self.virtual_width
        scale_y = self.screen_height / self.virtual_height
        
        # Letterbox/pillarbox to maintain aspect ratio
        self._scale_x = min(scale_x, scale_y)
        self._scale_y = min(scale_x, scale_y)
        
        # Calculate offsets for centering
        scaled_width = self.virtual_width * self._scale_x
        scaled_height = self.virtual_height * self._scale_y
        self._offset_x = (self.screen_width - scaled_width) // 2
        self._offset_y = (self.screen_height - scaled_height) // 2
    
    def resize(self, screen_width: int, screen_height: int) -> None:
        """Update viewport for new screen size."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._update_scaling()
    
    def virtual_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """Convert virtual coordinates to screen coordinates."""
        screen_x = int(x * self._scale_x + self._offset_x)
        screen_y = int(y * self._scale_y + self._offset_y)
        return (screen_x, screen_y)
    
    def screen_to_virtual(self, x: int, y: int) -> Tuple[float, float]:
        """Convert screen coordinates to virtual coordinates."""
        virtual_x = (x - self._offset_x) / self._scale_x
        virtual_y = (y - self._offset_y) / self._scale_y
        return (virtual_x, virtual_y)
    
    def get_viewport_rect(self) -> pygame.Rect:
        """Get viewport rectangle on screen (with letterboxing)."""
        return pygame.Rect(
            self._offset_x,
            self._offset_y,
            self.virtual_width * self._scale_x,
            self.virtual_height * self._scale_y
        )
    
    @property
    def scale_x(self) -> float:
        """Get X scale factor."""
        return self._scale_x
    
    @property
    def scale_y(self) -> float:
        """Get Y scale factor."""
        return self._scale_y

