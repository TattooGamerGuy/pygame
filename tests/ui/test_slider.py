"""
Tests for Slider component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.slider import Slider


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def slider(pygame_init_cleanup):
    """Create a Slider instance for testing."""
    return Slider(x=100, y=100, width=200, height=20, min_value=0.0, max_value=100.0)


class TestSliderInitialization:
    """Test Slider initialization."""
    
    def test_slider_initialization(self, slider):
        """Test Slider initialization."""
        assert slider.x == 100
        assert slider.y == 100
        assert slider.width == 200
        assert slider.height == 20
        assert slider.min_value == 0.0
        assert slider.max_value == 100.0
        assert slider.value == 50.0  # Default should be middle
    
    def test_slider_with_initial_value(self, pygame_init_cleanup):
        """Test Slider with initial value."""
        slider = Slider(0, 0, 200, 20, 0.0, 100.0, initial_value=25.0)
        assert slider.value == 25.0
    
    def test_slider_vertical(self, pygame_init_cleanup):
        """Test vertical slider."""
        slider = Slider(0, 0, 20, 200, 0.0, 100.0, vertical=True)
        assert slider.vertical == True
    
    def test_slider_step(self, pygame_init_cleanup):
        """Test slider with step value."""
        slider = Slider(0, 0, 200, 20, 0.0, 100.0, step=10.0)
        assert slider.step == 10.0


class TestSliderValue:
    """Test slider value handling."""
    
    def test_slider_set_value(self, slider):
        """Test setting slider value."""
        slider.value = 75.0
        assert slider.value == 75.0
    
    def test_slider_value_clamped_to_min(self, slider):
        """Test value is clamped to minimum."""
        slider.value = -10.0
        assert slider.value == 0.0
    
    def test_slider_value_clamped_to_max(self, slider):
        """Test value is clamped to maximum."""
        slider.value = 150.0
        assert slider.value == 100.0
    
    def test_slider_value_with_step(self, pygame_init_cleanup):
        """Test value snaps to step."""
        slider = Slider(0, 0, 200, 20, 0.0, 100.0, step=10.0)
        slider.value = 23.0
        # Should snap to nearest step (20.0 or 30.0)
        assert slider.value in [20.0, 30.0]


class TestSliderInteraction:
    """Test slider user interaction."""
    
    def test_slider_click_to_set_value(self, slider):
        """Test clicking slider sets value."""
        # Click at 75% of slider width (should set value to ~75)
        click_x = slider.x + int(slider.width * 0.75)
        click_y = slider.y + slider.height // 2
        
        slider.handle_click((click_x, click_y))
        
        # Value should be approximately 75
        assert 70.0 <= slider.value <= 80.0
    
    def test_slider_drag(self, slider):
        """Test dragging slider."""
        slider.focus()
        
        # Start drag
        slider.handle_mouse_down((slider.x + 50, slider.y + 10))
        
        # Drag to different position
        slider.handle_mouse_drag((slider.x + 150, slider.y + 10))
        
        # Value should have changed
        assert slider.value > 50.0
    
    def test_slider_drag_limits(self, slider):
        """Test drag respects min/max limits."""
        slider.value = 0.0
        slider.focus()
        slider.handle_mouse_down((slider.x, slider.y + 10))
        
        # Drag to negative position
        slider.handle_mouse_drag((slider.x - 50, slider.y + 10))
        
        # Should stay at minimum
        assert slider.value == 0.0


class TestSliderCallbacks:
    """Test slider callbacks."""
    
    def test_slider_on_change_callback(self, slider):
        """Test on_change callback."""
        callback_called = [False]
        new_value = [None]
        
        def on_change(value):
            callback_called[0] = True
            new_value[0] = value
        
        slider.on_change = on_change
        slider.value = 75.0
        
        assert callback_called[0]
        assert new_value[0] == 75.0
    
    def test_slider_on_change_not_called_if_same(self, slider):
        """Test on_change not called if value unchanged."""
        callback_count = [0]
        
        def on_change(value):
            callback_count[0] += 1
        
        slider.on_change = on_change
        
        # Set different value first to ensure callback is registered
        slider.value = 25.0
        initial_count = callback_count[0]
        
        # Set same value again
        slider.value = 25.0
        
        # Should not increment callback count
        assert callback_count[0] == initial_count


class TestSliderVisual:
    """Test slider visual representation."""
    
    def test_slider_normalized_value(self, slider):
        """Test normalized value (0.0 to 1.0)."""
        slider.value = 0.0
        assert slider.normalized_value == pytest.approx(0.0)
        
        slider.value = 50.0
        assert slider.normalized_value == pytest.approx(0.5)
        
        slider.value = 100.0
        assert slider.normalized_value == pytest.approx(1.0)
    
    def test_slider_handle_position(self, slider):
        """Test handle position calculation."""
        slider.value = 0.0
        handle_pos_0 = slider.handle_position
        
        slider.value = 100.0
        handle_pos_100 = slider.handle_position
        
        # Handle should move from left to right
        assert handle_pos_100 > handle_pos_0


class TestSliderVertical:
    """Test vertical slider."""
    
    def test_slider_vertical_value(self, pygame_init_cleanup):
        """Test vertical slider value interaction."""
        slider = Slider(0, 0, 20, 200, 0.0, 100.0, vertical=True)
        
        # Click at top (should be max)
        slider.handle_click((10, 0))
        assert slider.value == pytest.approx(100.0)
        
        # Click at bottom (should be min) - use y=199 to ensure it's within bounds
        slider.handle_click((10, 199))
        assert slider.value == pytest.approx(0.0)


class TestSliderEdgeCases:
    """Test slider edge cases."""
    
    def test_slider_same_min_max(self, pygame_init_cleanup):
        """Test slider with same min and max."""
        slider = Slider(0, 0, 200, 20, 50.0, 50.0)
        assert slider.value == 50.0
        
        slider.value = 60.0
        assert slider.value == 50.0  # Should be clamped
    
    def test_slider_reversed_range(self, pygame_init_cleanup):
        """Test slider with reversed range (max < min)."""
        # Should handle gracefully or swap
        slider = Slider(0, 0, 200, 20, 100.0, 0.0)
        # Implementation may swap or handle differently
        assert slider.min_value <= slider.max_value  # Or swapped
    

