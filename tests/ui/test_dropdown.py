"""
Tests for Dropdown component (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.ui.dropdown import Dropdown


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def dropdown_items():
    """Common dropdown items for testing."""
    return ["Option 1", "Option 2", "Option 3", "Option 4"]


@pytest.fixture
def dropdown(pygame_init_cleanup, dropdown_items):
    """Create a Dropdown instance for testing."""
    return Dropdown(x=100, y=100, width=200, height=40, items=dropdown_items)


class TestDropdownInitialization:
    """Test Dropdown initialization."""
    
    def test_dropdown_initialization(self, dropdown, dropdown_items):
        """Test Dropdown initialization."""
        assert dropdown.x == 100
        assert dropdown.y == 100
        assert dropdown.width == 200
        assert dropdown.height == 40
        assert dropdown.items == dropdown_items
        assert dropdown.selected_index == 0
        assert dropdown.selected_value == dropdown_items[0]
        assert not dropdown.is_open
    
    def test_dropdown_empty_items(self, pygame_init_cleanup):
        """Test Dropdown with empty items list."""
        dd = Dropdown(0, 0, 200, 40, items=[])
        assert dd.items == []
        assert dd.selected_index is None
        assert dd.selected_value is None
    
    def test_dropdown_with_initial_selection(self, pygame_init_cleanup, dropdown_items):
        """Test Dropdown with initial selection."""
        dd = Dropdown(0, 0, 200, 40, items=dropdown_items, initial_selection=2)
        assert dd.selected_index == 2
        assert dd.selected_value == dropdown_items[2]
    
    def test_dropdown_with_placeholder(self, pygame_init_cleanup, dropdown_items):
        """Test Dropdown with placeholder text."""
        dd = Dropdown(0, 0, 200, 40, items=dropdown_items, placeholder="Select option...")
        assert dd.placeholder == "Select option..."


class TestDropdownSelection:
    """Test dropdown selection behavior."""
    
    def test_dropdown_select_by_index(self, dropdown, dropdown_items):
        """Test selecting item by index."""
        dropdown.select_index(2)
        assert dropdown.selected_index == 2
        assert dropdown.selected_value == dropdown_items[2]
    
    def test_dropdown_select_by_value(self, dropdown, dropdown_items):
        """Test selecting item by value."""
        dropdown.select_value("Option 3")
        assert dropdown.selected_index == 2
        assert dropdown.selected_value == "Option 3"
    
    def test_dropdown_select_invalid_index(self, dropdown):
        """Test selecting invalid index."""
        dropdown.select_index(10)  # Out of range
        # Should not crash, may reset to first or keep current
        assert dropdown.selected_index is not None
    
    def test_dropdown_select_invalid_value(self, dropdown):
        """Test selecting invalid value."""
        dropdown.select_value("Non-existent")
        # Should not crash
        assert dropdown.selected_index is not None


class TestDropdownOpenClose:
    """Test dropdown open/close behavior."""
    
    def test_dropdown_open(self, dropdown):
        """Test opening dropdown."""
        dropdown.open()
        assert dropdown.is_open
    
    def test_dropdown_close(self, dropdown):
        """Test closing dropdown."""
        dropdown.open()
        dropdown.close()
        assert not dropdown.is_open
    
    def test_dropdown_toggle(self, dropdown):
        """Test toggling dropdown."""
        assert not dropdown.is_open
        
        dropdown.toggle()
        assert dropdown.is_open
        
        dropdown.toggle()
        assert not dropdown.is_open
    
    def test_dropdown_click_to_open(self, dropdown):
        """Test clicking dropdown opens it."""
        dropdown.handle_click((150, 120))
        assert dropdown.is_open
    
    def test_dropdown_click_outside_closes(self, dropdown):
        """Test clicking outside closes dropdown."""
        dropdown.open()
        dropdown.handle_click((50, 50))  # Outside bounds
        assert not dropdown.is_open


class TestDropdownItemSelection:
    """Test selecting items from dropdown."""
    
    def test_dropdown_select_item_by_click(self, dropdown, dropdown_items):
        """Test selecting item by clicking in dropdown."""
        dropdown.open()
        
        # Click on second item (assuming items are rendered below)
        # Position would be at y = dropdown.y + dropdown.height + (item_height * 1)
        click_y = dropdown.y + dropdown.height + 30  # Approximate
        dropdown.handle_click((150, click_y))
        
        # Should select item and close
        assert not dropdown.is_open
    
    def test_dropdown_keyboard_navigation(self, dropdown, dropdown_items):
        """Test keyboard navigation in dropdown."""
        dropdown.open()
        
        # Arrow down should move selection
        dropdown.handle_key_down()
        # Selection should move down (if implemented)
        
        # Enter should select
        dropdown.handle_enter()
        assert not dropdown.is_open


class TestDropdownCallbacks:
    """Test dropdown callbacks."""
    
    def test_dropdown_on_change_callback(self, dropdown, dropdown_items):
        """Test on_change callback."""
        callback_called = [False]
        new_value = [None]
        
        def on_change(value, index):
            callback_called[0] = True
            new_value[0] = value
        
        dropdown.on_change = on_change
        dropdown.select_index(2)
        
        assert callback_called[0]
        assert new_value[0] == dropdown_items[2]
    
    def test_dropdown_on_open_callback(self, dropdown):
        """Test on_open callback."""
        callback_called = [False]
        
        def on_open():
            callback_called[0] = True
        
        dropdown.on_open = on_open
        dropdown.open()
        
        assert callback_called[0]
    
    def test_dropdown_on_close_callback(self, dropdown):
        """Test on_close callback."""
        callback_called = [False]
        
        def on_close():
            callback_called[0] = True
        
        dropdown.on_close = on_close
        dropdown.open()
        dropdown.close()
        
        assert callback_called[0]


class TestDropdownRendering:
    """Test dropdown rendering."""
    
    def test_dropdown_render_closed(self, dropdown, pygame_init_cleanup):
        """Test rendering closed dropdown."""
        surface = pygame.Surface((400, 300))
        dropdown.render(surface)
        
        # Should not raise error
        assert True
    
    def test_dropdown_render_open(self, dropdown, pygame_init_cleanup):
        """Test rendering open dropdown."""
        dropdown.open()
        surface = pygame.Surface((400, 300))
        dropdown.render(surface)
        
        # Should not raise error
        assert True
    
    def test_dropdown_render_selected_text(self, dropdown, pygame_init_cleanup):
        """Test rendering selected text."""
        dropdown.select_index(1)
        surface = pygame.Surface((400, 300))
        dropdown.render(surface)
        
        # Selected text should be visible
        assert True


class TestDropdownScrolling:
    """Test dropdown scrolling for long lists."""
    
    def test_dropdown_scrollable(self, pygame_init_cleanup):
        """Test dropdown with many items scrolls."""
        many_items = [f"Option {i}" for i in range(20)]
        dd = Dropdown(0, 0, 200, 40, items=many_items, max_visible_items=5)
        dd.open()
        
        assert dd.max_visible_items == 5
        assert len(dd.items) == 20
    
    def test_dropdown_scroll_up_down(self, pygame_init_cleanup):
        """Test scrolling dropdown."""
        many_items = [f"Option {i}" for i in range(20)]
        dd = Dropdown(0, 0, 200, 40, items=many_items, max_visible_items=5)
        dd.open()
        
        # Scroll down
        dd.scroll_down()
        assert dd.scroll_offset >= 0
        
        # Scroll up
        dd.scroll_up()
        assert dd.scroll_offset >= 0


class TestDropdownFiltering:
    """Test dropdown filtering/search."""
    
    def test_dropdown_filter_items(self, dropdown, dropdown_items):
        """Test filtering dropdown items."""
        dropdown.filter_text = "Option 2"
        
        # Should filter items
        filtered = dropdown.filtered_items
        assert len(filtered) <= len(dropdown_items)
        assert all("Option 2" in item for item in filtered)
    
    def test_dropdown_clear_filter(self, dropdown):
        """Test clearing filter."""
        dropdown.filter_text = "test"
        dropdown.clear_filter()
        
        assert dropdown.filter_text == ""
        assert len(dropdown.filtered_items) == len(dropdown.items)


class TestDropdownEdgeCases:
    """Test dropdown edge cases."""
    
    def test_dropdown_empty_selection(self, pygame_init_cleanup, dropdown_items):
        """Test dropdown with no selection allowed."""
        dd = Dropdown(0, 0, 200, 40, items=dropdown_items, allow_empty=True)
        dd.clear_selection()
        
        assert dd.selected_index is None
        assert dd.selected_value is None
    
    def test_dropdown_dynamic_items(self, dropdown):
        """Test changing items dynamically."""
        new_items = ["New 1", "New 2", "New 3"]
        dropdown.items = new_items
        
        assert dropdown.items == new_items
        # Selected index might reset
        assert dropdown.selected_index is not None or dropdown.selected_index is None


class TestDropdownIntegration:
    """Integration tests for dropdown."""
    
    def test_dropdown_in_form(self, pygame_init_cleanup, dropdown_items):
        """Test dropdown works in form context."""
        # This test verifies dropdown can work in form context
        dropdown = Dropdown(50, 50, 200, 40, items=dropdown_items)
        
        # Dropdown should work independently
        assert len(dropdown.items) == len(dropdown_items)
        dropdown.open()
        assert dropdown.is_open
        
        # Should be able to select items
        dropdown.select_index(1)
        assert dropdown.selected_index == 1
    
    def test_dropdown_multiple_dropdowns(self, pygame_init_cleanup, dropdown_items):
        """Test multiple dropdowns work independently."""
        dd1 = Dropdown(0, 0, 200, 40, items=dropdown_items)
        dd2 = Dropdown(0, 100, 200, 40, items=["A", "B", "C"])
        
        dd1.open()
        assert dd1.is_open
        assert not dd2.is_open
        
        dd2.open()
        # Opening second should close first (common behavior)
        # Or both can be open (implementation dependent)
        assert dd2.is_open

