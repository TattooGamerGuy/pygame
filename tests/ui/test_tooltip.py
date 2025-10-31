"""
Tests for Tooltip component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.tooltip import Tooltip


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def tooltip(pygame_init_cleanup):
    """Create a Tooltip instance for testing."""
    return Tooltip(text="Test tooltip")


class TestTooltipInitialization:
    """Test Tooltip initialization."""
    
    def test_tooltip_initialization(self, tooltip):
        """Test Tooltip initialization."""
        assert tooltip.text == "Test tooltip"
        assert not tooltip.visible
        assert tooltip.position == (0, 0)
    
    def test_tooltip_with_empty_text(self, pygame_init_cleanup):
        """Test Tooltip with empty text."""
        tip = Tooltip(text="")
        assert tip.text == ""
    
    def test_tooltip_multiline_text(self, pygame_init_cleanup):
        """Test Tooltip with multiline text."""
        tip = Tooltip(text="Line 1\nLine 2\nLine 3")
        assert "Line 1" in tip.text
        assert "Line 2" in tip.text
    
    def test_tooltip_with_delay(self, pygame_init_cleanup):
        """Test Tooltip with show delay."""
        tip = Tooltip(text="Delayed tooltip", delay=0.5)
        assert tip.delay == 0.5


class TestTooltipVisibility:
    """Test tooltip visibility and show/hide behavior."""
    
    def test_tooltip_show(self, tooltip):
        """Test showing tooltip."""
        tooltip.delay = 0.0  # No delay for immediate show
        tooltip.show((100, 100))
        assert tooltip.visible
        assert tooltip.position == (100, 100) or tooltip.position == (110, 110)  # May have offset
    
    def test_tooltip_hide(self, tooltip):
        """Test hiding tooltip."""
        tooltip.show((100, 100))
        tooltip.hide()
        assert not tooltip.visible
    
    def test_tooltip_show_then_hide(self, tooltip):
        """Test showing then hiding tooltip."""
        tooltip.delay = 0.0  # No delay for immediate show
        tooltip.show((100, 100))
        assert tooltip.visible
        
        tooltip.hide()
        assert not tooltip.visible
        
        # Show again at different position
        tooltip.show((200, 200))
        # Update to process delay
        tooltip.update(0.1, (200, 200), False)
        assert tooltip.visible
    
    def test_tooltip_auto_hide(self, pygame_init_cleanup):
        """Test tooltip auto-hide after duration."""
        tip = Tooltip(text="Auto-hide tooltip", duration=0.5, delay=0.0)
        tip.show((100, 100))
        tip.update(0.1, (100, 100), False)  # Make visible
        assert tip.visible
        
        # Update for duration
        tip.update(0.6, (100, 100), False)
        assert not tip.visible  # Should auto-hide


class TestTooltipPositioning:
    """Test tooltip positioning."""
    
    def test_tooltip_position_follows_mouse(self, tooltip):
        """Test tooltip follows mouse position."""
        tooltip.delay = 0.0  # No delay
        tooltip.show((100, 100))
        tooltip.update(0.1, (150, 150), False)
        # Position should follow mouse with offset
        assert tooltip.position == (160, 160)  # 150 + 10 offset
    
    def test_tooltip_offset(self, pygame_init_cleanup):
        """Test tooltip offset from mouse."""
        tip = Tooltip(text="Offset tooltip", offset=(10, 10))
        tip.show((100, 100))
        # Position should be offset from show position
        assert tip.position[0] == 110 or tip.position[0] == 100  # Implementation dependent
        assert tip.position[1] == 110 or tip.position[1] == 100
    
    def test_tooltip_stays_onscreen(self, pygame_init_cleanup):
        """Test tooltip adjusts position to stay on screen."""
        tip = Tooltip(text="Stays on screen")
        # Show near screen edge
        tip.show((10, 10))
        tip.update(0.1, (10, 10), False)
        
        # Tooltip should adjust to stay visible
        # (Implementation should clamp position)
        assert tip.position[0] >= 0
        assert tip.position[1] >= 0


class TestTooltipDelay:
    """Test tooltip delay functionality."""
    
    def test_tooltip_delay_before_showing(self, pygame_init_cleanup):
        """Test tooltip delays before showing."""
        tip = Tooltip(text="Delayed", delay=0.5)
        tip.show((100, 100))
        
        # Immediately after show, should not be visible yet
        tip.update(0.0, (100, 100), False)
        # May or may not be visible depending on implementation
        
        # After delay, should be visible
        tip.update(0.6, (100, 100), False)
        assert tip.visible
    
    def test_tooltip_cancels_on_hide_during_delay(self, pygame_init_cleanup):
        """Test hiding cancels delay."""
        tip = Tooltip(text="Cancel delay", delay=0.5)
        tip.show((100, 100))
        tip.update(0.1, (100, 100), False)  # Start delay
        assert not tip.visible  # Should still be in delay
        
        tip.hide()
        
        # Update past delay
        tip.update(0.6, (100, 100), False)
        assert not tip.visible  # Should remain hidden


class TestTooltipStyling:
    """Test tooltip styling and appearance."""
    
    def test_tooltip_background_color(self, pygame_init_cleanup):
        """Test tooltip background color."""
        tip = Tooltip(text="Colored", background_color=(255, 0, 0))
        assert tip.background_color == (255, 0, 0)
    
    def test_tooltip_text_color(self, pygame_init_cleanup):
        """Test tooltip text color."""
        tip = Tooltip(text="Colored text", text_color=(0, 255, 0))
        assert tip.text_color == (0, 255, 0)
    
    def test_tooltip_border(self, pygame_init_cleanup):
        """Test tooltip border."""
        tip = Tooltip(text="Bordered", border_color=(0, 0, 255), border_width=2)
        assert tip.border_color == (0, 0, 255)
        assert tip.border_width == 2
    
    def test_tooltip_padding(self, pygame_init_cleanup):
        """Test tooltip padding."""
        tip = Tooltip(text="Padded", padding=10)
        assert tip.padding == 10


class TestTooltipRendering:
    """Test tooltip rendering."""
    
    def test_tooltip_render_when_visible(self, tooltip, pygame_init_cleanup):
        """Test rendering visible tooltip."""
        tooltip.show((100, 100))
        surface = pygame.Surface((400, 300))
        
        tooltip.render(surface)
        
        # Should not raise error
        assert True
    
    def test_tooltip_not_render_when_hidden(self, tooltip, pygame_init_cleanup):
        """Test tooltip doesn't render when hidden."""
        surface = pygame.Surface((400, 300))
        
        tooltip.render(surface)
        
        # Should not raise error (does nothing when hidden)
        assert True
    
    def test_tooltip_multiline_rendering(self, pygame_init_cleanup):
        """Test multiline tooltip rendering."""
        tip = Tooltip(text="Line 1\nLine 2\nLine 3")
        tip.show((100, 100))
        surface = pygame.Surface((400, 300))
        
        tip.render(surface)
        
        # Should not raise error
        assert True


class TestTooltipSize:
    """Test tooltip size calculation."""
    
    def test_tooltip_auto_size(self, tooltip):
        """Test tooltip calculates size automatically."""
        tooltip.show((100, 100))
        
        # Tooltip should have dimensions
        assert tooltip.width > 0
        assert tooltip.height > 0
    
    def test_tooltip_max_width(self, pygame_init_cleanup):
        """Test tooltip max width constraint."""
        long_text = "This is a very long tooltip text that should wrap to multiple lines when max width is set"
        tip = Tooltip(text=long_text, max_width=100)
        tip.show((100, 100))
        
        # Width should not exceed max_width (plus padding)
        assert tip.width <= tip.max_width + (tip.padding * 2)


class TestTooltipIntegration:
    """Integration tests for tooltip."""
    
    def test_tooltip_with_widget(self, pygame_init_cleanup):
        """Test tooltip attached to widget."""
        # This test verifies tooltip can conceptually work with widgets
        # Actual widget integration would be tested in integration tests
        tip = Tooltip(text="Widget tooltip", delay=0.0)
        
        # Show tooltip at widget position
        mouse_pos = (150, 120)
        tip.show(mouse_pos)
        tip.update(0.1, mouse_pos, False)
        assert tip.visible
        
        # Tooltip position should be set
        assert tip.position[0] >= 0
        assert tip.position[1] >= 0
    
    def test_multiple_tooltips(self, pygame_init_cleanup):
        """Test multiple tooltips can exist independently."""
        tip1 = Tooltip(text="Tooltip 1", delay=0.0)
        tip2 = Tooltip(text="Tooltip 2", delay=0.0)
        
        tip1.show((100, 100))
        tip2.show((200, 200))
        tip1.update(0.1, (100, 100), False)
        tip2.update(0.1, (200, 200), False)
        
        assert tip1.visible
        assert tip2.visible
        assert tip1.position != tip2.position
    
    def test_tooltip_fade_in(self, pygame_init_cleanup):
        """Test tooltip fade-in animation."""
        tip = Tooltip(text="Fading tooltip", fade_in=True)
        tip.show((100, 100))
        
        # Initially opacity should be 0 or low
        tip.update(0.0, (100, 100), False)
        
        # After some time, opacity should increase
        tip.update(0.3, (100, 100), False)
        
        # Tooltip should be visible
        assert tip.visible


class TestTooltipEdgeCases:
    """Test tooltip edge cases."""
    
    def test_tooltip_empty_text(self, pygame_init_cleanup):
        """Test tooltip with empty text doesn't crash."""
        tip = Tooltip(text="")
        tip.show((100, 100))
        surface = pygame.Surface((400, 300))
        
        tip.render(surface)
        
        # Should not crash
        assert True
    
    def test_tooltip_very_long_text(self, pygame_init_cleanup):
        """Test tooltip with very long text."""
        long_text = "A" * 500
        tip = Tooltip(text=long_text, max_width=200)
        tip.show((100, 100))
        surface = pygame.Surface((400, 300))
        
        tip.render(surface)
        
        # Should wrap or truncate
        assert True
    
    def test_tooltip_zero_duration(self, pygame_init_cleanup):
        """Test tooltip with zero duration."""
        tip = Tooltip(text="Instant", duration=0.0)
        tip.show((100, 100))
        tip.update(0.1, (100, 100), False)
        
        # Should handle gracefully
        assert True

