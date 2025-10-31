"""
Tests for TextInput component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.text_input import TextInput


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def text_input(pygame_init_cleanup):
    """Create a TextInput instance for testing."""
    return TextInput(x=100, y=100, width=200, height=40)


class TestTextInputInitialization:
    """Test TextInput initialization."""
    
    def test_text_input_initialization(self, text_input):
        """Test TextInput initialization."""
        assert text_input.x == 100
        assert text_input.y == 100
        assert text_input.width == 200
        assert text_input.height == 40
        assert text_input.text == ""
        assert text_input.placeholder == ""
        assert not text_input.is_focused
    
    def test_text_input_with_initial_text(self, pygame_init_cleanup):
        """Test TextInput with initial text."""
        input_field = TextInput(0, 0, 200, 40, initial_text="Hello")
        assert input_field.text == "Hello"
    
    def test_text_input_with_placeholder(self, pygame_init_cleanup):
        """Test TextInput with placeholder text."""
        input_field = TextInput(0, 0, 200, 40, placeholder="Enter text...")
        assert input_field.placeholder == "Enter text..."


class TestTextInputFocus:
    """Test TextInput focus behavior."""
    
    def test_text_input_focus(self, text_input):
        """Test focusing a text input."""
        text_input.focus()
        assert text_input.is_focused
    
    def test_text_input_unfocus(self, text_input):
        """Test unfocusing a text input."""
        text_input.focus()
        text_input.unfocus()
        assert not text_input.is_focused
    
    def test_text_input_click_to_focus(self, text_input):
        """Test that clicking focuses the input."""
        # Simulate click inside bounds
        text_input.handle_click((150, 120))
        assert text_input.is_focused
    
    def test_text_input_click_outside_unfocus(self, text_input):
        """Test that clicking outside unfocuses."""
        text_input.focus()
        # Click outside
        text_input.handle_click((50, 50))
        assert not text_input.is_focused


class TestTextInputTextEntry:
    """Test text entry functionality."""
    
    def test_text_input_enter_text(self, text_input):
        """Test entering text."""
        text_input.focus()
        text_input.handle_key('a')
        assert text_input.text == "a"
        
        text_input.handle_key('b')
        text_input.handle_key('c')
        assert text_input.text == "abc"
    
    def test_text_input_backspace(self, text_input):
        """Test backspace functionality."""
        text_input.focus()
        text_input.text = "abc"
        text_input.handle_backspace()
        assert text_input.text == "ab"
        
        text_input.handle_backspace()
        assert text_input.text == "a"
        
        text_input.handle_backspace()
        assert text_input.text == ""
        
        # Backspace on empty string should not crash
        text_input.handle_backspace()
        assert text_input.text == ""
    
    def test_text_input_delete(self, text_input):
        """Test delete key functionality."""
        text_input.focus()
        text_input.text = "abc"
        text_input.cursor_position = 1  # Position after 'a'
        text_input.handle_delete()
        assert text_input.text == "ac"
    
    def test_text_input_enter(self, text_input):
        """Test Enter key submission."""
        callback_called = [False]
        submitted_text = [None]
        
        def on_submit(text):
            callback_called[0] = True
            submitted_text[0] = text
        
        text_input.on_submit = on_submit
        text_input.focus()
        text_input.text = "Hello"
        text_input.handle_enter()
        
        assert callback_called[0]
        assert submitted_text[0] == "Hello"
    
    def test_text_input_escape_unfocus(self, text_input):
        """Test Escape key unfocuses."""
        text_input.focus()
        text_input.handle_escape()
        assert not text_input.is_focused


class TestTextInputCursor:
    """Test cursor functionality."""
    
    def test_text_input_cursor_position(self, text_input):
        """Test cursor position."""
        text_input.focus()
        text_input.text = "abc"
        assert text_input.cursor_position == 3  # At end
        
        text_input.cursor_position = 1
        assert text_input.cursor_position == 1
    
    def test_text_input_cursor_left_arrow(self, text_input):
        """Test left arrow key moves cursor."""
        text_input.focus()
        text_input.text = "abc"
        text_input.cursor_position = 3
        
        text_input.handle_left_arrow()
        assert text_input.cursor_position == 2
        
        text_input.handle_left_arrow()
        assert text_input.cursor_position == 1
        
        text_input.handle_left_arrow()
        assert text_input.cursor_position == 0  # Can't go negative
    
    def test_text_input_cursor_right_arrow(self, text_input):
        """Test right arrow key moves cursor."""
        text_input.focus()
        text_input.text = "abc"
        text_input.cursor_position = 0
        
        text_input.handle_right_arrow()
        assert text_input.cursor_position == 1
        
        text_input.handle_right_arrow()
        assert text_input.cursor_position == 2
        
        text_input.handle_right_arrow()
        assert text_input.cursor_position == 3
        
        # Can't go past end
        text_input.handle_right_arrow()
        assert text_input.cursor_position == 3
    
    def test_text_input_cursor_home_end(self, text_input):
        """Test Home/End keys."""
        text_input.focus()
        text_input.text = "abc"
        text_input.cursor_position = 2
        
        text_input.handle_home()
        assert text_input.cursor_position == 0
        
        text_input.handle_end()
        assert text_input.cursor_position == 3


class TestTextInputSelection:
    """Test text selection functionality."""
    
    def test_text_input_select_all(self, text_input):
        """Test selecting all text."""
        text_input.focus()
        text_input.text = "Hello World"
        text_input.select_all()
        
        assert text_input.selection_start == 0
        assert text_input.selection_end == 11
        assert text_input.has_selection
    
    def test_text_input_clear_selection(self, text_input):
        """Test clearing selection."""
        text_input.focus()
        text_input.text = "Hello"
        text_input.select_all()
        text_input.clear_selection()
        
        assert not text_input.has_selection
        assert text_input.selection_start == text_input.cursor_position
    
    def test_text_input_delete_selection(self, text_input):
        """Test deleting selected text."""
        text_input.focus()
        text_input.text = "Hello World"
        text_input.selection_start = 0
        text_input.selection_end = 5  # Select "Hello"
        text_input.delete_selection()
        
        assert text_input.text == " World"
        assert not text_input.has_selection


class TestTextInputConstraints:
    """Test text input constraints and validation."""
    
    def test_text_input_max_length(self, pygame_init_cleanup):
        """Test maximum length constraint."""
        input_field = TextInput(0, 0, 200, 40, max_length=5)
        input_field.focus()
        
        input_field.handle_key('a')
        input_field.handle_key('b')
        input_field.handle_key('c')
        input_field.handle_key('d')
        input_field.handle_key('e')
        input_field.handle_key('f')  # Should be ignored
        
        assert input_field.text == "abcde"
        assert len(input_field.text) == 5
    
    def test_text_input_numeric_only(self, pygame_init_cleanup):
        """Test numeric-only input."""
        input_field = TextInput(0, 0, 200, 40, numeric_only=True)
        input_field.focus()
        
        input_field.handle_key('1')
        input_field.handle_key('2')
        input_field.handle_key('a')  # Should be ignored
        input_field.handle_key('3')
        
        assert input_field.text == "123"
    
    def test_text_input_alphanumeric_only(self, pygame_init_cleanup):
        """Test alphanumeric-only input."""
        input_field = TextInput(0, 0, 200, 40, alphanumeric_only=True)
        input_field.focus()
        
        input_field.handle_key('a')
        input_field.handle_key('1')
        input_field.handle_key(' ')  # Space should be ignored
        input_field.handle_key('b')
        
        assert input_field.text == "a1b"


class TestTextInputRendering:
    """Test text input rendering."""
    
    def test_text_input_render_empty(self, text_input, pygame_init_cleanup):
        """Test rendering empty input with placeholder."""
        text_input.placeholder = "Enter text..."
        surface = pygame.Surface((400, 300))
        
        text_input.render(surface)
        
        # Should not raise error
        assert True
    
    def test_text_input_render_with_text(self, text_input, pygame_init_cleanup):
        """Test rendering input with text."""
        text_input.text = "Hello"
        text_input.focus()
        surface = pygame.Surface((400, 300))
        
        text_input.render(surface)
        
        # Should not raise error
        assert True
    
    def test_text_input_render_focused(self, text_input, pygame_init_cleanup):
        """Test rendering focused state."""
        text_input.focus()
        surface = pygame.Surface((400, 300))
        
        text_input.render(surface)
        
        # Focused state should have different visual appearance
        assert text_input.is_focused


class TestTextInputIntegration:
    """Integration tests for TextInput."""
    
    def test_text_input_full_typing_session(self, text_input):
        """Test complete typing session."""
        text_input.focus()
        
        # Type word
        for char in "Hello":
            text_input.handle_key(char)
        
        assert text_input.text == "Hello"
        
        # Navigate and insert
        text_input.handle_left_arrow()
        text_input.handle_left_arrow()
        text_input.handle_key(' ')
        
        assert text_input.text == "Hel lo"
        
        # Delete character
        text_input.handle_backspace()
        assert text_input.text == "Hello"
        
        # Select and delete
        text_input.select_all()
        text_input.delete_selection()
        assert text_input.text == ""

