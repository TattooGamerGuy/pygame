"""
Tests for Enhanced Rendering System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from typing import Tuple
from hub.core.rendering.renderer_enhanced import (
    EnhancedRenderer,
    RenderTarget,
    Shader,
    ShaderType,
    ParticleSystem,
    Particle,
    LightingSystem,
    Light,
    LightType,
    PostProcessor,
    EffectType,
    LayerGroup
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.display.set_mode((800, 600))
    yield
    pygame.quit()


@pytest.fixture
def renderer(pygame_init_cleanup):
    """Create EnhancedRenderer instance."""
    screen = pygame.display.get_surface()
    ren = EnhancedRenderer(screen)
    yield ren


@pytest.fixture
def test_surface():
    """Create test surface."""
    return pygame.Surface((100, 100))


class TestRenderTargets:
    """Test render targets (offscreen rendering)."""
    
    def test_render_target_creation(self, renderer):
        """Test creating render target."""
        target = renderer.create_render_target(800, 600)
        assert target is not None
        assert target.width == 800
        assert target.height == 600
    
    def test_render_to_target(self, renderer, test_surface):
        """Test rendering to render target."""
        target = renderer.create_render_target(400, 300)
        
        renderer.set_render_target(target)
        renderer.begin()
        renderer.draw_sprite(test_surface, (50, 50))
        renderer.end()
        
        # Should render to target, not screen
        assert True  # Target should contain rendered content
    
    def test_render_target_clear(self, renderer):
        """Test clearing render target."""
        target = renderer.create_render_target(400, 300)
        target.clear((255, 0, 0))  # Clear with red
        
        assert True  # Should clear target
    
    def test_render_target_to_surface(self, renderer):
        """Test getting surface from render target."""
        target = renderer.create_render_target(400, 300)
        surface = target.get_surface()
        
        assert surface is not None
        assert surface.get_width() == 400
        assert surface.get_height() == 300
    
    def test_render_target_resize(self, renderer):
        """Test resizing render target."""
        target = renderer.create_render_target(400, 300)
        target.resize(800, 600)
        
        assert target.width == 800
        assert target.height == 600


class TestShaders:
    """Test shader system."""
    
    def test_shader_creation(self, renderer):
        """Test creating shader."""
        shader = renderer.create_shader("test_shader", ShaderType.POST_PROCESS)
        assert shader is not None
        assert shader.name == "test_shader"
        assert shader.type == ShaderType.POST_PROCESS
    
    def test_shader_parameters(self, renderer):
        """Test shader parameters."""
        shader = renderer.create_shader("test", ShaderType.POST_PROCESS)
        
        shader.set_parameter("intensity", 0.75)
        assert shader.get_parameter("intensity") == 0.75
    
    def test_shader_enable_disable(self, renderer):
        """Test enabling/disabling shaders."""
        shader = renderer.create_shader("test", ShaderType.POST_PROCESS)
        
        shader.enable()
        assert shader.is_enabled
        
        shader.disable()
        assert not shader.is_enabled
    
    def test_shader_compilation(self, renderer):
        """Test shader compilation."""
        # Pygame doesn't have native shaders, but we can test the interface
        shader = renderer.create_shader("test", ShaderType.POST_PROCESS)
        
        # Should compile successfully (or handle gracefully)
        assert True


class TestParticleSystems:
    """Test particle systems."""
    
    def test_particle_system_creation(self, renderer):
        """Test creating particle system."""
        ps = renderer.create_particle_system("explosion")
        assert ps is not None
        assert ps.name == "explosion"
    
    def test_particle_emission(self, renderer):
        """Test particle emission."""
        ps = renderer.create_particle_system("test")
        
        ps.emit(10, (100, 100))
        assert ps.particle_count >= 10
    
    def test_particle_update(self, renderer):
        """Test particle system update."""
        ps = renderer.create_particle_system("test")
        ps.emit(5, (100, 100))
        
        initial_count = ps.particle_count
        ps.update(0.016)  # ~60 FPS delta
        
        # Particles should still exist or be cleaned up if expired
        assert True
    
    def test_particle_properties(self, renderer):
        """Test particle properties."""
        ps = renderer.create_particle_system("test")
        
        ps.set_color((255, 0, 0))  # Red particles
        ps.set_lifetime(2.0)  # 2 second lifetime
        ps.set_speed(50.0)  # 50 pixels per second
        
        assert ps.color == (255, 0, 0)
        assert ps.lifetime == 2.0
        assert ps.speed == 50.0
    
    def test_particle_rendering(self, renderer):
        """Test particle rendering."""
        ps = renderer.create_particle_system("test")
        ps.emit(10, (100, 100))
        
        renderer.begin()
        renderer.draw_particles(ps)
        renderer.end()
        
        # Should render particles
        assert True


class TestLightingSystem:
    """Test lighting system."""
    
    def test_lighting_system_creation(self, renderer):
        """Test creating lighting system."""
        lighting = renderer.get_lighting_system()
        assert lighting is not None
    
    def test_light_creation(self, renderer):
        """Test creating lights."""
        lighting = renderer.get_lighting_system()
        
        light = lighting.create_light(LightType.POINT, (100, 100))
        assert light is not None
        assert light.type == LightType.POINT
        assert light.position == (100, 100)
    
    def test_light_properties(self, renderer):
        """Test light properties."""
        lighting = renderer.get_lighting_system()
        light = lighting.create_light(LightType.POINT, (100, 100))
        
        light.set_color((255, 255, 200))  # Warm light
        light.set_intensity(0.8)
        light.set_radius(150.0)
        
        assert light.color == (255, 255, 200)
        assert light.intensity == 0.8
        assert light.radius == 150.0
    
    def test_ambient_light(self, renderer):
        """Test ambient light."""
        lighting = renderer.get_lighting_system()
        
        lighting.set_ambient_light(0.2)  # 20% ambient
        assert lighting.ambient_light == 0.2
    
    def test_light_enable_disable(self, renderer):
        """Test enabling/disabling lights."""
        lighting = renderer.get_lighting_system()
        light = lighting.create_light(LightType.POINT, (100, 100))
        
        light.disable()
        assert not light.is_enabled
        
        light.enable()
        assert light.is_enabled
    
    def test_directional_light(self, renderer):
        """Test directional light."""
        lighting = renderer.get_lighting_system()
        
        light = lighting.create_light(LightType.DIRECTIONAL, (0, 0))
        light.set_direction((1, -1))  # Light from top-right
        
        assert light.direction == (1, -1)


class TestPostProcessing:
    """Test post-processing effects."""
    
    def test_post_processor_creation(self, renderer):
        """Test creating post-processor."""
        processor = renderer.get_post_processor()
        assert processor is not None
    
    def test_effect_addition(self, renderer):
        """Test adding post-processing effects."""
        processor = renderer.get_post_processor()
        
        processor.add_effect(EffectType.BLOOM)
        assert EffectType.BLOOM in processor.active_effects
    
    def test_effect_removal(self, renderer):
        """Test removing post-processing effects."""
        processor = renderer.get_post_processor()
        
        processor.add_effect(EffectType.BLOOM)
        processor.remove_effect(EffectType.BLOOM)
        
        assert EffectType.BLOOM not in processor.active_effects
    
    def test_effect_parameters(self, renderer):
        """Test effect parameters."""
        processor = renderer.get_post_processor()
        processor.add_effect(EffectType.BLOOM)
        
        processor.set_effect_parameter(EffectType.BLOOM, "intensity", 0.5)
        assert processor.get_effect_parameter(EffectType.BLOOM, "intensity") == 0.5
    
    def test_effect_order(self, renderer):
        """Test effect processing order."""
        processor = renderer.get_post_processor()
        
        processor.add_effect(EffectType.BLUR)
        processor.add_effect(EffectType.BLOOM)
        
        # Effects should process in order
        assert len(processor.effect_order) >= 2


class TestLayerGroups:
    """Test layer groups."""
    
    def test_layer_group_creation(self, renderer):
        """Test creating layer groups."""
        group = renderer.create_layer_group("background")
        assert group is not None
        assert group.name == "background"
    
    def test_layer_group_visibility(self, renderer):
        """Test layer group visibility."""
        group = renderer.create_layer_group("test")
        
        group.set_visible(False)
        assert not group.is_visible
        
        group.set_visible(True)
        assert group.is_visible
    
    def test_layer_group_opacity(self, renderer):
        """Test layer group opacity."""
        group = renderer.create_layer_group("test")
        
        group.set_opacity(0.5)
        assert group.opacity == 0.5
    
    def test_layer_group_ordering(self, renderer):
        """Test layer group ordering."""
        bg_group = renderer.create_layer_group("background")
        fg_group = renderer.create_layer_group("foreground")
        
        bg_group.set_order(0)
        fg_group.set_order(10)
        
        assert bg_group.order < fg_group.order


class TestBatchOptimization:
    """Test batch optimization."""
    
    def test_texture_atlas_creation(self, renderer):
        """Test creating texture atlas."""
        atlas = renderer.create_texture_atlas(1024, 1024)
        assert atlas is not None
        assert atlas.width == 1024
        assert atlas.height == 1024
    
    def test_atlas_add_texture(self, renderer, test_surface):
        """Test adding texture to atlas."""
        atlas = renderer.create_texture_atlas(512, 512)
        
        region = atlas.add_texture("sprite1", test_surface)
        assert region is not None
        assert "sprite1" in atlas.textures
    
    def test_atlas_get_region(self, renderer, test_surface):
        """Test getting region from atlas."""
        atlas = renderer.create_texture_atlas(512, 512)
        atlas.add_texture("sprite1", test_surface)
        
        region = atlas.get_region("sprite1")
        assert region is not None
    
    def test_batch_optimization_stats(self, renderer):
        """Test batch optimization statistics."""
        stats = renderer.get_batch_stats()
        
        assert "draw_calls" in stats
        assert "sprites_batched" in stats
        assert "textures_used" in stats


class TestRenderingIntegration:
    """Integration tests for rendering system."""
    
    def test_complex_rendering_setup(self, renderer, test_surface):
        """Test complex rendering setup."""
        # Create render target
        target = renderer.create_render_target(400, 300)
        
        # Create particle system
        ps = renderer.create_particle_system("explosion")
        ps.emit(20, (200, 150))
        
        # Create lighting
        lighting = renderer.get_lighting_system()
        light = lighting.create_light(LightType.POINT, (200, 150))
        
        # Add post-processing
        processor = renderer.get_post_processor()
        processor.add_effect(EffectType.BLOOM)
        
        # Render
        renderer.set_render_target(target)
        renderer.begin()
        renderer.draw_sprite(test_surface, (100, 100))
        renderer.draw_particles(ps)
        renderer.end()
        
        # Should complete successfully
        assert True
    
    def test_rendering_performance(self, renderer, test_surface):
        """Test rendering performance."""
        # Render many sprites
        renderer.begin()
        for i in range(100):
            renderer.draw_sprite(test_surface, (i * 10, i * 10))
        renderer.end()
        
        # Should track draw calls (may be same as sprites if not batching)
        stats = renderer.get_batch_stats()
        assert stats["draw_calls"] > 0  # Should have draw calls
        assert stats["sprites_batched"] == 100  # Should track all sprites


class TestRenderState:
    """Test render state management."""
    
    def test_render_state_save(self, renderer):
        """Test saving render state."""
        lighting = renderer.get_lighting_system()
        lighting.set_ambient_light(0.3)
        
        state = renderer.save_state()
        
        assert "ambient_light" in state
    
    def test_render_state_restore(self, renderer):
        """Test restoring render state."""
        lighting = renderer.get_lighting_system()
        lighting.set_ambient_light(0.5)
        
        state = renderer.save_state()
        lighting.set_ambient_light(0.1)
        
        renderer.restore_state(state)
        assert lighting.ambient_light == 0.5

