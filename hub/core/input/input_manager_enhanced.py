"""
Enhanced input system management.

Supports touch input, gesture recognition, input remapping, profiles,
recording/playback, input hints, and improved gamepad handling.
"""

from typing import Dict, List, Optional, Tuple, Set, Callable, Any
from enum import Enum
from dataclasses import dataclass, field
import pygame
import time
import json
import math


class GestureType(Enum):
    """Gesture types."""
    TAP = "tap"
    LONG_PRESS = "long_press"
    SWIPE = "swipe"
    PINCH = "pinch"
    ROTATE = "rotate"
    DRAG = "drag"


@dataclass
class Gesture:
    """Gesture data."""
    type: GestureType
    position: Tuple[float, float]
    start_position: Tuple[float, float]
    end_position: Tuple[float, float]
    distance: float = 0.0
    direction: Tuple[float, float] = (0.0, 0.0)
    duration: float = 0.0
    touch_id: int = 0


class TouchInput:
    """Multi-touch input handler."""
    
    def __init__(self):
        """Initialize touch input."""
        self._touches: Dict[int, Tuple[float, float]] = {}
        self._touch_start_times: Dict[int, float] = {}
    
    def on_touch_down(self, touch_id: int, position: Tuple[float, float]) -> None:
        """Handle touch down."""
        self._touches[touch_id] = position
        self._touch_start_times[touch_id] = time.time()
    
    def on_touch_up(self, touch_id: int) -> None:
        """Handle touch up."""
        if touch_id in self._touches:
            del self._touches[touch_id]
        if touch_id in self._touch_start_times:
            del self._touch_start_times[touch_id]
    
    def on_touch_move(self, touch_id: int, position: Tuple[float, float]) -> None:
        """Handle touch move."""
        if touch_id in self._touches:
            self._touches[touch_id] = position
    
    def get_touch_position(self, touch_id: int) -> Optional[Tuple[float, float]]:
        """Get touch position."""
        return self._touches.get(touch_id)
    
    def is_touching(self, touch_id: int) -> bool:
        """Check if touch is active."""
        return touch_id in self._touches
    
    def get_touch_count(self) -> int:
        """Get number of active touches."""
        return len(self._touches)
    
    def get_all_touches(self) -> Dict[int, Tuple[float, float]]:
        """Get all active touches."""
        return self._touches.copy()


class GestureRecognizer:
    """Gesture recognition system."""
    
    def __init__(self):
        """Initialize gesture recognizer."""
        self._touch_input = TouchInput()
        self._gesture_history: List[Gesture] = []
        self._touch_start_positions: Dict[int, Tuple[float, float]] = {}
        self._touch_end_positions: Dict[int, Tuple[float, float]] = {}
        self._swipe_threshold = 50.0  # Minimum distance for swipe
        self._tap_max_duration = 0.3  # Max duration for tap (seconds)
        self._long_press_duration = 0.5  # Duration for long press
        self._pinch_threshold = 20.0  # Minimum distance change for pinch
    
    def on_touch_down(self, touch_id: int, position: Tuple[float, float]) -> None:
        """Handle touch down."""
        self._touch_input.on_touch_down(touch_id, position)
        self._touch_start_positions[touch_id] = position
        self._touch_end_positions[touch_id] = position
    
    def on_touch_up(self, touch_id: int) -> None:
        """Handle touch up."""
        # Detect gesture when touch ends
        if touch_id in self._touch_start_positions:
            start_pos = self._touch_start_positions[touch_id]
            end_pos = self._touch_end_positions.get(touch_id, start_pos)
            start_time = self._touch_input._touch_start_times.get(touch_id, time.time())
            duration = time.time() - start_time
            
            # Detect gestures
            self._detect_and_store_gesture(touch_id, start_pos, end_pos, duration)
        
        self._touch_input.on_touch_up(touch_id)
        if touch_id in self._touch_start_positions:
            del self._touch_start_positions[touch_id]
        if touch_id in self._touch_end_positions:
            del self._touch_end_positions[touch_id]
    
    def on_touch_move(self, touch_id: int, position: Tuple[float, float]) -> None:
        """Handle touch move."""
        self._touch_input.on_touch_move(touch_id, position)
        if touch_id in self._touch_end_positions:
            self._touch_end_positions[touch_id] = position
    
    def _detect_and_store_gesture(
        self,
        touch_id: int,
        start: Tuple[float, float],
        end: Tuple[float, float],
        duration: float
    ) -> None:
        """Detect gesture and store it."""
        gesture = None
        
        # Detect tap
        tap = self._detect_tap(start, end, duration)
        if tap:
            tap.touch_id = touch_id
            gesture = tap
        # Detect swipe
        elif duration < 0.5:  # Swipe must be quick
            swipe = self._detect_swipe(start, end)
            if swipe:
                swipe.touch_id = touch_id
                swipe.duration = duration
                gesture = swipe
        
        if gesture:
            self._gesture_history.append(gesture)
    
    def process(self) -> List[Gesture]:
        """
        Process touches and recognize gestures.
        
        Returns:
            List of recognized gestures
        """
        gestures = self._gesture_history.copy()
        self._gesture_history.clear()
        
        # Detect pinch if multiple touches are moving
        # Pinch detection happens while touches are active
        touches = self._touch_input.get_all_touches()
        if len(touches) >= 2:
            touch_ids = list(touches.keys())
            if len(touch_ids) >= 2:
                pos1 = touches[touch_ids[0]]
                pos2 = touches[touch_ids[1]]
                start1 = self._touch_start_positions.get(touch_ids[0], pos1)
                start2 = self._touch_start_positions.get(touch_ids[1], pos2)
                
                # Check if touches have moved significantly from start
                dx1 = pos1[0] - start1[0]
                dy1 = pos1[1] - start1[1]
                dx2 = pos2[0] - start2[0]
                dy2 = pos2[1] - start2[1]
                
                if abs(dx1) > 5 or abs(dy1) > 5 or abs(dx2) > 5 or abs(dy2) > 5:
                    pinch = self._detect_pinch(start1, start2, pos1, pos2)
                    if pinch:
                        gestures.append(pinch)
        
        return gestures
    
    def _detect_swipe(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float]
    ) -> Optional[Gesture]:
        """Detect swipe gesture."""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance >= self._swipe_threshold:
            direction = (dx / distance, dy / distance)
            return Gesture(
                type=GestureType.SWIPE,
                position=start,
                start_position=start,
                end_position=end,
                distance=distance,
                direction=direction
            )
        return None
    
    def _detect_tap(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        duration: float
    ) -> Optional[Gesture]:
        """Detect tap gesture."""
        # Tap: short duration, small movement
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if duration <= self._tap_max_duration and distance < 10.0:  # Small movement threshold
            return Gesture(
                type=GestureType.TAP,
                position=start,
                start_position=start,
                end_position=end,
                distance=distance,
                duration=duration
            )
        return None
    
    def _detect_pinch(
        self,
        start1: Tuple[float, float],
        start2: Tuple[float, float],
        end1: Tuple[float, float],
        end2: Tuple[float, float]
    ) -> Optional[Gesture]:
        """Detect pinch gesture."""
        # Calculate initial and final distances between two touches
        dx1 = start2[0] - start1[0]
        dy1 = start2[1] - start1[1]
        initial_distance = math.sqrt(dx1 * dx1 + dy1 * dy1)
        
        dx2 = end2[0] - end1[0]
        dy2 = end2[1] - end1[1]
        final_distance = math.sqrt(dx2 * dx2 + dy2 * dy2)
        
        distance_change = abs(final_distance - initial_distance)
        
        if distance_change >= self._pinch_threshold:
            center_x = (end1[0] + end2[0]) / 2
            center_y = (end1[1] + end2[1]) / 2
            return Gesture(
                type=GestureType.PINCH,
                position=(center_x, center_y),
                start_position=((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2),
                end_position=(center_x, center_y),
                distance=distance_change
            )
        return None
    
    def clear_history(self) -> None:
        """Clear gesture history."""
        self._gesture_history.clear()


class InputRemapping:
    """Input remapping system."""
    
    def __init__(self):
        """Initialize input remapping."""
        self._key_to_action: Dict[int, str] = {}
        self._action_to_keys: Dict[str, Set[int]] = {}
        self._button_to_action: Dict[int, str] = {}
        self._action_to_buttons: Dict[str, Set[int]] = {}
        self._axis_to_action: Dict[int, str] = {}
        self._action_to_axes: Dict[str, Set[int]] = {}
    
    def map_key(self, key: int, action: str) -> None:
        """Map key to action."""
        self._key_to_action[key] = action
        
        if action not in self._action_to_keys:
            self._action_to_keys[action] = set()
        self._action_to_keys[action].add(key)
    
    def get_action_for_key(self, key: int) -> Optional[str]:
        """Get action for key."""
        return self._key_to_action.get(key)
    
    def get_keys_for_action(self, action: str) -> Set[int]:
        """Get keys for action."""
        return self._action_to_keys.get(action, set())
    
    def map_button(self, button: int, action: str) -> None:
        """Map button to action."""
        self._button_to_action[button] = action
        
        if action not in self._action_to_buttons:
            self._action_to_buttons[action] = set()
        self._action_to_buttons[action].add(button)
    
    def get_action_for_button(self, button: int) -> Optional[str]:
        """Get action for button."""
        return self._button_to_action.get(button)
    
    def map_axis(self, axis: int, action: str) -> None:
        """Map axis to action."""
        self._axis_to_action[axis] = action
        
        if action not in self._action_to_axes:
            self._action_to_axes[action] = set()
        self._action_to_axes[action].add(axis)
    
    def get_action_for_axis(self, axis: int) -> Optional[str]:
        """Get action for axis."""
        return self._axis_to_action.get(axis)
    
    def clear(self) -> None:
        """Clear all remappings."""
        self._key_to_action.clear()
        self._action_to_keys.clear()
        self._button_to_action.clear()
        self._action_to_buttons.clear()
        self._axis_to_action.clear()
        self._action_to_axes.clear()
    
    def save(self) -> Dict:
        """Save remapping to dictionary."""
        return {
            'keys': {str(k): v for k, v in self._key_to_action.items()},
            'buttons': {str(k): v for k, v in self._button_to_action.items()},
            'axes': {str(k): v for k, v in self._axis_to_action.items()}
        }
    
    def load(self, data: Dict) -> None:
        """Load remapping from dictionary."""
        self.clear()
        
        if 'keys' in data:
            for k, v in data['keys'].items():
                self.map_key(int(k), v)
        
        if 'buttons' in data:
            for k, v in data['buttons'].items():
                self.map_button(int(k), v)
        
        if 'axes' in data:
            for k, v in data['axes'].items():
                self.map_axis(int(k), v)


class InputProfile:
    """Input profile for saving/loading configurations."""
    
    def __init__(self, name: str):
        """Initialize input profile."""
        self.name = name
        self.remapping = InputRemapping()
        self._gamepad_configs: Dict[int, Dict] = {}
    
    def save(self) -> Dict:
        """Save profile to dictionary."""
        return {
            'name': self.name,
            'remapping': self.remapping.save(),
            'gamepad_configs': self._gamepad_configs.copy()
        }
    
    def load(self, data: Dict) -> None:
        """Load profile from dictionary."""
        if 'name' in data:
            self.name = data['name']
        if 'remapping' in data:
            self.remapping.load(data['remapping'])
        if 'gamepad_configs' in data:
            self._gamepad_configs = data['gamepad_configs'].copy()


@dataclass
class InputEvent:
    """Recorded input event."""
    event_type: str
    value: Any
    timestamp: float


class InputRecorder:
    """Input recording system."""
    
    def __init__(self):
        """Initialize input recorder."""
        self._events: List[InputEvent] = []
        self._recording = False
        self._start_time: Optional[float] = None
    
    def start_recording(self) -> None:
        """Start recording."""
        self._recording = True
        self._events.clear()
        self._start_time = time.time()
    
    def stop_recording(self) -> None:
        """Stop recording."""
        self._recording = False
        self._start_time = None
    
    @property
    def is_recording(self) -> bool:
        """Check if recording."""
        return self._recording
    
    def record_key_press(self, key: int, timestamp: Optional[float] = None) -> None:
        """Record key press."""
        if self._recording:
            t = timestamp if timestamp is not None else (time.time() - (self._start_time or 0))
            self._events.append(InputEvent("key_press", key, t))
    
    def record_key_release(self, key: int, timestamp: Optional[float] = None) -> None:
        """Record key release."""
        if self._recording:
            t = timestamp if timestamp is not None else (time.time() - (self._start_time or 0))
            self._events.append(InputEvent("key_release", key, t))
    
    def get_recorded_events(self) -> List[InputEvent]:
        """Get recorded events."""
        return self._events.copy()
    
    def save_to_file(self, filepath: str) -> bool:
        """Save events to file."""
        try:
            data = [
                {
                    'type': e.event_type,
                    'value': e.value,
                    'timestamp': e.timestamp
                }
                for e in self._events
            ]
            with open(filepath, 'w') as f:
                json.dump(data, f)
            return True
        except Exception:
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """Load events from file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self._events = [
                InputEvent(e['type'], e['value'], e['timestamp'])
                for e in data
            ]
            return True
        except Exception:
            return False


class InputReplayer:
    """Input playback system."""
    
    def __init__(self, events: List[InputEvent]):
        """Initialize input replayer."""
        self._events = events
        self._current_index = 0
        self._playing = False
        self._playback_start_time: Optional[float] = None
    
    def start_playback(self) -> None:
        """Start playback."""
        self._playing = True
        self._current_index = 0
        self._playback_start_time = time.time()
    
    def stop_playback(self) -> None:
        """Stop playback."""
        self._playing = False
        self._playback_start_time = None
    
    @property
    def is_playing(self) -> bool:
        """Check if playing."""
        return self._playing
    
    def update(self) -> List[InputEvent]:
        """
        Update playback and return events to replay.
        
        Returns:
            List of events to replay this frame
        """
        if not self._playing or not self._playback_start_time:
            return []
        
        current_time = time.time() - self._playback_start_time
        events_to_replay = []
        
        while (self._current_index < len(self._events) and
               self._events[self._current_index].timestamp <= current_time):
            events_to_replay.append(self._events[self._current_index])
            self._current_index += 1
        
        if self._current_index >= len(self._events):
            self.stop_playback()
        
        return events_to_replay


class InputHint:
    """Visual input hint for tutorials."""
    
    def __init__(
        self,
        text: str,
        position: Tuple[float, float],
        duration_ms: Optional[int] = None
    ):
        """Initialize input hint."""
        self.text = text
        self.position = position
        self.duration_ms = duration_ms
        self._visible = False
        self._show_time: Optional[float] = None
        self.color = (255, 255, 255)
        self.font_size = 16
        self.background_color = (0, 0, 0, 128)  # RGBA
    
    def show(self) -> None:
        """Show hint."""
        self._visible = True
        if self.duration_ms:
            self._show_time = time.time()
    
    def hide(self) -> None:
        """Hide hint."""
        self._visible = False
        self._show_time = None
    
    @property
    def is_visible(self) -> bool:
        """Check if visible."""
        if self._visible and self.duration_ms and self._show_time:
            elapsed = (time.time() - self._show_time) * 1000
            if elapsed >= self.duration_ms:
                self._visible = False
        return self._visible
    
    def set_position(self, position: Tuple[float, float]) -> None:
        """Set hint position."""
        self.position = position
    
    def set_style(self, color: Optional[Tuple[int, int, int]] = None, size: Optional[int] = None) -> None:
        """Set hint style."""
        if color:
            self.color = color
        if size:
            self.font_size = size


class GamepadConfig:
    """Gamepad configuration."""
    
    def __init__(self, gamepad_id: int):
        """Initialize gamepad config."""
        self.gamepad_id = gamepad_id
        self._deadzones: Dict[int, float] = {}
        self._axis_inverted: Dict[int, bool] = {}
        self._button_mappings: Dict[int, str] = {}
    
    def set_deadzone(self, axis: int, deadzone: float) -> None:
        """Set deadzone for axis (0.0 to 1.0)."""
        self._deadzones[axis] = max(0.0, min(1.0, deadzone))
    
    def get_deadzone(self, axis: int) -> float:
        """Get deadzone for axis."""
        return self._deadzones.get(axis, 0.1)  # Default 10%
    
    def set_axis_inverted(self, axis: int, inverted: bool) -> None:
        """Set axis inversion."""
        self._axis_inverted[axis] = inverted
    
    def is_axis_inverted(self, axis: int) -> bool:
        """Check if axis is inverted."""
        return self._axis_inverted.get(axis, False)
    
    def map_button(self, button: int, action: str) -> None:
        """Map button to action."""
        self._button_mappings[button] = action
    
    def get_action_for_button(self, button: int) -> Optional[str]:
        """Get action for button."""
        return self._button_mappings.get(button)
    
    def apply_deadzone(self, axis: int, value: float) -> float:
        """Apply deadzone to axis value."""
        deadzone = self.get_deadzone(axis)
        
        if abs(value) < deadzone:
            return 0.0
        
        # Scale value to account for deadzone
        sign = 1.0 if value >= 0 else -1.0
        scaled = (abs(value) - deadzone) / (1.0 - deadzone)
        return sign * scaled
    
    def apply_inversion(self, axis: int, value: float) -> float:
        """Apply inversion to axis value."""
        if self.is_axis_inverted(axis):
            return -value
        return value


class EnhancedInputManager:
    """Enhanced input manager with advanced features."""
    
    def __init__(self):
        """Initialize enhanced input manager."""
        self._touch_input: Optional[TouchInput] = None
        self._gesture_recognizer: Optional[GestureRecognizer] = None
        self._remapping: Optional[InputRemapping] = None
        self._profiles: Dict[str, InputProfile] = {}
        self._active_profile: Optional[InputProfile] = None
        self._recorders: List[InputRecorder] = []
        self._replayers: List[InputReplayer] = []
        self._hints: List[InputHint] = []
        self._gamepad_configs: Dict[int, GamepadConfig] = {}
        self._action_callbacks: Dict[str, Callable] = {}
        self._action_bindings: Dict[str, Set[int]] = {}
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize input system."""
        if self._initialized:
            return
        
        pygame.joystick.init()
        self._initialized = True
    
    def cleanup(self) -> None:
        """Cleanup input resources."""
        pygame.joystick.quit()
        self._initialized = False
    
    def get_touch_input(self) -> TouchInput:
        """Get or create touch input."""
        if self._touch_input is None:
            self._touch_input = TouchInput()
        return self._touch_input
    
    def get_gesture_recognizer(self) -> GestureRecognizer:
        """Get or create gesture recognizer."""
        if self._gesture_recognizer is None:
            self._gesture_recognizer = GestureRecognizer()
        return self._gesture_recognizer
    
    def get_remapping(self) -> InputRemapping:
        """Get or create input remapping."""
        if self._remapping is None:
            self._remapping = InputRemapping()
        return self._remapping
    
    def create_profile(self, name: str) -> InputProfile:
        """Create input profile."""
        profile = InputProfile(name)
        self._profiles[name] = profile
        return profile
    
    def get_profile(self, name: str) -> Optional[InputProfile]:
        """Get profile by name."""
        return self._profiles.get(name)
    
    def get_profile_for_game(self, game_name: str, profile_name: str) -> InputProfile:
        """Get or create game-specific profile."""
        full_name = f"{game_name}_{profile_name}"
        if full_name not in self._profiles:
            return self.create_profile(full_name)
        return self._profiles[full_name]
    
    def set_active_profile(self, name: str) -> None:
        """Set active profile."""
        profile = self._profiles.get(name)
        if profile:
            self._active_profile = profile
            self._remapping = profile.remapping
    
    @property
    def active_profile(self) -> Optional[InputProfile]:
        """Get active profile."""
        return self._active_profile
    
    def create_recorder(self) -> InputRecorder:
        """Create input recorder."""
        recorder = InputRecorder()
        self._recorders.append(recorder)
        return recorder
    
    def create_replayer(self, events: List[InputEvent]) -> InputReplayer:
        """Create input replayer."""
        replayer = InputReplayer(events)
        self._replayers.append(replayer)
        return replayer
    
    def create_hint(
        self,
        text: str,
        position: Tuple[float, float],
        duration_ms: Optional[int] = None
    ) -> InputHint:
        """Create input hint."""
        hint = InputHint(text, position, duration_ms)
        self._hints.append(hint)
        return hint
    
    def get_gamepad_config(self, gamepad_id: int) -> GamepadConfig:
        """Get or create gamepad config."""
        if gamepad_id not in self._gamepad_configs:
            self._gamepad_configs[gamepad_id] = GamepadConfig(gamepad_id)
        return self._gamepad_configs[gamepad_id]
    
    def get_gamepad_count(self) -> int:
        """Get number of connected gamepads."""
        return pygame.joystick.get_count()
    
    def get_detected_gamepads(self) -> List[Dict]:
        """Get list of detected gamepads."""
        gamepads = []
        count = pygame.joystick.get_count()
        for i in range(count):
            try:
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                gamepads.append({
                    'id': i,
                    'name': joystick.get_name(),
                    'num_axes': joystick.get_numaxes(),
                    'num_buttons': joystick.get_numbuttons()
                })
            except Exception:
                pass
        return gamepads
    
    def get_gamepad_info(self, gamepad_id: int) -> Dict:
        """Get gamepad information."""
        try:
            joystick = pygame.joystick.Joystick(gamepad_id)
            joystick.init()
            return {
                'id': gamepad_id,
                'name': joystick.get_name(),
                'num_axes': joystick.get_numaxes(),
                'num_buttons': joystick.get_numbuttons()
            }
        except Exception:
            return {'id': gamepad_id, 'name': 'Unknown'}
    
    def register_action(self, action: str, key: int) -> None:
        """Register action with key."""
        if action not in self._action_bindings:
            self._action_bindings[action] = set()
        self._action_bindings[action].add(key)
    
    def set_action_callback(self, action: str, callback: Callable) -> None:
        """Set callback for action."""
        self._action_callbacks[action] = callback
    
    def is_action_pressed(self, action: str) -> bool:
        """Check if action is pressed."""
        keys = self._action_bindings.get(action, set())
        pressed = pygame.key.get_pressed()
        return any(pressed[k] for k in keys if k < len(pressed))

