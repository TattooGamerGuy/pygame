"""Label widget for text display."""

from typing import Optional, Tuple
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager, Theme


class Label(BaseWidget):
    """Text label widget."""
    
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: Optional[int] = None,
        color: Optional[Tuple[int, int, int]] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize label.
        
        Args:
            x: X position
            y: Y position
            text: Label text
            font_size: Font size (uses theme default if None)
            color: Text color (uses theme default if None)
            theme: Optional theme
        """
        self._theme = theme or ThemeManager.get_default_theme()
        self._font_size = font_size or self._theme.font_size
        self._color = color or self._theme.text_color
        
        pygame.font.init()
        self._font = pygame.font.Font(None, self._font_size)
        
        self._text = text
        self._text_surface: Optional[pygame.Surface] = None
        self._update_text_surface()
        
        # Set size based on text
        if self._text_surface:
            width, height = self._text_surface.get_size()
        else:
            width, height = 0, 0
        
        super().__init__(x, y, width, height)
    
    def _update_text_surface(self) -> None:
        """Update text surface."""
        if self._font:
            self._text_surface = self._font.render(self._text, True, self._color)
            if self._text_surface:
                self.width = self._text_surface.get_width()
                self.height = self._text_surface.get_height()
    
    def _update_widget(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> None:
        """Label has no update logic."""
        pass
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render label text."""
        if self._text_surface:
            surface.blit(self._text_surface, self._rect.topleft)
    
    @property
    def text(self) -> str:
        """Get label text."""
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """Set label text."""
        self._text = value
        self._update_text_surface()
    
    @property
    def color(self) -> Tuple[int, int, int]:
        """Get text color."""
        return self._color
    
    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        """Set text color."""
        self._color = value
        self._update_text_surface()

