"""Keyboard state and events - Modular."""

from typing import Dict, Set
import pygame


class Keyboard:
    """Manages keyboard input state."""
    
    def __init__(self):
        """Initialize keyboard handler."""
        self._pressed_keys: Set[int] = set()
        self._just_pressed_keys: Set[int] = set()
        self._just_released_keys: Set[int] = set()
        self._key_states: Dict[int, bool] = {}
    
    def update(self, events: list) -> None:
        """
        Update keyboard state from events.
        
        Args:
            events: List of pygame events
        """
        # Clear frame-specific states
        self._just_pressed_keys.clear()
        self._just_released_keys.clear()
        
        # Get current pressed keys
        current_pressed = set(pygame.key.get_pressed())
        was_pressed = self._pressed_keys.copy()
        
        # Detect just pressed and just released
        self._just_pressed_keys = current_pressed - was_pressed
        self._just_released_keys = was_pressed - current_pressed
        
        # Update state
        self._pressed_keys = current_pressed
        
        # Update key states dictionary
        for key in self._just_pressed_keys:
            self._key_states[key] = True
        for key in self._just_released_keys:
            self._key_states[key] = False
    
    def is_pressed(self, key: int) -> bool:
        """
        Check if key is currently pressed.
        
        Args:
            key: pygame key constant
            
        Returns:
            True if key is pressed
        """
        return key in self._pressed_keys
    
    def is_just_pressed(self, key: int) -> bool:
        """
        Check if key was just pressed this frame.
        
        Args:
            key: pygame key constant
            
        Returns:
            True if key was just pressed
        """
        return key in self._just_pressed_keys
    
    def is_just_released(self, key: int) -> bool:
        """
        Check if key was just released this frame.
        
        Args:
            key: pygame key constant
            
        Returns:
            True if key was just released
        """
        return key in self._just_released_keys
    
    def clear(self) -> None:
        """Clear all keyboard state."""
        self._pressed_keys.clear()
        self._just_pressed_keys.clear()
        self._just_released_keys.clear()
        self._key_states.clear()

