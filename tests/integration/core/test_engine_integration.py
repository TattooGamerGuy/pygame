"""
Integration tests for GameEngine.

Tests engine initialization with all systems, cleanup, tick/delta time,
and integration scenarios.
"""

import pytest
import pygame
from hub.core.engine import GameEngine
from hub.core.display.display_manager import DisplayManager
from hub.core.audio.audio_manager import AudioManager
from hub.core.timing.clock_manager import ClockManager


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


class TestEngineInitialization:
    """Test GameEngine initialization."""
    
    def test_engine_default_initialization(self, pygame_init_cleanup):
        """Test GameEngine with default managers."""
        engine = GameEngine()
        assert not engine._initialized
        assert engine.display is not None
        assert engine.audio is not None
        assert engine.clock is not None
        
        engine.initialize()
        assert engine._initialized
        
        engine.cleanup()
    
    def test_engine_custom_managers(self, pygame_init_cleanup):
        """Test GameEngine with custom managers."""
        display = DisplayManager(size=(800, 600))
        audio = AudioManager()
        clock = ClockManager(target_fps=30)
        
        engine = GameEngine(
            display_manager=display,
            audio_manager=audio,
            clock_manager=clock
        )
        
        assert engine.display == display
        assert engine.audio == audio
        assert engine.clock == clock
        
        engine.initialize()
        assert engine._initialized
        
        engine.cleanup()
    
    def test_engine_initialization_idempotent(self, pygame_init_cleanup):
        """Test that initialization can be called multiple times safely."""
        engine = GameEngine()
        
        engine.initialize()
        assert engine._initialized
        
        engine.initialize()  # Should not break
        engine.initialize()  # Should not break
        
        assert engine._initialized
        engine.cleanup()


class TestEngineCleanup:
    """Test GameEngine cleanup."""
    
    def test_engine_cleanup(self, pygame_init_cleanup):
        """Test engine cleanup."""
        engine = GameEngine()
        engine.initialize()
        
        engine.cleanup()
        assert not engine._initialized
    
    def test_engine_cleanup_idempotent(self, pygame_init_cleanup):
        """Test that cleanup can be called multiple times safely."""
        engine = GameEngine()
        engine.initialize()
        
        engine.cleanup()
        engine.cleanup()  # Should not raise error
        engine.cleanup()  # Should not raise error
    
    def test_engine_reinitialization(self, pygame_init_cleanup):
        """Test engine can be reinitialized after cleanup."""
        engine = GameEngine()
        
        # First cycle
        engine.initialize()
        assert engine._initialized
        engine.cleanup()
        assert not engine._initialized
        
        # Second cycle
        engine.initialize()
        assert engine._initialized
        engine.cleanup()


class TestEngineRunning:
    """Test engine running state."""
    
    def test_engine_running_property(self, pygame_init_cleanup):
        """Test engine running property."""
        engine = GameEngine()
        engine.initialize()
        
        assert not engine.running
        engine.running = True
        assert engine.running
        
        engine.running = False
        assert not engine.running
        
        engine.cleanup()
    
    def test_engine_running_setter(self, pygame_init_cleanup):
        """Test setting engine running state."""
        engine = GameEngine()
        engine.initialize()
        
        engine.running = True
        assert engine._running
        
        engine.running = False
        assert not engine._running
        
        engine.cleanup()


class TestEngineTick:
    """Test engine tick functionality."""
    
    def test_engine_tick(self, pygame_init_cleanup):
        """Test engine tick returns delta time."""
        engine = GameEngine()
        engine.initialize()
        
        dt = engine.tick()
        assert dt >= 0.0
        assert dt < 1.0  # Should be reasonable
        
        engine.cleanup()
    
    def test_engine_multiple_ticks(self, pygame_init_cleanup):
        """Test multiple engine ticks."""
        engine = GameEngine()
        engine.initialize()
        
        delta_times = []
        for _ in range(10):
            dt = engine.tick()
            delta_times.append(dt)
        
        # All delta times should be reasonable
        for dt in delta_times:
            assert dt >= 0.0
            assert dt < 0.5  # Capped to prevent large jumps
        
        engine.cleanup()


class TestEngineSystemIntegration:
    """Test engine integration with all systems."""
    
    def test_engine_display_integration(self, pygame_init_cleanup):
        """Test engine properly initializes display."""
        engine = GameEngine()
        engine.initialize()
        
        # Display should be initialized
        assert engine.display._initialized
        assert engine.display.screen is not None
        
        engine.cleanup()
    
    def test_engine_audio_integration(self, pygame_init_cleanup):
        """Test engine properly initializes audio."""
        engine = GameEngine()
        engine.initialize()
        
        # Audio should be initialized
        assert engine.audio._initialized
        
        engine.cleanup()
    
    def test_engine_clock_integration(self, pygame_init_cleanup):
        """Test engine properly initializes clock."""
        engine = GameEngine()
        engine.initialize()
        
        # Clock should be available
        assert engine.clock is not None
        
        # Test tick through engine
        dt = engine.tick()
        assert dt >= 0.0
        
        engine.cleanup()


@pytest.mark.mobile
class TestEngineMobileIntegration:
    """Test engine integration with mobile scenarios."""
    
    def test_engine_mobile_resolution(self, pygame_init_cleanup):
        """Test engine with mobile resolution."""
        display = DisplayManager(size=(390, 844))  # iPhone 12
        engine = GameEngine(display_manager=display)
        
        engine.initialize()
        assert engine.display.size == (390, 844)
        
        engine.cleanup()
    
    def test_engine_mobile_fps_target(self, pygame_init_cleanup):
        """Test engine with mobile FPS target."""
        clock = ClockManager(target_fps=30)
        engine = GameEngine(clock_manager=clock)
        
        engine.initialize()
        assert engine.clock.target_fps == 30
        
        engine.cleanup()


class TestEngineEdgeCases:
    """Test engine edge cases."""
    
    def test_engine_multiple_instances(self, pygame_init_cleanup):
        """
        Test behavior with multiple engine instances.
        
        Note: This test documents expected behavior.
        Multiple engines may or may not be supported.
        """
        engine1 = GameEngine()
        engine1.initialize()
        
        # Creating second engine
        engine2 = GameEngine()
        # Behavior depends on implementation
        
        engine1.cleanup()
        engine2.cleanup()


class TestEngineFullCycle:
    """Test complete engine lifecycle."""
    
    def test_engine_full_lifecycle(self, pygame_init_cleanup):
        """Test complete engine lifecycle."""
        engine = GameEngine()
        
        # Initialize
        engine.initialize()
        assert engine._initialized
        
        # Run loop
        engine.running = True
        for _ in range(5):
            if engine.running:
                dt = engine.tick()
                assert dt >= 0.0
        
        # Cleanup
        engine.cleanup()
        assert not engine._initialized

