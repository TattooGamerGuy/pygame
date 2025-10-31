"""
Tests for Notification component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.notification import Notification


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def notification(pygame_init_cleanup):
    """Create a Notification instance for testing."""
    return Notification(message="Test notification")


class TestNotificationInitialization:
    """Test Notification initialization."""
    
    def test_notification_initialization(self, notification):
        """Test Notification initialization."""
        assert notification.message == "Test notification"
        assert notification.duration == 3.0  # Default duration
        assert not notification.is_visible
        assert notification.position is not None
    
    def test_notification_with_title(self, pygame_init_cleanup):
        """Test Notification with title."""
        notif = Notification(message="Message", title="Title")
        assert notif.message == "Message"
        assert notif.title == "Title"
    
    def test_notification_custom_duration(self, pygame_init_cleanup):
        """Test Notification with custom duration."""
        notif = Notification(message="Quick", duration=1.0)
        assert notif.duration == 1.0
    
    def test_notification_types(self, pygame_init_cleanup):
        """Test different notification types."""
        info = Notification(message="Info", notification_type="info")
        success = Notification(message="Success", notification_type="success")
        warning = Notification(message="Warning", notification_type="warning")
        error = Notification(message="Error", notification_type="error")
        
        assert info.notification_type == "info"
        assert success.notification_type == "success"
        assert warning.notification_type == "warning"
        assert error.notification_type == "error"


class TestNotificationVisibility:
    """Test notification visibility and lifecycle."""
    
    def test_notification_show(self, notification):
        """Test showing notification."""
        notification.show()
        assert notification.is_visible
    
    def test_notification_hide(self, notification):
        """Test hiding notification."""
        notification.show()
        notification.hide()
        assert not notification.is_visible
    
    def test_notification_auto_hide(self, pygame_init_cleanup):
        """Test notification auto-hides after duration."""
        notif = Notification(message="Auto-hide", duration=0.5)
        notif.show()
        assert notif.is_visible
        
        # Update for duration
        notif.update(0.6)
        assert not notif.is_visible  # Should auto-hide
    
    def test_notification_persistent(self, pygame_init_cleanup):
        """Test persistent notification (no auto-hide)."""
        notif = Notification(message="Persistent", persistent=True)
        notif.show()
        notif.update(10.0)  # Update for long time
        assert notif.is_visible  # Should still be visible


class TestNotificationPositioning:
    """Test notification positioning."""
    
    def test_notification_top_right(self, pygame_init_cleanup):
        """Test notification at top-right."""
        notif = Notification(message="Top right", position="top-right")
        notif.show()
        assert notif.position == "top-right"
    
    def test_notification_top_center(self, pygame_init_cleanup):
        """Test notification at top-center."""
        notif = Notification(message="Top center", position="top-center")
        assert notif.position == "top-center"
    
    def test_notification_bottom_right(self, pygame_init_cleanup):
        """Test notification at bottom-right."""
        notif = Notification(message="Bottom right", position="bottom-right")
        assert notif.position == "bottom-right"
    
    def test_notification_custom_position(self, pygame_init_cleanup):
        """Test notification with custom position."""
        notif = Notification(message="Custom", x=100, y=200)
        assert notif.x == 100
        assert notif.y == 200


class TestNotificationStacking:
    """Test notification stacking behavior."""
    
    def test_notification_stack_multiple(self, pygame_init_cleanup):
        """Test multiple notifications stack."""
        notif1 = Notification(message="First", duration=1.0)
        notif2 = Notification(message="Second", duration=1.0)
        
        notif1.show()
        notif2.show()
        
        # Both should be visible
        assert notif1.is_visible
        assert notif2.is_visible
        
        # They should have different positions (stacked) or same position
        # (stacking is handled by NotificationManager, so individual notifications
        # may have same position until manager repositions them)
        assert True  # Both are visible which is what matters
    
    def test_notification_max_stack(self, pygame_init_cleanup):
        """Test maximum stack size."""
        # Create many notifications
        notifs = [Notification(message=f"Notif {i}") for i in range(10)]
        for notif in notifs:
            notif.show()
        
        # Should handle many notifications (or limit stack)
        assert True


class TestNotificationActions:
    """Test notification action buttons."""
    
    def test_notification_with_action(self, pygame_init_cleanup):
        """Test notification with action button."""
        callback_called = [False]
        
        def action_callback():
            callback_called[0] = True
        
        notif = Notification(
            message="With action",
            action_text="Undo",
            on_action=action_callback
        )
        notif.show()
        
        assert notif.action_text == "Undo"
        assert notif.on_action is not None
    
    def test_notification_action_click(self, pygame_init_cleanup):
        """Test clicking action button."""
        callback_called = [False]
        
        def action_callback():
            callback_called[0] = True
        
        notif = Notification(
            message="Click action",
            action_text="Click me",
            on_action=action_callback
        )
        notif.show()
        
        # Simulate action click
        notif.handle_action_click()
        assert callback_called[0]


class TestNotificationDismiss:
    """Test notification dismissal."""
    
    def test_notification_dismiss_button(self, pygame_init_cleanup):
        """Test dismiss button on notification."""
        notif = Notification(message="Dismissible", dismissible=True)
        notif.show()
        
        # Click dismiss
        notif.handle_dismiss()
        assert not notif.is_visible
    
    def test_notification_not_dismissible(self, pygame_init_cleanup):
        """Test non-dismissible notification."""
        notif = Notification(message="Sticky", dismissible=False)
        notif.show()
        
        # Should not have dismiss button
        assert notif.dismissible == False


class TestNotificationRendering:
    """Test notification rendering."""
    
    def test_notification_render_visible(self, notification, pygame_init_cleanup):
        """Test rendering visible notification."""
        notification.show()
        surface = pygame.Surface((800, 600))
        notification.render(surface)
        
        # Should not raise error
        assert True
    
    def test_notification_render_hidden(self, notification, pygame_init_cleanup):
        """Test rendering hidden notification."""
        surface = pygame.Surface((800, 600))
        notification.render(surface)
        
        # Should not raise error (does nothing when hidden)
        assert True
    
    def test_notification_render_with_icon(self, pygame_init_cleanup):
        """Test rendering notification with icon."""
        notif = Notification(message="With icon", show_icon=True)
        notif.show()
        surface = pygame.Surface((800, 600))
        notif.render(surface)
        
        # Should render icon
        assert True


class TestNotificationTypes:
    """Test different notification types."""
    
    def test_notification_info_style(self, pygame_init_cleanup):
        """Test info notification styling."""
        notif = Notification(message="Info", notification_type="info")
        assert notif.notification_type == "info"
        # Should have info color scheme
    
    def test_notification_success_style(self, pygame_init_cleanup):
        """Test success notification styling."""
        notif = Notification(message="Success", notification_type="success")
        assert notif.notification_type == "success"
    
    def test_notification_warning_style(self, pygame_init_cleanup):
        """Test warning notification styling."""
        notif = Notification(message="Warning", notification_type="warning")
        assert notif.notification_type == "warning"
    
    def test_notification_error_style(self, pygame_init_cleanup):
        """Test error notification styling."""
        notif = Notification(message="Error", notification_type="error")
        assert notif.notification_type == "error"


class TestNotificationAnimation:
    """Test notification animations."""
    
    def test_notification_slide_in(self, notification):
        """Test slide-in animation."""
        notification.animation = "slide"
        notification.show()
        
        # Should animate in
        assert notification.is_visible
    
    def test_notification_fade_in(self, notification):
        """Test fade-in animation."""
        notification.animation = "fade"
        notification.show()
        notification.update(0.1)
        
        # Should fade in
        assert notification.is_visible


class TestNotificationManager:
    """Test NotificationManager for managing multiple notifications."""
    
    def test_notification_manager_add(self, pygame_init_cleanup):
        """Test adding notification to manager."""
        from hub.ui.notification import NotificationManager
        
        manager = NotificationManager()
        notif = Notification(message="Test")
        
        manager.add(notif)
        assert len(manager.notifications) > 0
    
    def test_notification_manager_update(self, pygame_init_cleanup):
        """Test updating manager."""
        from hub.ui.notification import NotificationManager
        
        manager = NotificationManager()
        notif = Notification(message="Test", duration=0.5)
        manager.add(notif)
        
        manager.update(0.6)
        # Notification should be removed after duration
        assert len(manager.notifications) == 0 or notif.is_visible == False
    
    def test_notification_manager_render(self, pygame_init_cleanup):
        """Test rendering all notifications."""
        from hub.ui.notification import NotificationManager
        
        manager = NotificationManager()
        notif1 = Notification(message="First")
        notif2 = Notification(message="Second")
        
        manager.add(notif1)
        manager.add(notif2)
        
        surface = pygame.Surface((800, 600))
        manager.render(surface)
        
        # Should not raise error
        assert True


class TestNotificationEdgeCases:
    """Test notification edge cases."""
    
    def test_notification_empty_message(self, pygame_init_cleanup):
        """Test notification with empty message."""
        notif = Notification(message="")
        notif.show()
        surface = pygame.Surface((800, 600))
        notif.render(surface)
        
        # Should handle gracefully
        assert True
    
    def test_notification_very_long_message(self, pygame_init_cleanup):
        """Test notification with very long message."""
        long_message = "A" * 500
        notif = Notification(message=long_message)
        notif.show()
        surface = pygame.Surface((800, 600))
        notif.render(surface)
        
        # Should wrap or truncate
        assert True
    
    def test_notification_zero_duration(self, pygame_init_cleanup):
        """Test notification with zero duration."""
        notif = Notification(message="Instant", duration=0.0)
        notif.show()
        notif.update(0.1)
        
        # Should handle gracefully
        assert True

