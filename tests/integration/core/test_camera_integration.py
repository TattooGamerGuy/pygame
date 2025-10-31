"""
Integration tests for Camera system.

Tests camera following, bounds clamping, world-to-screen conversion,
and integration with display/viewport systems.
"""

import pytest
import pygame
from typing import Tuple
from hub.core.display.camera import Camera


@pytest.fixture
def camera():
    """Create a Camera instance for testing."""
    return Camera(x=0.0, y=0.0, width=800, height=600)


class TestCameraBasicOperations:
    """Test basic camera operations."""
    
    def test_camera_initialization(self, camera):
        """Test camera initialization with default parameters."""
        assert camera.x == 0.0
        assert camera.y == 0.0
        assert camera.width == 800
        assert camera.height == 600
        assert camera.zoom == 1.0
        assert camera.target is None
        assert camera.follow_speed == 0.1
    
    def test_camera_set_position(self, camera):
        """Test setting camera position."""
        camera.set_position(100.0, 200.0)
        assert camera.x == 100.0
        assert camera.y == 200.0
    
    def test_camera_move(self, camera):
        """Test moving camera by offset."""
        camera.set_position(50.0, 50.0)
        camera.move(25.0, -10.0)
        assert camera.x == 75.0
        assert camera.y == 40.0
    
    def test_camera_world_to_screen(self, camera):
        """Test world-to-screen coordinate conversion."""
        camera.set_position(100.0, 100.0)
        screen_x, screen_y = camera.world_to_screen(150.0, 150.0)
        assert screen_x == 50  # (150 - 100) * 1.0
        assert screen_y == 50  # (150 - 100) * 1.0
    
    def test_camera_screen_to_world(self, camera):
        """Test screen-to-world coordinate conversion."""
        camera.set_position(100.0, 100.0)
        world_x, world_y = camera.screen_to_world(50, 50)
        assert abs(world_x - 150.0) < 0.01  # 50 / 1.0 + 100
        assert abs(world_y - 150.0) < 0.01
    
    def test_camera_zoom_affects_coordinates(self, camera):
        """Test that zoom affects coordinate conversion."""
        camera.set_position(100.0, 100.0)
        camera.zoom = 2.0
        
        screen_x, screen_y = camera.world_to_screen(150.0, 150.0)
        assert screen_x == 100  # (150 - 100) * 2.0
        assert screen_y == 100


class TestCameraFollowing:
    """Test camera target following functionality."""
    
    def test_camera_set_target(self, camera):
        """Test setting a target for camera to follow."""
        camera.set_target(500.0, 300.0, speed=0.2)
        assert camera.target == (500.0, 300.0)
        assert camera.follow_speed == 0.2
    
    def test_camera_smooth_follow(self, camera):
        """Test smooth camera following with update."""
        camera.set_position(0.0, 0.0)
        camera.set_target(200.0, 100.0, speed=0.5)
        
        initial_x, initial_y = camera.x, camera.y
        
        # Update multiple times
        for _ in range(10):
            camera.update(0.016)  # ~60 FPS delta
        
        # Camera should have moved towards target
        assert camera.x > initial_x
        assert camera.y > initial_y
        assert camera.x < 200.0  # Should not reach instantly
        assert camera.y < 100.0
    
    def test_camera_follow_completes(self, camera):
        """Test that camera eventually reaches target."""
        camera.set_position(0.0, 0.0)
        camera.set_target(100.0, 100.0, speed=1.0)  # Fast follow
        
        # Update many times to reach target
        for _ in range(100):
            camera.update(0.016)
        
        # Should be very close to target
        assert abs(camera.x - 100.0) < 1.0
        assert abs(camera.y - 100.0) < 1.0


class TestCameraBounds:
    """Test camera bounds clamping."""
    
    def test_camera_bounds_clamping_left(self, camera):
        """Test camera clamping to left bound."""
        bounds = pygame.Rect(0, 0, 2000, 2000)
        camera = Camera(x=0, y=0, width=800, height=600, bounds=bounds)
        
        camera.set_position(-100.0, 100.0)
        assert camera.x >= bounds.left
    
    def test_camera_bounds_clamping_top(self, camera):
        """Test camera clamping to top bound."""
        bounds = pygame.Rect(0, 0, 2000, 2000)
        camera = Camera(x=0, y=0, width=800, height=600, bounds=bounds)
        
        camera.set_position(100.0, -100.0)
        assert camera.y >= bounds.top
    
    def test_camera_bounds_clamping_right(self):
        """Test camera clamping to right bound."""
        bounds = pygame.Rect(0, 0, 1000, 1000)
        camera = Camera(x=0, y=0, width=800, height=600, bounds=bounds)
        
        camera.set_position(500.0, 100.0)  # Would go past right edge
        view_rect = camera.get_view_rect()
        assert view_rect.right <= bounds.right
    
    def test_camera_bounds_clamping_bottom(self):
        """Test camera clamping to bottom bound."""
        bounds = pygame.Rect(0, 0, 1000, 1000)
        camera = Camera(x=0, y=0, width=800, height=600, bounds=bounds)
        
        camera.set_position(100.0, 500.0)  # Would go past bottom edge
        view_rect = camera.get_view_rect()
        assert view_rect.bottom <= bounds.bottom
    
    def test_camera_move_respects_bounds(self):
        """Test that camera move respects bounds."""
        bounds = pygame.Rect(0, 0, 1000, 1000)
        camera = Camera(x=100, y=100, width=800, height=600, bounds=bounds)
        
        camera.move(-200.0, -200.0)  # Would go out of bounds
        view_rect = camera.get_view_rect()
        assert view_rect.left >= bounds.left
        assert view_rect.top >= bounds.top


class TestCameraViewRect:
    """Test camera view rectangle functionality."""
    
    def test_camera_get_view_rect(self, camera):
        """Test getting camera view rectangle."""
        camera.set_position(100.0, 200.0)
        view_rect = camera.get_view_rect()
        
        assert view_rect.x == 100.0
        assert view_rect.y == 200.0
        assert view_rect.width == 800.0 / camera.zoom
        assert view_rect.height == 600.0 / camera.zoom
    
    def test_camera_view_rect_with_zoom(self):
        """Test view rect calculation with zoom."""
        camera = Camera(x=0, y=0, width=800, height=600, zoom=2.0)
        view_rect = camera.get_view_rect()
        
        # With 2x zoom, visible area should be half
        assert view_rect.width == 400.0  # 800 / 2.0
        assert view_rect.height == 300.0  # 600 / 2.0


@pytest.mark.mobile
class TestCameraMobileIntegration:
    """Test camera integration with mobile resolutions."""
    
    @pytest.mark.parametrize("device,resolution", [
        ("iphone_se", (320, 568)),
        ("iphone_12", (390, 844)),
        ("ipad", (768, 1024)),
    ])
    def test_camera_mobile_resolution(self, device, resolution):
        """Test camera works correctly with mobile resolutions."""
        width, height = resolution
        camera = Camera(x=0, y=0, width=width, height=height)
        
        assert camera.width == width
        assert camera.height == height
        
        view_rect = camera.get_view_rect()
        assert view_rect.width == width / camera.zoom
        assert view_rect.height == height / camera.zoom
    
    def test_camera_coordinate_conversion_mobile(self):
        """Test coordinate conversion on mobile resolutions."""
        # iPhone SE resolution
        camera = Camera(x=0, y=0, width=320, height=568)
        
        world_x, world_y = 160.0, 284.0  # Center of screen in world
        screen_x, screen_y = camera.world_to_screen(world_x, world_y)
        
        # Should map to center of screen
        assert abs(screen_x - 160) < 1  # Half of 320
        assert abs(screen_y - 284) < 1  # Half of 568

