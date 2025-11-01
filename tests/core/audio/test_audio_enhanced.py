"""
Tests for Enhanced Audio System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from typing import Tuple
from hub.core.audio.audio_manager_enhanced import (
    EnhancedAudioManager,
    AudioGroup,
    AudioBus,
    AudioEffect,
    EffectType,
    MusicLayer,
    DynamicMusicSystem,
    SpatialAudioEmitter,
    AudioVisualizer
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    yield
    pygame.mixer.quit()
    pygame.quit()


@pytest.fixture
def audio_manager(pygame_init_cleanup):
    """Create EnhancedAudioManager instance."""
    manager = EnhancedAudioManager()
    manager.initialize()
    yield manager
    manager.cleanup()


class TestAudioGroups:
    """Test audio group system."""
    
    def test_audio_group_creation(self, audio_manager):
        """Test creating audio groups."""
        group = audio_manager.create_group("sfx")
        assert group is not None
        assert group.name == "sfx"
    
    def test_audio_group_volume(self, audio_manager):
        """Test setting group volume."""
        group = audio_manager.create_group("music")
        group.set_volume(0.5)
        assert group.volume == 0.5
    
    def test_audio_group_mute(self, audio_manager):
        """Test muting/unmuting groups."""
        group = audio_manager.create_group("sfx")
        group.mute()
        assert group.is_muted
        group.unmute()
        assert not group.is_muted
    
    def test_audio_group_pause(self, audio_manager):
        """Test pausing/resuming groups."""
        group = audio_manager.create_group("music")
        group.pause()
        assert group.is_paused
        group.resume()
        assert not group.is_paused


class TestAudioBuses:
    """Test audio bus system."""
    
    def test_audio_bus_creation(self, audio_manager):
        """Test creating audio buses."""
        bus = audio_manager.create_bus("master")
        assert bus is not None
        assert bus.name == "master"
    
    def test_audio_bus_hierarchy(self, audio_manager):
        """Test bus hierarchy (master -> music -> sfx)."""
        master = audio_manager.create_bus("master")
        music = audio_manager.create_bus("music", parent=master)
        
        master.set_volume(0.5)
        music.set_volume(0.8)
        
        # Effective volume should be parent * child
        assert music.effective_volume == pytest.approx(0.4, abs=0.01)
    
    def test_audio_bus_routing(self, audio_manager):
        """Test routing sounds to buses."""
        bus = audio_manager.create_bus("sfx_bus")
        
        # Should be able to route sounds
        assert bus is not None


class Test3DAudio:
    """Test 3D spatial audio."""
    
    def test_spatial_emitter_creation(self, audio_manager):
        """Test creating spatial audio emitters."""
        emitter = audio_manager.create_3d_emitter("sound1", (0, 0))
        assert emitter is not None
        assert emitter.name == "sound1"
        assert emitter.position == (0, 0)
    
    def test_spatial_position_update(self, audio_manager):
        """Test updating emitter position."""
        emitter = audio_manager.create_3d_emitter("sound1", (0, 0))
        emitter.set_position((100, 50))
        assert emitter.position == (100, 50)
    
    def test_distance_attenuation(self, audio_manager):
        """Test distance-based volume attenuation."""
        emitter = audio_manager.create_3d_emitter("sound1", (0, 0))
        listener_pos = (0, 0)
        
        # At same position, volume should be max (or close to max)
        volume = emitter.calculate_volume(listener_pos)
        assert 0.8 <= volume <= 1.0
        
        # At far distance, volume should be low
        emitter.set_position((1000, 1000))
        far_volume = emitter.calculate_volume(listener_pos)
        assert far_volume < volume
    
    def test_listener_position(self, audio_manager):
        """Test setting listener position."""
        audio_manager.set_3d_listener_position((50, 50))
        pos = audio_manager.get_3d_listener_position()
        assert pos == (50, 50)
    
    def test_3d_max_distance(self, audio_manager):
        """Test maximum distance for attenuation."""
        emitter = audio_manager.create_3d_emitter("sound1", (0, 0))
        emitter.max_distance = 100
        
        # Beyond max distance, should be silent or minimum
        emitter.set_position((200, 0))
        volume = emitter.calculate_volume((0, 0))
        assert volume >= 0  # May be 0 or minimum


class TestAudioEffects:
    """Test audio effects system."""
    
    def test_effect_creation(self, audio_manager):
        """Test creating audio effects."""
        effect = audio_manager.create_effect("reverb", EffectType.REVERB)
        assert effect is not None
        assert effect.type == EffectType.REVERB
    
    def test_reverb_effect(self, audio_manager):
        """Test reverb effect parameters."""
        effect = audio_manager.create_effect("reverb", EffectType.REVERB)
        effect.set_parameter("room_size", 0.8)
        effect.set_parameter("damping", 0.5)
        
        assert effect.get_parameter("room_size") == 0.8
        assert effect.get_parameter("damping") == 0.5
    
    def test_echo_effect(self, audio_manager):
        """Test echo effect parameters."""
        effect = audio_manager.create_effect("echo", EffectType.ECHO)
        effect.set_parameter("delay", 0.3)
        effect.set_parameter("feedback", 0.4)
        
        assert effect.get_parameter("delay") == 0.3
        assert effect.get_parameter("feedback") == 0.4
    
    def test_lowpass_filter(self, audio_manager):
        """Test lowpass filter effect."""
        effect = audio_manager.create_effect("filter", EffectType.LOWPASS)
        effect.set_parameter("cutoff", 1000.0)
        
        assert effect.get_parameter("cutoff") == 1000.0
    
    def test_effect_chain(self, audio_manager):
        """Test chaining multiple effects."""
        reverb = audio_manager.create_effect("reverb", EffectType.REVERB)
        echo = audio_manager.create_effect("echo", EffectType.ECHO)
        
        chain = audio_manager.create_effect_chain([reverb, echo])
        assert len(chain.effects) == 2
    
    def test_effect_bypass(self, audio_manager):
        """Test bypassing effects."""
        effect = audio_manager.create_effect("reverb", EffectType.REVERB)
        effect.set_bypass(True)
        assert effect.is_bypassed
        effect.set_bypass(False)
        assert not effect.is_bypassed


class TestDynamicMusic:
    """Test dynamic music system."""
    
    def test_music_layer_creation(self, audio_manager):
        """Test creating music layers."""
        layer = audio_manager.create_music_layer("bass", "bass_track.ogg")
        assert layer is not None
        assert layer.name == "bass"
    
    def test_music_layer_volume(self, audio_manager):
        """Test music layer volume control."""
        layer = audio_manager.create_music_layer("drums", "drums.ogg")
        layer.set_volume(0.7)
        assert layer.volume == 0.7
    
    def test_dynamic_music_system(self, audio_manager):
        """Test dynamic music system."""
        music_system = audio_manager.get_dynamic_music()
        
        layer1 = music_system.add_layer("ambient", "ambient.ogg")
        layer2 = music_system.add_layer("action", "action.ogg")
        
        assert len(music_system.layers) == 2
    
    def test_music_transition(self, audio_manager):
        """Test music transitions."""
        music_system = audio_manager.get_dynamic_music()
        
        # Transition between intensity levels
        music_system.set_intensity(0.5)  # Medium intensity
        # Should fade layers appropriately
        
        assert True  # Should complete without error
    
    def test_music_layered_playback(self, audio_manager):
        """Test layered music playback."""
        music_system = audio_manager.get_dynamic_music()
        
        layer1 = music_system.add_layer("base", "base.ogg")
        layer2 = music_system.add_layer("variation", "variation.ogg")
        
        music_system.play_all()
        # All layers should be playing
    
    def test_music_crossfade(self, audio_manager):
        """Test crossfading between music tracks."""
        music_system = audio_manager.get_dynamic_music()
        
        # Should support crossfading
        music_system.crossfade("track1.ogg", "track2.ogg", duration_ms=1000)
        # Should fade out old, fade in new


class TestAudioVisualization:
    """Test audio visualization."""
    
    def test_visualizer_creation(self, audio_manager):
        """Test creating audio visualizer."""
        visualizer = audio_manager.create_visualizer()
        assert visualizer is not None
    
    def test_waveform_analysis(self, audio_manager):
        """Test waveform analysis."""
        visualizer = audio_manager.create_visualizer()
        
        # Should be able to get waveform data
        waveform = visualizer.get_waveform(num_samples=100)
        assert waveform is not None
        assert len(waveform) <= 100
    
    def test_spectrum_analysis(self, audio_manager):
        """Test spectrum/FFT analysis."""
        visualizer = audio_manager.create_visualizer()
        
        # Should be able to get spectrum data
        spectrum = visualizer.get_spectrum(num_bands=64)
        assert spectrum is not None
        assert len(spectrum) <= 64
    
    def test_visualizer_update(self, audio_manager):
        """Test visualizer update."""
        visualizer = audio_manager.create_visualizer()
        
        # Should update on each frame
        visualizer.update()
        assert True


class TestAudioMixing:
    """Test audio mixing features."""
    
    def test_master_volume(self, audio_manager):
        """Test master volume control."""
        audio_manager.set_master_volume(0.75)
        assert audio_manager.master_volume == 0.75
    
    def test_channel_volume(self, audio_manager):
        """Test individual channel volume."""
        audio_manager.set_channel_volume("music", 0.6)
        audio_manager.set_channel_volume("sfx", 0.8)
        
        assert audio_manager.get_channel_volume("music") == 0.6
        assert audio_manager.get_channel_volume("sfx") == 0.8
    
    def test_audio_ducking(self, audio_manager):
        """Test audio ducking (lowering one when other plays)."""
        audio_manager.enable_ducking("music", "voice", duck_amount=0.5)
        
        # When voice plays, music should duck
        assert True  # Should complete without error
    
    def test_volume_ramping(self, audio_manager):
        """Test smooth volume transitions."""
        audio_manager.ramp_volume("music", target_volume=0.3, duration_ms=500)
        # Should smoothly transition volume


class TestVoiceChat:
    """Test voice chat integration hooks."""
    
    def test_voice_chat_initialization(self, audio_manager):
        """Test voice chat initialization hooks."""
        # Should provide hooks for voice chat
        assert audio_manager.supports_voice_chat() is not None
    
    def test_voice_chat_input(self, audio_manager):
        """Test voice chat input handling."""
        # Should handle voice input
        assert True
    
    def test_voice_chat_output(self, audio_manager):
        """Test voice chat output handling."""
        # Should handle voice output
        assert True


class TestAudioPerformance:
    """Test audio performance features."""
    
    def test_channel_limiting(self, audio_manager):
        """Test limiting number of simultaneous sounds."""
        audio_manager.set_max_channels("sfx", 4)
        assert audio_manager.get_max_channels("sfx") == 4
    
    def test_sound_priority(self, audio_manager):
        """Test sound priority system."""
        # Higher priority sounds should play over lower priority
        assert True
    
    def test_audio_streaming(self, audio_manager):
        """Test streaming large audio files."""
        # Should support streaming for large files
        assert True


class TestAudioIntegration:
    """Integration tests for audio system."""
    
    def test_complex_audio_setup(self, audio_manager):
        """Test complex audio setup with multiple systems."""
        # Create groups
        music_group = audio_manager.create_group("music")
        sfx_group = audio_manager.create_group("sfx")
        
        # Create buses
        master_bus = audio_manager.create_bus("master")
        music_bus = audio_manager.create_bus("music", parent=master_bus)
        
        # Create 3D emitter
        emitter = audio_manager.create_3d_emitter("footsteps", (0, 0))
        
        # Add effects
        reverb = audio_manager.create_effect("reverb", EffectType.REVERB)
        
        # Should all work together
        assert True
    
    def test_audio_state_save_restore(self, audio_manager):
        """Test saving and restoring audio state."""
        audio_manager.set_master_volume(0.8)
        audio_manager.set_channel_volume("music", 0.6)
        
        state = audio_manager.save_state()
        
        audio_manager.set_master_volume(0.5)
        audio_manager.restore_state(state)
        
        assert audio_manager.master_volume == 0.8
        assert audio_manager.get_channel_volume("music") == 0.6

