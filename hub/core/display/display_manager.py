"""Display and window management."""

from typing import Tuple, Optional
import pygame
from hub.config.defaults import DEFAULT_RESOLUTION, DEFAULT_WINDOW_TITLE


class DisplayManager:
    """Manages the game window and display settings."""
    
    def __init__(
        self,
        size: Tuple[int, int] = DEFAULT_RESOLUTION,
        title: str = DEFAULT_WINDOW_TITLE,
        fullscreen: bool = False,
        resizable: bool = False
    ):
        """
        Initialize display manager.
        
        Args:
            size: Window size (width, height)
            title: Window title
            fullscreen: Start in fullscreen mode
            resizable: Allow window resizing
        """
        self._size = size
        self._title = title
        self._fullscreen = fullscreen
        self._resizable = resizable
        self._screen: Optional[pygame.Surface] = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the display."""
        if self._initialized:
            return
        
        pygame.display.init()
        
        flags = 0
        if self._fullscreen:
            flags |= pygame.FULLSCREEN
        if self._resizable:
            flags |= pygame.RESIZABLE
        
        self._screen = pygame.display.set_mode(self._size, flags)
        pygame.display.set_caption(self._title)
        self._initialized = True
    
    def cleanup(self) -> None:
        """Cleanup display resources."""
        if self._initialized:
            pygame.display.quit()
            self._initialized = False
            self._screen = None
    
    @property
    def screen(self) -> pygame.Surface:
        """Get the main screen surface."""
        if not self._initialized:
            raise RuntimeError("Display not initialized. Call initialize() first.")
        return self._screen
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get current window size."""
        if self._screen:
            return self._screen.get_size()
        return self._size
    
    @property
    def width(self) -> int:
        """Get window width."""
        return self.size[0]
    
    @property
    def height(self) -> int:
        """Get window height."""
        return self.size[1]
    
    def set_title(self, title: str) -> None:
        """Set window title."""
        self._title = title
        if self._initialized:
            pygame.display.set_caption(title)
    
    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        if not self._initialized:
            return
        
        self._fullscreen = not self._fullscreen
        flags = pygame.FULLSCREEN if self._fullscreen else 0
        if self._resizable:
            flags |= pygame.RESIZABLE
        
        self._screen = pygame.display.set_mode(self._size, flags)
    
    def flip(self) -> None:
        """Update the display."""
        if self._initialized:
            pygame.display.flip()

