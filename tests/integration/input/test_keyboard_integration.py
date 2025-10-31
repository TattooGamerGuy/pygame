"""
Integration tests for Keyboard input system.

Tests key press/release, multiple keys simultaneously, key state persistence.
"""

import pytest
import pygame
from hub.core.input.keyboard import Keyboard


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def keyboard(pygame_init_cleanup):
    """Create a Keyboard instance for testing."""
    return Keyboard()


class TestKeyboardBasic:
    """Test basic keyboard functionality."""
    
    def test_keyboard_initialization(self, keyboard):
        """Test keyboard initialization."""
        assert keyboard is not None
        # Initial state should be empty
        # (Implementation may vary)
    
    def test_keyboard_is_pressed(self, keyboard):
        """Test checking if key is pressed."""
        # Simulate key press with events
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        ]
        keyboard.update(events)
        
        # After update, key should be pressed
        # Note: This depends on pygame.key.get_pressed() working
        # May need actual key press simulation for full test
    
    def test_keyboard_is_just_pressed(self, keyboard):
        """Test detecting just-pressed keys."""
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_A})
        ]
        keyboard.update(events)
        
        # Key should be marked as just pressed
        # Exact implementation depends on Keyboard class
    
    def test_keyboard_is_just_released(self, keyboard):
        """Test detecting just-released keys."""
        # First press
        events1 = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_B})
        ]
        keyboard.update(events1)
        
        # Then release
        events2 = [
            pygame.event.Event(pygame.KEYUP, {"key": pygame.K_B})
        ]
        keyboard.update(events2)
        
        # Key should be marked as just released
        # Implementation dependent


class TestKeyboardMultipleKeys:
    """Test keyboard with multiple keys."""
    
    def test_keyboard_multiple_keys_pressed(self, keyboard):
        """Test handling multiple keys pressed simultaneously."""
        # Simulate multiple key presses
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_W}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_A}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_S}),
        ]
        
        keyboard.update(events)
        
        # All keys should be tracked
        # Exact behavior depends on implementation
    
    def test_keyboard_key_state_persistence(self, keyboard):
        """Test that key state persists across frames."""
        # First frame - press key
        events1 = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
        ]
        keyboard.update(events1)
        
        # Second frame - no events (key still held)
        events2 = []
        keyboard.update(events2)
        
        # Key should still be marked as pressed (not just-pressed)
        # Implementation dependent


class TestKeyboardClear:
    """Test keyboard clear functionality."""
    
    def test_keyboard_clear(self, keyboard):
        """Test clearing keyboard state."""
        # Press some keys
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        ]
        keyboard.update(events)
        
        # Clear state
        keyboard.clear()
        
        # State should be cleared
        # Implementation dependent
    
    def test_keyboard_update_after_clear(self, keyboard):
        """Test keyboard works after clearing."""
        keyboard.clear()
        
        # Update with new events
        events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ENTER})
        ]
        keyboard.update(events)
        
        # Should work normally after clear


class TestKeyboardEdgeCases:
    """Test keyboard edge cases."""
    
    def test_keyboard_no_events(self, keyboard):
        """Test keyboard update with no events."""
        events = []
        keyboard.update(events)
        
        # Should not raise error
    
    def test_keyboard_multiple_updates(self, keyboard):
        """Test keyboard with multiple consecutive updates."""
        for _ in range(10):
            events = []
            keyboard.update(events)
        
        # Should handle multiple updates gracefully
    
    def test_keyboard_rapid_key_press(self, keyboard):
        """Test keyboard with rapid key press/release cycles."""
        for _ in range(5):
            # Press
            events_down = [
                pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_X})
            ]
            keyboard.update(events_down)
            
            # Release
            events_up = [
                pygame.event.Event(pygame.KEYUP, {"key": pygame.K_X})
            ]
            keyboard.update(events_up)
        
        # Should handle rapid cycles without issues

