"""
Notification component for UI.

Supports toast notifications, alerts, badges, and notification management.
"""

from typing import Optional, Callable, List, Tuple
import pygame
from hub.ui.theme import ThemeManager
from hub.ui.animation import Tween, Easing, AnimationState


class Notification:
    """Notification widget (toast notification)."""
    
    def __init__(
        self,
        message: str,
        title: Optional[str] = None,
        notification_type: str = "info",
        duration: float = 3.0,
        persistent: bool = False,
        dismissible: bool = True,
        position: str = "top-right",
        x: Optional[int] = None,
        y: Optional[int] = None,
        action_text: Optional[str] = None,
        on_action: Optional[Callable[[], None]] = None,
        on_dismiss: Optional[Callable[[], None]] = None,
        animation: str = "slide",
        show_icon: bool = True,
        theme=None
    ):
        """
        Initialize notification.
        
        Args:
            message: Notification message
            title: Optional title
            notification_type: Type ("info", "success", "warning", "error")
            duration: Auto-hide duration in seconds (0 for persistent)
            persistent: Whether notification persists until manually dismissed
            dismissible: Whether notification can be dismissed
            position: Position preset ("top-right", "top-center", "bottom-right", etc.)
            x: Custom X position (overrides position preset)
            y: Custom Y position (overrides position preset)
            action_text: Optional action button text
            on_action: Callback when action is clicked
            on_dismiss: Callback when notification is dismissed
            animation: Animation type ("slide", "fade", "none")
            show_icon: Whether to show notification icon
            theme: Optional theme
        """
        self.message = message
        self.title = title
        self.notification_type = notification_type
        self.duration = duration if not persistent else 0.0
        self.persistent = persistent
        self.dismissible = dismissible
        self.position = position
        self.action_text = action_text
        self.on_action = on_action
        self.on_dismiss = on_dismiss
        self.animation = animation
        self.show_icon = show_icon
        self.theme = theme or ThemeManager.get_default_theme()
        
        # Screen dimensions for positioning
        self._screen_width = 800  # Default
        self._screen_height = 600  # Default
        
        # State
        self._is_visible = False
        self._timer = 0.0
        self._width = 300  # Initial estimate
        self._height = 80  # Initial estimate
        self._opacity = 1.0
        self._slide_offset = 0.0
        self._animation_tween: Optional[Tween] = None
        
        # Initialize font
        pygame.font.init()
        self._font = pygame.font.Font(None, self.theme.font_size)
        self._title_font = pygame.font.Font(None, self.theme.font_size + 2)
        self._surface_cache: Optional[pygame.Surface] = None
        
        # Calculate position (after width/height are set)
        if x is not None and y is not None:
            self._x = x
            self._y = y
        else:
            self._calculate_position(self._screen_width, self._screen_height)
    
    def _calculate_position(self, screen_width: int, screen_height: int) -> None:
        """Calculate position based on preset."""
        margin = 20
        
        if self.position == "top-right":
            self._x = screen_width - self._width - margin
            self._y = margin
        elif self.position == "top-center":
            self._x = (screen_width - self._width) // 2
            self._y = margin
        elif self.position == "top-left":
            self._x = margin
            self._y = margin
        elif self.position == "bottom-right":
            self._x = screen_width - self._width - margin
            self._y = screen_height - self._height - margin
        elif self.position == "bottom-center":
            self._x = (screen_width - self._width) // 2
            self._y = screen_height - self._height - margin
        elif self.position == "bottom-left":
            self._x = margin
            self._y = screen_height - self._height - margin
        else:
            # Default to top-right
            self._x = screen_width - self._width - margin
            self._y = margin
    
    @property
    def x(self) -> int:
        """Get X position."""
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        """Set X position."""
        self._x = value
    
    @property
    def y(self) -> int:
        """Get Y position."""
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        """Set Y position."""
        self._y = value
    
    @property
    def is_visible(self) -> bool:
        """Check if notification is visible."""
        return self._is_visible
    
    def show(self) -> None:
        """Show notification."""
        if not self._is_visible:
            self._is_visible = True
            self._timer = 0.0
            
            # Start animation
            if self.animation == "fade":
                self._opacity = 0.0
                self._animation_tween = Tween(
                    start_value=0.0,
                    end_value=1.0,
                    duration=0.3,
                    easing=Easing.ease_out,
                    on_update=lambda v: setattr(self, '_opacity', v)
                )
                self._animation_tween.start()
            elif self.animation == "slide":
                self._slide_offset = -self._width
                self._animation_tween = Tween(
                    start_value=-self._width,
                    end_value=0.0,
                    duration=0.3,
                    easing=Easing.ease_out,
                    on_update=lambda v: setattr(self, '_slide_offset', v)
                )
                self._animation_tween.start()
            
            self._rebuild_surface()
    
    def hide(self) -> None:
        """Hide notification."""
        if self._is_visible:
            self._is_visible = False
            self._timer = 0.0
            if self._animation_tween:
                self._animation_tween.stop()
            self._animation_tween = None
    
    def dismiss(self) -> None:
        """Dismiss notification."""
        self.hide()
        if self.on_dismiss:
            self.on_dismiss()
    
    def handle_action_click(self) -> None:
        """Handle action button click."""
        if self.on_action:
            self.on_action()
    
    def handle_dismiss(self) -> None:
        """Handle dismiss button click."""
        if self.dismissible:
            self.dismiss()
    
    def update(self, dt: float) -> None:
        """
        Update notification state.
        
        Args:
            dt: Delta time
        """
        if not self._is_visible:
            return
        
        # Update animation
        if self._animation_tween and self._animation_tween.state == AnimationState.RUNNING:
            self._animation_tween.update(dt)
            if self._animation_tween.state == AnimationState.COMPLETED:
                self._animation_tween = None
        
        # Update timer for auto-hide
        if not self.persistent and self.duration > 0:
            self._timer += dt
            if self._timer >= self.duration:
                self.hide()
    
    def _rebuild_surface(self) -> None:
        """Rebuild notification surface."""
        # Calculate size
        padding = 15
        icon_size = 24 if self.show_icon else 0
        
        # Calculate text width
        message_width = self._font.size(self.message)[0]
        title_width = self._title_font.size(self.title)[0] if self.title else 0
        text_width = max(message_width, title_width)
        
        self._width = text_width + padding * 2 + icon_size + 10
        if self.dismissible:
            self._width += 20  # Dismiss button
        
        if self.action_text:
            self._width += self._font.size(self.action_text)[0] + 20
        
        # Calculate height
        line_height = self._font.get_height()
        self._height = padding * 2 + line_height
        if self.title:
            self._height += self._title_font.get_height() + 5
        
        # Create surface
        self._surface_cache = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        
        # Get color based on type
        bg_color = self._get_background_color()
        border_color = self._get_border_color()
        
        # Draw background
        pygame.draw.rect(self._surface_cache, bg_color, self._surface_cache.get_rect())
        pygame.draw.rect(self._surface_cache, border_color, self._surface_cache.get_rect(), 2)
        
        # Draw icon (simplified - just a colored circle)
        if self.show_icon:
            icon_x = padding
            icon_y = self._height // 2
            pygame.draw.circle(self._surface_cache, self._get_icon_color(), (icon_x + 12, icon_y), 10)
        
        # Draw title
        text_x = padding + icon_size + 10
        text_y = padding
        if self.title:
            title_surface = self._title_font.render(self.title, True, self.theme.text_color)
            self._surface_cache.blit(title_surface, (text_x, text_y))
            text_y += self._title_font.get_height() + 5
        
        # Draw message
        message_surface = self._font.render(self.message, True, self.theme.text_color)
        self._surface_cache.blit(message_surface, (text_x, text_y))
    
    def _get_background_color(self) -> Tuple[int, int, int]:
        """Get background color based on notification type."""
        if self.notification_type == "success":
            return (50, 150, 50)  # Green
        elif self.notification_type == "warning":
            return (200, 150, 50)  # Orange
        elif self.notification_type == "error":
            return (200, 50, 50)  # Red
        else:  # info
            return (50, 100, 200)  # Blue
    
    def _get_border_color(self) -> Tuple[int, int, int]:
        """Get border color based on notification type."""
        if self.notification_type == "success":
            return (100, 200, 100)
        elif self.notification_type == "warning":
            return (255, 200, 100)
        elif self.notification_type == "error":
            return (255, 100, 100)
        else:  # info
            return (100, 150, 255)
    
    def _get_icon_color(self) -> Tuple[int, int, int]:
        """Get icon color based on notification type."""
        return self.theme.text_color
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render notification.
        
        Args:
            surface: Surface to render on
        """
        if not self._is_visible or not self._surface_cache:
            return
        
        # Calculate render position with animation offset
        render_x = self._x + int(self._slide_offset)
        render_y = self._y
        
        # Apply opacity if fading
        if self._opacity < 1.0:
            temp_surface = self._surface_cache.copy()
            temp_surface.set_alpha(int(255 * self._opacity))
            surface.blit(temp_surface, (render_x, render_y))
        else:
            surface.blit(self._surface_cache, (render_x, render_y))


class NotificationManager:
    """Manager for multiple notifications."""
    
    def __init__(self, max_notifications: int = 5):
        """
        Initialize notification manager.
        
        Args:
            max_notifications: Maximum number of visible notifications
        """
        self.notifications: List[Notification] = []
        self.max_notifications = max_notifications
    
    def add(self, notification: Notification) -> None:
        """
        Add notification to manager.
        
        Args:
            notification: Notification to add
        """
        self.notifications.append(notification)
        notification.show()
        
        # Remove old notifications if over limit
        if len(self.notifications) > self.max_notifications:
            old_notif = self.notifications.pop(0)
            old_notif.hide()
        
        # Reposition notifications for stacking
        self._reposition_notifications()
    
    def _reposition_notifications(self) -> None:
        """Reposition notifications for stacking."""
        spacing = 10
        current_y_offset = 0
        
        for notif in self.notifications:
            if notif.position.startswith("top"):
                notif._y = 20 + current_y_offset
            else:
                notif._y = 600 - 80 - 20 - current_y_offset  # Approximate
            
            current_y_offset += notif._height + spacing
    
    def remove(self, notification: Notification) -> None:
        """
        Remove notification from manager.
        
        Args:
            notification: Notification to remove
        """
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.hide()
            self._reposition_notifications()
    
    def clear(self) -> None:
        """Clear all notifications."""
        for notification in self.notifications:
            notification.hide()
        self.notifications.clear()
    
    def update(self, dt: float) -> None:
        """
        Update all notifications.
        
        Args:
            dt: Delta time
        """
        # Update notifications and remove expired ones
        expired = []
        for notification in self.notifications:
            notification.update(dt)
            if not notification.is_visible:
                expired.append(notification)
        
        for notification in expired:
            self.remove(notification)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render all notifications.
        
        Args:
            surface: Surface to render on
        """
        for notification in self.notifications:
            notification.render(surface)

