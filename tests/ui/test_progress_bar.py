"""
Tests for ProgressBar component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.progress_bar import ProgressBar


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def progress_bar(pygame_init_cleanup):
    """Create a ProgressBar instance for testing."""
    return ProgressBar(x=100, y=100, width=200, height=20)


class TestProgressBarInitialization:
    """Test ProgressBar initialization."""
    
    def test_progress_bar_initialization(self, progress_bar):
        """Test ProgressBar initialization."""
        assert progress_bar.x == 100
        assert progress_bar.y == 100
        assert progress_bar.width == 200
        assert progress_bar.height == 20
        assert progress_bar.min_value == 0.0
        assert progress_bar.max_value == 100.0
        assert progress_bar.value == 0.0
    
    def test_progress_bar_with_initial_value(self, pygame_init_cleanup):
        """Test ProgressBar with initial value."""
        bar = ProgressBar(0, 0, 200, 20, initial_value=50.0)
        assert bar.value == 50.0
    
    def test_progress_bar_custom_range(self, pygame_init_cleanup):
        """Test ProgressBar with custom value range."""
        bar = ProgressBar(0, 0, 200, 20, min_value=0.0, max_value=200.0)
        assert bar.min_value == 0.0
        assert bar.max_value == 200.0
    
    def test_progress_bar_show_percentage(self, pygame_init_cleanup):
        """Test ProgressBar with percentage display."""
        bar = ProgressBar(0, 0, 200, 20, show_percentage=True)
        assert bar.show_percentage == True


class TestProgressBarValue:
    """Test progress bar value handling."""
    
    def test_progress_bar_set_value(self, progress_bar):
        """Test setting progress bar value."""
        progress_bar.value = 50.0
        assert progress_bar.value == 50.0
    
    def test_progress_bar_value_clamped_to_min(self, progress_bar):
        """Test value is clamped to minimum."""
        progress_bar.value = -10.0
        assert progress_bar.value == 0.0
    
    def test_progress_bar_value_clamped_to_max(self, progress_bar):
        """Test value is clamped to maximum."""
        progress_bar.value = 150.0
        assert progress_bar.value == 100.0
    
    def test_progress_bar_normalized_progress(self, progress_bar):
        """Test normalized progress calculation."""
        progress_bar.value = 0.0
        assert progress_bar.normalized_progress == pytest.approx(0.0)
        
        progress_bar.value = 50.0
        assert progress_bar.normalized_progress == pytest.approx(0.5)
        
        progress_bar.value = 100.0
        assert progress_bar.normalized_progress == pytest.approx(1.0)
    
    def test_progress_bar_increment(self, progress_bar):
        """Test incrementing progress."""
        progress_bar.value = 0.0
        progress_bar.increment(25.0)
        assert progress_bar.value == 25.0
        
        progress_bar.increment(25.0)
        assert progress_bar.value == 50.0
    
    def test_progress_bar_increment_clamped(self, progress_bar):
        """Test increment respects max value."""
        progress_bar.value = 90.0
        progress_bar.increment(20.0)
        assert progress_bar.value == 100.0  # Clamped
    
    def test_progress_bar_decrement(self, progress_bar):
        """Test decrementing progress."""
        progress_bar.value = 100.0
        progress_bar.decrement(25.0)
        assert progress_bar.value == 75.0
        
        progress_bar.decrement(25.0)
        assert progress_bar.value == 50.0
    
    def test_progress_bar_decrement_clamped(self, progress_bar):
        """Test decrement respects min value."""
        progress_bar.value = 10.0
        progress_bar.decrement(20.0)
        assert progress_bar.value == 0.0  # Clamped


class TestProgressBarVisual:
    """Test progress bar visual representation."""
    
    def test_progress_bar_empty(self, progress_bar, pygame_init_cleanup):
        """Test rendering empty progress bar."""
        progress_bar.value = 0.0
        surface = pygame.Surface((400, 300))
        
        progress_bar.render(surface)
        
        # Should not raise error
        assert True
    
    def test_progress_bar_full(self, progress_bar, pygame_init_cleanup):
        """Test rendering full progress bar."""
        progress_bar.value = 100.0
        surface = pygame.Surface((400, 300))
        
        progress_bar.render(surface)
        
        # Should not raise error
        assert True
    
    def test_progress_bar_partial(self, progress_bar, pygame_init_cleanup):
        """Test rendering partial progress bar."""
        progress_bar.value = 75.0
        surface = pygame.Surface((400, 300))
        
        progress_bar.render(surface)
        
        # Should not raise error
        assert True
    
    def test_progress_bar_fill_width(self, progress_bar):
        """Test fill width calculation."""
        progress_bar.value = 50.0
        # Fill width should be 50% of total width
        expected_fill = int(progress_bar.width * 0.5)
        assert progress_bar.fill_width == expected_fill
    
    def test_progress_bar_orientation_vertical(self, pygame_init_cleanup):
        """Test vertical progress bar."""
        bar = ProgressBar(0, 0, 20, 200, vertical=True)
        assert bar.vertical == True
        
        bar.value = 50.0
        # For vertical, fill height should be calculated
        assert bar.fill_height > 0


class TestProgressBarColors:
    """Test progress bar color customization."""
    
    def test_progress_bar_custom_colors(self, pygame_init_cleanup):
        """Test progress bar with custom colors."""
        bar = ProgressBar(
            0, 0, 200, 20,
            background_color=(255, 0, 0),
            fill_color=(0, 255, 0)
        )
        assert bar.background_color == (255, 0, 0)
        assert bar.fill_color == (0, 255, 0)
    
    def test_progress_bar_color_gradient(self, pygame_init_cleanup):
        """Test progress bar with color gradient based on value."""
        bar = ProgressBar(0, 0, 200, 20, use_gradient=True)
        bar.value = 25.0  # Low - should be one color
        color_low = bar.get_current_fill_color()
        
        bar.value = 75.0  # High - should be different color
        color_high = bar.get_current_fill_color()
        
        # Colors should be different (implementation dependent)
        assert color_low is not None
        assert color_high is not None


class TestProgressBarAnimation:
    """Test progress bar animation."""
    
    def test_progress_bar_animated_update(self, progress_bar):
        """Test animated progress update."""
        progress_bar.value = 0.0
        progress_bar.set_value_animated(100.0, duration=1.0)
        
        # After some time, value should be increasing
        progress_bar.update(0.5, (0, 0), False)
        
        # Value should have changed (not at 0 or 100)
        assert 0.0 < progress_bar.value < 100.0
    
    def test_progress_bar_animated_complete(self, progress_bar):
        """Test animated progress completes."""
        progress_bar.value = 0.0
        progress_bar.set_value_animated(100.0, duration=1.0)
        
        # Complete animation
        progress_bar.update(1.0, (0, 0), False)
        
        # Should be at target value
        assert progress_bar.value == pytest.approx(100.0, abs=1.0)


class TestProgressBarText:
    """Test progress bar text display."""
    
    def test_progress_bar_show_percentage_text(self, pygame_init_cleanup):
        """Test percentage text display."""
        bar = ProgressBar(0, 0, 200, 20, show_percentage=True)
        bar.value = 75.0
        
        # Should have percentage text
        assert bar.show_percentage == True
    
    def test_progress_bar_custom_label(self, pygame_init_cleanup):
        """Test custom label text."""
        bar = ProgressBar(0, 0, 200, 20, label="Loading...")
        assert bar.label == "Loading..."


class TestProgressBarEdgeCases:
    """Test progress bar edge cases."""
    
    def test_progress_bar_zero_range(self, pygame_init_cleanup):
        """Test progress bar with zero range."""
        bar = ProgressBar(0, 0, 200, 20, min_value=50.0, max_value=50.0)
        assert bar.value == 50.0
        assert bar.normalized_progress == pytest.approx(0.5)  # Or 0.0/1.0
    
    def test_progress_bar_negative_range(self, pygame_init_cleanup):
        """Test progress bar with negative range."""
        bar = ProgressBar(0, 0, 200, 20, min_value=-100.0, max_value=100.0)
        bar.value = 0.0
        assert bar.normalized_progress == pytest.approx(0.5)  # Midpoint


class TestProgressBarIntegration:
    """Integration tests for progress bar."""
    
    def test_progress_bar_with_animation_framework(self, progress_bar):
        """Test progress bar integrates with animation framework."""
        from hub.ui.animation import AnimationManager
        
        manager = AnimationManager()
        
        # Animate progress from 0 to 100
        progress_bar.set_value_animated(100.0, duration=1.0)
        
        # Update via animation manager (if integrated)
        # This test defines expected integration behavior
        
        assert progress_bar.value >= 0.0
    
    def test_progress_bar_multiple_bars(self, pygame_init_cleanup):
        """Test multiple progress bars work independently."""
        bar1 = ProgressBar(0, 0, 200, 20)
        bar2 = ProgressBar(0, 30, 200, 20)
        
        bar1.value = 50.0
        bar2.value = 75.0
        
        assert bar1.value == 50.0
        assert bar2.value == 75.0
        assert bar1.value != bar2.value

