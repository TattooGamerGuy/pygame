"""Gamepad/joystick support - Modular."""

from typing import List, Dict, Optional, Tuple
import pygame


class Joystick:
    """Manages gamepad and joystick input."""
    
    def __init__(self):
        """Initialize joystick handler."""
        self._joysticks: List[pygame.joystick.Joystick] = []
        self._axis_values: Dict[int, Dict[int, float]] = {}
        self._button_states: Dict[int, Dict[int, bool]] = {}
        self._hat_states: Dict[int, Dict[int, Tuple[int, int]]] = {}
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize joystick system."""
        if self._initialized:
            return
        
        pygame.joystick.init()
        
        # Detect all connected joysticks
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self._joysticks.append(joystick)
            self._axis_values[i] = {}
            self._button_states[i] = {}
            self._hat_states[i] = {}
        
        self._initialized = True
    
    def cleanup(self) -> None:
        """Cleanup joystick resources."""
        for joystick in self._joysticks:
            joystick.quit()
        self._joysticks.clear()
        self._axis_values.clear()
        self._button_states.clear()
        self._hat_states.clear()
        self._initialized = False
    
    def update(self, events: list) -> None:
        """
        Update joystick state from events.
        
        Args:
            events: List of pygame events
        """
        if not self._initialized:
            return
        
        for joystick_id, joystick in enumerate(self._joysticks):
            # Update axes
            num_axes = joystick.get_numaxes()
            for axis_id in range(num_axes):
                axis_value = joystick.get_axis(axis_id)
                self._axis_values[joystick_id][axis_id] = axis_value
            
            # Update buttons
            num_buttons = joystick.get_numbuttons()
            for button_id in range(num_buttons):
                button_pressed = joystick.get_button(button_id)
                self._button_states[joystick_id][button_id] = button_pressed
            
            # Update hats
            num_hats = joystick.get_numhats()
            for hat_id in range(num_hats):
                hat_value = joystick.get_hat(hat_id)
                self._hat_states[joystick_id][hat_id] = hat_value
    
    def get_axis(self, joystick_id: int, axis_id: int) -> float:
        """
        Get axis value.
        
        Args:
            joystick_id: Joystick index
            axis_id: Axis index
            
        Returns:
            Axis value (-1.0 to 1.0)
        """
        if joystick_id in self._axis_values and axis_id in self._axis_values[joystick_id]:
            return self._axis_values[joystick_id][axis_id]
        return 0.0
    
    def is_button_pressed(self, joystick_id: int, button_id: int) -> bool:
        """
        Check if button is pressed.
        
        Args:
            joystick_id: Joystick index
            button_id: Button index
            
        Returns:
            True if button is pressed
        """
        if joystick_id in self._button_states and button_id in self._button_states[joystick_id]:
            return self._button_states[joystick_id][button_id]
        return False
    
    def get_hat(self, joystick_id: int, hat_id: int) -> Tuple[int, int]:
        """
        Get hat value.
        
        Args:
            joystick_id: Joystick index
            hat_id: Hat index
            
        Returns:
            Hat value tuple (x, y) where each is -1, 0, or 1
        """
        if joystick_id in self._hat_states and hat_id in self._hat_states[joystick_id]:
            return self._hat_states[joystick_id][hat_id]
        return (0, 0)
    
    @property
    def count(self) -> int:
        """Get number of connected joysticks."""
        return len(self._joysticks)
    
    def get_name(self, joystick_id: int) -> Optional[str]:
        """
        Get joystick name.
        
        Args:
            joystick_id: Joystick index
            
        Returns:
            Joystick name or None
        """
        if 0 <= joystick_id < len(self._joysticks):
            return self._joysticks[joystick_id].get_name()
        return None

