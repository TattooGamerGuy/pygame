"""
Progress bar component for UI.

Displays progress with visual feedback, optional text, and animation support.
"""

from typing import Optional, Tuple
import pygame
from hub.ui.base_widget import BaseWidget
from hub.ui.theme import ThemeManager
from hub.ui.animation import Tween, Easing, AnimationState


class ProgressBar(BaseWidget):
    """Progress bar widget for displaying completion/progress."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float = 0.0,
        max_value: float = 100.0,
        initial_value: float = 0.0,
        show_percentage: bool = False,
        label: Optional[str] = None,
        vertical: bool = False,
        background_color: Optional[Tuple[int, int, int]] = None,
        fill_color: Optional[Tuple[int, int, int]] = None,
        use_gradient: bool = False,
        theme=None
    ):
        """
        Initialize progress bar.
        
        Args:
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            min_value: Minimum value
            max_value: Maximum value
            initial_value: Initial progress value
            show_percentage: Whether to show percentage text
            label: Optional label text
            vertical: Whether bar is vertical
            background_color: Background color (uses theme if None)
            fill_color: Fill color (uses theme if None)
            use_gradient: Whether to use color gradient based on value
            theme: Optional theme
        """
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.show_percentage = show_percentage
        self.label = label
        self.vertical = vertical
        self.use_gradient = use_gradient
        self.theme = theme or ThemeManager.get_default_theme()
        
        # Ensure min <= max
        if self.min_value > self.max_value:
            self.min_value, self.max_value = self.max_value, self.min_value
        
        # Set colors
        self.background_color = background_color or self.theme.background_color
        self.fill_color = fill_color or self.theme.active_color
        
        # Set initial value
        self._value = self._clamp(initial_value)
        self._target_value = self._value
        self._animation_tween: Optional[Tween] = None
        
        # Initialize font if showing text
        if show_percentage or label:
            pygame.font.init()
            self._font = pygame.font.Font(None, self.theme.font_size)
        else:
            self._font = None
    
    @property
    def value(self) -> float:
        """Get current progress value."""
        return self._value
    
    @value.setter
    def value(self, new_value: float) -> None:
        """Set progress value."""
        self._value = self._clamp(new_value)
        self._target_value = self._value
    
    @property
    def normalized_progress(self) -> float:
        """Get normalized progress (0.0 to 1.0)."""
        if self.max_value == self.min_value:
            return 0.5  # Default to middle if no range
        return (self._value - self.min_value) / (self.max_value - self.min_value)
    
    @property
    def fill_width(self) -> int:
        """Get fill width in pixels."""
        return int(self.width * self.normalized_progress)
    
    @property
    def fill_height(self) -> int:
        """Get fill height in pixels."""
        return int(self.height * self.normalized_progress)
    
    def _clamp(self, value: float) -> float:
        """
        Clamp value to min/max range.
        
        Args:
            value: Value to clamp
            
        Returns:
            Clamped value
        """
        return max(self.min_value, min(value, self.max_value))
    
    def increment(self, amount: float) -> None:
        """
        Increment progress by amount.
        
        Args:
            amount: Amount to increment
        """
        self.value = self._value + amount
    
    def decrement(self, amount: float) -> None:
        """
        Decrement progress by amount.
        
        Args:
            amount: Amount to decrement
        """
        self.value = self._value - amount
    
    def set_value_animated(self, target_value: float, duration: float = 1.0) -> None:
        """
        Animate progress to target value.
        
        Args:
            target_value: Target value
            duration: Animation duration in seconds
        """
        target_value = self._clamp(target_value)
        self._target_value = target_value
        
        # Create tween animation
        start_value = self._value
        
        def update_value(value: float):
            self._value = value
        
        self._animation_tween = Tween(
            start_value=start_value,
            end_value=target_value,
            duration=duration,
            easing=Easing.ease_in_out,
            on_update=update_value
        )
        self._animation_tween.start()
    
    def get_current_fill_color(self) -> Tuple[int, int, int]:
        """
        Get current fill color (with gradient if enabled).
        
        Returns:
            Current fill color
        """
        if not self.use_gradient:
            return self.fill_color
        
        # Gradient: low values = red, high values = green
        normalized = self.normalized_progress
        
        if normalized < 0.5:
            # Red to yellow
            r = 255
            g = int(normalized * 2 * 255)
            b = 0
        else:
            # Yellow to green
            r = int((1.0 - normalized) * 2 * 255)
            g = 255
            b = 0
        
        return (r, g, b)
    
    def _update_widget(self, dt: float, mouse_pos: tuple, mouse_clicked: bool) -> None:
        """Update widget state."""
        # Update animation if active
        if self._animation_tween and self._animation_tween.state == AnimationState.RUNNING:
            self._animation_tween.update(dt)
            
            # Remove tween if completed
            if self._animation_tween.state == AnimationState.COMPLETED:
                self._animation_tween = None
    
    def _render_widget(self, surface: pygame.Surface) -> None:
        """Render progress bar."""
        # Draw background
        bg_color = self.background_color if self._enabled else self.theme.disabled_color
        pygame.draw.rect(surface, bg_color, self._rect)
        pygame.draw.rect(surface, self.theme.border_color, self._rect, self.theme.border_width)
        
        # Draw fill
        fill_color = self.get_current_fill_color()
        
        if self.vertical:
            # Vertical: fill from bottom
            fill_height = self.fill_height
            fill_rect = pygame.Rect(
                self.x,
                self.y + (self.height - fill_height),
                self.width,
                fill_height
            )
        else:
            # Horizontal: fill from left
            fill_width = self.fill_width
            fill_rect = pygame.Rect(
                self.x,
                self.y,
                fill_width,
                self.height
            )
        
        if fill_rect.width > 0 and fill_rect.height > 0:
            pygame.draw.rect(surface, fill_color, fill_rect)
        
        # Draw text (percentage or label)
        if self._font and (self.show_percentage or self.label):
            if self.show_percentage:
                percentage = int(self.normalized_progress * 100)
                text = f"{percentage}%"
            else:
                text = self.label or ""
            
            text_surface = self._font.render(text, True, self.theme.text_color)
            text_rect = text_surface.get_rect(center=self._rect.center)
            surface.blit(text_surface, text_rect)

