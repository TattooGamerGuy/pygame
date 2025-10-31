"""
Integration tests for Renderer system.

Tests renderer with sprite batch, layer manager, rendering performance,
and mobile rendering considerations.
"""

import pytest
import pygame
from hub.core.rendering.renderer import Renderer


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def renderer(pygame_init_cleanup):
    """Create a Renderer instance with a screen."""
    screen = pygame.display.set_mode((800, 600))
    return Renderer(screen)


@pytest.fixture
def test_surface():
    """Create a test surface for rendering."""
    pygame.init()
    surface = pygame.Surface((32, 32))
    surface.fill((255, 0, 0))  # Red
    yield surface
    pygame.quit()


class TestRendererInitialization:
    """Test Renderer initialization."""
    
    def test_renderer_initialization(self, renderer):
        """Test Renderer initialization."""
        assert renderer.screen is not None
        assert renderer.sprite_batch is not None
        assert renderer.layer_manager is not None
    
    def test_renderer_clear_color(self, renderer):
        """Test renderer clear color setting."""
        # Default clear color should be set
        # Implementation dependent


class TestRendererLifecycle:
    """Test Renderer begin/end lifecycle."""
    
    def test_renderer_begin_end(self, renderer):
        """Test renderer begin and end."""
        renderer.begin()
        renderer.end()
        
        # Should not raise errors
    
    def test_renderer_multiple_cycles(self, renderer):
        """Test multiple render cycles."""
        for _ in range(5):
            renderer.begin()
            renderer.end()
        
        # Should handle multiple cycles


class TestRendererDrawSprite:
    """Test drawing sprites through renderer."""
    
    def test_renderer_draw_sprite(self, renderer, test_surface):
        """Test drawing a sprite."""
        renderer.begin()
        renderer.draw_sprite(test_surface, (100, 100))
        renderer.end()
        
        # Should not raise errors
    
    def test_renderer_draw_sprite_with_layer(self, renderer, test_surface):
        """Test drawing sprite with layer."""
        renderer.begin()
        renderer.draw_sprite(test_surface, (200, 200), layer=1)
        renderer.draw_sprite(test_surface, (200, 200), layer=2)
        renderer.end()
        
        # Should handle layers correctly
    
    def test_renderer_draw_sprite_with_transform(self, renderer, test_surface):
        """Test drawing sprite with rotation and scale."""
        renderer.begin()
        renderer.draw_sprite(
            test_surface,
            (150, 150),
            rotation=45.0,
            scale=2.0
        )
        renderer.end()
        
        # Should handle transforms


class TestRendererPerformance:
    """Test renderer performance."""
    
    def test_renderer_many_sprites(self, renderer, test_surface):
        """Test rendering many sprites."""
        renderer.begin()
        for i in range(100):
            renderer.draw_sprite(test_surface, (i * 10, i * 10))
        renderer.end()
        
        # Should handle many sprites efficiently
    
    @pytest.mark.performance
    def test_renderer_performance(self, renderer, test_surface):
        """Test renderer performance."""
        import time
        
        renderer.begin()
        
        start = time.time()
        for _ in range(60):  # 60 sprites
            renderer.draw_sprite(test_surface, (100, 100))
        renderer.end()
        elapsed = time.time() - start
        
        # Should be fast enough for 60 FPS
        assert elapsed < 0.1  # Less than 100ms for 60 sprites


@pytest.mark.mobile
class TestRendererMobile:
    """Test renderer with mobile considerations."""
    
    def test_renderer_mobile_resolution(self, pygame_init_cleanup):
        """Test renderer with mobile resolution."""
        screen = pygame.display.set_mode((390, 844))  # iPhone 12
        renderer = Renderer(screen)
        
        test_surface = pygame.Surface((32, 32))
        test_surface.fill((0, 255, 0))
        
        renderer.begin()
        renderer.draw_sprite(test_surface, (195, 422))  # Center
        renderer.end()
        
        # Should work on mobile resolution
    
    @pytest.mark.mobile_performance
    def test_renderer_mobile_performance(self, renderer, test_surface):
        """Test renderer performance on mobile (lower sprite count)."""
        import time
        
        renderer.begin()
        
        start = time.time()
        for _ in range(30):  # Fewer sprites for mobile
            renderer.draw_sprite(test_surface, (100, 100))
        renderer.end()
        elapsed = time.time() - start
        
        # Should be fast enough for 30 FPS mobile
        assert elapsed < 0.05  # Less than 50ms for 30 sprites

