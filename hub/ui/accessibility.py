"""
Accessibility features for UI components.

Includes keyboard navigation, focus management, screen reader support,
high contrast mode, and font size controls.
"""

from typing import List, Optional, Dict, Callable, Any
import pygame
from hub.ui.theme import Theme, ThemeManager


class FocusManager:
    """Manages widget focus for keyboard navigation."""
    
    def __init__(self):
        """Initialize focus manager."""
        self.focus_order: List[Any] = []
        self.current_focus: Optional[Any] = None
        self.show_focus_indicator = True
        self.focus_indicator_color = (255, 255, 0)  # Yellow
        self.focus_indicator_width = 2
    
    def register(self, widget: Any, index: Optional[int] = None) -> None:
        """
        Register widget for focus.
        
        Args:
            widget: Widget to register (must have 'focused' attribute)
            index: Optional insertion index
        """
        if widget in self.focus_order:
            return
        
        if index is not None:
            self.focus_order.insert(index, widget)
        else:
            self.focus_order.append(widget)
    
    def unregister(self, widget: Any) -> None:
        """
        Unregister widget from focus.
        
        Args:
            widget: Widget to unregister
        """
        if widget in self.focus_order:
            self.focus_order.remove(widget)
            if self.current_focus == widget:
                self.clear_focus()
    
    def set_focus(self, widget: Any) -> None:
        """
        Set focus to widget.
        
        Args:
            widget: Widget to focus
        """
        if self.current_focus:
            if hasattr(self.current_focus, 'focused'):
                self.current_focus.focused = False
        
        self.current_focus = widget
        if widget and hasattr(widget, 'focused'):
            widget.focused = True
    
    def clear_focus(self) -> None:
        """Clear current focus."""
        if self.current_focus:
            if hasattr(self.current_focus, 'focused'):
                self.current_focus.focused = False
        self.current_focus = None
    
    def next_focus(self) -> None:
        """Move to next focus."""
        if not self.focus_order:
            return
        
        if self.current_focus is None:
            self.set_focus(self.focus_order[0])
            return
        
        try:
            current_index = self.focus_order.index(self.current_focus)
            next_index = (current_index + 1) % len(self.focus_order)
            self.set_focus(self.focus_order[next_index])
        except ValueError:
            self.set_focus(self.focus_order[0])
    
    def previous_focus(self) -> None:
        """Move to previous focus."""
        if not self.focus_order:
            return
        
        if self.current_focus is None:
            self.set_focus(self.focus_order[-1])
            return
        
        try:
            current_index = self.focus_order.index(self.current_focus)
            prev_index = (current_index - 1) % len(self.focus_order)
            self.set_focus(self.focus_order[prev_index])
        except ValueError:
            self.set_focus(self.focus_order[-1])


class KeyboardNavigator:
    """Handles keyboard navigation."""
    
    def __init__(self, focus_manager: FocusManager):
        """
        Initialize keyboard navigator.
        
        Args:
            focus_manager: Focus manager to use
        """
        self.focus_manager = focus_manager
        self.enabled = True
        self.navigation_keys = {
            'next': pygame.K_TAB,
            'previous': (pygame.K_TAB, True),  # Shift+Tab
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'activate': pygame.K_RETURN,
            'cancel': pygame.K_ESCAPE
        }
    
    def handle_key(self, key: int, shift: bool = False) -> None:
        """
        Handle keyboard key press.
        
        Args:
            key: Key code
            shift: Whether shift is held
        """
        if not self.enabled:
            return
        
        if key == self.navigation_keys['next'] and not shift:
            self.focus_manager.next_focus()
        elif key == self.navigation_keys['previous'][0] and shift:
            self.focus_manager.previous_focus()
        elif key == self.navigation_keys['down']:
            self.focus_manager.next_focus()
        elif key == self.navigation_keys['up']:
            self.focus_manager.previous_focus()
        elif key == self.navigation_keys['activate']:
            self._activate_focused()
        elif key == self.navigation_keys['cancel']:
            self.focus_manager.clear_focus()
    
    def _activate_focused(self) -> None:
        """Activate currently focused widget."""
        if self.focus_manager.current_focus:
            widget = self.focus_manager.current_focus
            if hasattr(widget, 'activate'):
                widget.activate()
            elif hasattr(widget, 'on_click'):
                widget.on_click()


class ScreenReader:
    """Screen reader support for accessibility."""
    
    def __init__(self):
        """Initialize screen reader."""
        self.enabled = False
        self._announce_callback: Optional[Callable[[str], None]] = None
    
    def enable(self) -> None:
        """Enable screen reader."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable screen reader."""
        self.enabled = False
    
    def announce(self, text: str, priority: str = "polite") -> None:
        """
        Announce text to screen reader.
        
        Args:
            text: Text to announce
            priority: Priority level ("polite" or "assertive")
        """
        if not self.enabled:
            return
        
        if self._announce_callback:
            self._announce_callback(text)
        # In real implementation, would integrate with actual screen reader API
    
    def set_announce_callback(self, callback: Callable[[str], None]) -> None:
        """
        Set callback for announcements.
        
        Args:
            callback: Function to call with announcement text
        """
        self._announce_callback = callback


class HighContrastTheme(Theme):
    """High contrast theme for accessibility."""
    
    def __init__(self):
        """Initialize high contrast theme."""
        super().__init__(
            name="high-contrast",
            background_color=(0, 0, 0),  # Black
            text_color=(255, 255, 255),  # White
            hover_color=(255, 255, 0),  # Yellow
            active_color=(255, 0, 0),  # Red
            disabled_color=(128, 128, 128),  # Gray
            border_color=(255, 255, 255),  # White
            border_width=3,
            font_size=28
        )


class AccessibilityManager:
    """Central manager for accessibility features."""
    
    def __init__(self):
        """Initialize accessibility manager."""
        self.focus_manager = FocusManager()
        self.keyboard_navigator = KeyboardNavigator(self.focus_manager)
        self.screen_reader = ScreenReader()
        
        self.keyboard_navigation_enabled = True
        self.screen_reader_enabled = False
        self.high_contrast_enabled = False
        self.font_scale = 1.0
        self.min_font_scale = 0.8
        self.max_font_scale = 2.0
        
        self._original_theme: Optional[Theme] = None
        self._high_contrast_theme = HighContrastTheme()
        self.current_theme = ThemeManager.get_current_theme()
    
    def enable_keyboard_navigation(self) -> None:
        """Enable keyboard navigation."""
        self.keyboard_navigation_enabled = True
        self.keyboard_navigator.enabled = True
    
    def disable_keyboard_navigation(self) -> None:
        """Disable keyboard navigation."""
        self.keyboard_navigation_enabled = False
        self.keyboard_navigator.enabled = False
    
    def enable_screen_reader(self) -> None:
        """Enable screen reader support."""
        self.screen_reader_enabled = True
        self.screen_reader.enable()
    
    def disable_screen_reader(self) -> None:
        """Disable screen reader support."""
        self.screen_reader_enabled = False
        self.screen_reader.disable()
    
    def enable_high_contrast(self) -> None:
        """Enable high contrast mode."""
        if not self.high_contrast_enabled:
            self._original_theme = ThemeManager.get_current_theme()
        
        self.high_contrast_enabled = True
        ThemeManager.set_current_theme("high-contrast", animated=False)
        if not ThemeManager.get_theme("high-contrast"):
            ThemeManager.register_theme(self._high_contrast_theme)
        ThemeManager.set_current_theme("high-contrast", animated=False)
    
    def disable_high_contrast(self) -> None:
        """Disable high contrast mode."""
        self.high_contrast_enabled = False
        if self._original_theme:
            ThemeManager.set_current_theme(self._original_theme.name, animated=False)
        else:
            ThemeManager.set_current_theme("default", animated=False)
    
    def set_font_scale(self, scale: float) -> None:
        """
        Set font size scale factor.
        
        Args:
            scale: Scale factor (1.0 = normal, 1.5 = 150%, etc.)
        """
        self.font_scale = max(self.min_font_scale, min(self.max_font_scale, scale))
    
    def get_effective_font_size(self, base_size: Optional[int] = None) -> int:
        """
        Get effective font size with scale applied.
        
        Args:
            base_size: Base font size (uses theme if None)
            
        Returns:
            Scaled font size
        """
        if base_size is None:
            base_size = self.current_theme.font_size if hasattr(self.current_theme, 'font_size') else 24
        
        return int(base_size * self.font_scale)
    
    def get_minimum_touch_size(self) -> int:
        """
        Get minimum touch target size.
        
        Returns:
            Minimum size in pixels (44x44 recommended)
        """
        return 44  # Apple's Human Interface Guidelines minimum
    
    def enforce_touch_target_size(self, widget: Any) -> None:
        """
        Enforce minimum touch target size on widget.
        
        Args:
            widget: Widget to enforce size on
        """
        min_size = self.get_minimum_touch_size()
        
        if hasattr(widget, 'width'):
            widget.width = max(widget.width, min_size)
        if hasattr(widget, 'height'):
            widget.height = max(widget.height, min_size)
    
    def handle_keyboard_input(self, key: int, shift: bool = False) -> None:
        """
        Handle keyboard input for navigation.
        
        Args:
            key: Key code
            shift: Whether shift is held
        """
        if self.keyboard_navigation_enabled:
            self.keyboard_navigator.handle_key(key, shift)
    
    def get_keyboard_shortcuts(self) -> Dict[str, str]:
        """
        Get list of keyboard shortcuts.
        
        Returns:
            Dictionary of shortcut descriptions
        """
        return {
            "Tab": "Next focus",
            "Shift+Tab": "Previous focus",
            "Arrow Keys": "Navigate",
            "Enter": "Activate",
            "Escape": "Cancel/Clear focus"
        }
    
    @property
    def current_theme(self) -> Theme:
        """Get current theme."""
        return ThemeManager.get_current_theme()
    
    @current_theme.setter
    def current_theme(self, theme: Theme) -> None:
        """Set current theme."""
        ThemeManager.set_current_theme(theme.name, animated=False)


# Global accessibility manager instance
_accessibility_manager: Optional[AccessibilityManager] = None


def get_accessibility_manager() -> AccessibilityManager:
    """
    Get global accessibility manager instance.
    
    Returns:
        Accessibility manager
    """
    global _accessibility_manager
    if _accessibility_manager is None:
        _accessibility_manager = AccessibilityManager()
    return _accessibility_manager

