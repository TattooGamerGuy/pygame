"""
Dropdown menu component for UI.

Supports single selection, keyboard navigation, filtering, and scrolling.
"""

from typing import Optional, List, Callable, Tuple
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager


class Dropdown(BaseWidget):
    """Dropdown menu widget."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        items: List[str],
        initial_selection: Optional[int] = 0,
        placeholder: Optional[str] = None,
        max_visible_items: Optional[int] = None,
        allow_empty: bool = False,
        on_change: Optional[Callable[[str, int], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
        theme=None
    ):
        """
        Initialize dropdown.
        
        Args:
            x: X position
            y: Y position
            width: Dropdown width
            height: Dropdown height
            items: List of selectable items
            initial_selection: Initial selected index (None for no selection)
            placeholder: Placeholder text when no selection
            max_visible_items: Maximum visible items in dropdown list
            allow_empty: Whether empty selection is allowed
            on_change: Callback when selection changes (value, index)
            on_open: Callback when dropdown opens
            on_close: Callback when dropdown closes
            theme: Optional theme
        """
        super().__init__(x, y, width, height)
        self.items = items
        self.placeholder = placeholder
        self.max_visible_items = max_visible_items or len(items)
        self.allow_empty = allow_empty
        self.on_change = on_change
        self.on_open = on_open
        self.on_close = on_close
        self.theme = theme or ThemeManager.get_default_theme()
        
        # State
        self._is_open = False
        self._selected_index = initial_selection if initial_selection is not None and initial_selection < len(items) else (0 if items and not allow_empty else None)
        self._hovered_index = None
        self._scroll_offset = 0
        self._filter_text = ""
        self._highlighted_index = None
        
        # Initialize font
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
        self._item_height = self._font.get_height() + 4
    
    @property
    def is_open(self) -> bool:
        """Check if dropdown is open."""
        return self._is_open
    
    @property
    def selected_index(self) -> Optional[int]:
        """Get selected index."""
        return self._selected_index
    
    @property
    def selected_value(self) -> Optional[str]:
        """Get selected value."""
        if self._selected_index is not None and 0 <= self._selected_index < len(self.items):
            return self.items[self._selected_index]
        return None
    
    @property
    def filtered_items(self) -> List[str]:
        """Get filtered items based on filter text."""
        if not self._filter_text:
            return self.items
        return [item for item in self.items if self._filter_text.lower() in item.lower()]
    
    @property
    def filter_text(self) -> str:
        """Get filter text."""
        return self._filter_text
    
    @filter_text.setter
    def filter_text(self, value: str) -> None:
        """Set filter text."""
        self._filter_text = value
        self._scroll_offset = 0  # Reset scroll when filtering
    
    @property
    def scroll_offset(self) -> int:
        """Get scroll offset."""
        return self._scroll_offset
    
    def select_index(self, index: int) -> None:
        """
        Select item by index.
        
        Args:
            index: Item index
        """
        if 0 <= index < len(self.items):
            old_index = self._selected_index
            self._selected_index = index
            
            if old_index != index and self.on_change:
                self.on_change(self.items[index], index)
    
    def select_value(self, value: str) -> None:
        """
        Select item by value.
        
        Args:
            value: Item value
        """
        try:
            index = self.items.index(value)
            self.select_index(index)
        except ValueError:
            pass  # Value not found
    
    def clear_selection(self) -> None:
        """Clear selection."""
        if self.allow_empty:
            old_index = self._selected_index
            self._selected_index = None
            
            if old_index is not None and self.on_change:
                self.on_change(None, None)
    
    def open(self) -> None:
        """Open dropdown."""
        if not self._is_open:
            self._is_open = True
            self._scroll_offset = 0
            self._hovered_index = None
            if self.on_open:
                self.on_open()
    
    def close(self) -> None:
        """Close dropdown."""
        if self._is_open:
            self._is_open = False
            self._hovered_index = None
            self._filter_text = ""
            if self.on_close:
                self.on_close()
    
    def toggle(self) -> None:
        """Toggle dropdown open/close."""
        if self._is_open:
            self.close()
        else:
            self.open()
    
    def scroll_up(self) -> None:
        """Scroll dropdown list up."""
        if self._scroll_offset > 0:
            self._scroll_offset -= 1
    
    def scroll_down(self) -> None:
        """Scroll dropdown list down."""
        filtered = self.filtered_items
        max_offset = max(0, len(filtered) - self.max_visible_items)
        if self._scroll_offset < max_offset:
            self._scroll_offset += 1
    
    def clear_filter(self) -> None:
        """Clear filter text."""
        self._filter_text = ""
        self._scroll_offset = 0
    
    def handle_click(self, pos: tuple) -> None:
        """
        Handle mouse click.
        
        Args:
            pos: Click position (x, y)
        """
        if self.contains_point(pos):
            self.toggle()
            return
        
        # Check if clicking on dropdown list items
        if self._is_open:
            filtered = self.filtered_items
            list_start_y = self._rect.y + self._rect.height
            
            for i in range(self.max_visible_items):
                item_index = self._scroll_offset + i
                if item_index >= len(filtered):
                    break
                
                item_y = list_start_y + (i * self._item_height)
                item_rect = pygame.Rect(self._rect.x, item_y, self._rect.width, self._item_height)
                
                if item_rect.collidepoint(pos):
                    # Find actual index in original items list
                    actual_index = self.items.index(filtered[item_index])
                    self.select_index(actual_index)
                    self.close()
                    return
            
            # Clicked outside dropdown list
            self.close()
    
    def handle_key_down(self) -> None:
        """Handle down arrow key."""
        if self._is_open:
            filtered = self.filtered_items
            if self._highlighted_index is None:
                self._highlighted_index = 0
            else:
                max_index = len(filtered) - 1
                if self._highlighted_index < max_index:
                    self._highlighted_index += 1
                    # Scroll if needed
                    if self._highlighted_index >= self._scroll_offset + self.max_visible_items:
                        self.scroll_down()
        else:
            self.open()
    
    def handle_key_up(self) -> None:
        """Handle up arrow key."""
        if self._is_open:
            if self._highlighted_index is None:
                self._highlighted_index = 0
            else:
                if self._highlighted_index > 0:
                    self._highlighted_index -= 1
                    # Scroll if needed
                    if self._highlighted_index < self._scroll_offset:
                        self.scroll_up()
    
    def handle_enter(self) -> None:
        """Handle Enter key."""
        if self._is_open and self._highlighted_index is not None:
            filtered = self.filtered_items
            if 0 <= self._highlighted_index < len(filtered):
                actual_index = self.items.index(filtered[self._highlighted_index])
                self.select_index(actual_index)
                self.close()
    
    def handle_escape(self) -> None:
        """Handle Escape key."""
        if self._is_open:
            self.close()
    
    def _update_widget(self, dt: float, mouse_pos: tuple, mouse_clicked: bool) -> None:
        """Update widget state."""
        if mouse_clicked:
            self.handle_click(mouse_pos)
        
        # Update hover state for dropdown list
        if self._is_open:
            filtered = self.filtered_items
            list_start_y = self._rect.y + self._rect.height
            
            self._hovered_index = None
            for i in range(self.max_visible_items):
                item_index = self._scroll_offset + i
                if item_index >= len(filtered):
                    break
                
                item_y = list_start_y + (i * self._item_height)
                item_rect = pygame.Rect(self._rect.x, item_y, self._rect.width, self._item_height)
                
                if item_rect.collidepoint(mouse_pos):
                    self._hovered_index = item_index
                    break
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render dropdown."""
        # Draw main button/field
        bg_color = self.theme.background_color if self._enabled else self.theme.disabled_color
        pygame.draw.rect(surface, bg_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw selected text or placeholder
        display_text = self.selected_value if self.selected_value else (self.placeholder or "")
        text_color = self.theme.text_color if self.selected_value else (128, 128, 128)
        
        if display_text:
            text_surface = self._font.render(display_text, True, text_color)
            text_rect = text_surface.get_rect(midleft=(self._rect.x + 5, self._rect.centery))
            surface.blit(text_surface, text_rect)
        
        # Draw dropdown arrow
        arrow_size = 8
        arrow_x = self._rect.right - arrow_size - 5
        arrow_y = self._rect.centery
        arrow_points = [
            (arrow_x, arrow_y - arrow_size // 2),
            (arrow_x + arrow_size, arrow_y - arrow_size // 2),
            (arrow_x + arrow_size // 2, arrow_y + arrow_size // 2)
        ]
        pygame.draw.polygon(surface, self.theme.text_color, arrow_points)
        
        # Draw dropdown list if open
        if self._is_open:
            filtered = self.filtered_items
            list_height = min(len(filtered), self.max_visible_items) * self._item_height
            list_rect = pygame.Rect(self._rect.x, self._rect.y + self._rect.height, self._rect.width, list_height)
            
            # Draw list background
            pygame.draw.rect(surface, self.theme.background_color, list_rect)
            pygame.draw.rect(surface, self.theme.border_color, list_rect, self.theme.border_width)
            
            # Draw items
            for i in range(min(len(filtered), self.max_visible_items)):
                item_index = self._scroll_offset + i
                if item_index >= len(filtered):
                    break
                
                item = filtered[item_index]
                item_y = list_rect.y + (i * self._item_height)
                item_rect = pygame.Rect(self._rect.x, item_y, self._rect.width, self._item_height)
                
                # Highlight hovered or highlighted item
                if item_index == self._hovered_index or item_index == self._highlighted_index:
                    pygame.draw.rect(surface, self.theme.hover_color, item_rect)
                
                # Highlight selected item
                if self.items.index(item) == self._selected_index:
                    pygame.draw.rect(surface, self.theme.active_color, item_rect)
                
                # Draw item text
                text_surface = self._font.render(item, True, self.theme.text_color)
                text_rect = text_surface.get_rect(midleft=(self._rect.x + 5, item_y + self._item_height // 2))
                surface.blit(text_surface, text_rect)

