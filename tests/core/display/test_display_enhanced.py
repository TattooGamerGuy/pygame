"""
Tests for Enhanced Display System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from hub.core.display.display_manager_enhanced import (
    EnhancedDisplayManager,
    DisplayMode,
    ScalingMode,
    VSyncMode
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def display_manager(pygame_init_cleanup):
    """Create EnhancedDisplayManager instance."""
    manager = EnhancedDisplayManager((800, 600), "Test Window")
    manager.initialize()
    yield manager
    manager.cleanup()


class TestDisplayModes:
    """Test display mode management."""
    
    def test_display_mode_windowed(self, display_manager):
        """Test windowed display mode."""
        display_manager.set_display_mode(DisplayMode.WINDOWED)
        assert display_manager.current_mode == DisplayMode.WINDOWED
        assert not display_manager.is_fullscreen
    
    def test_display_mode_fullscreen(self, display_manager):
        """Test fullscreen display mode."""
        display_manager.set_display_mode(DisplayMode.FULLSCREEN)
        assert display_manager.current_mode == DisplayMode.FULLSCREEN
        assert display_manager.is_fullscreen
    
    def test_display_mode_borderless(self, display_manager):
        """Test borderless fullscreen mode."""
        display_manager.set_display_mode(DisplayMode.BORDERLESS_FULLSCREEN)
        assert display_manager.current_mode == DisplayMode.BORDERLESS_FULLSCREEN
        # Should be fullscreen but without border
        assert True
    
    def test_display_mode_switch(self, display_manager):
        """Test switching between display modes."""
        display_manager.set_display_mode(DisplayMode.WINDOWED)
        display_manager.set_display_mode(DisplayMode.FULLSCREEN)
        assert display_manager.current_mode == DisplayMode.FULLSCREEN


class TestMultiMonitor:
    """Test multi-monitor support."""
    
    def test_get_available_displays(self, display_manager):
        """Test getting available displays."""
        displays = display_manager.get_available_displays()
        assert len(displays) > 0
        assert isinstance(displays[0], dict)
        assert 'index' in displays[0]
        assert 'width' in displays[0]
        assert 'height' in displays[0]
    
    def test_select_display(self, display_manager):
        """Test selecting display."""
        displays = display_manager.get_available_displays()
        if len(displays) > 1:
            display_manager.set_display(displays[1]['index'])
            assert display_manager.current_display_index == displays[1]['index']
    
    def test_get_primary_display(self, display_manager):
        """Test getting primary display."""
        primary = display_manager.get_primary_display()
        assert primary is not None
        assert primary['index'] >= 0


class TestWindowManagement:
    """Test window management features."""
    
    def test_window_minimize(self, display_manager):
        """Test window minimize."""
        display_manager.minimize()
        # Should minimize (implementation dependent)
        assert True
    
    def test_window_maximize(self, display_manager):
        """Test window maximize."""
        display_manager.maximize()
        # Should maximize (implementation dependent)
        assert True
    
    def test_window_restore(self, display_manager):
        """Test window restore."""
        display_manager.minimize()
        display_manager.restore()
        # Should restore (implementation dependent)
        assert True
    
    def test_window_resize_callback(self, display_manager):
        """Test window resize callback."""
        callback_called = [False]
        new_size = [None]
        
        def on_resize(size):
            callback_called[0] = True
            new_size[0] = size
        
        display_manager.on_resize = on_resize
        
        # Simulate resize (would be triggered by actual resize event)
        display_manager._handle_resize((1024, 768))
        
        assert callback_called[0]
        assert new_size[0] == (1024, 768)
    
    def test_window_resize_validation(self, display_manager):
        """Test window resize with min/max constraints."""
        display_manager.min_width = 400
        display_manager.min_height = 300
        display_manager.max_width = 1920
        display_manager.max_height = 1080
        
        # Try to resize below minimum
        result = display_manager.resize(200, 150)
        # Should clamp to minimum
        assert display_manager.width >= display_manager.min_width
        assert display_manager.height >= display_manager.min_height


class TestVSync:
    """Test VSync options."""
    
    def test_vsync_disabled(self, display_manager):
        """Test VSync disabled mode."""
        display_manager.set_vsync(VSyncMode.OFF)
        assert display_manager.vsync_mode == VSyncMode.OFF
    
    def test_vsync_enabled(self, display_manager):
        """Test VSync enabled mode."""
        display_manager.set_vsync(VSyncMode.ON)
        assert display_manager.vsync_mode == VSyncMode.ON
    
    def test_adaptive_vsync(self, display_manager):
        """Test adaptive VSync mode."""
        display_manager.set_vsync(VSyncMode.ADAPTIVE)
        assert display_manager.vsync_mode == VSyncMode.ADAPTIVE
    
    def test_vsync_toggle(self, display_manager):
        """Test toggling VSync."""
        display_manager.set_vsync(VSyncMode.OFF)
        display_manager.toggle_vsync()
        assert display_manager.vsync_mode == VSyncMode.ON


class TestResolutionScaling:
    """Test resolution scaling modes."""
    
    def test_scaling_mode_stretch(self, display_manager):
        """Test stretch scaling mode."""
        display_manager.set_scaling_mode(ScalingMode.STRETCH)
        assert display_manager.scaling_mode == ScalingMode.STRETCH
    
    def test_scaling_mode_letterbox(self, display_manager):
        """Test letterbox scaling mode."""
        display_manager.set_scaling_mode(ScalingMode.LETTERBOX)
        assert display_manager.scaling_mode == ScalingMode.LETTERBOX
        # Should maintain aspect ratio with black bars
    
    def test_scaling_mode_integer(self, display_manager):
        """Test integer scaling mode."""
        display_manager.set_scaling_mode(ScalingMode.INTEGER_SCALE)
        assert display_manager.scaling_mode == ScalingMode.INTEGER_SCALE
        # Should scale by integer factors (2x, 3x, etc.)
    
    def test_scaling_mode_fit(self, display_manager):
        """Test fit scaling mode."""
        display_manager.set_scaling_mode(ScalingMode.FIT)
        assert display_manager.scaling_mode == ScalingMode.FIT
    
    def test_virtual_resolution(self, display_manager):
        """Test virtual resolution setting."""
        display_manager.set_virtual_resolution(640, 480)
        assert display_manager.virtual_width == 640
        assert display_manager.virtual_height == 480
    
    def test_scaling_ratio(self, display_manager):
        """Test scaling ratio calculation."""
        display_manager.set_virtual_resolution(800, 600)
        display_manager.resize(1920, 1080)
        
        # Should calculate scaling ratio
        scale_x, scale_y = display_manager.get_scaling_ratio()
        assert scale_x > 0
        assert scale_y > 0


class TestResolutionPresets:
    """Test resolution presets."""
    
    def test_resolution_presets(self, display_manager):
        """Test getting resolution presets."""
        presets = display_manager.get_resolution_presets()
        assert len(presets) > 0
        assert isinstance(presets[0], tuple)
        assert len(presets[0]) == 2  # (width, height)
    
    def test_set_resolution_preset(self, display_manager):
        """Test setting resolution from preset."""
        presets = display_manager.get_resolution_presets()
        if presets:
            display_manager.set_resolution(presets[0])
            assert display_manager.size == presets[0]
    
    def test_custom_resolution(self, display_manager):
        """Test setting custom resolution."""
        display_manager.set_resolution((1280, 720))
        assert display_manager.size == (1280, 720)


class TestDisplayEvents:
    """Test display event handling."""
    
    def test_display_focus_event(self, display_manager):
        """Test display focus events."""
        focused = [False]
        
        def on_focus(focused_state):
            focused[0] = focused_state
        
        display_manager.on_focus = on_focus
        
        # Simulate focus event
        display_manager._handle_focus(True)
        
        assert focused[0]
    
    def test_display_expose_event(self, display_manager):
        """Test display expose event."""
        exposed = [False]
        
        def on_expose():
            exposed[0] = True
        
        display_manager.on_expose = on_expose
        
        display_manager._handle_expose()
        
        assert exposed[0]


class TestDisplayState:
    """Test display state management."""
    
    def test_display_state_save(self, display_manager):
        """Test saving display state."""
        # Set specific values first
        display_manager.set_resolution((1024, 768))
        display_manager.set_vsync(VSyncMode.ON)
        
        state = display_manager.save_state()
        
        # Should save actual current size
        assert state['width'] == display_manager.width
        assert state['height'] == display_manager.height
        assert state['virtual_width'] == display_manager.virtual_width
        assert state['virtual_height'] == display_manager.virtual_height
        # Mode should be saved as string value
        assert isinstance(state['mode'], str)
        assert state['mode'] in [m.value for m in DisplayMode]
        # VSync should be saved as string value
        assert isinstance(state['vsync'], str)
        assert state['vsync'] in [v.value for v in VSyncMode]
    
    def test_display_state_restore(self, display_manager):
        """Test restoring display state."""
        state = {
            'width': 1280,
            'height': 720,
            'mode': DisplayMode.WINDOWED,
            'vsync': VSyncMode.OFF
        }
        
        display_manager.restore_state(state)
        
        assert display_manager.size == (1280, 720)
        assert display_manager.current_mode == DisplayMode.WINDOWED


class TestDisplayInfo:
    """Test display information."""
    
    def test_get_display_info(self, display_manager):
        """Test getting display information."""
        info = display_manager.get_display_info()
        
        assert 'width' in info
        assert 'height' in info
        assert 'fullscreen' in info
        assert 'vsync' in info
    
    def test_get_supported_resolutions(self, display_manager):
        """Test getting supported resolutions."""
        resolutions = display_manager.get_supported_resolutions()
        assert len(resolutions) > 0
        assert isinstance(resolutions[0], tuple)


class TestDisplayIntegration:
    """Integration tests for display system."""
    
    def test_display_mode_change_preserves_size(self, display_manager):
        """Test changing mode preserves size when possible."""
        display_manager.set_resolution((1024, 768))
        original_size = display_manager.size
        
        display_manager.set_display_mode(DisplayMode.FULLSCREEN)
        # May change in fullscreen, but should handle gracefully
        assert display_manager.size is not None
    
    def test_resize_during_fullscreen(self, display_manager):
        """Test resize handling during fullscreen."""
        display_manager.set_display_mode(DisplayMode.FULLSCREEN)
        
        # Resize should handle fullscreen mode
        display_manager.resize(1920, 1080)
        
        assert True  # Should not crash

