"""Debug information overlay - Modular."""

from typing import Optional
import pygame
from hub.core.debug.profiler import Profiler


class DebugOverlay:
    """On-screen debug information overlay."""
    
    def __init__(self, profiler: Profiler):
        """
        Initialize debug overlay.
        
        Args:
            profiler: Profiler instance for performance data
        """
        self.profiler = profiler
        self.enabled = False
        self.font: Optional[pygame.font.Font] = None
        self._init_font()
    
    def _init_font(self) -> None:
        """Initialize debug font."""
        try:
            self.font = pygame.font.Font(None, 16)
        except:
            self.font = None
    
    def toggle(self) -> None:
        """Toggle overlay on/off."""
        self.enabled = not self.enabled
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render debug overlay.
        
        Args:
            surface: Target surface
        """
        if not self.enabled or not self.font:
            return
        
        y_offset = 5
        line_height = 18
        
        # FPS
        fps_text = f"FPS: {self.profiler.fps:.1f}"
        self._render_text(surface, fps_text, (5, y_offset))
        y_offset += line_height
        
        # Frame time
        frame_time_text = f"Frame: {self.profiler.frame_time_ms:.2f}ms"
        self._render_text(surface, frame_time_text, (5, y_offset))
        y_offset += line_height
        
        # Average frame time
        avg_text = f"Avg: {self.profiler.avg_frame_time * 1000:.2f}ms"
        self._render_text(surface, avg_text, (5, y_offset))
        y_offset += line_height
        
        # Memory
        memory_text = f"Objects: {self.profiler.memory_usage}"
        self._render_text(surface, memory_text, (5, y_offset))
    
    def _render_text(self, surface: pygame.Surface, text: str, position: tuple) -> None:
        """
        Render debug text.
        
        Args:
            surface: Target surface
            text: Text to render
            position: (x, y) position
        """
        if self.font:
            text_surface = self.font.render(text, True, (255, 255, 0))
            surface.blit(text_surface, position)

