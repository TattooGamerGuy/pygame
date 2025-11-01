"""Input handling service."""

from typing import Set, Tuple, Dict, List, Optional
import pygame
import json
import os
import time
from dataclasses import dataclass, field
from hub.events.event_bus import EventBus
from hub.events.events import QuitEvent


@dataclass
class InputAction:
    """Input action definition."""
    name: str
    keys: List[int]
    _pressed: bool = field(default=False, init=False)
    _just_pressed: bool = field(default=False, init=False)
    _just_released: bool = field(default=False, init=False)
    
    def check(self, keys_pressed: Set[int], keys_just_pressed: Set[int], keys_just_released: Set[int]) -> None:
        """Check action state."""
        self._pressed = any(key in keys_pressed for key in self.keys)
        self._just_pressed = any(key in keys_just_pressed for key in self.keys)
        self._just_released = any(key in keys_just_released for key in self.keys)
    
    @property
    def is_pressed(self) -> bool:
        return self._pressed
    
    @property
    def is_just_pressed(self) -> bool:
        return self._just_pressed


@dataclass
class InputCombo:
    """Input combo definition."""
    name: str
    keys: List[int]
    max_time_ms: int = 500
    _pressed: bool = field(default=False, init=False)
    _press_times: Dict[int, float] = field(default_factory=dict, init=False)
    
    def check(self, keys_pressed: Set[int], current_time: float) -> bool:
        """Check if combo is pressed."""
        if not all(key in keys_pressed for key in self.keys):
            self._pressed = False
            return False
        
        for key in self.keys:
            if key not in self._press_times:
                self._press_times[key] = current_time
        
        times = list(self._press_times.values())
        if times:
            time_diff = (current_time - min(times)) * 1000
            if time_diff <= self.max_time_ms:
                self._pressed = True
                return True
        
        self._pressed = False
        return False
    
    def reset(self) -> None:
        self._press_times.clear()
        self._pressed = False


@dataclass
class InputSequence:
    """Input sequence definition."""
    name: str
    keys: List[int]
    max_time_ms: int = 1000
    _current_index: int = field(default=0, init=False)
    _start_time: Optional[float] = field(default=None, init=False)
    _completed: bool = field(default=False, init=False)
    
    def check(self, key_just_pressed: int, current_time: float) -> bool:
        """Check if next key in sequence was pressed."""
        if self._completed:
            return True
        
        if self._current_index == 0 and key_just_pressed == self.keys[0]:
            self._start_time = current_time
            self._current_index = 1
            return False
        
        if self._start_time is not None:
            elapsed = (current_time - self._start_time) * 1000
            if elapsed > self.max_time_ms:
                self._reset()
                return False
        
        if self._current_index < len(self.keys):
            if key_just_pressed == self.keys[self._current_index]:
                self._current_index += 1
                if self._current_index >= len(self.keys):
                    self._completed = True
                    return True
        
        return False
    
    def _reset(self) -> None:
        self._current_index = 0
        self._start_time = None
        self._completed = False
    
    @property
    def is_completed(self) -> bool:
        return self._completed
    
    def reset(self) -> None:
        self._reset()


class InputService:
    """Centralized input handling service."""
    
    def __init__(self, event_bus: EventBus):
        """
        Initialize input service.
        
        Args:
            event_bus: Event bus for publishing input events
        """
        self.event_bus = event_bus
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_pressed: Tuple[bool, bool, bool] = (False, False, False)
        self.mouse_just_clicked: Tuple[bool, bool, bool] = (False, False, False)
        
        # Enhanced features
        self._actions: Dict[str, InputAction] = {}
        self._combos: Dict[str, InputCombo] = {}
        self._sequences: Dict[str, InputSequence] = {}
        self._touch_actions: Dict[str, Tuple[int, int, int, int]] = {}
    
    def update(self, events: list) -> None:
        """
        Update input state from pygame events.
        
        Args:
            events: List of pygame events
        """
        # Reset just-pressed/clicked states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_just_clicked = (False, False, False)
        
        # Update mouse state
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
        
        current_time = time.time()
        
        # Process events
        for event in events:
            if event.type == pygame.QUIT:
                self.event_bus.publish(QuitEvent())
            
            elif event.type == pygame.KEYDOWN:
                if event.key not in self.keys_pressed:
                    self.keys_just_pressed.add(event.key)
                    
                    # Check sequences
                    for sequence in self._sequences.values():
                        sequence.check(event.key, current_time)
                
                self.keys_pressed.add(event.key)
            
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_just_released.add(event.key)
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_index = event.button - 1
                if 0 <= button_index < 3:
                    self.mouse_just_clicked = tuple(
                        i == button_index if i < 3 else False
                        for i in range(3)
                    )
        
        # Update actions
        for action in self._actions.values():
            action.check(self.keys_pressed, self.keys_just_pressed, self.keys_just_released)
        
        # Update combos
        for combo in self._combos.values():
            combo.check(self.keys_pressed, current_time)
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is currently pressed."""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if key was just pressed this frame."""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if key was just released this frame."""
        return key in self.keys_just_released
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return self.mouse_pos
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if mouse button is pressed (0=left, 1=middle, 2=right)."""
        if 0 <= button < 3:
            return self.mouse_pressed[button]
        return False
    
    def is_mouse_button_clicked(self, button: int) -> bool:
        """Check if mouse button was just clicked this frame."""
        if 0 <= button < 3:
            return self.mouse_just_clicked[button]
        return False
    
    # Enhanced features - Action system
    def register_action(self, action_name: str, keys: List[int]) -> None:
        """Register an input action."""
        self._actions[action_name] = InputAction(action_name, keys)
    
    def is_action_registered(self, action_name: str) -> bool:
        """Check if action is registered."""
        return action_name in self._actions
    
    def is_action_pressed(self, action_name: str) -> bool:
        """Check if action is currently pressed."""
        action = self._actions.get(action_name)
        return action.is_pressed if action else False
    
    def is_action_just_pressed(self, action_name: str) -> bool:
        """Check if action was just pressed."""
        action = self._actions.get(action_name)
        return action.is_just_pressed if action else False
    
    def remap_action(self, action_name: str, keys: List[int]) -> None:
        """Remap action to different keys."""
        if action_name in self._actions:
            self._actions[action_name].keys = keys.copy()
        else:
            self.register_action(action_name, keys)
    
    # Combo system
    def register_combo(self, combo_name: str, keys: List[int], max_time_ms: int = 500) -> None:
        """Register an input combo."""
        self._combos[combo_name] = InputCombo(combo_name, keys, max_time_ms)
    
    def is_combo_pressed(self, combo_name: str) -> bool:
        """Check if combo is pressed."""
        combo = self._combos.get(combo_name)
        return combo.is_pressed if combo else False
    
    # Sequence system
    def register_sequence(self, sequence_name: str, keys: List[int], max_time_ms: int = 1000) -> None:
        """Register an input sequence."""
        self._sequences[sequence_name] = InputSequence(sequence_name, keys, max_time_ms)
    
    def is_sequence_completed(self, sequence_name: str) -> bool:
        """Check if sequence is completed."""
        sequence = self._sequences.get(sequence_name)
        return sequence.is_completed if sequence else False
    
    # Touch actions
    def register_touch_action(self, action_name: str, region: Tuple[int, int, int, int]) -> None:
        """Register a touch-based action."""
        self._touch_actions[action_name] = region
        if action_name not in self._actions:
            self.register_action(action_name, [])
    
    # Profile save/load
    def save_profile(self, filepath: str) -> bool:
        """Save input profile."""
        try:
            data = {
                'actions': {name: action.keys for name, action in self._actions.items()},
                'combos': {name: {'keys': combo.keys, 'max_time_ms': combo.max_time_ms} for name, combo in self._combos.items()},
                'sequences': {name: {'keys': seq.keys, 'max_time_ms': seq.max_time_ms} for name, seq in self._sequences.items()},
                'touch_actions': {name: region for name, region in self._touch_actions.items()}
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_profile(self, filepath: str) -> bool:
        """Load input profile."""
        try:
            if not os.path.exists(filepath):
                return False
            with open(filepath, 'r') as f:
                data = json.load(f)
            for name, keys in data.get('actions', {}).items():
                self.register_action(name, keys)
            for name, combo_data in data.get('combos', {}).items():
                self.register_combo(name, combo_data['keys'], combo_data.get('max_time_ms', 500))
            for name, seq_data in data.get('sequences', {}).items():
                self.register_sequence(name, seq_data['keys'], seq_data.get('max_time_ms', 1000))
            for name, region in data.get('touch_actions', {}).items():
                self.register_touch_action(name, tuple(region))
            return True
        except Exception:
            return False

