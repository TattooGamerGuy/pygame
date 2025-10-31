"""
Integration tests for Viewport system.

Tests viewport scaling, aspect ratio handling, virtual-to-screen conversion,
and mobile resolution support.
"""

import pytest
import pygame
from typing import Tuple
from hub.core.display.viewport import Viewport


@pytest.fixture
def viewport():
    """Create a Viewport instance for testing."""
    return Viewport(virtual_width=800, virtual_height=600, screen_width=800, screen_height=600)


class TestViewportInitialization:
    """Test viewport initialization."""
    
    def test_viewport_default_initialization(self, viewport):
        """Test viewport with matching virtual and screen sizes."""
        assert viewport.virtual_width == 800
        assert viewport.virtual_height == 600
        assert viewport.screen_width == 800
        assert viewport.screen_height == 600
        assert viewport.scale_x == 1.0
        assert viewport.scale_y == 1.0
    
    def test_viewport_different_sizes(self):
        """Test viewport with different virtual and screen sizes."""
        viewport = Viewport(
            virtual_width=400, virtual_height=300,
            screen_width=800, screen_height=600
        )
        assert viewport.virtual_width == 400
        assert viewport.virtual_height == 300
        assert viewport.scale_x == 2.0  # 800/400
        assert viewport.scale_y == 2.0  # 600/300


class TestViewportScaling:
    """Test viewport scaling functionality."""
    
    def test_viewport_maintains_aspect_ratio(self):
        """Test that viewport maintains aspect ratio (letterboxing)."""
        # Virtual: 16:9, Screen: 4:3
        viewport = Viewport(
            virtual_width=1600, virtual_height=900,  # 16:9
            screen_width=800, screen_height=600       # 4:3
        )
        
        # Should use smaller scale to fit both dimensions
        assert viewport.scale_x == viewport.scale_y  # Uniform scaling
        assert viewport.scale_x < 1.0  # Should be less than 1.0
    
    def test_viewport_letterboxing(self):
        """Test viewport creates letterboxing for different aspect ratios."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,   # 4:3
            screen_width=1280, screen_height=720      # 16:9
        )
        
        # Should have offsets for centering
        viewport_rect = viewport.get_viewport_rect()
        assert viewport_rect.x >= 0  # Offset X for centering
        assert viewport_rect.y >= 0  # Offset Y for centering
    
    def test_viewport_pillarboxing(self):
        """Test viewport creates pillarboxing for different aspect ratios."""
        viewport = Viewport(
            virtual_width=1600, virtual_height=900,   # 16:9
            screen_width=800, screen_height=600       # 4:3
        )
        
        # Should have offsets for centering
        viewport_rect = viewport.get_viewport_rect()
        assert viewport_rect.x >= 0
        assert viewport_rect.y >= 0


class TestViewportCoordinateConversion:
    """Test virtual-to-screen coordinate conversion."""
    
    def test_virtual_to_screen_matching_sizes(self, viewport):
        """Test conversion when virtual and screen sizes match."""
        screen_x, screen_y = viewport.virtual_to_screen(400.0, 300.0)
        assert screen_x == 400
        assert screen_y == 300
    
    def test_virtual_to_screen_scaled(self):
        """Test conversion with scaling."""
        viewport = Viewport(
            virtual_width=400, virtual_height=300,
            screen_width=800, screen_height=600
        )
        screen_x, screen_y = viewport.virtual_to_screen(200.0, 150.0)
        assert screen_x == 400  # 200 * 2.0
        assert screen_y == 300  # 150 * 2.0
    
    def test_screen_to_virtual_matching_sizes(self, viewport):
        """Test screen-to-virtual conversion when sizes match."""
        virtual_x, virtual_y = viewport.screen_to_virtual(400, 300)
        assert abs(virtual_x - 400.0) < 0.01
        assert abs(virtual_y - 300.0) < 0.01
    
    def test_screen_to_virtual_scaled(self):
        """Test screen-to-virtual conversion with scaling."""
        viewport = Viewport(
            virtual_width=400, virtual_height=300,
            screen_width=800, screen_height=600
        )
        virtual_x, virtual_y = viewport.screen_to_virtual(800, 600)
        assert abs(virtual_x - 400.0) < 0.01  # 800 / 2.0
        assert abs(virtual_y - 300.0) < 0.01  # 600 / 2.0
    
    def test_coordinate_conversion_roundtrip(self, viewport):
        """Test that coordinate conversion is reversible."""
        virtual_x, virtual_y = 250.0, 180.0
        screen_x, screen_y = viewport.virtual_to_screen(virtual_x, virtual_y)
        back_virtual_x, back_virtual_y = viewport.screen_to_virtual(screen_x, screen_y)
        
        assert abs(back_virtual_x - virtual_x) < 1.0
        assert abs(back_virtual_y - virtual_y) < 1.0


class TestViewportResize:
    """Test viewport resizing functionality."""
    
    def test_viewport_resize_updates_scaling(self, viewport):
        """Test that resize updates scale factors."""
        original_scale_x = viewport.scale_x
        
        viewport.resize(1600, 1200)
        assert viewport.screen_width == 1600
        assert viewport.screen_height == 1200
        assert viewport.scale_x != original_scale_x
    
    def test_viewport_resize_maintains_virtual_size(self, viewport):
        """Test that resize doesn't change virtual size."""
        original_virtual_width = viewport.virtual_width
        original_virtual_height = viewport.virtual_height
        
        viewport.resize(1280, 720)
        assert viewport.virtual_width == original_virtual_width
        assert viewport.virtual_height == original_virtual_height


@pytest.mark.mobile
@pytest.mark.mobile_resolution
class TestViewportMobileIntegration:
    """Test viewport integration with mobile resolutions."""
    
    @pytest.mark.parametrize("device,resolution,aspect_ratio", [
        ("iphone_se", (320, 568), 568 / 320),
        ("iphone_12", (390, 844), 844 / 390),
        ("iphone_12_pro_max", (428, 926), 926 / 428),
        ("ipad", (768, 1024), 1024 / 768),
        ("android_small", (360, 640), 640 / 360),
    ])
    def test_viewport_mobile_resolution(self, device, resolution, aspect_ratio):
        """Test viewport with various mobile resolutions."""
        screen_width, screen_height = resolution
        
        # Use a standard virtual resolution (16:9)
        virtual_width, virtual_height = 800, 450  # 16:9
        
        viewport = Viewport(
            virtual_width=virtual_width,
            virtual_height=virtual_height,
            screen_width=screen_width,
            screen_height=screen_height
        )
        
        # Should maintain aspect ratio
        assert viewport.scale_x == viewport.scale_y
        
        # Should have proper viewport rect
        viewport_rect = viewport.get_viewport_rect()
        assert viewport_rect.width > 0
        assert viewport_rect.height > 0
    
    def test_viewport_mobile_iphone_se(self):
        """Test viewport specifically for iPhone SE resolution."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,
            screen_width=320, screen_height=568
        )
        
        # Should scale down appropriately
        assert viewport.scale_x < 1.0
        assert viewport.scale_x == viewport.scale_y
        
        # Center of virtual should map to center of screen (with offsets)
        virtual_center_x, virtual_center_y = 400.0, 300.0
        screen_x, screen_y = viewport.virtual_to_screen(virtual_center_x, virtual_center_y)
        
        # Should be in center area of screen (accounting for letterboxing)
        assert 100 < screen_x < 220  # Roughly center of 320 width
        assert 200 < screen_y < 368  # Roughly center of 568 height
    
    def test_viewport_mobile_ipad(self):
        """Test viewport specifically for iPad resolution."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,
            screen_width=768, screen_height=1024
        )
        
        # Should scale appropriately
        scale = min(768 / 800, 1024 / 600)
        assert abs(viewport.scale_x - scale) < 0.01
    
    def test_viewport_mobile_coordinate_accuracy(self):
        """Test coordinate conversion accuracy on mobile."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,
            screen_width=390, screen_height=844  # iPhone 12
        )
        
        # Test multiple virtual coordinates
        test_points = [
            (0, 0),
            (400, 300),  # Center
            (800, 600),  # Bottom-right
        ]
        
        for vx, vy in test_points:
            sx, sy = viewport.virtual_to_screen(vx, vy)
            back_vx, back_vy = viewport.screen_to_virtual(sx, sy)
            
            # Should be close to original (accounting for scaling and offsets)
            assert abs(back_vx - vx) < 10.0  # Allow some tolerance
            assert abs(back_vy - vy) < 10.0


class TestViewportEdgeCases:
    """Test viewport edge cases."""
    
    def test_viewport_very_small_screen(self):
        """Test viewport with very small screen size."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,
            screen_width=100, screen_height=75
        )
        
        # Should still scale appropriately
        assert viewport.scale_x > 0
        assert viewport.scale_y > 0
    
    def test_viewport_very_large_screen(self):
        """Test viewport with very large screen size."""
        viewport = Viewport(
            virtual_width=800, virtual_height=600,
            screen_width=3840, screen_height=2160  # 4K
        )
        
        # Should scale up appropriately
        assert viewport.scale_x > 1.0
        assert viewport.scale_y > 1.0
    
    def test_viewport_viewport_rect(self, viewport):
        """Test getting viewport rectangle."""
        viewport_rect = viewport.get_viewport_rect()
        assert viewport_rect.width > 0
        assert viewport_rect.height > 0
        assert viewport_rect.x >= 0
        assert viewport_rect.y >= 0

