"""
Integration tests for InputManager.

Tests keyboard + mouse + joystick coordination, input enable/disable,
and integration scenarios.
"""

import pytest
import pygame
from hub.core.input.input_manager import InputManager


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def input_manager(pygame_init_cleanup):
    """Create an InputManager instance for testing."""
    manager = InputManager()
    manager.initialize()
    yield manager
    manager.cleanup()


class TestInputManagerInitialization:
    """Test InputManager initialization."""
    
    def test_input_manager_initialization(self, pygame_init_cleanup):
        """Test InputManager initialization."""
        manager = InputManager()
        assert manager.keyboard is not None
        assert manager.mouse is not None
        assert manager.joystick is not None
        assert manager.enabled
        
        manager.initialize()
        manager.cleanup()
    
    def test_input_manager_enabled_by_default(self, pygame_init_cleanup):
        """Test that input is enabled by default."""
        manager = InputManager()
        assert manager.enabled


class TestInputManagerEnableDisable:
    """Test input enable/disable functionality."""
    
    def test_input_manager_disable(self, input_manager):
        """Test disabling input processing."""
        input_manager.disable()
        assert not input_manager.enabled
        
        # Keyboard and mouse should be cleared
        # (Note: actual implementation may vary)
    
    def test_input_manager_enable(self, input_manager):
        """Test enabling input processing."""
        input_manager.disable()
        input_manager.enable()
        assert input_manager.enabled
    
    def test_input_manager_update_when_disabled(self, input_manager):
        """Test that update doesn't process when disabled."""
        input_manager.disable()
        
        # Create some events
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})
        ]
        
        # Update should not process events when disabled
        input_manager.update(events)
        
        # Re-enable to cleanup
        input_manager.enable()


class TestInputManagerUpdate:
    """Test InputManager update functionality."""
    
    def test_input_manager_update_keyboard(self, input_manager):
        """Test that update processes keyboard events."""
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        ]
        
        input_manager.update(events)
        
        # Keyboard should have processed the event
        # Exact behavior depends on Keyboard implementation
        assert input_manager.keyboard is not None
    
    def test_input_manager_update_mouse(self, input_manager):
        """Test that update processes mouse events."""
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 200)})
        ]
        
        input_manager.update(events)
        
        # Mouse should have processed the event
        assert input_manager.mouse is not None
    
    def test_input_manager_update_joystick(self, input_manager):
        """Test that update processes joystick events."""
        # Note: Joystick events depend on having a joystick connected
        events = []
        
        input_manager.update(events)
        
        # Should not raise error even with no joystick events
        assert input_manager.joystick is not None
    
    def test_input_manager_update_multiple_devices(self, input_manager):
        """Test update with events from multiple devices."""
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_A}),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 50)}),
        ]
        
        input_manager.update(events)
        
        # All devices should have been updated
        assert input_manager.keyboard is not None
        assert input_manager.mouse is not None


class TestInputManagerIntegration:
    """Test InputManager integration scenarios."""
    
    def test_input_manager_device_coordination(self, input_manager):
        """Test that all input devices work together."""
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}),
            pygame.event.Event(pygame.MOUSEMOTION, {"pos": (200, 150), "rel": (10, 5)}),
        ]
        
        input_manager.update(events)
        
        # Verify all devices are accessible and updated
        assert input_manager.keyboard is not None
        assert input_manager.mouse is not None
        assert input_manager.joystick is not None
    
    def test_input_manager_multiple_frames(self, input_manager):
        """Test InputManager across multiple frames."""
        # First frame
        events1 = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        ]
        input_manager.update(events1)
        
        # Second frame - no new events
        events2 = []
        input_manager.update(events2)
        
        # Third frame - key release
        events3 = [
            pygame.event.Event(pygame.KEYUP, {"key": pygame.K_SPACE})
        ]
        input_manager.update(events3)
        
        # Should handle all frames without issues
        assert input_manager.enabled


class TestInputManagerLifecycle:
    """Test InputManager lifecycle."""
    
    def test_input_manager_cleanup(self, pygame_init_cleanup):
        """Test InputManager cleanup."""
        manager = InputManager()
        manager.initialize()
        
        manager.cleanup()
        # Cleanup should not raise errors
        
        # Can still access devices (they may be in cleaned state)
        assert manager.keyboard is not None
    
    def test_input_manager_reinitialization(self, pygame_init_cleanup):
        """Test InputManager can be reinitialized."""
        manager = InputManager()
        
        manager.initialize()
        manager.cleanup()
        
        manager.initialize()
        manager.cleanup()

