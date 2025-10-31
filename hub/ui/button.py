"""Button widget component."""

from typing import Optional, Callable, Tuple
import pygame
from hub.ui.base_widget import BaseWidget
from hub.events.event_bus import EventBus
from hub.ui.theme import ThemeManager, Theme


class Button(BaseWidget):
    """Interactive button widget."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Optional[Callable[[], None]] = None,
        event_bus: Optional[EventBus] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize button.
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            callback: Function to call when clicked
            event_bus: Optional event bus
            theme: Optional theme (uses default if None)
        """
        super().__init__(x, y, width, height, event_bus)
        self.text = text
        self.callback = callback
        self.theme = theme or ThemeManager.get_default_theme()
        self._is_hovered = False
        self._is_pressed = False
        self._font: Optional[pygame.font.Font] = None
        self._text_surface: Optional[pygame.Surface] = None
        
        # Initialize font
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
        self._update_text_surface()
    
    def _update_text_surface(self) -> None:
        """Update text surface rendering."""
        if self._font:
            self._text_surface = self._font.render(self.text, True, self.theme.text_color)
    
    def _update_widget(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> None:
        """Update button state."""
        was_hovered = self._is_hovered
        self._is_hovered = self.contains_point(mouse_pos)
        
        if self._is_hovered and mouse_clicked and self.callback:
            self._is_pressed = True
            if not was_hovered:
                self.callback()
        else:
            self._is_pressed = False
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render button."""
        # Determine colors based on state
        if not self._enabled:
            bg_color = self.theme.disabled_color
        elif self._is_pressed:
            bg_color = self.theme.active_color
        elif self._is_hovered:
            bg_color = self.theme.hover_color
        else:
            bg_color = self.theme.background_color
        
        # Draw button background
        pygame.draw.rect(surface, bg_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw text centered
        if self._text_surface:
            text_rect = self._text_surface.get_rect(center=self._rect.center)
            surface.blit(self._text_surface, text_rect)
    
    @property
    def text(self) -> str:
        """Get button text."""
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """Set button text."""
        self._text = value
        self._update_text_surface()

