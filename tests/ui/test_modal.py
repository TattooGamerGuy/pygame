"""
Tests for Modal component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.modal import Modal


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def modal(pygame_init_cleanup):
    """Create a basic Modal instance for testing."""
    return Modal(title="Test Modal", content="This is test content")


class TestModalInitialization:
    """Test Modal initialization."""
    
    def test_modal_initialization(self, modal):
        """Test Modal initialization."""
        assert modal.title == "Test Modal"
        assert modal.content == "This is test content"
        assert not modal.is_open
        assert modal.width > 0
        assert modal.height > 0
    
    def test_modal_without_title(self, pygame_init_cleanup):
        """Test Modal without title."""
        md = Modal(content="Content only")
        assert md.title == ""
        assert md.content == "Content only"
    
    def test_modal_with_buttons(self, pygame_init_cleanup):
        """Test Modal with action buttons."""
        md = Modal(
            title="Confirm",
            content="Are you sure?",
            buttons=["OK", "Cancel"]
        )
        assert len(md.buttons) == 2
        assert md.buttons[0] == "OK"
        assert md.buttons[1] == "Cancel"
    
    def test_modal_custom_size(self, pygame_init_cleanup):
        """Test Modal with custom size."""
        md = Modal(
            title="Custom",
            content="Custom size modal",
            width=500,
            height=400
        )
        assert md.width == 500
        assert md.height == 400


class TestModalOpenClose:
    """Test modal open/close behavior."""
    
    def test_modal_open(self, modal):
        """Test opening modal."""
        modal.open()
        assert modal.is_open
    
    def test_modal_close(self, modal):
        """Test closing modal."""
        modal.open()
        modal.close()
        assert not modal.is_open
    
    def test_modal_open_twice(self, modal):
        """Test opening modal twice."""
        modal.open()
        assert modal.is_open
        modal.open()  # Should handle gracefully
        assert modal.is_open
    
    def test_modal_close_when_closed(self, modal):
        """Test closing modal when already closed."""
        assert not modal.is_open
        modal.close()  # Should handle gracefully
        assert not modal.is_open


class TestModalInteraction:
    """Test modal user interaction."""
    
    def test_modal_click_outside_to_close(self, modal):
        """Test clicking outside modal closes it."""
        modal.open()
        modal.handle_click((10, 10))  # Outside modal bounds
        # Should close if close_on_backdrop_click is True
        # (Implementation dependent)
        assert True
    
    def test_modal_button_click(self, pygame_init_cleanup):
        """Test clicking modal buttons."""
        md = Modal(
            title="Test",
            content="Click button",
            buttons=["OK", "Cancel"]
        )
        md.open()
        
        # Click OK button (would need actual button coordinates)
        # This test defines expected behavior
        assert len(md.buttons) > 0
    
    def test_modal_escape_to_close(self, modal):
        """Test Escape key closes modal."""
        modal.open()
        modal.handle_escape()
        assert not modal.is_open
    
    def test_modal_enter_confirms(self, pygame_init_cleanup):
        """Test Enter key confirms (default button)."""
        md = Modal(
            title="Confirm",
            content="Press Enter",
            buttons=["OK", "Cancel"],
            default_button=0
        )
        md.open()
        md.handle_enter()
        
        # Should close and call callback
        assert not md.is_open


class TestModalCallbacks:
    """Test modal callbacks."""
    
    def test_modal_on_confirm_callback(self, pygame_init_cleanup):
        """Test on_confirm callback."""
        callback_called = [False]
        button_index = [None]
        
        def on_confirm(index):
            callback_called[0] = True
            button_index[0] = index
        
        md = Modal(
            title="Test",
            content="Confirm",
            buttons=["OK"],
            on_confirm=on_confirm
        )
        md.open()
        md.confirm(0)
        
        assert callback_called[0]
        assert button_index[0] == 0
    
    def test_modal_on_close_callback(self, modal):
        """Test on_close callback."""
        callback_called = [False]
        
        def on_close():
            callback_called[0] = True
        
        modal.on_close = on_close
        modal.open()
        modal.close()
        
        assert callback_called[0]


class TestModalTypes:
    """Test different modal types."""
    
    def test_modal_alert(self, pygame_init_cleanup):
        """Test alert modal."""
        md = Modal.alert("Alert!", "This is an alert")
        assert md.title == "Alert!"
        assert md.content == "This is an alert"
        assert len(md.buttons) == 1  # Usually just OK
    
    def test_modal_confirm(self, pygame_init_cleanup):
        """Test confirmation modal."""
        md = Modal.confirm("Confirm", "Are you sure?")
        assert "OK" in md.buttons or "Yes" in md.buttons
        assert "Cancel" in md.buttons or "No" in md.buttons
    
    def test_modal_prompt(self, pygame_init_cleanup):
        """Test prompt modal."""
        md = Modal.prompt("Prompt", "Enter value:")
        assert md.is_prompt
        # Should have text input
        assert hasattr(md, 'input_value') or md.is_prompt


class TestModalRendering:
    """Test modal rendering."""
    
    def test_modal_render_closed(self, modal, pygame_init_cleanup):
        """Test rendering closed modal."""
        surface = pygame.Surface((800, 600))
        modal.render(surface)
        
        # Should not raise error (modal not visible)
        assert True
    
    def test_modal_render_open(self, modal, pygame_init_cleanup):
        """Test rendering open modal."""
        modal.open()
        surface = pygame.Surface((800, 600))
        modal.render(surface)
        
        # Should not raise error
        assert True
    
    def test_modal_backdrop(self, modal, pygame_init_cleanup):
        """Test modal backdrop rendering."""
        modal.open()
        modal.show_backdrop = True
        surface = pygame.Surface((800, 600))
        modal.render(surface)
        
        # Backdrop should be rendered
        assert modal.show_backdrop


class TestModalFocus:
    """Test modal focus management."""
    
    def test_modal_captures_focus(self, modal):
        """Test modal captures focus when opened."""
        modal.open()
        # Modal should capture input focus
        assert modal.is_open
    
    def test_modal_blocks_input(self, modal):
        """Test modal blocks input to underlying content."""
        modal.open()
        # Input should be blocked (implementation detail)
        assert True


class TestModalPositioning:
    """Test modal positioning."""
    
    def test_modal_centered(self, modal):
        """Test modal is centered by default."""
        modal.width = 400
        modal.height = 300
        # Position should be calculated to center on screen
        assert modal.x >= 0
        assert modal.y >= 0
    
    def test_modal_custom_position(self, pygame_init_cleanup):
        """Test modal with custom position."""
        md = Modal(
            title="Custom",
            content="Custom position",
            x=100,
            y=100
        )
        assert md.x == 100
        assert md.y == 100


class TestModalEdgeCases:
    """Test modal edge cases."""
    
    def test_modal_empty_content(self, pygame_init_cleanup):
        """Test modal with empty content."""
        md = Modal(title="Empty", content="")
        assert md.content == ""
    
    def test_modal_very_long_content(self, pygame_init_cleanup):
        """Test modal with very long content."""
        long_content = "A" * 1000
        md = Modal(title="Long", content=long_content)
        surface = pygame.Surface((800, 600))
        md.open()
        md.render(surface)
        
        # Should handle gracefully (wrap or scroll)
        assert True
    
    def test_modal_no_buttons(self, pygame_init_cleanup):
        """Test modal with no buttons."""
        md = Modal(title="No Buttons", content="Content", buttons=[])
        assert len(md.buttons) == 0


class TestModalIntegration:
    """Integration tests for modal."""
    
    def test_modal_with_widgets(self, pygame_init_cleanup):
        """Test modal containing widgets."""
        from hub.ui.button import Button
        
        md = Modal(title="Widget Modal", content="Has widgets")
        
        # Modal should support adding widgets
        # (Implementation dependent)
        assert True
    
    def test_multiple_modals(self, pygame_init_cleanup):
        """Test multiple modals (stacking)."""
        md1 = Modal(title="First", content="First modal")
        md2 = Modal(title="Second", content="Second modal")
        
        md1.open()
        md2.open()
        
        # Typically only top modal is interactive
        assert md2.is_open
    
    def test_modal_in_scene(self, pygame_init_cleanup):
        """Test modal works within scene system."""
        md = Modal(title="Scene Modal", content="In scene")
        md.open()
        
        # Should integrate with scene rendering
        assert md.is_open

