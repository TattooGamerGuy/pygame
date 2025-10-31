"""
Text input field component for UI.

Supports text entry, cursor navigation, selection, and validation.
"""

from typing import Optional, Callable
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager


class TextInput(BaseWidget):
    """Text input field widget."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        initial_text: str = "",
        placeholder: str = "",
        max_length: Optional[int] = None,
        numeric_only: bool = False,
        alphanumeric_only: bool = False,
        on_submit: Optional[Callable[[str], None]] = None,
        theme=None
    ):
        """
        Initialize text input.
        
        Args:
            x: X position
            y: Y position
            width: Input width
            height: Input height
            initial_text: Initial text value
            placeholder: Placeholder text when empty
            max_length: Maximum text length (None for unlimited)
            numeric_only: Only allow numeric input
            alphanumeric_only: Only allow alphanumeric input
            on_submit: Callback when Enter is pressed
            theme: Optional theme
        """
        super().__init__(x, y, width, height)
        self._text = initial_text
        self.placeholder = placeholder
        self.max_length = max_length
        self.numeric_only = numeric_only
        self.alphanumeric_only = alphanumeric_only
        self.on_submit = on_submit
        self.theme = theme or ThemeManager.get_default_theme()
        
        self._is_focused = False
        self._cursor_position = len(initial_text)
        self._selection_start = 0
        self._selection_end = 0
        self._blink_timer = 0.0
        
        # Initialize font
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
    
    @property
    def text(self) -> str:
        """Get current text."""
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """Set text."""
        # Apply constraints
        if self.max_length and len(value) > self.max_length:
            value = value[:self.max_length]
        
        if self.numeric_only:
            value = ''.join(c for c in value if c.isdigit())
        
        if self.alphanumeric_only:
            value = ''.join(c for c in value if c.isalnum())
        
        self._text = value
        # When text is set externally, move cursor to end
        self._cursor_position = len(self._text)
    
    @property
    def is_focused(self) -> bool:
        """Check if input is focused."""
        return self._is_focused
    
    @property
    def cursor_position(self) -> int:
        """Get cursor position."""
        return self._cursor_position
    
    @cursor_position.setter
    def cursor_position(self, value: int) -> None:
        """Set cursor position."""
        self._cursor_position = max(0, min(value, len(self._text)))
    
    @property
    def selection_start(self) -> int:
        """Get selection start position."""
        return self._selection_start
    
    @selection_start.setter
    def selection_start(self, value: int) -> None:
        """Set selection start position."""
        self._selection_start = max(0, min(value, len(self._text)))
    
    @property
    def selection_end(self) -> int:
        """Get selection end position."""
        return self._selection_end
    
    @selection_end.setter
    def selection_end(self, value: int) -> None:
        """Set selection end position."""
        self._selection_end = max(0, min(value, len(self._text)))
    
    @property
    def has_selection(self) -> bool:
        """Check if text is selected."""
        return self._selection_start != self._selection_end
    
    def focus(self) -> None:
        """Focus the input."""
        self._is_focused = True
    
    def unfocus(self) -> None:
        """Unfocus the input."""
        self._is_focused = False
        self.clear_selection()
    
    def handle_click(self, pos: tuple) -> None:
        """
        Handle mouse click.
        
        Args:
            pos: Click position (x, y)
        """
        if self.contains_point(pos):
            self.focus()
            # TODO: Set cursor position based on click
        else:
            self.unfocus()
    
    def handle_key(self, char: str) -> None:
        """
        Handle character key press.
        
        Args:
            char: Character to insert
        """
        if not self._is_focused:
            return
        
        # Validate character
        if self.numeric_only and not char.isdigit():
            return
        if self.alphanumeric_only and not char.isalnum():
            return
        
        # Delete selection if any
        if self.has_selection:
            self.delete_selection()
        
        # Insert character at cursor
        if self.max_length is None or len(self._text) < self.max_length:
            self._text = (
                self._text[:self._cursor_position] +
                char +
                self._text[self._cursor_position:]
            )
            self._cursor_position += 1
    
    def handle_backspace(self) -> None:
        """Handle backspace key."""
        if not self._is_focused:
            return
        
        if self.has_selection:
            self.delete_selection()
        elif self._cursor_position > 0:
            # Delete character before cursor
            self._cursor_position -= 1
            self._text = (
                self._text[:self._cursor_position] +
                self._text[self._cursor_position + 1:]
            )
    
    def handle_delete(self) -> None:
        """Handle delete key."""
        if not self._is_focused:
            return
        
        if self.has_selection:
            self.delete_selection()
        elif self._cursor_position < len(self._text):
            self._text = (
                self._text[:self._cursor_position] +
                self._text[self._cursor_position + 1:]
            )
    
    def handle_enter(self) -> None:
        """Handle Enter key."""
        if not self._is_focused:
            return
        
        if self.on_submit:
            self.on_submit(self._text)
    
    def handle_escape(self) -> None:
        """Handle Escape key."""
        if self._is_focused:
            self.unfocus()
    
    def handle_left_arrow(self) -> None:
        """Handle left arrow key."""
        if not self._is_focused:
            return
        
        if self.has_selection:
            self._cursor_position = min(self._selection_start, self._selection_end)
            self.clear_selection()
        elif self._cursor_position > 0:
            self._cursor_position -= 1
    
    def handle_right_arrow(self) -> None:
        """Handle right arrow key."""
        if not self._is_focused:
            return
        
        if self.has_selection:
            self._cursor_position = max(self._selection_start, self._selection_end)
            self.clear_selection()
        elif self._cursor_position < len(self._text):
            self._cursor_position += 1
    
    def handle_home(self) -> None:
        """Handle Home key."""
        if self._is_focused:
            self._cursor_position = 0
            self.clear_selection()
    
    def handle_end(self) -> None:
        """Handle End key."""
        if self._is_focused:
            self._cursor_position = len(self._text)
            self.clear_selection()
    
    def select_all(self) -> None:
        """Select all text."""
        if self._is_focused:
            self._selection_start = 0
            self._selection_end = len(self._text)
    
    def clear_selection(self) -> None:
        """Clear selection."""
        self._selection_start = self._cursor_position
        self._selection_end = self._cursor_position
    
    def delete_selection(self) -> None:
        """Delete selected text."""
        if not self.has_selection:
            return
        
        start = min(self._selection_start, self._selection_end)
        end = max(self._selection_start, self._selection_end)
        
        self._text = self._text[:start] + self._text[end:]
        self._cursor_position = start
        self.clear_selection()
    
    def _update_widget(self, dt: float, mouse_pos: tuple, mouse_clicked: bool) -> None:
        """Update widget state."""
        if mouse_clicked:
            self.handle_click(mouse_pos)
        
        # Update cursor blink timer
        if self._is_focused:
            self._blink_timer += dt
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render text input."""
        # Draw background
        if not self._enabled:
            bg_color = self.theme.disabled_color
        elif self._is_focused:
            bg_color = self.theme.active_color
        else:
            bg_color = self.theme.background_color
        
        pygame.draw.rect(surface, bg_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw text or placeholder
        display_text = self._text if self._text else self.placeholder
        text_color = self.theme.text_color if self._text else (128, 128, 128)  # Gray for placeholder
        
        if display_text:
            text_surface = self._font.render(display_text, True, text_color)
            # Clip text to input width
            text_rect = text_surface.get_rect(midleft=(self._rect.x + 5, self._rect.centery))
            
            # Draw selection background if any
            if self.has_selection and self._is_focused:
                # TODO: Draw selection highlight
                pass
            
            surface.blit(text_surface, text_rect)
        
        # Draw cursor if focused
        if self._is_focused and int(self._blink_timer * 2) % 2 == 0:
            cursor_x = self._rect.x + 5 + self._font.size(self._text[:self._cursor_position])[0]
            cursor_y1 = self._rect.y + 5
            cursor_y2 = self._rect.bottom - 5
            pygame.draw.line(surface, self.theme.text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

