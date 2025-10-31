"""
Integration tests for AudioManager.

Tests audio initialization with different configs, cleanup/reinitialization,
and integration with pygame mixer.
"""

import pytest
import pygame
from hub.core.audio.audio_manager import AudioManager


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


class TestAudioManagerInitialization:
    """Test AudioManager initialization."""
    
    def test_audio_manager_default_initialization(self, pygame_init_cleanup):
        """Test AudioManager with default parameters."""
        manager = AudioManager()
        assert not manager._initialized
        assert not manager._available
        
        result = manager.initialize()
        
        # May or may not be available depending on system
        assert manager._initialized
        if result:
            assert manager.available
    
    def test_audio_manager_custom_initialization(self, pygame_init_cleanup):
        """Test AudioManager with custom audio parameters."""
        manager = AudioManager(
            frequency=22050,
            size=-16,
            channels=1,
            buffer=1024
        )
        
        result = manager.initialize()
        assert manager._initialized
        if result:
            assert manager.available
    
    def test_audio_manager_initialization_idempotent(self, pygame_init_cleanup):
        """Test that initialization can be called multiple times safely."""
        manager = AudioManager()
        
        result1 = manager.initialize()
        result2 = manager.initialize()
        result3 = manager.initialize()
        
        # Should return same result
        assert result1 == result2 == result3
        assert manager._initialized
    
    def test_audio_manager_cleanup(self, pygame_init_cleanup):
        """Test AudioManager cleanup."""
        manager = AudioManager()
        manager.initialize()
        
        manager.cleanup()
        assert not manager._initialized
        assert not manager.available
    
    def test_audio_manager_cleanup_idempotent(self, pygame_init_cleanup):
        """Test that cleanup can be called multiple times safely."""
        manager = AudioManager()
        manager.initialize()
        
        manager.cleanup()
        manager.cleanup()  # Should not raise error
        manager.cleanup()  # Should not raise error
        
        assert not manager._initialized


class TestAudioManagerReinitialization:
    """Test AudioManager reinitialization after cleanup."""
    
    def test_audio_manager_reinitialization(self, pygame_init_cleanup):
        """Test that AudioManager can be reinitialized after cleanup."""
        manager = AudioManager()
        
        # First initialization
        result1 = manager.initialize()
        assert manager._initialized
        
        manager.cleanup()
        assert not manager._initialized
        
        # Second initialization
        result2 = manager.initialize()
        assert manager._initialized
        # Results may differ depending on system state
        
        manager.cleanup()
    
    def test_audio_manager_multiple_cycles(self, pygame_init_cleanup):
        """Test multiple initialization/cleanup cycles."""
        manager = AudioManager()
        
        for _ in range(3):
            manager.initialize()
            assert manager._initialized
            manager.cleanup()
            assert not manager._initialized


class TestAudioManagerConfiguration:
    """Test AudioManager with different configurations."""
    
    def test_audio_manager_low_frequency(self, pygame_init_cleanup):
        """Test AudioManager with lower frequency."""
        manager = AudioManager(frequency=22050)
        result = manager.initialize()
        assert manager._initialized
        
        if result:
            assert manager.frequency == 22050
        
        manager.cleanup()
    
    def test_audio_manager_mono(self, pygame_init_cleanup):
        """Test AudioManager with mono channel."""
        manager = AudioManager(channels=1)
        result = manager.initialize()
        assert manager._initialized
        
        manager.cleanup()
    
    def test_audio_manager_small_buffer(self, pygame_init_cleanup):
        """Test AudioManager with smaller buffer."""
        manager = AudioManager(buffer=1024)
        result = manager.initialize()
        assert manager._initialized
        
        manager.cleanup()
    
    def test_audio_manager_volume_control(self, pygame_init_cleanup):
        """Test AudioManager volume setting."""
        manager = AudioManager()
        if manager.initialize():
            # Test various volume levels
            manager.set_volume(0.0)
            manager.set_volume(0.5)
            manager.set_volume(1.0)
            manager.set_volume(1.5)  # Should clamp to 1.0
            manager.set_volume(-0.5)  # Should clamp to 0.0
            
            manager.cleanup()


class TestAudioManagerProperties:
    """Test AudioManager properties."""
    
    def test_audio_manager_available_property(self, pygame_init_cleanup):
        """Test available property."""
        manager = AudioManager()
        assert not manager.available
        
        manager.initialize()
        # Available depends on system
        
        manager.cleanup()
        assert not manager.available
    
    def test_audio_manager_frequency_property(self, pygame_init_cleanup):
        """Test frequency property."""
        manager = AudioManager(frequency=44100)
        if manager.initialize():
            freq = manager.frequency
            # May be None if audio not available, or 44100 if available
            if freq is not None:
                assert freq > 0
            
            manager.cleanup()


@pytest.mark.mobile
class TestAudioManagerMobile:
    """Test AudioManager mobile-specific scenarios."""
    
    def test_audio_manager_mobile_low_quality(self, pygame_init_cleanup):
        """
        Test AudioManager with mobile-appropriate low quality settings.
        
        Mobile devices may have audio limitations, so lower quality
        settings should still work.
        """
        manager = AudioManager(
            frequency=22050,  # Lower frequency for mobile
            channels=1,       # Mono for mobile
            buffer=1024      # Smaller buffer
        )
        
        result = manager.initialize()
        assert manager._initialized
        
        manager.cleanup()
    
    def test_audio_manager_mobile_cleanup_on_error(self, pygame_init_cleanup):
        """
        Test that AudioManager handles initialization errors gracefully.
        
        On mobile devices, audio may not always be available.
        Manager should handle this gracefully.
        """
        manager = AudioManager()
        
        # Try to initialize (may fail on headless systems)
        result = manager.initialize()
        
        # Should always be able to cleanup, even if init failed
        manager.cleanup()
        assert not manager._initialized


class TestAudioManagerIntegration:
    """Test AudioManager integration scenarios."""
    
    def test_audio_manager_with_multiple_instances(self, pygame_init_cleanup):
        """
        Test behavior with multiple AudioManager instances.
        
        Note: This test documents expected behavior.
        Multiple audio managers may or may not be supported.
        """
        manager1 = AudioManager()
        result1 = manager1.initialize()
        
        # Creating second manager
        manager2 = AudioManager()
        # Behavior depends on implementation - may fail or succeed
        
        manager1.cleanup()
        if result1:
            manager2.cleanup()

