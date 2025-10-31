"""
Slider component for UI.

Supports horizontal and vertical sliders with value ranges, steps, and callbacks.
"""

from typing import Optional, Callable
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager


class Slider(BaseWidget):
    """Slider widget for selecting numeric values."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float,
        max_value: float,
        initial_value: Optional[float] = None,
        step: Optional[float] = None,
        vertical: bool = False,
        on_change: Optional[Callable[[float], None]] = None,
        theme=None
    ):
        """
        Initialize slider.
        
        Args:
            x: X position
            y: Y position
            width: Slider width
            height: Slider height
            min_value: Minimum value
            max_value: Maximum value
            initial_value: Initial value (defaults to middle)
            step: Step value for snapping (None for continuous)
            vertical: Whether slider is vertical
            on_change: Callback when value changes
            theme: Optional theme
        """
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.vertical = vertical
        self.on_change = on_change
        self.theme = theme or ThemeManager.get_default_theme()
        
        # Ensure min <= max
        if self.min_value > self.max_value:
            self.min_value, self.max_value = self.max_value, self.min_value
        
        # Set initial value
        if initial_value is None:
            initial_value = (min_value + max_value) / 2.0
        
        # Set value without calling callback during initialization
        self._value = self._clamp_and_snap(initial_value)
        self._initialized = False  # Track if we've called callbacks yet
        self._is_dragging = False
        self._drag_start_pos = None
    
    @property
    def value(self) -> float:
        """Get current value."""
        return self._value
    
    @value.setter
    def value(self, new_value: float) -> None:
        """Set value."""
        old_value = self._value
        clamped_value = self._clamp_and_snap(new_value)
        
        # Update value
        self._value = clamped_value
        
        # Call callback if value changed (and after initialization)
        if self._value != old_value:
            self._initialized = True
            if self.on_change:
                self.on_change(self._value)
    
    @property
    def normalized_value(self) -> float:
        """Get normalized value (0.0 to 1.0)."""
        if self.max_value == self.min_value:
            return 0.0
        return (self._value - self.min_value) / (self.max_value - self.min_value)
    
    @property
    def handle_position(self) -> tuple:
        """Get handle position (x, y)."""
        normalized = self.normalized_value
        
        if self.vertical:
            # Vertical: top is max, bottom is min
            y = self.y + int((1.0 - normalized) * self.height)
            x = self.x + self.width // 2
            return (x, y)
        else:
            # Horizontal: left is min, right is max
            x = self.x + int(normalized * self.width)
            y = self.y + self.height // 2
            return (x, y)
    
    def _clamp_and_snap(self, value: float) -> float:
        """
        Clamp value to range and snap to step if applicable.
        
        Args:
            value: Value to clamp and snap
            
        Returns:
            Clamped and snapped value
        """
        # Clamp to range
        value = max(self.min_value, min(value, self.max_value))
        
        # Snap to step if applicable
        if self.step and self.step > 0:
            value = round(value / self.step) * self.step
            # Clamp again after snapping
            value = max(self.min_value, min(value, self.max_value))
        
        return value
    
    def _value_from_position(self, pos: tuple) -> float:
        """
        Get value from screen position.
        
        Args:
            pos: Screen position (x, y)
            
        Returns:
            Value corresponding to position
        """
        px, py = pos
        
        if self.vertical:
            # Vertical: top is max, bottom is min
            # Clamp py to slider bounds first
            clamped_py = max(self.y, min(py, self.y + self.height - 1))
            
            # Normalized: 0.0 at bottom (min), 1.0 at top (max)
            # Calculate based on where click is relative to slider
            # For height=200, y=0: py=0 -> normalized=1.0, py=199 -> normalized~=0.0
            normalized = 1.0 - ((clamped_py - self.y) / max(1, self.height - 1))
            value = self.min_value + normalized * (self.max_value - self.min_value)
        else:
            # Horizontal: left is min
            if px <= self.x:
                return self.min_value
            elif px >= self.x + self.width:
                return self.max_value
            else:
                normalized = (px - self.x) / self.width
                value = self.min_value + normalized * (self.max_value - self.min_value)
        
        return self._clamp_and_snap(value)
    
    def focus(self) -> None:
        """Focus the slider."""
        self._is_focused = True
    
    def unfocus(self) -> None:
        """Unfocus the slider."""
        self._is_focused = False
        self._is_dragging = False
    
    def handle_click(self, pos: tuple) -> None:
        """
        Handle mouse click.
        
        Args:
            pos: Click position (x, y)
        """
        if self.contains_point(pos):
            self.focus()
            # Set value based on click position
            self.value = self._value_from_position(pos)
            self._is_dragging = True
            self._drag_start_pos = pos
        else:
            self.unfocus()
    
    def handle_mouse_down(self, pos: tuple) -> None:
        """
        Handle mouse down event.
        
        Args:
            pos: Mouse position (x, y)
        """
        if self.contains_point(pos):
            self._is_dragging = True
            self._drag_start_pos = pos
    
    def handle_mouse_drag(self, pos: tuple) -> None:
        """
        Handle mouse drag event.
        
        Args:
            pos: Mouse position (x, y)
        """
        if self._is_dragging:
            # Clamp position to slider bounds
            if self.vertical:
                clamped_y = max(self.y, min(pos[1], self.y + self.height))
                clamped_pos = (self.handle_position[0], clamped_y)
            else:
                clamped_x = max(self.x, min(pos[0], self.x + self.width))
                clamped_pos = (clamped_x, self.handle_position[1])
            
            self.value = self._value_from_position(clamped_pos)
    
    def handle_mouse_up(self, pos: tuple) -> None:
        """
        Handle mouse up event.
        
        Args:
            pos: Mouse position (x, y)
        """
        self._is_dragging = False
    
    def _update_widget(self, dt: float, mouse_pos: tuple, mouse_clicked: bool) -> None:
        """Update widget state."""
        # Update drag state if needed
        # (Implementation may track mouse state externally)
        pass
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render slider."""
        # Draw track background
        track_color = self.theme.background_color if self._enabled else self.theme.disabled_color
        pygame.draw.rect(surface, track_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw filled portion
        if self.vertical:
            fill_height = int(self.normalized_value * self.height)
            fill_rect = pygame.Rect(
                self.x,
                self.y + (self.height - fill_height),
                self.width,
                fill_height
            )
        else:
            fill_width = int(self.normalized_value * self.width)
            fill_rect = pygame.Rect(self.x, self.y, fill_width, self.height)
        
        fill_color = self.theme.active_color if self._is_focused else self.theme.hover_color
        pygame.draw.rect(surface, fill_color, fill_rect)
        
        # Draw handle
        handle_pos = self.handle_position
        handle_radius = min(self.width, self.height) // 4
        
        handle_color = self.theme.active_color if self._is_focused or self._is_dragging else self.theme.text_color
        pygame.draw.circle(surface, handle_color, handle_pos, handle_radius)
        pygame.draw.circle(surface, self.theme.border_color, handle_pos, handle_radius, 2)

