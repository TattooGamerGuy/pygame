"""Clock and timing management."""

from typing import Optional
import pygame
from hub.config.defaults import DEFAULT_TARGET_FPS


class ClockManager:
    """Manages game timing and frame rate limiting."""
    
    def __init__(self, target_fps: int = DEFAULT_TARGET_FPS):
        """
        Initialize clock manager.
        
        Args:
            target_fps: Target frames per second
        """
        self._clock = pygame.time.Clock()
        self._target_fps = target_fps
        self._last_time = 0.0
        self._delta_time = 0.0
        self._fps = 0.0
    
    def tick(self) -> float:
        """
        Advance clock and return delta time.
        
        Returns:
            Delta time in seconds
        """
        self._clock.tick(self._target_fps)
        self._fps = self._clock.get_fps()
        
        current_time = pygame.time.get_ticks() / 1000.0
        self._delta_time = current_time - self._last_time
        self._last_time = current_time
        
        # Cap delta time to prevent large jumps
        self._delta_time = min(self._delta_time, 0.1)
        
        return self._delta_time
    
    def reset(self) -> None:
        """Reset the clock."""
        self._last_time = pygame.time.get_ticks() / 1000.0
        self._delta_time = 0.0
    
    @property
    def delta_time(self) -> float:
        """Get last frame's delta time in seconds."""
        return self._delta_time
    
    @property
    def fps(self) -> float:
        """Get current FPS."""
        return self._fps
    
    @property
    def target_fps(self) -> int:
        """Get target FPS."""
        return self._target_fps
    
    def set_target_fps(self, fps: int) -> None:
        """Set target FPS."""
        self._target_fps = fps

