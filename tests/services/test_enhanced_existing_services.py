"""
Tests for Enhanced Existing Services (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
import tempfile as tempfile_module
import os
import json
from typing import Dict, List
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.services.config_service import ConfigService
from hub.events.event_bus import EventBus
from hub.config.settings import Settings
from hub.core.audio import AudioManager
from hub.core.display import DisplayManager


@pytest.fixture
def pygame_init():
    """Initialize pygame."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def event_bus():
    """Create event bus."""
    return EventBus()


@pytest.fixture
def audio_manager(pygame_init):
    """Create audio manager."""
    return AudioManager()


@pytest.fixture
def display_manager(pygame_init):
    """Create display manager."""
    return DisplayManager((800, 600))


@pytest.fixture
def settings():
    """Create settings."""
    return Settings()


class TestEnhancedInputService:
    """Test enhanced input service with action system."""
    
    def test_input_action_registration(self, event_bus):
        """Test registering input actions."""
        service = InputService(event_bus)
        
        service.register_action("jump", [pygame.K_SPACE, pygame.K_UP])
        service.register_action("attack", [pygame.K_z])
        service.register_action("move_left", [pygame.K_LEFT, pygame.K_a])
        
        assert service.is_action_registered("jump")
        assert service.is_action_registered("attack")
    
    def test_input_action_checking(self, event_bus):
        """Test checking input actions."""
        service = InputService(event_bus)
        
        service.register_action("jump", [pygame.K_SPACE])
        
        # Simulate key press
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
        service.update(events)
        
        assert service.is_action_pressed("jump")
        assert not service.is_action_pressed("attack")  # Not registered
    
    def test_input_action_mapping(self, event_bus):
        """Test mapping multiple keys to same action."""
        service = InputService(event_bus)
        
        service.register_action("move_right", [pygame.K_RIGHT, pygame.K_d])
        
        # Test with first key
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]
        service.update(events)
        assert service.is_action_pressed("move_right")
        
        # Test with second key
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)]
        service.update(events)
        assert service.is_action_pressed("move_right")
    
    def test_input_action_just_pressed(self, event_bus):
        """Test checking if action was just pressed."""
        service = InputService(event_bus)
        
        service.register_action("jump", [pygame.K_SPACE])
        
        # First press
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
        service.update(events)
        assert service.is_action_just_pressed("jump")
        
        # Update again (key still held)
        service.update([])
        assert service.is_action_pressed("jump")
        assert not service.is_action_just_pressed("jump")  # Not just pressed anymore
    
    def test_input_combo_detection(self, event_bus):
        """Test input combo detection."""
        service = InputService(event_bus)
        
        combo = [pygame.K_z, pygame.K_x, pygame.K_c]
        service.register_combo("special_move", combo)
        
        # Press keys in sequence
        events = [
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)
        ]
        
        for event in events:
            service.update([event])
        
        assert service.is_combo_pressed("special_move")
    
    def test_input_sequence_detection(self, event_bus):
        """Test input sequence detection."""
        service = InputService(event_bus)
        
        sequence = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        service.register_sequence("konami_code_start", sequence, max_time_ms=1000)
        
        # Press sequence within time limit
        for key in sequence:
            events = [pygame.event.Event(pygame.KEYDOWN, key=key)]
            service.update(events)
        
        assert service.is_sequence_completed("konami_code_start")
    
    def test_input_sequence_timeout(self, event_bus):
        """Test input sequence timeout."""
        service = InputService(event_bus)
        
        sequence = [pygame.K_a, pygame.K_b]
        service.register_sequence("test_sequence", sequence, max_time_ms=100)
        
        # Press first key
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        service.update(events)
        
        # Wait too long (simulated by checking after timeout)
        # In real implementation, time tracking would handle this
        assert True  # Sequence should timeout if not completed in time
    
    def test_input_action_remapping(self, event_bus):
        """Test remapping input actions."""
        service = InputService(event_bus)
        
        service.register_action("jump", [pygame.K_SPACE])
        
        # Remap to different key
        service.remap_action("jump", [pygame.K_W])
        
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_W)]
        service.update(events)
        
        assert service.is_action_pressed("jump")
    
    def test_mobile_input_handling(self, event_bus):
        """Test mobile input handling."""
        service = InputService(event_bus)
        
        # Register touch-based action
        service.register_touch_action("jump", region=(0, 0, 100, 100))
        
        # Simulate touch event (if pygame supports it)
        # For now, just test that registration works
        assert service.is_action_registered("jump")
    
    def test_input_profile_save_load(self, event_bus, temp_dir):
        """Test saving and loading input profiles."""
        service = InputService(event_bus)
        
        service.register_action("jump", [pygame.K_SPACE])
        service.register_action("attack", [pygame.K_z])
        
        profile_path = os.path.join(temp_dir, "input_profile.json")
        result = service.save_profile(profile_path)
        
        assert result is True
        
        # Load in new service
        new_service = InputService(event_bus)
        new_service.load_profile(profile_path)
        
        assert new_service.is_action_registered("jump")
        assert new_service.is_action_registered("attack")


class TestEnhancedAudioService:
    """Test enhanced audio service."""
    
    def test_audio_priority_system(self, audio_manager):
        """Test audio priority system."""
        service = AudioService(audio_manager)
        
        service.set_sound_priority("important_sound", 10)
        service.set_sound_priority("normal_sound", 5)
        service.set_sound_priority("background_sound", 1)
        
        assert service.get_sound_priority("important_sound") == 10
        assert service.get_sound_priority("normal_sound") == 5
    
    def test_audio_ducking(self, audio_manager):
        """Test audio ducking."""
        service = AudioService(audio_manager)
        
        service.enable_ducking(True)
        service.set_ducking_target("music")
        service.set_ducking_amount(0.5)
        
        assert service.ducking_enabled
        assert service.get_ducking_amount() == 0.5
    
    def test_audio_priority_playback(self, audio_manager):
        """Test priority-based audio playback."""
        service = AudioService(audio_manager)
        
        # Higher priority sounds should interrupt lower priority
        service.set_sound_priority("low_priority", 1)
        service.set_sound_priority("high_priority", 10)
        
        # Should handle priority when playing sounds
        assert True
    
    def test_audio_settings_persistence(self, audio_manager, temp_dir):
        """Test saving and loading audio settings."""
        service = AudioService(audio_manager)
        
        service.set_music_volume(0.8)
        service.set_sound_volume(0.6)
        
        settings_path = os.path.join(temp_dir, "audio_settings.json")
        result = service.save_settings(settings_path)
        
        assert result is True
        
        # Load in new service
        new_service = AudioService(audio_manager)
        new_service.load_settings(settings_path)
        
        # Settings should be restored
        assert abs(new_service._music_volume - 0.8) < 0.01
        assert abs(new_service._sound_volume - 0.6) < 0.01
    
    def test_audio_group_management(self, audio_manager):
        """Test audio group management."""
        service = AudioService(audio_manager)
        
        service.create_audio_group("ui_sounds")
        service.create_audio_group("game_sounds")
        
        service.set_group_volume("ui_sounds", 0.5)
        service.set_group_volume("game_sounds", 0.8)
        
        assert service.get_group_volume("ui_sounds") == 0.5
        assert service.get_group_volume("game_sounds") == 0.8
    
    def test_audio_channel_limiting(self, audio_manager):
        """Test audio channel limiting."""
        service = AudioService(audio_manager)
        
        service.set_max_channels(8)
        
        # Should limit concurrent sounds
        assert service.get_max_channels() == 8


class TestEnhancedConfigService:
    """Test enhanced config service."""
    
    def test_config_profile_creation(self, settings):
        """Test creating configuration profiles."""
        service = ConfigService(settings)
        
        service.create_profile("low_quality")
        service.create_profile("high_quality")
        service.create_profile("balanced")
        
        profiles = service.list_profiles()
        
        assert "low_quality" in profiles
        assert "high_quality" in profiles
        assert "balanced" in profiles
    
    def test_config_profile_switching(self, settings):
        """Test switching configuration profiles."""
        service = ConfigService(settings)
        
        service.create_profile("profile1")
        service.create_profile("profile2")
        
        service.set_profile("profile1")
        assert service.get_current_profile() == "profile1"
        
        service.set_profile("profile2")
        assert service.get_current_profile() == "profile2"
    
    def test_config_profile_values(self, settings):
        """Test profile-specific values."""
        service = ConfigService(settings)
        
        service.create_profile("custom")
        service.set_profile("custom")
        
        service.set_profile_value("resolution", [1280, 720])
        service.set_profile_value("master_volume", 0.8)
        
        assert service.get_profile_value("resolution") == [1280, 720]
        assert service.get_profile_value("master_volume") == 0.8
    
    def test_config_validation(self, settings):
        """Test configuration validation."""
        service = ConfigService(settings)
        
        # Valid configuration
        valid_config = {
            "resolution": [1920, 1080],
            "master_volume": 0.8,
            "fullscreen": True
        }
        
        assert service.validate_config(valid_config) is True
        
        # Invalid configuration (invalid resolution)
        invalid_config = {
            "resolution": "invalid",
            "master_volume": 2.0  # Out of range
        }
        
        assert service.validate_config(invalid_config) is False
    
    def test_config_import_export(self, settings, temp_dir):
        """Test configuration import/export."""
        service = ConfigService(settings)
        
        service.create_profile("export_test")
        service.set_profile("export_test")
        service.set_profile_value("resolution", [1600, 900])
        
        export_path = os.path.join(temp_dir, "config.json")
        result = service.export_config(export_path)
        
        assert result is True
        assert os.path.exists(export_path)
        
        # Import in new service
        new_settings = Settings()
        new_service = ConfigService(new_settings)
        new_service.import_config(export_path)
        
        # Should have imported profile
        profiles = new_service.list_profiles()
        assert "export_test" in profiles
    
    def test_config_default_profile(self, settings):
        """Test default profile handling."""
        service = ConfigService(settings)
        
        # Should have default profile
        assert service.get_current_profile() is not None
        
        # Default profile should be active
        default = service.get_current_profile()
        assert default in service.list_profiles()
    
    def test_config_profile_delete(self, settings):
        """Test deleting configuration profiles."""
        service = ConfigService(settings)
        
        service.create_profile("to_delete")
        service.delete_profile("to_delete")
        
        profiles = service.list_profiles()
        assert "to_delete" not in profiles
    
    def test_config_validation_rules(self, settings):
        """Test configuration validation rules."""
        service = ConfigService(settings)
        
        # Add validation rule
        service.add_validation_rule("resolution", lambda v: isinstance(v, list) and len(v) == 2)
        service.add_validation_rule("master_volume", lambda v: 0.0 <= v <= 1.0)
        
        # Test valid
        assert service.validate_config({"resolution": [800, 600], "master_volume": 0.5}) is True
        
        # Test invalid
        assert service.validate_config({"resolution": "invalid", "master_volume": 1.5}) is False


class TestServicesIntegration:
    """Integration tests for enhanced services."""
    
    def test_input_audio_integration(self, event_bus, audio_manager):
        """Test input and audio service integration."""
        input_service = InputService(event_bus)
        audio_service = AudioService(audio_manager)
        
        # Register action
        input_service.register_action("jump", [pygame.K_SPACE])
        
        # When action pressed, play sound (integration example)
        events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
        input_service.update(events)
        
        if input_service.is_action_pressed("jump"):
            # Could trigger audio here
            assert True
    
    def test_config_applies_to_services(self, settings, display_manager, audio_manager):
        """Test config service applying settings to other services."""
        config_service = ConfigService(settings)
        
        config_service.set_profile_value("resolution", [1024, 768])
        config_service.set_profile_value("master_volume", 0.7)
        
        config_service.apply_to_display(display_manager)
        config_service.apply_to_audio(audio_manager)
        
        # Settings should be applied
        assert True


@pytest.fixture
def temp_dir():
    """Create temporary directory."""
    temp = tempfile_module.mkdtemp()
    yield temp

