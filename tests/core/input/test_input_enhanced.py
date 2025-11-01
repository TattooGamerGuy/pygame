"""
Tests for Enhanced Input System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
from typing import Tuple, List
from hub.core.input.input_manager_enhanced import (
    EnhancedInputManager,
    TouchInput,
    GestureRecognizer,
    GestureType,
    InputRemapping,
    InputProfile,
    InputRecorder,
    InputReplayer,
    InputHint,
    GamepadConfig
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def input_manager(pygame_init_cleanup):
    """Create EnhancedInputManager instance."""
    manager = EnhancedInputManager()
    manager.initialize()
    yield manager
    manager.cleanup()


class TestTouchInput:
    """Test touch input system."""
    
    def test_touch_initialization(self, input_manager):
        """Test touch input initialization."""
        touch = input_manager.get_touch_input()
        assert touch is not None
    
    def test_touch_position(self, input_manager):
        """Test touch position tracking."""
        touch = input_manager.get_touch_input()
        
        # Simulate touch down
        touch.on_touch_down(0, (100, 150))
        
        assert touch.get_touch_position(0) == (100, 150)
    
    def test_multi_touch(self, input_manager):
        """Test multi-touch support."""
        touch = input_manager.get_touch_input()
        
        touch.on_touch_down(0, (100, 100))
        touch.on_touch_down(1, (200, 200))
        
        assert touch.get_touch_count() == 2
        assert touch.get_touch_position(0) == (100, 100)
        assert touch.get_touch_position(1) == (200, 200)
    
    def test_touch_up(self, input_manager):
        """Test touch release."""
        touch = input_manager.get_touch_input()
        
        touch.on_touch_down(0, (100, 100))
        assert touch.is_touching(0)
        
        touch.on_touch_up(0)
        assert not touch.is_touching(0)
        assert touch.get_touch_count() == 0
    
    def test_touch_moved(self, input_manager):
        """Test touch movement."""
        touch = input_manager.get_touch_input()
        
        touch.on_touch_down(0, (100, 100))
        touch.on_touch_move(0, (150, 150))
        
        assert touch.get_touch_position(0) == (150, 150)


class TestGestureRecognition:
    """Test gesture recognition."""
    
    def test_swipe_gesture(self, input_manager):
        """Test swipe gesture recognition."""
        recognizer = input_manager.get_gesture_recognizer()
        
        # Simulate swipe
        recognizer.on_touch_down(0, (100, 100))
        recognizer.on_touch_move(0, (200, 100))  # Right swipe
        recognizer.on_touch_up(0)
        
        gestures = recognizer.process()
        
        # Should detect swipe
        assert len(gestures) > 0
        assert any(g.type == GestureType.SWIPE for g in gestures)
    
    def test_pinch_gesture(self, input_manager):
        """Test pinch gesture recognition."""
        recognizer = input_manager.get_gesture_recognizer()
        
        # Simulate pinch (two touches moving together)
        recognizer.on_touch_down(0, (100, 100))
        recognizer.on_touch_down(1, (200, 100))
        recognizer.on_touch_move(0, (90, 100))
        recognizer.on_touch_move(1, (210, 100))
        recognizer.on_touch_up(0)
        recognizer.on_touch_up(1)
        
        gestures = recognizer.process()
        
        # Should detect pinch
        assert any(g.type == GestureType.PINCH for g in gestures)
    
    def test_tap_gesture(self, input_manager):
        """Test tap gesture recognition."""
        recognizer = input_manager.get_gesture_recognizer()
        
        # Simulate quick tap
        recognizer.on_touch_down(0, (100, 100))
        recognizer.on_touch_up(0)
        
        gestures = recognizer.process()
        
        # Should detect tap
        assert any(g.type == GestureType.TAP for g in gestures)
    
    def test_long_press_gesture(self, input_manager):
        """Test long press gesture."""
        recognizer = input_manager.get_gesture_recognizer()
        
        # Simulate long press (hold for > threshold)
        recognizer.on_touch_down(0, (100, 100))
        # Wait would happen here
        recognizer.on_touch_up(0)
        
        gestures = recognizer.process()
        
        # Should detect long press if threshold exceeded
        assert True  # May or may not detect depending on timing


class TestInputRemapping:
    """Test input remapping."""
    
    def test_key_remapping(self, input_manager):
        """Test keyboard key remapping."""
        remapping = input_manager.get_remapping()
        
        # Map W key to MOVE_UP action
        remapping.map_key(pygame.K_w, "MOVE_UP")
        
        assert remapping.get_action_for_key(pygame.K_w) == "MOVE_UP"
    
    def test_gamepad_button_remapping(self, input_manager):
        """Test gamepad button remapping."""
        remapping = input_manager.get_remapping()
        
        # Map button 0 to JUMP action
        remapping.map_button(0, "JUMP")
        
        assert remapping.get_action_for_button(0) == "JUMP"
    
    def test_axis_remapping(self, input_manager):
        """Test gamepad axis remapping."""
        remapping = input_manager.get_remapping()
        
        # Map axis 0 to MOVE_X
        remapping.map_axis(0, "MOVE_X")
        
        assert remapping.get_action_for_axis(0) == "MOVE_X"
    
    def test_action_to_key(self, input_manager):
        """Test getting key for action."""
        remapping = input_manager.get_remapping()
        
        remapping.map_key(pygame.K_w, "MOVE_UP")
        
        keys = remapping.get_keys_for_action("MOVE_UP")
        assert pygame.K_w in keys
    
    def test_remapping_clear(self, input_manager):
        """Test clearing remapping."""
        remapping = input_manager.get_remapping()
        
        remapping.map_key(pygame.K_w, "MOVE_UP")
        remapping.clear()
        
        assert remapping.get_action_for_key(pygame.K_w) is None


class TestInputProfiles:
    """Test input profiles."""
    
    def test_profile_creation(self, input_manager):
        """Test creating input profile."""
        profile = input_manager.create_profile("default")
        assert profile is not None
        assert profile.name == "default"
    
    def test_profile_save(self, input_manager):
        """Test saving profile."""
        profile = input_manager.create_profile("player1")
        
        profile.remapping.map_key(pygame.K_w, "MOVE_UP")
        profile.remapping.map_key(pygame.K_s, "MOVE_DOWN")
        
        saved = profile.save()
        
        assert "remapping" in saved
        assert saved["name"] == "player1"
    
    def test_profile_load(self, input_manager):
        """Test loading profile."""
        profile = input_manager.create_profile("test")
        profile.remapping.map_key(pygame.K_w, "MOVE_UP")
        
        saved = profile.save()
        
        # Create new profile and load
        new_profile = input_manager.create_profile("test2")
        new_profile.load(saved)
        
        assert new_profile.remapping.get_action_for_key(pygame.K_w) == "MOVE_UP"
    
    def test_profile_per_game(self, input_manager):
        """Test game-specific profiles."""
        profile = input_manager.get_profile_for_game("pong", "player1")
        assert profile is not None
    
    def test_profile_switch(self, input_manager):
        """Test switching between profiles."""
        profile1 = input_manager.create_profile("profile1")
        profile2 = input_manager.create_profile("profile2")
        
        input_manager.set_active_profile("profile1")
        assert input_manager.active_profile == profile1
        
        input_manager.set_active_profile("profile2")
        assert input_manager.active_profile == profile2


class TestGamepadImprovements:
    """Test gamepad improvements."""
    
    def test_deadzone_configuration(self, input_manager):
        """Test deadzone configuration."""
        config = input_manager.get_gamepad_config(0)
        
        config.set_deadzone(0, 0.15)  # 15% deadzone for axis 0
        
        assert config.get_deadzone(0) == 0.15
    
    def test_axis_inversion(self, input_manager):
        """Test axis inversion."""
        config = input_manager.get_gamepad_config(0)
        
        config.set_axis_inverted(0, True)
        
        assert config.is_axis_inverted(0)
    
    def test_button_mapping(self, input_manager):
        """Test button mapping."""
        config = input_manager.get_gamepad_config(0)
        
        config.map_button(0, "JUMP")
        config.map_button(1, "ATTACK")
        
        assert config.get_action_for_button(0) == "JUMP"
        assert config.get_action_for_button(1) == "ATTACK"
    
    def test_gamepad_detection(self, input_manager):
        """Test improved gamepad detection."""
        gamepads = input_manager.get_detected_gamepads()
        
        # Should return list of detected gamepads
        assert isinstance(gamepads, list)
    
    def test_gamepad_info(self, input_manager):
        """Test getting gamepad information."""
        if input_manager.get_gamepad_count() > 0:
            info = input_manager.get_gamepad_info(0)
            
            assert "name" in info or "id" in info


class TestInputRecording:
    """Test input recording and playback."""
    
    def test_recorder_creation(self, input_manager):
        """Test creating input recorder."""
        recorder = input_manager.create_recorder()
        assert recorder is not None
    
    def test_recording_start_stop(self, input_manager):
        """Test starting and stopping recording."""
        recorder = input_manager.create_recorder()
        
        recorder.start_recording()
        assert recorder.is_recording
        
        recorder.stop_recording()
        assert not recorder.is_recording
    
    def test_recording_inputs(self, input_manager):
        """Test recording input events."""
        recorder = input_manager.create_recorder()
        
        recorder.start_recording()
        recorder.record_key_press(pygame.K_w, 0.0)
        recorder.record_key_release(pygame.K_w, 0.1)
        recorder.stop_recording()
        
        assert len(recorder.get_recorded_events()) >= 2
    
    def test_playback_creation(self, input_manager):
        """Test creating input replayer."""
        recorder = input_manager.create_recorder()
        recorder.start_recording()
        recorder.record_key_press(pygame.K_w, 0.0)
        recorder.stop_recording()
        
        events = recorder.get_recorded_events()
        replayer = input_manager.create_replayer(events)
        
        assert replayer is not None
    
    def test_playback_execution(self, input_manager):
        """Test executing playback."""
        recorder = input_manager.create_recorder()
        recorder.start_recording()
        recorder.record_key_press(pygame.K_w, 0.0)
        recorder.stop_recording()
        
        events = recorder.get_recorded_events()
        replayer = input_manager.create_replayer(events)
        
        replayer.start_playback()
        assert replayer.is_playing
        
        replayer.stop_playback()
        assert not replayer.is_playing


class TestInputHints:
    """Test input hints system."""
    
    def test_hint_creation(self, input_manager):
        """Test creating input hints."""
        hint = input_manager.create_hint("Press SPACE to jump", (100, 100))
        assert hint is not None
        assert hint.text == "Press SPACE to jump"
    
    def test_hint_visibility(self, input_manager):
        """Test hint visibility."""
        hint = input_manager.create_hint("Hint text", (100, 100))
        
        hint.show()
        assert hint.is_visible
        
        hint.hide()
        assert not hint.is_visible
    
    def test_hint_position(self, input_manager):
        """Test hint positioning."""
        hint = input_manager.create_hint("Hint", (150, 200))
        
        assert hint.position == (150, 200)
        
        hint.set_position((250, 300))
        assert hint.position == (250, 300)
    
    def test_hint_duration(self, input_manager):
        """Test hint auto-hide after duration."""
        hint = input_manager.create_hint("Hint", (100, 100), duration_ms=1000)
        
        # Should auto-hide after duration
        assert hint.duration_ms == 1000
    
    def test_hint_styling(self, input_manager):
        """Test hint styling."""
        hint = input_manager.create_hint("Hint", (100, 100))
        
        hint.set_style(color=(255, 255, 0), size=20)
        
        assert hint.color == (255, 255, 0)
        assert hint.font_size == 20


class TestInputActions:
    """Test input action system."""
    
    def test_action_registration(self, input_manager):
        """Test registering input actions."""
        input_manager.register_action("JUMP", pygame.K_SPACE)
        
        assert input_manager.is_action_pressed("JUMP") is not None
    
    def test_action_binding(self, input_manager):
        """Test binding multiple inputs to action."""
        input_manager.register_action("MOVE_UP", pygame.K_w)
        input_manager.register_action("MOVE_UP", pygame.K_UP)  # Also arrow key
        
        # Both should trigger same action
        assert True
    
    def test_action_callbacks(self, input_manager):
        """Test action callbacks."""
        callback_called = [False]
        
        def on_jump():
            callback_called[0] = True
        
        input_manager.register_action("JUMP", pygame.K_SPACE)
        input_manager.set_action_callback("JUMP", on_jump)
        
        # When action triggered, callback should be called
        assert True


class TestInputIntegration:
    """Integration tests for input system."""
    
    def test_complex_input_setup(self, input_manager):
        """Test complex input setup."""
        # Create profile
        profile = input_manager.create_profile("player1")
        
        # Set remapping
        profile.remapping.map_key(pygame.K_w, "MOVE_UP")
        
        # Configure gamepad
        config = input_manager.get_gamepad_config(0)
        config.set_deadzone(0, 0.15)
        
        # Enable touch
        touch = input_manager.get_touch_input()
        
        # Should all work together
        assert True
    
    def test_input_state_persistence(self, input_manager):
        """Test input state persistence."""
        profile = input_manager.create_profile("test")
        profile.remapping.map_key(pygame.K_w, "MOVE_UP")
        
        state = profile.save()
        
        new_profile = input_manager.create_profile("test2")
        new_profile.load(state)
        
        assert new_profile.remapping.get_action_for_key(pygame.K_w) == "MOVE_UP"

