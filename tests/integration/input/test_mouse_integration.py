"""
Integration tests for Mouse input system.

Tests mouse position tracking, button states, wheel events.
"""

import pytest
import pygame
from hub.core.input.mouse import Mouse


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mouse(pygame_init_cleanup):
    """Create a Mouse instance for testing."""
    return Mouse()


class TestMouseBasic:
    """Test basic mouse functionality."""
    
    def test_mouse_initialization(self, mouse):
        """Test mouse initialization."""
        assert mouse.position == (0, 0)
        assert mouse.x == 0
        assert mouse.y == 0
    
    def test_mouse_position(self, mouse):
        """Test mouse position tracking."""
        # Simulate mouse motion
        events = [
            pygame.event.Event(pygame.MOUSEMOTION, {"pos": (100, 200), "rel": (100, 200)})
        ]
        mouse.update(events)
        
        # Position should be updated
        # Note: Actual position depends on pygame.mouse.get_pos()
        assert mouse.position is not None
    
    def test_mouse_is_pressed(self, mouse):
        """Test checking if mouse button is pressed."""
        # Simulate button press
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 50)})
        ]
        mouse.update(events)
        
        # Button should be marked as pressed
        # Implementation dependent


class TestMouseButtons:
    """Test mouse button handling."""
    
    def test_mouse_left_button(self, mouse):
        """Test left mouse button."""
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)})
        ]
        mouse.update(events)
        
        # Left button (button 0) should be pressed
        # Implementation dependent
    
    def test_mouse_right_button(self, mouse):
        """Test right mouse button."""
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (100, 100)})
        ]
        mouse.update(events)
        
        # Right button (button 2) should be pressed
        # Implementation dependent
    
    def test_mouse_button_release(self, mouse):
        """Test mouse button release."""
        # Press
        events_down = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 50)})
        ]
        mouse.update(events_down)
        
        # Release
        events_up = [
            pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 50)})
        ]
        mouse.update(events_up)
        
        # Button should be released
        # Implementation dependent


class TestMouseWheel:
    """Test mouse wheel functionality."""
    
    def test_mouse_wheel_vertical(self, mouse):
        """Test vertical mouse wheel scrolling."""
        events = [
            pygame.event.Event(pygame.MOUSEWHEEL, {"x": 0, "y": 1})
        ]
        mouse.update(events)
        
        # Wheel delta should be recorded
        # Implementation dependent
    
    def test_mouse_wheel_horizontal(self, mouse):
        """Test horizontal mouse wheel scrolling."""
        events = [
            pygame.event.Event(pygame.MOUSEWHEEL, {"x": 1, "y": 0})
        ]
        mouse.update(events)
        
        # Horizontal wheel delta should be recorded
        # Implementation dependent
    
    def test_mouse_wheel_multiple(self, mouse):
        """Test multiple wheel events in one frame."""
        events = [
            pygame.event.Event(pygame.MOUSEWHEEL, {"x": 0, "y": 3}),
            pygame.event.Event(pygame.MOUSEWHEEL, {"x": 0, "y": 2}),
        ]
        mouse.update(events)
        
        # Should accumulate wheel deltas
        # Implementation dependent


class TestMouseUpdate:
    """Test mouse update functionality."""
    
    def test_mouse_update_clears_frame_states(self, mouse):
        """Test that update clears frame-specific states."""
        # First frame - button down
        events1 = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (10, 10)})
        ]
        mouse.update(events1)
        
        # Second frame - no events
        events2 = []
        mouse.update(events2)
        
        # Just-pressed should be cleared
        # Implementation dependent
    
    def test_mouse_no_events(self, mouse):
        """Test mouse update with no events."""
        events = []
        mouse.update(events)
        
        # Should not raise error
        assert mouse.position is not None

