"""
Tooltip component for UI.

Displays contextual help text when hovering over widgets.
"""

from typing import Optional, Tuple, List
import pygame
from hub.ui.theme import ThemeManager
from hub.ui.animation import Tween, Easing, AnimationState


class Tooltip:
    """Tooltip widget for displaying hover information."""
    
    def __init__(
        self,
        text: str,
        delay: float = 0.3,
        duration: Optional[float] = None,
        offset: Tuple[int, int] = (10, 10),
        background_color: Optional[Tuple[int, int, int]] = None,
        text_color: Optional[Tuple[int, int, int]] = None,
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 1,
        padding: int = 5,
        max_width: Optional[int] = None,
        fade_in: bool = False,
        theme=None
    ):
        """
        Initialize tooltip.
        
        Args:
            text: Tooltip text (supports newlines for multiline)
            delay: Delay before showing tooltip (seconds)
            duration: Auto-hide duration (None for no auto-hide)
            offset: Offset from mouse position
            background_color: Background color (uses theme if None)
            text_color: Text color (uses theme if None)
            border_color: Border color (uses theme if None)
            border_width: Border width
            padding: Internal padding
            max_width: Maximum width (None for auto)
            fade_in: Whether to fade in tooltip
            theme: Optional theme
        """
        self.text = text
        self.delay = delay
        self.duration = duration
        self.offset = offset
        self.border_width = border_width
        self.padding = padding
        self.max_width = max_width
        self.fade_in = fade_in
        self.theme = theme or ThemeManager.get_default_theme()
        
        # Colors
        self.background_color = background_color or (50, 50, 50)
        self.text_color = text_color or self.theme.text_color
        self.border_color = border_color or self.theme.border_color
        
        # State
        self._visible = False
        self._position = (0, 0)
        self._delay_timer = 0.0
        self._duration_timer = 0.0
        self._opacity = 1.0
        
        # Font and surface cache
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
        self._surface_cache: Optional[pygame.Surface] = None
        self._fade_tween: Optional[Tween] = None
    
    @property
    def visible(self) -> bool:
        """Check if tooltip is visible."""
        return self._visible
    
    @property
    def position(self) -> Tuple[int, int]:
        """Get tooltip position."""
        return self._position
    
    @property
    def width(self) -> int:
        """Get tooltip width."""
        if self._surface_cache:
            return self._surface_cache.get_width()
        return self._calculate_size()[0]
    
    @property
    def height(self) -> int:
        """Get tooltip height."""
        if self._surface_cache:
            return self._surface_cache.get_height()
        return self._calculate_size()[1]
    
    def _calculate_size(self) -> Tuple[int, int]:
        """Calculate tooltip size."""
        if not self.text:
            return (0, 0)
        
        lines = self.text.split('\n')
        max_line_width = 0
        
        for line in lines:
            if not line.strip():
                continue
            text_surface = self._font.render(line, True, self.text_color)
            line_width = text_surface.get_width()
            max_line_width = max(max_line_width, line_width)
        
        # Apply max_width constraint if set
        if self.max_width and max_line_width > self.max_width:
            # Estimate wrapped width
            max_line_width = self.max_width
        
        width = max_line_width + (self.padding * 2)
        line_height = self._font.get_height()
        height = (len([l for l in lines if l.strip()]) * line_height) + (self.padding * 2)
        
        return (width, height)
    
    def _rebuild_surface(self) -> None:
        """Rebuild tooltip surface."""
        if not self.text:
            self._surface_cache = None
            return
        
        lines = [line for line in self.text.split('\n') if line.strip() or line == '']
        if not lines:
            self._surface_cache = None
            return
        
        # Calculate size
        width, height = self._calculate_size()
        
        # Create surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw background
        bg_color_with_alpha = (*self.background_color, int(255 * self._opacity))
        pygame.draw.rect(surface, self.background_color, surface.get_rect())
        
        # Draw border
        if self.border_width > 0:
            border_color_with_alpha = (*self.border_color, int(255 * self._opacity))
            pygame.draw.rect(surface, self.border_color, surface.get_rect(), self.border_width)
        
        # Draw text lines
        y_offset = self.padding
        for line in lines:
            if not line.strip():
                y_offset += self._font.get_height()
                continue
            
            # Handle max_width wrapping (simple implementation)
            text_to_render = line
            if self.max_width:
                # Simple word wrap (could be improved)
                words = line.split(' ')
                wrapped_lines = []
                current_line = []
                current_width = 0
                
                for word in words:
                    word_surface = self._font.render(word, True, self.text_color)
                    word_width = word_surface.get_width()
                    
                    if current_width + word_width + (len(current_line) * self._font.size(' ')[0]) <= self.max_width:
                        current_line.append(word)
                        current_width += word_width
                    else:
                        if current_line:
                            wrapped_lines.append(' '.join(current_line))
                        current_line = [word]
                        current_width = word_width
                
                if current_line:
                    wrapped_lines.append(' '.join(current_line))
                
                text_to_render = wrapped_lines
            
            # Render text
            if isinstance(text_to_render, str):
                text_surface = self._font.render(text_to_render, True, self.text_color)
                surface.blit(text_surface, (self.padding, y_offset))
                y_offset += self._font.get_height()
            else:
                for wrapped_line in text_to_render:
                    text_surface = self._font.render(wrapped_line, True, self.text_color)
                    surface.blit(text_surface, (self.padding, y_offset))
                    y_offset += self._font.get_height()
        
        self._surface_cache = surface
    
    def show(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Show tooltip at position.
        
        Args:
            mouse_pos: Mouse position (x, y)
        """
        self._position = (
            mouse_pos[0] + self.offset[0],
            mouse_pos[1] + self.offset[1]
        )
        
        # Clamp to screen bounds (simple implementation)
        # In full implementation, would use screen size
        self._position = (
            max(0, min(self._position[0], 800)),  # Assuming max screen width
            max(0, min(self._position[1], 600))   # Assuming max screen height
        )
        
        self._delay_timer = 0.0
        self._duration_timer = 0.0
        
        if self.fade_in:
            self._opacity = 0.0
            self._visible = True  # Visible but faded
            self._fade_tween = Tween(
                start_value=0.0,
                end_value=1.0,
                duration=0.2,
                easing=Easing.ease_out,
                on_update=lambda v: setattr(self, '_opacity', v)
            )
            self._fade_tween.start()
        else:
            self._opacity = 1.0
            # Show immediately if no delay, otherwise wait for delay
            if self.delay == 0.0:
                self._visible = True
            # Otherwise visible will be set after delay in update()
        
        self._rebuild_surface()
    
    def hide(self) -> None:
        """Hide tooltip."""
        self._visible = False
        self._delay_timer = -1.0  # Use negative to indicate not showing
        self._duration_timer = 0.0
        self._opacity = 1.0
        if self._fade_tween:
            self._fade_tween.stop()
            self._fade_tween = None
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_down: bool) -> None:
        """
        Update tooltip state.
        
        Args:
            dt: Delta time
            mouse_pos: Current mouse position
            mouse_down: Whether mouse is down
        """
        # Update fade animation
        if self._fade_tween and self._fade_tween.state == AnimationState.RUNNING:
            self._fade_tween.update(dt)
            if self._fade_tween.state == AnimationState.COMPLETED:
                self._visible = True
                self._fade_tween = None
        
        # Update delay timer (only if we've called show() but aren't visible yet)
        if self._delay_timer >= 0.0 and not self._visible and not self.fade_in:
            self._delay_timer += dt
            if self._delay_timer >= self.delay:
                self._visible = True
        
        # Update position to follow mouse (if visible or during delay)
        if self._visible or (self._delay_timer >= 0.0 and self._delay_timer < self.delay):
            self._position = (
                mouse_pos[0] + self.offset[0],
                mouse_pos[1] + self.offset[1]
            )
            
            # Clamp to screen bounds
            self._position = (
                max(0, min(self._position[0], 800)),
                max(0, min(self._position[1], 600))
            )
        
        # Update duration timer
        if self._visible and self.duration is not None:
            self._duration_timer += dt
            if self._duration_timer >= self.duration:
                self.hide()
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render tooltip.
        
        Args:
            surface: Surface to render on
        """
        if not self._visible or not self.text:
            return
        
        # Rebuild surface if needed (text changed, etc.)
        if self._surface_cache is None:
            self._rebuild_surface()
        
        if self._surface_cache:
            # Apply opacity if fading
            if self._opacity < 1.0:
                temp_surface = self._surface_cache.copy()
                temp_surface.set_alpha(int(255 * self._opacity))
                surface.blit(temp_surface, self._position)
            else:
                surface.blit(self._surface_cache, self._position)

